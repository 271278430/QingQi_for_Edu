# reporting

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 reporting 测试场景。

### 文件

| 文件                                                   | 简要说明                                                                                                                    |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| [e2e-coverage-heatmap.ts](e2e-coverage-heatmap.ts)     | 实现或公开接口：CoverageHeatmapDomain、CoverageHeatmapFile、CoverageHeatmapDomainData、CoverageHeatmapData。                |
| [e2e-failure-artifacts.ts](e2e-failure-artifacts.ts)   | \* 为失败 case 收集独立的日志增量和窗口视频。                                                                               |
| [e2e-node-coverage.ts](e2e-node-coverage.ts)           | Electron main 必须从进程启动时就继承 NODE_V8_COVERAGE；host 与 CLI                                                          |
| [e2e-reporting-coverage.ts](e2e-reporting-coverage.ts) | 实现或公开接口：renderUICoverageMarkdownSection。                                                                           |
| [e2e-reporting-stats.ts](e2e-reporting-stats.ts)       | 实现或公开接口：NumericStats、BYTES_PER_KB、BYTES_PER_MB、numericStats。                                                    |
| [e2e-reporting-summary.ts](e2e-reporting-summary.ts)   | 实现或公开接口：appendJsonLine、writeJson、normalizeSpecs、sanitizeFilePart。                                               |
| [e2e-reporting-types.ts](e2e-reporting-types.ts)       | 实现或公开接口：ProcessMetricSample、ErrorCategory、E2ELifecyclePhase、E2ELifecycleEvent。                                  |
| [e2e-reporting.ts](e2e-reporting.ts)                   | 修复原因：ChromeDriver target 元数据仍可能显示 file://，但 renderer 的实际                                                  |
| [e2e-source-evidence.ts](e2e-source-evidence.ts)       | 串行小文件读取控制内存；只保存指纹，不将源码或凭据复制到报告。                                                              |
| [e2e-ui-coverage.ts](e2e-ui-coverage.ts)               | 实现或公开接口：ScriptCoverageSummary、SourceFileCoverageSummary、UIRendererCoverageSummary、createE2EUICoverageCollector。 |
| [istanbul-reporting.d.ts](istanbul-reporting.d.ts)     | 修复原因：desktop e2e tsconfig 没有直接引入 Istanbul 的 @types 包，                                                         |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                                                            |

<!-- qingqi-directory-index:end -->
