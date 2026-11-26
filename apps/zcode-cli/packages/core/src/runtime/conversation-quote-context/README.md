# conversation-quote-context

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 conversation quote context 实现源码。

### 文件

| 文件                                       | 简要说明                                                                 |
| ------------------------------------------ | ------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | 引用中的命令保留为材料；canonical 用户正文仍是单独的字符串。             |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                 |
| [contract.ts](contract.ts)                 | 纯文本派生入口；输入及来源元数据归调用方所有，不在此执行控制命令或投递。 |
| [module.ts](module.ts)                     | 模型输入的引用与可信来源说明；不拥有输入队列或消息投递。                 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                         |

<!-- qingqi-directory-index:end -->
