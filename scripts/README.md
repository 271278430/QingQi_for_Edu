# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

工作区构建、架构、格式、发布和工程检查脚本。

### 子目录

| 目录                                                                  | 存放内容                                                  |
| --------------------------------------------------------------------- | --------------------------------------------------------- |
| [architecture/](architecture/README.md)                               | architecture 工程脚本，属于 scripts 目录。                |
| [dev/](dev/README.md)                                                 | dev 工程脚本，属于 scripts 目录。                         |
| [engineering-tests/](engineering-tests/README.md)                     | engineering tests 工程脚本，属于 scripts 目录。           |
| [lib/](lib/README.md)                                                 | lib 工程脚本，属于 scripts 目录。                         |
| [license-texts/](license-texts/README.md)                             | license texts 工程脚本，属于 scripts 目录。               |
| [native-search-tools-windows/](native-search-tools-windows/README.md) | native search tools windows 工程脚本，属于 scripts 目录。 |
| [release-it/](release-it/README.md)                                   | release it 工程脚本，属于 scripts 目录。                  |
| [test/](test/README.md)                                               | test 测试场景，属于 scripts 目录。                        |
| [windows-runtime-host/](windows-runtime-host/README.md)               | windows runtime host 工程脚本，属于 scripts 目录。        |
| [zcode-distribution/](zcode-distribution/README.md)                   | zcode distribution 工程脚本，属于 scripts 目录。          |

### 文件

