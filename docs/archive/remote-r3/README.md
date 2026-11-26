# R3 远程主链过程文档归档

2026-09-13 归档，2026-10-10 压缩过程正文。这些文档记录 R3 Source Server 远程主链的规格草案、评审、实施计划与实机测试过程，内容已被当前事实文档取代或并入，只作历史背景，不作实现依据。当前阅读入口见 [`docs/remote/README.md`](../../remote/README.md)。

| 文件                                                                     | 归档原因                                                                                                                                |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| `r3-remote-ui-prototype-gap-audit.md`                                    | §8 实施合同已并入主规格 §8.4；其余为原型逐界面差异审计与十二轮复审记录                                                                  |
| `r3-remote-ui-prototype-gap-audit-review.md`                             | 上述审计的复审记录                                                                                                                      |
| `r3-remote-ui-implementation.md`                                         | 实施记录；「新线路资源下载方式默认值」一条与代码矛盾（该偏好已于 2026-08-28 撤销），以主规格 §8.4.4 与 ux-spec 为准                     |
| `r3-provider-refactor-merge.md`                                          | Provider 重构合并过程记录；§7 遗留项已并入主规格 §15                                                                                    |
| `r3-controller-remote-row-migration-inventory.md`                        | 逐表盘点已并入主规格 §9.1                                                                                                               |
| `r3-source-server-remote-impact-brief.md`                                | 实施前影响简报                                                                                                                          |
| `r3-source-server-remote-implementation-review.md`                       | 实施评审记录                                                                                                                            |
| `r3-source-server-remote-completion-plan.md`                             | 完成计划；产品面缺口已随实现关闭或转入问题台账                                                                                          |
| `r3-source-server-remote-completion-review.md`                           | 完成计划评审记录                                                                                                                        |
| `remote-domain-simplification-and-conversation-workspace-spec-review.md` | 领域简化规格评审记录                                                                                                                    |
| `r3-source-server-release-test-plan.md`                                  | 旧发布测试方案；R3-REMOTE-xx 编号由 `conversation-session-case-catalog.md` 承载，执行方案由 `testing/r3-remote-automation-plan.md` 接替 |
| `r3-remote-automation-readiness-2026-09-07.md`                           | 自动化准备度记录                                                                                                                        |
| `r3-remote-environment-readiness-2026-09-08.md`                          | 环境准备度记录                                                                                                                          |
| `r3-remote-automation-live-run-2026-09-08.md`                            | 首批实跑台账；后续全量结果见 `testing/r3-remote-full-rerun-2026-09-10.md`                                                               |
| `r3-remote-full-validation-2026-09-08.md`                                | 早期全量验证记录，已被 2026-09-10 重跑取代                                                                                              |
| `r3-source-server-ssh-live-test-record-2026-08-20.md`                    | 实机记录，基线 commit 不是当前 HEAD 祖先（问题台账 R3-ISSUE-020）                                                                       |
| `r3-source-server-expanded-live-test-record-2026-08-21.md`               | 同上                                                                                                                                    |
| `ssh-project-entry-helper.md`                                            | 已并入 `testing/ssh-remote-p0-e2e-plan.md`「SSH 项目入口编排」                                                                          |

## 原始证据与读取方式

每个原文件保留历史入口。完整正文冻结在提交 `a17a875588b8d66c2bee49236292e174df651363`，使用入口中的
`git show <commit>:<path>` 读取；历史章节和行号均以该快照为准。此提交是文档快照，
不是这些实跑共同的产品基线。读取需要包含该提交的原始仓库历史；浅克隆或导出副本缺少对象时，应明确报告证据不可用，不能据入口推定验证通过。旧评审的未决项以当前问题台账逐项核对，不因压缩正文关闭。

| 证据                   | 必须保留的解释边界                                                                                                                                 |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-08-20/21 SSH 实跑 | 基线并非当前分支祖先，不能证明当前 HEAD；R3-ISSUE-020 仍待验证。原始环境、artifact 路径、通过与阻塞项在对应快照。                                  |
| 2026-09-08 首批验证    | 产品基线 `2af3a51991`；原三项 SSH E2E 为 0/3，后续代表通过不等于整套通过。原 artifact 根为 `packages/desktop/.e2e-artifacts/r3-20260907-155200/`。 |
| 环境准备度 / 早期全量  | 连接、登录、配对探针只能证明前置；历史 FAIL、BLOCKED 与清理记录保留在原快照，不转换为当前 PASS。                                                   |
| Provider 合并决策      | 采用本地编辑、自动 Provisioning；当前合同见 [Provider Provisioning](../../remote/provider-provisioning.md)，遗留项见主规格 §15。                   |
| 旧发布计划和审查       | 用例稳定 ID 由 case 目录承接；执行要求见当前测试方案。历史评论不是新增实施授权。                                                                   |

