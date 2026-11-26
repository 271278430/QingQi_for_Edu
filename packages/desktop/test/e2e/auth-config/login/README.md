# login

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 login 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                     | 简要说明                                                                                    |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| [oauth-completion-race.test.ts](oauth-completion-race.test.ts)           | oauth-completion-race.test 的实现文件。                                                     |
| [oauth-login-failure-cancel.test.ts](oauth-login-failure-cancel.test.ts) | PlatformChannels.OAuthCallback 的 channel 值(main 进程 execute 里无法 import @zcode/shared, |
| [oauth-provisioning.test.ts](oauth-provisioning.test.ts)                 | oauth-provisioning.test 的实现文件。                                                        |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                            |

<!-- qingqi-directory-index:end -->
