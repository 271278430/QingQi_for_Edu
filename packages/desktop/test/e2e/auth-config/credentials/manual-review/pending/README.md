# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                       | 简要说明                                                                                     |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| [credential-store-recovery.test.ts](credential-store-recovery.test.ts)     | \* 单入口登录按区域选择渠道：中文默认国内 zai_cn，其轮询只受夹具 cn-ready 控制。             |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                             |
| [system-credential-data-root.test.ts](system-credential-data-root.test.ts) | ZCT-2120723935487688704：3.18.0 起系统条目按凭据文件路径区分，切换数据存储路径只复制文件时， |
| [system-credential-owner-mcp.test.ts](system-credential-owner-mcp.test.ts) | 采用完整的本地 MCP OAuth 授权、持久化及真实 CLI 工具回合，增加系统库 owner 断言。            |
| [system-credential-owner.test.ts](system-credential-owner.test.ts)         | 大 profile 加密后会膨胀；回复必须可接收，超限失败也不能卡住后续读写。                        |
| [system-credential-storage.test.ts](system-credential-storage.test.ts)     | 测试 HOME 不含 macOS 默认钥匙串；只链接系统库位置，应用数据仍留在隔离目录。                  |

<!-- qingqi-directory-index:end -->
