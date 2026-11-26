# account

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 account 测试场景。

### 文件

| 文件                                                                                                 | 简要说明                                                                         |
| ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [account-key-usage-scene.test.ts](account-key-usage-scene.test.ts)                                   | 采用已有账号 mock 数据；没有目标名称 Key，由真实 Host resolver 发起创建。        |
| [coding-plan-team-usage.test.ts](coding-plan-team-usage.test.ts)                                     | 修复原因：WDIO 为每个 run 注入隔离 HOME，但 os.homedir() 在 Node 进程中不会      |
| [README.md](README.md)                                                                               | 本目录用途、子目录与逐文件说明。                                                 |
| [subagent-coding-plan-login-catalog-stale.test.ts](subagent-coding-plan-login-catalog-stale.test.ts) | 登录后的目录以当前内置配置的 GLM-5.3 为准，旧 release payload 不再定义模型成员。 |

<!-- qingqi-directory-index:end -->
