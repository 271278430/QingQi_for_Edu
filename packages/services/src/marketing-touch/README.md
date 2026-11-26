# marketing-touch

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 marketing touch 实现源码。

### 文件

| 文件                                                   | 简要说明                                                                         |
| ------------------------------------------------------ | -------------------------------------------------------------------------------- |
| [marketingAssetRegistry.ts](marketingAssetRegistry.ts) | 下载授权只来自宿主已验证的投放响应；Renderer 不能自行授权地址。                  |
| [marketingTouch.ts](marketingTouch.ts)                 | 实现或公开接口：IMarketingTouchService。                                         |
| [marketingTouchService.ts](marketingTouchService.ts)   | X-Client-Language 必须是真实界面语言（含 ja-JP/ru-RU/ko-KR），不能先降级成中英。 |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                 |

<!-- qingqi-directory-index:end -->
