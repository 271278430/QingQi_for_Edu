"""Read-only checks of both real product entries and the current catalogue."""
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'education/service/src'))
from qingqi.catalogue import Catalogue,complete_item


def run():
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    entries=[]
    for port in (18772,18774):
        base=f'http://127.0.0.1:{port}'
        with opener.open(base+'/api/health',timeout=8) as response:health=json.load(response)
        with opener.open(base+'/',timeout=8) as response:status=response.status;html=response.read().decode()
        asset=re.search(r'<script[^>]+src="([^"]+)"',html).group(1)
        with opener.open(base+asset,timeout=8) as response:bundle_status=response.status;bundle_size=len(response.read())
        assert status==bundle_status==200 and health.get('product')=='qingqi-education'
        entries.append({'url':base+'/','html_status':status,'health':health,'bundle_status':bundle_status,'bundle_bytes':bundle_size})
    catalogue=Catalogue(ROOT/'education/service/runs/product')
    try:
        meta={k:json.loads(v) for k,v in catalogue.db.execute('select * from metadata')}
        usable=[e for e in catalogue.bank.values() if e.get('grade')=='7' and complete_item(e)]
        audit={'version':catalogue.version,'graph_nodes':catalogue.db.execute('select count(*) from nodes').fetchone()[0],
               'graph_relations':[list(r) for r in catalogue.db.execute('select relation,count(*) from edges group by relation')],
               'indexed_topics':len(catalogue.topics),'profile_topics':len(catalogue.initial['topics']),
               'mapped_profile_topics':len(set(catalogue.initial['topics']) & {t['id'] for t in catalogue.topics}),
               'usable_grade7_now':len(usable),'usable_topic_supply':len({e['topic'] for e in usable}),
               'import_quality':meta['import_report']['question_quality']}
    finally:catalogue.db.close()
    report={'checked_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),'entries':entries,'data_audit':audit}
    (ROOT/'education/.local/reports/tutoring-evolution-deployment.local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':run()
