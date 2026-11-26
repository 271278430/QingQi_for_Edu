"""Read-only architecture: primary connections only; details live in module maps."""


def node(id,x,y,width,height,*,module_id=None,kind='module',title=None,lines=(),**extra):
    return {'id':id,'x':x,'y':y,'width':width,'height':height,'kind':kind,
            **({'module_id':module_id} if module_id else {}),**({'title':title} if title else {}),'lines':list(lines),**extra}


def edge(id,source,target,points,*,kind='call',label='',label_at=None,heads='end',bridge=None):
    return {'id':id,'source':source,'target':target,'points':points,'kind':kind,'label':label,'heads':heads,
            **({'label_at':label_at} if label_at else {}),**({'bridge':bridge} if bridge else {})}


def diagram(title,nodes,edges,*,width=1160,height=1460,groups=()):
    return {'width':width,'height':height,'title':title,'legend_y':height-54,
            'groups':list(groups),'nodes':nodes,'edges':edges,
            'legend':[{'kind':'call','label':'执行 / 调用'},{'kind':'read','label':'读取 / 投影'},
                      {'kind':'write','label':'命令 / 提交'},{'kind':'constraint','label':'能力约束'}]}


def panorama(module_ids=None):
    nodes=[
      node('web',390,82,360,88,module_id='web',lines=['文字 / 图片 / 历史题 / 四功能操作','浏览器只拥有草稿和展示状态']),
      node('permissions',390,238,360,88,module_id='permissions',lines=['身份 / 来源 / CSRF / 资源归属','在业务执行前完成请求准入']),
      node('management',820,238,270,88,module_id='management',lines=['系统设置 / 模型连接 / 架构','管理操作额外检查角色']),
      node('tutoring',40,414,240,88,module_id='tutoring',lines=['原题与当前问 → 教学任务','多意图与教学模式按问判断']),
      node('path',310,414,240,88,module_id='path',lines=['学情 + 真实先修 + 可练题','多路线地图 / 保存选择']),
      node('dashboard',580,414,240,88,module_id='dashboard',lines=['只读学习快照与证据','摘要 / 学情图谱 / 节点依据']),
      node('practice',850,414,240,88,module_id='practice',lines=['路线 + 学情 + 曝光 → 三题','核验作答 / 原题绑定提示']),
      node('learning-bus',310,539,780,42,kind='compact',title='学习服务：路径 / 看板 / 练习 → Store命令与学习投影'),
      node('loop',365,650,435,370,module_id='loop',kind='frame',lines=['同一任务 / 有界上下文 / 执行预算']),
      node('decision',390,720,385,54,kind='compact',title='决策：候选回复 / 工具动作'),
      node('action',590,820,185,54,kind='process',title='工具调用',lines=['登记编号 / 受控执行']),
      node('observe',590,900,185,54,kind='process',title='观察 → 再决策',lines=['工具结果 / 检查点']),
      node('validation',390,820,170,134,kind='process',title='回复核验',lines=['原题 / 数学 / 许可','失败：预算内修复','预算耗尽：停止']),
      node('accepted',390,976,385,30,kind='compact',title='通过 → Store.commit规范提交'),
      node('routing',40,650,280,88,module_id='routing',lines=['恢复同题模式 / 拆分多意图','生成每问教法、长度和许可']),
      node('memory',40,790,280,88,module_id='memory',lines=['当前题 / 当前问 / episode / fact','同学生同题筛选 / 有界召回']),
      node('skills',40,930,280,88,module_id='skills',lines=['固定manifest / 哈希 / 教学指导','声明工具与Registry取交集']),
      node('tools',850,650,280,88,module_id='tools',lines=['Schema / Registry / 权限检查','本地工具 / MCP / 可选Worker']),
      node('models',850,790,280,88,module_id='models',title='模型适配与子Agent',lines=['文本或视觉型号 / 推理档位','冻结配置 / 协议适配 / 流式推理']),
      node('visuals',850,930,280,88,module_id='visuals',lines=['当前目标 → 一张图或一段动画','精确标签 / 原题与披露核验']),
      node('data',40,1122,300,116,module_id='data',lines=['真实先修 / 共现 / 合格数学题库','Catalogue核验；初始画像带来源','运行时只读，不覆盖源资料']),
      node('persistence',435,1122,350,116,module_id='persistence',lines=['Store是唯一可写状态所有者','会话 / 原题 / 记忆 / 学习事件','设置 / 模型配置 / 租约与调用账本']),
      node('output',435,1290,350,88,kind='terminal',title='学生Web采用规范结果',lines=['对话 / 图示 / 地图 / 学情 / 三题','新的学习行为写回同一个Store'])]
    edges=[edge('web-request','web','permissions',[[570,170],[570,238]]),
      edge('manage-admission','permissions','management',[[750,280],[820,280]]),
      *[edge('dispatch-'+id,'permissions',id,[[570,326],[570,357],[x,357],[x,414]]) for id,x in [('tutoring',160),('path',430),('dashboard',700),('practice',970)]],
      edge('tutor-loop','tutoring','loop',[[160,502],[160,605],[580,605],[580,650]],label='原题教学任务',label_at=[380,597]),
      *[edge('learning-link-'+id,'learning-bus' if id=='dashboard' else id,id if id=='dashboard' else 'learning-bus',[[x,539],[x,502]] if id=='dashboard' else [[x,502],[x,539]],kind='read' if id=='dashboard' else 'call') for id,x in [('path',430),('dashboard',700),('practice',970)]],
      edge('learning-state','learning-bus','persistence',[[1090,560],[1180,560],[1180,1190],[785,1190]],kind='write',heads='both',label='学习命令 / 投影',label_at=[946,1178]),
      edge('route-plan','routing','loop',[[320,696],[365,696]]),
      edge('memory-read','memory','loop',[[320,836],[365,836]],kind='read'),
      edge('skill-capabilities','skills','loop',[[320,976],[365,976]],kind='constraint'),
      edge('tool-call','loop','tools',[[800,696],[850,696]],heads='both'),
      edge('model-call','loop','models',[[800,836],[850,836]],heads='both'),
      edge('visual-call','loop','visuals',[[800,976],[850,976]],heads='both'),
      edge('loop-enter','loop','decision',[[582,708],[582,720]]),
      edge('decide-call','decision','action',[[685,774],[685,820]]),
      edge('call-observe','action','observe',[[685,874],[685,900]]),
      edge('observe-decide','observe','decision',[[775,927],[788,927],[788,747],[775,747]]),
      edge('decide-check','decision','validation',[[475,774],[475,820]],label='候选回复',label_at=[475,804]),
      edge('repair-decide','validation','decision',[[390,887],[377,887],[377,747],[390,747]]),
      edge('check-accepted','validation','accepted',[[475,954],[475,964],[582,964],[582,976]]),
      edge('commit','accepted','persistence',[[582,1006],[582,1122]],kind='write',label='核验通过后提交',label_at=[680,1070]),
      edge('initial-profile','data','persistence',[[340,1170],[435,1170]],kind='read',label='只读资料',label_at=[387,1158]),
      edge('accepted-output','persistence','output',[[610,1238],[610,1290]],kind='read')]
    if module_ids is not None and {n.get('module_id') for n in nodes if n.get('module_id')}!=set(module_ids):
        raise ValueError('系统图与实际模块清单不一致。')
    groups=[{'id':id,'title':title,'x':24,'y':y,'width':1150,'height':h} for id,title,y,h in [
      ('web-layer','01  Web交互',38,154),('admission-layer','02  请求与管理',202,144),
      ('business-layer','03  学生业务',376,214),('agent-layer','04  智能体运行',614,430),
      ('state-layer','05  数据与状态',1084,174)]]
    return diagram('清启教育Agent · 系统关系与Agent Loop',nodes,edges,width=1200,groups=groups)
