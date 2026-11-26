# helpers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 helpers 验收与回归场景。

### 文件

| 文件                                                       | 简要说明                                                                                                                             |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| [fake-provider-server.ts](fake-provider-server.ts)         | \* 假 provider 服务器（apps/zcode-cli/packages/dynamic-workflow/docs/execution-engine.md「Verification」）。                         |
| [fake-provider-wire.ts](fake-provider-wire.ts)             | \* 假 provider 服务器的 wire 帧（apps/zcode-cli/packages/dynamic-workflow/docs/execution-engine.md「Verification」）：Anthropic      |
| [fake-zcode-app.ts](fake-zcode-app.ts)                     | 实现或公开接口：createFakeApp。                                                                                                      |
| [fault-matrix-cells.ts](fault-matrix-cells.ts)             | \* 故障矩阵的快 / 全两档（apps/zcode-cli/packages/dynamic-workflow/docs/execution-engine.md「Verification」）。                      |
| [fault-matrix-scripts.ts](fault-matrix-scripts.ts)         | 故障矩阵的并行度轴：八个脚本形状（apps/zcode-cli/packages/dynamic-workflow/docs/execution-engine.md「Verification」）                |
| [fault-matrix.ts](fault-matrix.ts)                         | 故障矩阵的格装配（apps/zcode-cli/packages/dynamic-workflow/docs/execution-engine.md「Verification」「每格断言」）                    |
| [fault-programs.ts](fault-programs.ts)                     | \* 预制故障程序（apps/zcode-cli/packages/dynamic-workflow/docs/execution-engine.md「Verification」）。                               |
| [fault-provider-model.ts](fault-provider-model.ts)         | \* 把假 provider 服务器接成一条**真**的模型链（apps/zcode-cli/packages/dynamic-workflow/docs/execution-engine.md「Verification」）： |
| [legacy-selection-store.ts](legacy-selection-store.ts)     | 旧数据必须从磁盘播种；新版 writer 会包装新字段，不能拿它伪造升级前状态。                                                             |
| [pdf-provider-fixture.ts](pdf-provider-fixture.ts)         | 旧注册器已经退场；PDF 真实请求测试采用 App 的 Registry 到 Model 装配边界。                                                           |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                                                                                     |
| [registry-backed-test-app.ts](registry-backed-test-app.ts) | 测试基座默认关闭标题生成，避免无关 Session 测试产生额外模型调用与事件。                                                              |
| [subagents.ts](subagents.ts)                               | 实现或公开接口：loadPluginAgentProfiles。                                                                                            |
| [test-agent-runtime.ts](test-agent-runtime.ts)             | bootstrap 测试的 Model / AgentRuntime 夹具（照 core/tests 的同名夹具）                                                               |

<!-- qingqi-directory-index:end -->
