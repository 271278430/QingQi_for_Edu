# image

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 image 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                  |
| ------------------------------------------ | ----------------------------------------------------------------------------------------- |
| [image-budget.ts](image-budget.ts)         | 实现或公开接口：ImageBudget、createImageBudget、validatePrepareRequest、fitsImageBudget。 |
| [index.ts](index.ts)                       | 实现或公开接口：createJimpImageProcessorAdapter。                                         |
| [jimp-compression.ts](jimp-compression.ts) | PNG 原尺寸优化失败后，旧策略会在每个缩放档重新尝试 PNG，导致较大尺寸 JPEG                 |
| [jimp-media.ts](jimp-media.ts)             | 实现或公开接口：normalizeMediaType、jimpOutputMediaType、throwIfAborted。                 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                          |
| [webp-passthrough.ts](webp-passthrough.ts) | 实现或公开接口：prepareWebpPassthrough。                                                  |

<!-- qingqi-directory-index:end -->
