# window-project-directory

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 window project directory 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                          |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                         | 实现或公开接口：windowProjectDirectoryExample。                                   |
| [CONTRACT.md](CONTRACT.md)                                         | 模块职责、公共接口、依赖方向和状态约定。                                          |
| [contract.ts](contract.ts)                                         | 整组选择，避免把窗口项目与 Source 成员目录或广播混用。                            |
| [index.ts](index.ts)                                               | 远端 scope 曾消费 Source 的项目广播。这里只转发窗口目录变化，不扩大广播读写权限。 |
| [module.ts](module.ts)                                             | \* window-project-directory 模块清单（architecture-governance managed 模块）。    |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                  |
| [webRemoteProjectTreeActivity.ts](webRemoteProjectTreeActivity.ts) | \* 手机项目树的实时待处理交互叠加。                                               |

<!-- qingqi-directory-index:end -->
