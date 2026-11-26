# local-ttft

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 local ttft 实现源码。

### 文件

| 文件                                       | 简要说明                                                                  |
| ------------------------------------------ | ------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 验证入口只接纳关联 ID 与本地出口选择，不携带业务内容。                    |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                  |
| [contract.ts](contract.ts)                 | 本地默认采集不能顺带开启云端；在一次发送开始时冻结出口选择。              |
| [module.ts](module.ts)                     | \* local-ttft-contract 模块清单（architecture-governance managed 模块）。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                          |

<!-- qingqi-directory-index:end -->
