"""Source-bound subsystem catalogue; the Web client only projects these facts."""
import json
from .architecture_bindings import REPO, P, R, W, verified_bindings
from .architecture_panorama import panorama
from .domain_tools import SPECS
from .visual_teaching import TOOL as VISUAL
from .geometry_solver import TOOL as GEOMETRY
from .function_solver import TOOL as FUNCTION
from .student_task_tools import SPECS as STUDENT_TOOLS
VERSION='source_architecture_v14'

def item(id,title,group,owner,summary,files,interfaces,reuse,limits):
    return {'id':id,'title':title,'group':group,'owner':owner,'summary':summary,
            'description':summary,'files':files,
            'interfaces':interfaces,'reuse':reuse,'limits':limits,
            'status':'configured_optional' if id=='models' else 'implemented',
            'bindings':verified_bindings(id)}

def architecture(deployment):
    modules=[
      item('tutoring','个性化辅导','学生业务','Agent.run + Store当前题资源','自然对话、图片和历史题，沿用同会话原题',
           [P+'agent.py',P+'student_tasks.py',P+'conversation.py',P+'providers.py',P+'tutoring_grounding.py',W+'workspace.tsx',W+'student-task-results.tsx'],
           ['POST /api/teach','POST /api/tutor/images','GET /api/practice/history'],
           ['ZCode消息、附件、工具运行时'],['聊天推断不是已核验学生成绩']),
      item('path','学习路径','学生业务','Store学习快照 + branch_plan','图谱约束与学情驱动的分支路线，选择影响练习',
           [P+'learning_branches.py',P+'learning_evidence.py',W+'learning-route.tsx'],
           ['GET /api/learning','POST /api/learning/route'],
           ['ZCode共享UI与主题'],['共现不是先修，缺少关系时不补造']),
      item('dashboard','学情看板','学生业务','Store学习事件 → learning_projection','首屏摘要、真实知识图谱和独立作答证据',
           [P+'learning.py',P+'learning_evidence.py',P+'learning_map.py',W+'learning-dashboard.tsx'],
           ['GET /api/learning'],['ZCode UI与主题'],
           ['初始画像为估计，未知不等于掌握']),
      item('practice','个性化练习','学生业务','Agent提示 + Store事务 + Catalogue核验','当前路线与动态学情匹配的三题多样性组合',
           [P+'product.py',P+'agent.py',P+'providers.py',P+'tutoring_grounding.py',P+'storage.py',P+'catalogue.py',P+'learning.py',W+'learning.tsx'],
           ['POST /api/practice/start','POST /api/practice/recommendations','POST /api/practice/answer','POST /api/practice/hint'],
           ['ZCode输入与数学消息组件'],['受合格题库供给限制，帮助后成功不伪装独立首次成功']),
      item('permissions','权限管理','安全边界','HTTP Handler + Store准入 + Registry + PermissionService','账户与CSRF、资源归属、管理权限和工具能力边界',
           [P+'product.py',P+'web_store.py',P+'storage.py',P+'tools.py',R+'index.ts'],
           ['Handler.principal/host_ok','WebStore.admit_teaching','Registry.authorize','PermissionService'],
           ['真实复用ZCode PermissionService；Web账户和CSRF由教育服务实现'],
           ['客户端不能授予can_manage，学生内容不能注册工具或扩权']),
      item('loop','Agent Loop','核心系统','Agent.run决策；Store拥有已接受结果','决策 → 调用 → 观察 → 再决策，预算内核验后提交',
           [P+'agent.py',P+'turn_control.py',P+'tutoring_scope.py',P+'planning.py',P+'context.py',P+'storage.py'],
           ['Agent.run','Store.begin/prepare_call/checkpoint/commit/stop_turn','CancellationScope.check','Controller.next'],
           ['ZCode Registry、Executor、Scheduler与Trace'],
           ['教育Loop由Python适配，未原样运行ZCode编码Agent全部功能']),
      item('tools','工具系统','核心系统','Registry授权 + ZCodeRuntime执行','受控本地工具、图谱MCP和8B/27B模型Worker',
           [P+'tools.py',P+'student_task_tools.py',P+'mcp.py',P+'zcode_runtime.py',R+'index.ts'],
           ['Registry.authorize/call','createToolRegistry/createToolExecutor','createMcpAdapter'],
           ['真实复用@zcode/core与@zcode/adapters/mcp'],
           ['固定只读白名单；业务写入由Store命令负责，无任意Shell']),
      item('memory','记忆系统','核心系统','Store唯一可写owner；ZCode有界召回筛选','当前题、临时状态、episode/fact与学习证据分层',
           [P+'storage.py',P+'conversation.py',P+'context.py',P+'math_display.py',R+'memory.ts'],
           ['Store.current_problem/problem_turns/retrieve/commit','math_display.model_history','selectScopedMemory','Store.clear_history'],
           ['ZCode recall合同和筛选预算适配；持久化由教育SQLite实现'],
           ['严格学生隔离与会话题目边界；推断不等于掌握事实']),
      item('routing','意图与教学策略','教学能力','prepare + LayeredRouter + choose + tutoring_scope','按小问拆分多意图；同题模式与会话意图决定教法，许可隔离，学情控制帮助深度',
           [P+'conversation.py',P+'layered_routing.py',P+'request_controls.py',P+'presentation.py',P+'teaching_policy.py',P+'teaching_plan.py',P+'tutoring_scope.py'],
           ['prepare','LayeredRouter.route','request_controls.answer_directives','presentation.resolve','choose/build'],
           ['参考ZCode任务路由与调度设计，教育识别为本项目实现'],
           ['TF-IDF相似度不是校准概率']),
      item('models','模型适配与子Agent','教学能力','Store/ModelSettings配置 + Deployment快照 + JSONModel协议','自选文本/视觉或共享多模态连接，流式导师及受控8B/27B专项任务',
           [P+'product.py',P+'model_settings.py',P+'provider_models.py',P+'providers.py',P+'model_stream.py',P+'workers.py',P+'tutor_images.py',R+'index.ts',W+'model-settings.tsx',W+'provider-editor.tsx',W+'provider-form.ts','packages/ui/src/settings/model-provider-section/ProviderCardSections.tsx'],
           ['generate/generate_text/generate_teaching','make_workers','createExploreSubagentPort'],
           ['直接复用ZCode供应商布局、连接区块、API Key与ModelRow/Metadata编辑器；复用Explore Subagent Port'],
           ['未配置模型不参与调用；配置就绪不等于远端健康，Worker是受限专项任务']),
      item('skills','Skills技能','教学能力','Skills.load + 固定manifest/index','教学指导、内容哈希校验与工具白名单交集',
           [P+'skills.py','education/service/skills/index.json',R+'index.ts'],
           ['Skills.load','createNodeSkillAdapter'],
           ['真实复用ZCode Node Skill Adapter'],
           ['学生题干/图片是数据，不能改Skill或权限']),
      item('visuals','数学与可视化','教学能力','teaching_plan择一；符号工具核验；播放器拥有进度','按当前小问目标选择一张讲解图或一段教学动画',
           [P+'function_solver.py',P+'geometry_solver.py',P+'function_reasoning.py',P+'nonnegative_reasoning.py',P+'identity_animation.py',P+'visual_followup.py',P+'visual_model_contract.py',P+'animation_teaching.py',P+'teaching_visual_pair.py',P+'visual_teaching.py',P+'math_display.py',W+'number-line.tsx',W+'static-reasoning-diagram.tsx',W+'problem-animation.tsx',W+'teaching-animation.tsx',W+'opposite-animation.tsx'],
           ['analyze_function/solve_geometry','visual_followup.plan','visual_model_contract.select','render_teaching_visual','useTeachingAnimation'],
           ['ZCode工具链、Mermaid、图表与Dialog'],
           ['符号题型有明确范围；动画不替代数学证明']),
      item('persistence','持久化与Web接口','基础与运维','Store SQLite事务 + WebStore投影','唯一状态owner、幂等与租约、history epoch和响应投影',
           [P+'storage.py',P+'web_store.py',P+'product.py','education/client/src/http.ts'],
           ['Store.begin/commit','WebStore.detail/admit_teaching','EducationService.get/post'],
           ['参考ZCode单owner、身份与重放边界'],
           ['本机监听127.0.0.1；不在UI另建服务端事实']),
      item('data','教材图谱与题库','基础与运维','Catalogue / Graph只读索引','真实先修/共现、合格题库和保留的初始学情画像',
           [P+'catalogue.py',P+'graph.py',P+'learning_map.py',P+'catalogue_variants.py'],
           ['Catalogue.item/grade','Graph.search/context','learning_projection'],
           ['图谱查询通过ZCode MCP工具执行链'],
           ['两套源用户ID为明确标注的示例初始化；清理不删除源数据']),
      item('web','Web交互与客户端','基础与运维','useEducationWorkspace + 公共HTTP契约','四功能与后台、附件草稿、generation和局部展示状态',
           [W+'use-workspace.ts',W+'workspace.tsx','education/client/src/http.ts','education/client/src/contract.ts'],
           ['useEducationWorkspace','EducationService.get/post/stream','TeachingVisuals'],
           ['ZCode消息、附件、UI、主题与国际化'],
           ['草稿与动画进度不代表服务端事实；只保留Web交互']),
      item('management','设置与管理','基础与运维','Store.system_settings / model_settings / clear_history','产品设置、模型适配、历史清理、运行状态与源码架构',
           [P+'management.py',P+'storage.py',P+'architecture_catalog.py',P+'architecture_details.py',P+'architecture_steps.py',P+'architecture_panorama.py',W+'settings-panel.tsx',W+'architecture-board.tsx',W+'architecture-svg.tsx'],
           ['GET/POST /api/settings','POST /api/settings/history/clear','GET /api/settings/architecture'],
           ['ZCode主题、国际化、Mermaid和Dialog'],
           ['不暴露密钥或跨学生正文；清理只保留无正文的幂等回执']),
    ]
    from .architecture_details import details
    for module in modules:
        if module['id']=='management':
            module['files'] += [W+'architecture-panel.tsx',W+'architecture-module.tsx']
        if module['id']=='models':
            module['description']='用户选择文本/视觉或共享多模态连接；正式适配器负责协议、凭据、流式输出及受控专项模型。'
            module['interfaces'] += ['GET /api/settings/models','GET/POST /api/chat/models','ChatModels.select/resolve_selection','ModelSettings.update_provider/select/resolve','JSONModel.generate_teaching','SecretStore.seal/open']
            module['limits'] += ['API Key不回传浏览器；模型标记与连接测试不等于完整教学效果评测']
            module['files'] += [P+'model_settings.py',P+'provider_models.py',W+'model-settings.tsx',W+'provider-editor.tsx',W+'provider-form.ts',P+'secret_store.py',P+'model_protocol.py',P+'model_stream.py','packages/ui/src/settings/model-provider-section/SectionLayout.tsx','packages/ui/src/settings/model-provider-section/ProviderCardSections.tsx','packages/ui/src/settings/model-provider-section/ProviderFormControls.tsx','packages/ui/src/settings/model-provider-section/ProviderModelMetadataDialog.tsx']
            module['files'] += [P+'chat_models.py',P+'model_options.py',R+'model-options.ts',W+'composer-models.tsx',W+'use-chat-models.ts','packages/ui/src/ModelConfigSelect.tsx','packages/model-option-map/src/compiler.ts']
            module['files'] += ['education/client/src/chat-model-contract.ts']
            module['reuse'] += ['原ModelConfigSelect / ComposerModelMenu / 受限CEL推理参数映射']
        module['scope']=details(module)
        module['files']=list(dict.fromkeys(module['files']))
        module['interfaces']=list(dict.fromkeys(module['interfaces']))
        for file in module['files']:
            if not (REPO/file).is_file():raise ValueError('architecture source missing: '+file)
    hierarchy={'Web交互':['web'],'请求与管理':['permissions','management'],'学生业务':['tutoring','path','dashboard','practice'],'智能体运行':['loop','routing','memory','skills','tools','models','visuals'],'数据与状态':['data','persistence']}
    systems=[{'id':str(i),'title':group,'description':group,'modules':ids} for i,(group,ids) in enumerate(hierarchy.items())]
    for module in modules:
        module['group']=next(group for group,ids in hierarchy.items() if module['id'] in ids)
    skills=json.loads((REPO/'education/service/skills/index.json').read_text(encoding='utf-8'))
    tools=[*SPECS.values(),VISUAL,GEOMETRY,FUNCTION,*STUDENT_TOOLS.values()]
    from .workers import make_workers
    from .providers import JSONModel
    tools += [spec for spec,_ in make_workers({name:JSONModel(e) for name,e in deployment.endpoints.items() if e.enabled}).values()]
    system=panorama(m['id'] for m in modules)
    return {'version':VERSION,'panorama':system,'systems':systems,'modules':modules,
            'tools':[{'name':t.name,'transport':t.transport,'effect':t.effect} for t in tools],
            'skills':[{'id':s['id'],'intents':s['intents']} for s in skills],'models':deployment.status()}
