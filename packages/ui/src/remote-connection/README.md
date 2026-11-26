# remote-connection

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 remote connection 实现源码。

### 文件

| 文件                                                                     | 简要说明                                                                                               |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| [EditConnectionProfileDialog.tsx](EditConnectionProfileDialog.tsx)       | 0 表示尚未保存；每次字段校验失败递增，用于显示内联错误并聚焦第一个出错字段。                           |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                                       |
| [RemoteConnectionConnectingStep.tsx](RemoteConnectionConnectingStep.tsx) | 连接向导与侧栏详情共用的用户阶段；原始 phase 的归并规则只在这里维护一份。                              |
| [RemoteConnectionHistoryInput.tsx](RemoteConnectionHistoryInput.tsx)     | 实现或公开接口：RemoteConnectionHistoryInput。                                                         |
| [remoteConnectionHistoryPopover.ts](remoteConnectionHistoryPopover.ts)   | 实现或公开接口：shouldIgnoreRemoteConnectionHistoryPopoverInteractOutside。                            |
| [remoteConnectionLogScroll.ts](remoteConnectionLogScroll.ts)             | 实现或公开接口：isRemoteConnectionLogScrolledToLatest、scrollRemoteConnectionLogsToLatestIfFollowing。 |
| [RemoteConnectionSelection.tsx](RemoteConnectionSelection.tsx)           | 实现或公开接口：RemoteConnectionSelection。                                                            |
| [RemoteConnectionStateIcon.tsx](RemoteConnectionStateIcon.tsx)           | 项目行仅保留这一个状态图标位；已连接项目使用中性云。                                                   |
| [RemoteConnectionTags.tsx](RemoteConnectionTags.tsx)                     | \* 连接类型的唯一配色来源。类型 token 只表达连接类型（DESIGN.md），                                    |
| [RemoteLinkRail.tsx](RemoteLinkRail.tsx)                                 | 实现或公开接口：formatRemoteLinkRailTarget、formatRemoteLinkRailDevice。                               |
| [RemotePasswordInput.tsx](RemotePasswordInput.tsx)                       | 显隐只属于字段草稿，不复制凭据值，也不触发表单提交。                                                   |
| [RemoteTaskDeviceLabel.tsx](RemoteTaskDeviceLabel.tsx)                   | 实现或公开接口：RemoteTaskDeviceLabel。                                                                |
| [sshHistorySuggestions.ts](sshHistorySuggestions.ts)                     | SSH 历史候选要按最近连接顺序去重展示，否则同一个 host / username                                       |

<!-- qingqi-directory-index:end -->
