# gen-ui

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 gen ui 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                                |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：exampleGenUiReference、exampleGenUiState、exampleGenUiTweakRegistration。                               |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                                                |
| [contract.ts](contract.ts)                 | 自有 CDN：visualize/gen-ui 页面引用 zcode.z.ai 上的图片等静态资源（与上面公共 CDN 同走 resourceDomains，                |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                                      |
| [module.ts](module.ts)                     | 实现或公开接口：genUiProtocolModule。                                                                                   |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                                        |
| [tweakProtocol.ts](tweakProtocol.ts)       | 实现或公开接口：genUiAnnotationControlSchema、GenUiAnnotationControl、isGenUiAnnotationValue、genUiTweakMessageSchema。 |

<!-- qingqi-directory-index:end -->
