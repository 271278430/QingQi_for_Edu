# 维护职责与入口

| 模块               | 唯一责任                                              | 主要维护入口                                                                                           |
| ------------------ | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 辅导与Agent Loop   | 原题恢复、按问任务、模型/工具决策、教学核验           | service/src/qingqi/agent.py、tutoring_scope.py、teaching_policy.py、teaching_plan.py                   |
| 状态与记忆         | 正式回复、当前题、学习事件、租约/epoch与幂等          | service/src/qingqi/storage.py、web_store.py                                                            |
| 学习路径/看板/推荐 | 从同一学习证据派生结果；选择与作答经Store写入         | service/src/qingqi/learning_branches.py、learning.py、learning_evidence.py                             |
| ZCode运行能力      | 按公共契约执行固定工具、MCP、Skills、专项子任务和召回 | runtime/src/index.ts、memory.ts                                                                        |
| Web与公共接口      | 输入草稿、同会话请求、SSE展示、动画进度与四功能页面   | client/src、web/src                                                                                    |
| 权限与设置         | 身份、CSRF、归属、can_manage、配置/清理回执           | service/src/qingqi/product.py、management.py                                                           |
| 模型适配           | Store版本化连接/模型/角色、加密凭据；每轮冻结客户端   | service/src/qingqi/model_settings.py、provider_models.py、secret_store.py；web/src/provider-editor.tsx |
| 架构说明           | 服务端源码目录与符号事实；前端只呈现                  | service/src/qingqi/architecture*catalog.py、architecture*_.py、web/src/architecture-_.tsx              |
| 本机部署           | 配置、依赖、受控启动和停止                            | tools/open-workspace.ps1、run_models.py、stop-workspace.ps1                                            |

变更行为先维护spec，再运行对应既有CLI/HTTP/浏览器验收。类型、lint/Hooks与架构门禁遵循根AGENTS.md。不要向源码、日志或图示写入密钥与真实学生正文；不要把查看看板或自由概念讨论算作知识点作答。

运维见[operations.md](operations.md)，验收见[verification.md](verification.md)，当前架构见[architecture.md](architecture.md)，发布与提示边界见根目录specs/education/release-readiness-v1.md；v8模型组件来源仍见[zcode-source-architecture-v8.md](zcode-source-architecture-v8.md)。历史专项审查集中在reviews目录。

当前v8以Store/ModelSettings拥有供应商连接、嵌套models和角色选择，provider_models负责完整模型配置校验与推理投影。原ZCode模型组件经公共出口复用。当前只展示单张五层系统图与实际Loop回路，点击节点查看模块职责和源码。

当前教学策略由Store的dialogue_state拥有teaching_mode，Agent读取后选择本轮教法，规范回复提交时同事务写回。已公开答案来自按问answer_parts，与教学模式字段独立。teaching_plan按目标选择一个图或动画，render_teaching_visual是唯一执行入口；teaching_visual_pair复用同题静态和动态投影，前端保存标注草稿与播放进度。当前视觉规格见[single-teaching-visual-v1.md](../../specs/education/single-teaching-visual-v1.md)。
