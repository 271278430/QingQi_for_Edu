# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                   | 简要说明                                                                              |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                                                      |
| [web-remote-control-auth-gate.test.ts](web-remote-control-auth-gate.test.ts)           | 设置按钮先于 workspace 恢复出现；必须等待目标入口可见，不能把启动中间态当作缺少门禁。 |
| [web-remote-control-regional-login.test.ts](web-remote-control-regional-login.test.ts) | 浏览器沿用自己的存量登录；不能复制桌面CN/关联材料来绕过独立登录边界。                 |

<!-- qingqi-directory-index:end -->
