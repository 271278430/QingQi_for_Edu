"""Versioned Provider/ModelSelection facade over the existing Store; views contain no keys."""
from dataclasses import asdict,replace
import base64,io,json,os,re,secrets,time,urllib.request,urllib.parse,urllib.error
from PIL import Image,ImageDraw,ImageFont
from .contracts import ContractError,Denied,canonical,fingerprint
from .providers import Endpoint,JSONModel,NoRedirect
from .secret_store import SecretStore
from .zcode_runtime import RuntimeFailure


def make_image_probe():
    number=str(secrets.randbelow(90000)+10000);image=Image.new('RGB',(260,80),'white')
    ImageDraw.Draw(image).text((20,16),number,fill='black',font=ImageFont.load_default(size=36))
    buffer=io.BytesIO();image.save(buffer,format='JPEG')
    return number,'data:image/jpeg;base64,'+base64.b64encode(buffer.getvalue()).decode()


class ModelSettings:
    def __init__(self,store,scope,defaults):
        self.store=store;self.db=store.db;self.scope=scope;self.defaults=dict(defaults);self.secrets=SecretStore(store.root)
        self.db.executescript('''CREATE TABLE IF NOT EXISTS model_settings(scope TEXT PRIMARY KEY,version INTEGER,data TEXT);
        CREATE TABLE IF NOT EXISTS model_setting_events(scope TEXT,request_id TEXT,payload_hash TEXT,PRIMARY KEY(scope,request_id));
        CREATE TABLE IF NOT EXISTS model_probe_results(scope TEXT,provider_id TEXT,provider_version INTEGER,kind TEXT,data TEXT,PRIMARY KEY(scope,provider_id,kind));''')

    def default_providers(self):
        from .model_deployment import DEPLOYMENT_IDS,ROLE_NAMES
        result={}
        for role,id in DEPLOYMENT_IDS.items():
            e=self.defaults.get(role)
            if e:
                result[id]={**asdict(e),'id':id,'display_name':ROLE_NAMES[role],'readonly':True,'version':0,
                            'supports_image':e.supports_image if e.supports_image is not None else role=='vision'}
        return result

    def sync_deployment(self):
        from .model_deployment import sync
        return sync(self)

    def default_selection(self):
        defaults=self.default_providers()
        text=next((id for id in ('deployment-text','deployment-vision') if defaults.get(id,{}).get('enabled')),None)
        vision='deployment-vision' if defaults.get('deployment-vision',{}).get('enabled') else None
        return {'mode':'shared' if text and text==vision else 'split','text_provider_id':text,'vision_provider_id':vision,'source':'deployment'}

    def read(self):
        row=self.db.execute('SELECT version,data FROM model_settings WHERE scope=?',(self.scope,)).fetchone()
        if row:return row[0],json.loads(row[1])
        return 0,{'providers':{},'selection':self.default_selection()}

    def connections(self,data):return dict(data['providers']) if data.get('deployment_synced') else {**self.default_providers(),**data['providers']}

    def providers(self,data):
        from .provider_models import flatten
        return {model['id']:model for provider in self.connections(data).values() for model in flatten(provider)}

    def credential(self,p):
        if p.get('readonly'):return os.environ.get(p['key_env'],'')
        if p.get('encrypted_key'):return self.secrets.open(p['encrypted_key'])
        if p.get('credential_ref'):
            source=self.default_providers().get(p['credential_ref'])
            data=self.read()[1];stored=data['providers'].get(p['credential_ref'])
            if data.get('deployment_synced') and not stored:raise Denied('deployment credential source removed')
            if stored and stored.get('origin')=='deployment' and stored['id']!=p['id']:source=stored
            if not source or source['base_url'].rstrip('/')!=p['base_url'].rstrip('/') or source['protocol']!=p['protocol']:raise Denied('deployment credential endpoint mismatch')
            if source.get('encrypted_key'):return self.secrets.open(source['encrypted_key'])
            return os.environ.get(source['key_env'],'')
        return ''

    def ready(self,p):
        try:return bool(self.credential(p)) or not p.get('requires_key',True)
        except Denied:return False

    def view(self):
        if self.db.in_transaction:return self._view()
        with self.db:
            self.db.execute('BEGIN')
            return self._view()

    def _view(self):
        from .model_deployment import role_ids
        version,data=self.read();items=[]
        for p in self.providers(data).values():
            public={k:p.get(k) for k in ('id','display_name','model','base_url','protocol','supports_image','supports_tools','requires_key','readonly','version','timeout','max_tokens','json_mode','credential_ref','model_enabled')}
            public['credential_ready']=self.ready(p)
            public['uses']=[role for role,id in role_ids(data['selection']).items() if id==p['id']]
            public['tests']={r[0]:json.loads(r[1]) for r in self.db.execute('SELECT kind,data FROM model_probe_results WHERE scope=? AND provider_id=? AND provider_version=?',(self.scope,p['id'],p['version']))}
            items.append(public)
        from .provider_models import definitions
        connections=[]
        for p in self.connections(data).values():
            connections.append({**{k:p.get(k) for k in ('id','display_name','base_url','protocol','readonly','version','timeout','requires_key','credential_ref')},'origin':p.get('origin','custom'),'credential_ready':self.ready(p),'models':definitions(p)})
        return {'version':version,'scope':self.scope,'providers':items,'connections':connections,'selection':data['selection'],'secret_storage':'本机用户加密；API Key不会回传浏览器'}

    def _admit(self,body):
        if not isinstance(body.get('request_id'),str) or not 1<=len(body['request_id'])<=160 or type(body.get('version')) is not int:raise ContractError('配置需要版本和操作编号。')
        old=self.db.execute('SELECT payload_hash FROM model_setting_events WHERE scope=? AND request_id=?',(self.scope,body['request_id'])).fetchone()
        if old:
            if old[0]!=fingerprint(body):raise RuntimeFailure('settings_conflict','该操作编号已用于另一份模型配置。')
            return None
        version,data=self.read()
        if version!=body['version']:raise RuntimeFailure('settings_conflict','模型配置已更新，请重新读取后保存。')
        return version,data

    def _commit(self,body,version,data):
        self.db.execute('INSERT INTO model_settings VALUES(?,?,?) ON CONFLICT(scope) DO UPDATE SET version=excluded.version,data=excluded.data',(self.scope,version+1,canonical(data)))
        self.db.execute('INSERT INTO model_setting_events VALUES(?,?,?)',(self.scope,body['request_id'],fingerprint(body)))

    def update_provider(self,body):
        if set(body)-{'request_id','version','operation','provider','provider_id'}:raise ContractError('未知模型配置字段。')
        with self.db:
            self.db.execute('BEGIN IMMEDIATE');current=self._admit(body)
            if current is None:return self.view()
            version,data=current;operation=body.get('operation')
            if operation=='delete':
                id=body.get('provider_id')
                if not isinstance(id,str):raise ContractError('请选择自定义连接。')
                if id not in data['providers']:raise ContractError('只能删除自己的自定义连接。')
                if any(selected==id or isinstance(selected,str) and selected.startswith(id+'~') for selected in (data['selection']['text_provider_id'],data['selection']['vision_provider_id'])):raise RuntimeFailure('settings_conflict','请先更换正在使用的模型，再删除连接。')
                from .model_deployment import role_ids
                if any(selected==id or isinstance(selected,str) and selected.startswith(id+'~') for role,selected in role_ids(data['selection']).items() if role not in {'text','vision'}):raise RuntimeFailure('settings_conflict','请先取消或更换该连接的专项用途。')
                del data['providers'][id]
            elif operation=='upsert':
                if not isinstance(body.get('provider'),dict):raise ContractError('连接配置需要对象。')
                p=dict(body.get('provider') or {})
                allowed={'id','display_name','model','models','base_url','protocol','supports_image','supports_tools','requires_key','timeout','max_tokens','json_mode','api_key','key_action','credential_ref'}
                if set(p)-allowed:raise ContractError('未知连接字段。')
                id=p.get('id')
                imported=id in data.get('deployment_imports',{}).values() if isinstance(id,str) else False
                if not isinstance(id,str) or not (re.fullmatch(r'custom-[A-Za-z0-9_-]{1,80}',id) or imported and id in data['providers']):raise ContractError('连接编号无效。')
                prior=data['providers'].get(id,{})
                if not isinstance(p.get('display_name'),str) or not 1<=len(p['display_name'].strip())<=60:raise ContractError('请输入连接名称。')
                if not isinstance(p.get('model',''),str) or len(p.get('model',''))>160:raise ContractError('模型型号过长。')
                p['model']=p.get('model','').strip()
                # 外部配置必须在解析前核对类型，避免数字地址或数组角色触发未处理异常。
                if not isinstance(p.get('base_url'),str) or len(p['base_url'])>2048:raise ContractError('请输入有效的接口地址。')
                p['base_url']=p['base_url'].strip()
                if re.search(r'\s|[\x00-\x1f]',p['base_url']):raise ContractError('接口地址不能含空白或控制字符。')
                try:
                    url=urllib.parse.urlsplit(p['base_url']);url.port
                except ValueError:raise ContractError('接口地址或端口无效。') from None
                if url.scheme not in {'http','https'} or not url.hostname or url.username or url.password or url.query or url.fragment:raise ContractError('接口地址需为http/https，不能包含用户名、查询或片段。')
                if not isinstance(p.get('protocol'),str) or p['protocol'] not in {'openai','anthropic'}:raise ContractError('请选择受支持的接口协议。')
                if 'models' in p:
                    from .provider_models import validated
                    p['models']=validated(p['models'],p['protocol'])
                if not isinstance(p.get('credential_ref',''),str):raise ContractError('部署凭据引用无效。')
                for flag in ('supports_image','supports_tools','requires_key','json_mode'):
                    if type(p.get(flag,False)) is not bool:raise ContractError('模型能力需要布尔标记。')
                if p.get('json_mode') and p['protocol']!='openai':raise ContractError('此JSON模式仅用于OpenAI兼容接口。')
                if type(p.get('timeout')) is not int or not 1<=p['timeout']<=90 or type(p.get('max_tokens')) is not int or not 64<=p['max_tokens']<=8192:raise ContractError('请检查超时与输出预算。')
                action=p.pop('key_action','keep');key=p.pop('api_key','')
                if not isinstance(key,str) or len(key)>4096 or any(c in key for c in '\r\n\0') or not isinstance(action,str) or action not in {'keep','replace','clear'}:raise ContractError('API Key配置无效。')
                p['version']=prior.get('version',0)+1;p['readonly']=False;p['base_url']=p['base_url'].rstrip('/');p['display_name']=p['display_name'].strip()
                for field in ('origin','reasoning_effort','model_options','context_window'):
                    if field in prior:p[field]=prior[field]
                if action=='replace':
                    if not key.strip():raise ContractError('请输入新的API Key。')
                    p['encrypted_key']=self.secrets.seal(key.strip());p.pop('credential_ref',None)
                elif action=='keep':
                    if prior.get('encrypted_key'):p['encrypted_key']=prior['encrypted_key'];p.pop('credential_ref',None)
                    elif prior.get('credential_ref') and not p.get('credential_ref'):p['credential_ref']=prior['credential_ref']
                else:p.pop('credential_ref',None)
                try:self.credential(p)
                except Denied:raise ContractError('凭据引用与当前接口不匹配，请填写此接口的API Key。') from None
                from .provider_models import flatten
                candidates={model['id']:model for model in flatten(p)}
                for role in ('text_provider_id','vision_provider_id'):
                    selected=data['selection'][role]
                    if selected==id or isinstance(selected,str) and selected.startswith(id+'~'):
                        candidate=candidates.get(selected)
                        if not candidate or not candidate['model'] or not candidate['model_enabled'] or p.get('requires_key',True) and not self.credential(p):raise ContractError('正在使用的模型必须保留型号、启用状态与可用凭据。')
                        if role=='vision_provider_id' and not candidate['supports_image']:raise ContractError('请先更换视觉模型，再关闭当前模型的图片能力。')
                for selected in data['selection'].get('worker_provider_ids',{}).values():
                    if selected==id or isinstance(selected,str) and selected.startswith(id+'~'):
                        candidate=candidates.get(selected)
                        if not candidate or not candidate['model_enabled']:raise ContractError('请先取消该型号的专项用途，再移除或关闭型号。')
                data['providers'][id]=p
            else:raise ContractError('未知模型操作。')
            self._commit(body,version,data)
        return self.view()

    def select(self,body):
        if 'role' in body:return self.select_role(body)
        if set(body)-{'request_id','version','mode','text_provider_id','vision_provider_id'}:raise ContractError('未知模型选择字段。')
        with self.db:
            self.db.execute('BEGIN IMMEDIATE');current=self._admit(body)
            if current is None:return self.view()
            version,data=current;mode=body.get('mode')
            if not isinstance(mode,str):raise ContractError('请选择模型分工方式。')
            if mode=='deployment':
                selection=self.default_selection()
                if data.get('deployment_synced'):
                    providers=self.providers(data)
                    text=next((id for id in ('deployment-text','deployment-vision') if providers.get(id,{}).get('model_enabled')),None)
                    vision='deployment-vision' if providers.get('deployment-vision',{}).get('model_enabled') else None
                    selection={'mode':'shared' if text and text==vision else 'split','text_provider_id':text,'vision_provider_id':vision,'source':'deployment'}
            else:
                if mode not in {'split','shared'}:raise ContractError('未知模型分工方式。')
                text=body.get('text_provider_id');vision=body.get('vision_provider_id');providers=self.providers(data)
                if any(id is not None and not isinstance(id,str) for id in (text,vision)):raise ContractError('请选择有效的模型连接。')
                if mode=='shared' and (not text or text!=vision):raise ContractError('共享模式需要选择同一个多模态模型。')
                for id in (text,vision):
                    if id and (id not in providers or not providers[id].get('model') or not providers[id]['model_enabled'] or not self.ready(providers[id])):raise ContractError('请选择已启用且设置型号和凭据的模型。')
                if vision and not providers[vision].get('supports_image'):raise ContractError('视觉角色需要支持图片的模型。')
                selection={'mode':mode,'text_provider_id':text,'vision_provider_id':vision,'source':'custom'}
            selection['worker_provider_ids']=data['selection'].get('worker_provider_ids',{})
            data['selection']=selection;self._commit(body,version,data)
        return self.view()

    def select_role(self,body):
        from .model_deployment import WORKER_ROLES
        if set(body)-{'request_id','version','role','provider_id'}:raise ContractError('未知模型用途字段。')
        role=body.get('role');id=body.get('provider_id')
        if not isinstance(role,str) or role not in {'text','vision',*WORKER_ROLES} or id is not None and not isinstance(id,str):raise ContractError('请选择有效的模型用途。')
        with self.db:
            self.db.execute('BEGIN IMMEDIATE');current=self._admit(body)
            if current is None:return self.view()
            version,data=current;p=self.providers(data).get(id)
            if id and (not p or not p['model_enabled'] or not p['model'] or not self.ready(p)):raise ContractError('请选择已启用且具有可用凭据的型号。')
            if id and role=='vision' and not p['supports_image']:raise ContractError('图片用途需要图片输入能力。')
            # 单角色命令只改当前用途，另一旧角色失效时仍可逐个修复，不制造第二套角色草稿。
            selection=data['selection']
            if role in WORKER_ROLES:selection.setdefault('worker_provider_ids',{})[role]=id
            else:selection['text_provider_id' if role=='text' else 'vision_provider_id']=id
            selection['mode']='shared' if selection['text_provider_id'] and selection['text_provider_id']==selection['vision_provider_id'] else 'split'
            selection['source']='custom';self._commit(body,version,data)
        return self.view()

    def model(self,p,role,options=None):
        url=urllib.parse.urlsplit(p['base_url']);key=self.credential(p)
        # 自定义模型分工仍要保留部署的推理档位，不能重建Endpoint时悄悄退回供应商默认值。
        endpoint=Endpoint(name=role,base_url=p['base_url'],model=p['model'],key_env='provider:'+p['id']+':'+str(p['version']),protocol=p['protocol'],enabled=True,allowed_hosts=(url.hostname,),
                          timeout=p.get('timeout',30),max_tokens=p.get('max_tokens',1200),reasoning_effort=p.get('reasoning_effort',''),model_options=p.get('model_options',{}),json_mode=p.get('json_mode',False),supports_image=p.get('supports_image',False),supports_tools=p.get('supports_tools',True),requires_key=p.get('requires_key',True),context_window=p.get('config',{}).get('properties',{}).get('contextWindow',128000))
        if options is not None:endpoint=replace(endpoint,reasoning_effort='' if options else endpoint.reasoning_effort,model_options=options)
        return JSONModel(endpoint,credential=lambda:key)

    def resolve(self):
        if self.db.in_transaction:return self._resolve()
        with self.db:
            self.db.execute('BEGIN')
            return self._resolve()

    def _resolve(self):
        version,data=self.read()
        if not data.get('deployment_synced') and data['selection'].get('source')=='deployment':return None
        providers=self.providers(data);models={}
        from .model_deployment import role_ids
        for role,id in role_ids(data['selection']).items():
            p=providers.get(id)
            if p and p['model_enabled'] and p['model'] and self.ready(p):models['glm' if role=='text' else role]=self.model(p,'glm' if role=='text' else role)
        return models

    def discover(self,id):
        version,data=self.read();p=self.connections(data).get(id)
        if not p:raise ContractError('连接不存在。')
        if not self.ready(p):raise ContractError('请先配置有效的API Key或凭据引用。')
        key=self.credential(p)
        if p.get('requires_key',True) and not key:raise ContractError('请先设置API Key。')
        headers={'Accept':'application/json'}
        if key:headers.update({'Authorization':'Bearer '+key} if p['protocol']=='openai' else {'x-api-key':key,'anthropic-version':'2023-06-01'})
        request=urllib.request.Request(p['base_url'].rstrip('/')+'/models',headers=headers)
        try:
            with urllib.request.build_opener(NoRedirect(),urllib.request.ProxyHandler({})).open(request,timeout=min(p.get('timeout',10),10)) as response:raw=response.read(128001)
            if len(raw)>128000:raise ContractError('型号列表过大。')
            envelope=json.loads(raw)
            if not isinstance(envelope,dict):raise ContractError('型号列表格式不兼容。')
            values=envelope.get('data',[])
            if not isinstance(values,list):raise ContractError('型号列表格式不兼容。')
            models=[]
            for m in values[:250]:
                if not isinstance(m,dict) or not isinstance(m.get('id'),str):continue
                modalities=m.get('input_modalities') or m.get('input_format') or []
                image=m.get('supports_image') if isinstance(m.get('supports_image'),bool) else 'image' in modalities if isinstance(modalities,list) else None
                models.append({'id':m['id'][:160],'supports_image':image})
            return {'models':models,'message':'未知图片能力的型号需按服务文档设置并测试。'}
        except (urllib.error.HTTPError,urllib.error.URLError,ValueError,TimeoutError) as error:raise RuntimeFailure('model_discovery_failed','无法读取型号列表；连接已保留，可以手动填写服务支持的型号。') from error

    def test(self,id,kind):
        version,data=self.read();p=self.providers(data).get(id)
        if not p or not p.get('model') or not isinstance(kind,str) or kind not in {'text','vision'}:raise ContractError('请选择型号与测试类型。')
        if not self.ready(p):raise ContractError('请先配置有效的API Key或凭据引用。')
        if kind=='vision' and not p.get('supports_image'):raise ContractError('该连接没有声明图片输入能力。')
        model=self.model(p,'probe');model.endpoint=replace(model.endpoint,timeout=min(20,model.endpoint.timeout),max_tokens=min(512,model.endpoint.max_tokens))
        try:
            if kind=='vision':
                number,image=make_image_probe();text=model.generate_text('你正在测试图片识别能力。只返回图片中的整数，不要解释。',{'task':'读取图中整数'},images=[image]);ok=number in text
            else:text=model.generate_text('你正在测试模型接口。请简短回复OK。',{'task':'连接测试'});ok=bool(text.strip())
            result={'success':ok,'tested_at':time.time(),'message':'图像识别测试通过。' if ok and kind=='vision' else '文本连接测试通过。' if ok else '接口已响应，但未正确识别测试图片。'}
        except (RuntimeFailure,ContractError,Denied) as error:result={'success':False,'tested_at':time.time(),'message':'模型测试失败，请检查型号、协议、API Key和服务可用性。','code':getattr(error,'code','model_test_failed')}
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            current=self.providers(self.read()[1]).get(id)
            if not current or current['version']!=p['version']:return {'success':False,'stale':True,'tested_at':time.time(),'message':'测试期间模型配置已更新，请测试当前版本。'}
            self.db.execute('INSERT INTO model_probe_results VALUES(?,?,?,?,?) ON CONFLICT(scope,provider_id,kind) DO UPDATE SET provider_version=excluded.provider_version,data=excluded.data',(self.scope,id,p['version'],kind,canonical(result)))
        return result
