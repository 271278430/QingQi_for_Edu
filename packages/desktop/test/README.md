# test

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 test 测试场景。

### 子目录

| 目录                            | 存放内容                                              |
| ------------------------------- | ----------------------------------------------------- |
| [e2e/](e2e/README.md)           | @zcode/desktop 基础工程中的 e2e 测试场景。            |
| [fixtures/](fixtures/README.md) | @zcode/desktop 基础工程中的 fixtures 测试夹具与样例。 |
| [mocks/](mocks/README.md)       | @zcode/desktop 基础工程中的 mocks 测试场景。          |

### 文件

| 文件                                                                                       | 简要说明                                                                                                     |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| [agent-crash-diagnostic.node.test.ts](agent-crash-diagnostic.node.test.ts)                 | perf_agent_crash 的退出诊断回归。App 业务单测已退役（docs/testing/unit-test-quality.md）；                   |
| [app-asar-repack.test.ts](app-asar-repack.test.ts)                                         | app-asar-repack.test 的实现文件。                                                                            |
| [build-native-search-tools.test.ts](build-native-search-tools.test.ts)                     | 内网依赖源由环境显式配置；用中性主机，测试不依赖仓库默认的内网地址（开源导出里默认地址为空）。               |
| [bundledNpmAssets.test.ts](bundledNpmAssets.test.ts)                                       | 按 npm registry tarball 布局（顶层 package/）打一个最小 npm 包。                                             |
| [bundleMirrorFallback.test.ts](bundleMirrorFallback.test.ts)                               | 模拟未配置内网依赖源的构建环境（例如开源构建）：内网地址解析抛错。                                           |
| [cdnPreloadScript.test.ts](cdnPreloadScript.test.ts)                                       | cdn-preload.sh 是纯 bash 脚本，Windows 上没有原生 bash 环境（或行为不一致），跳过整个测试套件。              |
| [chromedriverPreflight.test.ts](chromedriverPreflight.test.ts)                             | chromedriverPreflight.test 的实现文件。                                                                      |
| [clientScenesMockServer.test.ts](clientScenesMockServer.test.ts)                           | clientScenesMockServer.test 的实现文件。                                                                     |
| [codeCommandRecorder.test.ts](codeCommandRecorder.test.ts)                                 | codeCommandRecorder.test 的实现文件。                                                                        |
| [codingPlanDataPlaneResponse.test.ts](codingPlanDataPlaneResponse.test.ts)                 | codingPlanDataPlaneResponse.test 的实现文件。                                                                |
| [codingPlanE2EMockEnv.test.ts](codingPlanE2EMockEnv.test.ts)                               | codingPlanE2EMockEnv.test 的实现文件。                                                                       |
| [codingPlanUpgradeMockServer.test.ts](codingPlanUpgradeMockServer.test.ts)                 | codingPlanUpgradeMockServer.test 的实现文件。                                                                |
| [confirmedProcess.test.ts](confirmedProcess.test.ts)                                       | confirmedProcess.test 的实现文件。                                                                           |
| [conversationSessionChatRootSnapshot.test.ts](conversationSessionChatRootSnapshot.test.ts) | Bug 根因：snapshot helper 增加 pane 内 Stop 查询后，旧测试桩仍只实现                                         |
| [conversationSessionNetwork.test.ts](conversationSessionNetwork.test.ts)                   | conversationSessionNetwork.test 的实现文件。                                                                 |
| [conversationShareMockRoute.test.ts](conversationShareMockRoute.test.ts)                   | 非 UTF-8 字节用于证明 HTTP 适配器没有先解码字符串再重新编码文件。                                            |
| [conversationTelemetryParity.test.ts](conversationTelemetryParity.test.ts)                 | conversationTelemetryParity.test 的实现文件。                                                                |
| [conversationTurnEvidence.test.ts](conversationTurnEvidence.test.ts)                       | conversationTurnEvidence.test 的实现文件。                                                                   |
| [credential-keyring-assets.test.ts](credential-keyring-assets.test.ts)                     | 实现或公开接口：open。                                                                                       |
| [credentialFault.test.ts](credentialFault.test.ts)                                         | credentialFault.test 的实现文件。                                                                            |
| [customOpenAIProviderStore.test.ts](customOpenAIProviderStore.test.ts)                     | customOpenAIProviderStore.test 的实现文件。                                                                  |
| [desktop-native-package-policy.test.ts](desktop-native-package-policy.test.ts)             | 其余已知全平台变体必须全部裁剪（含跨 OS 与同 OS 异架构）。                                                   |
| [desktopAgentBytecode.test.ts](desktopAgentBytecode.test.ts)                               | 不应出现在字节码产物中的源码注释                                                                             |
| [desktopAppCliConfig.test.ts](desktopAppCliConfig.test.ts)                                 | desktopAppCliConfig.test 的实现文件。                                                                        |
| [desktopAppLexicalInputAdmission.test.ts](desktopAppLexicalInputAdmission.test.ts)         | jsdom 不实现该浏览器属性；根据真实 DOM 属性模拟可编辑状态。                                                  |
| [desktopAppTestIdLookup.test.ts](desktopAppTestIdLookup.test.ts)                           | desktopAppTestIdLookup.test 的实现文件。                                                                     |
| [desktopAppWorkspaceReadiness.test.ts](desktopAppWorkspaceReadiness.test.ts)               | 路径徽标的上下文信息改由 tooltip 承载，DOM 不再有 title；只认数据属性锚点。                                  |
| [desktopE2EContainerScript.test.ts](desktopE2EContainerScript.test.ts)                     | desktopE2EContainerScript.test 的实现文件。                                                                  |
| [desktopProductIdentity.test.ts](desktopProductIdentity.test.ts)                           | 合并上游发布提交只对齐当前版本，不恢复上游旧版本，也不重算依赖锁。                                           |
| [devDesktopRemoteProdScript.test.ts](devDesktopRemoteProdScript.test.ts)                   | devDesktopRemoteProdScript.test 的实现文件。                                                                 |
| [devElectronAppBundle.test.ts](devElectronAppBundle.test.ts)                               | Windows 普通用户无符号链接权限（需开发者模式），fs.symlink EPERM；覆盖由 CI Linux 承担。                     |
| [devStartupReadyState.test.ts](devStartupReadyState.test.ts)                               | 扩展进程是独立 tsup target（docs/plugins/extension-host.md §12.1），不复制 scheduler 未接 ready 标记的遗漏。 |
| [devWatchBlacklist.test.ts](devWatchBlacklist.test.ts)                                     | devWatchBlacklist.test 的实现文件。                                                                          |
| [download-native-search-tools.test.ts](download-native-search-tools.test.ts)               | download-native-search-tools.test 的实现文件。                                                               |
| [dynamicWorkflowConfigMockServer.test.ts](dynamicWorkflowConfigMockServer.test.ts)         | dynamicWorkflowConfigMockServer.test 的实现文件。                                                            |
| [e2eAllCoverageRunner.test.ts](e2eAllCoverageRunner.test.ts)                               | 仓库不再提供共享 key：示例文件只列变量名，真实 key 只能来自 shell 或本机 .env.e2e.local。                    |
| [e2eAppOutputStage.test.ts](e2eAppOutputStage.test.ts)                                     | e2eAppOutputStage.test 的实现文件。                                                                          |
| [e2eAtomicJsonFile.test.ts](e2eAtomicJsonFile.test.ts)                                     | e2eAtomicJsonFile.test 的实现文件。                                                                          |
| [e2eBashPrefixPermissionShim.test.ts](e2eBashPrefixPermissionShim.test.ts)                 | e2eBashPrefixPermissionShim.test 的实现文件。                                                                |
| [e2eBeforeSessionSetup.test.ts](e2eBeforeSessionSetup.test.ts)                             | e2eBeforeSessionSetup.test 的实现文件。                                                                      |
| [e2eChromedriverServer.test.ts](e2eChromedriverServer.test.ts)                             | e2eChromedriverServer.test 的实现文件。                                                                      |
| [e2eConversationPreparation.test.ts](e2eConversationPreparation.test.ts)                   | 修复原因：准备流程末尾会等待 fixture workspace 的 slash 目录写入 session store；                             |
| [e2eCoverageHeatmap.test.ts](e2eCoverageHeatmap.test.ts)                                   | e2eCoverageHeatmap.test 的实现文件。                                                                         |
| [e2eDesktopBuildCache.test.ts](e2eDesktopBuildCache.test.ts)                               | Vite 配置同时包含 serve/build；Scan 仅用于 serve，不应让生产构建缓存失效。                                   |
| [e2eDraftRegenerationResend.test.ts](e2eDraftRegenerationResend.test.ts)                   | wdio beforeTest 在每个 case 开始时调用。                                                                     |
| [e2eElectronBinary.test.ts](e2eElectronBinary.test.ts)                                     | e2eElectronBinary.test 的实现文件。                                                                          |
| [e2eElectronReload.test.ts](e2eElectronReload.test.ts)                                     | e2eElectronReload.test 的实现文件。                                                                          |
| [e2eElectronServiceLifecycle.test.ts](e2eElectronServiceLifecycle.test.ts)                 | Bug 根因：上游 9.2.1 的 ContextId Promise 成功 resolve 后没有取消 timeout，                                  |
| [e2eElectronStorage.test.ts](e2eElectronStorage.test.ts)                                   | e2eElectronStorage.test 的实现文件。                                                                         |
| [e2eElectronWindowRecorder.test.ts](e2eElectronWindowRecorder.test.ts)                     | e2eElectronWindowRecorder.test 的实现文件。                                                                  |
| [e2eFailureArtifacts.test.ts](e2eFailureArtifacts.test.ts)                                 | e2eFailureArtifacts.test 的实现文件。                                                                        |
| [e2eInfrastructureLifecycle.test.ts](e2eInfrastructureLifecycle.test.ts)                   | e2eInfrastructureLifecycle.test 的实现文件。                                                                 |
| [e2eModelProviderReplayContract.test.ts](e2eModelProviderReplayContract.test.ts)           | Bug 根因：Coding Plan spec 判定已从 wdio.conf.ts 抽到独立 helper，继续扫描入口                               |
| [e2eNetworkCaptureRedaction.test.ts](e2eNetworkCaptureRedaction.test.ts)                   | e2eNetworkCaptureRedaction.test 的实现文件。                                                                 |
| [e2eNetworkCaptureReplay.test.ts](e2eNetworkCaptureReplay.test.ts)                         | e2eNetworkCaptureReplay.test 的实现文件。                                                                    |
| [e2eNodeCoverageNormalization.test.ts](e2eNodeCoverageNormalization.test.ts)               | 实现或公开接口：covered、lazy。                                                                              |
| [e2eProcessCleanup.test.ts](e2eProcessCleanup.test.ts)                                     | Bugfix: dev watcher 会清空共享 out；Electron 必须从 runId 隔离副本启动。                                     |
| [e2ePromotionAuditTransaction.test.ts](e2ePromotionAuditTransaction.test.ts)               | e2ePromotionAuditTransaction.test 的实现文件。                                                               |
| [e2eProviderConfigSeedBoundary.test.ts](e2eProviderConfigSeedBoundary.test.ts)             | 这里只约束 Provider seed 的写入边界。其他 E2E（例如 workspace plugin）也会                                   |
| [e2eProviderEndpoint.test.ts](e2eProviderEndpoint.test.ts)                                 | 普通用例是否切控制面属于请求安全实现（开源版为空）；这里只验证公共 helper 原样委托。                         |
| [e2eRemoteSessionDatabaseFault.test.ts](e2eRemoteSessionDatabaseFault.test.ts)             | 故障目标是 Linux 容器；用本机 Bash 和临时目录执行真实命令，避免碰触用户的会话库。                            |
| [e2eRendererBridgeRootHook.test.ts](e2eRendererBridgeRootHook.test.ts)                     | e2eRendererBridgeRootHook.test 的实现文件。                                                                  |
| [e2eReportingErrorClassification.test.ts](e2eReportingErrorClassification.test.ts)         | e2eReportingErrorClassification.test 的实现文件。                                                            |
| [e2eReportingLifecycle.test.ts](e2eReportingLifecycle.test.ts)                             | e2eReportingLifecycle.test 的实现文件。                                                                      |
| [e2eReportingSummarySkipped.test.ts](e2eReportingSummarySkipped.test.ts)                   | e2eReportingSummarySkipped.test 的实现文件。                                                                 |
| [e2eRuntimePaths.test.ts](e2eRuntimePaths.test.ts)                                         | 这条守卫约束的是「Desktop E2E 自己的 runtime 文件不许落在本机系统 /tmp」。                                   |
| [e2eSourceEvidence.test.ts](e2eSourceEvidence.test.ts)                                     | e2eSourceEvidence.test 的实现文件。                                                                          |
| [e2eSpecAdmission.test.ts](e2eSpecAdmission.test.ts)                                       | 转正后领域可以没有候选；发现规则必须使用独立 fixture，不能依赖仓库一直留有 pending。                         |
| [e2eSpecResolution.test.ts](e2eSpecResolution.test.ts)                                     | e2eSpecResolution.test 的实现文件。                                                                          |
| [e2eSqliteReadiness.test.ts](e2eSqliteReadiness.test.ts)                                   | e2eSqliteReadiness.test 的实现文件。                                                                         |
| [e2eSshRemoteReleaseAssets.test.ts](e2eSshRemoteReleaseAssets.test.ts)                     | 与 stage:remote-assets（remoteAssetRelease.ts collectSourceServerRemoteReleaseArchives）                     |
| [e2eStartupCredentials.test.ts](e2eStartupCredentials.test.ts)                             | e2eStartupCredentials.test 的实现文件。                                                                      |
| [e2eToolFullAccess.test.ts](e2eToolFullAccess.test.ts)                                     | e2eToolFullAccess.test 的实现文件。                                                                          |
| [e2eUICoverageCollector.test.ts](e2eUICoverageCollector.test.ts)                           | e2eUICoverageCollector.test 的实现文件。                                                                     |
| [e2eUnreadContextContract.test.ts](e2eUnreadContextContract.test.ts)                       | 执行实际配置表达式；其它专项布尔门禁均关闭，避免为测试import启动整套WDIO。                                   |
| [e2eV4TurnCompletion.test.ts](e2eV4TurnCompletion.test.ts)                                 | e2eV4TurnCompletion.test 的实现文件。                                                                        |
| [e2eV4WindowSize.test.ts](e2eV4WindowSize.test.ts)                                         | e2eV4WindowSize.test 的实现文件。                                                                            |
| [e2eWindowsRuntimeHostPreflight.test.ts](e2eWindowsRuntimeHostPreflight.test.ts)           | Bug 根因：Windows 上 Agent CLI 只能经过 zcode-runtime-host.exe 启动，而 E2E 只跑                             |
| [e2eWindowTargetBinding.test.ts](e2eWindowTargetBinding.test.ts)                           | e2eWindowTargetBinding.test 的实现文件。                                                                     |
| [e2eWorkerEnvironmentResolution.test.ts](e2eWorkerEnvironmentResolution.test.ts)           | 数据存储路径切换后的密钥登记只在真实系统库上有意义，同样不能注入托管密钥。                                   |
| [e2eWorkerIsolation.test.ts](e2eWorkerIsolation.test.ts)                                   | Bugfix: launcher 的完整请求列表不能决定当前 worker 的 credential/provider fixture。                          |
| [electronBuilderLanguages.test.ts](electronBuilderLanguages.test.ts)                       | Windows/Linux：locales/<name>.pak                                                                            |
| [electronBuilderLinuxPackageTargets.test.ts](electronBuilderLinuxPackageTargets.test.ts)   | Linux 打包目标契约：rpm 是 deb 之外的安装分发格式，不能改变既有更新链路。                                    |
| [electronBuilderSecurity.test.ts](electronBuilderSecurity.test.ts)                         | 用锁定版本的真实更新器消费生成配置，确认不再落入缺失 publisherName 的免检分支。                              |
| [ensureElectronRuntime.test.ts](ensureElectronRuntime.test.ts)                             | ensureElectronRuntime.test 的实现文件。                                                                      |
| [genUiPresentationClipboard.test.ts](genUiPresentationClipboard.test.ts)                   | genUiPresentationClipboard.test 的实现文件。                                                                 |
| [highspeedE2EMockEnv.test.ts](highspeedE2EMockEnv.test.ts)                                 | highspeedE2EMockEnv.test 的实现文件。                                                                        |
| [macElectronLocales.test.ts](macElectronLocales.test.ts)                                   | macElectronLocales.test 的实现文件。                                                                         |
| [macosReleaseAppDoctor.test.ts](macosReleaseAppDoctor.test.ts)                             | Test selection must not inherit a developer's active dev/preview helper variant.                             |
| [macosUpdateManifest.test.ts](macosUpdateManifest.test.ts)                                 | macosUpdateManifest.test 的实现文件。                                                                        |
| [mcpAppsHostRunner.test.ts](mcpAppsHostRunner.test.ts)                                     | mcpAppsHostRunner.test 的实现文件。                                                                          |
| [miseToolchainEnv.test.ts](miseToolchainEnv.test.ts)                                       | 修复原因：Windows 盘符包含 `:`，用 macOS/Linux 宿主分隔符拆分会先破坏模拟的 Windows 路径。                   |
| [mobileLogPull.test.ts](mobileLogPull.test.ts)                                             | mobileLogPull.test 的实现文件。                                                                              |
| [mobileLogPullExport.test.ts](mobileLogPullExport.test.ts)                                 | mobileLogPullExport.test 的实现文件。                                                                        |
| [mobileLogSink.test.ts](mobileLogSink.test.ts)                                             | 续写要么落在最后一个分片，要么因超限再滚一个新分片，但不能覆盖 part 0。                                      |
| [mobileMessageEvidence.test.ts](mobileMessageEvidence.test.ts)                             | mobileMessageEvidence.test 的实现文件。                                                                      |
| [mobilePairingDiagnostics.test.ts](mobilePairingDiagnostics.test.ts)                       | mobilePairingDiagnostics.test 的实现文件。                                                                   |
| [mobileReplayFixture.test.ts](mobileReplayFixture.test.ts)                                 | mobileReplayFixture.test 的实现文件。                                                                        |
| [modelProviderCatalogE2EMock.test.ts](modelProviderCatalogE2EMock.test.ts)                 | modelProviderCatalogE2EMock.test 的实现文件。                                                                |
| [modelProviderRestartConfig.test.ts](modelProviderRestartConfig.test.ts)                   | modelProviderRestartConfig.test 的实现文件。                                                                 |
| [modelProviderRestartRuntime.test.ts](modelProviderRestartRuntime.test.ts)                 | modelProviderRestartRuntime.test 的实现文件。                                                                |
| [modelProviderRestartWorkspace.test.ts](modelProviderRestartWorkspace.test.ts)             | modelProviderRestartWorkspace.test 的实现文件。                                                              |
| [node-pty-package-assets.test.ts](node-pty-package-assets.test.ts)                         | node-pty-package-assets.test 的实现文件。                                                                    |
| [node-pty-rebuild.test.ts](node-pty-rebuild.test.ts)                                       | node-pty-rebuild.test 的实现文件。                                                                           |
| [nsis-install-section-patch.test.ts](nsis-install-section-patch.test.ts)                   | 只修改隔离副本，不污染开发依赖；真实模板锚点变更不能被手写 fixture 掩盖。                                    |
| [packagedPlatformDependencyPrune.test.ts](packagedPlatformDependencyPrune.test.ts)         | packagedPlatformDependencyPrune.test 的实现文件。                                                            |
| [packagedSourcemapCleanup.test.ts](packagedSourcemapCleanup.test.ts)                       | packagedSourcemapCleanup.test 的实现文件。                                                                   |
| [permissionInteractionId.test.ts](permissionInteractionId.test.ts)                         | permissionInteractionId.test 的实现文件。                                                                    |
| [placeholderProducerDetection.test.ts](placeholderProducerDetection.test.ts)               | placeholderProducerDetection.test 的实现文件。                                                               |
| [pluginE2EAdmissionScripts.test.ts](pluginE2EAdmissionScripts.test.ts)                     | 修复原因：pending 与 formal 共用 canonical fixture identity，probe 也必须模拟完整合同。                      |
| [pluginMarketStartupCredentials.test.ts](pluginMarketStartupCredentials.test.ts)           | pluginMarketStartupCredentials.test 的实现文件。                                                             |
| [powershell-command.test.ts](powershell-command.test.ts)                                   | 工程适配器回归：只替换系统进程，仍执行真实临时文件读取与清理。                                               |
| [prepare-native-search-tools.test.ts](prepare-native-search-tools.test.ts)                 | 用可切换的替身模拟“依赖源已配置 / 未配置时抛错”两种环境；已配置时显式注入中性主机，                          |
| [prepareAgentNodeBundle.test.ts](prepareAgentNodeBundle.test.ts)                           | 修复原因：只断言源码包含 rmSync 调用会漏掉缺少导入的 ReferenceError。                                        |
| [projectPointerDrag.test.ts](projectPointerDrag.test.ts)                                   | 模拟 PointerSensor：跨阈值的事件激活，后续事件才更新位移。                                                   |
| [providerPrefix.test.ts](providerPrefix.test.ts)                                           | providerPrefix.test 的实现文件。                                                                             |
| [providerRefreshWorkspace.test.ts](providerRefreshWorkspace.test.ts)                       | providerRefreshWorkspace.test 的实现文件。                                                                   |
| [provisioningSyncEvidence.test.ts](provisioningSyncEvidence.test.ts)                       | provisioningSyncEvidence.test 的实现文件。                                                                   |
| [radixMenuListenerPatch.test.ts](radixMenuListenerPatch.test.ts)                           | ZCT-2114201711710621696 回归守护：@radix-ui/react-menu 的键盘检测 once 监听补丁必须存在。                    |
| [README.md](README.md)                                                                     | 本目录用途、子目录与逐文件说明。                                                                             |
| [releaseChangelogWriter.test.ts](releaseChangelogWriter.test.ts)                           | third change`),                                                                                              |
| [remoteAssetHttpProxy.test.ts](remoteAssetHttpProxy.test.ts)                               | remoteAssetHttpProxy.test 的实现文件。                                                                       |
| [remoteProjectE2EActions.test.ts](remoteProjectE2EActions.test.ts)                         | 项目详情 hover card 会盖住对话区：新建草稿后必须把指针移出项目行。                                           |
| [remoteRendererReadyEvidence.test.ts](remoteRendererReadyEvidence.test.ts)                 | remoteRendererReadyEvidence.test 的实现文件。                                                                |
| [remoteStartupProfile.test.ts](remoteStartupProfile.test.ts)                               | E2E 冷启动的 profile 里没有本地任务；只验证引导记录 fixture 本身是否生效。                                   |
| [remoteToolExecutionEvidence.test.ts](remoteToolExecutionEvidence.test.ts)                 | remoteToolExecutionEvidence.test 的实现文件。                                                                |
| [rendererTypecheckCoverage.test.ts](rendererTypecheckCoverage.test.ts)                     | TypeScript 配置解析器只提供同步文件系统接口；与真实 tsc 共用配置继承和 include 规则。                        |
| [run-production-build.test.ts](run-production-build.test.ts)                               | Windows 上 normalize会把 /repo/ 前缀转成 E:\repo\，导致路径匹配失败                                          |
| [sharpComputerUseRequirement.test.ts](sharpComputerUseRequirement.test.ts)                 | sharpComputerUseRequirement.test 的实现文件。                                                                |
| [signWindowsHook.test.ts](signWindowsHook.test.ts)                                         | 内置模块的 CJS 导出对象是全局单例，钩子在调用点 require，                                                    |
| [sourceServerReleaseFaults.test.ts](sourceServerReleaseFaults.test.ts)                     | sourceServerReleaseFaults.test 的实现文件。                                                                  |
| [sourceServerUpdateFixture.test.ts](sourceServerUpdateFixture.test.ts)                     | sourceServerUpdateFixture.test 的实现文件。                                                                  |
| [spawn-command.test.ts](spawn-command.test.ts)                                             | spawn-command.test 的实现文件。                                                                              |
| [ssh-remote-p0-config.test.ts](ssh-remote-p0-config.test.ts)                               | ssh-remote-p0-config.test 的实现文件。                                                                       |
| [sshConnectionCompletion.test.ts](sshConnectionCompletion.test.ts)                         | 虚拟轮询只控制浏览器边界；独立 VM 执行实际 helper 回调，避免复制被测状态机。                                 |
| [sshControlCommandTimeout.test.ts](sshControlCommandTimeout.test.ts)                       | sshControlCommandTimeout.test 的实现文件。                                                                   |
| [sshDirectoryFlow.test.ts](sshDirectoryFlow.test.ts)                                       | 使用独立 VM 执行真实 browser callback，捕获误用 Node 闭包常量的问题。                                        |
| [sshFirstConnectionProxy.test.ts](sshFirstConnectionProxy.test.ts)                         | sshFirstConnectionProxy.test 的实现文件。                                                                    |
| [sshHeldResponseProxy.test.ts](sshHeldResponseProxy.test.ts)                               | sshHeldResponseProxy.test 的实现文件。                                                                       |
| [sshHostProbe.test.ts](sshHostProbe.test.ts)                                               | sshHostProbe.test 的实现文件。                                                                               |
| [sshLifecycleProjectDraft.test.ts](sshLifecycleProjectDraft.test.ts)                       | 全局新建按产品合同切换到本地未分类任务，不能冒充远程项目内新建。                                             |
| [sshProjectSelection.test.ts](sshProjectSelection.test.ts)                                 | sshProjectSelection.test 的实现文件。                                                                        |
| [sshRemoteP0Replay.test.ts](sshRemoteP0Replay.test.ts)                                     | sshRemoteP0Replay.test 的实现文件。                                                                          |
| [sshStallableProxy.test.ts](sshStallableProxy.test.ts)                                     | 使用真实 socket.bytesRead 作事件屏障，保证释放前 banner 已被代理读取。                                       |
| [stdioTapCredentialRedaction.test.ts](stdioTapCredentialRedaction.test.ts)                 | stdioTapCredentialRedaction.test 的实现文件。                                                                |
| [storageWorkerDiagnostics.test.ts](storageWorkerDiagnostics.test.ts)                       | storageWorkerDiagnostics.test 的实现文件。                                                                   |
| [subagentConfigProxy.test.ts](subagentConfigProxy.test.ts)                                 | 与 WDIO 注入方式一致：Windows 的 ESM loader 不接受裸绝对路径，预加载必须是 file:// URL。                     |
| [subagentSettingsReadiness.test.ts](subagentSettingsReadiness.test.ts)                     | subagentSettingsReadiness.test 的实现文件。                                                                  |
| [subagentSnapshotWait.test.ts](subagentSnapshotWait.test.ts)                               | 在独立 Node 子进程执行真实测试 preload，避免其文件边界替换污染单测进程。                                     |
| [taskStatusPrinter.test.ts](taskStatusPrinter.test.ts)                                     | taskStatusPrinter.test 的实现文件。                                                                          |
| [taskTitleMarqueeFixture.test.ts](taskTitleMarqueeFixture.test.ts)                         | taskTitleMarqueeFixture.test 的实现文件。                                                                    |
| [telemetryFieldContract.test.ts](telemetryFieldContract.test.ts)                           | 自动归并是认可扩展，不把一次观察提升为每次必填。                                                             |
| [tsupChunkIsolation.test.ts](tsupChunkIsolation.test.ts)                                   | tsupChunkIsolation.test 的实现文件。                                                                         |
| [upstreamProviderPreferenceSeed.test.ts](upstreamProviderPreferenceSeed.test.ts)           | upstreamProviderPreferenceSeed.test 的实现文件。                                                             |
| [upstreamRecordedModels.test.ts](upstreamRecordedModels.test.ts)                           | upstreamRecordedModels.test 的实现文件。                                                                     |
| [upstreamReplayFixtureResolution.test.ts](upstreamReplayFixtureResolution.test.ts)         | upstreamReplayFixtureResolution.test 的实现文件。                                                            |
| [upstreamReplayServer.test.ts](upstreamReplayServer.test.ts)                               | 工具调用简写只在流式请求返回 SSE；下面的断言读取 partial_json，必须声明 stream。                             |
| [viteRendererConfig.test.ts](viteRendererConfig.test.ts)                                   | Windows 跳过：环境配置差异导致断言失败，需要 CI 环境统一配置                                                 |
| [webRemoteControlActionRequests.test.ts](webRemoteControlActionRequests.test.ts)           | webRemoteControlActionRequests.test 的实现文件。                                                             |
| [webRemoteControlAuthGateFixture.test.ts](webRemoteControlAuthGateFixture.test.ts)         | webRemoteControlAuthGateFixture.test 的实现文件。                                                            |
| [webRemoteTerminalProbe.test.ts](webRemoteTerminalProbe.test.ts)                           | 本地 PowerShell 与 POSIX shell 共用 Node CLI；提取实际脚本执行，不复制探针逻辑。                             |
| [windows-e2e-shards.test.ts](windows-e2e-shards.test.ts)                                   | 修复原因：默认 full run 已改为单 shard；路径隔离断言必须显式进入并发分片场景。                               |
| [windowsInstallerCompile.test.ts](windowsInstallerCompile.test.ts)                         | NSIS 自带的 mac 编译器是 x86_64；Apple Silicon 缺少 Rosetta 时只跳过此环境不支持的编译测试。                 |
| [windowsInstallerNshSmoke.test.ts](windowsInstallerNshSmoke.test.ts)                       | windowsInstallerNshSmoke.test 的实现文件。                                                                   |
| [windowsInstallerPreserveFiles.test.ts](windowsInstallerPreserveFiles.test.ts)             | windowsInstallerPreserveFiles.test 的实现文件。                                                              |

<!-- qingqi-directory-index:end -->
