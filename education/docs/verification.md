# 验收说明

当前唯一入口是 `education/tools/review_manifest.json`，完整运行 `node education/tools/review_all.mjs`。失败修复后用 `--failed` 重跑失败项与新增项，并合并原报告。

2026-11-26发布检查包含56组当前回归，全部通过。覆盖四功能、同题/小问、模型选择、真实SSE片段、附件/标注、数学精确表达、提示归因与答案保护、工具能力、租约/幂等、历史清理、错误恢复、设置、手机及单张系统关系图。

- 类型、构建、Lint、Hooks和架构边界为工程检查。
- 可控HTTP模型服务用来验证协议、错误和权限，不衡量真实模型的题目正确率。
- 少量真实API探针另行验证文本、图片和流式接入。
- 正式两入口使用只读页面检查；前后核对学习摘要、历史计数、画像与模型配置指纹。
- 公开演示由项目自编数据构建，不依赖学生原始资料。运行 `python education/tests/demo_acceptance.py` 验证启动、图谱、三题、提示、核对和重开保留状态。

需要Node 24、Python 3.12+、已构建Web/runtime；设置QINGQI_PYTHON、QINGQI_NODE和PYTHONPATH=education/service/src。浏览器脚本使用Edge。完整资料相关回归需要先导入自己的数学资料，未配置真实模型时不运行付费探针。

产物：`.local/reports/review-all.local.json`和`full-review/`；详细报告不上传。演示图片位于`docs/media`，由隔离的合成学生生成。

架构验收为 `node education/tests/architecture_browser.mjs`。只保留单张系统关系图，检查实际循环、16模块源码、排版、下载、缩放、详情/Escape、主题和手机。旧的三总图与Mermaid模块图验收已退役。
