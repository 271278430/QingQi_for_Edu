# file-menu

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 file menu 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                                     |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| [ArtifactOpenAsFileButton.tsx](ArtifactOpenAsFileButton.tsx)       | \* 产物 tab 头部的「作为文件打开」分段按钮（docs/dynamic-workflow/authoring.md「How the user sees them」）。 |
| [contract.example.ts](contract.example.ts)                         | 已有 fileService 满足读取契约，无需新增另一份文件状态。                                                      |
| [CONTRACT.md](CONTRACT.md)                                         | 模块职责、公共接口、依赖方向和状态约定。                                                                     |
| [contract.ts](contract.ts)                                         | 文件所属 Host 的读取端口。路径保持该 Host 的语义，不转换成本机路径。                                         |
| [DefaultFileApplicationLabel.tsx](DefaultFileApplicationLabel.tsx) | 已知默认应用才展示其身份；中性系统动作不能借用首个候选或历史选择的图标。                                     |
| [FileApplicationChoices.tsx](FileApplicationChoices.tsx)           | 少量候选直接可见；默认快捷项占同一个名额，更多菜单只接收剩余项。                                             |
| [FileApplicationIcon.tsx](FileApplicationIcon.tsx)                 | 文件菜单共用系统应用图标；缺图和加载失败不能让不同入口出现空白图标位。                                       |
| [fileApplicationSubmenu.css](fileApplicationSubmenu.css)           | Radix 在紧邻的浮层上给出真实展开方向；只翻转本组件的末尾箭头，不另存定位状态。                               |
| [FileApplicationSubmenu.tsx](FileApplicationSubmenu.tsx)           | 所有文件入口共用候选列表：主菜单高度不再随系统安装的应用数量增长。                                           |
| [fileCopy.ts](fileCopy.ts)                                         | 先完整读取原字节再交给保存对话框，选择同一文件也不会先截断源文件。                                           |
| [FileSaveAsMenuItem.tsx](FileSaveAsMenuItem.tsx)                   | 实现或公开接口：FileSaveAsMenuItem。                                                                         |
| [index.ts](index.ts)                                               | index 的实现文件。                                                                                           |
| [module.ts](module.ts)                                             | \* ui-file-menu 模块清单（architecture-governance managed 模块）。                                           |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                             |
| [useFileApplications.ts](useFileApplications.ts)                   | 实现或公开接口：useFileApplications。                                                                        |

<!-- qingqi-directory-index:end -->
