# test

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

test 测试场景，属于 scripts 目录。

### 文件

| 文件                                                                                                               | 简要说明                                                                                        |
| ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| [affected-engineering-test-cli.test.mjs](affected-engineering-test-cli.test.mjs)                                   | 外层 hook 的 SHA 和 Git local env 不属于夹具，必须用环境副本隔离。                              |
| [architecture-default-branch.test.mjs](architecture-default-branch.test.mjs)                                       | architecture-default-branch.test 的实现文件。                                                   |
| [architecture-governance-review.test.mjs](architecture-governance-review.test.mjs)                                 | 2026-09 review 补测：以下场景在首版检查器上全部"0 违规"通过，属于门禁失明。                     |
| [architecture-governance.test.mjs](architecture-governance.test.mjs)                                               | Windows 上 git 子进程与索引句柄会短暂滞留，直接 rm(recursive) 偶发                              |
| [architecture-upstream-admission.test.mjs](architecture-upstream-admission.test.mjs)                               | 实现或公开接口：value。                                                                         |
| [arms-patch-install-contract.test.mjs](arms-patch-install-contract.test.mjs)                                       | Bugfix：旧 patch 分次追加 hunk 后仍保留旧目标 hash，pnpm hoisted 第二次安装会误判并重复打补丁。 |
| [bootstrap-patched-dependencies.test.mjs](bootstrap-patched-dependencies.test.mjs)                                 | bootstrap-patched-dependencies.test 的实现文件。                                                |
| [build-time-config.test.mjs](build-time-config.test.mjs)                                                           | build-time-config.test 的实现文件。                                                             |
| [cli-lint-admission.test.mjs](cli-lint-admission.test.mjs)                                                         | cli-lint-admission.test 的实现文件。                                                            |
| [cli-release.test.mjs](cli-release.test.mjs)                                                                       | cli-release.test 的实现文件。                                                                   |
| [cli-test-environment.test.mjs](cli-test-environment.test.mjs)                                                     | cli-test-environment.test 的实现文件。                                                          |
| [conversation-session-formal-admission-audit.test.mjs](conversation-session-formal-admission-audit.test.mjs)       | conversation-session-formal-admission-audit.test 的实现文件。                                   |
| [conversation-session-formal-admission-review-2.test.mjs](conversation-session-formal-admission-review-2.test.mjs) | 准入新增身份校验后，合法夹具也须携带归属，避免无关拒绝掩盖本场景断言。                          |
| [conversation-session-formal-admission-review.test.mjs](conversation-session-formal-admission-review.test.mjs)     | 准入新增身份校验后，合法夹具也须携带归属，避免无关拒绝掩盖本场景断言。                          |
| [conversation-session-formal-admission.test.mjs](conversation-session-formal-admission.test.mjs)                   | conversation-session-formal-admission.test 的实现文件。                                         |
| [e2e-remote-targets-check.test.mjs](e2e-remote-targets-check.test.mjs)                                             | e2e-remote-targets-check.test 的实现文件。                                                      |
| [installer-process-helper.test.mjs](installer-process-helper.test.mjs)                                             | helper 可以先终止目标；随后关闭 stdin 时的 EPIPE 不能成为未处理异常。                           |
| [license-identifiers.test.mjs](license-identifiers.test.mjs)                                                       | license-identifiers.test 的实现文件。                                                           |
| [marketing-executable-lines.test.mjs](marketing-executable-lines.test.mjs)                                         | 实现或公开接口：f、x、view。                                                                    |
| [marketing-source-map-evidence.test.mjs](marketing-source-map-evidence.test.mjs)                                   | marketing-source-map-evidence.test 的实现文件。                                                 |
| [marketing-touch-coverage-audit.test.mjs](marketing-touch-coverage-audit.test.mjs)                                 | marketing-touch-coverage-audit.test 的实现文件。                                                |
| [pre-push-worktree.test.mjs](pre-push-worktree.test.mjs)                                                           | 附注标签的对象 SHA 与 commit 不同；发布工具同时推送分支和标签时必须按目标 commit 校验。         |
| [react-hooks-lint.test.mjs](react-hooks-lint.test.mjs)                                                             | 实现或公开接口：useMissing、useExtra、Example、usePrecise。                                     |
| [README.md](README.md)                                                                                             | 本目录用途、子目录与逐文件说明。                                                                |
| [retired-app-unit-evidence.test.mjs](retired-app-unit-evidence.test.mjs)                                           | retired-app-unit-evidence.test 的实现文件。                                                     |
| [session-control-boundary.test.mjs](session-control-boundary.test.mjs)                                             | 实现或公开接口：result、load。                                                                  |
| [source-size-policy.test.mjs](source-size-policy.test.mjs)                                                         | 只验证规则本身；根 runner 排除 CLI，由独立 CLI runner 检查。                                    |
| [sqlite-schema-contract.test.mjs](sqlite-schema-contract.test.mjs)                                                 | sqlite-schema-contract.test 的实现文件。                                                        |
| [third-party-npm-platform.test.mjs](third-party-npm-platform.test.mjs)                                             | 评审 CR-03 回归：Windows autocrlf 工作区根 lockfile 为 CRLF、安装快照为 LF，                    |
| [verify-electron-builder-binaries-mirror.test.mjs](verify-electron-builder-binaries-mirror.test.mjs)               | 停滞注入用例会留下未完成连接；close 前强制断开，避免等待残留套接字。                            |
| [windows-runtime-host-build.test.mjs](windows-runtime-host-build.test.mjs)                                         | windows-runtime-host-build.test 的实现文件。                                                    |

<!-- qingqi-directory-index:end -->
