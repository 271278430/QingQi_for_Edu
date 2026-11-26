# input-prediction

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 input prediction 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                          |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | \* remote-input-prediction 标准调用示例：手机发请求前校验参数，桌面回包后校验结果。               |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                          |
| [contract.test.ts](contract.test.ts)       | 线格式细节由 packages/shared/test/zcodeProtocolV4InputPrediction.test.ts 覆盖；这里只守契约边界。 |
| [contract.ts](contract.ts)                 | 手机远控输入预测（ghost hint）的 v4 只读查询线格式。                                              |
| [module.ts](module.ts)                     | \* remote-input-prediction 模块清单（architecture-governance managed 模块）。                     |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                  |

<!-- qingqi-directory-index:end -->
