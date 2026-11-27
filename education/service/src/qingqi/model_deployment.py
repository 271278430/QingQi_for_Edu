"""One-time deployment import and shared role identities for the Store model directory."""
import copy,os
from dataclasses import asdict
from .contracts import canonical
from .provider_models import model_config
from .model_options import reasoning_spec

WORKER_ROLES=('course8b','difficulty8b','review27b')
ROLE_NAMES={'glm':'系统文本连接','vision':'系统图片连接','course8b':'课程模型连接','difficulty8b':'学情模型连接','review27b':'审查模型连接'}
DEPLOYMENT_IDS={'glm':'deployment-text','vision':'deployment-vision',**{role:'deployment-'+role for role in WORKER_ROLES}}

def role_ids(selection):
    return {'text':selection.get('text_provider_id'),'vision':selection.get('vision_provider_id'),**selection.get('worker_provider_ids',{})}

def sync(manager):
    with manager.db:
        manager.db.execute('BEGIN IMMEDIATE')
        version,data=manager.read();data=copy.deepcopy(data)
        imports=data.setdefault('deployment_imports',{})
        changed=not data.get('deployment_synced')
        workers=data['selection'].setdefault('worker_provider_ids',{})
        for role,endpoint in manager.defaults.items():
            if role not in DEPLOYMENT_IDS or role in imports:continue
            id=DEPLOYMENT_IDS[role];imports[role]=id;changed=True
            if id not in data['providers']:
                provider={**asdict(endpoint),'id':id,'display_name':ROLE_NAMES[role],'readonly':False,'version':0,'origin':'deployment',
                          'supports_image':bool(endpoint.supports_image if endpoint.supports_image is not None else role=='vision')}
                config=model_config(provider);config['enabled']=endpoint.enabled
                config['optionSpecs']['reasoningLevel']=reasoning_spec(provider)
                provider['models']=[{'key':'main','model':endpoint.model,'config':config}]
                key=os.environ.get(endpoint.key_env,'')
                if key:provider['encrypted_key']=manager.secrets.seal(key)
                elif endpoint.requires_key:provider['credential_ref']=id
                data['providers'][id]=provider
            if role in WORKER_ROLES and role not in workers:workers[role]=id if endpoint.enabled else None
        if changed:
            # 部署文件只负责首次导入；重启不能覆盖用户保存的型号、密钥、用途或已删除连接。
            data['deployment_synced']=True
            body={'request_id':'deployment-sync-v1-'+str(version),'operation':'deployment-sync','roles':sorted(imports)}
            manager._commit(body,version,data)
    return changed
