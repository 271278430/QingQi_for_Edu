# credential-security

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 credential security 实现源码。

### 文件

| 文件                                                   | 简要说明                                                             |
| ------------------------------------------------------ | -------------------------------------------------------------------- |
| [bridge.ts](bridge.ts)                                 | 只走已建立的可信进程通道；系统主密钥始终留在 owner，不进入消息载荷。 |
| [contract.example.ts](contract.example.ts)             | 实现或公开接口：credentialCipherExample。                            |
| [CONTRACT.md](CONTRACT.md)                             | 模块职责、公共接口、依赖方向和状态约定。                             |
| [contract.ts](contract.ts)                             | 独立 Server 在开放服务前验证安全后端；不返回密钥。                   |
| [module.ts](module.ts)                                 | module 的实现文件。                                                  |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                     |
| [systemCredentialCipher.ts](systemCredentialCipher.ts) | 与凭据文件同目录的来源标记；内容只能是 OS_SOURCE_MARKER，不含密钥。  |

<!-- qingqi-directory-index:end -->
