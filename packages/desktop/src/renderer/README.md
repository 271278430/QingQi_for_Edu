# renderer

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 renderer 实现源码。

### 子目录

| 目录                        | 存放内容                                      |
| --------------------------- | --------------------------------------------- |
| [public/](public/README.md) | @zcode/desktop 基础工程中的 public 实现源码。 |
| [src/](src/README.md)       | @zcode/desktop 基础工程中的 src 实现源码。    |

### 文件

| 文件                                                           | 简要说明                                                                                      |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [cua-permission-panel.html](cua-permission-panel.html)         | cua-permission-panel 模块的资源或工程文件。                                                   |
| [cuaPermissionPanel.ts](cuaPermissionPanel.ts)                 | 挂载即预热：install+verify 是异步的，必须在用户开始拖之前完成，                               |
| [cuaPermissionPanelMessages.ts](cuaPermissionPanelMessages.ts) | 权限引导面板只有中英两套文案；日/俄/韩直接下标会取到 undefined 导致面板渲染崩溃，降级到英文。 |
| [index.html](index.html)                                       | index 模块的资源或工程文件。                                                                  |
| [plugin-sandbox.html](plugin-sandbox.html)                     | plugin-sandbox 模块的资源或工程文件。                                                         |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                              |
| [resource-manager.html](resource-manager.html)                 | resource-manager 模块的资源或工程文件。                                                       |

<!-- qingqi-directory-index:end -->
