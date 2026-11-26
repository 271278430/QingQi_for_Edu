# browser-local-preview

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 browser local preview 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                      |
| ------------------------------------------ | --------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | \* browser-local-preview 标准调用示例：agent 靠模仿写代码，这里放的就是该模仿的那份。         |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                      |
| [contract.ts](contract.ts)                 | 仅可信宿主调用；校验文件后授权其目录。非 file URL 原样返回，不授予新权限。                    |
| [index.ts](index.ts)                       | 完整退出会清空浏览器标签；进程内共享签名密钥即可支持刷新和 guest 恢复，无需第二份持久化状态。 |
| [module.ts](module.ts)                     | \* browser-local-preview 模块清单（architecture-governance managed 模块）。                   |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                              |

<!-- qingqi-directory-index:end -->
