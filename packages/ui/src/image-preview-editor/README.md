# image-preview-editor

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 image preview editor 实现源码。

### 文件

| 文件                                               | 简要说明                                                                    |
| -------------------------------------------------- | --------------------------------------------------------------------------- |
| [annotations.tsx](annotations.tsx)                 | 只栅格化当前原图与标注；不用屏幕截图，避免缩放和主题背景污染输出像素。      |
| [composerTarget.ts](composerTarget.ts)             | 同步捕获当前接收方。异步导出完成后不能重新查找，以免追加到另一会话。        |
| [contract.example.ts](contract.example.ts)         | 接收方沿用既有附件 API；不能从此处调用发送命令。                            |
| [CONTRACT.md](CONTRACT.md)                         | 模块职责、公共接口、依赖方向和状态约定。                                    |
| [contract.ts](contract.ts)                         | 同步走现有附件 admission；拒绝时返回 false，不发送消息。                    |
| [geometry.ts](geometry.ts)                         | 实现或公开接口：Point、Size、Transform、History。                           |
| [ImageEditorToolbar.tsx](ImageEditorToolbar.tsx)   | 实现或公开接口：ImageEditorToolbar。                                        |
| [ImagePreviewActions.tsx](ImagePreviewActions.tsx) | 只有保存后的真实本机文件才能查询系统关联；下载/定位也必须刷新默认应用身份。 |
| [ImagePreviewSurface.tsx](ImagePreviewSurface.tsx) | 实现或公开接口：ImagePreviewSurface。                                       |
| [index.ts](index.ts)                               | index 的实现文件。                                                          |
| [module.ts](module.ts)                             | 实现或公开接口：imagePreviewEditorModule。                                  |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                            |

<!-- qingqi-directory-index:end -->
