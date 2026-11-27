"""Store-owned stop commands and one temporary cancellation scope per accepted turn."""
import http.client,json,socket,sqlite3,threading,urllib.request
from .contracts import ContractError, fingerprint
from .zcode_runtime import RuntimeFailure


def stop_reason(db,identity,request,epoch):
    current=db.execute('SELECT epoch FROM history_control WHERE id=1').fetchone()[0]
    if current!=epoch:return 'history_changed'
    row=db.execute('SELECT payload_hash,epoch FROM turn_stop_commands WHERE student=? AND session=? AND request_id=?',(identity.student,identity.session,request.request_id)).fetchone()
    if row and row[1]==epoch and row[0]==fingerprint(request.dump()):return 'turn_cancelled'
    return None


def stopped_error(reason):
    return RuntimeFailure(reason,'已停止本轮生成，原问题和未完成文字已保留。' if reason=='turn_cancelled' else '历史已变更，此请求已停止，请刷新会话。')


def request_stop(store,identity,request,*,expected_history_epoch=None):
    digest=fingerprint(request.dump())
    with store.db:
        store.db.execute('BEGIN IMMEDIATE')
        epoch=store.history_status()['epoch']
        if expected_history_epoch is not None and epoch!=expected_history_epoch:raise stopped_error('history_changed')
        row=store.db.execute('SELECT id,payload_hash,response,state,lease,expires FROM runs WHERE student=? AND session=? AND request_id=?',(identity.student,identity.session,request.request_id)).fetchone()
        if row and row['payload_hash']!=digest:raise ContractError('停止请求与原输入不一致。')
        if row and row['response']:return {'status':'completed','request_id':request.request_id}
        previous=store.db.execute('SELECT payload_hash,epoch FROM turn_stop_commands WHERE student=? AND session=? AND request_id=?',(identity.student,identity.session,request.request_id)).fetchone()
        if previous and previous[1]==epoch and previous[0]!=digest:raise ContractError('该编号的停止命令已用于另一份输入。')
        import time
        store.db.execute('INSERT INTO turn_stop_commands VALUES(?,?,?,?,?,?) ON CONFLICT(student,session,request_id) DO NOTHING',(identity.student,identity.session,request.request_id,digest,epoch,time.time()))
        stopped=bool(row and json.loads(row['state']).get('error_code')=='turn_cancelled')
        return {'status':'stopped' if stopped else 'stopping','request_id':request.request_id}


class CancellationScope:
    def __init__(self,store,identity,request):
        self.store=store;self.identity=identity;self.request=request;self.epoch=store.history_status()['epoch']
        self.reason=None;self.exit=threading.Event();self.lock=threading.Lock();self.closers=[]
        self.thread=threading.Thread(target=self.watch,daemon=True);self.thread.start()
    def signal(self,reason):
        with self.lock:
            if self.reason:return
            self.reason=reason;closers=list(reversed(self.closers))
        for close in closers:
            try:close()
            except (OSError,RuntimeError):pass
    def check(self):
        reason=self.reason or stop_reason(self.store.db,self.identity,self.request,self.epoch)
        if reason:
            self.signal(reason)
            raise stopped_error(reason)
    def attach(self,close):
        with self.lock:
            self.closers.append(close);stopped=self.reason
        if stopped:
            try:close()
            except OSError:pass
        self.check()
    def watch(self):
        db=sqlite3.connect(self.store.root.joinpath('agent.sqlite').as_uri()+'?mode=ro',uri=True,timeout=1)
        try:
            while not self.exit.is_set():
                try:reason=stop_reason(db,self.identity,self.request,self.epoch)
                except sqlite3.OperationalError:reason=None
                if reason:self.signal(reason);return
                self.exit.wait(.08)
        finally:db.close()
    def close(self):
        self.exit.set();self.thread.join(timeout=6)
        with self.lock:self.closers.clear()


def transport_handlers(scope):
    if scope is None:return []
    def connection(base):
        class Connected(base):
            def connect(self):
                scope.check();super().connect();transport=self.sock
                # 连接由本轮拥有；shutdown 唤醒正在等待正文的读者，关闭页面显示本身不能停止后台。
                scope.attach(lambda:transport.shutdown(socket.SHUT_RDWR))
        return Connected
    class HTTP(urllib.request.HTTPHandler):
        def http_open(self,request):return self.do_open(connection(http.client.HTTPConnection),request)
    class HTTPS(urllib.request.HTTPSHandler):
        def https_open(self,request):return self.do_open(connection(http.client.HTTPSConnection),request,context=self._context)
    return [HTTP(),HTTPS()]
