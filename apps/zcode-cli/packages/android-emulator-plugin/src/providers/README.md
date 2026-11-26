# providers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/android-emulator-plugin 基础工程中的 providers 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                      |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| [app.ts](app.ts)                           | 实现或公开接口：install、launch、terminate、openUrl。                                                         |
| [avd.ts](avd.ts)                           | 实现或公开接口：listAvds、parseAvds、ensureDevice、startEmulator。                                            |
| [build.ts](build.ts)                       | 实现或公开接口：buildApp、buildAndRun、pickApk。                                                              |
| [config.ts](config.ts)                     | 实现或公开接口：androidApiLevel、androidBuildToolsVersion、androidSystemImageVariant、androidSystemImageAbi。 |
| [device.ts](device.ts)                     | 实现或公开接口：Device、validSerial、listDevices、parseAdbDevices。                                           |
| [logs.ts](logs.ts)                         | 实现或公开接口：logs。                                                                                        |
| [preflight.ts](preflight.ts)               | 缺少可信 JDK 时，裸 java 会再次从工作区解析；直接报告缺失，不尝试执行。                                       |
| [project-template.ts](project-template.ts) | 实现或公开接口：templateFiles。                                                                               |
| [project.ts](project.ts)                   | 实现或公开接口：discover、create、findApks。                                                                  |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                              |
| [screenshot.ts](screenshot.ts)             | 实现或公开接口：shot。                                                                                        |
| [sdk.ts](sdk.ts)                           | SDK 的 Java 脚本缺少 JAVA_HOME 时也会裸跑 java；不能只修复预检自身的 Java 调用。                              |
| [ui.ts](ui.ts)                             | 实现或公开接口：status、describe、resolve、tap。                                                              |

<!-- qingqi-directory-index:end -->
