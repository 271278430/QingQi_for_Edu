# shortcuts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 shortcuts 测试场景。

### 文件

| 文件                                                                         | 简要说明                                                                                   |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                           |
| [shortcut-settings-key-search.test.ts](shortcut-settings-key-search.test.ts) | \* 快捷键「按组合键搜索」E2E（spec docs/desktop/shortcut-settings-spec.md §8/§10）：       |
| [shortcut-settings-realkeys.test.ts](shortcut-settings-realkeys.test.ts)     | \* 快捷键设置真实按键 E2E：browser.keys() 走 CDP 真实输入管线（与合成 KeyboardEvent 不同， |
| [shortcut-settings-rebind.test.ts](shortcut-settings-rebind.test.ts)         | \* 快捷键设置 E2E（spec docs/desktop/shortcut-settings-spec.md §10）：                     |

<!-- qingqi-directory-index:end -->
