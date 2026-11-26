"""Pure response budgets and quality boundaries over actual pedagogical decisions."""
import re
from .contracts import ContractError
from .teaching_goals import concepts,goal
from .visual_tasks import wants_animation,refuses_animation

VERSION='teaching_plan_v5'


def practice_hint_plan(plan):
    # 练习卡片只接收文字提示；沿用对话追问会索要回答，还会生成卡片无法展示的图。
    return {**plan,'goal':'hint','content_style':'brief_hint','interaction_style':'hint_only','allow_final_answer':False,
            'budget':{**plan['budget'],'target_min':30,'target_max':180,'hard_max':400,'questions':0,'hard_questions':0},
            'visual':{**plan['visual'],'delivery':'text','prefer_animation':False,'explicit_animation':False,'forbid_animation':True,'max_outputs':0}}


def build(request,decision,learner=None,problem=None):
    learner=learner or {};problem=problem or {};q=request.question
    purpose=decision.get('goal',goal(q));mode=decision['mode']
    source='catalogue_level' if problem.get('level') else 'concept_structure_estimate'
    problem_text=problem.get('expression','')+' '+q
    related=concepts(problem_text)
    part_count=max(1,len(re.findall(r'[（(][1-9][）)]',problem_text)))
    level=max(1,min(3,int(problem.get('level') or (3 if re.search(r'求证|证明|自变量.*范围',problem_text) or part_count>=3 else 2 if len(related)>1 else 1))))
    p=learner.get('current_topic') or {}
    enough=p.get('recent_independent_attempts',0)>=3
    weak=enough and (p.get('accuracy') or 0)<60
    strong=enough and (p.get('accuracy') or 0)>=80
    lo,hi={'socratic':(60,140),'heuristic':(100,220),'explain':(180,360),'answer':(120,300)}.get(mode,(80,180))
    stepwise=bool(re.search(r'逐步|分步|一步一步|一步步|从头',q))
    content='worked_solution' if mode=='answer' or decision.get('allow_final_answer') and decision.get('full_walkthrough_requested') else 'stepwise' if stepwise else 'micro_explanation' if mode=='explain' or purpose=='concept' else 'brief_hint'
    interaction='direct' if decision.get('no_questions') or mode=='answer' else 'guided_question' if mode=='socratic' else 'independent_try'
    if content=='stepwise' and interaction=='guided_question':lo,hi=120,300+40*(level-1)
    if content=='worked_solution':lo,hi=220,600+180*(level-1)+150*min(3,part_count-1)
    if purpose=='check':lo,hi=80,180
    if mode=='explain':hi+=60*(level-1)+(60 if weak else -40 if strong else 0)
    elif level==3:hi+=40
    short=bool(re.search(r'简短|短一点|短点|一句话|不要.*长|别.*长',q))
    detailed=bool(re.search(r'详细|完整讲解|从头|从基础',q)) and not short
    if short:lo,hi=min(lo,60),min(hi,180)
    if detailed:hi=min(700,hi+180)
    questions=0 if mode=='answer' or decision.get('no_questions') else 1
    template=None
    if purpose=='concept' and '绝对值' in related:template='nonnegative_sum' if '平方根' in related else 'absolute_distance'
    elif purpose=='concept' and '平方根' in related:template='square_root'
    elif re.search('路程|相遇|追及',q):template='travel_motion'
    elif re.search('数轴|加减',q):template='number_line_motion'
    from .function_solver import identify as identify_function
    from .nonnegative_teaching import identify as identify_nonnegative
    from .teaching_visual_pair import choose_delivery,delivery
    visual_delivery,visual_reason=choose_delivery(q)
    if identify_function(problem.get('expression') or q):template='function_reasoning'
    elif identify_nonnegative({'expression':problem_text}):template='nonnegative_reasoning'
    return {'version':VERSION,'goal':purpose,'mode':mode,'content_style':content,'interaction_style':interaction,'difficulty':{'level':level,'source':source,'concepts':related[:6]},
            'support':{'state':'needs_explanation' if weak or purpose=='concept' else 'light_scaffold' if strong else 'unknown_or_current_request',
                       'source':'recent_independent_work' if enough else 'current_request_not_verified_mastery'},
            'budget':{'target_min':lo,'target_max':hi,'hard_max':min(5500,hi+600) if content=='worked_solution' else min(1000,hi+160),'questions':questions,'hard_questions':0 if questions==0 else None,'review_questions':2,'unit':'unicode_characters'},
            'visual':{'recommended_template':template,'prefer_animation':visual_delivery=='animation','explicit_animation':delivery(q)=='animation','forbid_animation':visual_delivery in {'picture','text'},'delivery':visual_delivery,'selection_reason':visual_reason,'max_outputs':1,'optional':True,'selection_basis':'owned_problem_structure' if template in {'function_reasoning','nonnegative_reasoning'} else 'current_concept_or_request'},
            'allow_final_answer':decision['allow_final_answer']}


