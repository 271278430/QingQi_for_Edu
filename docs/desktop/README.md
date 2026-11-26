# desktop

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

desktop 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                                   | 简要说明                                                    |
| -------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [agent-shutdown-latency.md](agent-shutdown-latency.md)                                 | Agent Shutdown Latency：说明文档。                          |
| [auto-update-auto-download-install.md](auto-update-auto-download-install.md)           | 自动下载并安装更新：说明文档。                              |
| [auto-update-baseline.md](auto-update-baseline.md)                                     | 自动更新临时 Baseline（历史方案）：说明文档。               |
| [auto-update-service-manifest.md](auto-update-service-manifest.md)                     | 桌面端服务端 Manifest 自动更新：说明文档。                  |
| [auto-update-superseded-ready-package.md](auto-update-superseded-ready-package.md)     | 自动更新已下载包被新版本替代：说明文档。                    |
| [build-time-optional-capabilities.md](build-time-optional-capabilities.md)             | 桌面构建期可选能力：说明文档。                              |
| [chromium-hardware-acceleration-setting.md](chromium-hardware-acceleration-setting.md) | Chromium Hardware Acceleration Setting：说明文档。          |
| [computer-use-producer-detection.md](computer-use-producer-detection.md)               | Computer Use producer 检测：说明文档。                      |
| [configurable-data-directory.md](configurable-data-directory.md)                       | 可配置数据存储目录：说明文档。                              |
| [database-migration-startup-gate-plan.md](database-migration-startup-gate-plan.md)     | 进入 ZCode 前统一准备数据库：说明文档。                     |
| [database-startup-implementation-review.md](database-startup-implementation-review.md) | 全局数据库启动：实施复审：说明文档。                        |
| [database-startup-plan-review.md](database-startup-plan-review.md)                     | Todo 145 开工审查与影响面：说明文档。                       |
| [dev-auto-update-test.md](dev-auto-update-test.md)                                     | 桌面端开发态自动更新验证：说明文档。                        |
| [dev-build-watch.md](dev-build-watch.md)                                               | Desktop 开发构建 watcher 范围：说明文档。                   |
| [dev-deep-link.md](dev-deep-link.md)                                                   | Desktop Dev deep link：说明文档。                           |
| [dev-runtime.md](dev-runtime.md)                                                       | Desktop 开发运行时目录：说明文档。                          |
| [e2e-process-lifecycle.md](e2e-process-lifecycle.md)                                   | Desktop E2E Process Lifecycle：说明文档。                   |
| [finder-open-folder-deep-link.md](finder-open-folder-deep-link.md)                     | Desktop Open Folder From System Context Menu：说明文档。    |
| [interface-zoom-removal.md](interface-zoom-removal.md)                                 | Interface Zoom Removal：说明文档。                          |
| [linux-appimage-deep-link.md](linux-appimage-deep-link.md)                             | Linux AppImage Deep Link 回调：说明文档。                   |
| [linux-close-to-tray.md](linux-close-to-tray.md)                                       | Linux 关闭窗口驻留托盘(close-to-tray)Spec：说明文档。       |
| [linux-pacman-package.md](linux-pacman-package.md)                                     | Linux Arch pacman package：说明文档。                       |
| [local-crash-capture.md](local-crash-capture.md)                                       | Desktop 本地 Crash 留档：说明文档。                         |
| [log-export-retention.md](log-export-retention.md)                                     | Log Export Retention：说明文档。                            |
| [macos-dmg-signing-notarization.md](macos-dmg-signing-notarization.md)                 | macOS DMG Signing And Notarization：说明文档。              |
| [main-window-size.md](main-window-size.md)                                             | Desktop Main Window Size：说明文档。                        |
| [oss-cdn-multi-target-migration.md](oss-cdn-multi-target-migration.md)                 | OSS/CDN 多目标迁移：说明文档。                              |
| [post-update-release-notes.md](post-update-release-notes.md)                           | Post-Update Release Notes：说明文档。                       |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                            |
| [release-notification-card.md](release-notification-card.md)                           | ZCode 发版通知卡片：说明文档。                              |
| [shortcut-settings-spec.md](shortcut-settings-spec.md)                                 | 快捷键设置（Shortcut Settings）Spec：说明文档。             |
| [sidebar-zoom-menu.md](sidebar-zoom-menu.md)                                           | Sidebar Zoom Menu：说明文档。                               |
| [startup-critical-path.md](startup-critical-path.md)                                   | Desktop 启动关键路径优化：说明文档。                        |
| [storage-profile-rollback.md](storage-profile-rollback.md)                             | Desktop storage profile 回滚：说明文档。                    |
| [system-zoom-shortcuts.md](system-zoom-shortcuts.md)                                   | System Zoom Shortcuts：说明文档。                           |
| [unread-badge.md](unread-badge.md)                                                     | Desktop 未读 Badge（已退役，并入新 spec）：说明文档。       |
| [update-button-release-notes-hover.md](update-button-release-notes-hover.md)           | Update Button Release Notes Hover：说明文档。               |
| [windows-installer-diagnostics.md](windows-installer-diagnostics.md)                   | Windows 安装器诊断规范：说明文档。                          |
| [windows-installer-overhaul-spec.md](windows-installer-overhaul-spec.md)               | Windows 安装器改造 Spec：说明文档。                         |
| [windows-installer-preserve-files.md](windows-installer-preserve-files.md)             | Windows 更新：安装目录文件保留规范：说明文档。              |
| [windows-taskbar-unread-badge.md](windows-taskbar-unread-badge.md)                     | Windows 任务栏未读角标（taskbar overlay badge）：说明文档。 |
| [windows-update-install-handoff.md](windows-update-install-handoff.md)                 | Windows 更新安装交接：说明文档。                            |
| [windows-vsigntool-timestamp-retry.md](windows-vsigntool-timestamp-retry.md)           | Windows vsigntool 时间戳重试：说明文档。                    |
| [workspace-directory-picker.md](workspace-directory-picker.md)                         | Workspace Directory Picker：说明文档。                      |
| [zcode-desktop-context.md](zcode-desktop-context.md)                                   | ZCode Desktop Context：说明文档。                           |
| [zcode-preview-packaging.md](zcode-preview-packaging.md)                               | ZCode Preview 内部测试包：说明文档。                        |

<!-- qingqi-directory-index:end -->
