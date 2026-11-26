# argument-parsing

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/cli 基础工程中的 argument parsing 实现源码。

### 文件

| 文件                                       | 简要说明                                                            |
| ------------------------------------------ | ------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 先提取可变长度工具规则，再交给同一个严格全局解析器。                |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                            |
| [contract.ts](contract.ts)                 | 沿用现有函数签名；这里只声明边界，不复制选项表或参数校验。          |
| [module.ts](module.ts)                     | \* cli-arguments 模块清单（architecture-governance managed 模块）。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                    |

<!-- qingqi-directory-index:end -->
