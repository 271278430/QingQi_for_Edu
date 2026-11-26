"""Teaching from verified geometry facts; no free-form model proof is trusted."""
import re
from .planning import find,reply
from .contracts import fingerprint
from fractions import Fraction
from .geometry_lessons import tex

def question_part(question,history=()):
    if re.search(r'第\s*[（(]?\s*(?:3|三)',question):return 3
    if re.search(r'第\s*[（(]?\s*(?:2|二)',question):return 2
    if re.search(r'第\s*[（(]?\s*(?:1|一)',question):return 1
    if re.search(r'函数|取值|范围|自变量',question):return 3
    if re.search(r'相似|垂足|锐角|分点比|长度比',question):return 2
    for turn in history:
        previous=turn['request']['question']
        if re.search(r'第\s*[（(]?\s*[123一二三]',previous):return question_part(previous)
    return 1

def answer(report,question,policy,history=()):
    n=report['labels'];A,B,C,D,E,F=(n[k] for k in ('a','b','c','d','e','f'));param=report['parameter'];x=report['x_variable'];y=report['y_variable']
    H,K=(report['elementary_proof']['helpers'][k] for k in ('h','k'))
    part=question_part(question,history)
    if re.search(r'第\s*[（(]?\s*[4-9四五六七八九]',question):return reply('当前题干识别到三个小问，请确认你要讨论的小问编号。','clarify')
    requested_angles=re.findall(r'∠\s*([A-Z]{3})|角\s*([A-Z]{3})',question)
    foot_angles={H+D+E,K+D+F}
    if any((a or b) in foot_angles for a,b in requested_angles) or re.search(r'锐角.*(?:相等|一样)|(?:相等|一样).*锐角',question):
        return reply(f'先讨论非重合位置。${D}{H}\\perp {D}{K}$，同时 ${D}{E}\\perp {D}{F}$；两组对应边各转过直角，所以 $\\angle {H}{D}{E}=\\angle {K}{D}{F}$。这两个锐角随动点变化，并不固定为 $45^\\circ$。若动点与垂足重合，就不使用这两个角来判相似。','explain')
    if re.search(r'重合|退化',question) and re.search(r'相似|为什么|可以|能',question):
        return reply(f'重合时不能按三角形相似来证明。此时 ${E}={H}$、${F}={K}$，所以 ${D}{E}={D}{H}$、${D}{F}={D}{K}$，直接比较两条垂距即可。','explain')
    if requested_angles and part==1:
        known=report['midpoint']['angles'];named=[a or b for a,b in requested_angles]
        values=[f'$\\angle {a}={known[a]}^\\circ$' for a in named if a in known]
        if values:return reply('第（1）问的中点条件下，'+ '，'.join(values)+'。连接'+C+D+'后，中线垂直斜边并平分直角；请区分这两个不同的角。','explain')
    if not policy['allow_final_answer']:
        # 提示历史只用于控制帮助步骤；未经核验的学生文字不能被当成掌握证据。
        stage=min(2,sum(t['response']['teaching_action'] in {'ask','explain'} and question_part(t['request']['question'])==part for t in history))
        if part==1 and 'midpoint' in report['parts']:
            explanation,task=[
                (f'连接 ${C}{D}$：中点条件给出 ${A}{D}={C}{D}$ 和 $\\angle {A}{D}{C}=90^\\circ$。这是观察旋转对应的起点。',f'你能先说明 $\\angle {D}{A}{E}$ 与 $\\angle {D}{C}{F}$ 分别是多少吗？'),
                (f'接下来以 ${D}$ 为中心顺时针旋转 $90^\\circ$，${A}$ 到 ${C}$，${C}$ 到 ${B}$，所以边 ${A}{C}$ 到边 ${C}{B}$。',f'你能说明 ${E}$ 的像为什么同时落在 ${C}{B}$ 上，并与 ${D}{E}$ 的方向垂直吗？'),
                (f'旋转保持到中心 ${D}$ 的距离。${E}$ 的像同时满足“在指定射线上”和“与 ${D}{E}$ 垂直”两个条件，可以用来识别对应点。',f'你能把点的对应关系写清楚，再完成对应边的证明吗？')][stage]
        elif part==3 and 'function' in report['parts']:
            explanation,task=[
                (rf'先从 ${D}$ 向两直角边作垂线，垂足 ${H}$、${K}$。用矩形和45°直角三角形，把题中的比例转成两段垂距之比。',rf'你能先求出 ${A}{H}$ 和 ${B}{K}$ 吗？'),
                (rf'现在看 ${E}$ 在 ${H}$ 的哪一侧。相似关系决定 ${K}{F}$ 与 ${H}{E}$ 的倍率；${F}$ 在 ${K}$ 两侧时，${B}{F}$ 分别用加法或减法。',rf'你能先写出当前这一侧的长度关系吗？'),
                (rf'函数求出后仍要检查位置：${E}$ 在边内部，${F}$ 在指定射线上；重合时直接看两条垂距。',rf'你能把这两组位置限制合并吗？')][stage]
        else:
            explanation,task=[
                (rf'从 ${D}$ 向 ${A}{C}$、${B}{C}$ 作垂线，垂足 ${H}$、${K}$。先看两组45°直角三角形。',rf'你能说明分点比与垂距比为什么相同吗？'),
                (rf'接下来比较 $\triangle {D}{H}{E}$ 与 $\triangle {D}{K}{F}$；两组对应边分别互相垂直。',rf'你能说明两组锐角为什么相等吗？'),
                (rf'两个非退化直角三角形有两组相等的角，就可以写对应边比。若 ${E}={H}$，则应直接比较两条垂距。',rf'你能写出当前情形的对应边关系吗？')][stage]
        guidance=task.replace('你能先','先').replace('你能','试着').rstrip('？?')+'。'
        text=explanation+(guidance if policy.get('no_questions') or policy['mode']!='socratic' else task)
        return reply(text,'explain' if policy.get('no_questions') or policy['mode']=='explain' else 'ask')
    requested=re.findall(r'第\s*[（(]?\s*([123一二三])',question)
    chosen={('midpoint','ratio','function')[int(v)-1] if v.isdigit() else {'一':'midpoint','二':'ratio','三':'function'}[v] for v in requested} if requested else set(report['parts'])
    if not chosen.intersection(report['parts']):return reply('当前识别的题干没有对应小问，请指出具体条件。','clarify')
    if re.search(r'只(?:要|需|需要|给|说).*(?:答案|结果)|不要.*(?:过程|推导)',question):
        results=[]
        if 'midpoint' in chosen:results.append(f'（1）${D}{E}={D}{F}$。')
        if 'ratio' in chosen:results.append(f'（2）${D}{E}:{D}{F}={param}$。')
        if 'function' in chosen:
            p=report['function'];closed='\\le' if p['upper_closed'] else '<'
            results.append(f'（3）${y}={p["expression"]}$，$0<{x}{closed}{p["upper"]}$。')
        return reply('\n\n'.join(results),'give_answer')
    parts=[]
    if 'midpoint' in report['parts'] and 'midpoint' in chosen:
        parts.append(f'**（1）证明等长**\n连接 ${C}{D}$。直角等腰三角形中，斜边中点满足 ${A}{D}={C}{D}$、${C}{D}\\perp {A}{B}$，并平分 $\\angle {C}$。以 ${D}$ 为中心顺时针旋转 $90^\\circ$，${A}$ 到 ${C}$，${C}$ 到 ${B}$，所以线段 ${A}{C}$ 到线段 ${C}{B}$。${E}$ 的像位于 ${C}{B}$，且其连线与 ${D}{E}$ 垂直，正是题目唯一确定的 ${F}$。因此 $\\triangle {A}{D}{E}$ 旋转到 $\\triangle {C}{D}{F}$，对应边 ${D}{E}={D}{F}$。注意 $\\angle {E}{C}{D}=45^\\circ$，不是 $90^\\circ$。')
    if 'ratio' in report['parts'] and 'ratio' in chosen:
        parts.append('\n\n'.join([
            '**（2）一般比值**',
            rf'从 ${D}$ 向 ${A}{C}$、${B}{C}$ 作垂线，垂足为 ${H}$、${K}$。两组45°直角三角形给出 $\frac{{{D}{H}}}{{{D}{K}}}=\frac{{{A}{D}}}{{{D}{B}}}={param}>0$。',
            rf'当 ${E}\ne {H}$ 时，${D}{H}\perp {D}{K}$ 且 ${D}{E}\perp {D}{F}$，对应锐角相等，又有两组直角，所以 $\triangle {D}{H}{E}\sim\triangle {D}{K}{F}$。对应边给出 $$\frac{{{D}{E}}}{{{D}{F}}}=\frac{{{D}{H}}}{{{D}{K}}}={param}.$$',
            rf'若 ${E}={H}$，则 ${F}={K}$，直接比较两条垂距也得到同一结论。故 $\boxed{{{D}{E}:{D}{F}={param}}}$；重合时不能使用退化三角形的相似。']))
    if 'function' in report['parts'] and 'function' in chosen:
        p=report['function'];expression=re.sub(r'\bx\b',x,p['expression']);closed=r'\le' if p['upper_closed'] else '<'
        a=Fraction(p['side']);r=Fraction(p['ratio']);dh=a*r/(1+r);dk=a/(1+r);factor=1/r;upper=tex(Fraction(p['upper']))
        parts.append('\n\n'.join([
            '**（3）函数与范围**',
            rf'沿用垂足 ${H}$、${K}$。矩形和45°直角三角形给出 ${A}{H}={D}{H}={tex(dh)}$、${B}{K}={D}{K}={tex(dk)}$；由相似得 ${K}{F}={tex(factor)}{H}{E}$。',
            rf'若 $0<{x}<{tex(dh)}$，${E}$ 在 ${H}$ 靠 ${A}$ 的一侧，${F}$ 沿 ${K}$ 向 ${C}$，所以 $${y}={B}{K}+{K}{F}={tex(dk)}+{tex(factor)}({tex(dh)}-{x}).$$',
            rf'若 ${x}>{tex(dh)}$，位置转到另一侧，所以 $${y}={B}{K}-{K}{F}={tex(dk)}-{tex(factor)}({x}-{tex(dh)}).$$',
            rf'两式化简相同；${x}={tex(dh)}$ 时 ${E}={H}$、${F}={K}$，直接有 ${y}={tex(dk)}$，也满足 $$\boxed{{{y}={expression}}}.$$',
            rf'${E}$ 在边内部给出 $0<{x}<{tex(a)}$，${F}$ 在指定射线上给出 ${y}\ge0$，合并为 $$\boxed{{0<{x}{closed}{upper}}}.$$' + (rf'上端点可取，此时 ${F}={B}$。' if p['upper_closed'] else '边的端点不包含在动点范围内。')]))
    if not parts:return reply('当前识别的题干没有对应小问，请指出要讨论的具体条件。','clarify')
    return reply('\n\n'.join(parts)+'\n\n上述垂直、长度比和旋转映射已由符号计算核验。','give_answer')

