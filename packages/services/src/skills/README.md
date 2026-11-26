# skills

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 skills 技能指导和资源。

### 文件

| 文件                                           | 简要说明                                                                         |
| ---------------------------------------------- | -------------------------------------------------------------------------------- |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                 |
| [skillDiscoveryWalk.ts](skillDiscoveryWalk.ts) | 扫描策略来自 @zcode/shared，供桌面端（本包）与 agent 端（@zcode/adapters）共享， |
| [skills.ts](skills.ts)                         | 将指定 skill 复制到通用目录（.zcode/skills），成功后返回新 skill 的路径。        |
| [skillsService.ts](skillsService.ts)           | frontmatter 中出现过的顶层 key，保留给后续能力判断，不再作为 warning 暴露。      |

<!-- qingqi-directory-index:end -->
