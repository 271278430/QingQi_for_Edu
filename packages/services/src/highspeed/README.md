# highspeed

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 highspeed 实现源码。

### 文件

| 文件                                                   | 简要说明                                                                                          |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| [highspeedCard.ts](highspeedCard.ts)                   | 实现或公开接口：IHighspeedCardService。                                                           |
| [highspeedCardService.ts](highspeedCardService.ts)     | \* 加速推理的动态鉴权材料。加速走 /api/v1/highspeed/ 网关，与 draw 采用同一套 Coding Plan         |
| [highspeedHttpTransport.ts](highspeedHttpTransport.ts) | \* 后台请求生命期上限。必须明确大于 1s 发送等待预算：慢但合法的 draw 仍能在后台落地供下一轮使用； |
| [highspeedMockTransport.ts](highspeedMockTransport.ts) | 实现或公开接口：createHighspeedMockTransport。                                                    |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                                  |

<!-- qingqi-directory-index:end -->
