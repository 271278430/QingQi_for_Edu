# windows-runtime-host

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 windows runtime host 实现源码。

### 文件

| 文件                                       | 简要说明                                                                             |
| ------------------------------------------ | ------------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | \* windows-runtime-host 标准调用示例：agent 靠模仿写代码，这里放的就是该模仿的那份。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                             |
| [contract.ts](contract.ts)                 | stdio 属于 CLI；ChildProcess 的 pid/exit 属于原生托管程序，不能当成 CLI 身份。       |
| [index.ts](index.ts)                       | 继续查找明确的部署位置。                                                             |
| [module.ts](module.ts)                     | \* windows-runtime-host 模块清单（architecture-governance managed 模块）。           |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                     |

<!-- qingqi-directory-index:end -->
