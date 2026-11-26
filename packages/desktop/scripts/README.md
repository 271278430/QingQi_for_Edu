# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 scripts 工程脚本。

### 子目录

| 目录                                                      | 存放内容                                                     |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| [gen-ui-fixture/](gen-ui-fixture/README.md)               | @zcode/desktop 基础工程中的 gen ui fixture 工程脚本。        |
| [lib/](lib/README.md)                                     | @zcode/desktop 基础工程中的 lib 工程脚本。                   |
| [mcp-apps-host-fixture/](mcp-apps-host-fixture/README.md) | @zcode/desktop 基础工程中的 mcp apps host fixture 工程脚本。 |

### 文件

| 文件                                                                                   | 简要说明                                                                                              |
| -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [admit-conversation-e2e-docker.mjs](admit-conversation-e2e-docker.mjs)                 | admit-conversation-e2e-docker 的实现文件。                                                            |
| [admit-plugin-e2e-docker.mjs](admit-plugin-e2e-docker.mjs)                             | admit-plugin-e2e-docker 的实现文件。                                                                  |
| [app-asar-repack.mjs](app-asar-repack.mjs)                                             | CI 的 TMPDIR 位于隐藏目录 `.tmp`。旧 glob 含 `**/`，@electron/asar 用绝对路径                         |
| [audit-bundle-size.mjs](audit-bundle-size.mjs)                                         | audit-bundle-size 的实现文件。                                                                        |
| [audit-telemetry-fields.mjs](audit-telemetry-fields.mjs)                               | audit-telemetry-fields 的实现文件。                                                                   |
| [auto-update-ca-constraints-smoke.mjs](auto-update-ca-constraints-smoke.mjs)           | 实现或公开接口：EMBEDDED_BROWSER_PARTITION。                                                          |
| [auto-update-install-reentry-smoke.mjs](auto-update-install-reentry-smoke.mjs)         | 真实 Electron 退出时序回归：替换安装器 IO，不接触用户应用、更新缓存或 ShipIt。                        |
| [auto-update-network-smoke.mjs](auto-update-network-smoke.mjs)                         | 用真实 updater Session 和 HTTP executor 验证出口，不改用户配置或下载真实安装包。                      |
| [auto-update-source-security-smoke.mjs](auto-update-source-security-smoke.mjs)         | 普通 Linux Electron 没有 APPIMAGE，打包态模拟不会经过产品的开发态激活逻辑。                           |
| [browser-background-activity-smoke.mjs](browser-background-activity-smoke.mjs)         | executeJavaScript 自身会短时调度少量帧；timer 计数用于补足后台静止的稳定判据。                        |
| [browser-hidden-guest-screenshot-smoke.mjs](browser-hidden-guest-screenshot-smoke.mjs) | 与 controller 一致：先给 Viz 一个有界 presentation grace，再为 owner/guest                            |
| [browser-screenshot-surface-smoke.mjs](browser-screenshot-surface-smoke.mjs)           | browser-screenshot-surface-smoke 的实现文件。                                                         |
| [browser-webm-recording-smoke.mjs](browser-webm-recording-smoke.mjs)                   | MediaRecorder 的流式 WebM 不写 Duration 头，video.duration 是 Infinity。                              |
| [build-macos-window-bounds.mjs](build-macos-window-bounds.mjs)                         | 编译 macOS 窗口 bounds 辅助程序（CUA 权限浮窗的吸附数据源）。                                         |
| [build-metadata.mjs](build-metadata.mjs)                                               | ignore invalid package.json and continue walking up                                                   |
| [build-windows-browser-import-helper.mjs](build-windows-browser-import-helper.mjs)     | build-windows-browser-import-helper 的实现文件。                                                      |
| [bundle.mjs](bundle.mjs)                                                               | 该脚本聚合了打包入口、重试策略、计时与产物校验逻辑，短期内拆文件会影响 CI 稳定性。                    |
| [bundled-npm-assets.mjs](bundled-npm-assets.mjs)                                       | 随包 npm：桌面 agent 跑在 Electron Node 上，用户机器没装 Node 时，stdio MCP 的 npm/npx                |
| [check-e2e-fixtures.mjs](check-e2e-fixtures.mjs)                                       | check-e2e-fixtures 的实现文件。                                                                       |
| [chromedriver-preflight.mjs](chromedriver-preflight.mjs)                               | Electron 的 Chromium 补丁未必发布所有平台驱动；官方要求用同 MAJOR.MINOR.BUILD 查询。                  |
| [cloud-content-mock.d.mts](cloud-content-mock.d.mts)                                   | cloud-content-mock.d 模块的资源或工程文件。                                                           |
| [cloud-content-mock.mjs](cloud-content-mock.mjs)                                       | 显式启动的开发 fixture 服务，不由生产 App 自动开启。                                                  |
| [cloud-content-mock.test.mjs](cloud-content-mock.test.mjs)                             | cloud-content-mock.test 的实现文件。                                                                  |
| [computer-use-producer.mjs](computer-use-producer.mjs)                                 | \* 判定当前安装的 `@zcode/zcode-cua` 是闭源真实 producer 还是开源占位包。                             |
| [conversation-docker-plan.mjs](conversation-docker-plan.mjs)                           | 格式化会在表格与结束标记之间留空行；直接替换标记会把新行写成表外文本。                                |
| [desktop-native-package-policy.mjs](desktop-native-package-policy.mjs)                 | sharp 通过 optionalDependencies 分发全平台二进制变体。electron-builder 26.17 的                       |
| [desktop-product-identity.d.mts](desktop-product-identity.d.mts)                       | desktop-product-identity.d 模块的资源或工程文件。                                                     |
| [desktop-product-identity.mjs](desktop-product-identity.mjs)                           | \* 构建期开关：为真时安装包使用 Preview 身份，而后端环境仍由 `ZCODE_ENV` 单独决定。                   |
| [dev.mjs](dev.mjs)                                                                     | 扩展进程是 Main 按需拉起的独立产物；未就绪就启动 Electron 会让首个 Window Host 拉起失败。             |
| [devElectronAppBundle.mjs](devElectronAppBundle.mjs)                                   | 副本布局版本，见 prepareDevElectronAppBundle 中的指纹说明。                                           |
| [e2e-chromedriver-server.d.mts](e2e-chromedriver-server.d.mts)                         | e2e-chromedriver-server.d 模块的资源或工程文件。                                                      |
| [e2e-chromedriver-server.mjs](e2e-chromedriver-server.mjs)                             | WDIO launcher 已按该版本准备驱动；容器的兼容补丁由预取入口通过 explicitPath 提供。                    |
| [e2e-formal-spec-selection.d.mts](e2e-formal-spec-selection.d.mts)                     | e2e-formal-spec-selection.d 模块的资源或工程文件。                                                    |
| [e2e-formal-spec-selection.mjs](e2e-formal-spec-selection.mjs)                         | 直接读取内部队列会让开源 WDIO 配置加载失败；清单由原队列生成，目标判定保持一致。                      |
| [e2e-mobile-web-server.mjs](e2e-mobile-web-server.mjs)                                 | 端口由夹具传入；"0" 表示独立夹具，从 5174 开始由 Vite 自行绑定空闲端口（Vite 把 0 当作默认端口）。    |
| [e2e-remote-target-specs.json](e2e-remote-target-specs.json)                           | e2e-remote-target-specs 的数据或配置定义。                                                            |
| [e2e-step-process.mjs](e2e-step-process.mjs)                                           | 修复原因：spawn 的 error 过去会 reject Promise.all，导致其他 shard 未等待、manifest 未写入。          |
| [ensure-e2e-desktop-build.d.mts](ensure-e2e-desktop-build.d.mts)                       | ensure-e2e-desktop-build.d 模块的资源或工程文件。                                                     |
| [ensure-e2e-desktop-build.mjs](ensure-e2e-desktop-build.mjs)                           | Bugfix: tsup 会根据 CI 分支或 Tag 判断是否为正式发布构建；这些值必须参与缓存指纹，                    |
| [ensure-electron-runtime.mjs](ensure-electron-runtime.mjs)                             | 新安装入口未配置镜像时会直连 GitHub；仅给安装子进程补既有镜像，避免影响 builder 辅助包下载。          |
| [ensure-local-runtime-assets.mjs](ensure-local-runtime-assets.mjs)                     | Windows Chrome 导入入口未启用，默认 dev 启动不应把可选 helper 当成本地必需资源。                      |
| [gen-ui-e2e.mjs](gen-ui-e2e.mjs)                                                       | gen-ui-e2e 的实现文件。                                                                               |
| [gen-ui-runtime-assets.mjs](gen-ui-runtime-assets.mjs)                                 | Inline 和导出共用实际资源文件，避免维护另一份有细节差异的运行时。                                     |
| [gen-ui-runtime-assets.test.ts](gen-ui-runtime-assets.test.ts)                         | 清单只承载当前资源的完整性数据，避免把无关的构建元数据带入分发包。                                    |
| [gen-ui-vendor-export.test.py](gen-ui-vendor-export.test.py)                           | 实现或公开接口：VendorExportTests。                                                                   |
| [generate-cloud-content-video.cjs](generate-cloud-content-video.cjs)                   | 通过已有 Electron 的 MediaRecorder 生成原创小型 WebM fixture，stdout 输出 base64。                    |
| [koffi-package-assets.mjs](koffi-package-assets.mjs)                                   | Koffi native runtime staging for the bundled CUA MCP server.                                          |
| [mac-electron-locales.mjs](mac-electron-locales.mjs)                                   | macOS Electron locale whitelist and packaged-app guard.                                               |
| [macos-update-manifest.mjs](macos-update-manifest.mjs)                                 | electron-updater 比较 os.release()；macOS 13 对应 Darwin 22，不能填营销版本 13。                      |
| [mcp-apps-host-e2e.mjs](mcp-apps-host-e2e.mjs)                                         | Agent bundle 必须来自本次源码；否则 Electron 用新代码、stdio 却测到旧 dist。                          |
| [mcp-apps-host-options.mjs](mcp-apps-host-options.mjs)                                 | 正式入口不能因拼错参数或混用模式而静默运行其它场景。                                                  |
| [node-pty-package-assets.mjs](node-pty-package-assets.mjs)                             | Linux 包中 node-pty 本体只会查自己的 prebuilds/linux-\*/pty.node，                                    |
| [node-pty-rebuild.mjs](node-pty-rebuild.mjs)                                           | electron-rebuild 会在 Windows 强制 node-gyp build-from-source。                                       |
| [packaged-platform-dependency-prune.mjs](packaged-platform-dependency-prune.mjs)       | 实现或公开接口：pruneIncompatiblePlatformPackages。                                                   |
| [packaged-sourcemap-cleanup.mjs](packaged-sourcemap-cleanup.mjs)                       | 只清理位于行首的 sourceMappingURL 注释。压缩后的 bundle 可能在模板字符串里内嵌                        |
| [patch-nsis-install-section.mjs](patch-nsis-install-section.mjs)                       | \* 给 electron-builder 的安装段补上可见阶段，并开启 NSIS 内置逐文件详情。                             |
| [powershell-command.d.mts](powershell-command.d.mts)                                   | powershell-command.d 模块的资源或工程文件。                                                           |
| [powershell-command.mjs](powershell-command.mjs)                                       | 首次模块导入会向 stderr 写进度 CLIXML；只静默进度，实际错误仍须拒绝更新。                             |
| [prepare-agent-node-bundle.mjs](prepare-agent-node-bundle.mjs)                         | 桌面打包态的 agent 运行时资产：把 agent 的 JS bundle（zcode.cjs）放进 bundled-agents/<platform>/glm， |
| [prepare-runtime-assets.mjs](prepare-runtime-assets.mjs)                               | Windows Chrome 导入入口未启用，默认构建继续编译 helper 会增加 CI 时间和发布签名面。                   |
| [prepare-windows-cua-helper.mjs](prepare-windows-cua-helper.mjs)                       | prepare-windows-cua-helper 的实现文件。                                                               |
| [project-token-retry-after-smoke.mjs](project-token-retry-after-smoke.mjs)             | 真实 HTTP -> ApiClient -> readApiJson -> Host adapter -> shared owner；不替换其中任何解析层。         |
| [promote-conversation-e2e.mjs](promote-conversation-e2e.mjs)                           | promote-conversation-e2e 的实现文件。                                                                 |
| [promote-plugin-e2e.mjs](promote-plugin-e2e.mjs)                                       | promote-plugin-e2e 的实现文件。                                                                       |
| [r3-remote-spec-inventory.mjs](r3-remote-spec-inventory.mjs)                           | R3 远程 e2e 服务器全量队列（harness/remote/run-all-remote.sh）的共享名单与解析：                      |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                                                                      |
| [run-all-e2e-coverage.mjs](run-all-e2e-coverage.mjs)                                   | 仓库不提供供应商地址与 key：两者只来自 shell 或本机 .env.e2e.local，示例文件值留空不参与判断。        |
| [run-e2e-session-lifecycle-stress.mjs](run-e2e-session-lifecycle-stress.mjs)           | 每个 alias 都由同一个 WDIO launcher 派发为独立 worker/session，复现全量                               |
| [run-production-build.mjs](run-production-build.mjs)                                   | tsup / vite 配置里的入口路径都是相对 desktop 包根目录声明的。                                         |
| [run-windows-e2e-shards.mjs](run-windows-e2e-shards.mjs)                               | 修复原因：性能入口固定携带 --shards=10；若显式分片先返回，定向、人工复核、                            |
| [runtime-dependency-closure.mjs](runtime-dependency-closure.mjs)                       | 父包相对解析失败时，继续走 workspace lookup roots 兜底。                                              |
| [sharp-package-assets.mjs](sharp-package-assets.mjs)                                   | Sharp native module staging for the shared node_repl runtime.                                         |
| [sign-windows-hook.cjs](sign-windows-hook.cjs)                                         | 修复原因：electron-builder 26.17 的 pnpm 收集器按 lockfile 图把 sharp 的全平台                        |
| [sign-windows-hook.d.cts](sign-windows-hook.d.cts)                                     | sign-windows-hook.d 模块的资源或工程文件。                                                            |
| [stage-agent-bundle.mjs](stage-agent-bundle.mjs)                                       | Agent bundle 的暂存动作：把 apps/zcode-cli/packages/cli/dist/zcode.cjs 放进                           |
| [target-platform.d.mts](target-platform.d.mts)                                         | target-platform.d 模块的资源或工程文件。                                                              |
| [target-platform.mjs](target-platform.mjs)                                             | 部分 Linux optional native 包声明了 libc=glibc。                                                      |
| [test-installer-nsh-smoke.mjs](test-installer-nsh-smoke.mjs)                           | test-installer-nsh-smoke 的实现文件。                                                                 |
| [test-installer-preserve-files.mjs](test-installer-preserve-files.mjs)                 | 夹具只校验文件字节，不执行该载荷；避免 32 位 NSIS 将 System32 重定向到 SysWOW64。                     |
| [ttft-otlp-receiver.mjs](ttft-otlp-receiver.mjs)                                       | 本地验收接收器：保留最终 OTLP 解码证据，不拦截内部埋点调用。                                          |
| [windows-cua-helper-assets.mjs](windows-cua-helper-assets.mjs)                         | 根因：交叉构建时 process.env 目标可能与 electron-builder 实际 context 不同；                          |
| [windows-update-publisher.mjs](windows-update-publisher.mjs)                           | 当前 electron-updater 缺少 publisherName 时会跳过自定义校验。                                         |
| [write-dev-ready-marker.mjs](write-dev-ready-marker.mjs)                               | scheduler 已成为独立 tsup target，onSuccess 会调用同一 marker 脚本。                                  |

<!-- qingqi-directory-index:end -->
