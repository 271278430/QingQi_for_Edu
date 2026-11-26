# project-workspace-navigation

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 project workspace navigation 实现源码。

### 文件

| 文件                                       | 简要说明                                                               |
| ------------------------------------------ | ---------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：openProjectExample。                                   |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                               |
| [contract.ts](contract.ts)                 | 由窗口 Registry admission 返回；本地没有远端 descriptor。              |
| [index.ts](index.ts)                       | 导航必须先有远程项目，不能因设备在线就分配无归属目录和 logical scope。 |
| [module.ts](module.ts)                     | Window Host 项目目录导航；依赖须与 architecture-policy 一致。          |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                       |

<!-- qingqi-directory-index:end -->
