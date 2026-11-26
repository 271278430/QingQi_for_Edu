# runtime

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 runtime 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                               | 简要说明                                                                               |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [provider-readiness-agent-startup.test.ts](provider-readiness-agent-startup.test.ts)               | 修复原因：只看 Process Monitor 只能证明 CLI 启动，不能证明用户真的拿到了历史。         |
| [README.md](README.md)                                                                             | 本目录用途、子目录与逐文件说明。                                                       |
| [workspace-agent-warmup-lifecycle.test.ts](workspace-agent-warmup-lifecycle.test.ts)               | renderer reload 应只给存活 Host 重新挂 MessagePort，不能重跑 InitLocal 或复制 Agent。  |
| [workspace-agent-warmup-small-set.test.ts](workspace-agent-warmup-small-set.test.ts)               | workspace-agent-warmup-small-set.test 的实现文件。                                     |
| [workspace-close-persists-across-restart.test.ts](workspace-close-persists-across-restart.test.ts) | 原因：项目归属由 Host 一次迁移；旧 settings 的目录快照不能在重启时重新生成已删除入口。 |
| [workspace-passive-agent-startup.test.ts](workspace-passive-agent-startup.test.ts)                 | workspace-passive-agent-startup.test 的实现文件。                                      |
| [workspace-provider-save-dormant-agent.test.ts](workspace-provider-save-dormant-agent.test.ts)     | Bug 回归：旧 provider 同步会串行启动 6 个 dormant workspace；观察窗口必须覆盖          |
| [workspace-removal-runtime-release.test.ts](workspace-removal-runtime-release.test.ts)             | 本例使用两个专用目录，不能调用强制等待默认 ZCodeProject 的通用准备入口。               |

<!-- qingqi-directory-index:end -->
