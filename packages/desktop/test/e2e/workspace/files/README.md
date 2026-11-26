# files

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 files 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                           | 简要说明                                                               |
| ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [README.md](README.md)                                                                         | 本目录用途、子目录与逐文件说明。                                       |
| [workspace-file-tree-compact-hierarchy.test.ts](workspace-file-tree-compact-hierarchy.test.ts) | 首次懒加载合并时只有 chat 已展开；重开后则由 transport 保存展开标记。  |
| [workspace-file-tree-refresh.test.ts](workspace-file-tree-refresh.test.ts)                     | 文件树已迁到右侧标签；左侧导航保持可用，不再等待退役侧栏的位移动画。   |
| [workspace-file-tree-shared-search.test.ts](workspace-file-tree-shared-search.test.ts)         | 前序用例已建立搜索索引；重启后读取本例新建文件，避免依赖索引刷新时机。 |

<!-- qingqi-directory-index:end -->
