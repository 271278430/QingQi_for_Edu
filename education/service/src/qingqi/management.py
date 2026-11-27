"""Real settings commands share the existing SQLite owner and request ledger."""
import json
import time
from .contracts import canonical,fingerprint,validate,obj,SHORT,ContractError
from .zcode_runtime import RuntimeFailure

DEFAULT={'version':0,'app_name':'清启','notice':'','maintenance':False}
SCHEMA=obj({'request_id':SHORT,'version':{'type':'integer','minimum':0},'app_name':{'type':'string','minLength':1,'maxLength':30},'notice':{'type':'string','maxLength':160},'maintenance':{'type':'boolean'}})
def settings(store):
    row=store.db.execute('SELECT data FROM system_settings WHERE id=1').fetchone()
    return json.loads(row[0]) if row else dict(DEFAULT)
def update(store,principal,body):
    validate(body,SCHEMA)
    if not body['app_name'].strip() or '<' in body['app_name']+body['notice']:raise ContractError('设置文本不能为空或含HTML标签')
    with store.db:
        store.db.execute('BEGIN IMMEDIATE')
        row=store.db.execute('SELECT payload_hash,data FROM system_setting_events WHERE principal=? AND request_id=?',(principal,body['request_id'])).fetchone()
        if row:
            if row[0]!=fingerprint(body):raise RuntimeFailure('settings_conflict','该操作编号已用于另一份设置，请重新读取后保存。')
            # 旧命令只确认已经接受；返回当前投影，不能把较新的设置在界面上回滚。
            return settings(store)
        prior=settings(store)
        if prior['version']!=body['version']:raise RuntimeFailure('settings_conflict','设置已被其他操作更新，请刷新后重新修改。')
        data={k:body[k] for k in ('app_name','notice','maintenance')};data['version']=prior['version']+1
        store.db.execute('INSERT INTO system_settings(id,data) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data',(canonical(data),))
        store.db.execute('INSERT INTO system_setting_events VALUES(?,?,?,?,?)',(principal,body['request_id'],fingerprint(body),canonical(data),time.time()))
        return data
def overview(store,deployment,principal):
    from .architecture_catalog import VERSION
    c=store.catalogue
    counts={table:store.db.execute(f'SELECT COUNT(*) FROM {table} WHERE student=?',(principal,)).fetchone()[0] for table in ('runs','episodes','practice_assignments')}
    from .catalogue import complete_item
    source_items=c.db.execute('select count(*) from items where eligible=1').fetchone()[0] if c.db else len(c.bank)
    grade=c.initial.get('grade','')
    ready=sum(complete_item(v) and (not grade or v.get('grade')==grade) for v in c.bank.values())
    # 主动停止是正常终态；运行中的请求和历史清理也不是系统故障。
    errors=store.db.execute("SELECT id,state FROM runs WHERE student=? AND response IS NULL AND json_extract(state,'$.error_code') IS NOT NULL AND json_extract(state,'$.error_code') NOT IN ('turn_cancelled','history_changed') ORDER BY id DESC LIMIT 5",(principal,)).fetchall()
    return {'settings':settings(store),'history':store.history_status(),'models':deployment.status(),'deployment':deployment.configuration_status(),'runtime':'ZCode Registry / Executor / MCP / Skills','counts':counts,'catalogue':{'topics':len(c.topics),'questions':len(c.bank),'source_items':source_items,'generated_items':len(c.bank)-source_items,'student_ready_items':ready,'grade':grade,'graph_nodes':c.db.execute('select count(*) from nodes').fetchone()[0] if c.db else 0},'architecture_version':VERSION,'sample':bool(c.config),'recent_errors':[{'run_id':r[0],'code':json.loads(r[1])['error_code']} for r in errors]}
