"""Bounded bridge to ZCode's original CEL model-option-map compiler."""
import json,os,shutil,subprocess
from functools import lru_cache
from pathlib import Path
from .contracts import ContractError,canonical

@lru_cache(maxsize=128)
def _compile(source,levels):
    repo=Path(__file__).resolve().parents[4]
    node=os.environ.get('QINGQI_NODE') or (str(repo/'tmp/node24/node.exe') if os.name=='nt' else shutil.which('node'))
    try:
        result=subprocess.run([node,str(repo/'education/runtime/dist/model-options.js')],input=canonical({'map':source,'levels':levels}),capture_output=True,text=True,encoding='utf-8',timeout=8,
                              creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        if result.returncode or len(result.stdout)>64000:raise ValueError('invalid map')
        patches=json.loads(result.stdout)['patches']
        for patch in patches.values():
            if not isinstance(patch,dict) or set(patch)-{'reasoning_effort','thinking'}:raise ValueError('unsupported option')
            if 'reasoning_effort' in patch and (not isinstance(patch['reasoning_effort'],str) or len(patch['reasoning_effort'])>40):raise ValueError('invalid effort')
            if 'thinking' in patch and (not isinstance(patch['thinking'],dict) or set(patch['thinking'])-{'type','budget_tokens'}):raise ValueError('invalid thinking')
            if 'thinking' in patch:
                thinking=patch['thinking']
                if thinking.get('type') not in {'enabled','disabled','adaptive'} or 'budget_tokens' in thinking and (type(thinking['budget_tokens']) is not int or not 0<=thinking['budget_tokens']<=32768):raise ValueError('invalid thinking')
        return canonical(patches)
    except (OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired):raise ContractError('推理档位映射无效，请检查模型能力配置。') from None

def patches(source,levels):
    if not isinstance(source,str) or len(source)>16000 or not isinstance(levels,list) or not 1<=len(levels)<=16 or any(not isinstance(x,str) or not 1<=len(x)<=40 for x in levels) or len(set(levels))!=len(levels):
        raise ContractError('推理档位配置无效。')
    return json.loads(_compile(source,tuple(levels)))

def reasoning_spec(provider):
    spec=provider.get('config',{}).get('optionSpecs',{}).get('reasoningLevel',{'values':['default'],'map':'{}'})
    # 旧配置未声明GLM档位；补齐已验证的三档，避免菜单和实际请求使用不同默认值。
    if provider['protocol']=='openai' and provider['model'].startswith('glm-5.3') and spec=={'values':['default'],'map':'{}'}:
        spec={'values':['low','high','max'],'map':'{"reasoning_effort": reasoningLevel}'}
    return spec

def initial_level(levels):return 'high' if 'high' in levels else levels[-1]
