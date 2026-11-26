# embedded-browser-permission-contract

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 embedded browser permission contract 实现源码。

### 文件

| 文件                                       | 简要说明                                           |
| ------------------------------------------ | -------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 装配方传入现有工厂和依赖，不通过契约另起生命周期。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。           |
| [contract.ts](contract.ts)                 | 既有入口的类型契约；不创建第二份状态或转发实现。   |
| [module.ts](module.ts)                     | 只登记现有入口；实现位置与调用链保持不变。         |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                   |

<!-- qingqi-directory-index:end -->
