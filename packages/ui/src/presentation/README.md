# presentation

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 presentation 实现源码。

### 文件

| 文件                                                             | 简要说明                                                                                                            |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| [pptxRendererPreviewEngine.ts](pptxRendererPreviewEngine.ts)     | 只为当前页建立 group 文本索引，避免显式选择一页时提前 materialize 整份演示文稿。                                    |
| [presentationElementModel.ts](presentationElementModel.ts)       | 原因：pptx-renderer 对纵向 merge continuation 仍推进 gridSpan，横向                                                 |
| [presentationPdfPrintExport.ts](presentationPdfPrintExport.ts)   | 单图解码失败不阻塞导出（预览同样会失败），整体解码等待设上限                                                        |
| [presentationPreviewControls.ts](presentationPreviewControls.ts) | 实现或公开接口：PPTX_MIN_ZOOM_PERCENT、PPTX_MAX_ZOOM_PERCENT、PPTX_ZOOM_STEP_PERCENT、clampPresentationPageNumber。 |
| [presentationTextSelection.ts](presentationTextSelection.ts)     | \* 从浏览器 Selection 中只提取当前高亮 PPTX 元素 bounds 内的文本。                                                  |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                                                    |
| [types.ts](types.ts)                                             | 后续 DOM 编辑能力的标记边界；第一期不定义尚未验证的编辑命令语义。                                                   |

<!-- qingqi-directory-index:end -->
