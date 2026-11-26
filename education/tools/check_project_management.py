"""Read-only inventory of production data, source management and module ownership."""
from pathlib import Path
import json
import subprocess
import urllib.request
from qingqi.catalogue import Catalogue, complete_item

ROOT=Path(__file__).resolve().parents[2]
REPORTS=ROOT/'education/.local/reports'


def run():
    catalogue=Catalogue(ROOT/'education/service/runs/product')
    try:
        profile=set(catalogue.initial['topics'])
        usable=[v for v in catalogue.bank.values() if complete_item(v) and v['grade']==catalogue.initial['grade']]
        supply={v['topic'] for v in usable}
        data={'graph_nodes':catalogue.db.execute('select count(*) from nodes').fetchone()[0],
              'profile_topics':len(profile),'mapped_profile_topics':len(profile & {t['id'] for t in catalogue.topics}),
              'candidate_items':len(catalogue.bank),'student_ready_items':len(usable),'usable_topic_supply':len(supply),
              'profile_topics_with_ready_items':len(profile & supply)}
    finally:catalogue.close()
    def git(*args):
        return subprocess.run(['git',*args],cwd=ROOT,text=True,encoding='utf-8',capture_output=True,check=True).stdout.splitlines()
    tracked=git('ls-files','--','education','specs/education')
    untracked=git('ls-files','--others','--exclude-standard','--','education','specs/education')
    source={'tracked_education_files':len(tracked),'untracked_education_files':len(untracked),
            'version_baseline_complete':bool(tracked) and not untracked,
            'credential_files_excluded':subprocess.run(['git','check-ignore','education/service/config/models.local.json'],cwd=ROOT,capture_output=True).returncode==0,
            'production_state_excluded':subprocess.run(['git','check-ignore','education/service/runs/product/web.sqlite'],cwd=ROOT,capture_output=True).returncode==0}
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    entries=[]
    for port in (18772,18774):
        with opener.open(f'http://127.0.0.1:{port}/api/health',timeout=10) as r:health=json.load(r)
        entries.append({'url':f'http://127.0.0.1:{port}/','available':health['status']=='ok','demo':health['demo']})
    report={'read_only':True,'data':data,'source_management':source,'entries':entries,
            'ownership':'Agent/Store own accepted state; Web owns drafts/selection; ZCode adapter executes capabilities',
            'gate_scope':'Root architecture policy manages education-runtime/client/web; Python ownership is checked via source bindings and HTTP/browser scenarios, not a complete automatic Python layer checker'}
    REPORTS.mkdir(parents=True,exist_ok=True)
    (REPORTS/'project-management-audit.local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':run()
