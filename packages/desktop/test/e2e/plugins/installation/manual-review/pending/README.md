# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                             | 简要说明                                                                         |
| ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| [plugin-builtin-ui-uninstall.test.ts](plugin-builtin-ui-uninstall.test.ts)                       | 旧实现中可恢复条目丢了 componentTypes 的 "ui"，卡片会掉进「生产力」分类分组。    |
| [plugin-cdn-zip-official-cdn-smoke.test.ts](plugin-cdn-zip-official-cdn-smoke.test.ts)           | plugin-cdn-zip-official-cdn-smoke.test 的实现文件。                              |
| [plugin-management-recoverable-failures.test.ts](plugin-management-recoverable-failures.test.ts) | plugin-management-recoverable-failures.test 的实现文件。                         |
| [plugin-update-all-failure.test.ts](plugin-update-all-failure.test.ts)                           | 原因：directory market 同时有来源和 managed 副本；两处移除才会触发真实升级失败。 |
| [README.md](README.md)                                                                           | 本目录用途、子目录与逐文件说明。                                                 |

<!-- qingqi-directory-index:end -->
