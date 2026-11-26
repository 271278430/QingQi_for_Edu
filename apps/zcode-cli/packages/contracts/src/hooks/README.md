# hooks

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/contracts 基础工程中的 hooks 生命周期与操作入口。

### 文件

| 文件                                                           | 简要说明                                                                                  |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [index.ts](index.ts)                                           | \* hook 自身出错（非 0 且非 2 退出、超时、输出 JSON 不合 schema）时怎么办。缺省 `allow`： |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                          |
| [workspace-hook-trust-store.ts](workspace-hook-trust-store.ts) | \* Trust store 文件 schema 已下沉到 `@zcode/shared/workspace-hook-trust-store-file`       |
| [workspace-hook-trust.ts](workspace-hook-trust.ts)             | onError 进声明摘要（shared/workspace-hook-digest.ts），改了要重新信任。                   |

<!-- qingqi-directory-index:end -->
