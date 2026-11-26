# bot-project-runtime

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 bot project runtime 实现源码。

### 文件

| 文件                                       | 简要说明                                                                  |
| ------------------------------------------ | ------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：example。                                                 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                  |
| [contract.ts](contract.ts)                 | 物理连接的代际标识；router 不拥有或关闭该连接。                           |
| [index.ts](index.ts)                       | 只转发当前物理 owner 的未来事件；不缓存、不补发手机 replayable 内容。     |
| [module.ts](module.ts)                     | \* bot-project-runtime 模块清单（architecture-governance managed 模块）。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                          |

<!-- qingqi-directory-index:end -->
