"""Isolated browser fixture; controlled provider requests only."""
import json,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from model_settings_fixture import Fixture,KEY
from qingqi.storage import Store
from qingqi.provider_models import model_config
from multimodal_fixture import sample_image

f=Fixture();owner=Store(f.root);manager=f.deployment.model_settings(owner)
p={'id':'custom-composer','display_name':'测试供应商','model':'','base_url':f.model_base,'protocol':'openai','supports_image':True,'supports_tools':False,'requires_key':True,'timeout':15,'max_tokens':1600,'json_mode':False,'api_key':KEY,'key_action':'replace'}
c=model_config(p);c['optionSpecs']['reasoningLevel']={'values':['low','high','max'],'map':'{"reasoning_effort": reasoningLevel}'}
p['models']=[{'key':'text','model':'text-local','config':c},{'key':'vision','model':'vision-local','config':c},{'key':'gated','model':'gated-model','config':c}]
v=manager.update_provider({'version':0,'request_id':'seed','operation':'upsert','provider':p})
manager.select({'version':v['version'],'request_id':'defaults','mode':'split','text_provider_id':'custom-composer~text','vision_provider_id':'custom-composer~vision'});owner.close()
class Control(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        raw=json.dumps({'calls':f.calls,'started':f.started.is_set()}).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def do_POST(self):f.release.set();self.send_response(204);self.end_headers()
control=ThreadingHTTPServer(('127.0.0.1',0),Control);threading.Thread(target=control.serve_forever,daemon=True).start()
image=f.root/'equation.png';image.write_bytes(sample_image())
print(json.dumps({'base':f.base,'control':f'http://127.0.0.1:{control.server_port}','image':str(image)}),flush=True)
try:f.instance.serve_forever()
finally:f.instance.server_close();f.model.shutdown();control.shutdown()
