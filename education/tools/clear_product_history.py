"""Explicit operator command; clears the shared product history without touching source data."""
import argparse
import http.cookiejar
import json
import urllib.request
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--execute',action='store_true',required=True)
parser.add_argument('--request-id',required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parents[2]
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
base='http://127.0.0.1:18774'
def get(url):
    with opener.open(url,timeout=30) as r:return json.load(r)
boot=get(base+'/api/bootstrap')
assert boot['can_manage'],'Current deployment account cannot manage this project'
request=urllib.request.Request(base+'/api/settings/history/clear',data=json.dumps({'request_id':args.request_id,'scope':'project'}).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
with opener.open(request,timeout=90) as r:receipt=json.load(r)
checks=[]
for port in (18772,18774):
    entry=f'http://127.0.0.1:{port}'
    get(entry+'/api/bootstrap')
    sessions=get(entry+'/api/sessions')['sessions']
    history=get(entry+'/api/practice/history')['items']
    memory=get(entry+'/api/memory')
    learning=get(entry+'/api/learning')
    assert not sessions and not history and not memory['episodes'] and not memory['facts']
    assert learning['summary']['attempts']==learning['summary']['turns']==0
    assert learning['initial']['history_count']==0 and learning['knowledge_map']['nodes']
    checks.append({'url':entry+'/','sessions':len(sessions),'historical_questions':len(history),'memory_events':len(memory['episodes']),'practice_attempts':learning['summary']['attempts'],'profile_and_graph_retained':True})
report={'receipt':receipt,'checks':checks}
(root/'education/.local/reports/history-clear-production.local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
