# 本机启动与维护

首次克隆可先运行 `pnpm education:build` 和 `pnpm education:demo`。演示无需本机模型配置，使用自编数据与独立的 `service/runs/demo-v1`，不覆盖正式学生目录。配置真实模型或导入资料后再使用下列本机入口。

Windows上的pnpm启动命令复用双击启动器，记录同一launcher PID；启动完成后可关闭命令窗口，停止服务使用对应停止文件。

仓库根目录提供两个独立配置入口，它们共享同一教育产品和学生状态：

| 启动文件           | 停止文件           | 默认访问地址            | 配置                                          |
| ------------------ | ------------------ | ----------------------- | --------------------------------------------- |
| 打开教育工作台.cmd | 停止教育工作台.cmd | http://127.0.0.1:18772/ | 完整模型：GLM、Flash、课程8B、困难8B、审查27B |
| 打开Flash教学.cmd  | 停止Flash教学.cmd  | http://127.0.0.1:18774/ | Flash识图与自然对话；本地数学工具仍可用       |

Flash使用云API。两个入口是不同模型配置；开启哪一个、调用哪些模型取决于其配置和任务。默认只监听本机。后台的凭据就绪检查不执行实时远端健康探测。

在仓库根执行：

```powershell
pnpm education:build
pnpm education:start
# 或使用Flash配置，需先设置EDU_GLM_API_KEY
pnpm education:flash
```

需要Node 24、pnpm 10、Python 3.12+以及 `service/requirements.txt`。`QINGQI_NODE`和`QINGQI_PYTHON`可指定实际可执行文件。安装依赖后须构建ZCode core/adapters、education runtime和Web；`education:build`沿这些包的已有构建入口执行。

从 `service/config/models.example.json`准备 `models.local.json`；Flash入口使用 `vision.local.json`。密钥由配置引用环境变量，GLM/Flash通常使用 `EDU_GLM_API_KEY`。完整模式沿 `tools/run_models.py`建立既有SSH隧道并读取专项凭据。`server/connection.local.json`保存连接资料；账户位于 `service/config/accounts.local.json`。这些本机配置由Git忽略，不能写入示例、报告或提交。

启动文件在未运行时安全提示输入云API key，只传给进程。停止文件按launcher PID、可执行文件和仓库归属核对，不停止其他项目。可用 `QINGQI_PORT`覆盖端口；停止时使用同一端口。

生产状态在 `service/runs/product`，只读数学索引在 `service/data`。搬迁机器需要复制受保护配置和索引或重新导入资料；源码仓库本身不包含个人原始数据。历史清空是后台中的独立业务操作，普通目录清理不会删除学生历史。

导入自己的数学资料时，从仓库根目录传入实际文件路径：

```sh
python education/tools/import_student_data.py --books /path/to/books --questions /path/to/success.jsonl --profiles /path/to/profiles.jsonl --conversations /path/to/conversations.csv
```

Windows路径使用引号。导入结果绑定到独立的示例学生，画像与会话用户未确认对应时会明确标记；不把两套标识冒充同一真实学生。关系按资料中的实际定义导入，不凭文件夹名称补造先修关系。

模型也可在「设置管理 → 模型适配」添加、测试并选择。自定义配置由同一Store加密保存，按入口配置文件名隔离；重启保留，历史清空保留。Windows密文绑定本机用户DPAPI，复制数据库到另一台机器后需要重新填写Key；Unix使用受权限保护的Fernet本机密钥文件。默认连接只读，可复制为自定义；只在相同地址和协议下明确复用默认环境凭据。新请求读取新配置，在途轮次保持快照。使用方法及协议边界见[模型适配说明](zcode-source-architecture-v8.md)。

## 清理约定

长期说明在 `docs`，生成证据在 `.local/reports`。旧报告和临时研究资料归档到仓库旁的 `QingQi-ZCode-archive/2026-11-23-project-cleanup`。明确可重建的验收数据库和Python缓存可以移除；上游apps/packages、许可证、node_modules、运行bundle、模型配置和生产数据保留。

```powershell
powershell -NoProfile -File education/tools/cleanup-project.ps1
# 查看 .local/reports/project-cleanup-plan.local.json 后执行
powershell -NoProfile -File education/tools/cleanup-project.ps1 -Apply
```

脚本对所有绝对删除/移动路径进行边界检查，遇到锁定、重解析点或归档冲突保留原项并记录。维护辅助脚本仍在Git忽略的tmp中，它们用于当前本机安全重启与真实模型专项验收。

公网学校部署仍需TLS、统一身份、备份、容量和保留策略；当前本机验收不等价于公网部署认证。专项服务维护见 [server说明](../server/README.md)。
