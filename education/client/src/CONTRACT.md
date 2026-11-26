# 教育 HTTP 客户端

TeachingResponse.student_tasks为已接受的学生任务结果，包含题卡、学情摘要或路线预览；不含题库答案、内部工具账本或凭据。增量仍是草稿，done和历史共用规范结果，题卡选择使用已有练习入口。见specs/education/current-task-tools-v1.md。

ChatModelsView来自安全GET/POST /api/chat/models，只有模型目录、能力、档位与会话版本，不含地址和凭据。TeachingRequest.model_selection冻结具体模型身份/配置版本/reasoning_level；旧请求不补字段。发送前图片上传、新会话初始化、重试与明确重新回答遵循specs/education/zcode-composer-model-selection-v1.md。

断网与非JSON代理响应使用稳定的network_unavailable/invalid_response中文错误。保留原HTTP状态、输入和待确认命令，不能将解析失败当成未受理或生成新编号。见specs/education/product-solid-review-v1.md。

模型投影v8增加connections与嵌套models，providers保留兼容投影。模型标识为连接ID（main）或连接ID~模型key，配置保存完整ModelConfig，同一连接共享加密凭据。GET不回传密钥，写入沿version/request_id契约，角色由服务端解析为具体模型。见specs/education/zcode-model-settings-v8.md。

ModelSettingsView和ModelProvider仅携带无密钥的配置投影、输入能力、选择版本和测试结果。新增模型连接/选择/发现/测试均走EducationService并由服务端校验can_manage、CSRF与版本。已保存API Key永不回传；默认部署凭据仅可在同endpoint下引用。切换配置后原未完成请求返回model_changed，不以旧编号重发新模型调用。ArchitectureModule.scope描述输入、职责、输出、步骤和协作模块，UI不另造服务端状态。见specs/education/model-adaptation-architecture-v7.md。

分问流式教学：TeachingScope提供本次按顺序处理的小问、各问模式和当前问。EducationService.stream仍POST原/api/teach与原request_id，校验SSE序号和请求归属，done返回原JSON规范投影；途中只有临时增量/阶段/替换，不成为持久消息。原JSON调用继续可用。见specs/education/scoped-stream-tutoring-v1.md。

v8的ReasoningCurve新增可选精确刻度、轴名、公式和说明；非负和term_curves携带两条当前表达式曲线及合法观察点。function_plot的square_root/absolute使用已批准内部一次式，axis_labels区分两变量；数据仍由原题工具编译，静态/动态共用许可，旧消息兼容。见specs/education/curve-first-teaching-v1.md。

TeachingVisual.reasoning_lesson是problem_reasoning_v1的只读判别联合。function_reasoning绑定原系数、区间、零点情形、消元和最值比较；nonnegative_reasoning绑定原表达式、矛盾、方程运算及所求。提示版不携带solved参数或结果。分镜来自工具而非模型或UI推断，旧模板保持可读。见specs/education/problem-reasoning-animation-v1.md。

TeachingVisual的identity_probe增加可选scorekeepers scenario和algebra_lesson.story/accounts，工具提供原题规则与分镜账单；UI不自行推断。v5扩展兼容历史v4普通动画。见specs/education/story-context-v1.md。

Bootstrap携带服务端can_manage与SystemSettings投影；管理设置和架构模块仅通过公共EducationService读取，客户端不赋权。FunctionDisplay携带符号工具的精确公式、区间和关键点，数值采样与教学展示分离。见specs/education/system-management-v1.md。

function_plot/function_trace支持cubic的a,b,c,d系数、工具核验标记和focus_interval。函数inspection_steps与几何lesson分型，播放器仍拥有唯一progress。原题引用在服务端Store保存，不由客户端猜测历史题。见specs/education/conversation-problem-v2.md。

几何animation_scene可带工具生成的lesson步骤、运动时间窗、披露模式、定义域及轨迹边界。客户端仅展示这些数据；旧图示由服务端只读投影升级，不改原记录。见specs/education/geometry-lessons-v1.md。

CoordinateSegment.role 的 connection 表示未推断几何性质的普通连线；不能因斜向就标为对角线。function_plot 的 problem 来源由 owner 核对原表达式的系数等价性。见 specs/education/visual-tasks-v3.md。

Response.visuals 是教学 owner 已接受的只读 TeachingVisual 判别联合；类型经本契约公开导出。文字与图一起投影，客户端不补条件、不发绘图调用、不写学情。旧完成消息无图仍可读。见 specs/education/visual-teaching.md。

profile.review 与 review*overview 为单一事件快照的只读复习投影；recent_independent*\* 是 30 天、最多五次新题独立作答，累计独立统计保留。unassisted 表示当前 assignment 无帮助的首次作答，复做可检验保持但不算 independent。见 specs/education/learning-evidence.md。

