# providers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 providers 测试场景。

### 文件

| 文件                                                                                         | 简要说明                                                                                           |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [coding-plan-entitlement-presentation.test.ts](coding-plan-entitlement-presentation.test.ts) | 模拟保存的商品与当前订阅不同，但团队组织/项目未变的启动恢复。                                      |
| [provider-builtin-refresh-failure.test.ts](provider-builtin-refresh-failure.test.ts)         | 仅替换远端配置响应；权益、项目身份等仍走既有隔离账号控制面。                                       |
| [provider-builtin-refresh.test.ts](provider-builtin-refresh.test.ts)                         | afterSession 会清理隔离工作区，验收证据必须写到报告目录。                                          |
| [provider-connectivity-prompt.test.ts](provider-connectivity-prompt.test.ts)                 | synthetic / fast-text：固定白名单禁止在 Prompt 中追加 E2E marker，按独立模型 ID 和完整 body 识别。 |
| [provider-family-responsive.test.ts](provider-family-responsive.test.ts)                     | 响应式导航有隐藏副本，必须操作真实可见元素。                                                       |
| [provider-key-native-open.test.ts](provider-key-native-open.test.ts)                         | 只记录本例 canary 路径，不收集默认浏览器的 Cookie、历史或其他页面。                                |
| [provider-model-smart-config.test.ts](provider-model-smart-config.test.ts)                   | 高级区展开时仍在裁切并移动能力开关，原生 click 成功不保证点中目标。                                |
| [provider-opencode-go.test.ts](provider-opencode-go.test.ts)                                 | 目录扩容曾使固定数量断言失效；从本次加载的配置核对完整成员，避免数量相同但型号遗漏。               |
| [provider-plan-navigation-labels.test.ts](provider-plan-navigation-labels.test.ts)           | 响应式布局保留隐藏副本，只操作当前可见导航。                                                       |
| [provider-reasoning-fallback.test.ts](provider-reasoning-fallback.test.ts)                   | synthetic / fast-text：白名单固定 Prompt，使用独立模型 ID 识别测试请求。                           |
| [provider-settings-write-recovery.test.ts](provider-settings-write-recovery.test.ts)         | 重复成员由真实写入边界拒绝；弹窗不能把“请求已发出”当成保存成功。                                   |
| [README.md](README.md)                                                                       | 本目录用途、子目录与逐文件说明。                                                                   |

<!-- qingqi-directory-index:end -->
