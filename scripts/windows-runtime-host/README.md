# windows-runtime-host

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

windows runtime host 工程脚本，属于 scripts 目录。

### 文件

| 文件                                                           | 简要说明                                                                      |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [acceptance.cpp](acceptance.cpp)                               | 原生验收同时可在 Windows 和 Wine 执行；Wine 结果不能代替 Windows 实机验收。   |
| [CMakeLists.txt](CMakeLists.txt)                               | CMakeLists 模块的资源或工程文件。                                             |
| [host-acceptance.cjs](host-acceptance.cjs)                     | Windows 原生运行时验收。传入包含 helper、fixture、adapter.cjs 的构建目录。    |
| [installer-process-fixture.cpp](installer-process-fixture.cpp) | 共享打开仍然成功，但字节范围锁令真正的追加写入返回 ERROR_LOCK_VIOLATION。     |
| [installer-process-helper.cpp](installer-process-helper.cpp)   | 修复原因：诊断日志被占用或不可写时，不能改变进程检查结果。                    |
| [main.cpp](main.cpp)                                           | 内核在最后一个句柄关闭且全部成员退出后销毁 Job；不存在是原 Job 已消失的事实。 |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                              |

<!-- qingqi-directory-index:end -->
