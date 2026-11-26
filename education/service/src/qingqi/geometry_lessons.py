"""Trusted elementary-school geometry steps from the owner-bound construction."""
from fractions import Fraction

def rational(value):
    exact=Fraction(str(value));simple=exact.limit_denominator(100000)
    return simple if abs(float(simple-exact))<=1e-12*max(1,abs(float(exact))) else exact

def tex(value):
    v=rational(value)
    return str(v.numerator) if v.denominator==1 else ('-' if v<0 else '')+rf'\frac{{{abs(v.numerator)}}}{{{v.denominator}}}'

def helper_labels(labels):
    available=[v for v in 'HKMNGLOPQRSTUVWX' if v not in labels.values()]
    return {'h':available[0],'k':available[1]}

def build(template,p):
    n=p['labels'];A,B,C,D,E,F=(n[k] for k in ('a','b','c','d','e','f'))
    solution=p.get('lesson_mode')=='solution';rotation=template=='triangle_rotation'
    # 用owner的精确分数决定公式和开闭，不能把接近1的比值舍入成1。
    a=Fraction(p['side_exact']) if p.get('side_exact') else rational(p['side'])
    r=Fraction(1) if rotation else Fraction(p['ratio_exact']) if p.get('ratio_exact') else rational(p['ratio'])
    xv=p.get('x_variable','x');yv=p.get('y_variable','y')
    def step(at,title,explanation,formula=''):return {'at':at,'title':title,'explanation':explanation,**({'formula':formula} if formula else {})}
    base={'version':'geometry_lesson_v1','mode':'solution' if solution else 'hint','symbols':{'x':xv,'y':yv}}
    if rotation:
        if not solution:
            if p.get('teaching_mode') in {'heuristic','explain'}:
                steps=[step(0,'读取当前小问的条件',f'{D}为斜边中点，{C}为直角顶点；先把已知条件和待证结论分开。'),
                       step(.2,'连接CD，说明为什么有用',f'直角等腰三角形的斜边中线给出等长与垂直，因此可以选择{D}作旋转中心。',rf'{A}{D}={C}{D},\quad {C}{D}\perp {A}{B}'),
                       step(.4,'把对应边完整转过90度',f'以{D}为中心顺时针转满90度，观察{A}到{C}、{C}到{B}。这是当前步骤的对应关系，最终证明仍留给你完成。',rf'{A}\mapsto {C},\quad {C}\mapsto {B}'),
                       step(1,'回到原题，说明E的像',f'现在对照图中指定射线与垂直条件，说明{E}的像必须满足哪些条件。这里不直接写最后的对应边结论。')]
                return {**base,'steps':steps,'motion_window':[.4,.9],'rotation_fraction':1}
            steps=[step(0,'读中点与直角',f'{D}是斜边中点，{C}是直角顶点。先区分原题给定条件与要证明的结论。'),
                   step(.25,'连接辅助线',f'连接{C}{D}，利用直角等腰三角形的中线性质。观察两条长度相等且互相垂直的线段。',rf'{A}{D}={C}{D},\quad {C}{D}\perp {A}{B}'),
                   step(.6,'预测旋转对应',f'先转动一小段，预测转满90°后{A}、{C}及{E}分别会落在哪里；请自己说明原因。')]
            return {**base,'steps':steps,'motion_window':[.6,1],'rotation_fraction':.25}
        steps=[step(0,'读中点与直角',f'先抓住中点与直角条件。{E}在边内部，{D}{F}垂直{D}{E}，{F}由指定射线确定。',rf'{A}{D}={D}{B},\quad \angle {C}=90^\circ'),
               step(.18,'添加辅助线',f'连接{C}{D}。斜边中点到三个顶点等距；等腰中线垂直斜边，这是选择旋转中心的依据。',rf'{A}{D}={C}{D},\quad {C}{D}\perp {A}{B}'),
               step(.34,'旋转寻找对应',f'以{D}为中心顺时针旋转90°。同时看{A}、{C}的像，边{A}{C}随之转到边{C}{B}。',rf'{A}\mapsto {C},\quad {C}\mapsto {B}'),
               step(.78,'定位对应点',f'{E}的像在{C}{B}上，连线与{D}{E}垂直；这两个条件唯一确定原题的{F}，所以{E}的像就是{F}。',f"{A}'={C},\\quad {C}'={B},\\quad {E}'={F}"),
               step(.9,'对应边得结论',f'旋转保持长度，两组三角形重合。最后把图形对应转成证明，不能只靠示例中的测量数值。',rf'\triangle {A}{D}{E}\cong\triangle {C}{D}{F}\quad\Rightarrow\quad {D}{E}={D}{F}')]
        return {**base,'steps':steps,'motion_window':[.34,.78],'rotation_fraction':1}
    helper=helper_labels(n);H,K=helper['h'],helper['k']
    upper=min(a,2*a*r/(1+r));dx=a/(1+r);dy=a*r/(1+r);intercept=2*a/(1+r);slope=-1/r
    base={**base,'helper_labels':helper,'method':'perpendicular_similarity','coincidence_x':float(dy)}
    if p.get('lesson_goal')=='ratio':
        m=p.get('parameter','m')
        if not solution:
            steps=[step(0,'固定分点比',f'本图取{m}={tex(r)}作示例，先确认{D}的位置。改变{E}时保持这个分点比。'),
                   step(.25,'作垂线找辅助点',f'从{D}向{A}{C}、{B}{C}作垂线，垂足为{H}、{K}。观察两个直角三角形。'),
                   step(.6,'预测相似与比值',f'利用两组垂直关系比较锐角，再判断相似边；若{E}与{H}重合，直接看两条垂距。')]
            if p.get('teaching_mode')=='explain':steps[2]=step(.6,'解释对应锐角为什么相等',f'两组对应边都互相垂直，相当于一起转过同一个直角；角的大小保持不变。比值与最终结论留给你完成。',rf'{D}{H}\perp {D}{K},\quad {D}{E}\perp {D}{F}\\\angle {H}{D}{E}=\angle {K}{D}{F}')
            return {**base,'goal':'ratio','steps':steps,'motion_window':[.25,1],'rotation_fraction':1}
        steps=[step(0,'固定分点比',f'分点比{m}>0是参数。动态图取{m}={tex(r)}作观察例子；后面的证明对任意正{m}成立。',rf'{A}{D}:{D}{B}={m}>0'),
               step(.18,'作垂线找辅助点',f'从{D}向两直角边作垂线，垂足{H}、{K}。两个45°直角三角形给出垂距比与分点比相同。',rf'{D}{H}\perp {A}{C},\quad {D}{K}\perp {B}{C}\\\frac{{{D}{H}}}{{{D}{K}}}=\frac{{{A}{D}}}{{{D}{B}}}={m}'),
               step(.38,'寻找相等的锐角',f'{D}{H}与{D}{K}垂直，{D}{E}与{D}{F}也垂直，所以对应锐角相等。先讨论{E}与{H}不重合的情形。',rf'\angle {D}{H}{E}=\angle {D}{K}{F}=90^\circ\\\angle {H}{D}{E}=\angle {K}{D}{F}'),
               step(.56,'相似得到长度比',f'两组角分别相等，两个直角三角形相似。动点变化时，对应垂距比固定，所以斜边比也固定。',rf'\triangle {D}{H}{E}\sim\triangle {D}{K}{F}\\\frac{{{D}{E}}}{{{D}{F}}}=\frac{{{D}{H}}}{{{D}{K}}}={m}'),
               step(.86,'处理重合并得结论',f'若{E}与{H}重合，{F}也与{K}重合，直接比较垂距，不能使用退化三角形的相似。所有合法位置都得到同一结论。',rf'{E}={H},\;{F}={K}\Rightarrow {D}{E}:{D}{F}={D}{H}:{D}{K}={m}')]
        return {**base,'goal':'ratio','steps':steps,'motion_window':[.56,.86],'rotation_fraction':1}
    if not solution:
        steps=[step(0,'读长度与比例',f'{xv}表示{A}{E}，{yv}表示{B}{F}；确认{E}的活动边和{F}所在的射线。'),
               step(.25,'作垂线观察关系',f'从{D}向两直角边作垂线，垂足{H}、{K}。移动{E}时，{F}仍满足射线与垂直关系。'),
               step(.6,'预测变化趋势',f'观察{xv}增大时{yv}怎样变化。先尝试用相似关系求辅助线段，再检查位置范围。')]
        return {**base,'steps':steps,'motion_window':[.25,1],'rotation_fraction':1}
    function=rf'{yv}={tex(intercept)}-{tex(-slope)}{xv}'
    closed=r'\le' if r<1 else '<'
    steps=[step(0,'读长度与比例',f'{xv}是{A}{E}，{yv}是{B}{F}。{F}在从{B}经过{C}的射线上，允许越过{C}，不是只在{B}{C}线段上。',rf'{A}{C}={B}{C}={tex(a)},\quad {A}{D}:{D}{B}={tex(r)}'),
           step(.18,'作垂线确定长度',f'作垂线，垂足{H}、{K}。利用矩形和45°直角三角形，得{A}{H}={D}{H}、{B}{K}={D}{K}；再用比例和边长求两段长度。',rf'{A}{H}={D}{H}={tex(dy)},\quad {B}{K}={D}{K}={tex(dx)}'),
           step(.38,'分位置列长度关系',f'由相似得{K}{F}=({tex(1/r)}){H}{E}。{E}在{H}靠{A}一侧时，{F}沿{K}向{C}，所以用加法；另一侧用减法。重合时直接取{yv}={B}{K}。',rf'{xv}<{tex(dy)}:\quad {yv}={tex(dx)}+{tex(1/r)}({tex(dy)}-{xv})\\{xv}>{tex(dy)}:\quad {yv}={tex(dx)}-{tex(1/r)}({xv}-{tex(dy)})'),
           step(.56,'观察函数轨迹',f'两种位置的长度关系都化简为同一函数。一起看{E}、{F}移动以及({xv},{yv})轨迹；位置重合时也满足这个式子。',function),
           step(.86,'合并位置范围',f'{E}在边内部不包含两端点；{F}在指定射线上要求{yv}≥0。'+(f'上端点可取，此时{F}与{B}重合。' if r<1 else '两个边端点都不可取，上端点为空心点。'),rf'0<{xv}<{tex(a)},\quad {yv}\ge0\\\Rightarrow\quad 0<{xv}{closed}{tex(upper)}')]
    return {**base,'steps':steps,'motion_window':[.56,.86],'rotation_fraction':1,'domain':{'upper':float(upper),'upper_closed':r<1},'coefficients':{'a':float(slope),'b':float(intercept)}}

def motion_progress(lesson,progress):
    lo,hi=lesson['motion_window']
    return max(0,min(1,(progress-lo)/(hi-lo)))*lesson['rotation_fraction']
