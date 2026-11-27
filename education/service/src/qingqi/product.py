"""HTTP product adapter; the existing teaching Loop owns accepted state."""
from __future__ import annotations
import argparse
import hashlib
import hmac
import json
import mimetypes
import os
import secrets
import threading
import time
import uuid
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from .agent import Agent, PROJECT
from .contracts import ContractError, Denied, Identity, Request, SHORT, obj, validate,MODEL_SELECTION_SCHEMA
from .graph import Graph
from .providers import Endpoint, GLMController, JSONModel
from .storage import Busy, Store
from .web_store import WebStore
from .workers import make_workers
from .zcode_runtime import VERSION as RUNTIME_VERSION, RuntimeFailure
from .projection import project_response

COOKIE = "qingqi_education_session"
DEMO = {"student-a": {"name": "学习者 A", "role": "student"}, "student-b": {"name": "学习者 B", "role": "student"}, "teacher-demo": {"name": "教师演示", "role": "teacher"}}

def password_hash(password, salt=None):
    salt = salt or secrets.token_hex(16)
    value = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 310000).hex()
    return f"pbkdf2_sha256$310000${salt}${value}"

def check_password(password, encoded):
    try:
        algorithm, count, salt, digest = encoded.split("$")
        return algorithm == "pbkdf2_sha256" and count == "310000" and hmac.compare_digest(hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 310000).hex(), digest)
    except (ValueError, TypeError):
        return False

class Deployment:
    def __init__(self, config=None, accounts=None):
        configuration = json.loads(config.read_text(encoding="utf-8-sig")) if config else {}
        values = configuration.get("models", {})
        self.turn_seconds = configuration.get("turn_seconds", 25)
        self.lease_seconds = configuration.get("lease_seconds", 30)
        if not 1 <= self.turn_seconds <= 300 or not self.turn_seconds < self.lease_seconds <= 400:
            raise ValueError("invalid execution budgets")
        self.endpoints = {}
        self.model_root = None
        self.model_scope = config.name if config else 'local'
        for name, options in values.items():
            if name not in {"glm", "vision", "course8b", "difficulty8b", "review27b"}:
                raise ValueError("unknown model role")
            endpoint = Endpoint(name=name, **{'supports_image':name=='vision',**options})
            if not isinstance(endpoint.json_mode, bool) or endpoint.json_mode and endpoint.protocol != "openai":
                raise ValueError("invalid JSON mode configuration")
            if not 1 <= endpoint.timeout <= min(90, self.turn_seconds) or not 64 <= endpoint.max_tokens <= 8192 or endpoint.reasoning_effort not in {"", "low", "high", "max"}:
                raise ValueError("invalid model generation budget")
            self.endpoints[name] = endpoint
        self.demo = accounts is None
        self.accounts = DEMO if self.demo else json.loads(accounts.read_text(encoding="utf-8-sig"))["accounts"]
        if not self.accounts:
            raise ValueError("at least one account required")
        for key, account in self.accounts.items():
            if not key or len(key) > 80 or account.get("role") not in {"student", "teacher"} or not isinstance(account.get("name"), str):
                raise ValueError("invalid account")
            if not self.demo and not account.get("password_hash", "").startswith("pbkdf2_sha256$310000$"):
                raise ValueError("provision accounts with the account command")

    def agent(self, root, chat_models=None):
        models = self.current_models(root)
        # GUI文本角色也使用glm别名，但选型不等于启用额外分类；仅部署显式主控使用模型路由。
        use_glm_controller=bool(self.endpoints.get('glm') and self.endpoints['glm'].enabled)
        if chat_models is not None:
            models={name:model for name,model in models.items() if name not in {'glm','vision'}}
            models.update(chat_models)
        controller = GLMController(models["glm"]) if use_glm_controller and "glm" in models else None
        from .layered_routing import LayeredRouter
        # 对话选模只更换推理客户端；原Flash入口保持本地意图路由，不能因文本/图片同型号多调用一次分类模型。
        router=controller or LayeredRouter()
        seconds=max(self.turn_seconds,max((m.endpoint.timeout+5 for m in models.values()),default=0))
        return Agent(root, self.graph_path, controller=controller, router=router, workers=make_workers(models), vision_model=models.get('vision'), text_model=models.get('glm'), turn_seconds=seconds, lease_seconds=max(self.lease_seconds,seconds+5))

    def model_settings(self,store):
        from .model_settings import ModelSettings
        return ModelSettings(store,self.model_scope,self.endpoints)

    def current_models(self,root=None):
        models={name:JSONModel(e) for name,e in self.endpoints.items() if e.enabled}
        root=root or self.model_root
        if root:
            owner=Store(root)
            try:custom=self.model_settings(owner).resolve()
            finally:owner.close()
            if custom is not None:
                models={name:model for name,model in models.items() if name not in {'glm','vision'}}
                models.update(custom)
        return models

    def status(self):
        labels = {"glm": "文本教学与任务决策", "vision": "图片识别与多模态辅导", "course8b": "课程导航 8B", "difficulty8b": "学习困难 8B", "review27b": "作答审查 27B"}
        models=self.current_models()
        return [{"id": key, "label": label, "model": models[key].endpoint.model if key in models else "",
                 "enabled":key in models,"supports_image":bool(models[key].endpoint.supports_image) if key in models else False,
                 "credential_ready":bool(models[key].credential() if models[key].credential else os.environ.get(models[key].endpoint.key_env)) or not models[key].endpoint.requires_key if key in models else False} for key,label in labels.items()]

    def configuration_status(self):
        enabled=set(self.current_models())
        profile='full' if enabled=={'glm','vision','course8b','difficulty8b','review27b'} else 'flash' if enabled=={'vision'} else 'local' if not enabled else 'custom'
        return {'profile':profile,'label':{'full':'完整模型配置','flash':'Flash教学配置','local':'本地规则配置','custom':'自定义模型配置'}[profile],'health_verified':False}

