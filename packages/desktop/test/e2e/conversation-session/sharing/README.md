# sharing

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 sharing 测试场景。

### 文件

| 文件                                                                                                         | 简要说明                                                                                   |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| [conversation-session-gen-ui-context.test.ts](conversation-session-gen-ui-context.test.ts)                   | conversation-session-gen-ui-context.test 的实现文件。                                      |
| [conversation-session-gen-ui-tweaks.test.ts](conversation-session-gen-ui-tweaks.test.ts)                     | GUT：Gen UI 卡片的「调整设计」面板（TweakPanel 经 genUiTweakPanelSource 接 Gen UI 页面）。 |
| [conversation-session-share-popover.test.ts](conversation-session-share-popover.test.ts)                     | SHARE34：真实 Desktop 入口与 Composer/选择器联动；不通过测试替身发布公开链接。             |
| [conversation-session-share-publish-import.test.ts](conversation-session-share-publish-import.test.ts)       | 有效期选项来自预检返回的服务端范围，预检完成前不渲染；先等选择器出现再操作。               |
| [conversation-session-share-tool-presentation.test.ts](conversation-session-share-tool-presentation.test.ts) | 验证真实发布 UI 与本地 fake API；人工 review 前只保留 pending，不自行转正。                |
| [README.md](README.md)                                                                                       | 本目录用途、子目录与逐文件说明。                                                           |

<!-- qingqi-directory-index:end -->
