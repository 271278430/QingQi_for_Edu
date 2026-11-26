# @zcode/zcode-cua

API-compatible placeholder package for Computer Use. This build ships without
Computer Use: every runtime surface (Computer Use runtime, broker RPC, Helper
install/launch/verify, PiP session client, native addon loader) reports
**unavailable** and fails closed, predicates about official CUA frames are
`false`, and permission ports keep their privacy fail-closed semantics.

License: Apache-2.0.

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/zcode-cua 基础工程中的 zcode cua 模块文件。

### 子目录

| 目录                    | 存放内容                                      |
| ----------------------- | --------------------------------------------- |
| [test/](test/README.md) | @zcode/zcode-cua 基础工程中的 test 测试场景。 |

### 文件

| 文件                                                         | 简要说明                                                                                                                                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [broker-helper-constants.d.ts](broker-helper-constants.d.ts) | broker-helper-constants.d 的实现文件。                                                                                                                                    |
| [broker-helper-constants.js](broker-helper-constants.js)     | 实现或公开接口：HELPER_APP_NAME、DEV_HELPER_APP_NAME、HELPER_DISPLAY_NAME、HELPER_BUNDLE_ID。                                                                             |
| [broker-helper-health.d.ts](broker-helper-health.d.ts)       | broker-helper-health.d 的实现文件。                                                                                                                                       |
| [broker-helper-health.js](broker-helper-health.js)           | broker-helper-health 的实现文件。                                                                                                                                         |
| [broker-ports.d.ts](broker-ports.d.ts)                       | broker-ports.d 的实现文件。                                                                                                                                               |
| [broker-ports.js](broker-ports.js)                           | 实现或公开接口：isCuaPermissionStatusAvailable、shouldRunCuaScreenCaptureProbe。                                                                                          |
| [broker-server.d.ts](broker-server.d.ts)                     | 公共调用方依赖上下文类型；unknown 曾使日志回调在开源类型检查中失去参数类型。                                                                                              |
| [broker-server.js](broker-server.js)                         | 实现或公开接口：HELPER_ADDON_ENV、WINDOWS_DEV_CONTROL_PROTOCOL、buildHelperOpenArgs、resolveHelperPermissionSubjectIdentity。                                             |
| [broker-socket-path.d.ts](broker-socket-path.d.ts)           | broker-socket-path.d 的实现文件。                                                                                                                                         |
| [broker-socket-path.js](broker-socket-path.js)               | broker-socket-path 的实现文件。                                                                                                                                           |
| [broker.d.ts](broker.d.ts)                                   | 实现或公开接口：HelperHealth、CallBrokerMethodArgs、ProbeHelperHealthOptions、SocketPathOptions。                                                                         |
| [broker.js](broker.js)                                       | 公共 Host 通过 broker 入口采用参数契约；占位包仍拒绝真实能力调用。                                                                                                        |
| [frame-contract.d.ts](frame-contract.d.ts)                   | 实现或公开接口：OFFICIAL_CUA_FRAME_INTEGRITY_META_KEY、OFFICIAL_CUA_FRAME_MODEL_CONTENT_PROTECTION、OFFICIAL_CUA_IMAGE_INLINE_BASE64_BYTES、OfficialCuaFrameAttestation。 |
| [frame-contract.js](frame-contract.js)                       | 实现或公开接口：OFFICIAL_CUA_FRAME_INTEGRITY_META_KEY、OFFICIAL_CUA_FRAME_MODEL_CONTENT_PROTECTION、OFFICIAL_CUA_IMAGE_INLINE_BASE64_BYTES、isOfficialCuaImageRefText。   |
| [host-display-contract.d.ts](host-display-contract.d.ts)     | host-display-contract.d 的实现文件。                                                                                                                                      |
| [host-display-contract.js](host-display-contract.js)         | 实现或公开接口：CUA_APP_ASSOCIATIONS_META_KEY、CUA_APP_ASSOCIATIONS_MAX_META_BYTES。                                                                                      |
| [index.d.ts](index.d.ts)                                     | 公共 broker 读取 MCP 元数据；占位返回同一结果类型，避免导出后丢失契约。                                                                                                   |
| [index.js](index.js)                                         | 实现或公开接口：createComputerUseRuntime。                                                                                                                                |
| [package.json](package.json)                                 | @zcode/zcode-cua 的包信息、依赖和开发命令。                                                                                                                               |
| [pip-session-node.d.ts](pip-session-node.d.ts)               | 实现或公开接口：PipSessionApplyResult、PipSessionClientOptions、PipSessionClient。                                                                                        |
| [pip-session-node.js](pip-session-node.js)                   | 实现或公开接口：createPipSessionClient。                                                                                                                                  |
| [pip-session.d.ts](pip-session.d.ts)                         | 实现或公开接口：PipSessionEvent。                                                                                                                                         |
| [pip-session.js](pip-session.js)                             | pip-session 的实现文件。                                                                                                                                                  |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                                                                                                          |
| [request-access-contract.d.ts](request-access-contract.d.ts) | 实现或公开接口：CuaRequestAccessStatus、CuaRequestAccessStatusSchema。                                                                                                    |
| [request-access-contract.js](request-access-contract.js)     | 实现或公开接口：CUA_REQUEST_ACCESS_STATUS_META_KEY、cuaRequestAccessStatusSchema。                                                                                        |
| [tsconfig.json](tsconfig.json)                               | 本模块的 TypeScript 编译、类型检查或构建范围。                                                                                                                            |
| [vitest.config.ts](vitest.config.ts)                         | 根单测引用固定项目入口；缺失此文件会在发现公共测试前直接终止。                                                                                                            |

<!-- qingqi-directory-index:end -->