LearningOverview.path.route_reason、routes.edges 和 steps.checkpoint 提供同一服务端快照的路线依据与学习检查点，均为只读解释，不构成新的作答状态。PracticeItem.source 明确区分导入自动标注题与系统生成、数值规则核验的基础变式。

LearningOverview.goal.route 与 path.routes/selected_route 表示学生路线偏好及同快照的可用分支链路，path.steps/focus 对应当前选择。POST /api/learning/route 使用 route/request_id，幂等接受选择；不计作答。推题按路线偏好派生。见 specs/education/learning-route.md。

model_protocol 为模型回复格式失败，HTTP 502、recoverable=false，客户端停止同编号重发并保留草稿供新问题编辑。账户、会话和 CSRF 拒绝仍为 403，不能把模型格式预算耗尽当作身份拒绝。

Request.images 是服务端颁发的学生所属附件 ID，POST /api/tutor/images 使用固定 request_id 与 data_url 上传真实图片，GET /api/tutor/image?id= 返回鉴权 JPEG。Message.images/recognized_question 只投影所属预览和识别文本。GET /api/practice/history 返回 HistoricalPractice 安全题干、来源与原会话，不返回答案。PracticeItem.usable/quality_note 表示残缺旧题只读。见 specs/education/multimodal-tutoring.md。

Detail.practice 提供本会话的安全 PracticeAssignment 参照，不返回答案/解析；Session.practice_item 用于最近对话去重展示，完整历史可展开。参照与对话都来自同一个 Store。见 specs/education/product-usability.md。

knowledge_map 是同一学情快照的只读投影：完整源画像节点、教材路径分类、开练可用性与现有先修候选边。未匹配教材的画像节点 topic_id 为 null，不伪造边或目标。历史画像与近期练习指标保留来源含义，不返回题目答案。见 specs/education/learning-map.md。

真实数学 Catalogue 的 PracticeItem 增加安全题干、选项、核验类型/空数和来源，不包含答案。LearningOverview.initial 与 topics.initial 标注画像估计和历史作答，本产品 summary/daily 只统计新的练习。默认初始化为来源未关联的示例学生，学生页面不提供教师或身份切换。见 specs/education/student-data.md。

LearningOverview 是目标、学情、路径、推题和当前练习的唯一公开投影。PracticeItem 不包含标准答案；PracticeFeedback 区分独立首次作答与辅助/重做。练习变更复用账户与 CSRF，由服务器绑定原题，客户端不能提交标准答案或学习者身份。练习操作使用稳定 request_id，重放不增加次数。

服务端唯一拥有认证身份与接受的教学状态。客户端只持有服务端颁发的 CSRF 字段，GET/POST 均携带同源 cookie。请求失败不会创建新的 request_id。响应中的模型状态表示配置，真实推理参与由教学响应记录。

Message.input 用于展示服务端解析后的作答，Message.original_input 保存原提交内容。继续未完成请求时必须使用 original_input 和原 request_id，以保持服务端输入指纹不变。

EducationRequestError 保留稳定 code、HTTP status、recoverable 与 retryAfter。model_unknown 不代表已拒绝受理，也不能静默创建新 request_id；model_busy 可以继续原请求。HTTP 返回学生可见白名单投影，不包含内部答案、完整上下文或子 Agent 报告。

Codex流式适配见specs/education/codex-streaming-recovery-v1.md。文字delta立即展示；done才接受结果。Message.partial_response仅是失败记录中的未完成文字，response仍为null。model_truncated不重放旧付费调用，明确重新回答才创建新编号并保留原题标注引用；CRLF、UTF8拆块和事件编号持续核验。

# 学情推荐补充

LearningOverview 路径提供可解释 summary/next_check，练习建议每组目标三道并给出 purpose/kind/group。recommendation_info 提供批次与供给说明。POST /api/practice/recommendations 使用 request_id，经原 HTTP transport 向 Store 发换组命令；不是作答。参考 specs/education/adaptive-learning.md。

教学图标注与响应性能遵循specs/education/visual-discussion-latency-v1.md。Web拥有笔迹草稿和PNG附件；visual_context通过原请求契约携带同会话接受图编号，Store验证并恢复原题，视觉导师直接讨论标注，不把标注作答当作掌握证据。精确坐标标签是输出显示元数据，不回填工具输入；数学依赖在服务就绪前准备，执行deadline不放宽。

架构v11只读投影：ArchitectureOverview只提供单张panorama、16模块职责和源码绑定。图形数据不授予权限，不拥有运行或学习状态。旧多图字段已移除，见specs/education/release-readiness-v1.md。
