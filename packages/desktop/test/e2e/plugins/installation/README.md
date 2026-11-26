# installation

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 installation 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                         | 简要说明                                                                                   |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [plugin-cdn-zip-marketplace-install.test.ts](plugin-cdn-zip-marketplace-install.test.ts)     | plugin-cdn-zip-marketplace-install.test 的实现文件。                                       |
| [plugin-concurrent-install.test.ts](plugin-concurrent-install.test.ts)                       | PLM-DETAIL-DURING-INSTALL：A 下载中、B 排在 A 后面时打开其他插件详情。                     |
| [plugin-management-builtin-inline.test.ts](plugin-management-builtin-inline.test.ts)         | 内置插件原本就不在 installedPlugins；等待真正的抑制状态，避免卸载 RPC 尚未完成就检查清理。 |
| [plugin-management-persistence-source.test.ts](plugin-management-persistence-source.test.ts) | 项目市场菜单写 workspace 覆盖；重启与跨项目断言需要真实 user-scope 操作。                  |
| [plugin-management-personal-lifecycle.test.ts](plugin-management-personal-lifecycle.test.ts) | plugin-management-personal-lifecycle.test 的实现文件。                                     |
| [plugin-no-git-github-archive.test.ts](plugin-no-git-github-archive.test.ts)                 | WebDriver 的 executeAsync 默认 30 秒；真实公网下载由 Agent 完成，Renderer bridge 只是在    |
| [README.md](README.md)                                                                       | 本目录用途、子目录与逐文件说明。                                                           |

<!-- qingqi-directory-index:end -->
