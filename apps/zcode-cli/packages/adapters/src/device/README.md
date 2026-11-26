# device

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 device 实现源码。

### 文件

| 文件                                                 | 简要说明                                                                              |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [cli-device-mid.ts](cli-device-mid.ts)               | \* 在 CLI 所在主机独立确保 deviceMid 存在；它是反馈与 provider 请求头使用的设备身份， |
| [process-probe-darwin.ts](process-probe-darwin.ts)   | macOS 只允许 `ps`；输出格式与列名成对声明，避免两处各写一份而静默错位。               |
| [process-probe-linux.ts](process-probe-linux.ts)     | Linux `USER_HZ`：`/proc/<pid>/stat` 的 utime/stime 以此为单位，所有支持平台上都是 100 |
| [process-probe-shared.ts](process-probe-shared.ts)   | \* 通用进程探针的共享契约与平台无关工具。                                             |
| [process-probe-windows.ts](process-probe-windows.ts) | \* Windows：唯一允许的外部进程是 `tasklist`，一次调用拿全部进程内存。                 |
| [process-probe.ts](process-probe.ts)                 | 进程树采样的实际口径：Windows 的 tasklist 没有 ppid，只能拿到直连进程。               |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                      |

<!-- qingqi-directory-index:end -->
