# attachments

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 attachments 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                             | 简要说明                                                                                         |
| -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [conversation-session-attachment-only-wire-padding.test.ts](conversation-session-attachment-only-wire-padding.test.ts)           | T06W：附件-only query 的 UI/session 事实保持空正文，只在 provider wire 边界补固定 (no content)。 |
| [conversation-session-attachment-resume.test.ts](conversation-session-attachment-resume.test.ts)                                 | 此用例不测模型选择；通过现有 fixture 设置启动模型，避免依赖已移除的旧 toolbar。                  |
| [conversation-session-attachment-upload-progress-gating.test.ts](conversation-session-attachment-upload-progress-gating.test.ts) | AP02/AP06：浏览器 File eager upload 的圆环进度与发送/队列门禁。                                  |
| [conversation-session-large-text-attachment.test.ts](conversation-session-large-text-attachment.test.ts)                         | Bug 根因：4096 字节样本在中文字符中间结束，旧编码探测拒读后附件正文被过滤。                      |
| [conversation-session-mixed-media-path-strip.test.ts](conversation-session-mixed-media-path-strip.test.ts)                       | conversation-session-mixed-media-path-strip.test 的实现文件。                                    |
| [conversation-session-native-file-picker-attachments.test.ts](conversation-session-native-file-picker-attachments.test.ts)       | 满额时应在打开系统选择器前拦截，监听真实 input click 而非已清空的 files。                        |
| [conversation-session-pasted-image-path-edge-cases.test.ts](conversation-session-pasted-image-path-edge-cases.test.ts)           | 1x1 24-bit BMP。Jimp/provider 链路可解码，但派生缓存故意不支持 image/bmp。                       |
| [conversation-session-pasted-image-path-projection.test.ts](conversation-session-pasted-image-path-projection.test.ts)           | 修复原因：WDIO wrapper 会在进入 test body 前读取 Mocha Runnable timeout；                        |
| [conversation-session-spreadsheet-paste.test.ts](conversation-session-spreadsheet-paste.test.ts)                                 | T11：Excel 多表示剪贴板中的 TSV 文本优先于同 payload 的合成 PNG。                                |
| [conversation-session-v4-attachment-layout.test.ts](conversation-session-v4-attachment-layout.test.ts)                           | 故意先加文件再加媒体，产品展示仍必须按“媒体 → 文件”分层；同类文件保持添加顺序。                  |
| [conversation-session-v4-attachment.test.ts](conversation-session-v4-attachment.test.ts)                                         | T06 + T07 + D12 门禁：仅附件首发；已发送图片预览；latest query 删除附件后 branch cut。           |
| [README.md](README.md)                                                                                                           | 本目录用途、子目录与逐文件说明。                                                                 |

<!-- qingqi-directory-index:end -->
