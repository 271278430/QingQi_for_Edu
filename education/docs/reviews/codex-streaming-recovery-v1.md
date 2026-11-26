# 流式教学与截断恢复审查 · 2026-11-25

本次截图对应正式run31：“连上这根线是否有帮助”。图片已上传，visual_context指向同会话接受图，失败发生在模型结束：89.5秒、4096个输出token全部用于推理、正文0、finish_reason=length。run30虽然成功，也等了83.4秒才出现正文。这两个样本说明问题发生在推理配置与响应链路，不是图片上传失败。

已下载openai/codex并核对提交`c265acf3b138a12629b6f344bd08ee1f2c28c934`。本轮参考的是开源引擎的流事件与协议设计，采用现有Python/TypeScript服务及ZCode工具运行时适配，不宣称复制Codex桌面界面的私有实现：

- [responses.rs](https://github.com/openai/codex/blob/c265acf3b138a12629b6f344bd08ee1f2c28c934/codex-rs/codex-api/src/sse/responses.rs)：`response.output_text.delta`即时转换文字事件，`completed/incomplete/failed`独立处理。
- [responses_error.rs](https://github.com/openai/codex/blob/c265acf3b138a12629b6f344bd08ee1f2c28c934/codex-rs/codex-api/src/sse/responses_error.rs)：错误根据终止原因和重试建议分类。
- [protocol.rs](https://github.com/openai/codex/blob/c265acf3b138a12629b6f344bd08ee1f2c28c934/codex-rs/protocol/src/protocol.rs)：消息增量、轮次开始和完成是不同协议事件。

实际修复分为四层。ModelSettings重建Endpoint时保留部署reasoning_effort，修复自定义模型分工丢失low的问题；官方GLM-5.3没有显式档位时采用受支持low，显式high/max不覆盖，模型型号、保存配置和输出预算不改。GLM-5.3不支持关闭思考，本轮没有发送thinking.disabled。

模型流适配支持CRLF、多行data与UTF8拆块。正文delta不等整句或公式闭合，草稿只执行可判定的禁止输出/错误归因检查，完整性、数学与工具许可仍在最终接受前检查。推理内容仅触发通用进度，不显示推理原文；工具参数必须完整组装和授权后才能执行。MathContent显式传入原ZCode MessageResponse.streaming，完成的历史使用静态模式。

length的自然文字输出独立归类model_truncated；结构化参数截断仍为协议失败。失败时checkpoint保留未接受partial_text，Web只读显示partial_response并标“未完成”，response仍为null；不计成绩、掌握或已接受导师事实。错误后主动读取同会话Store快照，避免上一轮回答看起来像本次回复。刷新后的旧标注截断也通过只读分类提供“重新回答”；用户明确点击后使用新编号、保留原问题、图片和visual_context。原失败账本不修改。网络未知结果不静默重新调用。

连续流式回复已经通过教学/数学校验时，轻微长度超目标不会再额外整轮润色并清空已显示文字。较早回放353字超过340字软预算时曾因此追加一次6.7秒的调用；本轮通过提供方调用计数验证这种长度问题只有一次模型调用。必要的语义、条件、答案许可和过多追问修复保留。字数目标继续用于提示与质量记录，不截断公式或条件。

内容复核还发现模型把新增红色EF误称为已有CD。现在给视觉教师提供原图点名/连线拓扑，要求先辨认新增颜色线；本问已核验角度从既有solve_geometry记录读取，不重复执行求解。只在中点问使用中点角度，不凭外观把全等三角形称作直角三角形，也不把学生标注当成核验结论。

最新真实回放使用原失败问句与原标注图片，隔离root重建接受来源，经过同类自定义视觉角色适配。首段正文3.6秒、7.5秒完成、131次提供方增量、1次视觉调用；提供方报告46个推理token。已人工核对新增线为EF，回复讨论EF和原图CD的关系，并保留学生推理任务。这个样本证明本场景能够流式完成，不是总体P95、任意题型准确率或学习效果统计。较早13秒、19秒及错误指代的回放不冒充最终成功样本。

验收证据：51组全量清单通过；末次源图绑定/流式恢复增量复测包括14项CLI、4组浏览器和既有17项标注CLI、8组标注浏览器。浏览器验证无标点片段在请求仍打开时可见、真实CRLF流、未完成文字刷新恢复、明确重新回答的新编号与相同标注引用、低推理参数与单次提供方调用。根typecheck、Web/runtime构建、架构检查通过；40文件Hooks专项0诊断，root lint532告警0错误。正式两入口只读页面验收另行记录；真实模型测试只写隔离root，正式run数保持31、活动lease为0。

流程与边界见[规格](../../../specs/education/codex-streaming-recovery-v1.md)。入口：[Flash教学](http://127.0.0.1:18774/) · [完整模型配置](http://127.0.0.1:18772/)。刷新页面后，可在旧失败消息处点击“重新回答”，继续讨论已保存的标注。
