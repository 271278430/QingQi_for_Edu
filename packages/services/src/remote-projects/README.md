# remote-projects

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 remote projects 实现源码。

### 文件

| 文件                                                 | 简要说明                                                                           |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [connection-membership.ts](connection-membership.ts) | \* 枚举线路找成员行时使用。地址不能构成成员身份（如 IPv6 主机含 `:`）时返回 null： |
| [contract.example.ts](contract.example.ts)           | 实现或公开接口：refreshAddedProject。                                              |
| [CONTRACT.md](CONTRACT.md)                           | 模块职责、公共接口、依赖方向和状态约定。                                           |
| [contract.ts](contract.ts)                           | 连接管理器的当前只读投影，不落 SQLite。                                            |
| [index.ts](index.ts)                                 | 不含连接运行态的本机目录；调用方负责 SQLite 读事务。                               |
| [module.ts](module.ts)                               | \* remote-projects 模块清单（architecture-governance managed 模块）。              |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                   |
| [validation.ts](validation.ts)                       | 实现或公开接口：text、targetSchema、rootSchema、cacheSchema。                      |
| [workspace-settings.ts](workspace-settings.ts)       | 单向兼容投影。输入必须是同一 SQLite 快照，不读取旧集合重建成员。                   |

<!-- qingqi-directory-index:end -->
