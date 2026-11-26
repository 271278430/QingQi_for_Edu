"""Create a self-authored demo catalogue; never reuse or overwrite a real student's state."""
import argparse
from contextlib import closing
import json
import sqlite3
import sys
import uuid
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'service/src'))
from import_student_data import SCHEMA
from qingqi.agent import PROJECT
from qingqi.contracts import canonical
from qingqi.domain_tools import number
from qingqi.graph import norm
from qingqi.learning import BANK,TOPICS
from qingqi.product import server
from qingqi.teaching_responses import calculation_steps

VERSION='qingqi_public_demo_v1'


def prepare(root=None):
    root=(root or PROJECT/'runs/demo-v1').resolve()
    if root==PROJECT/'runs/product':raise ValueError('演示数据不能写入正式学生目录。')
    target=PROJECT/'data/demo_seed_v1.sqlite'
    target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():
        stage=target.with_suffix('.'+uuid.uuid4().hex+'.tmp')
        # SQLite上下文只提交事务，Windows仍持有句柄；关闭后才能原子替换索引。
        with closing(sqlite3.connect(stage)) as db:
            db.executescript(SCHEMA)
            db.execute('INSERT INTO nodes VALUES(?,?,?,?,?,?,?)',('demo-math','数学基础',norm('数学基础'),'初中数学','Course','项目自编合成演示','QingQi demo'))
            for t in TOPICS:
                db.execute('INSERT INTO nodes VALUES(?,?,?,?,?,?,?)',(t['id'],t['title'],norm(t['title']),'初中数学','KnowledgeItem',t['objective'],'QingQi demo'))
                db.execute('INSERT INTO edges VALUES(?,?,?,?,?)',('contains-'+t['id'],'demo-math',t['id'],'contains','QingQi demo'))
                for prior in t['requires']:
                    db.execute('INSERT INTO prerequisites VALUES(?,?,?,?)',(prior+'-'+t['id'],prior,t['id'],'项目自编演示先修'))
            initial={'identity':'合成示例学生','grade':'七年级','subject':'数学','as_of':'2026-01-01','n_attempts':0,'history_count':0,'identity_link':'synthetic_demo','source':'项目自编合成演示','topics':{}}
            meta={'version':VERSION,'student_initial':initial,'student_history':[],'topics':TOPICS,'coverage':'项目自编演示 · 5个知识点 · 45道数值练习'}
            for key,value in meta.items():db.execute('INSERT INTO metadata VALUES(?,?)',(key,canonical(value)))
            for raw in BANK.values():
                entry={**raw,'version':VERSION,'grade':'七年级','kind':'numeric','key':{'kind':'numeric','values':[str(number(raw['expression']))]},'analysis':calculation_steps(raw['expression']),'options':[],'source':'项目自编演示','quality':'complete'}
                db.execute('INSERT INTO items VALUES(?,?,?)',(entry['id'],1,canonical(entry)))
            db.commit()
        stage.replace(target)
    root.mkdir(parents=True,exist_ok=True)
    registry=root/'catalogue.local.json'
    value={'path':str(target.resolve()),'version':VERSION,'profile':'demo-student','student':'edu-demo-student','name':'示例学生'}
    if registry.exists() and json.loads(registry.read_text(encoding='utf-8-sig'))!=value:
        raise ValueError('这个运行目录已有其他资料，请换一个演示目录。')
    if not registry.exists():registry.write_text(canonical(value),encoding='utf-8')
    return root


def main():
    parser=argparse.ArgumentParser(description='清启自编数据演示，无需密钥')
    parser.add_argument('--port',type=int,default=18774)
    args=parser.parse_args()
    instance=server(args.port,root=prepare())
    print(f'清启演示 http://127.0.0.1:{instance.server_port} · 退出请按 Ctrl+C',flush=True)
    try:instance.serve_forever()
    except KeyboardInterrupt:pass
    finally:instance.server_close()


if __name__=='__main__':main()
