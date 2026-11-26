# provider-tool-rounds

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 provider tool rounds 验收与回归场景。

### 文件

| 文件                                   | 简要说明                                                                                             |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| [contract.test.ts](contract.test.ts)   | 端到端行为（流切轮、落盘、卡片事件、冷恢复）见 adapters/tests/provider-builtin-tool-rounds.test.ts。 |
| [hydration.test.ts](hydration.test.ts) | 冷恢复边界：一条持久化 assistant 里服务端内置工具轮次与本地工具、正文、作废标记、异常结果的组合。    |
| [README.md](README.md)                 | 本目录用途、子目录与逐文件说明。                                                                     |

<!-- qingqi-directory-index:end -->
