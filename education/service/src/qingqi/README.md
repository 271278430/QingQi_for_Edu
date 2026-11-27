# qingqi

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

教学业务的实现：会话原题、意图与教学策略、工具、模型、学习证据和唯一 Store。

### 文件

| 文件                                                 | 简要说明                                                                  |
| ---------------------------------------------------- | ------------------------------------------------------------------------- |
| [\_\_init\_\_.py](__init__.py)                       | 教学业务包的入口标识。                                                    |
| [adaptive_learning.py](adaptive_learning.py)         | 依据学情规划重点并选择多样化三题。                                        |
| [advanced_visuals.py](advanced_visuals.py)           | 教学图的几何与数值编译。                                                  |
| [agent.py](agent.py)                                 | Agent Loop 主流程：接收所属题目，执行受控动作，核验候选回复并提交 Store。 |
| [animation_teaching.py](animation_teaching.py)       | 可信动画模板与参数编译。                                                  |
| [architecture_bindings.py](architecture_bindings.py) | 校验架构目录中的源码文件与入口符号。                                      |
| [architecture_catalog.py](architecture_catalog.py)   | 系统模块的只读目录与版本。                                                |
| [architecture_details.py](architecture_details.py)   | 16 个模块的输入、职责、输出和源码说明。                                   |
| [architecture_panorama.py](architecture_panorama.py) | 单张系统关系图与 Agent Loop 的节点、边和布局。                            |
| [architecture_steps.py](architecture_steps.py)       | 各模块的具体处理步骤说明。                                                |
| [catalogue.py](catalogue.py)                         | 只读题库入口、完整性检查和题目版本。                                      |
| [catalogue_variants.py](catalogue_variants.py)       | 保留来源标记的确定性数值变式题。                                          |
| [chat_models.py](chat_models.py)                     | 会话选型与发送时冻结的模型配置。                                          |
| [context.py](context.py)                             | 构造单轮上下文，组织请求、历史、观察和有界记忆。                          |
| [contracts.py](contracts.py)                         | 请求、回复、工具参数与错误的类型和运行时校验。                            |
| [conversation.py](conversation.py)                   | 恢复同一会话的原题，区分续问与新题。                                      |
| [domain_tools.py](domain_tools.py)                   | 数学计算、课程导航和审查所需的领域工具。                                  |
| [function_reasoning.py](function_reasoning.py)       | 绑定原题的函数曲线、零点、驻点和区间推理场景。                            |
| [function_solver.py](function_solver.py)             | 受支持函数题的精确符号求解。                                              |
| [geometry_animation.py](geometry_animation.py)       | 保持原题约束的连续几何动画坐标。                                          |
| [geometry_lessons.py](geometry_lessons.py)           | 几何构造对应的分步教学模板。                                              |
| [geometry_solver.py](geometry_solver.py)             | 声明几何构造的精确符号核验。                                              |
| [geometry_tasks.py](geometry_tasks.py)               | 识别题目明确给出的几何条件和构造任务。                                    |
| [geometry_tutor.py](geometry_tutor.py)               | 根据已核验几何事实组织教学。                                              |
| [graph.py](graph.py)                                 | 课程图谱的只读查询、关系与来源依据。                                      |
| [identity_animation.py](identity_animation.py)       | 恒等式的系数比较与参数教学动画。                                          |
| [layered_routing.py](layered_routing.py)             | 按问题和上下文选择任务路由，保留可审查的本地分类依据。                    |
| [learning.py](learning.py)                           | 学习快照、种子课程和学生可见题目投影。                                    |
| [learning_branches.py](learning_branches.py)         | 结合先修、学习时间和题库供给规划可选路线。                                |
| [learning_evidence.py](learning_evidence.py)         | 从实际学习事件派生掌握度、保持与复习证据。                                |
| [learning_map.py](learning_map.py)                   | 学情知识图谱的节点、边和来源投影。                                        |
| [management.py](management.py)                       | 系统设置、管理权限和版本化维护命令。                                      |
| [math_display.py](math_display.py)                   | 把计算结果表示为分数、根式或其他精确标签。                                |
| [mcp.py](mcp.py)                                     | 有边界的本地 MCP stdio 连接、发现和调用。                                 |
| [model_options.py](model_options.py)                 | 推理档位等参数到 ZCode CEL 参数映射的桥接。                               |
| [model_protocol.py](model_protocol.py)               | OpenAI 兼容和 Anthropic 的请求、授权与响应适配。                          |
| [model_settings.py](model_settings.py)               | 供应商连接、模型角色与版本化配置的 Store 接口。                           |
| [model_stream.py](model_stream.py)                   | 解析模型 SSE 增量及工具调用片段。                                         |
| [nonnegative_reasoning.py](nonnegative_reasoning.py) | 非负关系、反例、方程操作与代入的精确推理场景。                            |
| [nonnegative_teaching.py](nonnegative_teaching.py)   | 非负表达式的受控情景教学。                                                |
| [planning.py](planning.py)                           | 教学动作与工具阶段规划，组织候选回复和下一步执行。                        |
| [practice_tutoring.py](practice_tutoring.py)         | 绑定原题的提示、步骤核对与精确线性关系。                                  |
| [presentation.py](presentation.py)                   | 图示、动画、情景故事等呈现偏好，与教学方式分别处理。                      |
| [product.py](product.py)                             | HTTP/SSE 服务入口，完成身份、CSRF、资源归属和请求准入。                   |
| [projection.py](projection.py)                       | 学生可见回复，隐藏内部诊断和工具账本。                                    |
| [provider_models.py](provider_models.py)             | 模型连接和具体型号的无密钥展示投影。                                      |
| [providers.py](providers.py)                         | 文本、视觉与专项模型客户端及本轮教学推理。                                |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                          |
| [request_controls.py](request_controls.py)           | 解析学生对答案、追问和图示形式的明确要求。                                |
| [routing.py](routing.py)                             | 任务意图类别和基础路由契约。                                              |
| [secret_store.py](secret_store.py)                   | 在本机加密保存 API 密钥。                                                 |
| [skills.py](skills.py)                               | 教学 Skill 清单、指导内容与能力范围加载。                                 |
| [storage.py](storage.py)                             | 唯一可写状态所有者：会话、学习事件、模型配置、租约、幂等账本和提交事务。  |
| [student_task_tools.py](student_task_tools.py)       | 推荐练习、学习路线预览和学情读取的同学生工具端口。                        |
| [student_tasks.py](student_tasks.py)                 | 当前输入的任务识别、资料引用、查询 Controller 与任务产物校验。            |
| [teaching_goals.py](teaching_goals.py)               | 识别学生当前需要概念解释、步骤帮助、核对或其他教学目标。                  |
| [teaching_plan.py](teaching_plan.py)                 | 控制本轮教学目标、正文长度、追问数量、答案许可和可视化输出。              |
| [teaching_policy.py](teaching_policy.py)             | 根据会话、难度与学情选择提示、追问、讲解或解答方式。                      |
| [teaching_responses.py](teaching_responses.py)       | 构造教学文字、计算步骤和基础教学回复。                                    |
| [teaching_visual_pair.py](teaching_visual_pair.py)   | 每轮选择一张图或一段动画。                                                |
| [tools.py](tools.py)                                 | 教育工具注册与受控调用契约。                                              |
| [turn_control.py](turn_control.py)                   | Store停止命令、临时取消作用域及本轮HTTP连接中断。                         |
| [tutor_images.py](tutor_images.py)                   | 上传图片的格式、尺寸和数量校验。                                          |
| [tutoring_grounding.py](tutoring_grounding.py)       | 区分学生作答与教师解释，阻止虚构学生已完成的步骤。                        |
| [tutoring_scope.py](tutoring_scope.py)               | 多问题的当前小问、各问意图和答案披露范围。                                |
| [visual_expressions.py](visual_expressions.py)       | 有限范围的多项式与函数表达式解析。                                        |
| [visual_tasks.py](visual_tasks.py)                   | 选择当前问题所需的图示任务。                                              |
| [visual_teaching.py](visual_teaching.py)             | 生成绑定原题的确定性教学图。                                              |
| [web_store.py](web_store.py)                         | Web 会话列表与恢复投影，不保存第二份学习状态。                            |
| [workers.py](workers.py)                             | 课程、困难分析和审查专项模型的输入输出适配。                              |
| [zcode_runtime.py](zcode_runtime.py)                 | Python 到 ZCode Node 运行层的受控桥接。                                   |

<!-- qingqi-directory-index:end -->
