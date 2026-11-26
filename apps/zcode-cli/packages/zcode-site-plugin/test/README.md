# test

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/zcode-site-plugin 基础工程中的 test 测试场景。

### 文件

| 文件                                       | 简要说明                                                                                                         |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                                 |
| [stage.test.mjs](stage.test.mjs)           | packStage / checkStage 测试：在临时目录里搭 stage，检查产物包内容、契约检查和本地启动检查。                      |
| [zcode-site.test.mjs](zcode-site.test.mjs) | zcode-site CLI 测试：用内存里的 Sites API 替身（按 api/openapi.yaml 的状态机）代替 zcode-server 和后面的控制面。 |

<!-- qingqi-directory-index:end -->
