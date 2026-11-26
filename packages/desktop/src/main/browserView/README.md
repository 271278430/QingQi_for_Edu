# browserView

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 browserView 实现源码。

### 文件

| 文件                                                                                         | 简要说明                                                                                                                         |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| [browserCloseTabNotification.ts](browserCloseTabNotification.ts)                             | 构造 main→renderer 关闭通知所需的 owner scope 子集；完整 execution context 的其余字段与 renderer 无关。                          |
| [browserCommandExecutor.ts](browserCommandExecutor.ts)                                       | \* 核心子集：navigate / getState / screenshot / snapshot / click / type / press / scroll；                                       |
| [browserCommandInput.ts](browserCommandInput.ts)                                             | \* 键盘修饰键 → CDP modifiers 位掩码（Alt=1, Control=2, Meta=4, Shift=8）。                                                      |
| [browserCommandInteractionHandlers.ts](browserCommandInteractionHandlers.ts)                 | ref 与坐标 (x,y) 二选一：ref 走 resolveRefCenter（脚本内已 scrollIntoView），(x,y) 直接用作视口坐标。                            |
| [browserCommandPageHandlers.ts](browserCommandPageHandlers.ts)                               | legacy layout metrics 在 Retina guest 中可以是 CSS viewport 的 2 倍，                                                            |
| [browserCommandResult.ts](browserCommandResult.ts)                                           | 构造 ref 未找到的结构化错误（提示先 snapshot）。                                                                                 |
| [browserCommandScripts.ts](browserCommandScripts.ts)                                         | snapshot 默认最多返回的元素数（超出即 truncated=true）。                                                                         |
| [browserCommandState.ts](browserCommandState.ts)                                             | \* 导航命令的默认导航预算为 10s。超时/真实 loadURL 错误必须返回失败，                                                            |
| [browserCommandTypes.ts](browserCommandTypes.ts)                                             | \* 受控视图的最小抽象：executor 只依赖这些方法，便于用 stub 单测（无需真 Electron webContents）。                                |
| [browserGuestManager.ts](browserGuestManager.ts)                                             | 实现或公开接口：BrowserGuestExecutionContext、BrowserGuestManagerResidencyOptions、BrowserGuestManager、sanitizeBrowserMetaUrl。 |
| [browserOperationIndicator.ts](browserOperationIndicator.ts)                                 | \* 只有模型明确打开、显示、激活或改变 viewport 的命令才能重建 renderer 尺寸基线。                                                |
| [browserPlaywrightDomSnapshot.ts](browserPlaywrightDomSnapshot.ts)                           | Playwright 操作预算：顶层 snapshot 3s；IAB iframe 额外总预算 1s。                                                                |
| [browserPlaywrightExecutor.ts](browserPlaywrightExecutor.ts)                                 | 实现或公开接口：handlePlaywrightAction。                                                                                         |
| [browserPlaywrightLocatorExecutor.ts](browserPlaywrightLocatorExecutor.ts)                   | 响应式页面可能同时保留 desktop/mobile 两份 DOM。若仅因匹配数大于 1 就在 host                                                     |
| [browserPlaywrightTimeout.ts](browserPlaywrightTimeout.ts)                                   | \* 内置浏览器对常规 Playwright 操作使用短失败预算：默认 3s，且由调用点给出上限。                                                 |
| [browserRestoreBootstrapProtocol.ts](browserRestoreBootstrapProtocol.ts)                     | \* 恢复态 webview 必须先有 src 才创建 guest，但该导航不能在 pageState 前提交。                                                   |
| [browserScreenshotActivityController.ts](browserScreenshotActivityController.ts)             | 1×1 探测结果：transient 表示 Viz surface 尚未建立这类可自愈的失败。                                                              |
| [browserScreenshotCapture.ts](browserScreenshotCapture.ts)                                   | PNG 的 signature + IHDR 尺寸只占前 24 bytes，避免为了读宽高复制整张大图。                                                        |
| [browserScreenshotSurfaceContracts.ts](browserScreenshotSurfaceContracts.ts)                 | recording 用真实 100% renderer surface；普通截图缺失时保留当前预览比例。                                                         |
| [browserScreenshotSurfaceCoordinator.ts](browserScreenshotSurfaceCoordinator.ts)             | \* Desktop main 与 owner renderer 之间的瞬时截图表面握手。                                                                       |
| [browserScreenshotSurfaceCoordinatorWiring.ts](browserScreenshotSurfaceCoordinatorWiring.ts) | 将截图表面协调器绑定到 owner BrowserWindow；协调器本身不依赖 Electron 全局对象，便于测试。                                       |
| [browserScreenshotTransientRetry.ts](browserScreenshotTransientRetry.ts)                     | Chromium 在 Viz surface 建立前执行 CopyFromSurface 会抛 UnknownVizError；surface                                                 |
| [browserTabRecoveryStore.ts](browserTabRecoveryStore.ts)                                     | \* Electron windowId 跨重启无效；仅在当前进程认领后写入内存副本，落盘固定为 null。                                               |
| [browserTabResidencyCoordinator.ts](browserTabResidencyCoordinator.ts)                       | \* 每个 main 进程实例协调所有 BrowserWindow，但逻辑 tab 上限与 victim 选择都按 window 隔离。                                     |
| [browserTabResidencyPolicy.ts](browserTabResidencyPolicy.ts)                                 | 物理 guest 已 attach 且未 destroyed；logical residency 不能替代此事实。                                                          |
| [browserTransparentWindowBootstrap.ts](browserTransparentWindowBootstrap.ts)                 | \* showInactive 后 Viz surface 建立前的有界 presentation grace：同 turn 读回会抛                                                 |
| [browserVideoRecorder.ts](browserVideoRecorder.ts)                                           | 停止 Chromium MediaRecorder，并等待最后一个 WebM chunk 安全写盘。                                                                |
| [browserVirtualClipboard.ts](browserVirtualClipboard.ts)                                     | 实现或公开接口：BrowserInputExecutionTarget、withFocusedFrameSession、createInputTargetToken、assertFocusedInputTarget。         |
| [browserVirtualClipboardPageScript.ts](browserVirtualClipboardPageScript.ts)                 | 页面虚拟粘贴；此函数源码在目标 page execution context 内执行。                                                                   |
| [electronBrowserWebmRecorder.ts](electronBrowserWebmRecorder.ts)                             | 某个阶段提前失败时，后续阶段 deferred 仍会被 reject；预挂 catch 防止未进入该阶段的                                               |
| [playwrightInjectedScriptSource.ts](playwrightInjectedScriptSource.ts)                       | \* Playwright 1.59 的 generated injected script 未作为 public export 暴露。                                                      |
| [README.md](README.md)                                                                       | 本目录用途、子目录与逐文件说明。                                                                                                 |

<!-- qingqi-directory-index:end -->
