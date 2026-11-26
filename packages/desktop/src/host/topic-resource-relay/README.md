# topic-resource-relay

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 topic resource relay 实现源码。

### 文件

| 文件                                       | 简要说明                                                     |
| ------------------------------------------ | ------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | 宿主注入实时连接解析函数，窗口释放时调用返回对象的 dispose。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                     |
| [contract.ts](contract.ts)                 | 采用已有通道的读取、校验、取消与释放，不另建请求 owner。     |
| [module.ts](module.ts)                     | Host 负责绑定资源请求的物理连接和当前 logical session。      |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                             |

<!-- qingqi-directory-index:end -->
