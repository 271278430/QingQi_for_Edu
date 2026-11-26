# 仓库目录维护

清启是基于 ZCode 开发的学生端教育 Agent 项目。教育产品在 education；ZCode 基础源码在 apps 和 packages；工程工具、行为规格与第三方资料各自保持独立目录。

education/tools 存放启动、导入、账户配置、维护与素材制作。education/tests 存放教学验收、浏览器场景、可控模型服务和真实服务探针。当前自动验收由 tools/review_manifest.json 选取，tools/review_all.mjs 统一运行。

每个版本化目录的 README 列出直接子目录与直接文件。逐级阅读可覆盖全仓库。原有说明和版权正文保留；带 qingqi-directory-index 标记的部分由生成器维护。

新增、删除或移动文件后，在仓库根目录运行：

```sh
python education/tools/directory_docs.py
python education/tools/directory_docs.py --check
```

生成器以 Git 文件集为范围。文件职责优先来自 directory-descriptions.json 中的明确说明，其次是包信息、模块注释和公开符号。修改核心教育模块时同步维护明确说明。生成器只写 README，不修改源码、许可证或第三方资产。

node_modules、dist、运行目录、密钥、学生数据库、索引和本机报告不进入公开目录说明，也不上传。它们由各模块运行时生成或由部署者配置。

CI 在安装依赖后检查目录说明的覆盖率、文件索引和链接，再构建教学产品并执行公开演示验收。文档更新可以按项目格式工具整理；目录检查允许 Markdown 表格的空格对齐差异。
