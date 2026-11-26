# local-ttft

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 local ttft 实现源码。

### 文件

| 文件                                       | 简要说明                                                                 |
| ------------------------------------------ | ------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | 平台通过依赖注入提供日志和原有遥测能力。                                 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                 |
| [contract.ts](contract.ts)                 | 装配桌面本地观测；返回卸载函数，沿用既有云端开关。                       |
| [initialize.ts](initialize.ts)             | 本地日志默认开启；原有云端出口选择在发送开始时冻结。                     |
| [module.ts](module.ts)                     | \* local-ttft-desktop 模块清单（architecture-governance managed 模块）。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                         |

<!-- qingqi-directory-index:end -->
