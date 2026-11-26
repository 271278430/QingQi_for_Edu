# platform

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 platform 实现源码。

### 文件

| 文件                                       | 简要说明                                                                 |
| ------------------------------------------ | ------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | 此处 success 表示下载已发起，浏览器不提供实际落盘结果。                  |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                 |
| [contract.ts](contract.ts)                 | 实现或公开接口：WebRemoteControlPlatformProxy。                          |
| [index.ts](index.ts)                       | Web 端无法打开系统目录选择框                                             |
| [module.ts](module.ts)                     | \* web-platform 模块清单（architecture-governance managed 模块）。       |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                         |
| [saveBrowserFile.ts](saveBrowserFile.ts)   | 文件名来自上游产物；去掉路径和平台非法字符，避免浏览器把它当作目标目录。 |

<!-- qingqi-directory-index:end -->
