# plugin-startup-budget

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 plugin startup budget 实现源码。

### 文件

| 文件                                       | 简要说明                                                         |
| ------------------------------------------ | ---------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：resolveWithinStartupBudget。                     |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                         |
| [contract.ts](contract.ts)                 | 进程拥有的插件等待预算；超时降级只能由新进程解除。               |
| [index.ts](index.ts)                       | index 的实现文件。                                               |
| [module.ts](module.ts)                     | 同步摘要计算可能推迟定时器；完成时仍检查预算，不能接受超期结果。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                 |

<!-- qingqi-directory-index:end -->
