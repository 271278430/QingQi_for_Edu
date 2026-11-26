# feedback

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 feedback 实现源码。

### 文件

| 文件                                                                           | 简要说明                                                                                                                       |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| [FeatureRequestDialog.tsx](FeatureRequestDialog.tsx)                           | 实现或公开接口：FeatureRequestDialog、buildFeatureRequestDescription。                                                         |
| [FeedbackBackgroundUploadIndicator.tsx](FeedbackBackgroundUploadIndicator.tsx) | 多个上传任务必须按被点击卡片的 jobId 打开，不能再回退到最后一个活动任务。                                                      |
| [feedbackBadges.tsx](feedbackBadges.tsx)                                       | 两个反馈弹窗曾各自维护星号，导致读屏语义分叉；统一隐藏装饰符号，必填由输入框声明。                                             |
| [FeedbackCenter.tsx](FeedbackCenter.tsx)                                       | 实现或公开接口：FeedbackCenter。                                                                                               |
| [feedbackContactPreference.ts](feedbackContactPreference.ts)                   | localStorage 在隐私模式或 WebView 限制下可能不可用；联系方式记忆失败不能阻断反馈提交。                                         |
| [feedbackFramework.ts](feedbackFramework.ts)                                   | 实现或公开接口：inferFeedbackFrameworkFromAgentProvider。                                                                      |
| [FeedbackHost.tsx](FeedbackHost.tsx)                                           | FeedbackHost 的React 组件。                                                                                                    |
| [feedbackIcons.tsx](feedbackIcons.tsx)                                         | 实现或公开接口：FeedbackBugIcon、FeedbackQuestionIcon、FeedbackIdeaIcon、FeedbackPerformanceIcon。                             |
| [feedbackMeta.ts](feedbackMeta.ts)                                             | 公开反馈接口会把历史「答复关闭」归一为「已归档」返回。                                                                         |
| [FeedbackProcessView.tsx](FeedbackProcessView.tsx)                             | 实现或公开接口：FeedbackProcessView。                                                                                          |
| [feedbackProgress.tsx](feedbackProgress.tsx)                                   | \* 简化的工单流转进度（用户视角）：                                                                                            |
| [feedbackScreenshotDraft.ts](feedbackScreenshotDraft.ts)                       | 实现或公开接口：captureFeedbackScreenshotDraft。                                                                               |
| [FeedbackScreenshotPicker.tsx](FeedbackScreenshotPicker.tsx)                   | 实现或公开接口：ScreenshotAttachmentDraft、FeedbackScreenshotPicker、readScreenshotDraft。                                     |
| [feedbackStore.ts](feedbackStore.ts)                                           | 仅查看指定后台提交时设置；新建反馈必须保持为 null                                                                              |
| [feedbackSubmissionCopy.ts](feedbackSubmissionCopy.ts)                         | 实现或公开接口：useFeedbackSubmissionCopy。                                                                                    |
| [feedbackSubmissionJob.ts](feedbackSubmissionJob.ts)                           | 提交瞬间的用户表单快照，用于按 jobId 重新打开对应反馈。                                                                        |
| [feedbackSubmitDescription.ts](feedbackSubmitDescription.ts)                   | 实现或公开接口：buildFeedbackTitle、buildDeveloperFacingDescription。                                                          |
| [FeedbackSubmitForm.tsx](FeedbackSubmitForm.tsx)                               | 新反馈默认附带诊断日志；显式草稿值保留用户取消勾选及后台恢复时的选择。                                                         |
| [feedbackSubmitModelContext.ts](feedbackSubmitModelContext.ts)                 | 实现或公开接口：FeedbackAgentModelContext、readCurrentAgentModelContext。                                                      |
| [FeedbackSubmitProgressView.tsx](FeedbackSubmitProgressView.tsx)               | 实现或公开接口：SubmitProgressView。                                                                                           |
| [FeedbackSubmitSections.tsx](FeedbackSubmitSections.tsx)                       | Textarea 默认的 field-sizing-content 会让无换行长文本撑大输入框宽度。                                                          |
| [feedbackSubmitSubmission.ts](feedbackSubmitSubmission.ts)                     | 实现或公开接口：DEFAULT_FEEDBACK_TYPE、DEFAULT_FEEDBACK_SEVERITY、DEFAULT_FEEDBACK_MODULE、startSimplifiedFeedbackSubmission。 |
| [FeedbackSupplementComposer.tsx](FeedbackSupplementComposer.tsx)               | Bugfix: 新反馈接口要求 message 附件上传凭证携带 message_id；                                                                   |
| [feedbackTimeline.tsx](feedbackTimeline.tsx)                                   | 用 comment_id 去重：如果事件里已经有 staff_replied/ user_replied 指向某条评论，                                                |
| [feedbackTimelineSummary.ts](feedbackTimelineSummary.ts)                       | Bugfix: 后端事件摘要会持久化为中文，切到英文后历史数据仍会原样透出。                                                           |
| [feedbackUserView.ts](feedbackUserView.ts)                                     | 实现或公开接口：STATUS_USER_HINT、STATUS_USER_HINT_MESSAGE_IDS、formatFeedbackStatusHint、formatRelativeTime。                 |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                                                                               |
| [TicketDetail.tsx](TicketDetail.tsx)                                           | Bugfix: 后端旧数据里可能已经持久化了中文系统摘要；详情页展示时按当前语言重新映射系统事件。                                     |
| [TicketsView.tsx](TicketsView.tsx)                                             | 实现或公开接口：TicketsView、TicketsInitialLoadingState、FeedbackTicketList。                                                  |

<!-- qingqi-directory-index:end -->
