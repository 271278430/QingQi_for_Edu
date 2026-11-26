# extensions

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 extensions 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                     | 简要说明                                                                                                              |
| ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [plugin-extension-entries.test.ts](plugin-extension-entries.test.ts)                     | PLM-EXT-P2B：插件入口——主导航 nav.primary 与文件查看器 file.viewer（docs/plugins/extension-host.md §16.3–§16.5）。    |
| [plugin-extension-host-runtime.test.ts](plugin-extension-host-runtime.test.ts)           | PLM-EXT-2A：扩展进程基础设施与插槽（docs/plugins/extension-host.md §6、§12、§15、§16.1、§16.2）。                     |
| [plugin-extension-jarvis-host.test.ts](plugin-extension-jarvis-host.test.ts)             | PLM-EXT-JARVISHOST：Jarvis 要的宿主能力（docs/plugins/extension-host.md §18.1、§18.4 Jarvis 第 1 步）。               |
| [plugin-extension-logs.test.ts](plugin-extension-logs.test.ts)                           | PLM-EXT-P2E：扩展日志控制台（docs/plugins/extension-host.md §16.8、§16.10 第 5 步）。                                 |
| [plugin-extension-mention.test.ts](plugin-extension-mention.test.ts)                     | PLM-EXT-P2C：输入框 `@` 面板的插件分组 composer.mention（docs/plugins/extension-host.md §16.6）。                     |
| [plugin-extension-network.test.ts](plugin-extension-network.test.ts)                     | PLM-EXT-H3：扩展进程的网络跟随设置页（docs/plugins/extension-host.md §12.1、§18.1 H3、§18.4 GitLab 第 2 步）。        |
| [plugin-extension-plugin-project.test.ts](plugin-extension-plugin-project.test.ts)       | PLM-EXT-P3C2：扩展不指定项目建会话时放进插件项目（docs/plugins/extension-host.md §17.4 实现 P3c-2、§18.1 H7、         |
| [plugin-extension-session-approvals.test.ts](plugin-extension-session-approvals.test.ts) | PLM-EXT-P3E：插件回答审批、提问与切换权限模式（docs/plugins/extension-host.md §17.12）。                              |
| [plugin-extension-sessions-read.test.ts](plugin-extension-sessions-read.test.ts)         | PLM-EXT-P3B：扩展的会话读连接与商店安装后的激活确认（docs/plugins/extension-host.md §17.3、§17.5、§17.7、             |
| [plugin-extension-sessions-write.test.ts](plugin-extension-sessions-write.test.ts)       | PLM-EXT-P3C：扩展经 ctx.sessions.\* 写会话（docs/plugins/extension-host.md §17.3、§17.8、§17.10 第 3 步、             |
| [plugin-extension-settings.test.ts](plugin-extension-settings.test.ts)                   | PLM-EXT-P2D：插件设置与扩展的 settings 能力（docs/plugins/extension-host.md §16.7；存储见 CLI spec                    |
| [plugin-extension-start-draft.test.ts](plugin-extension-start-draft.test.ts)             | PLM-EXT-H2：扩展经 workbench.startDraft 开预填草稿（docs/plugins/extension-host.md §18.1 H2、§18.4 GitLab 第 3 步）。 |
| [plugin-extension-views.test.ts](plugin-extension-views.test.ts)                         | PLM-EXT-2B：扩展视图、context 组成与生成速率（docs/plugins/extension-host.md §7.2、§8、§9、§10、§15、§16.11）。       |
| [plugin-store-extension-compat.test.ts](plugin-store-extension-compat.test.ts)           | PLM-EXT-STORE（docs/plugins/plugin-publishing.md §4.3–4.4）：商店按插件 API 版本挡住不兼容的扩展插件，                |
| [README.md](README.md)                                                                   | 本目录用途、子目录与逐文件说明。                                                                                      |

<!-- qingqi-directory-index:end -->
