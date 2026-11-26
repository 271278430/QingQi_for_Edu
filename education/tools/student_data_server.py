import json
from student_data_acceptance import fixture_root, server, Store
from qingqi.catalogue import complete_item

root = fixture_root()
store = Store(root)
first = store.learning_overview('edu-math-student')['recommendations'][0]
entry = store.catalogue.item(first['id'])
choices = [e for e in store.catalogue.bank.values() if complete_item(e) and e['grade']=='7' and e['answer_kind']=='choice']
choice = next((e for e in choices if any('$' in option for option in e['options'])), choices[0])
store.close()
instance = server(0, root=root)
print(json.dumps({'base':f'http://127.0.0.1:{instance.server_port}','first':first,'answer':';'.join(entry['key']['values']), 'choice': {'id':choice['id'],'answer':choice['key']['values'][0], 'has_math':any('$' in o for o in choice['options'])}},ensure_ascii=False),flush=True)
instance.serve_forever()
