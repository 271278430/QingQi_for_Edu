# highspeed

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 highspeed 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                              |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| [highspeed-activation.css](highspeed-activation.css)               | Light 下使用反相后的深紫阶，保证模型标签、粒子与扫光在白底上可读（迁移自 ui/highspeed）。             |
| [highspeed-share.css](highspeed-share.css)                         | Highspeed 分享卡（左下角侧栏卡）与分享弹窗的样式与动效，视觉迁移自 ui/highspeed 分支。                |
| [HighspeedActivationVisual.tsx](HighspeedActivationVisual.tsx)     | \* 仅渲染 Highspeed 输入壳的视觉层；激活资格、有效期和模型仍由外部卡片快照决定。                      |
| [highspeedConversationRows.ts](highspeedConversationRows.ts)       | 协议行不可变，同一个行数组的到期时间集合不会变，升序缓存后按时钟二分即可。                            |
| [highspeedFooterExpiryClock.ts](highspeedFooterExpiryClock.ts)     | \* Highspeed 组尾 footer 的到期显隐时钟。                                                             |
| [HighspeedModelIndicator.tsx](HighspeedModelIndicator.tsx)         | 仅 draw 新命中时播放翻页入场；切回或恢复时直接呈现静止标识。                                          |
| [highspeedOutputFooter.ts](highspeedOutputFooter.ts)               | 由 footer 收口逻辑写回渲染单元的标记字段，宿主类型只需声明这两个可选字段。                            |
| [highspeedSavedTime.ts](highspeedSavedTime.ts)                     | CLI 已把真实模型/工具区间持久化；工具与其它等待不因模型换速而缩短。                                   |
| [highspeedSend.ts](highspeedSend.ts)                               | 与协议 payload 同源，避免 Renderer 再维护一份执行材料形状。                                           |
| [highspeedShare.ts](highspeedShare.ts)                             | \* 左下角分享卡通知的 payload。指标一律以毫秒事实携带（与发布门禁 isHighspeedShareEligible 同精度）， |
| [highspeedShareDiagnostics.ts](highspeedShareDiagnostics.ts)       | \* 诊断：这张卡为什么还不是自动分享候选，空数组表示已就绪。                                           |
| [HighspeedShareNoticeCard.tsx](HighspeedShareNoticeCard.tsx)       | Bug 根因：此前由秒级取整字段重建指标再复检资格，边界倍率被系统性低估而隐藏 View（spec §9）。          |
| [highspeedTime.ts](highspeedTime.ts)                               | 实现或公开接口：formatHighspeedRemainingTime。                                                        |
| [highspeedToastClaims.ts](highspeedToastClaims.ts)                 | \* 降级事件可能因 snapshot 重放或 SessionPane 重挂载被观察多次；模块级 claim 保证 Toast 只提示一次。  |
| [highspeedTurnHydration.ts](highspeedTurnHydration.ts)             | transcript → 内存记录的水合合并纯逻辑。从 highspeedTurnStore 拆出：store 只做状态 owner               |
| [highspeedTurnStore.ts](highspeedTurnStore.ts)                     | \* 冷启动恢复与跨端追平：到期时 renderer 可能不在场，内存 store 没有机会登记/收口这张卡；             |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                      |
| [useHighspeedComposerEntrance.ts](useHighspeedComposerEntrance.ts) | Highspeed 输入框入场方式：activation 播放激活动效，restore 直接呈现稳定态。                           |

<!-- qingqi-directory-index:end -->
