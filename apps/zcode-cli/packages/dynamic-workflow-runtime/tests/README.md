# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow-runtime 基础工程中的 tests 验收与回归场景。

### 文件

| 文件                                                         | 简要说明                                                                                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| [args.test.ts](args.test.ts)                                 | \* 运行实参 `args` 经**真实入口**抵达沙箱：runWorkflowScript → ChildPayload → vm context。                                            |
| [artifacts.test.ts](artifacts.test.ts)                       | \* 用户面产物（docs/dynamic-workflow/authoring.md）穿过整条管线：真实脚本 → lowering → 沙箱                                           |
| [auto-driver.ts](auto-driver.ts)                             | \* AutoDriver：集成测试用的**自治** fake driver——同时扮演 Boundary B 的 driver port 与"模型"。                                        |
| [child-entry-file.test.ts](child-entry-file.test.ts)         | \* 沙箱入口文件的落盘契约（docs/dynamic-workflow/launch.md「Single-executable builds」）。                                            |
| [child-source-bundled.test.ts](child-source-bundled.test.ts) | \* `renderChildEntry` 在 **esbuild 打包 / minify 之后**依然渲染出一份可运行的自包含入口文件。                                         |
| [child-spawn-args.test.ts](child-spawn-args.test.ts)         | \* 沙箱子进程的 **spawn 策略**契约（`RunWorkflowOptions.childSpawn`）。                                                               |
| [child-spawn-env.test.ts](child-spawn-env.test.ts)           | \* 沙箱子进程 spawn env 契约：必须显式携带 `ELECTRON_RUN_AS_NODE=1` 且继承父进程 env。                                                |
| [control.test.ts](control.test.ts)                           | \* harness 的活体控制面接线（`RunControlBinding`，docs/dynamic-workflow/concurrency.md                                                |
| [e2e.test.ts](e2e.test.ts)                                   | \* 端到端管线：真实脚本 → lowering → 沙箱子进程 → 引擎 → AutoDriver。断言最终 artifact、                                              |
| [failures.test.ts](failures.test.ts)                         | \* 失败路径：错误是一等公民。墙钟超时 / abort / 脚本抛错 / 子进程输出损坏的 NDJSON 都必须被                                           |
| [helpers.ts](helpers.ts)                                     | \* 集成测试共享装配：脚本文本 → 真实 schema 合成 + 真实 validate + 真实 lowering → 沙箱子进程                                         |
| [holes.test.ts](holes.test.ts)                               | \* 留白在 cell 里、在站点处求值（docs/execution-engine.md「The vm cell」的 Holes 段与「## Holes」）。                                 |
| [provider-stop.test.ts](provider-stop.test.ts)               | \* 确定性模型侧错误让整个 run 停下（apps/zcode-cli/packages/dynamic-workflow/docs/execution-engine.md「Terminal states」）：driver 经 |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                                                                      |
| [resume.test.ts](resume.test.ts)                             | \* Resume e2e：先把脚本跑到完成、落一份 journal；再以**全新子进程** + 同一 journal + 一个                                             |
| [run-identity.test.ts](run-identity.test.ts)                 | \* run 身份 `run` 经**真实入口**抵达沙箱：runWorkflowScript → ChildPayload → vm context。                                             |
| [run-metadata.test.ts](run-metadata.test.ts)                 | \* Run 元数据经**真实入口**落库：runWorkflowScript → 引擎构造 → createRun。                                                           |
| [security.test.ts](security.test.ts)                         | \* 沙箱安全：vm.createContext 求值单元的隔离契约（docs/execution-engine.md 的"The sandbox"）。                                        |
| [streams.test.ts](streams.test.ts)                           | \* 流水线原语 channel / future 与停滞检测在**真沙箱**里的行为（docs/dynamic-workflow/authoring.md                                     |
| [usage.test.ts](usage.test.ts)                               | \* 用量事件：driver 每次 ask 结算回报 stats，引擎累计 run 级 spentTokens 并发 `usage-updated`。                                       |

<!-- qingqi-directory-index:end -->
