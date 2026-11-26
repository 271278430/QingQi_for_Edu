# broadcast

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 broadcast 实现源码。

### 文件

| 文件                                       | 简要说明                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------- |
| [broadcast.ts](broadcast.ts)               | \* 用于跨窗口状态同步。从 Renderer 发出后经 host → main → 其他 host → 对应 Renderer。 |
| [broadcastService.ts](broadcastService.ts) | \* 广播服务 Node 实现 —— 运行在 host process 中                                       |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                      |

<!-- qingqi-directory-index:end -->
