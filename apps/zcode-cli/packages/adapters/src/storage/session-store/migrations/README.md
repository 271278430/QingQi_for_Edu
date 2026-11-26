# migrations

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 migrations 数据库迁移。

### 文件

| 文件                                                                         | 简要说明                                                                                   |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [0020-provider-model-selection.ts](0020-provider-model-selection.ts)         | 冻结的数据迁移只生成 SQL，checksum 覆盖最终 SQL；不调用可变账号/Registry。                 |
| [0021-official-glm-selection.ts](0021-official-glm-selection.ts)             | 冻结本次改名表与 SQL：不能改旧 migration 或引用会随发布变化的实时目录。                    |
| [0022-backfilled-session-reasoning.ts](0022-backfilled-session-reasoning.ts) | 0020 可能以不带档位的 assistant 回填会话选择；只能给迁移后未动过的会话补同模型 user 档位。 |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                           |

<!-- qingqi-directory-index:end -->
