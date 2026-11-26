# lib

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 lib 工程脚本。

### 文件

| 文件                                                                       | 简要说明                                                                          |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [conversation-telemetry-parity.d.mts](conversation-telemetry-parity.d.mts) | conversation-telemetry-parity.d 模块的资源或工程文件。                            |
| [conversation-telemetry-parity.mjs](conversation-telemetry-parity.mjs)     | 纯数据比较器：可由 Vitest、WDIO 或独立 Node runner 采用，不依赖测试框架全局变量。 |
| [e2e-promotion-audit-transaction.mjs](e2e-promotion-audit-transaction.mjs) | Bug 根因：promotion 过去会先留下 formal 文件，再由后续命令发现准入失败，          |
| [e2e-promotion-spec-imports.mjs](e2e-promotion-spec-imports.mjs)           | Bug 根因：pending spec 比 formal spec 多两层目录，只重写 helpers/pages 会让       |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                  |
| [telemetry-field-contract.d.mts](telemetry-field-contract.d.mts)           | telemetry-field-contract.d 模块的资源或工程文件。                                 |
| [telemetry-field-contract.mjs](telemetry-field-contract.mjs)               | 读取语法节点，避免注释、字符串、类型声明中的同名字段被当成生产赋值。              |

<!-- qingqi-directory-index:end -->
