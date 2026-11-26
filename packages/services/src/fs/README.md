# fs

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 fs 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                      |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| [atomicFileUtils.ts](atomicFileUtils.ts)   | 路径本身是否存在（lstat，不跟随软链：悬空软链也算存在）。其他错误原样抛出。                                   |
| [fsFaultInjection.ts](fsFaultInjection.ts) | 实现或公开接口：ZCODE_E2E_FS_FAULTS_ENV、ZCODE_E2E_FS_FAULTS_ALLOW_ENV、FsFaultOperation、FsFaultRuleConfig。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                              |

<!-- qingqi-directory-index:end -->
