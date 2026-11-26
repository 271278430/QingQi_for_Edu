# runtime-tools

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 runtime tools 实现源码。

### 文件

| 文件                                                             | 简要说明                                                                                                 |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [agentProxyEnv.ts](agentProxyEnv.ts)                             | 把设置页的 HTTP 代理、No Proxy 和自定义 CA 翻译成 agent 子进程的环境变量补丁。                           |
| [appCaCert.ts](appCaCert.ts)                                     | app 场景的自签 CA（区别于 debug 抓包代理那套，仅 debug 环境用）。                                        |
| [clientPlatform.ts](clientPlatform.ts)                           | 实现或公开接口：resolveReleaseTarget、resolveReleaseArch、resolveClientConfigPlatform。                  |
| [node-forge.d.ts](node-forge.d.ts)                               | node-forge 1.4.0 没有自带类型，也未安装 @types/node-forge。                                              |
| [nodeEnv.ts](nodeEnv.ts)                                         | NODE_ENV 是用户 shell 和 Node 生态都会使用的通用变量，不能作为 ZCode 运行时判据。                        |
| [providerRuntimeResolver.ts](providerRuntimeResolver.ts)         | 返回 provider + workspace 在应用内的专属配置目录路径                                                     |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                                         |
| [runtimeCommandEnv.ts](runtimeCommandEnv.ts)                     | shell init snapshot 会保存 cd/chpwd/precmd hook 函数；                                                   |
| [runtimeLoginShellEnvCapture.ts](runtimeLoginShellEnvCapture.ts) | GUI / remote service 进程的 PATH 往往不经过 login shell 初始化。                                         |
| [runtimeToolResolver.ts](runtimeToolResolver.ts)                 | 实现或公开接口：prependPathEntries、appendPathEntries、findRuntimeToolBinary、buildRuntimeToolEnvPatch。 |

<!-- qingqi-directory-index:end -->
