# workflow-artifacts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 workflow artifacts 实现源码。

### 子目录

| 目录                          | 存放内容                                  |
| ----------------------------- | ----------------------------------------- |
| [presets/](presets/README.md) | @zcode/ui 基础工程中的 presets 实现源码。 |

### 文件

| 文件                                                               | 简要说明                                                                                           |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| [artifactPresentation.tsx](artifactPresentation.tsx)               | \* 用户面产物在**几个表面**（run 侧板瓦片、完成卡瓦片、`workflow-artifact` tab、通知行药丸、中枢） |
| [ArtifactPresetBody.tsx](ArtifactPresetBody.tsx)                   | _ ⚠ 术语：artifact = 脚本经 `artifact._` 发布给用户看的产出，不是引擎内部那个「脚本顶层返回值」    |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                   |
| [WorkflowArtifactBody.tsx](WorkflowArtifactBody.tsx)               | \* `workflow-artifact` tab 的正文。                                                                |
| [WorkflowArtifactCards.tsx](WorkflowArtifactCards.tsx)             | \* 「不能内联渲染」的三种正文（html 卡、表外类型的元数据卡、loading / 错误的一句话）。             |
| [WorkflowArtifactTilePreview.tsx](WorkflowArtifactTilePreview.tsx) | \* 产物瓦片的预览区（侧板画廊同用）：产物**本身**的缩略。                                          |

<!-- qingqi-directory-index:end -->
