# upgrade

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 upgrade 测试场景。

### 文件

| 文件                                                                                                         | 简要说明                                                                        |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| [coding-plan-upgrade-personal-sold-out.test.ts](coding-plan-upgrade-personal-sold-out.test.ts)               | 本地 mock 只接管 BigModel 账号；夹带另一个账号族会访问真实控制面并污染登录态。  |
| [coding-plan-upgrade-personal-system-busy.test.ts](coding-plan-upgrade-personal-system-busy.test.ts)         | coding-plan-upgrade-personal-system-busy.test 的实现文件。                      |
| [coding-plan-upgrade-webview-refresh-provider.test.ts](coding-plan-upgrade-webview-refresh-provider.test.ts) | 测试窗口沿用当前语言；英文专用断言会把正确的中文 loading/error 误判为业务失败。 |
| [README.md](README.md)                                                                                       | 本目录用途、子目录与逐文件说明。                                                |

<!-- qingqi-directory-index:end -->