def server(port=18772, *, root=None, deployment=None, assets=None, origins=()):
    from .geometry_solver import prepare_geometry
    prepare_geometry()
    root = (root or PROJECT / "runs/product").resolve()
    deployment = deployment or Deployment()
    deployment.model_root=root
    assets = (assets or PROJECT.parent / "web/dist").resolve()
    initial = WebStore(root)
    c = initial.owner.catalogue
    deployment.graph_path = Path(c.config['path']) if c.config else PROJECT / 'data/curriculum.sqlite'
    deployment.student_only = bool(c.config)
    if c.config and deployment.demo:
        deployment.accounts = {c.config['profile']: {'name':c.config['name'], 'role':'student'}}
    deployment.default_profile = next(iter(deployment.accounts)) if deployment.demo else ''
    deployment.manage_profiles={k for k,v in deployment.accounts.items() if v.get('can_manage') is True}
    if deployment.demo and c.config:deployment.manage_profiles.add(deployment.default_profile)
    if c.config and any(a['role'] != 'student' for a in deployment.accounts.values()):
        raise ValueError('student-only deployment requires student accounts')
    initial.close()
    sessions, failures = {}, {}
    lock = threading.Lock()
    jobs = threading.BoundedSemaphore(4)
    dummy = password_hash(secrets.token_urlsafe(20))

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def safe(self):
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Cache-Control", "no-store")
            # 上游内嵌数学字体与 Shiki WASM 需对应来源许可；仍禁止 JS eval 与外部脚本。
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")

        def reply(self, status, value, cookie=None):
            if getattr(self,'stream_started',False):
                return self.stream_event({'kind':'done','value':value} if status<400 else {'kind':'error','status':status,**value})
            raw = json.dumps(value, ensure_ascii=False, allow_nan=False).encode()
            self.send_response(status)
            self.safe()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            if cookie is not None:
                # Cookie 不按端口隔离；两个本机入口必须使用不同名称，避免互相挤掉登录和 CSRF。
                self.send_header("Set-Cookie", f"{COOKIE}_{self.server.server_port}={cookie}; Path=/; HttpOnly; SameSite=Strict" + ("; Max-Age=0" if not cookie else ""))
            self.end_headers()
            self.wfile.write(raw)

        def stream_event(self,event):
            self.stream_seq+=1
            if getattr(self,'stream_disconnected',False):return
            try:
                raw=json.dumps({**event,'seq':self.stream_seq,'request_id':self.stream_request_id},ensure_ascii=False).encode()
                self.wfile.write(b'data: '+raw+b'\n\n');self.wfile.flush()
            except (BrokenPipeError,ConnectionResetError,OSError):
                # 断开的是展示链路，已经准入的Agent仍完成唯一事务，原编号可读已接受结果。
                self.stream_disconnected=True

        def host_ok(self):
            return self.headers.get("Host") in {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}

        def principal(self, create=False):
            jar = SimpleCookie()
            try:
                jar.load(self.headers.get("Cookie", ""))
            except Exception:
                pass
            cookie_name=f'{COOKIE}_{self.server.server_port}'
            key = jar[cookie_name].value if cookie_name in jar else ""
            with lock:
                record = sessions.get(key)
                if record and record["expires"] > time.time():
                    record["expires"] = time.time() + 43200
                    return key, dict(record), False
                if not create:
                    raise Denied("session expired")
                for old in [k for k, v in sessions.items() if v["expires"] <= time.time()]:
                    sessions.pop(old)
                if len(sessions) >= 100:
                    raise Busy("session capacity")
                key = secrets.token_urlsafe(32)
                record = {"profile": deployment.default_profile, "csrf": secrets.token_urlsafe(32), "expires": time.time() + 43200}
                sessions[key] = record
                return key, dict(record), True

        def account(self, record):
            if record["profile"] not in deployment.accounts:
                raise Denied("login required")
            return deployment.accounts[record["profile"]]

        def bootstrap(self, record):
            account = deployment.accounts.get(record["profile"])
            models = deployment.status()
            from .management import settings
            reader=Store(root)
            try:public_settings=settings(reader)
            finally:reader.close()
            return {"can_manage": record["profile"] in deployment.manage_profiles, "settings": public_settings, "authenticated": account is not None, "demo": deployment.demo, "profile": record["profile"], "name": account["name"] if account else "", "role": account["role"] if account else "", "csrf": record["csrf"], "profiles": [{"id": k, "name": v["name"], "role": v["role"]} for k, v in deployment.accounts.items()] if deployment.demo else [], "mode": "model" if any(v["enabled"] for v in models) else "offline", "models": models, "product": "清启 · ZCode Education"}

        def do_GET(self):
            if not self.host_ok():
                return self.reply(403, {"error": "host_denied"})
            url = urlsplit(self.path)
            if url.path == "/api/health":
                return self.reply(200, {"status": "ok", "product": "qingqi-education", "demo": deployment.demo, "runtime": RUNTIME_VERSION})
            if not url.path.startswith("/api/"):
                relative = url.path.lstrip("/")
                file = (assets / (relative if relative and relative != "education" else "index.html")).resolve()
                if not file.is_relative_to(assets):
                    return self.reply(404, {"error": "not_found"})
                if not file.is_file() and "." not in Path(relative).name:
                    file = assets / "index.html"
                if not file.is_file():
                    return self.reply(404, {"error": "assets_not_built", "message": "请先运行 pnpm education:build。"})
                raw = file.read_bytes()
                self.send_response(200)
                self.safe()
                self.send_header("Content-Type", (mimetypes.guess_type(file.name)[0] or "application/octet-stream"))
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                return self.wfile.write(raw)
            store = graph = None
            try:
                key, record, new = self.principal(url.path == "/api/bootstrap")
                if url.path == "/api/bootstrap":
                    return self.reply(200, self.bootstrap(record), key if new else None)
                account = self.account(record)
                student = "edu-" + record["profile"]
                store = WebStore(root)
                query = parse_qs(url.query)
                if url.path=='/api/chat/models':
                    from .chat_models import ChatModels
                    session=query.get('session',[''])[0]
                    if session:store.own(student,session)
                    return self.reply(200,ChatModels(deployment.model_settings(store.owner),student,session).view())
                if url.path == "/api/sessions":
                    return self.reply(200, {"sessions": store.sessions(student)})
                if url.path == "/api/session":
                    return self.reply(200, store.detail(student, query.get("id", [""])[0]))
                if url.path == "/api/memory":
                    return self.reply(200, store.memory(student))
                if url.path == "/api/models":
                    return self.reply(200, {"models": deployment.status()})
                if url.path == '/api/settings/models':
                    if record['profile'] not in deployment.manage_profiles:raise Denied('manager required')
                    return self.reply(200,deployment.model_settings(store.owner).view())
                if url.path in {'/api/settings','/api/settings/architecture'}:
                    if record['profile'] not in deployment.manage_profiles:raise Denied('manager required')
                    if url.path.endswith('/architecture'):
                        from .architecture_catalog import architecture
                        return self.reply(200,architecture(deployment))
                    from .management import overview
                    return self.reply(200,overview(store.owner,deployment,student))
                if url.path == "/api/learning":
                    return self.reply(200, store.owner.learning_overview(student))
                if url.path == '/api/practice/history':
                    return self.reply(200, {'items': store.practice_history(student)})
                if url.path == '/api/tutor/image':
                    raw = store.owner.image(student, query.get('id', [''])[0])['data']
                    self.send_response(200)
                    self.safe()
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', str(len(raw)))
                    self.end_headers()
                    return self.wfile.write(raw)
                if url.path in {"/api/courses", "/api/course", "/api/dashboard"}:
                    graph = Graph(deployment.graph_path)
                    if url.path == "/api/courses":
                        return self.reply(200, graph.search(query.get("q", [""])[0][:200], query.get("subject", [""])[0][:100], 20))
                    if url.path == "/api/course":
                        return self.reply(200, graph.context(query.get("id", [""])[0]))
                    responses = [json.loads(r[0]) for r in store.db.execute("SELECT response FROM runs WHERE student=? AND response IS NOT NULL", (student,))]
                    return self.reply(200, {"turns": len(responses), "sessions": len(store.sessions(student)), "verified_correct": sum(v.get("teaching_action") == "confirm" for v in responses), "nodes": graph.db.execute("SELECT count(*) FROM nodes").fetchone()[0], "edges": graph.db.execute("SELECT count(*) FROM edges").fetchone()[0]})
                if url.path == "/api/students" and account["role"] == "teacher":
                    return self.reply(200, {"students": [{"id": k, "name": v["name"]} for k, v in deployment.accounts.items() if v["role"] == "student"]})
                return self.reply(404, {"error": "not_found"})
            except Denied:
                self.reply(403, {"error": "not_allowed", "message": "请登录自己的账户，或选择属于当前学生的学习对话。"})
            except (ValueError, ContractError):
                self.reply(400, {"error": "invalid_input", "message": "请检查查询内容。"})
            except RuntimeFailure as error:
                self.reply(429 if error.code == "model_busy" else 422 if error.code == "unsupported_input" else 409 if error.code in {"model_unknown", "settings_conflict"} else 502,
                           {"error": error.code, "message": str(error), "recoverable": error.recoverable, "retry_after": error.retry_after})
            except Busy:
                self.reply(429, {"error": "busy", "message": "请求较多，请稍后重试。"})
            finally:
                if store:
                    store.close()
                if graph:
                    graph.close()

        def do_POST(self):
            if not self.host_ok():
                return self.reply(403, {"error": "host_denied"})
            store = agent = None
            acquired = False
            self.connection.settimeout(30)
            try:
                key, record, _ = self.principal()
                valid_origins = {f"http://127.0.0.1:{self.server.server_port}", f"http://localhost:{self.server.server_port}", *origins}
                if self.headers.get("Origin") not in valid_origins or not hmac.compare_digest(self.headers.get("X-Qingqi-CSRF", "").encode(), record["csrf"].encode()):
                    raise Denied("origin or csrf")
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= (12_000_000 if self.path == '/api/tutor/images' else 32000):
                    return self.reply(413, {"error": "input_too_large", "message": "请缩短问题或学习记录。"})
                body = json.loads(self.rfile.read(length))
                if self.path == "/api/login":
                    validate(body, obj({"username": SHORT, "password": {"type": "string", "minLength": 1, "maxLength": 256}}))
                    user = body["username"]
                    with lock:
                        now = time.time()
                        for old in [k for k, v in failures.items() if not v or now - v[-1] > 60]:
                            failures.pop(old)
                        if len(failures) >= 1000:
                            raise Busy("login capacity")
                        recent = [v for v in failures.get(user, []) if now - v < 60]
                        if len(recent) >= 5:
                            raise Busy("login rate limit")
                        failures[user] = recent + [now]
                    account = deployment.accounts.get(user)
                    verified = check_password(body["password"], account.get("password_hash", dummy) if account else dummy)
                    if deployment.demo or not verified or not account:
                        raise Denied("invalid login")
                    new_key = secrets.token_urlsafe(32)
                    with lock:
                        sessions.pop(key, None)
                        record = {"profile": user, "csrf": secrets.token_urlsafe(32), "expires": time.time() + 43200}
                        sessions[new_key] = record
                    return self.reply(200, self.bootstrap(record), new_key)
                account = self.account(record)
                if self.path == "/api/logout":
                    with lock:
                        sessions.pop(key, None)
                    return self.reply(200, {"ok": True}, "")
                if self.path == "/api/profile":
                    if not deployment.demo or deployment.student_only:
                        raise Denied("switch only in explicit demo")
                    validate(body, obj({"profile": {"type": "string", "enum": list(deployment.accounts)}}))
                    with lock:
                        sessions[key]["profile"] = body["profile"]
                        record = dict(sessions[key])
                    return self.reply(200, self.bootstrap(record))
                store = WebStore(root)
                student = "edu-" + record["profile"]
                if self.path=='/api/chat/models':
                    from .chat_models import ChatModels
                    if not isinstance(body.get('session',''),str) or len(body.get('session',''))>100:raise ContractError('会话编号无效。')
                    session=body.get('session','')
                    if session:store.own(student,session)
                    return self.reply(200,ChatModels(deployment.model_settings(store.owner),student,session).select(body))
                if self.path in {'/api/settings/model-providers','/api/settings/model-selection','/api/settings/models/discover','/api/settings/models/test'}:
                    if record['profile'] not in deployment.manage_profiles:raise Denied('manager required')
                    manager=deployment.model_settings(store.owner)
                    if self.path.endswith('/model-providers'):return self.reply(200,manager.update_provider(body))
                    if self.path.endswith('/model-selection'):return self.reply(200,manager.select(body))
                    if set(body)-{'provider_id','kind'} or not isinstance(body.get('provider_id'),str):raise ContractError('请指定已保存连接。')
                    acquired=jobs.acquire(blocking=False)
                    if not acquired:raise Busy('capacity')
                    return self.reply(200,manager.discover(body['provider_id']) if self.path.endswith('/discover') else manager.test(body['provider_id'],body.get('kind')))
                if self.path=='/api/settings':
                    if record['profile'] not in deployment.manage_profiles:raise Denied('manager required')
                    from .management import update
                    return self.reply(200,update(store.owner,student,body))
                if self.path=='/api/settings/history/clear':
                    if record['profile'] not in deployment.manage_profiles:raise Denied('manager required')
                    return self.reply(200,store.owner.clear_history(student,body))
                from .management import settings
                if settings(store.owner)['maintenance'] and self.path in {'/api/teach','/api/tutor/images','/api/practice/start','/api/practice/recommendations','/api/practice/answer','/api/practice/hint','/api/learning/goal','/api/learning/route'}:
                    return self.reply(423,{'error':'maintenance','message':'系统正在维护，已有学习记录仍可查看，请稍后再提交。'})
                if self.path == '/api/tutor/images':
                    validate(body, obj({'request_id': SHORT, 'name': {'type':'string', 'maxLength':80}, 'data_url': {'type':'string', 'maxLength':11_500_000}}))
                    acquired = jobs.acquire(blocking=False)
                    if not acquired:
                        raise Busy('capacity')
                    return self.reply(201, store.owner.upload_image(student, body))
                if self.path == "/api/sessions":
                    validate(body, obj({"title": {"type": "string", "maxLength": 100},'model_selection':MODEL_SELECTION_SCHEMA}, []))
                    from .chat_models import ChatModels
                    selection=body.get('model_selection')
                    if selection is not None:ChatModels(deployment.model_settings(store.owner),student,'').normalize(selection)
                    session=store.create(student, body.get("title", "新的学习对话"),initialize=(lambda id:ChatModels(deployment.model_settings(store.owner),student,id).initialize(selection)) if selection is not None else None)
                    return self.reply(201,session)
                if self.path == "/api/learning/goal":
                    validate(body, obj({"topic": {"type": "string", "enum": [t['id'] for t in store.owner.catalogue.topics]}, "minutes": {"type": "integer", "minimum": 10, "maximum": 45}}))
                    store.owner.set_learning_goal(student, body["topic"], body["minutes"])
                    return self.reply(200, {"ok": True})
                if self.path == "/api/practice/start":
                    validate(body, obj({"item_id": SHORT, "request_id": SHORT}))
                    return self.reply(201, store.start_practice(student, body))
                if self.path == '/api/learning/route':
                    from .learning_branches import ROUTES
                    validate(body, obj({'route': {'type': 'string', 'enum': list(ROUTES)}, 'request_id': SHORT}))
                    return self.reply(200, store.owner.select_learning_route(student, body))
                if self.path == "/api/practice/recommendations":
                    validate(body, obj({"request_id": SHORT}))
                    return self.reply(200, store.owner.renew_recommendations(student, body))
                if self.path in {"/api/practice/answer", "/api/practice/hint"}:
                    kind = "answer" if self.path.endswith("answer") else "hint"
                    extra = {"answer": {"type": "string", "minLength": 1, "maxLength": 120}} if kind == "answer" else {"style": {"type": "string", "enum": ["socratic", "heuristic", "explain"]}}
                    validate(body, obj({"assignment_id": SHORT, "request_id": SHORT, **extra}))
                    if kind=='hint' and body['style']!='explain' and store.owner.catalogue.config and bool({'glm','vision'} & deployment.current_models(root).keys()):
                        marker=store.owner.prepare_model_hint(student,body)
                        if 'result' in marker:return self.reply(200,marker['result'])
                        history_epoch=store.admit_teaching(student,marker['session'])
                        acquired=jobs.acquire(blocking=False)
                        if not acquired:raise Busy('capacity')
                        agent=deployment.agent(root)
                        request=Request.parse({'request_id':'hint:'+hashlib.sha256(body['request_id'].encode()).hexdigest()[:32],
                                               'question':'请返回原练习，给我一点提示，不要最终答案。'})
                        agent.run(Identity(student,marker['session']),request,expected_history_epoch=history_epoch,practice_hint=marker)
                        store.touch(student,marker['session'],request.question)
                        return self.reply(200,store.owner.prepare_model_hint(student,body)['result'])
                    return self.reply(200, store.owner.practice_action(student, kind, body))
                if self.path == "/api/teacher/facts":
                    if account["role"] != "teacher":
                        raise Denied("teacher required")
                    validate(body, obj({"student": SHORT, "key": SHORT, "value": SHORT, "source": SHORT}))
                    if deployment.accounts.get(body["student"], {}).get("role") != "student":
                        raise Denied("student outside deployment")
                    owner = Store(root)
                    try:
                        owner.confirm_fact(Identity("edu-" + body["student"], "teacher-confirmation"), body["key"], body["value"], body["source"], teacher_authorized=True)
                    finally:
                        owner.close()
                    return self.reply(201, {"ok": True})
                if self.path == "/api/teach":
                    validate(body, obj({"session": SHORT, "request": {"type": "object"}}))
                    request = Request.parse({"request_id": uuid.uuid4().hex, **body["request"]})
                    history_epoch=store.admit_teaching(student,body['session'],request)
                    acquired = jobs.acquire(blocking=False)
                    if not acquired:
                        raise Busy("capacity")
                    from .chat_models import ChatModels
                    manager=ChatModels(deployment.model_settings(store.owner),student,body['session'])
                    chosen=manager.resolve_selection(request.model_selection if 'model_selection' in body['request'] else None)
                    agent = deployment.agent(root,chosen) if chosen else deployment.agent(root)
                    streaming='text/event-stream' in self.headers.get('Accept','')
                    if streaming:
                        self.send_response(200);self.safe();self.send_header('Content-Type','text/event-stream; charset=utf-8');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Connection','close');self.send_header('X-Accel-Buffering','no');self.end_headers()
                        self.stream_started=True;self.stream_seq=0;self.stream_request_id=request.request_id
                        # SSE注释握手让浏览器立即进入流读取，不把短增量攒到正文嗅探阈值；它不是教学文字。
                        self.wfile.write(b': stream opened '+b' '*2048+b'\n\n');self.wfile.flush()
                        self.stream_event({'kind':'progress','text':'正在读取原题并识别本次教学任务。'})
                    response = agent.run(Identity(student, body["session"]), request,expected_history_epoch=history_epoch,on_event=self.stream_event if streaming else None)
                    store.touch(student, body["session"], request.question)
                    return self.reply(200, {"response": project_response(response), "session": store.detail(student, body["session"])})
                if self.path == '/api/teach/stop':
                    validate(body,obj({'session':SHORT,'request':{'type':'object'}}))
                    request=Request.parse(body['request'])
                    history_epoch=store.admit_teaching(student,body['session'],request)
                    result=store.owner.stop_turn(Identity(student,body['session']),request,expected_history_epoch=history_epoch)
                    if result['status']=='stopping':store.touch(student,body['session'],request.question)
                    return self.reply(200,result)
                return self.reply(404, {"error": "not_found"})
            except RuntimeFailure as error:
                self.reply(429 if error.code == "model_busy" else 422 if error.code == "unsupported_input" else 409 if error.code in {"model_unknown", "model_changed", "settings_conflict", "history_busy", "history_changed", "turn_cancelled"} else 502,
                           {"error": error.code, "message": str(error), "recoverable": error.recoverable, "retry_after": error.retry_after})
            except Busy:
                self.reply(429, {"error": "busy", "message": "请求正在处理或尝试过于频繁，请稍后重试。"})
            except Denied:
                self.reply(403, {"error": "not_allowed", "message": "账户、会话归属或操作权限不符，请重新登录或检查选择。"})
            except ContractError as error:
                self.reply(400, {'error': 'invalid_input', 'message': str(error)[:300]})
            except (ValueError, KeyError):
                self.reply(400, {"error": "invalid_input", "message": "请检查问题、算式和作答步骤。"})
            except TimeoutError:
                self.reply(504, {"error": "timeout", "message": "处理超时，进度已保留。可重试当前请求。"})
            except Exception:
                self.reply(500, {"error": "internal", "message": "暂时无法完成辅导，进度已保留。请检查模型连接或重试。"})
            finally:
                if agent:
                    agent.close()
                if store:
                    store.close()
                if acquired:
                    jobs.release()

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)

def main():
    parser = argparse.ArgumentParser(description="QingQi / ZCode education")
    parser.add_argument("--port", type=int, default=18772)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--accounts", type=Path)
    parser.add_argument("--assets", type=Path)
    parser.add_argument("--origin", action="append", default=[])
    args = parser.parse_args()
    instance = server(args.port, deployment=Deployment(args.config, args.accounts), assets=args.assets, origins=args.origin)
    print(f"清启教育工作台 http://127.0.0.1:{instance.server_port}", flush=True)
    try:
        instance.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        instance.server_close()

if __name__ == "__main__":
    main()
