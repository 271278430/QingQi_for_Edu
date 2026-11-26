# conversation-share

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 conversation share 实现源码。

### 文件

| 文件                                                                           | 简要说明                                                                             |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| [conversationShare.ts](conversationShare.ts)                                   | 分享有效时长；省略时使用服务端默认值。必须落在预检返回的 ttlOptions 范围内。         |
| [conversationShareArtifactDiscovery.ts](conversationShareArtifactDiscovery.ts) | 非阻断：被跳过的预览结果物，发布照常继续。                                           |
| [conversationShareArtifactSource.ts](conversationShareArtifactSource.ts)       | \* 兜底读失败统一带上 artifact_read_failed 与底层 errno：                            |
| [conversationShareConnectionScope.ts](conversationShareConnectionScope.ts)     | 管理 API 只读写当前 Host 账号自己的分享，不依赖会话 rows，所以桌面各分支都原样透传。 |
| [conversationShareHttpClient.ts](conversationShareHttpClient.ts)               | 服务端响应的请求 ID，用于和后端日志对账。                                            |
| [conversationShareInlineImages.ts](conversationShareInlineImages.ts)           | 内嵌图片转为既有 artifact；预检和发布使用同一份确定性转换，不新增文件读取通道。      |
| [conversationShareIntegrity.ts](conversationShareIntegrity.ts)                 | \* 服务端签发 signed URL 时才有的字段，不参与 artifact set 摘要。                    |
| [conversationSharePublicProjection.ts](conversationSharePublicProjection.ts)   | URI 前缀不能判定文本是否为附件；普通 file/data 文本保留，附件由正式引用校验。        |
| [conversationShareService.ts](conversationShareService.ts)                     | download 兜底不能是裸 fetch（无 AbortSignal/超时）：对象存储连接挂住时导入会停在     |
| [conversationShareWorkflowSnapshot.ts](conversationShareWorkflowSnapshot.ts)   | 合成摘要只用于展示，不能把产物标题再解释为工作区文件引用。                           |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                                     |
| [sharedContextFormatter.ts](sharedContextFormatter.ts)                         | 本 build 认不出、没能进 Markdown 的 row kind；调用方负责记日志。                     |

<!-- qingqi-directory-index:end -->
