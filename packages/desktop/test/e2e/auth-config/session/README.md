# session

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 session 测试场景。

### 文件

| 文件                                                                         | 简要说明                                                                            |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| [access-token-401-auto-logout.test.ts](access-token-401-auto-logout.test.ts) | 等待启动进入工作区，避免只观察首次核验、漏掉后续 PAT 资料读取造成的误退出。         |
| [jwt-401-auto-logout.test.ts](jwt-401-auto-logout.test.ts)                   | 旧用例 mock main net.fetch，不能证明 Host transport。先确认真实 Host 使用共享 JWT。 |
| [jwt-expiry-reauthentication.test.ts](jwt-expiry-reauthentication.test.ts)   | Bug 回归边界：认证事实必须在提示框确认前清理，否则用户停留在弹窗时仍会              |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                    |

<!-- qingqi-directory-index:end -->
