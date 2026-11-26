# ZCode 源码复用约束

教育产品优先使用当前官方 ZCode 源码提供的公共能力：已有组件通过 @zcode/ui 的公共子路径导入，不复制组件实现；缺少子路径时只公开现有源码，不新增另一套实现。保留上游第三方许可和来源。

本轮直接复用 useTheme 的主题持久化/系统主题处理、ZCodeIntlProvider 的语言偏好与组件翻译、Input/Textarea/Select 的输入与键盘交互，以及 Message/MessageContent/MessageResponse 的消息、Markdown、数学公式、代码和表格展示。教育控件只组合这些组件并绑定领域字段。消息展示不改变原提交、工具参数、证据或 request_id，不传入文件打开/工作区/平台执行回调。

共享消息组件通过动态导入接入，使用上游同一组件模块，不复制轻量替代渲染器。实际共享资源包体与预加载按构建和网络记录报告，不把入口块大小当作总启动负担。教育构建引用并检查 UI 工程声明与依赖，避免把其内部 @ 别名源码当作独立教育 TypeScript 工程输入。

共享消息组件依赖上游 TooltipProvider，教育根节点通过公共子路径组合已有 Provider，避免代码块操作提示触发 ErrorBoundary 后把整条消息降级为纯文本。数学字体允许同源和上游内嵌 data 字体，HTTP CSP 仅增加 font-src 'self' data:，其余执行与连接来源约束不放宽。浏览器验收同时捕获 console error、页面异常和失败资源，错误边界吞掉异常仍判为失败；核对字体实际加载。

代码高亮使用上游 Shiki WASM，script-src 允许 'wasm-unsafe-eval'，仍禁止 JavaScript unsafe-eval 与外部脚本。独立工作台通过 Vite publicDir 直接使用 packages/web/public 的图标和 favicon，避免消息组件请求已有上游资源却返回 404，不另造图标副本。

ZCode /education 和独立工作台加载同一个教育组件。教育产品只保留 Web 交互；教育 CLI、/learn、外部插件/MCP bridge 与安装器已退役，上游通用功能仍作为源码保留。内部 MCP 与 Skills 不依赖插件入口。

教学 Python 服务继续唯一拥有学生隔离、教学模式、图谱核验、教师事实、学习记忆与请求账本。内部 education/runtime 直接使用上游公共 ToolRegistry/Executor/Scheduler、MCP/Skills adapter、前台 SubagentPort 与 memory recall 函数。专项模型执行仍走受控 Python 回调；没有迁入完整 AgentRuntime/CommandInbox，也没有自动事实抽取/Dream。详见 runtime-reuse.md。

复用审计给出源码、真实调用位置、直接复用/设计参考/教育自建的区别。仅复制仓库不能证明复用。内部 MCP 复验从 @zcode/adapters/mcp 创建真实上游客户端，连接固定课程/数值领域 MCP server；模型、工具结果、回调和学生投影均经契约核验。模型夹具、离线协议测试与真实推理质量分别报告。

验收先维护浏览器场景：主题切换刷新持久化、系统主题变化、语言偏好刷新、Select 键盘选择/身份切换、Markdown/公式/代码/表格渲染、题目字段与原请求保持一致、窄屏无横向溢出、刷新恢复仍复用原编号。渲染夹具使用独立 HTTP owner、模拟回复和隔离数据，不消耗真实模型。执行构建、类型、Lint、Hooks 专项和架构检查。
