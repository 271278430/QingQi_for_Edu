# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

tests 验收与回归场景，属于 education 目录。

### 文件

| 文件                                                     | 简要说明                                                                                                                    |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                                                            |
| [test_agent.py](test_agent.py)                           | 实现或公开接口：root、agent、request、test_real_graph_curriculum_and_source_provenance。                                    |
| [test_api_and_repair.py](test_api_and_repair.py)         | 实现或公开接口：RepairFixture、test_bad_action_schema_is_repaired_and_real_tool_runs、test_resume_refuses_changed_budgets。 |
| [test_provider_transport.py](test_provider_transport.py) | Local HTTP contract fixtures: real transport, no actual model inference.                                                    |
| [test_routing_policy.py](test_routing_policy.py)         | End-to-end routing behavior with independent expectations and real tools.                                                   |
| [test_web.py](test_web.py)                               | Real local web requests over the Agent; no remote model or browser fixture.                                                 |
| [test_worker_contracts.py](test_worker_contracts.py)     | Worker stubs verify contracts only, never model ability.                                                                    |

<!-- qingqi-directory-index:end -->