当前验证入口为[测试方案](../../testing/r3-remote-automation-plan.md)、
[9 月 10 日历史重跑](../../testing/r3-remote-full-rerun-2026-09-10.md)和
[10 月桌面 SSH 指南回归](../../testing/desktop-ssh-guide-regression.md)。各报告独立保留基线、范围与未验证项；
不同基线的 PASS 不相加为当前全量通过。原始日志、录像不在本次整理中移动或删除。

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

remote r3 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                                                                                             | 简要说明                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| [r3-controller-remote-row-migration-inventory.md](r3-controller-remote-row-migration-inventory.md)                                               | R3 控制端旧 remote 行逐表盘点：说明文档。                                                  |
| [r3-provider-refactor-merge.md](r3-provider-refactor-merge.md)                                                                                   | R3 × Provider 重构合并记录（2026-09-07）：说明文档。                                       |
| [r3-remote-automation-live-run-2026-09-08.md](r3-remote-automation-live-run-2026-09-08.md)                                                       | R3 首批实际验证记录（2026-09-08）：说明文档。                                              |
| [r3-remote-automation-readiness-2026-09-07.md](r3-remote-automation-readiness-2026-09-07.md)                                                     | R3 远程自动化材料与准备记录（2026-09-07）：说明文档。                                      |
| [r3-remote-environment-readiness-2026-09-08.md](r3-remote-environment-readiness-2026-09-08.md)                                                   | R3 远程测试环境验证（2026-09-08）：说明文档。                                              |
| [r3-remote-full-validation-2026-09-08.md](r3-remote-full-validation-2026-09-08.md)                                                               | R3 92项完整实际验证执行记录：说明文档。                                                    |
| [r3-remote-ui-implementation.md](r3-remote-ui-implementation.md)                                                                                 | R3 远程 UI 实施记录：说明文档。                                                            |
| [r3-remote-ui-prototype-gap-audit-review.md](r3-remote-ui-prototype-gap-audit-review.md)                                                         | R3 远程 UI 原型差异修复文档审核记录：说明文档。                                            |
| [r3-remote-ui-prototype-gap-audit.md](r3-remote-ui-prototype-gap-audit.md)                                                                       | R3 远程 UI 原型还原度全量差异审查（2026-08-22）：说明文档。                                |
| [r3-source-server-expanded-live-test-record-2026-08-21.md](r3-source-server-expanded-live-test-record-2026-08-21.md)                             | R3 Source Server 扩展实机测试记录（2026-08-21）：说明文档。                                |
| [r3-source-server-release-test-plan.md](r3-source-server-release-test-plan.md)                                                                   | R3 Source Server 发布测试方案：说明文档。                                                  |
| [r3-source-server-remote-completion-plan.md](r3-source-server-remote-completion-plan.md)                                                         | R3 Source Server 收尾工作计划：说明文档。                                                  |
| [r3-source-server-remote-completion-review.md](r3-source-server-remote-completion-review.md)                                                     | R3 收尾实现审查报告（提交 1193e16ee4..d5fdd719da）：说明文档。                             |
| [r3-source-server-remote-impact-brief.md](r3-source-server-remote-impact-brief.md)                                                               | R3 Source Server 远程主链 Impact Brief：说明文档。                                         |
| [r3-source-server-remote-implementation-review.md](r3-source-server-remote-implementation-review.md)                                             | R3 实现审查报告（commit e3896b60e4）：说明文档。                                           |
| [r3-source-server-ssh-live-test-record-2026-08-20.md](r3-source-server-ssh-live-test-record-2026-08-20.md)                                       | R3 Source Server SSH 实机测试记录（2026-08-20）：说明文档。                                |
| [README.md](README.md)                                                                                                                           | 本目录用途、子目录与逐文件说明。                                                           |
| [remote-domain-simplification-and-conversation-workspace-spec-review.md](remote-domain-simplification-and-conversation-workspace-spec-review.md) | Review：Remote Domain Simplification and Non-Project Conversation 规格审查报告：说明文档。 |
| [ssh-project-entry-helper.md](ssh-project-entry-helper.md)                                                                                       | SSH 项目入口的 E2E 编排：说明文档。                                                        |

<!-- qingqi-directory-index:end -->
