"""Provider connection/model projection shared by settings and inference resolution."""
import copy,re
from .contracts import ContractError

def model_config(provider):
    return {'enabled':provider.get('enabled',True),'properties':{'contextWindow':provider.get('context_window',128000),'inputFormat':{'supportsText':True,'supportsImage':bool(provider.get('supports_image')),'supportsVideo':False,'supportsAudio':False,'supportsPdf':False},'supportsToolCall':provider.get('supports_tools',True),'supportsJsonSchemaOutput':provider.get('json_mode',False)},'optionSpecs':{'maxOutputTokens':{'max':provider.get('max_tokens',1600)},'reasoningLevel':{'values':['default'],'map':'{}'}}}

def definitions(provider):
    return provider.get('models', [{'key':'main','model':provider.get('model',''),'config':model_config(provider)}])

def flatten(provider):
    models=[]
    for definition in definitions(provider):
        config=copy.deepcopy(definition['config']);properties=config.get('properties',{});formats=properties.get('inputFormat',{})
        from .model_options import reasoning_spec
        config.setdefault('optionSpecs',{})['reasoningLevel']=reasoning_spec({**provider,'model':definition['model'],'config':config})
        id=provider['id'] if definition['key']=='main' else provider['id']+'~'+definition['key']
        models.append({**provider,'id':id,'connection_id':provider['id'],'model_key':definition['key'],'model':definition['model'],'config':config,
                       'model_enabled':config.get('enabled',True),'supports_image':formats.get('supportsImage',False),'supports_tools':properties.get('supportsToolCall',True),
                       'json_mode':properties.get('supportsJsonSchemaOutput',False),'max_tokens':config.get('optionSpecs',{}).get('maxOutputTokens',{}).get('max',1600)})
    return models

def validated(values,protocol):
    if not isinstance(values,list) or len(values)>50:raise ContractError('一个供应商最多配置50个模型。')
    result=[];keys=set();names=set()
    for value in values:
        if not isinstance(value,dict) or set(value)-{'key','model','config'}:raise ContractError('模型配置格式无效。')
        key=value.get('key');name=value.get('model');config=copy.deepcopy(value.get('config'))
        if not isinstance(key,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,80}',key) or key in keys:raise ContractError('模型编号无效或重复。')
        if not isinstance(name,str) or not 1<=len(name.strip())<=160 or name.strip() in names:raise ContractError('请填写不重复的模型ID。')
        if not isinstance(config,dict):raise ContractError('模型能力配置需要对象。')
        if set(config)-{'enabled','properties','optionSpecs'}:raise ContractError('未知模型配置字段。')
        properties=config.get('properties',{});options=config.get('optionSpecs',{})
        if not isinstance(properties,dict) or not isinstance(options,dict):raise ContractError('模型配置格式无效。')
        if set(properties)-{'contextWindow','inputFormat','outputFormat','supportsToolCall','supportsJsonSchemaOutput','supportsNativeWebSearch','supportsMidConversationSystem'} or set(options)-{'maxOutputTokens','reasoningLevel'}:raise ContractError('未知模型能力字段。')
        if properties.get('supportsNativeWebSearch') or properties.get('supportsMidConversationSystem'):raise ContractError('当前教学适配器没有启用该模型能力。')
        formats=properties.get('inputFormat',{})
        if not isinstance(formats,dict) or formats.get('supportsText') is not True:raise ContractError('教学模型需要文字输入。')
        if any(formats.get(field) for field in ('supportsAudio','supportsVideo','supportsPdf')):raise ContractError('教学入口当前支持文字和图片。')
        for flag in ('supportsImage',):
            if type(formats.get(flag,False)) is not bool:raise ContractError('图片能力需要布尔值。')
        for flag in ('supportsToolCall','supportsJsonSchemaOutput'):
            if type(properties.get(flag,False)) is not bool:raise ContractError('模型能力需要布尔值。')
        if properties.get('supportsJsonSchemaOutput') and protocol!='openai':raise ContractError('该协议不支持此JSON约束。')
        max_output=options.get('maxOutputTokens',{})
        if not isinstance(max_output,dict):raise ContractError('输出预算配置格式无效。')
        context=properties.get('contextWindow');limit=max_output.get('max')
        if type(context) is not int or not 64<=context<=4_000_000 or type(limit) is not int or not 64<=limit<=min(context,8192):raise ContractError('请检查上下文与输出Token预算。')
        if type(config.get('enabled',True)) is not bool:raise ContractError('启停配置需要布尔值。')
        reasoning=options.get('reasoningLevel',{'values':['default'],'map':'{}'})
        if not isinstance(reasoning,dict) or set(reasoning)-{'values','map'}:raise ContractError('推理档位配置无效。')
        from .model_options import patches
        patches(reasoning.get('map'),reasoning.get('values'))
        result.append({'key':key,'model':name.strip(),'config':config});keys.add(key);names.add(name.strip())
    return result
