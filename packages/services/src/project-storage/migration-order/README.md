# migration-order

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 migration order 实现源码。

### 文件

| 文件                         | 简要说明                                                                   |
| ---------------------------- | -------------------------------------------------------------------------- |
| [migration.ts](migration.ts) | 只在同一事务首次建立项目时调用；已经升级的用户不能再从旧 settings 猜顺序。 |
| [README.md](README.md)       | 本目录用途、子目录与逐文件说明。                                           |

<!-- qingqi-directory-index:end -->
