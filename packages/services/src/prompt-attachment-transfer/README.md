# prompt-attachment-transfer

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 prompt attachment transfer 实现源码。

### 文件

| 文件                                                                     | 简要说明                                                              |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| [promptAttachmentTransfer.ts](promptAttachmentTransfer.ts)               | \* Renderer 只消费这个 host 服务，不直接依赖 SSH/WSL/Docker backend。 |
| [promptAttachmentTransferService.ts](promptAttachmentTransferService.ts) | 本地 workspace 保持 localPath 零拷贝，不伪造上传进度。                |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                      |

<!-- qingqi-directory-index:end -->
