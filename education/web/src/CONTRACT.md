# 教育学习工作台

数轴布局由NumberLine根据实际宽度确定短编号和独立说明行，不改变已批准数学位置。原题数值由后端保留，未知长小数才作近似显示；短编号及完整标签仍进入标注快照和所属图示引用。完整解答与重画属于同轮两个目标，图示回执不能遮盖答案。见specs/education/current-intent-and-number-line-v1.md。

相反数动画读取服务端批准帧，播放器连续到末尾、前后按钮沿关键阶段，刷新采用同一规范历史。旧截断消息重新回答以新编号发送，不能修改旧失败记录。见specs/education/owned-visual-followup-v1.md。

生成中及刷新后的运行消息可通过原 EducationService 停止本轮；原请求引用与 generation/selection 保护迟到回包。读取服务端终态后确认停止，保留未完成文字与输入。见 specs/education/codex-turn-control-v1.md。

ComposerModels直接复用ZCode原ModelConfigSelect和推理滑条；useChatModels只保留Store接受选择的投影与未确认操作。新会话默认high，已存low不覆盖。点击发送前冻结模型和档位；图片上传与运行中预选不改变本轮。刷新/切会话读取Owner，失效配置锁发送并保留输入，见specs/education/zcode-composer-model-selection-v1.md。

solid整理：教育界面为完整中文；会话读取锁定输入并原子更新题目/预填草稿；学习三页共享一个生命周期且成功提示不跨页保留；设置由版本协调读取/保存并在子页卸载后通知工作区；非JSON代理失败保留原命令。见specs/education/product-solid-review-v1.md与47组验收清单。

v8模型设置直接调用ZCode供应商布局、连接、API Key、ModelRowInput、ModelMetadataDialog与原草稿校验。连接拥有凭据，嵌套models拥有能力和预算，角色选择具体模型。Store拥有接受的配置，UI保留草稿和未确认命令。新保存结果受版本保护，旧读取不能回滚。模块图采用统一五层与实际分支，episode提交和受信fact确认分别表示。见specs/education/zcode-model-settings-v8.md。

模型适配沿同一EducationService。UI只保存未提交草稿，Key输入在保存/关闭后清空；不使用localStorage保存密钥。版本化配置由Store拥有，保存后刷新模型能力与设置投影；新请求使用新配置，旧未完成请求收到model_changed时保留输入。ZCode改名草稿中未定义的能力不会覆盖已保存能力；显式false保留。当前规范为specs/education/zcode-model-settings-v8.md，v7模型界面已替换。

分问流式教学沿同一useEducationWorkspace发送路径。streamDraft/streamScope只属于当前generation的临时投影，done替换成Store规范会话；失败保留原输入和已上传图片，同编号只恢复已有结果，不静默创建新推理。正文、流式状态与图示标明当前小问，答案许可按问隔离。见specs/education/scoped-stream-tutoring-v1.md。

曲线教学v8复用图示工具和唯一播放器：支持函数题主动生成原题曲线；第一屏展示实际函数与关键点；提示使用明确符号尺度和原系数试探。非负和展示原式根式/绝对值曲线及各自横轴，拒绝动画时沿同一工具输出静态图。Curve读取编译器的精确刻度和关键点，plotTicks只排布普通网格；UI不推数学结论。见specs/education/curve-first-teaching-v1.md。

ProblemAnimation读取工具编译的reasoning_lesson，按同一useTeachingAnimation进度展示当前条件、操作、依据与公式。零点情形和候选点按钮仅seek当前播放器；放大、播放和前后步骤仍使用唯一进度。UI不求参数、不计成绩，不用游标描线替代原题推导。见specs/education/problem-reasoning-animation-v1.md。

教学呈现v6由学生原始请求的否定作用域决定：分别/特别不被当作“别”。函数Controller输出同一批准数据的动画或静态图，可附受控情景解释；非负和故事绑定表达式而非变量本身。前端继续展示同一消息与原播放器，不增加新状态。见specs/education/combined-presentation-v1.md。

情景故事复用identity_probe的可选scorekeepers场景，读取工具编译的原式、两记录器规则与逐步账单。与原动画共享progress，界面不推断数学或增加播放状态。持久原题和呈现偏好由Store拥有，TTL只清临时步骤，澄清不能解绑原题。见specs/education/story-context-v1.md。

identity_probe读取工具编译的algebra_lesson，以原式、试值和参数条件展示恒等式。TeachingAnimation用同一progress和currentStep驱动符号拼片、公式、单步和弹窗，播放连续到最后；hint不展示完整解，solution由服务端授权。合法函数图数据可适配function_trace，冲突参数拒绝。见specs/education/identity-animation-v1.md。

