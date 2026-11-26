# platform

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server-cli 基础工程中的 platform 实现源码。

### 文件

| 文件                                   | 简要说明                                                                     |
| -------------------------------------- | ---------------------------------------------------------------------------- |
| [README.md](README.md)                 | 本目录用途、子目录与逐文件说明。                                             |
| [serviceManager.ts](serviceManager.ts) | 正常 stop 会让 Supervisor 以 0 退出；只按异常退出重启，避免 launchd 的无条件 |

<!-- qingqi-directory-index:end -->
