# 教育后台复用 ZCode 运行能力

构建先在内存生成独立 ESM bundle，再在同目录临时文件写完后 rename 替换入口；运行中的产品不能在重构建时读到半个 server.js。历史题验收出现过一次 runtime_unavailable，完整诊断尚不足以确认该次原因，不能将重跑通过写成原因已证实。

Windows 的并发读句柄可能暂时拒绝 rename，完整构建验收已观察到 EPERM。参照 ZCode atomicFileUtils 的原子发布与有限重试设计，仅对 Windows 的 EPERM/EBUSY/EACCES 以异步短间隔重试最多四次；不删除正式入口或改为原地覆盖。永久失败保留原入口并清理临时文件，其他错误立即失败。这个文件发布边界不改变教学、模型或请求的执行预算。

2026-11-20。唯一用户交互为 Web。教学 Python 服务继续唯一拥有学生身份、接受的请求、会话顺序、检查点、回复和教师事实。新增内部 Node adapter 直接调用 ZCode 的公共 ToolRegistry/ToolExecutor/ToolScheduler、Skills adapter、MCP adapter、前台 SubagentPort，以及记忆候选过滤与预算函数。它不提供用户终端、外部插件或 MCP 产品入口，不另建学生业务数据库。

教育意图规则、题型判断和教学策略保留领域实现；ZCode 本身没有教育分类器。规则/上下文识别意图后，受控 DAG 使用上游调度器，GLM 通过上游 registry 生成的能力契约选择工具，专项任务使用上游前台子 Agent 生命周期。子 Agent 只执行绑定的专项能力，不能自行注册工具、改身份、调用 Shell、扫描全局 Skills 或写入掌握事实。每个 child 关联父 run/trace，结果仍须通过原题/步骤/图谱核验。只复用生命周期，不宣称教育主控已经迁入完整 AgentRuntime。

ToolScheduler 返回的 executionOrder 驱动教育当前未完成意图与工具准入。节点完成以实际课程上下文、作答核验或学情观察为准，禁止学情工具抢在其前置审查之前执行。确定工具阶段由领域计划构造，GLM 主要用于有歧义的意图回退与自由辅导决策；不能把结构化工作流称为完整自治模型循环。复合课程/审查/学情场景验收实际工具顺序与越序拒绝。

后台协议为有界双向 NDJSON：Python 发出 init/skills/plan/recall/contracts/call/close；Node 仅向 Python 请求已注册 local/model handler。Python 保留输入与输出 Schema 验证。init 仅使用可信部署生成的固定能力集合、解释器及本项目运行目录。每轮独占 adapter，结束后关闭 MCP 和子 Agent；超时终止所属进程树，不影响其他训练/推理。部署与能力版本参与检查点签名。

Node 启动/执行管道断开返回 runtime_unavailable，协议损坏返回 runtime_protocol，经 HTTP 边界映射为 502；不暴露底层进程栈或误报内部 500。关闭真实所属 Node 管道的验收证明错误契约。

Node 生产入口构建为 ESM bundle，消除每轮 --import tsx 冷解析上游源码图的开销。构建仍从公共包导入同一实现，生成物不是复制维护的另一套 runtime；保留类型声明构建。Node 内置模块与必须外置的原生能力仍按模块契约加载，服务目录定位保留在同一 dist 位置。部署运行 bundle，不放宽整轮预算；缺失产物明确失败。QINGQI_NODE 仅为可信部署指定 Node 24 解释器，优先于本项目自有 runtime，再使用系统 node；缺失时明确失败，不回退到自建协议客户端。构建、真实运行能力/浏览器回归与离线冷启动对照证明 bundle 的路径和行为。

MCP discovery、连接与调用直接使用 @zcode/adapters/mcp；原有 Python 图谱/数值 MCP server 保留为领域工具，退役自建 Python MCP client 的产品调用路径。Skills 只发现本项目固定根，保留 manifest/sha256 与能力交集校验。ToolRegistry/Executor 只注册教育白名单，禁止调用 registerBuiltInTools。

记忆原始事实唯一存于学生隔离的 SQLite；先按学生授权过滤，再排序，随后复用上游 manifest 白名单过滤、最多五项选择、去重和字符预算。无需第二份可写 Markdown 记忆。工作态按会话，学习历史带来源，教师确认带版本；模型回复和学情候选不能提升为掌握事实。自动抽取和 dream 合并暂不启用，因为通用编码记忆的自动写入不满足教育确认契约。

召回累计字符不得超过上游 MEMORY_RECALL_SESSION_CHARACTER_LIMIT；过大的完整条目跳过，不截断教师事实或原始作答。随后仍由教育 context_bytes 限制最终模型上下文；计数报告实际进入召回的条目。

学情回复把原生四分类候选显示为知识回忆、概念理解、解题步骤或知识迁移的待确认困难，不把这些标签退化为“其他困难”或提升为已确认事实。

同会话只允许一个在途请求，已完成结果可重放。所有模型请求（主控、路由、专项）在发出前写调用记录，区分 sending/unknown/busy/failed/done；unknown 阻止同编号静默重发。已明确的繁忙允许原编号恢复，不能误报权限错误。只读工具已完成结果沿用原账本。浏览器错误保留 code/request_id/retry_after/recoverable。

学生可见投影由服务端白名单构造；启发模式不返回数值答案、完整上下文、子 Agent 原始报告或完整 observations。保留来源、首错提示和安全执行元数据。已知事实的回复通过结构化证据绑定；不支持的题型先澄清，不能返回内部 500。

验收先维护：真实 HTTP 下上游 Skills/MCP/local tool/subagent 调用与事件、DAG 顺序、隔离记忆过滤、学生投影、同会话并发、模型已接收后断连原编号恢复、明确 429 恢复、正确作答/课程引用、部署变更与原输入恢复。模型夹具不冒充真实效果。执行教育 runtime/Web build/typecheck、根 typecheck/lint、CLI 受影响包检查、架构、浏览器复用与恢复；React 改动另做 Hooks 专项。

数值步骤核验必须绑定当前原题：支持原题 AST 子表达式的等值替换（如 2+3*4 → 3*4=12 → 2+12=14），拒绝无关等式 9=9。代数、除零与不在当前表达式范围内的输入在模型前澄清。已核验的作答/课程结论统一由证据渲染器输出并再次校验，合法引用不能掩盖虚构正文或启发模式泄答；自由对话的语义质量仍需模型评测。

Web-only 退役范围及回归迁移见 workspace.md。内部运行能力不依赖已退役教育插件、外部 MCP bridge 或旧 Python MCP client。Registry 的运行根必须由教学 owner 显式提供，不接受空根或用户指定目录。

Web 错误交互保留稳定 code。model_unknown/model_failed 不显示再次生成按钮，并提示记录已保留；历史投影包含 error_code，刷新后继续禁用同编号重试。明确 model_busy 与中断的只读工具仍可继续。浏览器恢复夹具新增已记录 unknown 状态的呈现场景；模型真正断连防重发由独立协议验收证明，夹具不冒充推理。
