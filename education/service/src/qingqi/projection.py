"""Student-visible contract; diagnostic results remain in the owned run store."""

def safe_route(route):
    if not route:
        return None
    teaching = route.get("teaching", {})
    return {"intents": route.get("intents", []), "teaching": {key: teaching[key] for key in ("mode", "reason", "allow_final_answer", "label", "display_mode") if key in teaching}}


def project_response(response,state=None):
    if response is None:
        return None
    keys = ("text", "teaching_action", "evidence_refs", "step_refs", "run_id", "controller", "duration_ms", "cache_hit", "model_inference", "tool_calls", "repairs", "visuals", "visual_version", "tutoring_scope")
    result = {key: response[key] for key in keys if key in response}
    route=response.get('route')
    decision=response.get('teaching_decision')
    if route and decision:route={**route,'teaching':{**route.get('teaching',{}),**{k:decision[k] for k in ('label','display_mode','reason') if k in decision}}}
    result["route"] = safe_route(route)
    if result.get('visuals'):
        import re
        # 旧接受消息只修正展示标题与类型措辞；不把静态历史图伪造成一段新动画。
        visuals=[]
        for v in result['visuals']:
            title=v.get('title','')
            repeated=re.match(r'第\s*[（(]?\s*([1-9])\s*[）)]?\s*问\s*[·:：]\s*第\s*[（(]?\s*([1-9])\s*[）)]?\s*问\s*[·:：]\s*',title)
            if repeated and repeated[1]==repeated[2]:title=f'第（{repeated[1]}）问 · '+title[repeated.end():]
            visuals.append({**v,'title':title})
        result['visuals']=visuals
    if not any(v['kind']=='animation_scene' for v in result.get('visuals',[])):
        result['text']=result['text'].replace('；动画用来观察这些关系。','；静态图用于对照这些关系。' if result.get('visuals') else '。')
    if response.get('controller')=='grounded_symbolic_function_v1' and result.get('visuals'):
        from .function_solver import _visuals
        from .animation_teaching import render
        import math
        cubic=next((v for v in result['visuals'] if v.get('params',{}).get('function')=='cubic' and not v.get('params',{}).get('display')),None)
        if cubic:
            p=cubic['params'];k=p.get('a',0);c=p.get('d',0)
            if k>0 and c>0 and math.isclose(p.get('b',0),-1.5*k*(2*c/k)**(1/3),rel_tol=1e-9) and not p.get('c'):
                # 旧已接受曲线只补精确标签，不改原回复、工具账本、模型调用或成绩。
                candidates=_visuals(k,c,'a',p.get('focus_interval',[-1,1]),cubic['basis']);updated=[]
                for v in result['visuals']:
                    q=v.get('params',{});candidate=next((a for a in candidates if a['params']['function']==q.get('function') and all(math.isclose(a['params'].get(t,0),q.get(t,0),abs_tol=1e-9,rel_tol=1e-9) for t in ('a','b','c','d'))),None)
                    if candidate and len(q.get('markers',[]))==len(candidate['params']['display']['markers']):
                        v={**v,'params':{**q,'display':candidate['params']['display']},'caption':candidate['caption']}
                        v={**v,**render(v)}
                    updated.append(v)
                result['visuals']=updated
    if response.get('controller')=='grounded_symbolic_geometry_v1' and result.get('visuals'):
        from .geometry_animation import PARAMS,render
        from .geometry_animation import label_coordinates
        from .contracts import validate,ContractError
        visuals=[]
        for v in result['visuals']:
            if v['kind']=='coordinates':
                import math,re
                args=(state or {}).get('geometry_task',{}).get('arguments',{})
                named=re.search(r'第\s*[（(]?\s*([1-9])\s*[）)]?\s*问',v.get('title','')+' '+(state or {}).get('geometry_question',''))
                part=v.get('teaching_part') or (int(named[1]) if named else (response.get('tutoring_scope') or {}).get('active_part'))
                points=v['points']
                if part==1 and 'midpoint' in args.get('parts',[]) and len(points)==6:
                    A,B,C,D,E,F=points
                    if not math.isclose(D['x'],(A['x']+B['x'])/2,abs_tol=1e-9) or not math.isclose(D['y'],(A['y']+B['y'])/2,abs_tol=1e-9):
                        from .geometry_animation import scene_at
                        side=math.hypot(C['x']-A['x'],C['y']-A['y']);ae=math.hypot(E['x']-A['x'],E['y']-A['y'])
                        points=scene_at('triangle_rotation',{'side':side,'labels':args['labels'],'ae':ae},0)['points'][:6]
                v={**v,'points':label_coordinates(points),'layout':'geometry'}
            if v.get('template') in PARAMS and not v.get('lesson'):
                try:
                    p={**v['params'],'lesson_mode':'solution' if (route or {}).get('teaching',{}).get('allow_final_answer') else 'hint'}
                    validate(p,PARAMS[v['template']])
                    # 旧已接受图示仅升级呈现；保留原ID与正文，不重复推理、工具或成绩提交。
                    v={**v,'params':p,**render(v['template'],p,v['duration']),'caption':'按原题构造逐步观察；图形示意与测量不能代替证明。'}
                except (ContractError,KeyError,ZeroDivisionError,ValueError):pass
            visuals.append(v)
        result['visuals']=visuals
    return result


def project_observations(observations):
    projected = []
    for observation in observations:
        raw = observation["result"]
        # 完整 answer/context/child report 属于内部诊断；白名单投影同时用于即时结果与历史。
        visible = {"evidence": [{key: evidence[key] for key in ("ref", "text", "source")} for evidence in raw.get("evidence", [])]}
        if raw.get("status") in {"correct", "incorrect", "unsupported", "no_steps", "candidate_requires_graph_confirmation"}:
            visible["status"] = raw["status"]
        if "first_error" in raw:
            visible["first_error"] = raw["first_error"]
        # checks只属于数值作答审查；其他工具的验证元数据不能被冒充为学生作答步骤。
        if observation['tool'] in {'review_arithmetic','worker_review27b'} and "checks" in raw:
            visible["checks"] = [{"index": check["index"], "valid": check["valid"]} for check in raw["checks"]]
        projected.append({"tool": observation["tool"], "result": visible})
    return projected
