# microphone-access

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 microphone access 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                         |
| -------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)               | \* desktop-microphone-access 标准调用示例：Main 启动时注册一次 IPC 处理器。      |
| [CONTRACT.md](CONTRACT.md)                               | 模块职责、公共接口、依赖方向和状态约定。                                         |
| [contract.ts](contract.ts)                               | \* desktop-microphone-access 对外契约：Main 进程的麦克风系统权限与系统设置跳转。 |
| [desktopMicrophoneAccess.ts](desktopMicrophoneAccess.ts) | 只允许打开这里列出的固定地址，renderer 只能选 target，不能传任意 URL。           |
| [index.ts](index.ts)                                     | index 的实现文件。                                                               |
| [module.ts](module.ts)                                   | \* desktop-microphone-access 模块清单（architecture-governance managed 模块）。  |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                 |

<!-- qingqi-directory-index:end -->
