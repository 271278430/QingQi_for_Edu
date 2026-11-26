# composer

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 composer 测试场景。

### 文件

| 文件                                                                           | 简要说明                                                                                              |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| [chat-input-mention-navigation.test.ts](chat-input-mention-navigation.test.ts) | chat-input-mention-navigation.test 的实现文件。                                                       |
| [composer-voice-input.test.ts](composer-voice-input.test.ts)                   | 规格：docs/chat/composer-voice-input.md。麦克风由 wdio appArgs 的 Chromium 假设备提供（持续正弦音）。 |
| [draft-greeting-layout.test.ts](draft-greeting-layout.test.ts)                 | 上午/中午的短问候语可能无法触发缩字；只调整 renderer 时区，保持真实时钟继续运行。                     |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                                                      |

<!-- qingqi-directory-index:end -->
