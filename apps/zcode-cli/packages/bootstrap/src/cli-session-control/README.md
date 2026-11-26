# cli-session-control

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 cli session control 实现源码。

### 文件

| 文件                                       | 简要说明                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 装配先取得 control，再创建并登记当前根；由宿主在关闭共享资源前 await close。          |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                              |
| [contract.test.ts](contract.test.ts)       | contract.test 的实现文件。                                                            |
| [contract.ts](contract.ts)                 | 新根的最小启动参数；不接受 actor mode、permission、parentSessionId 或 subagent 配置。 |
| [index.ts](index.ts)                       | index 的实现文件。                                                                    |
| [module.ts](module.ts)                     | 读本机会话库的列表只扫描有界窗口，避免一次把全部历史会话行解码进内存。                |
| [observation.ts](observation.ts)           | 本对象仅投影 owner 的输入事件，不持有 accepted queue，也不驱动执行。                  |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                      |

<!-- qingqi-directory-index:end -->
