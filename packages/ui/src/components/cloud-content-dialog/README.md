# cloud-content-dialog

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 cloud content dialog 界面组件。

### 子目录

| 目录                      | 存放内容                                |
| ------------------------- | --------------------------------------- |
| [mocks/](mocks/README.md) | @zcode/ui 基础工程中的 mocks 界面组件。 |

### 文件

| 文件                                                     | 简要说明                                                                                   |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [CloudContentDialog.tsx](CloudContentDialog.tsx)         | macOS 窗口合成中，backdrop-filter 与隔离 iframe 叠加会在圆角外留下方形暗块；父层裁切无效。 |
| [cloudContentDialogTypes.ts](cloudContentDialogTypes.ts) | 仅宿主设置 resolvedUrl；随 App 打包的可信资源不伪装成云端 ZIP。                            |
| [cloudDescriptionStyle.ts](cloudDescriptionStyle.ts)     | CSS 解析之后仍禁止变量 fallback、转义和资源函数；不能只靠属性名单放行值。                  |
| [CloudDialogDescription.tsx](CloudDialogDescription.tsx) | Markdown 内嵌 HTML 作为文字；显式 html format 才进入 HTML 解析路径。                       |
| [CloudDialogHero.tsx](CloudDialogHero.tsx)               | Banner 的 iframe 必须隔离点击，因此只桥接视觉 hover，不放开原生指针或 action。             |
| [CloudDialogMediaHero.tsx](CloudDialogMediaHero.tsx)     | 实现或公开接口：CloudImage、CloudVideo、CloudLottie。                                      |
| [cloudLottieRuntime.ts](cloudLottieRuntime.ts)           | light 播放器不执行 expressions；同时阻断图片/字体外联，避免绕过资源来源校验。              |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                           |
| [useCloudHeroEnvironment.ts](useCloudHeroEnvironment.ts) | 实现或公开接口：useCloudHeroEnvironment。                                                  |

<!-- qingqi-directory-index:end -->
