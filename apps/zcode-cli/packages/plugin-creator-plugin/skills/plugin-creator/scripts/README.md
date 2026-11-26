# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/plugin-creator-plugin 基础工程中的 scripts 工程脚本。

### 文件

| 文件                                                     | 简要说明                                                                  |
| -------------------------------------------------------- | ------------------------------------------------------------------------- |
| [create-basic-plugin.mjs](create-basic-plugin.mjs)       | 所有覆盖/路径检查先完成，避免在发现市场冲突前写出半份 scaffold。          |
| [marketplace-files.mjs](marketplace-files.mjs)           | 独占创建成功后才接管清理，避免失败时删除其他写入者的文件。                |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                          |
| [scaffold-files.mjs](scaffold-files.mjs)                 | 只生成已声明的组件；模板中的路径由插件 loader 在运行时解析。              |
| [upsert-dev-marketplace.mjs](upsert-dev-marketplace.mjs) | 只更新开发目录；安装状态始终由现有 CLI 管理，不能重写用户源码或内部缓存。 |
| [validate-plugin.mjs](validate-plugin.mjs)               | 附加完整性检查，不复制 ZCode 的 manifest schema。                         |

<!-- qingqi-directory-index:end -->
