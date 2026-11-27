"""Session model choices owned by the existing versioned ModelSettings Store."""
from .contracts import ContractError,fingerprint,validate,MODEL_SELECTION_SCHEMA
from .model_settings import ModelSettings
from .model_options import reasoning_spec,initial_level,patches
from .zcode_runtime import RuntimeFailure

class ChatModels(ModelSettings):
    def __init__(self,manager,student,session):
        self.manager=manager;self.student=student;self.session=session
        super().__init__(manager.store,manager.scope+':chat:'+fingerprint({'student':student,'session':session}),manager.defaults)

    def catalogue(self):return self.manager.providers(self.manager.read()[1])

    def read(self):
        row=self.db.execute('SELECT version,data FROM model_settings WHERE scope=?',(self.scope,)).fetchone()
        if row:
            import json
            return row[0],json.loads(row[1])
        providers=self.catalogue();selected=self.manager.read()[1]['selection'];selection={}
        for role,field in [('text','text_provider_id'),('vision','vision_provider_id')]:
            id=selected[field]
            if id:
                p=providers[id];selection[role]={'model_id':id,'model_version':p['version'],'reasoning_level':initial_level(reasoning_spec(p)['values'])}
        return 0,{'selection':selection,'chat_owner':{'student':self.student,'session':self.session}}

    def normalize(self,selection,strict=True):
        validate(selection,MODEL_SELECTION_SCHEMA);providers=self.catalogue();result={}
        for role,choice in selection.items():
            p=providers.get(choice['model_id'])
            if not p or not p['model_enabled'] or not p['model'] or not self.manager.ready(p) or role=='vision' and not p['supports_image']:
                raise RuntimeFailure('model_changed','所选模型已不可用，请在输入框重新选择。')
            if strict and p['version']!=choice['model_version']:raise RuntimeFailure('model_changed','模型配置已更新，请重新读取模型后发送。')
            if choice['reasoning_level'] not in reasoning_spec(p)['values']:raise RuntimeFailure('model_changed','所选推理档位已失效，请重新选择。')
            result[role]={**choice,'model_version':p['version']}
        return result

    def _view(self):
        version,data=self.read();providers=self.catalogue();selection={};issues=[];items=[]
        for role,choice in data['selection'].items():
            try:selection.update(self.normalize({role:choice},strict=False))
            except RuntimeFailure as error:selection[role]=choice;issues.append(str(error))
        for p in providers.values():
            ready=self.manager.ready(p)
            levels=reasoning_spec(p)['values']
            items.append({'id':p['id'],'name':p['model'],'provider_id':p['connection_id'],'provider_label':p['display_name'],'version':p['version'],
                          'supports_image':p['supports_image'],'available':bool(p['model_enabled'] and p['model'] and ready),'levels':levels,'default_level':initial_level(levels)})
        return {'version':version,'session':self.session,'selection':selection,'models':items,'issues':issues}

    def view(self):
        if self.db.in_transaction:return self._view()
        with self.db:
            self.db.execute('BEGIN')
            return self._view()

    def select(self,body):
        if set(body)-{'session','request_id','version','selection'}:raise ContractError('未知对话选模字段。')
        with self.db:
            self.db.execute('BEGIN IMMEDIATE');current=self._admit(body)
            if current is None:return self.view()
            # 只校验本次改动的角色；两个旧模型同时失效时，学生仍能逐个修复，而不被另一角色锁死。
            version,data=current;data['selection']={**data['selection'],**self.normalize(body.get('selection'))}
            self._commit(body,version,data)
        return self.view()

    def initialize(self,selection):
        normalized=self.normalize(selection)
        self._commit({'request_id':'initialize','selection':normalized},0,{'selection':normalized,'chat_owner':{'student':self.student,'session':self.session}})

    def resolve_selection(self,selection=None):
        # 核验身份与构造客户端读取同一配置快照，避免配置并发保存时混用两个版本。
        with self.db:
            self.db.execute('BEGIN')
            return self._resolve_selection(selection)

    def _resolve_selection(self,selection):
        selected=self.normalize(self.view()['selection'] if selection is None else selection);providers=self.catalogue();models={}
        for role,choice in selected.items():
            p=providers[choice['model_id']];spec=reasoning_spec(p)
            patch=patches(spec['map'],spec['values'])[choice['reasoning_level']]
            models['glm' if role=='text' else 'vision']=self.manager.model(p,'glm' if role=='text' else 'vision',patch)
        return models
