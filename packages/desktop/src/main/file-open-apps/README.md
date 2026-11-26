# file-open-apps

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 file open apps 实现源码。

### 文件

| 文件                                       | 简要说明                                                                        |
| ------------------------------------------ | ------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：exampleFileOpenApps。                                           |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                        |
| [contract.ts](contract.ts)                 | 系统关联的真实身份不跨 IPC，只将其摘要给 renderer。                             |
| [index.ts](index.ts)                       | 同一个 bundle 可能由多个浏览器内核目录注册；按路径去重会显示两条相同 Chromium。 |
| [linux.ts](linux.ts)                       | 缺失可执行文件不是有效安装。                                                    |
| [mac.ts](mac.ts)                           | NSWorkspace 直接读取 Launch Services 的文件关联，绝不维护应用白名单。           |
| [module.ts](module.ts)                     | \* file-open-apps 模块清单（architecture-governance managed 模块）。            |
| [native.ts](native.ts)                     | xdg-open 可能等待阅读器退出；只等待启动，避免超时把正常打开误报失败。           |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                |
| [windows-default.ts](windows-default.ts)   | 只用 Shell 的有效默认身份，不把原始 UserChoice 或展示名当成已生效默认。         |
| [windows-icon.ts](windows-icon.ts)         | 用系统 AppID 识别共享套件，不依据显示名称或文件扩展名猜测应用。                 |
| [windows.ts](windows.ts)                   | \* Shell 提供关联处理器和 IDataObject 启动，不自行拼接注册表 command。          |

<!-- qingqi-directory-index:end -->