练习仅保留提示与导师对话入口，苏格拉底追问按钮退役。真实模型提示复用所属题的Agent Loop，提示事件与回复由Store同事务提交；同编号重放沿用既有execute。提示深度与已核验学生进度分开，导师结论不成为学生掌握事实。见specs/education/grounded-hints-v1.md。

架构v11只显示一张系统关系图，Loop包含决策/调用/观察的实际回路。节点打开模块职责与源码详情，不再展示其它总图和内部图。唯一图形投影为SystemPanorama；缩放和弹窗是局部状态。见specs/education/release-readiness-v1.md。

设置管理独立于四个学生功能。can_manage控制运维接口；清空全部历史由原Store的租约/epoch/幂等事务处理，成功即失效客户端generation与会话投影。模型配置不冒充远端健康。界面偏好复用ZCode原owner。

函数animation_scene可带inspection_steps，AnimatedVisualCard仍拥有progress；关键步骤、播放、单步、读数和放大共享同一进度。函数值共用functionValue计算三次曲线；标记和最值区间来自工具，UI不推断参数或成绩。见specs/education/conversation-problem-v2.md。

几何lesson由工具生成，AnimatedVisualCard唯一持有播放进度，图形、公式与放大共享seek；播放连续到最后，上一步/下一步定位分镜。数字步骤导航退役。见specs/education/system-management-v1.md。

triangle_rotation与geometry_motion读取已核验几何构造的有界参数；显示进度只驱动同一构造的纯数学变换，不写学情。见specs/education/product-completion-v1.md。

coordinate_drawing 播放时只沿已接受端点连续延长当前线段，单步停在完整关键帧；UI不新增几何数据或教学结论。

coordinates 的 segments/polygons/circles 及 function_plot、area_model 是已接受工具结果，UI按索引绘制真实几何与工具采样，不补造点。coordinate_drawing、fraction_fill、pythagorean 使用同一动画播放器的局部进度。图形调整保留旧消息，新图可带parent_id。组合策略标签由服务端提供。见 specs/education/visual-tasks-v3.md。

情景动画随同一助手消息保存和刷新重放。播放、单步、暂停、进度与重置只改变展示，减少动态模式禁用连续播放，不发模型和成绩命令。已有概念对话的自然追问由服务端任务态承接；换题/取消后的 Detail.practice 不展示旧题。文字辅导的 model_protocol 失败同样保留可编辑草稿。见 specs/education/tutoring-evolution.md。

TeachingVisuals 在助手消息内呈现同一个已接受 Response.visuals。ArtifactTable/ArtifactChart 和 MessageResponse/Mermaid 直接使用 ZCode；数轴、坐标使用有界参数化 SVG。收起、Dialog 和演示是局部 UI 状态，不变更成绩；教学关系图隐藏代码操作。见 specs/education/visual-teaching.md。

摘要、图谱与地图使用 profile.review / review_overview 显示新练习复测和历史复习建议；不另建前端计时器或写入计划。节点当前正确率使用 30 天最多五次独立作答，累计次数在数据依据保留。辅导仍只有对话、图片与历史题，学情读取和帮助升级发生在同一后端 owner。见 specs/education/learning-evidence.md。

历史题的完整原题由所属会话读取，复习和讨论思路直接进入教学；不以固定提示词作为原题是否存在的判断。通用原题辅导走可信 GLM 自然文本，核验与成绩由服务端负责。MathContent 只映射教育数学中的独立遮盖符号为 TeX，继续复用 ZCode MessageResponse。

学习地图显示目标关联路线及整体理由，节点显示教材/题库关系和检查点。三至五站点按时间布局；源题库无题的基础目标可使用明确标注的系统数值变式。路线选择仍只有同一个服务端写入入口。

学习路径仅展示一张分支地图，同时显示 path.routes；选择经 execute 写入原学生 Store，实际影响三题组合。节点说明和设置嵌入地图，不再展示独立详情、今日行动与规则卡。点选知识点只改变本地查看，路线、目标及重点由服务端投影。见 specs/education/learning-route.md。

图片读取完成前禁止发送；实际请求等待中与已接受消息均使用 ZCode 附件组件展示同一条用户消息的 1–3 张图片。成功清理草稿，失败保留；已有编号的恢复不重复渲染临时气泡。见 specs/education/multimodal-tutoring.md。

图片附件直接调用 @zcode/ui/chat-attachments 的创建/序列化/释放函数与 @zcode/ui/attachments 的预览/移除组件。model_protocol 表示已知模型回复格式失败，保留草稿并解锁编辑，停止同编号恢复；不显示权限错误。新提交仍由用户操作生成新编号。见 specs/education/multimodal-tutoring.md。

辅导输入区新增图片草稿与历史题选择，复用公共按钮/对话框/输入控件。图片只作为草稿，上传后使用附件 ID，原输入与附件 ID 同编号恢复；识别结果和图片历史读取服务端投影。历史题按真实来源筛选并复用原会话，残缺题只读说明。见 specs/education/multimodal-tutoring.md。

