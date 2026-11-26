> 历史实现记录。架构现已简化为一张系统关系图，当前说明见[architecture.md](architecture.md)。

# ZCode模型设置与实际架构 v8

当前检出的ZCode版本为3.18.2。教育模型设置直接通过公共@zcode/ui/model-provider-settings出口调用原组件，该出口指向原ProviderCardSections.tsx。

| 界面功能               | 实际ZCode组件                                       |
| ---------------------- | --------------------------------------------------- |
| 供应商导航与双栏布局   | ModelProviderSectionLayout / Navigation             |
| 供应商标题、改名与删除 | ProviderCardHeader                                  |
| API地址与协议          | ProviderConnectionSection / ProviderApiFormatSelect |
| 密钥输入、显隐与只读   | ProviderApiKeySection / ApiKeyInput                 |
| 模型行、开关与测试     | ModelRowInput                                       |
| 添加与编辑模型         | ProviderModelMetadataDialog                         |
| 草稿与稀疏配置校验     | useProviderModelDraft / ProviderModelMetadata       |

原组件增加可选的能力展示和只读/禁用参数，教育界面开放文字、图片、上下文、输出上限、结构化输出与原生工具能力。草稿使用ZCode原类型与校验，随后补齐教育HTTP契约中的完整配置字段。修改模型ID保留已有能力配置，保存失败保留草稿，未知结果保存同一个操作编号。界面显示Store接受的配置，迟到的旧读取不能回滚新保存结果。

ZCode改名草稿可能返回undefined能力字段，教育适配只合并已定义字段，保留已关闭的原生工具能力；该问题已通过实际改名、请求中断及恢复操作回归。供应商导航选中项和详情一致，文本与视觉角色都有可见标签。

一个供应商保存API地址、协议和一份加密凭据，其下多个模型分别拥有ID、启停、输入能力和预算。文本导师与图片理解角色选择具体模型，也可以选择同一个多模态模型。旧单型号记录按main模型投影，原选择ID继续有效。

Python ModelSettings适配教育服务的状态和推理入口，Store/SQLite拥有接受的配置。ModelSettings.resolve从角色解析具体模型，JSONModel捕获本轮地址、协议、凭据与参数。新版本用于新请求，在途请求使用已捕获客户端。输出上限进入API的max_tokens，上下文参数参与文本输入预算保护，图片和工具能力决定传输方式。8B/27B专项模型通过既有ZCode前台子任务Port执行。

## 模块组织与图

| 层         | 模块                                         | 职责                                         |
| ---------- | -------------------------------------------- | -------------------------------------------- |
| Web交互    | Web客户端                                    | 输入与附件草稿、SSE临时展示、播放器进度      |
| 请求与管理 | 权限、设置管理                               | 身份、CSRF、资源归属、管理命令与实际源码架构 |
| 学生业务   | 辅导、路径、看板、练习                       | 原题教学、路线选择、证据投影与每组三题       |
| 智能体运行 | Loop、路由、记忆、Skills、工具、模型、可视化 | 任务与上下文、受控调用、观察、核验与交付     |
| 数据与状态 | 教材题库、Store                              | 只读课程资源与唯一会话/学情/配置写入         |

三张总图分别展示执行时序、系统依赖、四功能业务。16张内部图采用实际模块步骤，Loop、模型、记忆、持久化、管理和图示模块明确画出分支。图示工具返回观察，Loop核验后由Store保存，Web读取批准数据播放。普通回复提交原题、当前问和episode，fact确认使用内部受信的Store.confirm_fact。

模块目录同时提供输入、输出、步骤、调用模块、权限边界和真实文件/函数绑定。系统图与模块清单相互校验，绘图验收检查字形、重叠、箭头、连线穿越和完整SVG/PNG导出。

完整导出：[输入输出流程](../.local/reports/architecture-v8-flow.svg)、[系统关系](../.local/reports/architecture-v8-system.svg)、[四功能流程](../.local/reports/architecture-v8-business.svg)。16张内部图在同目录的v8-module-<id>.svg中，网页可逐个查看。

## 验收

```powershell
python education/tests/zcode_model_acceptance.py
python education/tests/model_settings_acceptance.py
python education/tests/model_settings_edge_acceptance.py
node education/tests/model_settings_browser.mjs
node education/tools/architecture_v8_browser.mjs
node education/tests/product_deployment_browser.mjs
pnpm typecheck
pnpm lint
pnpm architecture:check --changed
```

模型HTTP场景使用隔离目录和受控API，检查多模型、预算、图片、密钥及恢复语义。model_settings_live.py使用真实API，检查保存配置、文本连接、合成图片识别与默认苏格拉底流式辅导。正式入口检查只读，检查前后比较学习摘要。

2026-11-24完成记录：模型接口20项、边界11项、供应商多模型9项；原组件浏览器9项；四功能HTTP19项及浏览器5项；按问/SSE接口14项及浏览器4项。图形浏览器6组检查覆盖3总图和16内部图。真实API隔离验收3项，流式样例2次增量、0次修复。两套正式服务重启后18项只读检查通过，学习摘要保持一致。

根typecheck、Web构建、架构门禁通过；root lint为532告警、0错误，涉及本次组件与教育Web的43文件Hooks专项0诊断。上游freshness命令已执行，本次GitHub fetch连接失败；采用已检出的3.18.2源码与本机origin/main基线，未宣称跟踪到最新远端版本。架构门禁覆盖已登记的TypeScript模块；Python关系和交互另由接口/浏览器及源码绑定检查提供证据。
