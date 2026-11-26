"""Complete screenshot chain, legacy clarification recovery and story math through isolated HTTP."""
import http.cookiejar
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from grounded_hint_acceptance import fixture
from qingqi.storage import Store
from qingqi.contracts import Identity


def run():
    root,instance,model,calls=fixture();base=f'http://127.0.0.1:{instance.server_port}'
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with opener.open(base+path,timeout=70) as r:return json.load(r)
    boot=get('/api/bootstrap');student='edu-'+boot['profile']
    def post(path,body):
        req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
        try:
            with opener.open(req,timeout=70) as r:return json.load(r)
        except urllib.error.HTTPError as e:print('HTTP diagnostic:',e.code,e.read().decode(),flush=True);raise
    def teach(session,q,rid):return post('/api/teach',{'session':session,'request':{'request_id':rid,'question':q}})['response']
    checks=[]
    def check(name,ok):
        assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
    owner=Store(root)
    try:
        entry=next(e for e in owner.catalogue.bank.values() if 'mx-8=5x+n' in e['expression'].replace(' ','') and '个位' not in e['expression'])
        a=post('/api/practice/start',{'item_id':entry['id'],'request_id':'start'})
        identity=Identity(student,a['session'])
        initial=teach(a['session'],'能给动画的教学方式吗','initial-animation')
        with owner.db:
            owner.db.execute('UPDATE dialogue_state SET updated=? WHERE student=? AND session=?',(time.time()-4000,student,a['session']))
        story=teach(a['session'],'你不能创建情景故事来教学吗','reported-story')
        check('story_request_after_animation_does_not_clarify_or_detach',story['teaching_action']!='clarify' and not owner.dialogue(identity)['practice_detached'])
        lesson=story['visuals'][0]['algebra_lesson']
        check('requested_story_is_actually_created',lesson['story']['title']=='双记录器的积分故事' and '积分' in story['text'])
        narrative=lesson['story']
        check('story_mapping_uses_original_equation',lesson['equation']=='mx-8=5x+n' and narrative['left']['rate']=='m' and narrative['left']['offset']=='-8' and narrative['right']['rate']=='5' and narrative['right']['offset']=='n')
        check('story_keeps_original_x_domain', '负数' in narrative['domain_note'] and '分数' in narrative['domain_note'])
        from qingqi.identity_animation import render
        probes=render(story['visuals'][0]['params'],14)['algebra_lesson']['steps']
        check('story_has_mathematically_correct_probe_accounts',probes[1]['accounts']==['-8','n'] and probes[2]['accounts']==['m-8','n+5'] and probes[3]['accounts']==['2m-8','n+10'])
        follow=teach(a['session'],'题目就是上一个题目','reported-reference')
        check('previous_problem_correction_resumes_requested_story',follow['teaching_action']!='clarify' and '积分' in follow['text'] and 'mx-8' in follow['text'] and '5x+n' in follow['text'] and len(follow['visuals'])==1 and follow['visuals'][0]['algebra_lesson']['equation']=='mx-8=5x+n')
        check('conversation_reference_and_question_panel_remain_bound',get('/api/session?id='+a['session'])['practice']['id']==a['id'])
        count=len(calls);replay=teach(a['session'],'题目就是上一个题目','reported-reference')
        check('story_replay_does_not_duplicate_model_or_records',replay['cache_hit'] and replay['text']==follow['text'] and len(calls)==count)
        # 模拟此前已接受的错误澄清；只改隔离库，不调用生产清理。
        row=owner.db.execute("SELECT id,state,response FROM runs WHERE json_extract(request,'$.request_id')='reported-reference'").fetchone()
        old=json.loads(row['state']);old.pop('practice_entry',None);old.pop('practice_assignment_id',None);old.pop('presentation',None);old['route']['intents']=['clarify'];old['route']['continuity']='new_task';old['practice_detached']=True
        response=json.loads(row['response']);response['text']='请说一下你想理解的数学概念，或贴出题目和卡住的一步。';response['teaching_action']='clarify';response.pop('visuals',None)
        broken={'verified_work':{'source':'owned_catalogue_question','source_run_id':initial['run_id'],'assignment_id':a['id']},'practice_detached':True,'pending':{'kind':'required_slot','slot':'task_description'},'active_task':{'run_id':row['id'],'intents':['clarify']}}
        with owner.db:
            owner.db.execute('UPDATE runs SET state=?,response=? WHERE id=?',(json.dumps(old),json.dumps(response),row['id']))
            owner.db.execute('UPDATE dialogue_state SET data=?,updated=? WHERE student=? AND session=?',(json.dumps(broken),time.time()-4000,student,a['session']))
        check('legacy_question_panel_recovers_on_open_without_rewriting_history',get('/api/session?id='+a['session'])['practice']['id']==a['id'] and json.loads(owner.db.execute('SELECT response FROM runs WHERE id=?',(row['id'],)).fetchone()[0])['teaching_action']=='clarify')
        recovered=teach(a['session'],'题目还是刚才那道，用故事继续','legacy-recover')
        check('legacy_wrong_detach_recovers_across_temporary_state_expiry',recovered['teaching_action']!='clarify' and owner.dialogue(identity)['verified_work']['assignment_id']==a['id'] and not owner.dialogue(identity)['practice_detached'])
        state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(recovered['run_id'],)).fetchone()[0])
        check('clarification_does_not_cut_off_prior_good_history',any(t['question']=='能给动画的教学方式吗' for t in state['practice_turns']))
        text=teach(a['session'],'先不用故事，也不要动画，给我一点提示','plain')
        check('explicit_plain_request_changes_form_without_changing_question',all(v['kind']!='animation_scene' for v in text.get('visuals',[])) and '积分' not in text['text'] and not owner.dialogue(identity)['practice_detached'])
        repeated=teach(a['session'],'还是同一道题','same-question')
        check('short_reference_without_a_canned_hint_keeps_problem',repeated['teaching_action']!='clarify' and owner.dialogue(identity)['verified_work']['assignment_id']==a['id'])
        teach(a['session'],'取消','cancel')
        bare=teach(a['session'],'A','after-cancel')
        check('cancelled_problem_is_not_resurrected_by_bare_answer',bare['teaching_action']!='confirm' and owner.dialogue(identity)['practice_detached'])
        returned=teach(a['session'],'返回原练习，用情景故事解释','return')
        check('explicit_return_can_reopen_story_for_owned_exercise',returned['teaching_action']!='clarify' and returned['visuals'][0]['algebra_lesson']['equation']==entry['expression'].split('$')[1])
        other=post('/api/sessions',{})['id']
        empty=teach(other,'题目就是上一个题目','empty-reference')
        check('another_session_cannot_borrow_current_question',empty['teaching_action']=='clarify' and not empty.get('visuals'))
        teach(a['session'],'开始新题，解方程4x+1=13，先给提示','new-problem')
        new=teach(a['session'],'题目就是上一道题，继续给提示','new-reference')
        check('real_new_problem_does_not_restore_old_assignment',get('/api/session?id='+a['session'])['practice'] is None and 'mx-8' not in new['text'])
        check('new_problem_does_not_inherit_old_story',owner.dialogue(identity)['presentation']['kind']=='text')
        # 首轮故事、文字切换和TTL均通过既有HTTP命令，不依靠新服务或生产数据修改。
        sibling=next(e for e in owner.catalogue.bank.values() if 'mx-8=5x+n' in e['expression'].replace(' ','') and e['id']!=entry['id'])
        b=post('/api/practice/start',{'item_id':sibling['id'],'request_id':'first-story-start'})
        bid=Identity(student,b['session'])
        first=teach(b['session'],'用情景故事解释，不要给答案','first-story')
        first_lesson=first['visuals'][0]['algebra_lesson']
        check('first_turn_story_is_supported_without_a_hint_setup',first_lesson['story']['left']['expression']=='mx-8' and first_lesson['mode']=='hint')
        with owner.db:owner.db.execute('UPDATE dialogue_state SET updated=? WHERE student=? AND session=?',(time.time()-4000,student,b['session']))
        short=teach(b['session'],'这样讲得不清楚','unkeyword-followup')
        check('ttl_short_feedback_keeps_owned_question_and_story',short['teaching_action']!='clarify' and '积分' in short['text'] and owner.dialogue(bid)['verified_work']['assignment_id']==b['id'])
        check('ttl_preserves_student_answer_limit',owner.dialogue(bid)['no_final_requested'] and '(-3)' not in short['text'])
        plain_story=teach(b['session'],'换成文字故事，不要动画','text-story')
        check('story_can_be_text_without_forcing_an_animation',not plain_story.get('visuals') and '积分' in plain_story['text'])
        other_identity=Identity('unrelated-student',b['session'])
        check('student_ownership_does_not_allow_session_id_to_borrow_problem',owner.current_problem(other_identity) is None)
        from qingqi.identity_animation import specification,render
        variant={'expression':'已知 $ax+6=2x-b$ 对任意x恒成立，求 $(a+b)^4$。'}
        vspec=specification(variant,scenario='scorekeepers');vlesson=render(vspec['params'],14)['algebra_lesson']
        check('negative_parameter_story_preserves_signed_offset',vlesson['story']['left']['offset']=='6' and vlesson['story']['right']['offset']=='-b' and vlesson['steps'][1]['accounts']==['6','-b'] and vlesson['steps'][2]['accounts']==['a+6','-b+2'])
        from qingqi.visual_teaching import validate_binding
        from qingqi.contracts import ContractError
        verified=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(first['run_id'],)).fetchone()[0])
        wrong=json.loads(json.dumps(verified['visual_task']['arguments']));wrong['visuals'][0]['params'].pop('scenario')
        denied=False
        try:validate_binding(wrong,verified)
        except ContractError:denied=True
        check('requested_story_cannot_silently_revert_to_old_plain_animation',denied)
        from qingqi.presentation import story_opening_ok
        check('reported_glm_both_doubled_story_is_rejected',not story_opening_ok('每颗糖果按双份来数，相当于每人手里都翻一倍再合并。'))
        substitution=next(e for e in owner.catalogue.bank.values() if '遮住' in e['expression'] and 'x=6' in e['expression'].replace(' ','') and '2x+y=16' in e['expression'].replace(' ',''))
        c=post('/api/practice/start',{'item_id':substitution['id'],'request_id':'controlled-story-start'})
        controlled=teach(c['session'],'用文字故事帮我理解这道题，不要动画，不要答案','controlled-story')
        check('concept_story_explains_solution_meaning_and_correct_coefficients','方程组的解表示' in controlled['text'] and '蓝色积分计入 $2$ 份，紫色积分计入 $1$ 份' in controlled['text'] and controlled['teaching_action']!='clarify')
        accepted=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(controlled['run_id'],)).fetchone()[0])
        check('false_progress_in_model_story_opening_is_rejected',not accepted['story_opening']['accepted'] and '抓住' not in controlled['text'])
        model.fail_story_opening=True;count=len(calls)
        unavailable=teach(c['session'],'继续用文字故事解释，不用动画','unavailable-opening')
        accepted=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(unavailable['run_id'],)).fetchone()[0])
        check('optional_glm_opening_failure_keeps_correct_math_without_retry',unavailable['teaching_action']!='clarify' and '蓝色积分计入 $2$ 份，紫色积分计入 $1$ 份' in unavailable['text'] and accepted['story_opening'].get('failure_type') and len(calls)==count+1)
        check('compiled_story_fits_current_response_budget',len(unavailable['text'])<=accepted['teaching_plan']['budget']['hard_max'])
        check('story_and_viewing_do_not_become_grades',get('/api/learning')['summary']['attempts']==0)
    finally:owner.close();instance.shutdown();instance.server_close();model.shutdown();model.server_close()
    Path('education/.local/reports/story-context-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'isolated':True},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':run()
