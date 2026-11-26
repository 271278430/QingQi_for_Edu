# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server-cli 基础工程中的 scripts 工程脚本。

### 文件

| 文件                                                           | 简要说明                                                                               |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                       |
| [verify-proxy-stdio-docker.mjs](verify-proxy-stdio-docker.mjs) | \* R3 Docker Transport 验证：在真实 Linux 容器内安装 staged Source Server，启动 Core， |
| [verify-proxy-stdio-wsl.mjs](verify-proxy-stdio-wsl.mjs)       | \* R3 WSL Transport smoke：在真实 WSL 中从 archive 安装 Source Server，启动 daemon，   |
| [verify-remote-ssh-runtime.mjs](verify-remote-ssh-runtime.mjs) | 实现或公开接口：run、findFreePort、retry、assert。                                     |
| [verify-remote-ssh-target.mjs](verify-remote-ssh-target.mjs)   | 实现或公开接口：resolveVerificationTarget、dockerPlatformForTarget。                   |
| [verify-remote-ssh.mjs](verify-remote-ssh.mjs)                 | \* 远程验证编排：把 staged 发行包部署到带 sshd 的                                      |

<!-- qingqi-directory-index:end -->
