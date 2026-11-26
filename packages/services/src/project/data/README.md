# data

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 data 实现源码。

### 文件

| 文件                                         | 简要说明                                                                       |
| -------------------------------------------- | ------------------------------------------------------------------------------ |
| [contract.ts](contract.ts)                   | 项目数据彻底删除的端口与结果类型；IProjectService 的两条数据命令使用这些类型。 |
| [project-data-port.ts](project-data-port.ts) | ProjectDataPort 的装配实现：会话与记忆交给 CLI（v4/storage/sessionData/\*），  |
| [project-data.ts](project-data.ts)           | 彻底删除项目数据（设置 → 项目的「同时删除 ZCode 数据」）。                     |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                               |

<!-- qingqi-directory-index:end -->
