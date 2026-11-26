# entitlements

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 entitlements 测试场景。

### 文件

| 文件                                                                                                                                       | 简要说明                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| [conversation-session-highspeed-card-admission-retains-draft.test.ts](conversation-session-highspeed-card-admission-retains-draft.test.ts) | \* 在 draw 已命中、sendText 尚未进入 Agent admission 的唯一窗口撤销 Coding Plan。                             |
| [conversation-session-highspeed-card-draw-miss.test.ts](conversation-session-highspeed-card-draw-miss.test.ts)                             | Host Mock 场景：miss（未抽中，next_draw_at = 2 分钟后），见 helpers/highspeed-mock-env.ts。                   |
| [conversation-session-highspeed-card-draw-timeout.test.ts](conversation-session-highspeed-card-draw-timeout.test.ts)                       | Host Mock 场景：hit-after-timeout（draw 1.2s 后才命中，超出 1s 发送预算），见 helpers/highspeed-mock-env.ts。 |
| [conversation-session-highspeed-card-fallback-unlocks-model.test.ts](conversation-session-highspeed-card-fallback-unlocks-model.test.ts)   | Host Mock 场景：hit-invalid-model（按 spec 文件注入，见 helpers/highspeed-mock-env.ts）。                     |
| [conversation-session-highspeed-card.test.ts](conversation-session-highspeed-card.test.ts)                                                 | Host Mock 场景：hit-fast（按 spec 文件注入，见 helpers/highspeed-mock-env.ts）。                              |
| [conversation-session-highspeed-queue-edit.test.ts](conversation-session-highspeed-queue-edit.test.ts)                                     | Host Mock 场景：hit-queue-edit（按 spec 文件注入，见 helpers/highspeed-mock-env.ts）。                        |
| [README.md](README.md)                                                                                                                     | 本目录用途、子目录与逐文件说明。                                                                              |

<!-- qingqi-directory-index:end -->
