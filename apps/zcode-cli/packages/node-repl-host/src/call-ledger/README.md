# call-ledger

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/node-repl-host 基础工程中的 call ledger 实现源码。

### 文件

| 文件                                               | 简要说明                                                                                                 |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [browser-broker-proxy.ts](browser-broker-proxy.ts) | 浏览器代理 broker（apps/zcode-cli/docs/design/v2/tool/20-node-repl-call-ledger.md「浏览器代理 broker」） |
| [contract.example.ts](contract.example.ts)         | 一次 js 调用：开条目 → broker 按 token 写入事实 → 结果组装读 facts → 关闭条目。                          |
| [CONTRACT.md](CONTRACT.md)                         | 模块职责、公共接口、依赖方向和状态约定。                                                                 |
| [contract.ts](contract.ts)                         | \* node_repl 调用账本的公开入口（apps/zcode-cli/docs/design/v2/tool/20-node-repl-call-ledger.md）。      |
| [ledger.ts](ledger.ts)                             | node_repl 调用账本（apps/zcode-cli/docs/design/v2/tool/20-node-repl-call-ledger.md）                     |
| [module.ts](module.ts)                             | \* node-repl-call-ledger 模块清单（architecture-governance managed 模块）。                              |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                                         |

<!-- qingqi-directory-index:end -->