Detail.practice 是按学生与会话绑定的题目参照，用户自然消息无需复制题干。用户/助手消息共享安全数学渲染。最近对话只读搜索与折叠，不删除历史；同题开始由 Store 复用并保存请求别名。路径调整折叠，图谱焦点跟随服务端 path.focus。见 specs/education/product-usability.md。

学情看板首屏提供知识图谱，显示完整源画像与新作答；模式、筛选、节点选择和视角仅为局部 UI 状态。开练复用 LearningPanel 的学习目标命令，未知结果保留原编号。连接中的分类线与先修候选区分，不推断学生掌握事实。见 specs/education/learning-map.md。

首屏学情摘要基于完整 LearningOverview 的同一快照派生，概括学习现状、相对熟悉知识点与下一步建议；不生成新的掌握事实，不随图谱局部筛选改变。两块初始化/新练习统计卡退役，来源和详细计数折叠在“数据依据”。示例来源及历史/近期区别保留，新作答自动更新摘要。

真实数学图谱/题库支持安全 Markdown 数学题干与单选/数值作答；学情分开显示初始化画像估计与新练习，保留来源未关联提示。浏览器不持有标准答案，不把源会话渲染为本产品模型轨迹。见 specs/education/student-data.md。

当前产品仅四项导航：个性化辅导、学习路径、学情看板、个性化练习。模型、工具轨迹、技术记忆、课程检索与教师管理不作为独立页面。LearningPanel 通过公共 LearningOverview/PracticeAssignment 契约读取学生隔离投影；练习提交保留原编号直到服务器明确成功或拒绝，未知结果只重放原操作。输入拒绝可更正。目标、练习结果与能力证据由 Python SQLite owner 保存，浏览器刷新后恢复。见 specs/education/four-features.md。

辅导输入仅自然对话，模式与步骤由既有服务端解析；恢复仍发送 original_input。“换一组”通过同一 execute 命令使用固定 request_id，不另建曝光缓存。路径呈现动态原因和推进条件，推荐三道显示各自分工。见 specs/education/adaptive-learning.md。

从教育 HTTP 契约读取投影，不直接读 SQLite。接受的输入只通过教学服务写入。generation 与 selection 序号撤销切换身份/会话后的过期响应。网络失败保留原输入与 request_id。窄屏可访问发送、会话、练习与反馈。复用 ZCode 主题 token 与公开 Button。

恢复未完成消息提交 original_input；input 中补充的算式、步骤和课程字段仅供展示，不参与客户端重新构造请求。

模型结果未知或已失败通过稳定 error_code 投影，页面不提供同编号再次生成；刷新后仍保留停止状态。明确繁忙与只读工具中断可按原编号恢复。

直接复用 @zcode/ui 的 Button、Input、Textarea、Select、Message/MessageContent/MessageResponse、useTheme 和 ZCodeIntlProvider。主题、语言偏好按上游存储约定持久化；教育组件不复制其实现。Markdown 仅呈现已接受回复，不提供文件打开、工作区或平台执行回调。领域 Select 只编码“全部学科”的空值，不另行实现菜单/焦点/键盘状态。

根节点组合上游 TooltipProvider，消息代码块使用其上下文。独立构建直接读取 packages/web/public，HTTP CSP 定向允许内嵌字体和 Shiki WASM。渲染错误边界、异常与资源加载失败均纳入验收。

教学图标注与响应性能遵循specs/education/visual-discussion-latency-v1.md。Web拥有笔迹草稿和PNG附件；visual_context通过原请求契约携带同会话接受图编号，Store验证并恢复原题，视觉导师直接讨论标注，不把标注作答当作掌握证据。精确坐标标签是输出显示元数据，不回填工具输入；数学依赖在服务就绪前准备，执行deadline不放宽。

标注草稿与已提交笔迹共用一个React状态队列；回调内取指针坐标，延迟更新不保留事件对象。重绘按浏览器帧合并，导出前同步刷新。当前指针取消/丢失捕获只移除当前草稿，不影响原图和已提交笔迹。快速move/up批处理、长曲线与触摸中断使用浏览器验收覆盖。

Codex流式教学遵循specs/education/codex-streaming-recovery-v1.md。MathContent转发上游MessageResponse.streaming；增量不等整句或公式。失败后读取Store快照，partial_response明确作为未完成片段显示；网络无法读快照时保留本地流式草稿。切会话失效旧流，已知输出截断可明确重新回答，原题、图片及visual_context保留。
对话中的student_tasks是服务端已接受的任务产物，Web仅展示题卡/摘要/路线并通过已有服务选择题目或导航；没有结果时不能自行生成替代题。查询不触发旧题动画或讲解。见specs/education/current-task-tools-v1.md。
