# source-server

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server 基础工程中的 source server 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                   |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| [index.ts](index.ts)                                               | index 的实现文件。                                                                         |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                           |
| [sourceServerProbe.ts](sourceServerProbe.ts)                       | Bug 原因：set +e 加末尾 printf 会把 uname 失败覆盖为退出 0，空字段随后被误报为系统不支持。 |
| [sourceServerReleaseDownload.ts](sourceServerReleaseDownload.ts)   | 实现或公开接口：buildSourceServerReleaseDownloadCommand。                                  |
| [sourceServerTransportRuntime.ts](sourceServerTransportRuntime.ts) | Bug 原因：部分 SSH 堡垒机把远端 stderr 合并进 stdout，并在 stdout 结束后才投递。           |
| [transportAdapter.ts](transportAdapter.ts)                         | 当前 release 由显式降级安装时，被替换的版本。                                              |

<!-- qingqi-directory-index:end -->
