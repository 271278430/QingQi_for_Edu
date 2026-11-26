# source-server-workspace

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 source server workspace 实现源码。

### 文件

| 文件                                                                                           | 简要说明                                                                          |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [README.md](README.md)                                                                         | 本目录用途、子目录与逐文件说明。                                                  |
| [sourceServerWorkspace.ts](sourceServerWorkspace.ts)                                           | 实现或公开接口：ISourceServerWorkspaceService。                                   |
| [sourceServerWorkspaceIdentityChannelServer.ts](sourceServerWorkspaceIdentityChannelServer.ts) | Bug 原因：V4 workspace topic 把 identity 编码进复合字符串，旧的整串查表无法命中， |
| [sourceServerWorkspaceService.ts](sourceServerWorkspaceService.ts)                             | 实现或公开接口：createSourceServerWorkspaceService。                              |

<!-- qingqi-directory-index:end -->
