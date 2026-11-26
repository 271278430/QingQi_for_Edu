# cua-permission-broker

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 cua permission broker 实现源码。

### 文件

| 文件                                                             | 简要说明                                                                                                                              |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| [cuaAgentAdmissionGate.ts](cuaAgentAdmissionGate.ts)             | \* @deprecated 默认 CUA 装配已不再注入该准入屏障，仅为旧调用方保留兼容导出。                                                          |
| [cuaHelperInstaller.ts](cuaHelperInstaller.ts)                   | \* macOS `lipo -archs` 对 Intel 二进制返回 `x86_64`，而 Node 的运行时架构名是 `x64`。                                                 |
| [cuaPermissionService.ts](cuaPermissionService.ts)               | Computer Use Helper macOS permission service — services-side descriptor registration.                                                 |
| [cuaPipSession.ts](cuaPipSession.ts)                             | 实现或公开接口：CuaPipSessionService、ICuaPipSessionService。                                                                         |
| [cuaPipSessionService.ts](cuaPipSessionService.ts)               | \* 被 `credentials-unavailable` 丢掉的那条 `turn-started`，等凭据可用时补发。                                                         |
| [cuaStandaloneStatusLaunch.ts](cuaStandaloneStatusLaunch.ts)     | 实现或公开接口：resolveStandaloneStatusLaunchCandidates、StandaloneStatusLaunchAppPathOptions、resolveStandaloneStatusLaunchAppPath。 |
| [index.ts](index.ts)                                             | Thin re-export shim — the broker server (51 files, formerly under                                                                     |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                                                                      |
| [stableCuaTransport.ts](stableCuaTransport.ts)                   | 实现或公开接口：StableCuaWinRecipe、getStableCuaPipeName、resolveStableCuaWinRecipe、\_\_resetStableCuaTransportForTest。             |
| [windowsCuaDevHelperHost.ts](windowsCuaDevHelperHost.ts)         | authority 铸造兜底：config-provenance 随机数，与 node.ts 懒分支 spawn 同口径。                                                        |
| [windowsCuaDevRuntime.ts](windowsCuaDevRuntime.ts)               | \* Windows 产品运行时解析边界：                                                                                                       |
| [windowsCuaHelperHostSupport.ts](windowsCuaHelperHostSupport.ts) | Contract constants are single-sourced from the producer package: locally re-declared literals here had drifted risk — a rename in the |

<!-- qingqi-directory-index:end -->
