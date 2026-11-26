# ipc

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server-cli 基础工程中的 ipc 实现源码。

### 文件

| 文件                                 | 简要说明                                                                           |
| ------------------------------------ | ---------------------------------------------------------------------------------- |
| [controlClient.ts](controlClient.ts) | Omit 不对 union 分发：直接 Omit<ControlRequest, "id"> 会丢掉 confirmation/force 等 |
| [controlError.ts](controlError.ts)   | 实现或公开接口：ControlRequestError。                                              |
| [controlServer.ts](controlServer.ts) | server.close() 只会停止新连接，仍然会等待已有连接自然结束。                        |
| [framing.ts](framing.ts)             | 实现或公开接口：encodeJsonLine、JsonLineDecoder。                                  |
| [README.md](README.md)               | 本目录用途、子目录与逐文件说明。                                                   |

<!-- qingqi-directory-index:end -->
