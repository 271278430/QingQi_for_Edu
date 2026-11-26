# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/cli 基础工程中的 scripts 工程脚本。

### 文件

| 文件                                                                     | 简要说明                                                                                                                             |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| [build-sea.mjs](build-sea.mjs)                                           | pnpm hoisted 布局会把 postject 放到仓库根 node_modules，而不是 CLI 子包下。                                                          |
| [build.mjs](build.mjs)                                                   | hoisted 安装可能给多个消费者留下字节相同、路径不同的 Zod。                                                                           |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                                                                     |
| [sea-bundled-skill-assets.mjs](sea-bundled-skill-assets.mjs)             | 随 CLI 内置的技能包（apps/zcode-cli/packages/bundled-skills）。它不是官方插件：不进市场目录、                                        |
| [sea-node-download.mjs](sea-node-download.mjs)                           | 实现或公开接口：downloadFile、resolveDownloadedNodeBinary。                                                                          |
| [sea-official-plugin-assets.mjs](sea-official-plugin-assets.mjs)         | recording lookup 是录屏 API 的模型入口，SEA 不得接受缺失正文的插件资产。                                                             |
| [sea-playwright-assets.mjs](sea-playwright-assets.mjs)                   | 实现或公开接口：seaPlaywrightAssetPrefix、seaPlaywrightManifestAssetKey、collectSeaPlaywrightAssets。                                |
| [sea-provider-config-assets.mjs](sea-provider-config-assets.mjs)         | 实现或公开接口：SEA_ZCODE_BUILTIN_PROVIDER_CONFIG_ASSET_KEY、collectSeaProviderConfigAssets。                                        |
| [sea-runtime-package-resolution.mjs](sea-runtime-package-resolution.mjs) | 原收集器仅按包名去重，把 contracts 的 Zod 3 和 shared 的 Zod 4 压成同一个包。                                                        |
| [sea-runtime-tool-assets.mjs](sea-runtime-tool-assets.mjs)               | 单文件 SEA 同样分发原生工具，许可声明与来源清单随二进制内嵌，不依赖 dist 旁的伴随文件。                                              |
| [sea-runtime-tool-prepare.mjs](sea-runtime-tool-prepare.mjs)             | 与 desktop prepare:native-search 共用同一准备入口：内网依赖源已配置时仍下载，                                                        |
| [sea-targets.mjs](sea-targets.mjs)                                       | Keep Windows release artifacts compatible with downstream release downloaders,                                                       |
| [sea-tui-assets.mjs](sea-tui-assets.mjs)                                 | TUI runtime 闭包会经由 @zcode/contracts 依赖仓库根的 @zcode/shared；                                                                 |
| [sea-workspace-package-assets.mjs](sea-workspace-package-assets.mjs)     | 根 workspace 为开发环境导出 src/\*.ts；SEA 仅携带 dist，必须在暂存副本改写入口。                                                     |
| [upload-progress.mjs](upload-progress.mjs)                               | 实现或公开接口：fileMode、formatBytes、createConsoleProgressReporter、copyReleaseFiles。                                             |
| [upload-sea-smb.mjs](upload-sea-smb.mjs)                                 | 实现或公开接口：resolveDefaultSmbUrl、DEFAULT_SMB_URL、DEFAULT_MOUNT_ROOT、DEFAULT_DESTINATION_ROOT。                                |
| [windows-authenticode.mjs](windows-authenticode.mjs)                     | 实现或公开接口：readWindowsAuthenticodeDirectory、removeWindowsAuthenticodeSignatureFromBuffer、removeWindowsAuthenticodeSignature。 |

<!-- qingqi-directory-index:end -->
