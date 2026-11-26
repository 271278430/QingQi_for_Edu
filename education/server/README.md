# 专项模型服务

`serve_specialists.py` 每个进程只加载一个固定模型，监听服务器的 127.0.0.1。启动参数为 `--config <本机部署配置> --role course8b|difficulty8b|review27b`。需要 Transformers 5.4.0、torch 2.8、peft 0.18.1 和足够的 GPU 显存；路径、设备与随机 bearer 凭据在部署配置中，用户输入无权修改。

部署配置包含 models（每项 base、可选 adapter、gpu、port、name、system）和 token_file。system 取自对应原生训练/评测格式；禁止直接对微调模型套用产品的新 Schema。权重谱系见 ../source.json；实际服务器配置留在专属新目录，未写入源码。

课程模型使用原生名称列表，输出建议状态；学情模型使用原生四分类，模型生成的 memory 不替换真实历史；审查模型使用实际步骤 ID，转换后与独立符号核验一致才能返回。超时或分歧返回错误，不假造成功结果。

一个模型一次只允许一个推理请求，繁忙时返回 429。输入有大小和 token 上限，输出和推理时间有预算。连接关闭后仍持有模型锁直到该次推理结束，客户端不会自动重发未知结果。记录 provider 用量和原生输出哈希，不打印密钥或学生正文。

本机通过 SSH -L 连接 18008、18009、18027。`tools/run_models.py` 的配置文件仅存 SSH 主机和用户等连接信息，不保存 SSH 口令。专项服务应只由部署者维护；不要停止其他训练任务。当前三个自有进程使用 GPU 0、3、2，具体 PID 记录在服务器专属目录的 processes.local.json。

启动器不会修改系统 VPN 配置。2026-11-19 连接已恢复，采用同一 SSH 会话读取令牌和承载转发；隐藏进程使用显式输入输出管道。服务器临时 Python 读取进程只读令牌，等待输入管道关闭后退出，不写入服务器文件。启动产品前核对三个已认证模型列表；课程、审查和学情完整推理已通过，历史验收已归档；当前入口与复验说明见 ../docs/operations.md 和 ../docs/verification.md。

2026-11-20 本地运行能力改造：服务器适配器仍从 qingqi.domain_tools 导入同一核验实现。发布新版时需同步 service/src/qingqi 与匹配配置，在独立验收通过后再切换自有服务；仅更新 Web 或 server 脚本不会更新当前进程已加载的模块。新版本子表达式核验、模型调用账本与客户端恢复还未执行远端推理验收。

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

可选的课程、困难分析与审查模型服务。

### 文件

| 文件                                         | 简要说明                                                                      |
| -------------------------------------------- | ----------------------------------------------------------------------------- |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                              |
| [serve_specialists.py](serve_specialists.py) | Loopback OpenAI adapter for original training formats; one model per process. |

<!-- qingqi-directory-index:end -->
