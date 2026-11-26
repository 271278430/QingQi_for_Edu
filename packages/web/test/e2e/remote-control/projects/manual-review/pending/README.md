# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                         | 简要说明                                                                           |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                   |
| [remote-device-groups.mjs](remote-device-groups.mjs)                         | MD08–MD10：设备按完整 MID 聚合，SID 保持独立选择和连接。                           |
| [remote-device-switch.helpers.mjs](remote-device-switch.helpers.mjs)         | 设备导航验证用桌面 RPC 替身；采用真实帧协议，不模拟 UI 或修改产品模块。            |
| [remote-device-switch.mjs](remote-device-switch.mjs)                         | MD07：真实 Web 入口，受控 relay/桌面响应；不替代真机 OAuth/线上部署验收。          |
| [remote-home-only-workspaces.mjs](remote-home-only-workspaces.mjs)           | HO01：home-only 首页工作区列表与重连入口；真实 Web 入口，受控 relay/桌面响应。     |
| [remote-project-directory.fixture.mjs](remote-project-directory.fixture.mjs) | MRO02：真实 ProjectService / RemoteProjectService / SQLite，网络和模型由用例控制。 |
| [remote-project-directory.mjs](remote-project-directory.mjs)                 | MRO02：真实 Web 页面、RPC、Host 项目服务和隔离 SQLite；不发送模型请求。            |
| [remote-task-open.fixture.mjs](remote-task-open.fixture.mjs)                 | 只提供已完成历史，不产生模型请求；快照经真实协议 schema 校验后送入 renderer。      |
| [remote-task-open.mjs](remote-task-open.mjs)                                 | MRO01：真实 Web 入口与 RPC 帧；受控桌面 bridge 成功/失败，不发送模型请求。         |

<!-- qingqi-directory-index:end -->
