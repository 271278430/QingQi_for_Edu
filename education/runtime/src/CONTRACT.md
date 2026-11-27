# 教育后台 ZCode adapter

本轮 RPC 使用整个操作的绝对 deadline，并受整轮剩余预算限制；回调帧不能续期，同一正整数回调编号只执行一次。Store 的停止命令由 Python 临时 CancellationScope 监听，只终止本轮所属 Node/MCP/子任务。close 是独立有界清理，运行时不拥有第二份停止或会话接受队列。见 specs/education/codex-turn-control-v1.md。

固定只读学生工具recommend_practice、preview_learning_path、read_learning_dashboard按当前任务计划执行；Node不持有学情缓存，Python回调读取同一Store。参数不携带学生身份或路径，Owner验证原题引用与本轮请求。完整模型部署的注册上限为16，工具名仍为固定白名单。见specs/education/current-task-tools-v1.md。

函数工具保留精确分数/根式，display元数据只接受当前符号工具批准的图；渲染器仍执行同一个只读schema与调用账本。系统配置是Python Store的运维状态，不在Node持有第二套设置缓存。见specs/education/system-management-v1.md。

analyze_function是固定只读有界函数工具，经原Registry/Executor和账本执行。题干提取参数归Python owner；Node白名单不允许学生新增工具。原函数与导数图来自核验后的批准数据，仍用render_teaching_visual，不创建第二个可写题目缓存。见specs/education/conversation-problem-v2.md。

render_teaching_visual几何模板的lesson_mode由教学Owner绑定，完整步骤仅在allow_final_answer为true时开放；节点不拥有第二套分镜状态。见specs/education/geometry-lessons-v1.md。

solve_geometry是固定只读数学工具，与原工具共用Registry/Executor；工具数量与查询白名单上限12。其参数由Python教学owner绑定，Node只执行已授权调用，不持有几何或学生成绩真相。见specs/education/product-completion-v1.md。

图示v3仍沿唯一 render_teaching_visual 契约注册，新增几何、函数、分区和三种动画数据；点连接的明确计划由Python唯一owner生成并同编号执行，不新建第二条绘图调用路径或可写绘图Agent。见 specs/education/visual-tasks-v3.md。

render_teaching_visual 支持受限 animation_scene；模型只选择模板及有界参数，Python 工具计算关键帧，执行器仍读取同一 oneOf 契约。图示来源或语义参数不合要求由教学 owner 有界修复，不改变权限或扩大能力。见 specs/education/tutoring-evolution.md。

新增固定只读 render_teaching_visual，经现有 Registry/Executor 执行；oneOf 与权限使用上游校验。Python 回调只接受原授权参数，JSON 整数/浮点的等值表示不视作改写，其他字段边界保留。图示结果由 SQLite owner 保存，Node 不持有第二份教学事实。

init.graph_path 是 Python 部署传入的只读索引路径，默认旧 curriculum.sqlite；Node 解析真实路径并约束在 service/data，随后 MCP 只使用该路径。学生请求和工具输出无路径配置权限。数学 Catalogue 与辅导 MCP 因而共享同一索引版本，见 specs/education/student-data.md。

Python owner 发出 init/skills/plan/recall/contracts/call/close；Node 只有本轮执行状态、连接、子任务生命周期和原始执行元数据，不拥有学生会话接受队列或掌握事实。源能力通过 ZCode 公共入口导入。

固定项目 Skills 根和图谱 MCP server；白名单 registry 与上游 Executor 执行能力；专项模型使用上游前台 SubagentPort 的 trace/事件/报告生命周期。回调只有已注册 local/model 名称，参数须与本轮绑定输入相同。不得加载通用 built-in tools、用户插件、全局记忆或全局 Skills。

记忆是 SQLite 授权后的只读投影，复用 manifest 过滤和预算，不创建第二份可写记忆。Node stdout 仅有界协议；输出错误通过稳定 code 传播；close 取消所属执行并等待 MCP 清理。所有子报告仅留在本项目 runs，学生 HTTP 不返回原报告。

教学图标注与响应性能遵循specs/education/visual-discussion-latency-v1.md。Web拥有笔迹草稿和PNG附件；visual_context通过原请求契约携带同会话接受图编号，Store验证并恢复原题，视觉导师直接讨论标注，不把标注作答当作掌握证据。精确坐标标签是输出显示元数据，不回填工具输入；数学依赖在服务就绪前准备，执行deadline不放宽。

model-options入口只调用原@zcode/shared/model-config公开的受限CEL编译器，解析已配置reasoningLevel映射；无模型网络、凭据、教学状态或任意代码执行。Python缓存不可变映射结果，并限制可用于网关的参数键。见specs/education/zcode-composer-model-selection-v1.md。
