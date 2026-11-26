# local-ttft

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 local ttft 实现源码。

### 文件

| 文件                                       | 简要说明                                                                      |
| ------------------------------------------ | ----------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 检查点采用现有协议出口，实际首输出仍由内容帧确认。                            |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                      |
| [contract.test.ts](contract.test.ts)       | contract.test 的实现文件。                                                    |
| [contract.ts](contract.ts)                 | CLI 只提供阶段事实，不决定 accepted input 或内容首帧。                        |
| [module.ts](module.ts)                     | \* local-ttft-cli 模块清单（architecture-governance managed 模块）。          |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                              |
| [recorder.ts](recorder.ts)                 | 无业务裁决权：只跟随 inbox 和 live event，不建立第二份 accepted input queue。 |

<!-- qingqi-directory-index:end -->
