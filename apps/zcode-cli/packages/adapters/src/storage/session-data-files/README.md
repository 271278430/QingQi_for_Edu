# session-data-files

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 session data files 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                          |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | \* cli-session-data-files 标准调用示例：内存版端口，语义与 Node 实现一致（remove 返回删除前大小，重复删除得 0）。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                                          |
| [contract.test.ts](contract.test.ts)       | Node 实现的行为测试在 packages/adapters/tests/session-data-files.test.ts。                                        |
| [contract.ts](contract.ts)                 | cli-session-data-files 对外契约：CLI 存储根下按会话与目录定位的数据文件。                                         |
| [index.ts](index.ts)                       | 返回 `<cli>/memories/projects/<slug>-<hash>/memory`；删除其父目录。                                               |
| [module.ts](module.ts)                     | \* cli-session-data-files 模块清单（architecture-governance managed 模块）。                                      |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                                  |

<!-- qingqi-directory-index:end -->
