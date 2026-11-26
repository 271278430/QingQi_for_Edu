# marketing

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 marketing 测试场景。

### 文件

| 文件                                                                               | 简要说明                                                                                 |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [marketing-touch-anonymous.test.ts](marketing-touch-anonymous.test.ts)             | 只判断凭据是否存在，失败输出也不得带出凭据内容。                                         |
| [marketing-touch-delivery.test.ts](marketing-touch-delivery.test.ts)               | 原截图写入系统临时目录，违反运行目录隔离；统一归档到本轮报告目录。                       |
| [marketing-touch-entitlement.test.ts](marketing-touch-entitlement.test.ts)         | 通过隔离服务 fixture 准备已领取状态；真实 Banner/安全校验/上报链路由 delivery 用例覆盖。 |
| [marketing-touch-rewards.test.ts](marketing-touch-rewards.test.ts)                 | 正式 App 合同测试：网页与 App API 采用隔离 HTTP fixture，不提交邀请或发奖。              |
| [marketing-touch-task-completion.test.ts](marketing-touch-task-completion.test.ts) | 隔离账号可能首次进入引导；通过公开 Esc 行为关闭，不改写账号记录。                        |
| [README.md](README.md)                                                             | 本目录用途、子目录与逐文件说明。                                                         |

<!-- qingqi-directory-index:end -->
