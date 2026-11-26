# resident-rows-range

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 resident rows range 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                       |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | \* remote-resident-rows-range 标准调用示例：Host 转发只读热会话 rowsRange 前先确认执行端能力。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                       |
| [contract.test.ts](contract.test.ts)       | contract.test 的实现文件。                                                                     |
| [contract.ts](contract.ts)                 | 旧 CLI 的 rowsRange 会剥掉 residency 并冷恢复；确认执行端认识它才转发只读热会话请求。          |
| [module.ts](module.ts)                     | \* remote-resident-rows-range 模块清单（architecture-governance managed 模块）。               |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                               |

<!-- qingqi-directory-index:end -->
