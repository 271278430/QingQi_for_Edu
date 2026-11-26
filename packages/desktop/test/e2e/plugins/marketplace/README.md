# marketplace

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 marketplace 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                 | 简要说明                                                                                   |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [plugin-localization-creator.test.ts](plugin-localization-creator.test.ts)                           | plugin-localization-creator.test 的实现文件。                                              |
| [plugin-management-discovery-presentation.test.ts](plugin-management-discovery-presentation.test.ts) | plugin-management-discovery-presentation.test 的实现文件。                                 |
| [plugin-management-installed-menu-layout.test.ts](plugin-management-installed-menu-layout.test.ts)   | 内置插件默认已安装，只需在 Workspace 配置里显式启用即可得到 enabledSource=workspace，      |
| [plugin-management-ui-market.test.ts](plugin-management-ui-market.test.ts)                           | 每个评审步骤截图后停留，录像里能看清稳定态；同时记录时间点供生成字幕。                     |
| [plugin-store-auto-refresh-on-enter.test.ts](plugin-store-auto-refresh-on-enter.test.ts)             | 本例验证真实官方市场刷新，需要可访问公网 CDN；模型 replay 不替代市场 HTTP 请求。           |
| [plugin-store-auto-refresh-throttled.test.ts](plugin-store-auto-refresh-throttled.test.ts)           | 自动刷新若被误触发，operationId 会立刻置为 marketplace:update:\*；等一个远大于 UI 调度延迟 |
| [README.md](README.md)                                                                               | 本目录用途、子目录与逐文件说明。                                                           |

<!-- qingqi-directory-index:end -->
