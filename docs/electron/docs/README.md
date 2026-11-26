# Official Guides

> **ZCode repository notice:** this directory is a vendored Electron upstream development-branch
> snapshot, not the authoritative documentation for this project's installed Electron **44.7.0**.
> It contains APIs and behavior from a different upstream snapshot. For implementation decisions,
> use the installed `node_modules/electron/electron.d.ts` and Electron v44.7.0 tagged documentation.
> This mirror is not self-contained and is not built as part of the ZCode workspace.

Please make sure that you use the documents that match your Electron version.
The version number should be a part of the page URL. If it's not, you are
probably using the documentation of a development branch which may contain API
changes that are not compatible with your Electron version. To view older
versions of the documentation, you can
[browse by tag](https://github.com/electron/electron/tree/v1.4.0)
on GitHub by opening the "Switch branches/tags" dropdown and selecting the tag
that matches your version.

## FAQ

There are questions that are asked quite often. Check this out before creating
an issue:

- [Electron FAQ](faq.md)

## Guides and Tutorials

### Getting started

- [Introduction](tutorial/introduction.md)
- [Process Model](tutorial/process-model.md)

### Learning the basics

- Adding Features to Your App
  - [Notifications](tutorial/notifications.md)
  - [Recent Documents](tutorial/recent-documents.md)
  - [Application Progress](tutorial/progress-bar.md)
  - [Custom Dock Menu](tutorial/macos-dock.md)
  - [Custom Windows Taskbar](tutorial/windows-taskbar.md)
  - [Custom Linux Desktop Actions](tutorial/linux-desktop-actions.md)
  - [Keyboard Shortcuts](tutorial/keyboard-shortcuts.md)
  - [Offline/Online Detection](tutorial/online-offline-events.md)
  - [Represented File for macOS BrowserWindows](tutorial/represented-file.md)
  - [Native File Drag & Drop](tutorial/native-file-drag-drop.md)
  - [Navigation History](tutorial/navigation-history.md)
  - [Offscreen Rendering](tutorial/offscreen-rendering.md)
  - [Dark Mode](tutorial/dark-mode.md)
  - [Web embeds in Electron](tutorial/web-embeds.md)
- [Boilerplates and CLIs](tutorial/boilerplates-and-clis.md)
  - [Boilerplate vs CLI](tutorial/boilerplates-and-clis.md#boilerplate-vs-cli)
  - [Electron Forge](tutorial/boilerplates-and-clis.md#electron-forge)
  - [electron-builder](tutorial/boilerplates-and-clis.md#electron-builder)
  - [electron-react-boilerplate](tutorial/boilerplates-and-clis.md#electron-react-boilerplate)
  - [Other Tools and Boilerplates](tutorial/boilerplates-and-clis.md#other-tools-and-boilerplates)

### Advanced steps

- Application Architecture
  - [Using Native Node.js Modules](tutorial/using-native-node-modules.md)
  - [Performance Strategies](tutorial/performance.md)
  - [Security Strategies](tutorial/security.md)
  - [Process Sandboxing](tutorial/sandbox.md)
- [Accessibility](tutorial/accessibility.md)
  - [Manually Enabling Accessibility Features](tutorial/accessibility.md#manually-enabling-accessibility-features)
- [Testing and Debugging](tutorial/application-debugging.md)
  - [Debugging the Main Process](tutorial/debugging-main-process.md)
  - [Debugging with Visual Studio Code](tutorial/debugging-vscode.md)
  - [Testing on Headless CI Systems (Travis, Jenkins)](tutorial/testing-on-headless-ci.md)
  - [DevTools Extension](tutorial/devtools-extension.md)
  - [Automated Testing](tutorial/automated-testing.md)
  - [REPL](tutorial/repl.md)
- [Distribution](tutorial/application-distribution.md)
  - [Code Signing](tutorial/code-signing.md)
  - [Mac App Store](tutorial/mac-app-store-submission-guide.md)
  - [Windows Store](tutorial/windows-store-guide.md)
  - [Snapcraft](tutorial/snapcraft.md)
  - [ASAR Archives](tutorial/asar-archives.md)
- [Updates](tutorial/updates.md)
- [Getting Support](tutorial/support.md)

## Detailed Tutorials

These individual tutorials expand on topics discussed in the guide above.

- [Installing Electron](tutorial/installation.md)
  - [Proxies](tutorial/installation.md#proxies)
  - [Custom Mirrors and Caches](tutorial/installation.md#custom-mirrors-and-caches)
  - [Troubleshooting](tutorial/installation.md#troubleshooting)
- Electron Releases & Developer Feedback
  - [Versioning Policy](tutorial/electron-versioning.md)
  - [Release Timelines](tutorial/electron-timelines.md)

---

- [Glossary of Terms](glossary.md)

## API References

- [Process Object](api/process.md)
- [Supported Command Line Switches](api/command-line-switches.md)
- [Environment Variables](api/environment-variables.md)
- [Chrome Extensions Support](api/extensions.md)
- [Breaking API Changes](breaking-changes.md)

### Custom Web Features:

- [`-electron-corner-smoothing` CSS Rule](api/corner-smoothing-css.md)
- [`<webview>` Tag](api/webview-tag.md)
- [`window.open` Function](api/window-open.md)

### Modules for the Main Process:

- [app](api/app.md)
- [autoUpdater](api/auto-updater.md)
- [BaseWindow](api/base-window.md)
- [BrowserWindow](api/browser-window.md)
- [contentTracing](api/content-tracing.md)
- [desktopCapturer](api/desktop-capturer.md)
- [dialog](api/dialog.md)
- [globalShortcut](api/global-shortcut.md)
- [inAppPurchase](api/in-app-purchase.md)
- [ImageView](api/image-view.md)
- [ipcMain](api/ipc-main.md)
- [Menu](api/menu.md)
- [MenuItem](api/menu-item.md)
- [MessageChannelMain](api/message-channel-main.md)
- [MessagePortMain](api/message-port-main.md)
- [nativeTheme](api/native-theme.md)
- [net](api/net.md)
- [netLog](api/net-log.md)
- [Notification](api/notification.md)
- [powerMonitor](api/power-monitor.md)
- [powerSaveBlocker](api/power-save-blocker.md)
- [protocol](api/protocol.md)
- [pushNotifications](api/push-notifications.md)
- [safeStorage](api/safe-storage.md)
- [screen](api/screen.md)
- [ServiceWorkerMain](api/service-worker-main.md)
- [session](api/session.md)
- [ShareMenu](api/share-menu.md)
- [systemPreferences](api/system-preferences.md)
- [TouchBar](api/touch-bar.md)
- [Tray](api/tray.md)
- [utilityProcess](api/utility-process.md)
- [View](api/view.md)
- [webContents](api/web-contents.md)
- [webFrameMain](api/web-frame-main.md)
- [WebContentsView](api/web-contents-view.md)

### Modules for the Renderer Process (Web Page):

- [contextBridge](api/context-bridge.md)
- [ipcRenderer](api/ipc-renderer.md)
- [webFrame](api/web-frame.md)

### Modules for Both Processes:

- [clipboard](api/clipboard.md) (non-sandboxed renderers only)
- [crashReporter](api/crash-reporter.md)
- [nativeImage](api/native-image.md)
- [shell](api/shell.md) (non-sandboxed renderers only)

## Development

See [development/README.md](development/README.md)

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

docs 设计与维护文档，属于 docs 目录。

### 子目录

| 目录                                  | 存放内容                                     |
| ------------------------------------- | -------------------------------------------- |
| [api/](api/README.md)                 | api 设计与维护文档，属于 docs 目录。         |
| [development/](development/README.md) | development 设计与维护文档，属于 docs 目录。 |
| [fiddles/](fiddles/README.md)         | fiddles 设计与维护文档，属于 docs 目录。     |
| [images/](images/README.md)           | images 设计与维护文档，属于 docs 目录。      |
| [tutorial/](tutorial/README.md)       | tutorial 设计与维护文档，属于 docs 目录。    |

### 文件

| 文件                                               | 简要说明                                                            |
| -------------------------------------------------- | ------------------------------------------------------------------- |
| [.eslintrc.json](.eslintrc.json)                   | .eslintrc 的数据或配置定义。                                        |
| [api-history.schema.json](api-history.schema.json) | api-history.schema 的数据或配置定义。                               |
| [breaking-changes.md](breaking-changes.md)         | Breaking Changes：说明文档。                                        |
| [CLAUDE.md](CLAUDE.md)                             | Electron Documentation Guide（上游快照，非 ZCode 指令）：说明文档。 |
| [experimental.md](experimental.md)                 | Experimental APIs：说明文档。                                       |
| [faq.md](faq.md)                                   | Electron FAQ：说明文档。                                            |
| [glossary.md](glossary.md)                         | Glossary：说明文档。                                                |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                    |
| [why-electron.md](why-electron.md)                 | Why Electron：说明文档。                                            |

<!-- qingqi-directory-index:end -->
