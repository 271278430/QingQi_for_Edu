# process

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 process 实现源码。

### 文件

| 文件                                                       | 简要说明                                                                                   |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [processResourceSampler.ts](processResourceSampler.ts)     | \* 资源管理器 Host 侧采样。                                                                |
| [processTreeOwnership.ts](processTreeOwnership.ts)         | root PID 在 exit 回调落到 JS 前也可能进入延迟回收窗口。                                    |
| [processTreeSnapshot.ts](processTreeSnapshot.ts)           | Darwin 的 ps 只暴露秒级 lstart；追加完整 command 作为采用校验熵。                          |
| [processTreeSnapshotAsync.ts](processTreeSnapshotAsync.ts) | 查询期间原 root 退出后，PID 可能在 Node exit 回调与 CIM 返回之间                           |
| [processTreeTerminator.ts](processTreeTerminator.ts)       | 进程身份查询失败，只观察原 ChildProcess，禁止向裸 PID 发送 taskkill。                      |
| [processTreeTypes.ts](processTreeTypes.ts)                 | POSIX Host 在 spawn(detached=true) 时拥有的独立进程组；仅用于 cleanup 边界。               |
| [processTreeWaiter.ts](processTreeWaiter.ts)               | Windows 的 graceful taskkill 与 force timer 并发；只要存在已验证信号目标，就保守地         |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                                           |
| [runtimeProcessLifecycle.ts](runtimeProcessLifecycle.ts)   | 进程泳道（如 mcp-status）；缺省为 chat 主泳道。同 cwd、同 command 的多 lane 进程靠它归因。 |
| [windowsProcessListAsync.ts](windowsProcessListAsync.ts)   | Windows 11 24H2 及部分 Win10 镜像不再提供 WMIC；Windows 10+ 统一使用                       |
| [windowsTaskkillRunner.ts](windowsTaskkillRunner.ts)       | 多个 workspace 退出时，同步 taskkill 会按 Agent 数量串行阻塞 Host。                        |

<!-- qingqi-directory-index:end -->
