# provider-regression

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/provider-regression 基础工程中的 provider regression 模块文件。

### 子目录

| 目录                      | 存放内容                                                       |
| ------------------------- | -------------------------------------------------------------- |
| [src/](src/README.md)     | @zcode/provider-regression 基础工程中的 src 实现源码。         |
| [tests/](tests/README.md) | @zcode/provider-regression 基础工程中的 tests 验收与回归场景。 |

### 文件

| 文件                                       | 简要说明                                                                    |
| ------------------------------------------ | --------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：exampleProviderRegression。                                 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                    |
| [contract.test.ts](contract.test.ts)       | 清单身份在此校验；调用行为由 tests/regression.test.ts 覆盖真实 Adapter 链。 |
| [contract.ts](contract.ts)                 | 测试注入传输；不改全局 fetch，生产默认沿现有 Adapter 网络路径。             |
| [index.ts](index.ts)                       | index 的实现文件。                                                          |
| [module.ts](module.ts)                     | \* provider-regression 模块清单（architecture-governance managed 模块）。   |
| [package.json](package.json)               | @zcode/provider-regression 的包信息、依赖和开发命令。                       |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                            |
| [tsconfig.json](tsconfig.json)             | 本模块的 TypeScript 编译、类型检查或构建范围。                              |
| [vitest.config.ts](vitest.config.ts)       | vitest.config 的实现文件。                                                  |

<!-- qingqi-directory-index:end -->
