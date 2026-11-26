# smoke

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 smoke 测试场景。

### 文件

| 文件                                                     | 简要说明                                                                       |
| -------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [container-boot.test.ts](container-boot.test.ts)         | 修复原因：v4 renderer URL 只承载启动/恢复参数，workspace 绑定已经迁入 store。  |
| [e2ecase-regression.test.ts](e2ecase-regression.test.ts) | e2ecase-regression.test 的实现文件。                                           |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                               |
| [smoke.test.ts](smoke.test.ts)                           | 修复原因：v4 硬切后 legacy chat-view/chat-input 已退出产品 DOM；               |
| [upstream-provider.test.ts](upstream-provider.test.ts)   | 修复原因：beforeSession 重置 HOME 后会按当前 case 预置登录态；无条件点击欢迎页 |

<!-- qingqi-directory-index:end -->
