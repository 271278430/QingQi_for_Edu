# providers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 providers 实现源码。

### 子目录

| 目录                  | 存放内容                                    |
| --------------------- | ------------------------------------------- |
| [api/](api/README.md) | @zcode/services 基础工程中的 api 实现源码。 |

### 文件

| 文件                                                       | 简要说明                                                                          |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [codexConfigToml.ts](codexConfigToml.ts)                   | 实现或公开接口：stringifyCodexConfigToml。                                        |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                                  |
| [sourceHeaders.ts](sourceHeaders.ts)                       | deviceMid 的生命周期由 desktop/telemetry 负责；这里仅采用已存在值，不生成新身份。 |
| [zaiBusinessTokenResolver.ts](zaiBusinessTokenResolver.ts) | 实现或公开接口：ZaiBusinessTokenResolver。                                        |

<!-- qingqi-directory-index:end -->