class GeometryTutorController:
    name='grounded_symbolic_geometry_v1'
    uses_model=False
    deployment_signature=fingerprint({'geometry_tutor':'3','solver':'geometry_symbolic_v2'})
    def next(self,request,state,context,registry):
        report=find(state,'solve_geometry')
        if report is None:return {'kind':'call','tool':'solve_geometry','arguments':state['geometry_task']['arguments']}
        q=state['geometry_question'];animation=state['teaching_plan']['visual']['prefer_animation']
        from .teaching_visual_pair import delivery
        # “不要动画”仍可要求静态图，不能把“动画”的画字当成禁止绘图。
        drawing=delivery(q)!='text'
        requested_drawing=bool(re.search(r'画|绘|图示|可视化|图解|连(?:线|接|起来)',q))
        from .visual_tasks import wants_connections
        connecting=wants_connections(q)
        if (animation or drawing) and not find(state,'render_teaching_visual'):
            if animation and not connecting:figures=[v for v in report['approved_visuals'] if v['kind']=='animation_scene']
            else:
                midpoint=question_part(q,state.get('geometry_turns',[]))==1 and 'midpoint' in report['parts']
                choices=[v for v in report['approved_visuals'] if v['kind']=='coordinates' and v['title'].startswith('第（1）问')==midpoint]
                figures=[choices[-1 if re.search(r'连(?:线|接|起来)',q) else 0]]
            if animation and not connecting:
                figures=[v for v in figures if v['template']!='geometry_motion' or set(report['parts'])&{'ratio','function'}]
                requested=re.findall(r'第\s*[（(]?\s*([123一二三])',q)
                if not requested and re.search(r'这(?:一)?(?:小)?问',q):requested=[str(question_part(q,state.get('geometry_turns',[])))]
                templates={'1':'triangle_rotation','一':'triangle_rotation','2':'geometry_motion','二':'geometry_motion','3':'geometry_motion','三':'geometry_motion'}
                chosen={templates[p] for p in requested if p in templates}
                if chosen:figures=[v for v in figures if v['template'] in chosen]
                figures=[{**v,'params':{**v['params'],'lesson_mode':'solution' if policy_answer(state) else 'hint','teaching_mode':state['route']['teaching']['mode']}} for v in figures]
                goal='ratio' if (requested and set(requested)<={'2','二'}) or 'function' not in report['parts'] else 'function'
                figures=[{**v,'params':{**v['params'],'lesson_goal':goal}} if v['template']=='geometry_motion' else v for v in figures]
            return {'kind':'call','tool':'render_teaching_visual','arguments':{'visuals':figures}}
        visual=find(state,'render_teaching_visual')
        from .visual_tasks import wants_explanation
        from .visual_tasks import wants_animation
        # 自动附图不是“只要图示”的请求，仍必须回答学生提出的为什么和当前卡点。
        if (requested_drawing or wants_animation(q)) and not policy_answer(state) and not wants_explanation(q):
            v=next((v for v in visual['visuals'] if v['kind']=='animation_scene'),visual['visuals'][0])
            if v['kind']=='animation_scene':
                if v.get('template')=='coordinate_drawing':return reply(f'教学动画会依次画出 {len(v["geometry"]["segments"])} 条线段，帮助对照点之间的关系。图中动点是符合原题条件的示例位置。','explain')
                topics=' → '.join(step['title'] for step in v.get('lesson',{}).get('steps',[]))
                return reply('教学动画依次展示“'+topics+'”。播放可连续看到结尾，也可以逐步观察；最后的推导仍留给你完成。','explain')
            return reply(f'已画出示意图中的 {len(v.get("points",[]))} 个点和 {len(v.get("segments",[]))} 条真实连线。图中动点是满足原题条件的示例位置，可放大查看。','explain')
        result=answer(report,state['geometry_question'],state['route']['teaching'],state.get('geometry_turns',[]))
        if visual and result['reply']['teaching_action']=='give_answer' and (not state.get('scope_unit') or state['scope_unit']['part']==state['tutoring_scope']['active_part']):
            animations=[v for v in visual['visuals'] if v['kind']=='animation_scene']
            result['reply']['text']+='\n图片标出当前小问的条件；动画逐步展示对应构造与推导依据。' if animations and len(visual['visuals'])>1 else '\n动画逐步展示构造与推导依据。' if animations else '\n静态图用于对照当前小问的点、线与辅助条件。'
        return result

def policy_answer(state):return state['route']['teaching']['allow_final_answer']
