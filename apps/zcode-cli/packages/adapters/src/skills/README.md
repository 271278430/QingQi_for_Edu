# skills

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 skills 技能指导和资源。

### 文件

| 文件                   | 简要说明                                                                          |
| ---------------------- | --------------------------------------------------------------------------------- |
| [index.ts](index.ts)   | Node Skill Adapter                                                                |
| [README.md](README.md) | 本目录用途、子目录与逐文件说明。                                                  |
| [roots.ts](roots.ts)   | 合并而不是 fallback：用户可能同时安装原生 `.zcode` skill 和兼容 `.agents` skill。 |
| [scan.ts](scan.ts)     | manifest 的 skills 项既可指向单个技能目录，也可指向一层技能集合。                 |

<!-- qingqi-directory-index:end -->
