# model

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/contracts 基础工程中的 model 实现源码。

### 文件

| 文件                                           | 简要说明                                                                                                     |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [content-protection.ts](content-protection.ts) | Model content protection (generic host vocabulary)                                                           |
| [image-media.ts](image-media.ts)               | 实现或公开接口：DetectedImageMediaType、ParsedImageDataUrl、ParseImageDataUrlOptions、detectImageMediaType。 |
| [index.ts](index.ts)                           | Model Protocol - provider-neutral model contracts                                                            |
| [invocation-context.ts](invocation-context.ts) | \* 会话用过的能力标签，adapter 写入归因 header `x-zcode-session-features`                                    |
| [media-policy.ts](media-policy.ts)             | PDF 提取文本为空字符串时，adapter 会回退发送 file-data。                                                     |
| [model.ts](model.ts)                           | 仅保留 CLI 公共类型名，字段来自同一数据 Schema，不复制 Provider 配置定义。                                   |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                                             |

<!-- qingqi-directory-index:end -->