| 文件                                                                                         | 简要说明                                                                                                                                           |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [assert-node-version.mjs](assert-node-version.mjs)                                           | assert-node-version 的实现文件。                                                                                                                   |
| [audit-conversation-session-case-coverage.mjs](audit-conversation-session-case-coverage.mjs) | 修复原因：该 override 只用于 node:test 的真实 CLI 集成测试。若生产进程也能注入，                                                                   |
| [audit-zcode-agent-remnants.mjs](audit-zcode-agent-remnants.mjs)                             | audit-zcode-agent-remnants 的实现文件。                                                                                                            |
| [bootstrap-patched-dependencies.mjs](bootstrap-patched-dependencies.mjs)                     | Bug 原因：pnpm 10 + node-linker=hoisted 会把 patch 直接应用到目标目录；下一次                                                                      |
| [bootstrap.mjs](bootstrap.mjs)                                                               | 修复原因：默认 dev:desktop 使用生产账号；远程构建若沿用通用 test 默认值，                                                                          |
| [build-desktop-agent-bytecode.mjs](build-desktop-agent-bytecode.mjs)                         | 先写不可变依赖，最后原子替换入口；失败时上次可用的加载器仍能找到自己的字节码。                                                                     |
| [build-desktop-agent-cli.mjs](build-desktop-agent-cli.mjs)                                   | adapters tsc 在内存受限机器上会 OOM（exit 134），给整条构建链路提高堆上限。                                                                        |
| [build-native-search-tools.mjs](build-native-search-tools.mjs)                               | 实现或公开接口：buildNativeSearchTools。                                                                                                           |
| [build-time-config.mjs](build-time-config.mjs)                                               | \* 桌面构建期可选能力的唯一解析入口：ARMS RUM 上报、事件上报、自动更新。                                                                           |
| [build-windows-runtime-host.mjs](build-windows-runtime-host.mjs)                             | 实现或公开接口：resolveRuntimeHostBuild、verifyRuntimeHostPe、isRuntimeHostReady、buildRuntimeHost。                                               |
| [build-zcode.mjs](build-zcode.mjs)                                                           | build-zcode 的实现文件。                                                                                                                           |
| [builtin-provider-config.mjs](builtin-provider-config.mjs)                                   | 构建期采用运行时的完整 Release 校验，避免打包成功后才发现 Schema 不兼容。                                                                          |
| [cdn-preload.sh](cdn-preload.sh)                                                             | cdn-preload 的Shell 脚本。                                                                                                                         |
| [check-e2e-remote-targets.mjs](check-e2e-remote-targets.mjs)                                 | 开源树不含私有队列；只有该目录缺失才跳过，其他 IO 或清单错误仍须阻止推送。                                                                         |
| [check-push-worktree.mjs](check-push-worktree.mjs)                                           | App 单测选择器退役后，仍须保证检查内容就是推送版本；不自动 stash 或修改 index。                                                                    |
| [check-sqlite-schema.ts](check-sqlite-schema.ts)                                             | 基线是实际迁移产物；校验旧列/主键/索引兼容，并要求 schema 变更显式更新可审阅基线。                                                                 |
| [check-stale-doc-phrases.mjs](check-stale-doc-phrases.mjs)                                   | 规则改了以后，旧说法常留在别的文档里（同一条规则在多处复述）。这里登记已作废的说法，                                                               |
| [check-workspace-freshness.mjs](check-workspace-freshness.mjs)                               | 开工前基线新鲜度检查 —— 当前分支落后自己的远端、或（非特性分支时）落后                                                                             |
| [clean.mjs](clean.mjs)                                                                       | clean 的实现文件。                                                                                                                                 |
| [cli-lint-admission.mjs](cli-lint-admission.mjs)                                             | 当前各包都是直接 oxlint；未知脚本必须显式接入，不能被枚举器悄悄漏过。                                                                              |
| [compile-desktop-agent-bytecode.cjs](compile-desktop-agent-bytecode.cjs)                     | 仅编译，不调用模块；不能为了预热缓存触发 CLI 的存储、网络或进程副作用。                                                                            |
| [count-lines.sh](count-lines.sh)                                                             | count-lines 的Shell 脚本。                                                                                                                         |
| [create-workspace-hook-trust-uat-fixture.mjs](create-workspace-hook-trust-uat-fixture.mjs)   | create-workspace-hook-trust-uat-fixture 的实现文件。                                                                                               |
| [dep-refs.mjs](dep-refs.mjs)                                                                 | dep-refs 的实现文件。                                                                                                                              |
| [dependency-graph.mjs](dependency-graph.mjs)                                                 | pnpm run 在透传参数时会保留一个裸 --，这里需要显式跳过，避免把它误当成待分析路径。                                                                 |
| [desktop-agent-bytecode-runtime.cjs](desktop-agent-bytecode-runtime.cjs)                     | 字节码不带可重新编译的源码，必须完整编译并保留字节码；编译器和加载器共用这一处配置。                                                               |
| [deterministic-tar-archive.mjs](deterministic-tar-archive.mjs)                               | 实现或公开接口：packSourceAsDeterministicTarGzip、computeDeterministicSourceSha256。                                                               |
| [dev-desktop-cua-env.mjs](dev-desktop-cua-env.mjs)                                           | \* workspace 内 producer 相对仓库根的位置。Windows runtime 解析要求 DEV_ROOT 是物理目录                                                            |
| [dev-desktop-env.mjs](dev-desktop-env.mjs)                                                   | Computer Use Helper 只由真实 producer 提供；开源占位包下不构建 Helper、不注入 Helper 环境。                                                        |
| [dev-desktop-remote-prod.mjs](dev-desktop-remote-prod.mjs)                                   | remote CDN 基址现在跟随 ZCODE_ENV 分流；该脚本用于复现生产态下载链路，                                                                             |
| [dev-official-mcp-server.mjs](dev-official-mcp-server.mjs)                                   | \* 本地自测用的 fake 官方 Server MCP（Streamable HTTP）。                                                                                          |
| [dev-web-remote-control-desktop.mjs](dev-web-remote-control-desktop.mjs)                     | dev-web-remote-control-desktop 的实现文件。                                                                                                        |
| [dev-web-share-env.mjs](dev-web-share-env.mjs)                                               | 分享页同时支持 /cn/share/<code>（中文）与 /share/<code>（英文）。                                                                                  |
| [doctor-macos-release-app.sh](doctor-macos-release-app.sh)                                   | doctor-macos-release-app 的Shell 脚本。                                                                                                            |
| [download-glm.mjs](download-glm.mjs)                                                         | 下载并整理 GLM 平台二进制。                                                                                                                        |
| [download-glm.sh](download-glm.sh)                                                           | ) ARCH="$RAW_ARCH" ;;                                                                                                                              |
| [download-native-search-tools.mjs](download-native-search-tools.mjs)                         | Bugfix：缓存元数据只校验内容，不能让意外丢失的 Unix 可执行权限随 skip 流程继续传递。                                                               |
| [download-ripgrep.mjs](download-ripgrep.mjs)                                                 | 实现或公开接口：resolveRipgrepDownloadBaseUrl、resolveRipgrepDownloadPlan、downloadRipgrepBinary。                                                 |
| [electron-builder-binaries-macos.json](electron-builder-binaries-macos.json)                 | electron-builder-binaries-macos 的数据或配置定义。                                                                                                 |
| [engineering-test-files.json](engineering-test-files.json)                                   | engineering-test-files 的数据或配置定义。                                                                                                          |
| [ensure-native-search-deps.mjs](ensure-native-search-deps.mjs)                               | Bugfix：固定版本一旦发布就不可覆盖，必须在创建目标目录前拒绝摘要漂移的候选归档。                                                                   |
| [generate-third-party-notices.mjs](generate-third-party-notices.mjs)                         | 修复：递归扫描会把 bundled-agents/mock-cdn 的可删除缓存当作源码输入，重建立即失效。                                                                |
| [intranetDefaults.mjs](intranetDefaults.mjs)                                                 | 自建镜像机器地址统一从 INTRANET_MACHINE_HOST 读取，避免多处硬编码漏改。                                                                            |
| [license-identifiers.mjs](license-identifiers.mjs)                                           | 原作者补充的同版 metadata 和发布包证据见 third-party/README.md。                                                                                   |
| [licenses.mjs](licenses.mjs)                                                                 | - 实装清单 = 全 workspace node_modules 的递归集合，含嵌套版本与符号链接。                                                                          |
| [load-endpoint-env.mjs](load-endpoint-env.mjs)                                               | 实现或公开接口：loadEndpointEnv。                                                                                                                  |
| [marketing-executable-lines.mjs](marketing-executable-lines.mjs)                             | 先消除 TS 语法再插桩，避免直接解析 TS 时漏掉运行时 enum。                                                                                          |
| [marketing-source-map-evidence.mjs](marketing-source-map-evidence.mjs)                       | 只接受与该次构建完全匹配的 map；不会把当前 out 当作历史产物。                                                                                      |
| [marketing-touch-coverage-audit.mjs](marketing-touch-coverage-audit.mjs)                     | shared/client 等可在多个域使用；未定义归属不能自动判错或合并。                                                                                     |
| [mcp-image-payload-test-server.mjs](mcp-image-payload-test-server.mjs)                       | mcp-image-payload-test-server 的实现文件。                                                                                                         |
| [mise-run.mjs](mise-run.mjs)                                                                 | Windows 上 pnpm 是 .cmd 文件；其他平台直接使用 pnpm 可执行入口。                                                                                   |
| [mise-toolchain-env.mjs](mise-toolchain-env.mjs)                                             | \* 让所有子进程使用和启动器相同的 Node runtime。                                                                                                   |
| [multimodal-marker-png.mjs](multimodal-marker-png.mjs)                                       | 测试标记只需可读字符；直接绘制 5×7 点阵，避免为测试图片携带 Sharp/native 依赖。                                                                    |
| [multimodal-marker-png.test.mjs](multimodal-marker-png.test.mjs)                             | A 顶部留白、横线和左竖画：验证画的是字符，不是空图或仅含文本 metadata。                                                                            |
| [multimodal-tool-result-p0.mjs](multimodal-tool-result-p0.mjs)                               | 实现或公开接口：CASE_NAMES、buildCase、parseSelectedCases、hasOrderedMarkers。                                                                     |
| [native-search-tools-bundle-meta.mjs](native-search-tools-bundle-meta.mjs)                   | 实现或公开接口：resolveNativeSearchBundleMetaPath、isNativeSearchBundleCurrent、writeNativeSearchBundleMeta、writeNativeSearchProducerBundleMeta。 |
| [native-search-tools-config.mjs](native-search-tools-config.mjs)                             | 仓库内置的预编译归档与内网镜像同名、同 SHA-256；只在未配置内网依赖源时作为离线来源。                                                               |
| [native-search-tools-process.mjs](native-search-tools-process.mjs)                           | 实现或公开接口：run、runCapture、downloadAndExtractSources。                                                                                       |
| [native-search-tools-unix.mjs](native-search-tools-unix.mjs)                                 | macOS 26 SDK 会让 bfs 优先选择 26.0 才存在的标准函数；屏蔽后沿用 10.15 起可用的 \_np 版本。                                                        |
| [native-search-tools-verify.mjs](native-search-tools-verify.mjs)                             | 实现或公开接口：verifyNativeSearchBinaryTarget、getRequiredGlibcVersions、verifyLinuxGlibcBaseline、verifyMacosDeploymentTarget。                  |
| [native-search-tools-windows-pe.mjs](native-search-tools-windows-pe.mjs)                     | 实现或公开接口：readWindowsPeMetadata、verifyWindowsPeBinary。                                                                                     |
| [native-search-tools-windows.mjs](native-search-tools-windows.mjs)                           | 实现或公开接口：resolveNativeWindowsBuildConfig、buildNativeSearchToolsWindows。                                                                   |
| [package-native-search-tools.mjs](package-native-search-tools.mjs)                           | Bugfix: yazl 按本地时区编码 DOS 时间；固定本地时间并禁用扩展时间戳才能跨时区复现。                                                                 |
| [prebuilt-binary-download.mjs](prebuilt-binary-download.mjs)                                 | 解包、定位与归档验真只保留 prebuilt-binary-extract.mjs 一份实现：内网下载链路与仓库归档链路                                                        |
| [prebuilt-binary-extract.mjs](prebuilt-binary-extract.mjs)                                   | Bugfix: Windows GNU tar（Git Bash）会把绝对路径里的盘符冒号（C:）当成远程主机名，                                                                  |
| [prepare-native-search-tools.mjs](prepare-native-search-tools.mjs)                           | 缓存元数据只校验内容，不能让意外丢失的 Unix 可执行权限随 skip 流程继续传递。                                                                       |
| [README.md](README.md)                                                                       | 本目录用途、子目录与逐文件说明。                                                                                                                   |
| [remote-native-search-tools-config.mjs](remote-native-search-tools-config.mjs)               | legacy rg13 的版本与摘要仍由 native-search-tools-config.mjs 唯一持有（内网 download-ripgrep 链路同样读取），                                       |
| [restore-sqlite-migration.ts](restore-sqlite-migration.ts)                                   | 工程恢复入口：先停止使用目标库的应用/CLI；恢复逻辑只有共享 migration 模块这一份。                                                                  |
| [run-affected-engineering-tests.mjs](run-affected-engineering-tests.mjs)                     | hook 的临时 index 不能污染官方 Git 选择及测试中的临时仓库。                                                                                        |
| [run-cli-lint.mjs](run-cli-lint.mjs)                                                         | 沿用各包解析出的 oxlint 版本、cwd 和原参数；包级配置仍由 oxlint 自己读取。                                                                         |
| [spawn-command.mjs](spawn-command.mjs)                                                       | Windows runner 上 bare `pnpm` / `npm` 实际也是通过 cmd shim 提供。                                                                                 |
| [sqlite-schema-contract.mjs](sqlite-schema-contract.mjs)                                     | 字符串中的 CHECK/括号不是约束，字面量大小写也不能随 SQL 关键字一起归一化。                                                                         |
| [stage-credential-keyring.mjs](stage-credential-keyring.mjs)                                 | dev 与打包使用同一依赖布局；原生包不能内联进 JS，也不能混入其他目标平台。                                                                          |
| [stage-dev-cua-plugin-runtime.mjs](stage-dev-cua-plugin-runtime.mjs)                         | 开源占位包不提供 Computer Use 原生能力，也不随附 Sharp：没有真实 producer 时不暂存。                                                               |
| [test-desktop-e2e-container.sh](test-desktop-e2e-container.sh)                               | test-desktop-e2e-container 的Shell 脚本。                                                                                                          |
| [test-native-search-tools-e2e.mjs](test-native-search-tools-e2e.mjs)                         | test-native-search-tools-e2e 的实现文件。                                                                                                          |
| [test-sea-runtime-tools-e2e.mjs](test-sea-runtime-tools-e2e.mjs)                             | test-sea-runtime-tools-e2e 的实现文件。                                                                                                            |
| [test-web-app-gateway-reset.mjs](test-web-app-gateway-reset.mjs)                             | test-web-app-gateway-reset 的实现文件。                                                                                                            |
| [third-party-notices.mjs](third-party-notices.mjs)                                           | 工作区文本允许 Windows checkout 的 CRLF；原始许可和发行声明另用字节哈希校验。                                                                      |
| [third-party-notices.test.mjs](third-party-notices.test.mjs)                                 | third-party-notices.test 的实现文件。                                                                                                              |
| [third-party-npm.mjs](third-party-npm.mjs)                                                   | 解析锁文件（v9）packages 段的平台约束：` 'name@version':` 下的 ` os/cpu/libc: [..]` 行。                                                           |
| [verify-electron-builder-binaries-mirror.mjs](verify-electron-builder-binaries-mirror.mjs)   | electron-builder 26.17 起，macOS 打包在签名后并发下载 7zip@1.0.0 与 dmg-builder@1.2.5。                                                            |
| [verify-project-upgrade.mts](verify-project-upgrade.mts)                                     | verify-project-upgrade 模块的资源或工程文件。                                                                                                      |
| [zcode-distribution-smoke.mjs](zcode-distribution-smoke.mjs)                                 | 在仓库外验证发行包，避免开发机 node_modules 掩盖缺失的 TUI/native/worker 依赖。                                                                    |
| [zcode-distribution.test.mjs](zcode-distribution.test.mjs)                                   | zcode-distribution.test 的实现文件。                                                                                                               |

<!-- qingqi-directory-index:end -->
