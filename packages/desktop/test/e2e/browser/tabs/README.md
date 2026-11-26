# tabs

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 tabs 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                     | 简要说明                                                                                    |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [browser-empty-state-deferred-guest.test.ts](browser-empty-state-deferred-guest.test.ts) | Bug 回归：地址草稿不是已确认导航，不能提前裸露或创建 about:blank guest。                    |
| [browser-tab-close-cross-workspace.test.ts](browser-tab-close-cross-workspace.test.ts)   | \* 本 spec 守的是修复承诺对应的端到端场景：main 关闭逻辑 tab 时用户已经切到别的 workspace， |
| [browser-tab-close-idempotent.test.ts](browser-tab-close-idempotent.test.ts)             | 第一次关闭走真实 UI 路径：renderer 先向 main 申请授权，拿到授权后才移除标签。               |
| [browser-tab-residency.test.ts](browser-tab-residency.test.ts)                           | Bug 原因：旧 E2E 要求同时创建 32 个真实 webview，测试 Electron 在第 15 个附近会因           |
| [README.md](README.md)                                                                   | 本目录用途、子目录与逐文件说明。                                                            |

<!-- qingqi-directory-index:end -->
