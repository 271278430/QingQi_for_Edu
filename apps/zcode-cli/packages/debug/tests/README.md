# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

debug 基础工程中的 tests 验收与回归场景。

### 文件

| 文件                                                     | 简要说明                                                                           |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [analyzer.test.ts](analyzer.test.ts)                     | analyzer.test 的实现文件。                                                         |
| [api.test.ts](api.test.ts)                               | 漏传 logDir 会扫描操作者的真实日志，导致全量并发时超时；所有数据源都必须指向夹具。 |
| [network-capture.test.ts](network-capture.test.ts)       | network-capture.test 的实现文件。                                                  |
| [observation-events.test.ts](observation-events.test.ts) | observation-events.test 的实现文件。                                               |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                   |

<!-- qingqi-directory-index:end -->
