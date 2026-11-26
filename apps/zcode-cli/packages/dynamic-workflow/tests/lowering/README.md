# lowering

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 lowering 验收与回归场景。

### 子目录

| 目录                            | 存放内容                                                       |
| ------------------------------- | -------------------------------------------------------------- |
| [expected/](expected/README.md) | @zcode/dynamic-workflow 基础工程中的 expected 验收与回归场景。 |

### 文件

| 文件                                           | 简要说明                                                                                     |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------- |
| [chained-inline-ask.ts](chained-inline-ask.ts) | chained-inline-ask 的实现文件。                                                              |
| [channel-future.ts](channel-future.ts)         | channel / future lower to host passthroughs (docs/dynamic-workflow/authoring.md, "Streams"): |
| [files-read-glob.ts](files-read-glob.ts)       | files-read-glob 的实现文件。                                                                 |
| [git-and-grep.ts](git-and-grep.ts)             | Multi-argument and optional-argument world reads. What this pins in the lowered output:      |
| [helper-asks.ts](helper-asks.ts)               | helper-asks 的实现文件。                                                                     |
| [holes.ts](holes.ts)                           | Holes lower to `__host.hole(siteId, name, prompt ?? void 0, (__src) => eval(__src), body?)`  |
| [log-only.ts](log-only.ts)                     | log-only 的实现文件。                                                                        |
| [no-facade.ts](no-facade.ts)                   | no-facade 的实现文件。                                                                       |
| [phase-markers.ts](phase-markers.ts)           | Phase markers erase: the sandbox has no `phase` binding to call, so every marker must        |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                             |
| [report-and-log.ts](report-and-log.ts)         | report vs log 在同一份降级产物里各归其位：report 有站点（\_\_host.report(siteId, item)），   |

<!-- qingqi-directory-index:end -->
