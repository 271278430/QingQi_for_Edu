# mobile-ui

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 mobile ui 界面组件。

### 文件

| 文件                                             | 简要说明                                                                                                |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [bottom-sheet.tsx](bottom-sheet.tsx)             | \* 手机端底部弹层：沿用 Radix Dialog 的焦点圈定、Esc 关闭与可访问名称，只把内容贴底展示。               |
| [contract.example.ts](contract.example.ts)       | 实现或公开接口：platformIcon、closedSelection。                                                         |
| [CONTRACT.md](CONTRACT.md)                       | 模块职责、公共接口、依赖方向和状态约定。                                                                |
| [contract.ts](contract.ts)                       | 实现或公开接口：DevicePlatformIconProps、ZCodeAppLogoProps、BottomSheetProps、BottomSheetContentProps。 |
| [DevicePlatformIcon.tsx](DevicePlatformIcon.tsx) | 品牌轮廓来自 Simple Icons 16.32.0（CC0-1.0），仅用于标识远控设备的操作系统。                            |
| [index.ts](index.ts)                             | index 的实现文件。                                                                                      |
| [module.ts](module.ts)                           | 依赖与 architecture-policy.yaml 同步；新增文件必须属于此 managed 边界。                                 |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                                        |
| [ZCodeAppLogo.tsx](ZCodeAppLogo.tsx)             | \* 桌面端标题栏左上角同款应用 logo（圆角方块 + Z 字形，自带底色，深浅主题通用）。                       |

<!-- qingqi-directory-index:end -->
