# runtime

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server-cli 基础工程中的 runtime 实现源码。

### 文件

| 文件                                                 | 简要说明                                                                                            |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [agentWiring.ts](agentWiring.ts)                     | \* 发行包内 Core 既不在 monorepo、也没有 Electron runtime，`zcodeAgentProcessManager`               |
| [componentCache.ts](componentCache.ts)               | 实现或公开接口：extractArchiveSafely、ComponentCache。                                              |
| [immutableRelease.ts](immutableRelease.ts)           | \* 已存在的同 id release 只有两种合法结论：与本次 archive 一致可采用，或是本次 archive 的损坏副本。 |
| [installationOwnership.ts](installationOwnership.ts) | 直接 open install.json 后再写入会先暴露空文件，并发 ensure 可能把                                   |
| [lock.ts](lock.ts)                                   | 本进程当前持有的锁与恢复门 token。PID 等于自己时只有它能证明锁是本进程写的。                        |
| [manifest.ts](manifest.ts)                           | 入口是 ESM `.js`（tsup 产物）：server-cli 通过 `new URL("./server-core.js")` fork Core、            |
| [paths.ts](paths.ts)                                 | Supervisor 写出第一份状态前失败时的诊断摘要；不参与任何状态判断（R2 §7.1）。                        |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                                    |
| [releaseDownload.ts](releaseDownload.ts)             | 无数据活动时的超时；收到数据后会重新计时。                                                          |
| [releaseInstaller.ts](releaseInstaller.ts)           | macOS tar 可能额外写入 `._*` PAX/resource-fork 条目，不能因为这些旁路文件                           |
| [releaseManager.ts](releaseManager.ts)               | 并发写各自持有唯一临时文件，但 rename 替换同一目标时 Windows 的                                     |
| [serviceInstallation.ts](serviceInstallation.ts)     | 卸载先解除 OS 服务注册，再清理 descriptor/data root；否则 systemd/launchd 可能                      |
| [shutdownWait.ts](shutdownWait.ts)                   | \* 状态快照写出的 stop-failed：Supervisor 停 Core 失败后继续持锁，不会再自行停止。                  |
| [stableLauncher.ts](stableLauncher.ts)               | Bug 原因：远端以 "$HOME/.zcode/server/bin/zcode" 调用本脚本，NAS 等环境的 $HOME 经过符号链接        |
| [startupRecovery.ts](startupRecovery.ts)             | 实现或公开接口：recoverSupervisorStartup。                                                          |
| [statusSnapshot.ts](statusSnapshot.ts)               | Bug 原因：文件缺失表示离线，JSON/schema 损坏表示观测不可信；两者不能再折叠成同一个 null，           |
| [uninstallGuard.ts](uninstallGuard.ts)               | 实现或公开接口：acquireUninstallLock、removeRunContentsExceptLock、describeLockInspection。         |
| [updateCommand.ts](updateCommand.ts)                 | 返回被替换的版本；无法证明方向（首装或非 semver 历史版本）时不视为降级。                            |
| [updateErrors.ts](updateErrors.ts)                   | 实现或公开接口：updateErrorMessage、createRollbackFailure。                                         |
| [updateHandoff.ts](updateHandoff.ts)                 | 实现或公开接口：UpdateHandoffProcessBoundary、createUpdateDaemonHandoff。                           |
| [updatePreparation.ts](updatePreparation.ts)         | 只清理不可能比 current 更新的遗留候选；未来版本的 pending 仍保留，供用户在                          |
| [updateReadiness.ts](updateReadiness.ts)             | 实现或公开接口：waitForUpdateReady。                                                                |

<!-- qingqi-directory-index:end -->
