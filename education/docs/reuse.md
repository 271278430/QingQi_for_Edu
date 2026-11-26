# ZCode源码复用边界

对话框选模直接调用原ModelConfigSelect/ComposerModelMenu及受限CEL编译器。新增公开出口而不复制菜单或执行JS模板；发送快照参考原composerSubmissionConfig。会话选择、高低档真实HTTP与部署验收见[composer-model-selection-v1.md](reviews/composer-model-selection-v1.md)。新对话默认high，替代较早性能试验的默认low策略。

v8模型设置直接调用原供应商布局、标题/连接/API Key区块、ModelRowInput、ModelMetadataDialog与草稿校验。公共出口在原ProviderCardSections.tsx中，原组件增加可选的能力范围及只读参数，教育界面绑定Store连接、多模型和具体角色选择。详见[zcode-source-architecture-v8.md](zcode-source-architecture-v8.md)。

上游来源为 https://github.com/zai-org/ZCode ，来源提交、版本和许可证记录在 `source.json`。保留根LICENSE、NOTICE与THIRD-PARTY-NOTICES及上游源码。

| 实际复用                                | 教育适配                                             |
| --------------------------------------- | ---------------------------------------------------- |
| createToolRegistry / createToolExecutor | 固定教育ToolSpec、原题参数绑定和输入输出Schema       |
| ToolScheduler / PermissionService       | 教育阶段DAG、依赖顺序、能力白名单与有限执行          |
| MCP adapter                             | 内部课程图谱和数学工具的连接、发现、调用             |
| Node Skills adapter                     | 项目教学Skills的manifest/指导加载，哈希与能力交集    |
| createExploreSubagentPort               | 8B/27B专项子任务的profile、trace、事件与报告生命周期 |
| selectScopedMemory                      | 已授权候选中的有界召回、去重与上下文预算             |
| @zcode/ui与消息/数学/附件组件           | 仅Web的学生四功能、主题与教学可视化                  |

入口在 `runtime/src/index.ts`、`runtime/src/memory.ts`和Web的上游公共导入。Python Agent/Store拥有教育状态，Node runtime adapter执行受控能力，不能各自保存一套被接受的教学事实。

教育领域的意图类别、按问多意图、按会话选择教学方式、输出长度、学情证据、先修规划、三题多样性和教学图绑定由当前项目实现。ZCode没有现成的K12学情分类器；不把教育规则说成上游自带能力。

目前未接入完整ZCode AgentRuntime，也未复刻自动记忆抽取、合并与dream后台。专项子任务使用真实上游前台生命周期，模型回调仍由既有Python适配器执行。历史源码审查见 [runtime-reuse-review](reviews/runtime-reuse-review.md)，当前架构以 [architecture.md](architecture.md)及Web目录为准。
