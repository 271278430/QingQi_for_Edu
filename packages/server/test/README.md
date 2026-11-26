# test

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server 基础工程中的 test 测试场景。

### 文件

| 文件                                                                     | 简要说明                                                                                         |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                                 |
| [remoteOfficialPluginAssets.test.ts](remoteOfficialPluginAssets.test.ts) | design 的规则文件与脚本是会话里按需读取/执行的，远端缺一份只会在用到时失败；远端部署前的必需路径 |
| [tsupConfig.test.ts](tsupConfig.test.ts)                                 | Bugfix: pnpm 不会把传递依赖暴露给 @zcode/server；HTTP bundle 外置后必须从 server 自身解析。      |

<!-- qingqi-directory-index:end -->
