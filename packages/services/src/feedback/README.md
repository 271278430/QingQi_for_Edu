# feedback

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 feedback 实现源码。

### 文件

| 文件                                           | 简要说明                                                                          |
| ---------------------------------------------- | --------------------------------------------------------------------------------- |
| [compactLogArchive.ts](compactLogArchive.ts)   | 实现或公开接口：prepareCompactLogArchive、cleanupLogArchive。                     |
| [feedback.ts](feedback.ts)                     | 实现或公开接口：FeedbackUploadProgress、FeedbackCreateOptions、IFeedbackService。 |
| [feedbackHttpClient.ts](feedbackHttpClient.ts) | 反馈接口返回的业务失败，保留服务端 code 供调用方区分处理。                        |
| [feedbackLogArchive.ts](feedbackLogArchive.ts) | 只收集根目录下列出的文件名；用于允许单文件进入归档的配置入口。                    |
| [feedbackService.ts](feedbackService.ts)       | 匿名请求使用的 access token；登录请求没有。                                       |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                  |

<!-- qingqi-directory-index:end -->
