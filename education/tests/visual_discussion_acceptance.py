"""CLI/HTTP scenarios for symbolic startup, annotation ownership and real protocol options."""
import copy,json,threading,time,urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.geometry_solver import prepare_geometry,solve_geometry,TOOL
from qingqi.tools import Registry
from qingqi.catalogue import Catalogue
from qingqi.contracts import Identity,Request,Denied
from qingqi.storage import Store
from qingqi.product import server

ARGS={'construction':'right_isosceles_perpendicular','labels':dict(zip('abcdef','ABCDEF')),'scale':'6','ratio':'1/2','parameter':'m','x_variable':'x','y_variable':'y','parts':['midpoint','ratio','function']}
checks=[]
def check(name,value):
    assert value,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)

def run():
    root=fixture_root();c=Catalogue(root)
    start=time.perf_counter();r=Registry(Path(c.config['path']),root=root);ready_ms=round((time.perf_counter()-start)*1000,2)
    try:
        before=prepare_geometry.cache_info().misses
        results=[r.call(TOOL.name,ARGS,{TOOL.name}) for _ in range(2)]
        check('native_geometry_uses_prepared_verified_family_without_deadline_change',TOOL.timeout==12 and before==prepare_geometry.cache_info().misses and all(all(v['result']['proof_checks'].values()) for v in results))
        first=solve_geometry(**ARGS);first['proof_checks'].clear()
        check('immutable_family_does_not_share_student_result',all(solve_geometry(**ARGS)['proof_checks'].values()))
        from qingqi.tutoring_scope import build as scope
        from qingqi.contracts import Route
        from geometry_fixture_data import SOURCE
        scoped=scope(Request.parse({'request_id':'style-tail','question':'直接给第（1）问完整答案，并配合动画演示。'}),SOURCE,None,Route(('tutor',),()),[])
        check('per_part_route_keeps_trailing_animation_request',len(scoped['units'])==1 and scoped['units'][0]['teaching']['plan']['visual']['prefer_animation'])
        scoped=scope(Request.parse({'request_id':'style-group','question':'第二问和第三问都直接给答案，并且用动画展示。'}),SOURCE,None,Route(('tutor',),()),[])
        check('shared_part_group_receives_its_own_presentation_modifier',all(u['teaching']['plan']['visual']['prefer_animation'] for u in scoped['units']))
        scoped=scope(Request.parse({'request_id':'negative-whole','question':'先给我一点提示，不要给完整答案。'}),SOURCE,None,Route(('tutor',),()),[])
        check('negative_full_answer_does_not_expand_to_all_parts',len(scoped['units'])==1 and not scoped['units'][0]['allow_final_answer'])
        from qingqi.teaching_policy import choose
        for text in ('先解释依据，不要给完整解答。','请讨论标记是否合适，不需要给出完整解法。','先说这一步，不要告诉我最终答案。','先解释这条辅助线，无需提供完整解题过程。'):
            decision=choose(Request.parse({'request_id':'negated-explanation','question':text}),Route(('tutor',),()),[])
            assert decision['mode'] in {'explain','heuristic'} and decision['no_final_requested'] and not decision['allow_final_answer'] and not decision['full_walkthrough_requested'],text
        check('negated_solution_with_command_verbs_keeps_default_guided_teaching',True)
        owner=Store(root)
        try:
            rejected=False
            try:owner.visual_source(Identity('edu-math-student','s'),{'run_id':999,'visual_index':0})
            except Denied:rejected=True
            check('unaccepted_or_foreign_annotation_source_rejected',rejected)
        finally:owner.close()
        from qingqi.geometry_animation import scene_at
        p={'side':6,'side_exact':'6','ratio':.5,'ratio_exact':'1/2','labels':ARGS['labels'],'from_x':2,'to_x':2}
        points=scene_at('geometry_motion',p,0)['points']
        check('geometry_coordinate_labels_derived_as_exact_radicals',points[1]['x_tex']==r'6\sqrt{2}' and points[1]['y_tex']=='0' and all('x_tex' in v and 'y_tex' in v for v in points))
        from geometry_product_fixture import Fixture
        from multimodal_fixture import sample_image
        import base64,http.cookiejar
        fixture=Fixture();fixture.start()
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        def get(path):
            with opener.open(fixture.base+path) as response:return json.load(response)
        boot=get('/api/bootstrap')
        def post(path,body):
            req=urllib.request.Request(fixture.base+path,data=json.dumps(body).encode(),headers={'Origin':fixture.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
            with opener.open(req,timeout=45) as response:return json.load(response)
        try:
            photo=post('/api/tutor/images',{'request_id':'annotation-original','name':'source.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})
            session=post('/api/sessions',{})['id']
            first=post('/api/teach',{'session':session,'request':{'request_id':'annotation-source','question':'解这道题','images':[photo['id']]}})
            check('default_socratic_teaching_has_related_geometry',first['response']['teaching_action']=='ask' and first['response']['visuals'][0]['kind']=='coordinates')
            import math
            A,B,C,D,E,F=first['response']['visuals'][0]['points']
            de=(E['x']-D['x'])**2+(E['y']-D['y'])**2;df=(F['x']-D['x'])**2+(F['y']-D['y'])**2
            check('first_question_midpoint_diagram_matches_its_conditions',math.isclose(D['x'],(A['x']+B['x'])/2,abs_tol=1e-9) and math.isclose(D['y'],(A['y']+B['y'])/2,abs_tol=1e-9) and math.isclose(de,df,abs_tol=1e-9))
            from qingqi.projection import project_response
            from qingqi.geometry_animation import scene_at
            wrong=copy.deepcopy(first['response'])
            wrong['visuals'][0]['points']=scene_at('geometry_motion',p,0)['points']
            raw=copy.deepcopy(wrong)
            repaired=project_response(wrong,{'geometry_task':{'arguments':ARGS}})
            aa,bb,cc,dd,*_=repaired['visuals'][0]['points']
            third=copy.deepcopy(wrong);third['visuals'][0]['teaching_part']=3
            retained=project_response(third,{'geometry_task':{'arguments':ARGS}})
            check('historical_midpoint_projection_is_read_only_and_preserves_other_parts',wrong==raw and repaired['run_id']==wrong['run_id'] and math.isclose(dd['x'],(aa['x']+bb['x'])/2,abs_tol=1e-9) and retained['visuals'][0]['points'][3]['x']==raw['visuals'][0]['points'][3]['x'])
            start_calls=len(fixture.calls)
            ref={'run_id':first['response']['run_id'],'visual_index':0}
            annotated=post('/api/teach',{'session':session,'request':{'request_id':'annotation-discuss','question':'我画了辅助线，请结合原题给一个提示。','images':[photo['id']],'visual_context':ref}})
            check('annotation_goes_to_vision_without_retranscribing_or_solving_another_problem',len(fixture.calls)==start_calls+1 and fixture.calls[-1]['input']['annotation_discussion']['visual']['title'] and 'required_output_schema' not in fixture.calls[-1] and annotated['response']['controller']=='glm_vision_text_controller' and annotated['response']['teaching_action']=='ask')
            check('annotation_preserves_original_problem_and_does_not_add_mastery',get('/api/learning')['summary']['attempts']==0 and annotated['session']['messages'][-1]['original_input']['visual_context']==ref)
            denied=False
            try:post('/api/teach',{'session':post('/api/sessions',{})['id'],'request':{'request_id':'foreign-annotation','question':'讨论','images':[photo['id']],'visual_context':ref}})
            except urllib.error.HTTPError as e:denied=e.code==403
            check('another_session_cannot_use_the_visual_reference',denied)
            mixed=post('/api/teach',{'session':session,'request':{'request_id':'mixed-visuals','question':'第一问直接给答案并用动画演示，第三问只给一个提示，也用动画，不要第三问答案。'}})
            check('mixed_visuals_keep_per_part_solution_permission',len(mixed['response']['visuals'])==1 and all(v['params']['lesson_mode']==('solution' if v['template']=='triangle_rotation' else 'hint') for v in mixed['response']['visuals']))
        finally:fixture.close()
        from qingqi.providers import Endpoint,JSONModel
        from qingqi.tutor_images import VISION_SCHEMA
        from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
        bodies=[]
        class Model(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));bodies.append(body)
                raw=json.dumps({'choices':[{'message':{'content':json.dumps({'text':'题干','unclear':False,'note':''},ensure_ascii=False)},'finish_reason':'stop'}]}).encode()
                self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        h=ThreadingHTTPServer(('127.0.0.1',0),Model);threading.Thread(target=h.serve_forever,daemon=True).start()
        try:
            model=JSONModel(Endpoint('vision',f'http://127.0.0.1:{h.server_port}/v1','glm-5.3-flash','',enabled=True,allowed_hosts=('127.0.0.1',),requires_key=False,reasoning_effort='low'))
            model.generate('read',{},VISION_SCHEMA)
            check('other_provider_not_given_glm_specific_options','thinking' not in bodies[-1] and bodies[-1]['reasoning_effort']=='low')
            check('model_duration_is_measured_separately',model.usage[0]['duration_ms']>=0 and model.usage[0]['first_text_ms'] is None)
        finally:h.shutdown();h.server_close()
    finally:r.close();c.close()
    Path('education/.local/reports/visual-discussion-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'readiness_ms':ready_ms,'isolated':True},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':run()
