# lib

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/android-emulator-plugin 基础工程中的 lib 实现源码。

### 文件

| 文件                   | 简要说明                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| [path.ts](path.ts)     | 工具查找曾把工作区文件当成系统依赖执行；同时校验字面路径与真实路径，防止链接绕过。        |
| [README.md](README.md) | 本目录用途、子目录与逐文件说明。                                                          |
| [result.ts](result.ts) | 实现或公开接口：json、fail、image。                                                       |
| [run.ts](run.ts)       | Windows 环境变量不区分大小写；先合并同名键，再删除 undefined，避免保留旧 Path/JAVA_HOME。 |

<!-- qingqi-directory-index:end -->
