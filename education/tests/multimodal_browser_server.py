import json
from multimodal_fixture import fixture, sample_image, sample_table
from qingqi.web_store import WebStore
from qingqi.catalogue import complete_item

root, visual, product=fixture()
image=root/'equation.png'; image.write_bytes(sample_image())
table=root/'table.png'; table.write_bytes(sample_table())
second=root/'second-equation.png'; second.write_bytes(sample_image('2y + 1 = 7'))
store=WebStore(root)
entry=next(e for e in store.owner.catalogue.bank.values() if complete_item(e) and e['grade']=='7' and e['id'] not in store.owner.catalogue.initial['historical_items'])
a=store.start_practice('edu-math-student',{'item_id':entry['id'],'request_id':'history'})
store.owner.practice_action('edu-math-student','answer',{'assignment_id':a['id'],'request_id':'answer','answer':';'.join(entry['key']['values'])})
store.close()
print(json.dumps({'base':f'http://127.0.0.1:{product.server_port}','image':str(image),'table':str(table),'second':str(second),'history_title':entry['title']}),flush=True)
try: product.serve_forever()
finally: visual.shutdown(); product.server_close()
