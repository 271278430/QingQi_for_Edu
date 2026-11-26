# search

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 search 实现源码。

### 文件

| 文件                                       | 简要说明                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 同一份原始历史可以分别生成两种请求，调用方不保存投影结果作为新历史。                  |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                              |
| [contract.ts](contract.ts)                 | 契约直接采用现有入口；投影不改写 canonical 历史，工具执行仍由执行器负责。             |
| [description.ts](description.ts)           | Local 返回的定义描述目标参数，不能把它误读成已注册的直接调用入口。                    |
| [exposure.ts](exposure.ts)                 | 全部提升后仍需要控制入口处理后续目录变化，不能用剩余 deferred 数量关闭 Local。        |
| [history.ts](history.ts)                   | 同批结果尚未被模型看到：直到下一条 assistant 才合入已交付集合，避免并行搜索互相去重。 |
| [local-projection.ts](local-projection.ts) | 编码只在本次请求内采用；下一请求必须读取当前定义，不能跨请求留下过期 schema。         |
| [module.ts](module.ts)                     | 搜索控制入口、目录及请求投影共用现有工具执行身份。                                    |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                      |
| [search.ts](search.ts)                     | 实现或公开接口：searchTools。                                                         |

<!-- qingqi-directory-index:end -->
