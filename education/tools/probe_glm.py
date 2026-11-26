"""Validate the configured provider without printing or persisting credentials."""
import getpass
import json
import os
import urllib.error
import urllib.request

key = os.environ.get("EDU_GLM_API_KEY") or getpass.getpass("GLM API key: ")
model = os.environ.get("EDU_GLM_MODEL", "glm-5.3")
body = {"model": model, "messages": [{"role": "user", "content": "Return a JSON object with status equal to ok."}], "max_tokens": 2048, "reasoning_effort": "low"}
request = urllib.request.Request("https://open.bigmodel.cn/api/paas/v4/chat/completions", data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
try:
    with opener.open(request, timeout=90) as response:
        data = json.load(response)
    print(json.dumps({"model": data.get("model"), "content": data["choices"][0]["message"].get("content"), "usage": data.get("usage")}, ensure_ascii=False))
except urllib.error.HTTPError as error:
    data = json.loads(error.read())
    print(json.dumps({"status": error.code, "error": data.get("error")}, ensure_ascii=False))
    raise SystemExit(1)
