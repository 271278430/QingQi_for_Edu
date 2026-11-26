# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/provider-node 基础工程中的 src 实现源码。

### 文件

| 文件                                                                                           | 简要说明                                                                                                                                                                    |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [endpoint-scoped-zcode-builtin-source.ts](endpoint-scoped-zcode-builtin-source.ts)             | \* 让 Environment 的 ZCode 控制面 Endpoint 同时决定 Active/LKG 与刷新控制路径。                                                                                             |
| [index.ts](index.ts)                                                                           | index 的实现文件。                                                                                                                                                          |
| [legacy-reasoning-level-renames.ts](legacy-reasoning-level-renames.ts)                         | 一次性改名清单：选择器必须精确匹配 Built-in 原规则，不按模型名猜测。                                                                                                        |
| [legacy-reasoning-level.ts](legacy-reasoning-level.ts)                                         | 只为历史 Selection 恢复已知 Built-in 旧值域；不迁移 Personal 配置或在执行层放宽校验。                                                                                       |
| [model-selection-config-repository.ts](model-selection-config-repository.ts)                   | 默认选择只是 Personal 文件的一个字段；IO、锁和失效通知由同一个 Repository 拥有。                                                                                            |
| [model-selection-facade.ts](model-selection-facade.ts)                                         | Host 与受管理 Worker 共用身份分类；解析仍由纯 Provider Facade 负责。                                                                                                        |
| [personal-provider-config-repository.ts](personal-provider-config-repository.ts)               | 在配置锁内保护最终写入；跨文件调用方负责一致的锁顺序，不能再次取得配置锁。                                                                                                  |
| [provider-config-file-codec.ts](provider-config-file-codec.ts)                                 | 旧编辑器曾把 MFJS 当作手动必填项；隐藏后仅在文件边界识别旧合法形状，                                                                                                        |
| [provider-config-runtime.ts](provider-config-runtime.ts)                                       | 组装一个 Node.js 进程内共享的 ZCode Built-in/Personal Config 运行边界。                                                                                                     |
| [provider-registry-runtime.ts](provider-registry-runtime.ts)                                   | 一个 Node.js 进程内共享的 Config + Registry 生命周期。                                                                                                                      |
| [README.md](README.md)                                                                         | 本目录用途、子目录与逐文件说明。                                                                                                                                            |
| [runtime-paths.ts](runtime-paths.ts)                                                           | 实现或公开接口：ZCODE_BUILTIN_PROVIDER_CONFIG_FILE_ENV、ZCODE_BUILTIN_PROVIDER_BUNDLED_CONFIG_FILE_ENV、ZCODE_PERSONAL_PROVIDER_CONFIG_FILE_ENV、PERSONAL_PROVIDER_CONFIG_F |
| [zcode-builtin-cache-paths.ts](zcode-builtin-cache-paths.ts)                                   | 按平台与 App 版本隔离 Active/LKG；路径本身就是兼容范围。                                                                                                                    |
| [zcode-builtin-download.ts](zcode-builtin-download.ts)                                         | 内网和测试部署也会提供 HTTP 配置地址；协议准入不按产品环境区分。                                                                                                            |
| [zcode-builtin-provider-config-materializer.ts](zcode-builtin-provider-config-materializer.ts) | \* 在环境目录释放唯一随包基线；升级以退出旧进程为前提，不保留历史 hash 副本。                                                                                               |
| [zcode-builtin-provider-config-source.ts](zcode-builtin-provider-config-source.ts)             | Bundled、Active/LKG 与 Remote 共用同一 Release，并最终发布为现有 Config Snapshot。                                                                                          |
| [zcode-builtin-release.ts](zcode-builtin-release.ts)                                           | ZAPI 已退出产品，旧 Remote Release 或 LKG 不能在 Renderer 静态入口删除后                                                                                                    |
| [zcode-builtin-remote-synchronizer.ts](zcode-builtin-remote-synchronizer.ts)                   | Environment 共享控制文件合并多进程刷新；网络期间不持有文件锁。                                                                                                              |

<!-- qingqi-directory-index:end -->
