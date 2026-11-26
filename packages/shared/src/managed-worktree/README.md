# managed-worktree

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 managed worktree 实现源码。

### 文件

| 文件                                       | 简要说明                                                                               |
| ------------------------------------------ | -------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 示例：Host 侧用 node:fs/promises 适配只读端口，求一个工作区的 Trust identity。         |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                               |
| [contract.ts](contract.ts)                 | 受管 worktree 共享契约：目录布局（纯路径）与 Hook Trust identity 解析的输入/端口类型。 |
| [index.ts](index.ts)                       | index 的实现文件。                                                                     |
| [layout.ts](layout.ts)                     | 受管 worktree 目录布局（docs/git/worktree.md §5.3）。                                  |
| [module.ts](module.ts)                     | 实现或公开接口：moduleDefinition。                                                     |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                       |
| [trust-identity.ts](trust-identity.ts)     | Hook Trust identity 唯一 resolver（docs/specs/workspace-hook-trust.md D23）。          |

<!-- qingqi-directory-index:end -->
