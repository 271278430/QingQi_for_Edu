# channels

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 channels 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                         | 简要说明                                                                        |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [feishu-bound-groups-ui.test.ts](feishu-bound-groups-ui.test.ts)             | BOT-E2E-GR-UI-01：真实 Desktop → RPC → Bot repo；无平台凭据，不向真实群发消息。 |
| [feishu-channel-mention.test.ts](feishu-channel-mention.test.ts)             | feishu-channel-mention.test 的实现文件。                                        |
| [feishu-group-collaboration.test.ts](feishu-group-collaboration.test.ts)     | feishu-group-collaboration.test 的实现文件。                                    |
| [feishu-provider-interactions.test.ts](feishu-provider-interactions.test.ts) | feishu-provider-interactions.test 的实现文件。                                  |
| [feishu-topic-interactions.test.ts](feishu-topic-interactions.test.ts)       | feishu-topic-interactions.test 的实现文件。                                     |
| [feishu-topic-runtime.test.ts](feishu-topic-runtime.test.ts)                 | 待用户手动执行。真实 Host/CLI 与 DOM，材料为合成输入；不代表原生飞书验收。      |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                |

<!-- qingqi-directory-index:end -->
