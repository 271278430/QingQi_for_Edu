# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

四项学生功能及设置管理的 React 页面、交互状态、图谱、动画与标注组件。

### 文件

| 文件                                                         | 简要说明                                                       |
| ------------------------------------------------------------ | -------------------------------------------------------------- |
| [architecture-board.tsx](architecture-board.tsx)             | 架构图画布、缩放与下载。                                       |
| [architecture-module.tsx](architecture-module.tsx)           | 点击模块后的职责、步骤与源码详情。                             |
| [architecture-panel.tsx](architecture-panel.tsx)             | 项目架构页，只展示系统关系图。                                 |
| [architecture-svg.tsx](architecture-svg.tsx)                 | 系统关系图 SVG 节点和有向边。                                  |
| [composer-actions.tsx](composer-actions.tsx)                 | 生成期间的发送和停止按钮。                                     |
| [composer-models.tsx](composer-models.tsx)                   | 输入框中的文本、视觉模型和推理档位菜单。                       |
| [contract.example.ts](contract.example.ts)                   | 公开契约的使用示例。                                           |
| [CONTRACT.md](CONTRACT.md)                                   | Web 模块职责、依赖边界和状态约定。                             |
| [contract.ts](contract.ts)                                   | Web 模块的公开类型契约。                                       |
| [controls.tsx](controls.tsx)                                 | 教育页面的公共交互控件。                                       |
| [env.d.ts](env.d.ts)                                         | 前端环境与资源导入类型。                                       |
| [format.ts](format.ts)                                       | 页面文字、时间和展示值格式化。                                 |
| [geometry-animation.tsx](geometry-animation.tsx)             | 几何构造的连续动画组件。                                       |
| [geometry-lesson.tsx](geometry-lesson.tsx)                   | 几何分步教学与图形展示。                                       |
| [identity-animation.tsx](identity-animation.tsx)             | 恒等式教学动画组件。                                           |
| [index.ts](index.ts)                                         | Web 包的公开导出。                                             |
| [learning-content.tsx](learning-content.tsx)                 | 题目、反馈与学习内容的消息呈现。                               |
| [learning-dashboard.tsx](learning-dashboard.tsx)             | 学情看板页面。                                                 |
| [learning-map-canvas.tsx](learning-map-canvas.tsx)           | 学情知识图谱的绘制和节点交互。                                 |
| [learning-map-state.ts](learning-map-state.ts)               | 知识图谱的缩放、定位和选中状态。                               |
| [learning-route.css](learning-route.css)                     | 学习路径地图和节点样式。                                       |
| [learning-route.tsx](learning-route.tsx)                     | 可选择多条链路的学习路径地图。                                 |
| [learning-summary.tsx](learning-summary.tsx)                 | 看板开头的学情摘要。                                           |
| [learning-trend.tsx](learning-trend.tsx)                     | 展示学习证据与变化趋势。                                       |
| [learning.tsx](learning.tsx)                                 | 学习页面的模块入口与数据连接。                                 |
| [main.tsx](main.tsx)                                         | React 应用挂载入口。                                           |
| [math-number.ts](math-number.ts)                             | 精确数值、分数与根式的可读标签。                               |
| [model-settings.tsx](model-settings.tsx)                     | 模型连接与文本、视觉角色设置页面。                             |
| [module.ts](module.ts)                                       | 教育 Web 模块与依赖声明。                                      |
| [opposite-animation.tsx](opposite-animation.tsx)             | 相反数的同步对称点、等距线段和抵消关系的动画视图。             |
| [pages.tsx](pages.tsx)                                       | 四项学生功能的页面组织。                                       |
| [plot-ticks.ts](plot-ticks.ts)                               | 函数图坐标刻度与标签。                                         |
| [problem-animation.tsx](problem-animation.tsx)               | 绑定原题的解题步骤动画。                                       |
| [provider-editor.tsx](provider-editor.tsx)                   | 供应商连接和嵌套模型的编辑界面。                               |
| [provider-form.ts](provider-form.ts)                         | 模型表单字段、草稿与校验。                                     |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                               |
| [settings-panel.tsx](settings-panel.tsx)                     | 系统管理、模型适配与项目架构设置页。                           |
| [settings.css](settings.css)                                 | 设置界面的布局与样式。                                         |
| [static-reasoning-diagram.tsx](static-reasoning-diagram.tsx) | 解题推理的静态图示。                                           |
| [student-task-results.tsx](student-task-results.tsx)         | 对话中的题卡、学情和路线展示，以及旧错误回复的明确重执行入口。 |
| [styles.css](styles.css)                                     | 学生工作台的整体主题和布局样式。                               |
| [teaching-animation.tsx](teaching-animation.tsx)             | 教学动画的播放器与分段控制。                                   |
| [teaching-plots.tsx](teaching-plots.tsx)                     | 函数坐标和教学图组件。                                         |
| [teaching-visuals.css](teaching-visuals.css)                 | 教学图、播放器与标注布局。                                     |
| [teaching-visuals.tsx](teaching-visuals.tsx)                 | 选择和展示本轮教学图示。                                       |
| [turn-status.tsx](turn-status.tsx)                           | 运行、停止、失败与明确重新回答的消息操作。                     |
| [tutor-extras.tsx](tutor-extras.tsx)                         | 辅导附件和消息附加内容。                                       |
| [tutor-message-images.tsx](tutor-message-images.tsx)         | 用户消息内多张图片的展示。                                     |
| [use-chat-models.ts](use-chat-models.ts)                     | 读取会话模型目录并冻结发送配置。                               |
| [use-teaching-animation.ts](use-teaching-animation.ts)       | 连续播放、暂停、进度和逐步切换状态。                           |
| [use-workspace.ts](use-workspace.ts)                         | 管理草稿、请求生命周期、SSE 和历史恢复。                       |
| [visual-annotation.tsx](visual-annotation.tsx)               | 图上画笔、直线、曲线、标记与返图。                             |
| [workspace.tsx](workspace.tsx)                               | 对话工作区、输入框、发送和回复展示。                           |

<!-- qingqi-directory-index:end -->
