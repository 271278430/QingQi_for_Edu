"""Isolated real HTTP owner; controlled rich reply tests presentation, not models."""
import json
from pathlib import Path
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "service/src"))
from qingqi.agent import Agent, PROJECT
from qingqi.product import Deployment, server
from qingqi.planning import OfflineController, reply
from qingqi.zcode_runtime import RuntimeFailure


class RenderingController(OfflineController):
    def next(self, request, state, context, registry):
        if request.question == "你好,模拟断连":
            # 仅模拟已记录错误的呈现；真正断连防重发由 runtime_reuse_acceptance 覆盖。
            raise RuntimeFailure("model_unknown", "模型结果待核查，记录已保留。")
        if request.question == "你好":
            return reply("**学习笔记**\n\n行内公式 $\\frac{1}{2}+\\frac{1}{3}=\\frac{5}{6}$。\n\n$$a^2+b^2=c^2$$\n\n| 知识点 | 状态 |\n| --- | --- |\n| 分数 | 待练习 |\n\n```python\nprint(2 + 3)\n```", "chat")
        return super().next(request, state, context, registry)


class RenderingDeployment(Deployment):
    def agent(self, root):
        return Agent(root, PROJECT / "data/curriculum.sqlite", controller=RenderingController())


instance = server(0, root=PROJECT / "runs/source-reuse" / uuid.uuid4().hex, deployment=RenderingDeployment())
print(json.dumps({"base": f"http://127.0.0.1:{instance.server_port}"}), flush=True)
try:
    instance.serve_forever()
finally:
    instance.server_close()
