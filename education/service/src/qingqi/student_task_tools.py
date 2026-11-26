"""Read-only student operations use the same Store and the current source reference."""
import hashlib
import json
import re
import time
from .contracts import ToolSpec, ContractError, Denied
from .student_tasks import TOOLS, ARGUMENTS, OUTPUT

SPECS={name:ToolSpec(name,{'recommend':'按当前原题或知识点、学情与近期曝光推荐至多三道题，不返回答案。',
                        'learning_path':'读取或预览当前学生的学习路线，不改写选择。',
                        'learning_dashboard':'读取当前学生的实际学习证据与摘要。'}[kind],ARGUMENTS,OUTPUT,timeout=8.0,version='1') for kind,name in TOOLS.items()}


class StudentTaskTools:
    def __init__(self,store):self.store=store;self.identity=None
    def bind(self,identity):self.identity=identity
    # ZCode RPC 按关键字调用端口；接收同一已校验参数对象，避免查询误落到教学链路。
    def handlers(self):return {name:(lambda kind=kind,**args:self.execute(kind,args)) for kind,name in TOOLS.items()}

    def topic_ids(self,query):
        from .teaching_goals import concepts
        if not query:return set()
        exact={t['id'] for t in self.store.catalogue.topics if t['title']==query}
        if exact:return exact
        named=set(concepts(query))
        return {t['id'] for t in self.store.catalogue.topics if any(w in t['title'] for w in query.split()) or named&set(concepts(t['title']))}

    def execute(self,kind,args):
        if not self.identity or not self.store:raise Denied('student tools require an admitted identity and owner')
        snapshot=self.store.learning_overview(self.identity.student)
        if kind=='recommend':return self.recommend(args,snapshot)
        if kind=='learning_path':return self.path(args,snapshot)
        return self.dashboard(args,snapshot)

    def recommend(self,args,snapshot):
        from .catalogue import complete_item,normalized
        from .learning import public_item
        from .adaptive_learning import eligible_pool,kind,target_level,shape
        from .teaching_goals import concepts
        source=args['source'];catalogue=self.store.catalogue;bank=catalogue.bank
        source_entry=bank.get(source['item_id'])
        question=args['query'] or source['question']
        if not question and not source_entry:return {'kind':'recommend','status':'needs_source','text':'先发一道完整题目，或告诉我想练的知识点，我再推荐对应的题目。','items':[],'evidence':[]}
        named=set(concepts(question));query_topics=self.topic_ids(args['query'])
        if not named and not source_entry:
            from .practice_tutoring import free_entry
            if free_entry('解方程 '+question):named={'方程'}
            elif re.search(r'f\s*\(x\)|y\s*=',question):named={'函数'}
        source_topics=query_topics or (set(source_entry.get('topics',[source_entry['topic']])) if source_entry and not args['query'] else set())
        events=[{'kind':r['kind'],'data':json.loads(r['data']),'at':r['at']} for r in self.store.db.execute('SELECT kind,data,at FROM practice_events WHERE student=? ORDER BY id',(self.identity.student,))]
        pool=eligible_pool(bank,catalogue.initial,events,snapshot['active'],time.time())
        source_stem=normalized(source_entry['expression'] if source_entry else source['question'])
        candidates=[]
        for entry in pool:
            if not complete_item(entry) or entry['id']==source['item_id'] or source_stem and normalized(entry['expression'])==source_stem:continue
            topics=set(entry.get('topics',[entry['topic']]))
            shared=source_topics&topics;terms=named&set(concepts(entry['expression']+' '+entry['title']))
            if query_topics and not shared:continue
            if not shared and not terms:continue
            candidates.append((entry,shared,terms))
        if not candidates:return {'kind':'recommend','status':'no_candidates','text':'暂未找到符合这个知识点和年级的完整新题，可以换一个知识点，或继续讨论原题。','items':[],'evidence':[]}
        profiles={p['id']:p for p in snapshot['topics']}
        seen=[]
        for e in events:
            if e['kind'] in {'recommendations','chat_recommendations'}:
                seen.extend(i['id'] for i in e['data'].get('result',{}).get('items',[]))
        selected=[]
        for slot in range(min(args['count'],len(candidates))):
            available=[row for row in candidates if row[0]['id'] not in {p[0]['id'] for p in selected}]
            fresh=[row for row in available if row[0]['id'] not in seen[-24:]]
            available=fresh or available
            def rank(row):
                entry,shared,terms=row;p=profiles.get(entry['topic'])
                level=1 if args['difficulty']=='easy' else 3 if args['difficulty']=='challenge' else target_level(p) if p else 1
                diversity=sum(12*(shape(entry)==shape(other[0]))+8*(kind(entry)==kind(other[0])) for other in selected)
                similar=18*len(terms)+12*len(shared)+30*(bool(source_entry) and shape(entry)==shape(source_entry))
                tie=hashlib.sha256((source_stem+str(len(seen))+entry['id']).encode()).hexdigest()
                return -similar+abs(entry['level']-level)*14+seen.count(entry['id'])*40+diversity,tie
            selected.append(min(available,key=rank))
        items=[]
        for entry,shared,terms in selected:
            names='、'.join(t['title'] for t in catalogue.topics if t['id'] in shared) or '、'.join(sorted(terms)) or '当前知识点'
            p=profiles.get(entry['topic']);basis='依据已有作答匹配' if p and p.get('attempts') else '从基础练习开始验证'
            reason=f'共同知识：{names}。{basis}，难度：'+{1:'基础',2:'适中',3:'进阶'}.get(entry['level'],'进阶')+'。'
            items.append({**public_item(entry),'reason':reason,'purpose':'相似练习','kind':kind(entry)})
        count=len(items);status='ok' if count==args['count'] else 'limited_supply'
        text=f'找到{count}道对应练习，题目在下方。'+('当前符合条件的新题不足所需数量，按实际供给展示。' if status=='limited_supply' else '可以选择一题开始练习。')
        return {'kind':'recommend','status':status,'text':text,'items':items,'evidence':[{'ref':'bank:'+e['id'],'text':e['title'],'source':e.get('source','版本化数学题库')} for e in items]}

    def path(self,args,snapshot):
        value=snapshot['path']
        if args['query'] or args['minutes']:
            from .learning import learning_projection
            topics=self.store.catalogue.topics
            ids=self.topic_ids(args['query']);match=next((t for t in topics if t['id'] in ids),None)
            if args['query'] and not match:return {'kind':'learning_path','status':'unknown_topic','text':'当前学情与题库没有可对应的这个学习目标，请选择路径地图中的可用知识点。','evidence':[]}
            goal={**snapshot['goal'],'topic':match['id'] if match else snapshot['goal']['topic'],'minutes':args['minutes'] or snapshot['goal']['minutes']}
            events=[{'kind':r['kind'],'data':json.loads(r['data']),'at':r['at']} for r in self.store.db.execute('SELECT kind,data,at FROM practice_events WHERE student=? ORDER BY id',(self.identity.student,))]
            value=learning_projection(goal,events,snapshot['active'],snapshot['summary']['turns'],catalogue=self.store.catalogue,initial=self.store.catalogue.initial)['path']
        def steps(rows):return [{k:s[k] for k in ('topic','title','state','role','reason','has_practice') if k in s} for s in rows[:7]]
        path={k:value[k] for k in ('focus','summary','selected_route','route_title') if k in value}
        path['steps']=steps(value['steps'])
        path['routes']=[{**{k:r[k] for k in ('id','title','summary','available') if k in r},'steps':steps(r.get('steps',[]))} for r in value.get('routes',[])[:4]]
        return {'kind':'learning_path','status':'ok','text':value['summary']+' 这是当前学情下的路线预览，可在学习路径地图中选择链路。','path':path,'evidence':[]}

    def dashboard(self,args,snapshot):
        summary=snapshot['summary']
        ids=self.topic_ids(args['query'])
        if args['query'] and not ids:return {'kind':'learning_dashboard','status':'unknown_topic','text':'当前学情中没有对应知识点的学习证据，请选择学情图谱中的知识点。','evidence':[]}
        selected=sorted((p for p in snapshot['topics'] if not args['query'] or p['id'] in ids),key=lambda p:(p['state']!='needs_practice',-p.get('attempts',0)))[:3]
        topics=[{k:p[k] for k in ('id','title','state','attempts','accuracy') if k in p} for p in selected]
        text=(f"目前记录{summary['attempts']}次作答，其中{summary['independent_attempts']}次是独立作答。" if summary['attempts'] else '目前还没有新的作答证据，已有画像只作为起点参考。')
        if summary['accuracy'] is not None:text+=f"独立作答正确率为{summary['accuracy']}%。"
        return {'kind':'learning_dashboard','status':'ok','text':text+' 下方列出当前需要关注的知识点。','summary':summary,'topics':topics,'evidence':[]}
