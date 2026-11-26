# browser-use

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 browser use 实现源码。

### 文件

| 文件                                                                             | 简要说明                                                                                                                      |
| -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [BrowserDesignFields.tsx](BrowserDesignFields.tsx)                               | 属性面板的数值 / 颜色字段（docs/browser-use/2026-11-03-browser-design-mode-spec.md 第五节）。                                 |
| [BrowserDesignInspector.tsx](BrowserDesignInspector.tsx)                         | 画布右侧固定的属性面板（docs/browser-use/2026-11-03-browser-design-mode-spec.md 第五节）：                                    |
| [browserDesignProperties.ts](browserDesignProperties.ts)                         | 属性面板里能改的样式项与页面身份。纯函数，状态在 useBrowserDesignMode。                                                       |
| [BrowserDesignToolbar.tsx](BrowserDesignToolbar.tsx)                             | 设计工具行（docs/browser-use/2026-11-03-browser-design-mode-spec.md）：属性面板开关、版本、翻页、设备预设。                   |
| [browserElementScreenshot.ts](browserElementScreenshot.ts)                       | 选元素带截图（docs/browser-use/2026-11-03-browser-element-screenshot-and-live-reload-spec.md）。                              |
| [browserPageExport.ts](browserPageExport.ts)                                     | 内置浏览器人类用户「导出 PNG / PDF」（docs/browser-use/2026-10-16-browser-device-presets-and-export-spec.md）。               |
| [browserPermissionCapabilities.ts](browserPermissionCapabilities.ts)             | \* 站点权限设置标签页的能力目录（key = main 持久层的 permission 字符串，                                                      |
| [BrowserPermissionIcon.tsx](BrowserPermissionIcon.tsx)                           | 地址栏与面板采用同一能力字形；图标表示申请能力，不表示设备正在使用。                                                          |
| [BrowserSitePermissionsPage.tsx](BrowserSitePermissionsPage.tsx)                 | 站点权限设置标签页：数据源为 main 站点权限 store，「仅本次」临时态不展示。                                                    |
| [BrowserSiteSettingsEntry.tsx](BrowserSiteSettingsEntry.tsx)                     | \* 地址栏左侧的站点设置入口（spec：docs/browser-use/2026-10-08-embedded-browser-permission-governance-spec.md                 |
| [BrowserUseSidePaneContent.tsx](BrowserUseSidePaneContent.tsx)                   | browser-use 专用 TabsContent：非活动 tab 仅在截图准备期间保留真实合成布局。                                                   |
| [BrowserViewportSurface.tsx](BrowserViewportSurface.tsx)                         | 设计稿页面：深色点阵画布（自由尺寸下可见）                                                                                    |
| [BrowserViewportToolbar.tsx](BrowserViewportToolbar.tsx)                         | 并进设计工具栏同一行时只渲染控件组，行的边框、高度和溢出交给设计工具栏                                                        |
| [browserViewportZoom.ts](browserViewportZoom.ts)                                 | Fit 的画布内边距与 ResponsiveBrowserViewport 的 `p-4` 保持一致。                                                              |
| [EmbeddedBrowserPermissionPrompts.tsx](EmbeddedBrowserPermissionPrompts.tsx)     | \* 内置浏览器权限弹窗层（spec：docs/browser-use/2026-10-08-embedded-browser-permission-governance-spec.md）。                 |
| [HumanBrowserView.tsx](HumanBrowserView.tsx)                                     | Browser 显示边界：普通 human tab 持久化偏好，Agent popup 使用独立默认 viewport。                                              |
| [README.md](README.md)                                                           | 本目录用途、子目录与逐文件说明。                                                                                              |
| [ResponsiveBrowserResizeHandles.tsx](ResponsiveBrowserResizeHandles.tsx)         | 实现或公开接口：RESPONSIVE_BROWSER_VIEWPORT_LIMITS、ResizeDirection、ResizeHandleDirections、ResponsiveBrowserResizeHandles。 |
| [ResponsiveBrowserViewport.tsx](ResponsiveBrowserViewport.tsx)                   | \* 保持同一层 DOM 包装，仅切换 frame 的 CSS 尺寸，避免开关自由尺寸时重建 Electron guest。                                     |
| [UnifiedBrowserView.tsx](UnifiedBrowserView.tsx)                                 | \* UnifiedBrowserView —— 统一浏览器视图（`<webview>` + CDP-on-guest 架构）。                                                  |
| [useBrowserDesignMode.ts](useBrowserDesignMode.ts)                               | 设计工具的状态 owner（docs/browser-use/2026-11-03-browser-design-mode-spec.md）：每个浏览器 tab 一份。                        |
| [useBrowserDesignRuntime.ts](useBrowserDesignRuntime.ts)                         | 设计工具的宿主 ↔ 页面通信（docs/browser-use/2026-11-03-browser-design-mode-spec.md 第二节）。                                 |
| [useBrowserDesignSourceWriter.ts](useBrowserDesignSourceWriter.ts)               | 属性面板写回源文件与撤销（docs/browser-use/2026-11-03-browser-design-mode-spec.md 第五节）。                                  |
| [useBrowserFileLiveReload.ts](useBrowserFileLiveReload.ts)                       | 内置浏览器 file:// 页面自动刷新（docs/browser-use/2026-11-03-browser-element-screenshot-and-live-reload-spec.md）。           |
| [useBrowserPageExport.ts](useBrowserPageExport.ts)                               | \* Browser 工具栏「导出为 PNG / PDF」的接线：可用条件、同 tab 互斥与结果提示。                                                |
| [useBrowserResizeOperationWarning.ts](useBrowserResizeOperationWarning.ts)       | \* 在与 tab 鼠标图标相同的 Browser Use active 周期内监听浏览器区域尺寸。                                                      |
| [useBrowserScreenshotSurfaceReady.ts](useBrowserScreenshotSurfaceReady.ts)       | requestAnimationFrame 回调里上报，而 ZCode 主窗口被遮挡/最小化时 Chromium 会冻结                                              |
| [useBrowserScreenshotSurfaceRequest.ts](useBrowserScreenshotSurfaceRequest.ts)   | \* 跨进程恢复的 browser tab（browser: 前缀）在 renderer registry 里的 browserId                                               |
| [useBrowserUseOperationActive.ts](useBrowserUseOperationActive.ts)               | \* 采用 browser-use tab 鼠标图标的 5 秒 operation deadline。                                                                  |
| [useDesktopZoomFactor.ts](useDesktopZoomFactor.ts)                               | \* 读取当前窗口的 Electron 页面缩放；Web 装配返回 level 0，因此自然回退为 factor 1。                                          |
| [useEmbeddedBrowserWheelChain.ts](useEmbeddedBrowserWheelChain.ts)               | 把 guest 已到边界的二维 wheel 续接到自由尺寸宿主画布。                                                                        |
| [useResponsiveBrowserViewportControl.ts](useResponsiveBrowserViewportControl.ts) | viewport 事件也会用于模式内尺寸同步；仅在 false → true 时重置，避免覆盖用户刚选的固定缩放。                                   |

<!-- qingqi-directory-index:end -->
