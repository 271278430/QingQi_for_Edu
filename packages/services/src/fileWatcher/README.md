# fileWatcher

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 fileWatcher 实现源码。

### 文件

| 文件                                           | 简要说明                                                          |
| ---------------------------------------------- | ----------------------------------------------------------------- |
| [fileWatcher.ts](fileWatcher.ts)               | \* 按路径粒度管理 watcher 实例。UI 展开目录时调用非递归 watch()， |
| [fileWatcherService.ts](fileWatcherService.ts) | 防抖时间（ms）——批量文件变更（如 git checkout）时避免频繁刷新     |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                  |

<!-- qingqi-directory-index:end -->
