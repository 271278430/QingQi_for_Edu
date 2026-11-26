# ui

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 ui 实现源码。

### 文件

| 文件                                                                               | 简要说明                                                                                |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [README.md](README.md)                                                             | 本目录用途、子目录与逐文件说明。                                                        |
| [webRemoteControlBrand.tsx](webRemoteControlBrand.tsx)                             | 连接前各页的页头品牌：桌面端同款 logo 图标 + “ZCode”文字，纯静态标识，不可点击。        |
| [webRemoteControlConnectingScreen.tsx](webRemoteControlConnectingScreen.tsx)       | 连接过程页展示的目标电脑；名字来自连接参数，平台来自本机记住的设备记录。                |
| [webRemoteControlConnectionSheet.tsx](webRemoteControlConnectionSheet.tsx)         | 超过一个月的相对天数难以阅读，改用日期。                                                |
| [webRemoteControlDeviceListPage.tsx](webRemoteControlDeviceListPage.tsx)           | 多连接弹层的“启动于”相对时间基准，测试注入。                                            |
| [webRemoteControlFailureScreen.tsx](webRemoteControlFailureScreen.tsx)             | 实现或公开接口：WebRemoteControlFailureScreen。                                         |
| [webRemoteControlScanPage.tsx](webRemoteControlScanPage.tsx)                       | 实现或公开接口：WebRemoteControlScanPage。                                              |
| [webRemoteControlSwitchAccountDialog.tsx](webRemoteControlSwitchAccountDialog.tsx) | 实现或公开接口：WebRemoteControlSwitchAccountDialog。                                   |
| [webRemoteControlVersionNotice.tsx](webRemoteControlVersionNotice.tsx)             | 原页面保持挂载；原生 modal 阻止背景元素与其他 portal 的操作，全局快捷键由入口提前拦截。 |

<!-- qingqi-directory-index:end -->
