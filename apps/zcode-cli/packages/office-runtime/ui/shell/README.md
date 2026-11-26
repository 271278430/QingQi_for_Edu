# shell

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/office-runtime 基础工程中的 shell 模块文件。

### 文件

| 文件                                             | 简要说明                                                                                                        |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| [float.ts](float.ts)                             | Preferred side of the anchor; flips when there is no room.                                                      |
| [inline.tsx](inline.tsx)                         | \* 内联（对话内嵌）模式的面板：只读预览，点击任意处切到侧栏全屏。                                               |
| [menus.tsx](menus.tsx)                           | 面板标题栏的两个下拉菜单（切换文档、更多操作），从 main.tsx 拆出以控制单文件规模，行为不变。                    |
| [panes.tsx](panes.tsx)                           | 面板的文档导航与状态界面（抽屉、文件选择、空态、骨架、错误、文件变更提示），从 parts.tsx 拆出以控制单文件规模。 |
| [parts.tsx](parts.tsx)                           | ZCode dropdown: closes on Escape and on any pointer press outside it.                                           |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                                                |
| [state.ts](state.ts)                             | 面板外壳（main.tsx）共用的状态类型与持久化、错误描述等辅助函数，从 main.tsx 拆出以控制单文件规模。              |
| [useCaptureView.ts](useCaptureView.ts)           | \* 页面工具 capture_view：Agent 截取面板当前文档的某处画面。                                                    |
| [useFind.ts](useFind.ts)                         | \* 面板内查找：输入即搜，Enter / ⇧Enter 在结果间跳转。                                                          |
| [useOffscreenTargets.ts](useOffscreenTargets.ts) | \* Agent 标出的目标中不在可视区域内的那些，用于「还有 N 处」提示。                                              |
| [useShellKeys.ts](useShellKeys.ts)               | \* 面板快捷键：⌘F、⌘Enter、⌘± / ⌘0、翻页键，以及 Esc 逐层关闭最上层界面。                                       |

<!-- qingqi-directory-index:end -->
