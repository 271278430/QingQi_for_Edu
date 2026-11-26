# pluginSandbox

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pluginSandbox 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                         |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| [capture.ts](capture.ts)                   | 实现或公开接口：sandboxCaptureSchema、scaleCaptureRect。                                                         |
| [contract.example.ts](contract.example.ts) | host 登记后 main 返回给 host 的句柄应满足的派生规则。                                                            |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                                         |
| [contract.ts](contract.ts)                 | privileged scheme 与 URL / partition 派生规则。                                                                  |
| [csp.ts](csp.ts)                           | \* App iframe 的 CSP：缺省严格按 MCP Apps 规范块（`default-src 'none'; script-src 'self' 'unsafe-inline'; …`）， |
| [genUiVendor.ts](genUiVendor.ts)           | 每个 partition 共用一份只读清单；不下载、不缓存远程响应。                                                        |
| [guestPolicy.ts](guestPolicy.ts)           | will-attach-webview 时 `params.src` 是否指向插件沙箱 shell。                                                     |
| [host.ts](host.ts)                         | host 进程经 parentPort 登记；返回句柄前完成 partition session 准备。                                             |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                               |
| [module.ts](module.ts)                     | \* plugin-sandbox 模块清单（architecture-governance managed 模块）。                                             |
| [permissionGate.ts](permissionGate.ts)     | \* 沙箱 partition 的权限闸门：Electron request / check handler 只把原始参数交给这里。                            |
| [permissions.ts](permissions.ts)           | \* 页面浏览器权限的纯规则：Electron 权限名 → 规范四键、放行裁决、确认框文案。零 IO，Electron 接线在              |
| [protocol.ts](protocol.ts)                 | 打包产物在 out/renderer 下的文件名（vite input 名 `plugin-sandbox`）。                                           |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                                 |
| [registry.ts](registry.ts)                 | 与 HTML transient activation 一致：一次输入事件给 5 秒窗口，一次性消费。                                         |
| [session.ts](session.ts)                   | \* 每个可信 App 身份一个持久 partition（多个沙箱共享）。首次使用时把 partition session 锁死：                    |

<!-- qingqi-directory-index:end -->
