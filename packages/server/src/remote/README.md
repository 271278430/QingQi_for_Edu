# remote

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server 基础工程中的 remote 实现源码。

### 文件

| 文件                                                                                       | 简要说明                                                                                                                             |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| [backend.ts](backend.ts)                                                                   | WSL 可选的运行时网络解析；其它远端类型保持未注入。                                                                                   |
| [closeEvent.ts](closeEvent.ts)                                                             | 远端命令可能在调用方订阅 onClose 之前就瞬间退出。                                                                                    |
| [connect.ts](connect.ts)                                                                   | 仅 Desktop Host 注入，采用当前 stdio 的私有反向资源频道。                                                                            |
| [create-backend.ts](create-backend.ts)                                                     | 实现或公开接口：createRemoteBackend。                                                                                                |
| [deploy.ts](deploy.ts)                                                                     | 取消当前远端连接初始化与其拥有的上传。                                                                                               |
| [deployShared.ts](deployShared.ts)                                                         | 取消当前连接初始化；共享 cache 仍可独立完成，但不得继续写入远端 staging。                                                            |
| [detectEnv.ts](detectEnv.ts)                                                               | 某些 SSH/Docker 测试容器会把 `uname -s` 伪装成 Darwin，                                                                              |
| [docker-backend.ts](docker-backend.ts)                                                     | 直接 exec/read 跳过容器枚举后失去了隐式校验；在组装 argv 处拒绝选项形态和非法引用。                                                  |
| [docker-detect.ts](docker-detect.ts)                                                       | macOS GUI 应用从 Dock/Finder 启动时通常不会继承 shell PATH，                                                                         |
| [handshake.ts](handshake.ts)                                                               | Remaining data after the handshake line (to be fed into RPC)                                                                         |
| [index.ts](index.ts)                                                                       | index 的实现文件。                                                                                                                   |
| [localTarGz.ts](localTarGz.ts)                                                             | Windows 客户端不一定能 spawn System32\tar.exe，远端资源本地缓存不能依赖系统 tar。                                                    |
| [posixShell.ts](posixShell.ts)                                                             | 实现或公开接口：quotePosixShellArg、buildPosixShellExecCommand、quotePosixPathArg、resolvePosixHomePath。                            |
| [README.md](README.md)                                                                     | 本目录用途、子目录与逐文件说明。                                                                                                     |
| [remoteAssetCache.ts](remoteAssetCache.ts)                                                 | 实现或公开接口：RemoteAssetManifest、RemoteAssetManifestComponent、RemoteAssetManifestRef、RemoteAssetCacheLoggers。                 |
| [remoteAssetCdn.ts](remoteAssetCdn.ts)                                                     | 当调用方已经传入带版本的 CDN 基址时，继续盲目拼 `${base}/${version}`                                                                 |
| [remoteAssetDeployDecision.ts](remoteAssetDeployDecision.ts)                               | 实现或公开接口：RemoteAssetVersionResolverOptions、createRemoteComponentVersionResolver、deployNodeRuntime、deployNodePtyPrebuilds。 |
| [remoteAssetInstaller.ts](remoteAssetInstaller.ts)                                         | SSH 取消会先释放旧 backend，不能再用旧凭据立即 cleanup。                                                                             |
| [remoteAssetLiveIdentity.ts](remoteAssetLiveIdentity.ts)                                   | 旧 live marker 只记录 version，无法证明运行目录来自当前 manifest 制品。                                                              |
| [remoteAssetNetwork.ts](remoteAssetNetwork.ts)                                             | Desktop Host 的远程资源下载曾直接使用 global fetch，绕过设置页代理。                                                                 |
| [remoteAssetPreflight.ts](remoteAssetPreflight.ts)                                         | 实现或公开接口：RemoteDownloadTool、RemoteSha256Tool、RemoteAssetTools、detectRemoteTarTool。                                        |
| [remoteConnectionProgressContext.ts](remoteConnectionProgressContext.ts)                   | \* 把共享 Host 内并发产生的远程连接日志绑定到各自 requestId。                                                                        |
| [remoteDeployLock.ts](remoteDeployLock.ts)                                                 | release timeout 后只尽力关闭本次 lock-holder stream；清理失败不能再次覆盖 timeout 诊断。                                             |
| [remotePlatformSupport.ts](remotePlatformSupport.ts)                                       | \* 远端平台不在支持范围时的错误；带公开码，让 UI 显示专用原因，                                                                      |
| [runtimeToolDeploy.ts](runtimeToolDeploy.ts)                                               | 实现或公开接口：DeployRuntimeToolOptions、deployRuntimeTools。                                                                       |
| [serverBundleDeployCheck.ts](serverBundleDeployCheck.ts)                                   | 开发态远端 server 可能版本号相同但 bundle 内容仍是旧包，旧包没有                                                                     |
| [ssh-backend.ts](ssh-backend.ts)                                                           | 本次连接尝试中 keyboard-interactive 提示明确要求动态口令；每次 connect 前清零，只用于认证失败的分类。                                |
| [sshAuth.ts](sshAuth.ts)                                                                   | ssh2 每个间隔发一次心跳，第 COUNT_MAX + 1 次仍无响应时才报错，所以是 4 个间隔。                                                      |
| [sshUploadProgress.ts](sshUploadProgress.ts)                                               | SSH 连接弹窗之前只在 CDN 下载阶段展示“完成度 + 速度”，上传阶段只有静态起始日志。                                                     |
| [stdio-socket.ts](stdio-socket.ts)                                                         | \* Wrap a StdioStream (from IRemoteBackend.exec()) as an ISocket                                                                     |
| [wsl-backend.ts](wsl-backend.ts)                                                           | Bug 原因：身份探测曾用 `bash -lc` 并按行解析；profile 里的 echo 先于身份输出，被当成                                                 |
| [wsl-detect.ts](wsl-detect.ts)                                                             | `wsl.exe -l -v` 在 Windows 上常返回 UTF-16LE。                                                                                       |
| [wslProxy.ts](wslProxy.ts)                                                                 | 实现或公开接口：normalizeWslProxyUrl、isLoopbackProxyHostname、replaceProxyHostname、buildWslProxyPortProbeCommand。                 |
| [zcodeAgentBundleWrapper.ts](zcodeAgentBundleWrapper.ts)                                   | 远端 ZCode Agent 以「独立 node + 编译产物 zcode.cjs」的形态运行，而不是各平台内嵌 node 的原生二进制。                                |
| [zcodeAgentDeploy.ts](zcodeAgentDeploy.ts)                                                 | 实现或公开接口：DeployZCodeAgentRuntimeOptions、deployZCodeAgentRuntime。                                                            |
| [zcodeAgentDevDeploy.ts](zcodeAgentDevDeploy.ts)                                           | Vitest 里仓库真实 dist 可能存在；默认关闭，避免普通部署测试误走开发态分支。                                                          |
| [zcodeAgentOfficialPluginAssets.ts](zcodeAgentOfficialPluginAssets.ts)                     | 开发态远程插件复制使用独立白名单，遗漏 agents 会只在远端丢失子代理。                                                                 |
| [zcodeAgentOfficialPluginPermissionRepair.ts](zcodeAgentOfficialPluginPermissionRepair.ts) | 旧版从 Windows 重打 packages tar 时会把目录 mode 写成 0666，远端叠加 umask 后                                                        |
| [zcodeAgentWrapperDeploy.ts](zcodeAgentWrapperDeploy.ts)                                   | 历史原因：WSLBackend 曾以 `wsl.exe -- bash -lc <command>` 启动，默认 shell 会让多行                                                  |

<!-- qingqi-directory-index:end -->
