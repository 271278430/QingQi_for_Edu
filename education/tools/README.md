# tools

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

启动、账户配置、数据导入、素材制作与维护工具。验收及模型夹具位于 education/tests。

### 文件

| 文件                                                       | 简要说明                                            |
| ---------------------------------------------------------- | --------------------------------------------------- |
| [capture_product_media.mjs](capture_product_media.mjs)     | 采集产品截图与真实教学动画关键帧。                  |
| [check_project_management.py](check_project_management.py) | 只读检查数据覆盖、版本管理与正式入口。              |
| [cleanup-project.ps1](cleanup-project.ps1)                 | 列出并归档可重建产物，验证路径边界。                |
| [clear_product_history.py](clear_product_history.py)       | 需要显式执行参数的项目历史清理命令。                |
| [demo.py](demo.py)                                         | 生成自编题目和合成学生，启动独立演示。              |
| [demo_media_fixture.py](demo_media_fixture.py)             | 为公开截图启动隔离的合成学生服务。                  |
| [directory_docs.py](directory_docs.py)                     | 生成、更新并检查全仓库的 README 目录与文件索引。    |
| [import_student_data.py](import_student_data.py)           | 显式导入教材、题库、画像和会话资料。                |
| [open-workspace.ps1](open-workspace.ps1)                   | Windows 工作台启动与 PID 归属管理。                 |
| [probe_glm.py](probe_glm.py)                               | 显式连接 GLM 接口的诊断探针。                       |
| [probe_specialists.py](probe_specialists.py)               | 专项模型服务的诊断探针。                            |
| [project_integrity.py](project_integrity.py)               | 只读比较配置、索引和正式状态的保护指纹。            |
| [provision.py](provision.py)                               | 交互式建立本机账户，保存密码哈希。                  |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                    |
| [review_all.mjs](review_all.mjs)                           | 按当前清单运行 education/tests 下的验收并汇总报告。 |
| [review_manifest.json](review_manifest.json)               | 当前自动验收场景的文件名与业务范围。                |
| [run_models.py](run_models.py)                             | 完整模型模式的连接、专项服务和 HTTP 启动。          |
| [start.mjs](start.mjs)                                     | 统一 pnpm 启动入口，选择演示或本机模型配置。        |
| [stop-workspace.ps1](stop-workspace.ps1)                   | 按仓库、入口和 PID 安全停止服务。                   |

<!-- qingqi-directory-index:end -->
