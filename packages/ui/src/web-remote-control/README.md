# web-remote-control

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 web remote control 实现源码。

### 子目录

| 目录                        | 存放内容                                 |
| --------------------------- | ---------------------------------------- |
| [app/](app/README.md)       | @zcode/ui 基础工程中的 app 实现源码。    |
| [domain/](domain/README.md) | @zcode/ui 基础工程中的 domain 实现源码。 |

### 文件

| 文件                                                                         | 简要说明                                                                                                                                       |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                                   | 实现或公开接口：deviceNavigation。                                                                                                             |
| [CONTRACT.md](CONTRACT.md)                                                   | 模块职责、公共接口、依赖方向和状态约定。                                                                                                       |
| [contract.ts](contract.ts)                                                   | 实现或公开接口：WebRemoteControlDeviceNavigation、WebRemoteControlAuthPlatform、WebRemoteControlAuthEvents、WebRemoteControlTaskViewSwitcher。 |
| [index.ts](index.ts)                                                         | index 的实现文件。                                                                                                                             |
| [module.ts](module.ts)                                                       | 依赖与 architecture-policy.yaml 同步；新增文件必须属于此 managed 边界。                                                                        |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                                                                               |
| [WebRemoteControlDeviceHeader.tsx](WebRemoteControlDeviceHeader.tsx)         | 侧栏顶部的当前电脑行：与主导航同款 ghost 行，整行即“切换设备”入口。                                                                            |
| [WebRemoteControlDialog.tsx](WebRemoteControlDialog.tsx)                     | 远控401不清全局用户；必须指定当前渠道建立新登录尝试，避免统一入口把缓存用户当作成功。                                                          |
| [WebRemoteControlTaskViewReporter.tsx](WebRemoteControlTaskViewReporter.tsx) | 宽窄屏采用实际聊天表面；导航位置和当前查看分别上报，不保存第二份导航状态。                                                                     |

<!-- qingqi-directory-index:end -->
