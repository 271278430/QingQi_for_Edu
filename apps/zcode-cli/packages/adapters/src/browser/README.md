# browser

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 browser 实现源码。

### 文件

| 文件                                           | 简要说明                                                                                                    |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [descriptor.ts](descriptor.ts)                 | 实现或公开接口：createManagedCdpDescriptor。                                                                |
| [executable.ts](executable.ts)                 | 延迟加载很关键：Desktop/app-server 路径不会启用 CLI headless，不能因外置依赖缺失而启动失败。                |
| [index.ts](index.ts)                           | 实现或公开接口：ManagedCdpBrowserRuntimeOptions、ManagedCdpBrowserRuntime、createManagedCdpBrowserRuntime。 |
| [page-command.ts](page-command.ts)             | 实现或公开接口：isAllowedManagedBrowserUrl、readManagedPageState、executeManagedPageCommand。               |
| [playwright-command.ts](playwright-command.ts) | 实现或公开接口：evaluatePage、executeManagedPlaywrightAction。                                              |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                                            |
| [request.ts](request.ts)                       | 实现或公开接口：abortError、raceWithAbort、hasSideEffects、classifyError。                                  |
| [session.ts](session.ts)                       | 实现或公开接口：ManagedCdpTab、ManagedCdpSession。                                                          |
| [snapshot.ts](snapshot.ts)                     | \* 这段函数由 Playwright 序列化到页面执行，不能引用模块闭包。Element ref 不写入页面                         |

<!-- qingqi-directory-index:end -->
