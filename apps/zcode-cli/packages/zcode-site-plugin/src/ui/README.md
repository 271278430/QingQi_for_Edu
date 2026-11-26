# ui

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/zcode-site-plugin 基础工程中的 ui 实现源码。

### 文件

| 文件                           | 简要说明                                                                                             |
| ------------------------------ | ---------------------------------------------------------------------------------------------------- |
| [analytics.tsx](analytics.tsx) | \* 站点的「数据统计」标签（技术方案 8.1）：区间切换、四个核心指标、PV / UV 趋势和四种分布。          |
| [host.ts](host.ts)             | 页面导航状态，经 ZCode 扩展 `ui/set-widget-state` 交给宿主内存保存，切换会话后恢复。                 |
| [i18n.ts](i18n.ts)             | \* 面板文案。只按错误码和原因生成，不展示服务端 msg；`zh-CN` 以外的语言回落 `en`。                   |
| [main.tsx](main.tsx)           | 握手期间宿主可能先推 hostContext 变化，此时还没有 host，跳过重绘。                                   |
| [model.test.ts](model.test.ts) | model.test 的实现文件。                                                                              |
| [model.ts](model.ts)           | 与 api/openapi.yaml 的 Site / Deployment / Usage / Plans / DeploymentLogs 一致；面板只读用到的字段。 |
| [panel.html](panel.html)       | panel 模块的资源或工程文件。                                                                         |
| [parts.tsx](parts.tsx)         | 套餐表；读失败时为 "failed"，只在用量页就地提示，不影响上方用量。                                    |
| [README.md](README.md)         | 本目录用途、子目录与逐文件说明。                                                                     |
| [site.tsx](site.tsx)           | 实现或公开接口：SitePage。                                                                           |
| [views.tsx](views.tsx)         | 实现或公开接口：App。                                                                                |

<!-- qingqi-directory-index:end -->
