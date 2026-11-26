# remote-e2e-stability

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

remote e2e stability 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                                               | 简要说明                                                           |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [01-mobile-home-onboarding.md](01-mobile-home-onboarding.md)                                       | 手机远控首页被职业引导覆盖：说明文档。                             |
| [02-uninstall-reinstall-entry.md](02-uninstall-reinstall-entry.md)                                 | 卸载重装后的身份换代缺少确认入口：说明文档。                       |
| [03-share-api-unavailable.md](03-share-api-unavailable.md)                                         | SSH 产物分享的生产接口间歇性失败：说明文档。                       |
| [04-management-blocked-by-remote-counts.md](04-management-blocked-by-remote-counts.md)             | 远程 RPC 停滞时设备管理页无法显示已有设备与断开入口：说明文档。    |
| [05-directory-permission-reattach.md](05-directory-permission-reattach.md)                         | 目录权限收回后仍挂回为可用远程会话：说明文档。                     |
| [06-edited-route-ignored-by-project-reconnect.md](06-edited-route-ignored-by-project-reconnect.md) | 修改 SSH 地址后，侧栏原地重连仍使用旧线路：说明文档。              |
| [07-existing-project-upgrade-intent.md](07-existing-project-upgrade-intent.md)                     | 原项目连接中的认证、升级与重装交接缺失：说明文档。                 |
| [08-reinstall-history-visible-in-new-device.md](08-reinstall-history-visible-in-new-device.md)     | 保留数据卸载重装应沿用原设备身份与历史：说明文档。                 |
| [09-live-team-model-precondition.md](09-live-team-model-precondition.md)                           | 真实 Team 模型验证的本机前置未就绪：说明文档。                     |
| [10-connection-wizard-test-entry.md](10-connection-wizard-test-entry.md)                           | 连接向导 case 误用项目创建入口：说明文档。                         |
| [11-ssh-credential-missing-after-restart.md](11-ssh-credential-missing-after-restart.md)           | SSH 已保存连接在冷重启后缺少凭据：说明文档。                       |
| [12-project-symlink-workspace-identity.md](12-project-symlink-workspace-identity.md)               | 远程项目从符号链接创建任务后未收敛到 realpath identity：说明文档。 |
| [13-startup-reconnect-description.md](13-startup-reconnect-description.md)                         | 自动重连设置仍描述已取消的 7 天过滤：说明文档。                    |
| [14-renderer-reload-task-navigation.md](14-renderer-reload-task-navigation.md)                     | Renderer 重载后已就绪的远程任务无法切换：说明文档。                |
| [15-cold-start-open-workspace-siblings.md](15-cold-start-open-workspace-siblings.md)               | 冷启动未补齐已打开的另一远程工作区：说明文档。                     |
| [16-settings-show-project-focus.md](16-settings-show-project-focus.md)                             | 设置页“在侧边栏中显示”未定位项目焦点：说明文档。                   |
| [17-unavailable-root-history-navigation.md](17-unavailable-root-history-navigation.md)             | 远程主目录失效后原任务历史无法打开：说明文档。                     |
| [18-upgraded-project-history-open.md](18-upgraded-project-history-open.md)                         | 旧版项目历史打开：测试交互修正：说明文档。                         |
| [19-history-conflict-blocks-project-picker.md](19-history-conflict-blocks-project-picker.md)       | 单个工作区历史冲突阻塞整个远程项目选择页：说明文档。               |
| [20-retry-progress-not-visible.md](20-retry-progress-not-visible.md)                               | 自动重连执行三次，但项目页不显示重试进度：说明文档。               |
| [21-optional-update-notice-missing.md](21-optional-update-notice-missing.md)                       | 兼容版本连接成功后，设备卡缺少可延后的更新提示：说明文档。         |
| [22-project-editor-focus-missing.md](22-project-editor-focus-missing.md)                           | 从项目菜单打开编辑器后焦点仍在页面 body：说明文档。                |
| [23-desktop-upgrade-guidance-missing.md](23-desktop-upgrade-guidance-missing.md)                   | 版本门禁详情没有说明应升级桌面端：说明文档。                       |
| [24-remote-task-running-indicator-missing.md](24-remote-task-running-indicator-missing.md)         | 远程会话正在生成，侧栏任务行没有运行标志：说明文档。               |
| [25-data-directory-restart-startup-failure.md](25-data-directory-restart-startup-failure.md)       | 桌面设置和数据目录变更后冷启动失败：说明文档。                     |
| [26-minimized-connection-progress-missing.md](26-minimized-connection-progress-missing.md)         | 收起连接向导后主界面没有进度卡：说明文档。                         |
| [27-concurrent-navigation-shared-session.md](27-concurrent-navigation-shared-session.md)           | 并发导航进入同一远程项目时，共享会话被提前销毁：说明文档。         |
| [28-connect-wizard-one-click-sync-unreachable.md](28-connect-wizard-one-click-sync-unreachable.md) | 连接向导「一键同步」入口在现有流程中不可达：说明文档。             |
| [README.md](README.md)                                                                             | 本目录用途、子目录与逐文件说明。                                   |

<!-- qingqi-directory-index:end -->
