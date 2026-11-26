# credential

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 credential 实现源码。

### 子目录

| 目录                              | 存放内容                                          |
| --------------------------------- | ------------------------------------------------- |
| [providers/](providers/README.md) | @zcode/services 基础工程中的 providers 实现源码。 |

### 文件

| 文件                                         | 简要说明                                                                  |
| -------------------------------------------- | ------------------------------------------------------------------------- |
| [credential.ts](credential.ts)               | \* 提供 key-value 形式的凭据读写。                                        |
| [credentialService.ts](credentialService.ts) | 把损坏 JSON/schema 当成空 store 后继续 save 会清空其他 OAuth 与登录凭据。 |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                          |

<!-- qingqi-directory-index:end -->
