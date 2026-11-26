"""Pure per-part intent planning; the Store owns accepted scope and disclosure."""
import re,copy
from dataclasses import replace
from .teaching_policy import choose,LABELS

NUMBERS={str(i):i for i in range(1,10)}|dict(zip('一二三四五六七八九',range(1,10)))
REF=r'第\s*[（(]?\s*([1-9一二三四五六七八九])\s*[)）]?\s*(?:小)?(?:问|题)'

def build(request,source,prior,route,recent,learner=None,prior_mode=None):
    # 函数sin(1)、坐标和算式括号不是小问；只接受题干中的枚举标题形态。
    markers=[NUMBERS[v] for v in re.findall(r'(?<![A-Za-z0-9_])[（(]\s*([1-9一二三四五六七八九])\s*[)）](?=\s*[^\s$=+\-*/^,，;；。)）])',source)]
    available=sorted(set(markers)) if len(set(markers))>=2 else []
    refs=list(re.finditer(REF,request.question))
    old=(prior or {}).get('tutoring_scope') or {}
    if not available and not refs:return None
    if not available:available=[1]
    units=[]
    last_group=0;presentation_prefix=[]
    clauses=re.split(r'[，,。；;\n]|然后|接着|之后|接下来|并且',request.question)
    for clause in clauses:
        matches=list(re.finditer(REF,clause))
        if not matches:
            if re.search(r'下(?:一|个)(?:小)?问',clause):
                last=units[-1][0] if units else old.get('active_part',available[0])
                last_group=len(units)
                units.append((next((p for p in available if p>last),max(available)+1),clause))
            elif units and clause.strip():
                # 逗号后的“配合动画/不要答案/简短一点”仍修饰最近引用组，不能被丢弃。
                for i in range(last_group,len(units)):units[i]=(units[i][0],units[i][1]+'，'+clause)
            elif re.search(r'动画|图|可视化|文字|分步|详细|简短|不要|不用|无需',clause) and not re.search(r'答案|解答|结果',clause):
                presentation_prefix.append(clause)
            continue
        # 并列“第二问和第三问都给答案”共享本句操作；不同操作按引用边界分离。
        shared=bool(len(matches)>1 and re.search(r'都|一起|分别|和|与',clause) and not re.search(r'教学.*答案|答案.*教学|提示.*答案|答案.*提示',clause))
        last_group=len(units)
        for i,m in enumerate(matches):
            text=clause if shared else clause[(0 if i==0 else m.start()):matches[i+1].start() if i+1<len(matches) else len(clause)]
            units.append((NUMBERS[m[1]],text))
    if not units:
        from .request_controls import strip_denied
        whole=r'完整(?:答案|解答|解法)|全部(?:的)?(?:小问|问题|题目|答案)|所有(?:的)?(?:小问|问题|答案)|各问|每一问|三问'
        positive=strip_denied(request.question,whole)[0]
        units=[(p,request.question) for p in available] if re.search(whole,positive) else [(old.get('active_part') if old.get('active_part') in available else available[0],request.question)]
    merged=[]
    for part,text in units:
        if merged and merged[-1][0]==part:merged[-1]=(part,merged[-1][1]+'，'+text)
        else:merged.append((part,text))
    units=merged
    decisions=[]
    for part,text in units:
        q='，'.join([*presentation_prefix,text])
        explicit_answer=bool(re.search(r'答案|解答|结果',q) and re.search(r'给|告诉|回答|公布|只要|只需|完整解答',q) and not re.search(r'不要.{0,8}(?:答案|解答|结果)|不用.{0,8}(?:答案|解答|结果)|别.{0,8}答案',q))
        local=replace(request,question=q,mode='answer' if explicit_answer else request.mode)
        decision=choose(local,route,recent if prior else [],learner=learner,problem={'expression':source},continuing_problem=bool(prior),prior_mode=prior_mode or (prior or {}).get('teaching_mode'),current_part=part,
                        prior_disclosed=part in old.get('answer_parts',[]),prior_no_answer=bool((prior or {}).get('no_final_requested')))
        if explicit_answer:decision.update(reason='学生明确要求此小问的参考解答，许可不传给其他小问。',evidence=[{'source':'current_question_clause','text':text}])
        decisions.append({'part':part,'question':q,'mode':decision['mode'],'label':decision['label'],'allow_final_answer':decision['allow_final_answer'],'teaching':decision})
    active=decisions[-1]['part'] if decisions[-1]['part'] in available else old.get('active_part',available[0])
    return {'version':'scoped_tutoring_v1','available_parts':available,'active_part':active,'units':decisions,
            'clarify':any(u['part'] not in available for u in decisions)}

def public(scope):
    return {k:scope[k] for k in ('version','available_parts','active_part')}|{'units':[{k:u[k] for k in ('part','mode','label','allow_final_answer')} for u in scope['units']]}