def explains_concept(text):
    # 真实顶点定义使用“就是最高点/最低点”，固定连接词白名单会误拒绝。
    # 在同一陈述句中核验解释关系；普通“是”还须具有数学主语和数学属性。
    explanation = re.sub(r'\*\*|__|`', '', text)
    statements = [s.strip() for s in re.split(r'(?<=[。！？!?])|\n', explanation)
                  if len(s.strip()) > 8 and not re.search(r'[?？]', s)]
    relation = r'表示|意味着|是指|指的是|称为|叫做|称作|也就是|可以理解为|等于|对应.{0,40}(?:坐标|交点|数值|取值|图象|图像)|满足.{0,40}(?:条件|=)|定义.*是|非负|距离|平方'
    subject = r'函数|顶点|抛物线|零点|坐标|数轴|方程|不等式|分数|分母|分子|平方根|绝对值|有理数|三角形|相反数'
    attribute = r'最高点|最低点|转折点|交点|横坐标|纵坐标|取值|对称|开口|增减|距离|方向|比值|非负|[a-z]\s*(?:\([^)]{1,32}\))?\s*='
    return any(re.search(relation, s) or re.search(
        rf'(?:{subject}).{{0,32}}(?:就是|(?<!不)是|为).{{0,48}}(?:{attribute})', s)
        for s in statements)


def hint_requires_repair(text):
    return bool(re.search(r'[?？]|(?:告诉|回复|发给|反馈给)我|你(?:能|愿意|准备|觉得)|请(?:你)?(?:先)?(?:给出|回答|写出).{0,30}(?:答案|结果|等式)|看这张|如图所示',text))


def validate_text(text,plan,*,bound=False,previous=None,partial=False):
    if plan.get('interaction_style')=='hint_only' and hint_requires_repair(text):
        raise ContractError('practice hint must be declarative and standalone; do not ask for a reply or refer to an undisplayed visual')
    if bound and re.search(r'你希望查询课程|还是根据学习记录获得辅导|请选择.*辅导方式',text):
        raise ContractError('reply ignores the bound problem; answer the current learning question')
    if not partial and plan['goal']=='concept' and not explains_concept(text):
        raise ContractError('concept question needs an actual explanation, not only a question or generic instruction')
    if not partial and plan['goal']=='concept' and not any(len(part.strip())>8 and not re.search(r'[?？]',part) for part in re.split(r'(?<=[。！？!?])|\n',text)):
        raise ContractError('concept question needs declarative explanation before a follow-up question')
    if len(text)>6000:raise ContractError('reply exceeds bounded response transport size')
    outside_math=re.sub(r'\$[^$]*\$|```[\s\S]*?```','',text)
    count=len(re.findall(r'[?？]',outside_math))
    limit=plan['budget'].get('hard_questions',plan['budget']['questions'])
    if limit is not None and count>limit:raise ContractError('student explicitly requested no questions; explain the current point using declarative sentences')
    if not partial and previous and text.strip()==previous.strip() and plan['goal'] in {'concept','step'}:
        raise ContractError('repeated explanation did not address the current difficulty; change example or clarify the current step')


def instructions(plan):
    presentation=plan.get('presentation') or {}
    form=('学生要求用情景故事解释当前题。先给一个简短而完整的场景，明确角色、变量与原题条件的对应，再解释当前一步；故事不能更改符号、定义域或已知条件。不要只回复能否创建故事或重复普通提示。没有匹配的动画模板时用自然文字故事，不声称已经创建动画。' if presentation.get('kind')=='story' else '')
    b=plan['budget']
    if plan.get('interaction_style')=='hint_only':
        return '这是练习页面的一条文字提示，不是教学对话。只给当前题的一条可执行线索和必要依据，约30–180字。不反问，不要求学生回答、汇报或把结果告诉你；不能把问句改成索要回复的陈述句。不透露最终答案。不生成图或动画，不引用没有展示的图。保留原题条件，使用自然中文和精确公式。'
    depth='学生明确授权解答，先给结论和必要的关键推导。' if plan['allow_final_answer'] else '逐步与追问可以组合：本轮只推进当前一步，给必要依据，留一个学生思考任务，保留最终答案。'
    return f"本轮目标={plan['goal']}；内容组织={plan.get('content_style')}；互动方式={plan.get('interaction_style')}。{depth}正文约{b['target_min']}–{b['target_max']}字，最多{b['hard_max']}字；简单问题不用凑字数。追问目标{b['questions']}个；引导时前面用陈述句提供必要依据，只在结尾提出一个思考任务。若问方向，就不要再问长度或未知坐标；不要将同一问题重复改写成多个问句。概念问题先解释，直接模式不反问。使用自然对话，不强制栏目，不重复题干或图示数据；公式和条件保持完整。"+form


def after_visual(plan):
    if plan['content_style']=='worked_solution':return {**plan,'visual_completed':True}
    limit=380 if plan['budget']['target_max']>550 else 260
    target=min(plan['budget']['target_max'],limit)
    # 图示替代部分文字，但 Markdown 和双概念必要说明不应被过窄阈值误拒绝。
    return {**plan,'budget':{**plan['budget'],'target_min':min(80,target),'target_max':target,'hard_max':min(plan['budget']['hard_max'],target+280)},'visual_completed':True}
