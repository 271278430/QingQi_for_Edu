# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

教学产品验收、浏览器场景、模型夹具和真实服务探针；当前自动清单由 tools/review_manifest.json 管理。

### 文件

| 文件                                                                                   | 简要说明                                                     |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [acceptance.py](acceptance.py)                                                         | 验收与检查：Agent 请求、权限、工具和提交边界。               |
| [adaptive_learning_acceptance.py](adaptive_learning_acceptance.py)                     | 验收与检查：动态学情、学习路径与多样化三题。                 |
| [architecture_browser.mjs](architecture_browser.mjs)                                   | 浏览器交互验收：系统关系图、真实循环和模块职责。             |
| [architecture_geometry.mjs](architecture_geometry.mjs)                                 | 验收与检查：系统关系图、真实循环和模块职责。                 |
| [browser_acceptance.mjs](browser_acceptance.mjs)                                       | 浏览器交互验收：Agent 请求、权限、工具和提交边界。           |
| [browser_recovery_acceptance.mjs](browser_recovery_acceptance.mjs)                     | 浏览器交互验收：超时、错误与浏览器恢复。                     |
| [browser_recovery_server.py](browser_recovery_server.py)                               | 可控服务或样例数据：超时、错误与浏览器恢复。                 |
| [codex_stream_acceptance.py](codex_stream_acceptance.py)                               | 验收与检查：增量文字、错误终态与恢复。                       |
| [codex_stream_browser.mjs](codex_stream_browser.mjs)                                   | 浏览器交互验收：增量文字、错误终态与恢复。                   |
| [codex_stream_fixture.py](codex_stream_fixture.py)                                     | 可控服务或样例数据：增量文字、错误终态与恢复。               |
| [codex_stream_live.py](codex_stream_live.py)                                           | 真实服务探针：增量文字、错误终态与恢复。                     |
| [combined_presentation_acceptance.py](combined_presentation_acceptance.py)             | 验收与检查：图示、动画与故事的组合请求。                     |
| [combined_presentation_browser.mjs](combined_presentation_browser.mjs)                 | 浏览器交互验收：图示、动画与故事的组合请求。                 |
| [combined_presentation_live.py](combined_presentation_live.py)                         | 真实服务探针：图示、动画与故事的组合请求。                   |
| [composer_models_acceptance.py](composer_models_acceptance.py)                         | 验收与检查：对话选模、推理档位与发送快照。                   |
| [composer_models_browser.mjs](composer_models_browser.mjs)                             | 浏览器交互验收：对话选模、推理档位与发送快照。               |
| [composer_models_fixture.py](composer_models_fixture.py)                               | 可控服务或样例数据：对话选模、推理档位与发送快照。           |
| [composer_models_live.py](composer_models_live.py)                                     | 真实服务探针：对话选模、推理档位与发送快照。                 |
| [concept_definition_acceptance.py](concept_definition_acceptance.py)                   | 验收与检查：概念解释与引导。                                 |
| [contextual_teaching_acceptance.py](contextual_teaching_acceptance.py)                 | 验收与检查：上下文教学方式与单个可视化输出。                 |
| [contextual_teaching_browser.mjs](contextual_teaching_browser.mjs)                     | 浏览器交互验收：上下文教学方式与单个可视化输出。             |
| [contextual_teaching_live.py](contextual_teaching_live.py)                             | 真实服务探针：上下文教学方式与单个可视化输出。               |
| [conversation_function_acceptance.py](conversation_function_acceptance.py)             | 验收与检查：同题函数辅导。                                   |
| [conversation_problem_acceptance.py](conversation_problem_acceptance.py)               | 验收与检查：同题上下文与多问续聊。                           |
| [conversation_problem_browser.mjs](conversation_problem_browser.mjs)                   | 浏览器交互验收：同题上下文与多问续聊。                       |
| [conversation_problem_fixture.py](conversation_problem_fixture.py)                     | 可控服务或样例数据：同题上下文与多问续聊。                   |
| [conversation_problem_live.py](conversation_problem_live.py)                           | 真实服务探针：同题上下文与多问续聊。                         |
| [course_model_acceptance.py](course_model_acceptance.py)                               | 验收与检查：模型调用与结果边界。                             |
| [current_task_acceptance.py](current_task_acceptance.py)                               | 验收与检查：本轮任务优先、多图查询、推荐与同题续聊。         |
| [current_task_browser.mjs](current_task_browser.mjs)                                   | 浏览器交互验收：本轮任务优先、多图查询、推荐与同题续聊。     |
| [current_task_browser_server.py](current_task_browser_server.py)                       | 可控服务或样例数据：本轮任务优先、多图查询、推荐与同题续聊。 |
| [current_task_images_acceptance.py](current_task_images_acceptance.py)                 | 验收与检查：本轮任务优先、多图查询、推荐与同题续聊。         |
| [demo_acceptance.py](demo_acceptance.py)                                               | 验收与检查：Agent 请求、权限、工具和提交边界。               |
| [four_feature_acceptance.py](four_feature_acceptance.py)                               | 验收与检查：四项学生功能。                                   |
| [four_feature_browser.mjs](four_feature_browser.mjs)                                   | 浏览器交互验收：四项学生功能。                               |
| [four_feature_server.py](four_feature_server.py)                                       | 可控服务或样例数据：四项学生功能。                           |
| [geometry_browser_acceptance.mjs](geometry_browser_acceptance.mjs)                     | 浏览器交互验收：Agent 请求、权限、工具和提交边界。           |
| [geometry_fixture_data.py](geometry_fixture_data.py)                                   | 可控服务或样例数据：几何条件、构造与核验。                   |
| [geometry_grounding_acceptance.py](geometry_grounding_acceptance.py)                   | 验收与检查：Agent 请求、权限、工具和提交边界。               |
| [geometry_live_acceptance.py](geometry_live_acceptance.py)                             | 真实服务探针：Agent 请求、权限、工具和提交边界。             |
| [geometry_product_acceptance.py](geometry_product_acceptance.py)                       | 验收与检查：Agent 请求、权限、工具和提交边界。               |
| [geometry_product_fixture.py](geometry_product_fixture.py)                             | 可控服务或样例数据：几何条件、构造与核验。                   |
| [grounded_hint_acceptance.py](grounded_hint_acceptance.py)                             | 验收与检查：原题提示与学生进度归因。                         |
| [grounded_hint_browser.mjs](grounded_hint_browser.mjs)                                 | 浏览器交互验收：原题提示与学生进度归因。                     |
| [grounded_hint_browser_server.py](grounded_hint_browser_server.py)                     | 可控服务或样例数据：原题提示与学生进度归因。                 |
| [grounded_hint_live.py](grounded_hint_live.py)                                         | 真实服务探针：原题提示与学生进度归因。                       |
| [history_clear_acceptance.py](history_clear_acceptance.py)                             | 验收与检查：历史清理、版本和幂等回执。                       |
| [history_tutor_acceptance.py](history_tutor_acceptance.py)                             | 验收与检查：历史题选择与连续辅导。                           |
| [history_tutor_browser.mjs](history_tutor_browser.mjs)                                 | 浏览器交互验收：历史题选择与连续辅导。                       |
| [history_tutor_browser_server.py](history_tutor_browser_server.py)                     | 可控服务或样例数据：历史题选择与连续辅导。                   |
| [history_tutor_live_acceptance.py](history_tutor_live_acceptance.py)                   | 真实服务探针：历史题选择与连续辅导。                         |
| [identity_animation_acceptance.py](identity_animation_acceptance.py)                   | 验收与检查：恒等式动画与答案许可。                           |
| [identity_animation_browser.mjs](identity_animation_browser.mjs)                       | 浏览器交互验收：恒等式动画与答案许可。                       |
| [identity_animation_browser_server.py](identity_animation_browser_server.py)           | 可控服务或样例数据：恒等式动画与答案许可。                   |
| [identity_animation_live.py](identity_animation_live.py)                               | 真实服务探针：恒等式动画与答案许可。                         |
| [image_repair_live_acceptance.py](image_repair_live_acceptance.py)                     | 真实服务探针：Agent 请求、权限、工具和提交边界。             |
| [interaction_inventory_browser.mjs](interaction_inventory_browser.mjs)                 | 浏览器交互验收：页面全部操作入口。                           |
| [launcher_acceptance.py](launcher_acceptance.py)                                       | 验收与检查：Agent 请求、权限、工具和提交边界。               |
| [learning_evidence_acceptance.py](learning_evidence_acceptance.py)                     | 验收与检查：独立作答、保持与复习依据。                       |
| [learning_tutor_acceptance.py](learning_tutor_acceptance.py)                           | 验收与检查：练习与同题辅导的连续性。                         |
| [learning_tutor_live_acceptance.py](learning_tutor_live_acceptance.py)                 | 真实服务探针：练习与同题辅导的连续性。                       |
| [model_acceptance.py](model_acceptance.py)                                             | 验收与检查：模型调用与结果边界。                             |
| [model_settings_acceptance.py](model_settings_acceptance.py)                           | 验收与检查：模型连接、加密凭据与角色配置。                   |
| [model_settings_browser.mjs](model_settings_browser.mjs)                               | 浏览器交互验收：模型连接、加密凭据与角色配置。               |
| [model_settings_edge_acceptance.py](model_settings_edge_acceptance.py)                 | 验收与检查：模型连接、加密凭据与角色配置。                   |
| [model_settings_fixture.py](model_settings_fixture.py)                                 | 可控服务或样例数据：模型连接、加密凭据与角色配置。           |
| [model_settings_live.py](model_settings_live.py)                                       | 真实服务探针：模型连接、加密凭据与角色配置。                 |
| [model_stream_budget_acceptance.py](model_stream_budget_acceptance.py)                 | 验收与检查：模型流式与生成预算。                             |
| [multimodal_acceptance.py](multimodal_acceptance.py)                                   | 验收与检查：Agent 请求、权限、工具和提交边界。               |
| [multimodal_browser.mjs](multimodal_browser.mjs)                                       | 浏览器交互验收：多图上传、识读与消息附件。                   |
| [multimodal_browser_server.py](multimodal_browser_server.py)                           | 可控服务或样例数据：多图上传、识读与消息附件。               |
| [multimodal_fixture.py](multimodal_fixture.py)                                         | 可控服务或样例数据：多图上传、识读与消息附件。               |
| [precise_math_acceptance.py](precise_math_acceptance.py)                               | 验收与检查：分数、根式和精确数值展示。                       |
| [problem_reasoning_acceptance.py](problem_reasoning_acceptance.py)                     | 验收与检查：函数与几何的解题步骤图示。                       |
| [problem_reasoning_browser.mjs](problem_reasoning_browser.mjs)                         | 浏览器交互验收：函数与几何的解题步骤图示。                   |
| [product_deployment_browser.mjs](product_deployment_browser.mjs)                       | 浏览器交互验收：已部署入口、四页面和管理界面。               |
| [product_usability_acceptance.py](product_usability_acceptance.py)                     | 验收与检查：学生操作、原题绑定与错误状态。                   |
| [product_usability_browser.mjs](product_usability_browser.mjs)                         | 浏览器交互验收：学生操作、原题绑定与错误状态。               |
| [product_usability_server.py](product_usability_server.py)                             | 可控服务或样例数据：学生操作、原题绑定与错误状态。           |
| [provider_protocol_acceptance.py](provider_protocol_acceptance.py)                     | 验收与检查：模型协议适配。                                   |
| [read_teach_response.mjs](read_teach_response.mjs)                                     | 验收与检查：教学响应读取。                                   |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                             |
| [release_hint_live.py](release_hint_live.py)                                           | 真实服务探针：release hint live。                            |
| [route_quality_acceptance.py](route_quality_acceptance.py)                             | 验收与检查：任务路由与教学策略。                             |
| [runtime_bounds_acceptance.py](runtime_bounds_acceptance.py)                           | RPC绝对截止时间、重复回调和有界清理验收。                    |
| [runtime_build_acceptance.mjs](runtime_build_acceptance.mjs)                           | 验收与检查：Node 运行层构建与原子发布。                      |
| [runtime_reuse_acceptance.py](runtime_reuse_acceptance.py)                             | 验收与检查：ZCode 工具、MCP、Skills、记忆和子任务。          |
| [save_full_diagram.mjs](save_full_diagram.mjs)                                         | 验收与检查：完整 SVG 导出。                                  |
| [scoped_stream_acceptance.py](scoped_stream_acceptance.py)                             | 验收与检查：小问范围与流式输出。                             |
| [scoped_stream_browser.mjs](scoped_stream_browser.mjs)                                 | 浏览器交互验收：小问范围与流式输出。                         |
| [scoped_stream_live.py](scoped_stream_live.py)                                         | 真实服务探针：小问范围与流式输出。                           |
| [solid_web_browser.mjs](solid_web_browser.mjs)                                         | 浏览器交互验收：页面布局、设置生命周期与手机导航。           |
| [source_reuse_acceptance.mjs](source_reuse_acceptance.mjs)                             | 验收与检查：ZCode UI 与浏览器基础。                          |
| [source_reuse_server.py](source_reuse_server.py)                                       | 可控服务或样例数据：ZCode UI 与浏览器基础。                  |
| [story_context_acceptance.py](story_context_acceptance.py)                             | 验收与检查：情景故事与原题条件。                             |
| [story_context_live.py](story_context_live.py)                                         | 真实服务探针：情景故事与原题条件。                           |
| [student_data_acceptance.py](student_data_acceptance.py)                               | 验收与检查：教材、题库、画像与学情页面。                     |
| [student_data_browser.mjs](student_data_browser.mjs)                                   | 浏览器交互验收：教材、题库、画像与学情页面。                 |
| [student_data_server.py](student_data_server.py)                                       | 可控服务或样例数据：教材、题库、画像与学情页面。             |
| [system_management_acceptance.py](system_management_acceptance.py)                     | 验收与检查：系统设置与管理权限。                             |
| [system_review.py](system_review.py)                                                   | 验收与检查：路由、核验与错误场景。                           |
| [system_review_browser.mjs](system_review_browser.mjs)                                 | 浏览器交互验收：路由、核验与错误场景。                       |
| [system_review_cases.json](system_review_cases.json)                                   | 可控服务或样例数据：路由、核验与错误场景。                   |
| [turn_stop_acceptance.py](turn_stop_acceptance.py)                                     | 停止、输入归属、提交竞争、帮助曝光和双协议HTTP验收。         |
| [turn_stop_browser.mjs](turn_stop_browser.mjs)                                         | 桌面和手机停止、刷新恢复、双提交与草稿保留的浏览器验收。     |
| [turn_stop_fixture.py](turn_stop_fixture.py)                                           | 观察真实连接断开的本地模型与独立产品夹具。                   |
| [tutoring_evolution_acceptance.py](tutoring_evolution_acceptance.py)                   | 验收与检查：教学方式、追问与步骤演示。                       |
| [tutoring_evolution_browser_acceptance.mjs](tutoring_evolution_browser_acceptance.mjs) | 浏览器交互验收：教学方式、追问与步骤演示。                   |
| [tutoring_evolution_deployment_check.py](tutoring_evolution_deployment_check.py)       | 验收与检查：教学方式、追问与步骤演示。                       |
| [tutoring_evolution_fixture.py](tutoring_evolution_fixture.py)                         | 可控服务或样例数据：教学方式、追问与步骤演示。               |
| [tutoring_evolution_live_acceptance.py](tutoring_evolution_live_acceptance.py)         | 真实服务探针：教学方式、追问与步骤演示。                     |
| [vision_live_acceptance.py](vision_live_acceptance.py)                                 | 真实服务探针：Agent 请求、权限、工具和提交边界。             |
| [vision_protocol_fixture.py](vision_protocol_fixture.py)                               | 可控服务或样例数据：视觉模型协议。                           |
| [vision_schema_acceptance.py](vision_schema_acceptance.py)                             | 验收与检查：视觉模型协议与错误响应。                         |
| [vision_schema_live_acceptance.py](vision_schema_live_acceptance.py)                   | 真实服务探针：视觉模型协议与错误响应。                       |
| [visual_discussion_acceptance.py](visual_discussion_acceptance.py)                     | 验收与检查：图上标注与返图讨论。                             |
| [visual_discussion_browser.mjs](visual_discussion_browser.mjs)                         | 浏览器交互验收：图上标注与返图讨论。                         |
| [visual_discussion_live.py](visual_discussion_live.py)                                 | 真实服务探针：图上标注与返图讨论。                           |
| [visual_tasks_acceptance.py](visual_tasks_acceptance.py)                               | 验收与检查：可视化任务与原题参数。                           |
| [visual_tasks_browser_acceptance.mjs](visual_tasks_browser_acceptance.mjs)             | 浏览器交互验收：可视化任务与原题参数。                       |
| [visual_tasks_fixture.py](visual_tasks_fixture.py)                                     | 可控服务或样例数据：可视化任务与原题参数。                   |
| [visual_tasks_live_acceptance.py](visual_tasks_live_acceptance.py)                     | 真实服务探针：可视化任务与原题参数。                         |
| [visual_teaching_acceptance.py](visual_teaching_acceptance.py)                         | 验收与检查：教学图示与精确坐标。                             |
| [visual_teaching_browser_acceptance.mjs](visual_teaching_browser_acceptance.mjs)       | 浏览器交互验收：教学图示与精确坐标。                         |
| [visual_teaching_fixture.py](visual_teaching_fixture.py)                               | 可控服务或样例数据：教学图示与精确坐标。                     |
| [visual_teaching_http_acceptance.py](visual_teaching_http_acceptance.py)               | 验收与检查：教学图示与精确坐标。                             |
| [visual_teaching_live_acceptance.py](visual_teaching_live_acceptance.py)               | 真实服务探针：教学图示与精确坐标。                           |
| [zcode_model_acceptance.py](zcode_model_acceptance.py)                                 | 验收与检查：模型调用与结果边界。                             |

<!-- qingqi-directory-index:end -->
