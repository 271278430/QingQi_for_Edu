# exec

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 exec 实现源码。

### 文件

| 文件                                                                       | 简要说明                                                                                                                              |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| [bash-file-output.ts](bash-file-output.ts)                                 | Bash 只持有文件身份和观察器；原始输出由子进程写入，不经过 Node collector。                                                            |
| [bash-output-policy.ts](bash-output-policy.ts)                             | 实现或公开接口：resolveBashMaxOutputLength。                                                                                          |
| [bash-output-preview.ts](bash-output-preview.ts)                           | 只扫描本次有界尾读；原始字节数用于 Windows 编码下的行数估计。                                                                         |
| [bash-progress-poller.ts](bash-progress-poller.ts)                         | 按周期共享：产品默认只有一个 1 秒轮询器，内部自定义周期不改变其他任务的频率。                                                         |
| [bash-resource-telemetry.ts](bash-resource-telemetry.ts)                   | 每条命令独占状态与探针失败预算；finish 同步封口，绝不等待遥测 IO。                                                                    |
| [bash-shell-provider.ts](bash-shell-provider.ts)                           | 实现或公开接口：BashShellProvider、EffectiveBashShellResolution、resolveEffectiveBashShellSelection、resolvePosixBashShell。          |
| [bash-startup-script.ts](bash-startup-script.ts)                           | Windows 可能不保留 POSIX mode bit；文件仍位于 ZCode 自有 storage 下。                                                                 |
| [cwd-capture.ts](cwd-capture.ts)                                           | 每次 Bash 仍启动新 shell；成功后只把最终 pwd -P 写回主进程，不能持久化 env/alias/function。                                           |
| [embedded-search-prelude.ts](embedded-search-prelude.ts)                   | ugrep 的 -z/-Z 与 GNU grep 的 null-data 语义不同；这些参数必须绕回系统 grep。                                                         |
| [execution-adapter-types.ts](execution-adapter-types.ts)                   | Bash 移交时停止前台预览并重启文件 watchdog；不复制进程或输出。                                                                        |
| [execution-command.ts](execution-command.ts)                               | Bash/tool 子进程不能直接继承运行时的 NODE_ENV、http_proxy 或证书变量。                                                                |
| [execution-utils.ts](execution-utils.ts)                                   | losing timeout 不应在目标 Promise 已完成后继续单独保活 CLI。                                                                          |
| [index.ts](index.ts)                                                       | index 的实现文件。                                                                                                                    |
| [node-execution-adapter-base.ts](node-execution-adapter-base.ts)           | 实现或公开接口：NodeExecutionAdapterBase。                                                                                            |
| [node-execution-adapter-lifecycle.ts](node-execution-adapter-lifecycle.ts) | 实现或公开接口：NodeExecutionAdapterLifecycle。                                                                                       |
| [node-execution-adapter-process.ts](node-execution-adapter-process.ts)     | 实现或公开接口：NodeExecutionAdapterProcess。                                                                                         |
| [node-execution-adapter-results.ts](node-execution-adapter-results.ts)     | 仅对空输出且非零退出进行文件系统诊断，不把正常无输出命令误报为丢失。                                                                  |
| [node-execution-adapter-run.ts](node-execution-adapter-run.ts)             | 请求可能被采用；缓存保存的是实际路径，降级根必须始终来自原有配置。                                                                    |
| [node-execution-adapter.ts](node-execution-adapter.ts)                     | 实现或公开接口：NodeExecutionAdapter、createNodeExecutionAdapter。                                                                    |
| [output-collector.ts](output-collector.ts)                                 | \* 一路输出最后 maxBytes 字节的有界尾部（请求级 `outputLimit.tailBytes`）。                                                           |
| [outputEncoding.ts](outputEncoding.ts)                                     | Bash 工具的 stdout/stderr 是给 UI 和模型消费的 Unicode 文本。                                                                         |
| [process-tree.ts](process-tree.ts)                                         | 组长 exit 后，负 PGID 仍可能命中持有 pipe 的孙进程；仅当进程组                                                                        |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                                                                      |
| [shell-init-snapshot.ts](shell-init-snapshot.ts)                           | 实现或公开接口：DEFAULT_SHELL_INIT_SNAPSHOT_RETENTION_DAYS、ShellInitSnapshotDialect、ShellInitSnapshotShellKind、ShellInitSnapshot。 |
| [windows-executable.ts](windows-executable.ts)                             | \* Windows PATH 的目录列表：按 `;` 拆分，去掉首尾的双引号，跳过空条目。                                                               |

<!-- qingqi-directory-index:end -->
