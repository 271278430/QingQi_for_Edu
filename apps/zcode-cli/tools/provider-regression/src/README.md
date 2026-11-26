# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/provider-regression 基础工程中的 src 实现源码。

### 文件

| 文件                             | 简要说明                                                                         |
| -------------------------------- | -------------------------------------------------------------------------------- |
| [cases.ts](cases.ts)             | 旧编号重复执行同一场景；兼容历史清单，但不重复发起计费请求。                     |
| [cli.ts](cli.ts)                 | 配置解析错误可能含敏感输入，不把原始 Zod/网络异常打印到终端。                    |
| [config.ts](config.ts)           | 缺 Key 仍需解析能力以生成未测清单；占位值绝不进入请求，执行前检查 missingKeys。  |
| [execute.ts](execute.ts)         | 流块可能把 UTF-16 代理对拆开；字符数不能随分块方式变化。                         |
| [html.ts](html.ts)               | 实现或公开接口：parseReport、renderHtmlReport、generateHtmlReport。              |
| [persistence.ts](persistence.ts) | 原实现仅在整轮结束写盘，中断会丢掉全部结果；每次先捕获脱敏快照，再串行原子替换。 |
| [README.md](README.md)           | 本目录用途、子目录与逐文件说明。                                                 |
| [report-cli.ts](report-cli.ts)   | report-cli 的实现文件。                                                          |
| [report.ts](report.ts)           | 通用 Key 前缀只在词边界匹配，避免误删 task-platform 等普通标识中的 sk-。         |
| [run.ts](run.ts)                 | 实现或公开接口：runRegression。                                                  |
| [scheduler.ts](scheduler.ts)     | 同一层的唯一取件游标；错误后停止取件，等待所有在途任务收尾后再抛错。             |
| [session.ts](session.ts)         | 夹具只提供数据；参数校验、执行、历史回传由产品运行时负责。                       |
| [usage.ts](usage.ts)             | 只读取可重放 JSON 请求，不消费 Adapter 持有的 Request。                          |

<!-- qingqi-directory-index:end -->