class ScopedTutorController:
    """One loop, shared tool observations, independent reply validation per unit."""
    def __init__(self,inner,validate_reply,emit=None):
        self.inner=inner;self.name=inner.name;self.uses_model=inner.uses_model
        # 规则控制器没有远端配置签名；分问包装仍沿用同一控制器身份。
        self.deployment_signature=getattr(inner,'deployment_signature',inner.name);self.validator=validate_reply;self.emit=emit
    def next(self,request,state,context,registry):
        from .planning import reply
        scope=state['tutoring_scope']
        if scope['clarify']:return reply('当前题目包含 '+ '、'.join(f'第（{p}）问' for p in scope['available_parts'])+'，请确认要讨论的小问编号。','clarify')
        completed=state.setdefault('scope_replies',[])
        while len(completed)<len(scope['units']):
            i=len(completed);unit=scope['units'][i];local=copy.copy(state)
            local['route']={**state['route'],'teaching':unit['teaching']};local['teaching_plan']=unit['teaching']['plan']
            local['cursor']=state['cursor']*10+i;local['context']={**context,'content':{**context['content'],'teaching_plan':local['teaching_plan'],'routing':{**context['content'].get('routing',{}),'teaching':unit['teaching']}}}
            q=f'第（{unit["part"]}）问：'+unit['question']
            local['geometry_question']=q;local['function_question']=q
            local['scope_unit']=public(scope)['units'][i]
            local_request=replace(request,question=q,mode=unit['mode'])
            heading=f'**第（{unit["part"]}）问 · {unit["label"]}**\n\n'
            prefix='\n\n'.join(r['text'] for r in completed)+ ('\n\n' if completed else '')+heading
            if self.emit:self.emit({'kind':'scope','scope':public(scope),'part':unit['part'],'prefix':prefix})
            if i==0 and self.inner.name=='grounded_symbolic_geometry_v1' and all(u['allow_final_answer'] for u in scope['units']) and local['teaching_plan']['visual']['prefer_animation'] and not any(o['tool']=='render_teaching_visual' for o in state['observations']):
                # 全题提供对应问的受控候选，Agent择一展示当前问，不能让后续问误用第一问构造。
                local['geometry_question']='；'.join(f'第（{u["part"]}）问：'+u['question'] for u in scope['units'])
            elif i==0 and self.inner.name=='grounded_symbolic_geometry_v1' and any(o['tool']=='solve_geometry' for o in state['observations']) and not any(o['tool']=='render_teaching_visual' for o in state['observations']):
                from .visual_tasks import wants_drawing
                from .contracts import fingerprint
                candidates={}
                for candidate in scope['units']:
                    child=copy.copy(local)
                    child['route']={**local['route'],'teaching':candidate['teaching']};child['teaching_plan']=candidate['teaching']['plan']
                    child['geometry_question']=f'第（{candidate["part"]}）问：'+candidate['question']
                    proposed=self.inner.next(replace(request,question=child['geometry_question']),child,context,registry)
                    if proposed['kind']!='call' or proposed.get('tool')!='render_teaching_visual':continue
                    for figure in proposed['arguments']['visuals']:
                        key=fingerprint({k:v for k,v in figure.items() if k not in {'title','caption','basis'}})
                        candidates[key]=(candidate['part'],wants_drawing(candidate['question']),figure)
                ordered=sorted(candidates.values(),key=lambda v:(not v[1],v[0]))
                explicit=[v for v in ordered if v[1]];automatic=[v for v in ordered if not v[1]]
                selected=(explicit if len(explicit)<=2 else [explicit[0],explicit[-1]])+automatic[:max(0,2-len(explicit))]
                if selected:
                    selected=sorted(selected,key=lambda v:v[0]);state['scoped_visual_parts']=[v[0] for v in selected]
                    return {'kind':'call','tool':'render_teaching_visual','arguments':{'visuals':[v[2] for v in selected]}}
            if self.inner.name=='offline_rules_and_symbolic_v2' and local.get('practice_entry'):
                from .practice_tutoring import reply_for
                action=reply_for(local['practice_entry'],local_request.question,unit['teaching'],local['practice_assessment'])
            else:action=self.inner.next(local_request,local,local['context'],registry)
            if action['kind']=='call':return action
            result=action['reply']
            if unit['mode']=='socratic' and result['teaching_action']=='explain':
                result={**result,'text':result['text']+'\n你能用这个依据推进当前这一步吗？','teaching_action':'ask'}
            self.validator(local_request,local,result)
            completed.append({**result,'text':heading+result['text']})
            if self.emit:self.emit({'kind':'reset','text':'\n\n'.join(r['text'] for r in completed)})
        final=completed[-1]
        return {'kind':'respond','reply':{**final,'text':'\n\n'.join(r['text'] for r in completed),'evidence_refs':list(dict.fromkeys(e for r in completed for e in r['evidence_refs']))}}
