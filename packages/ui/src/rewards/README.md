# rewards

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 rewards 实现源码。

### 文件

| 文件                                       | 简要说明                                                                         |
| ------------------------------------------ | -------------------------------------------------------------------------------- |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                 |
| [RewardsProvider.tsx](RewardsProvider.tsx) | 登录后营销实例会重建；续接意图由窗口级 Provider 持有，不能挂在旧 controller 上。 |
| [RewardsWebview.tsx](RewardsWebview.tsx)   | 奖励页是外部网页，只有中英两套；非中文界面语言打开英文页。                       |

<!-- qingqi-directory-index:end -->
