"""Source-aligned business scope and navigable steps for the sixteen real modules."""
FLOW={
 'tutoring':('文字、原图、历史题与当前问题','按当前小问组织的辅导回复与批准图示','绑定当前题|按小问确定任务|执行教学循环|交付当前问回复','routing,loop,visuals,persistence'),
 'path':('目标、时间、学情、先修图谱和可用题','多链路地图；所选路线影响三题','读取目标与学情|检查真实先修|生成可用路线|保存学生选择','data,persistence,practice'),
 'dashboard':('初始估计、独立作答与帮助事件','学情摘要、图谱与节点依据','读取学习事件|聚合证据与置信度|映射知识图谱|输出摘要与行动','data,memory,persistence'),
 'practice':('所选路线、近期学情、合格题与曝光','每组三题、核对反馈与学习事件','筛选完整同年级题|按学情与路线排序|形成多样三题|核验作答并回流','data,path,tutoring,persistence'),
 'permissions':('身份、来源、资源编号与操作类型','允许执行的有限请求或明确拒绝','确认访问身份|校验Host与CSRF|检查学生资源归属|检查管理与工具权限','management,loop,tools,persistence'),
 'loop':('分问任务、有界上下文、能力和预算','工具观察、已核验回复与规范提交','准入与恢复|构建上下文|决定回复或调用|观察结果再决策|核验候选输出|向Store提交','routing,models,tools,memory,persistence'),
 'routing':('当前输入、原题和同题上下文','小问任务、每问教法、长度和答案许可','预处理原始请求|恢复当前任务|按小问拆意图|确定教法与长度|生成任务及能力集合','memory,skills,loop,models'),
 'models':('已保存连接、会话选模、推理档位与本轮任务','冻结模型客户端；文字、工具动作或识图结果','管理连接与加密凭据|对话框选择模型和档位|点击发送冻结配置|校验版本能力并用ZCode CEL映射|编码文字图片工具并消费增量|校验结果返回观察','management,permissions,persistence,loop'),
 'tools':('Controller动作、原题参数与工具白名单','经Schema核验的工具观察','绑定原题参数|计算能力交集|检查Schema与权限|按DAG执行本地/MCP/Worker|核验返回观察','permissions,skills,data,models,visuals'),
 'memory':('当前题、当前问、同题历史与学习依据','授权且有界的上下文','定位学生与会话|读取原题和当前问|过滤历史候选|按预算召回|提交时写回运行记忆','persistence,data,routing'),
 'skills':('已识别意图与实际注册工具','教学指导与有限工具集合','选择当前教学技能|核对manifest版本与哈希|加载指导内容|限制允许工具','routing,tools,permissions'),
 'visuals':('原题、教学目标和本问答案许可','批准的函数、几何、情景图或动画数据','选择对应数学表达|编译函数/几何/情景|核验原题与披露|随回复保存|按唯一进度呈现','tools,persistence,web'),
 'persistence':('回复提交、学习命令和管理命令','规范会话、学情快照与配置投影','校验命令和版本|建立事务或运行租约|写回复/当前题/事件|保存设置与加密模型配置|返回可重放投影','data'),
 'data':('教材图谱、题库与示例画像来源','只读图谱、合格题库与初始估计','读取已有数学资料|筛选去重并对齐|区分先修和共现|标记题目质量|发布只读索引',''),
 'web':('学生四功能操作、文字图片和设置操作','自然对话、地图、图谱、三题及设置UI','恢复身份与会话|收集文字图片或选择|经公共服务提交|展示临时文字|采用done规范结果|呈现图示与学习页面','permissions,tutoring,path,dashboard,practice,management'),
 'management':('经授权的设置、模型与架构请求','版本化设置回执、模型配置与实际架构说明','校验管理权限|读取或校验版本|执行设置/模型/清理命令|返回当前投影|展示职责与源码架构','permissions,models,persistence'),
}

def details(module):
    source,output,flow,calls=FLOW[module['id']]
    titles=flow.split('|')
    from .architecture_steps import STEPS
    steps=STEPS[module['id']]
    if len(titles)!=len(steps):raise ValueError('architecture step descriptions do not match module flow')
    return {'inputs':[source],'outputs':[output],'responsibilities':[module['description']], 'boundaries':module['limits'],
            'calls':calls.split(',') if calls else [],
            'steps':[{'id':module['id']+'-'+str(i+1),'title':title,'detail':steps[i][0],'interface':steps[i][1]} for i,title in enumerate(titles)]}
