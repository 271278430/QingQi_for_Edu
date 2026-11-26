"""Deterministic, explicitly sourced arithmetic variants for empty curriculum topics."""
import hashlib
from .domain_tools import number


def fill_arithmetic_gaps(topics, bank, version, grade):
    from .catalogue import complete_item
    generated = {}
    for topic in topics:
        if topic['title'] not in {'有理数的加法法则','有理数的减法法则'}:
            continue
        # 有原题但缺必要图表仍无可练供给，不能因此跳过基础变式补齐。
        if any(e['topic']==topic['id'] and e.get('grade')==grade and complete_item(e) for e in bank.values()):
            continue
        adding = topic['title']=='有理数的加法法则'
        for index in range(48):
            a = (index * 7 % 23) - 11
            b = (index * 11 % 19) - 9
            operation = '+' if adding else '-'
            expression = f'({a}){operation}({b})'
            answer = str(number(expression))
            style = index % 4
            options = []
            kind, form = 'numeric', '数值计算'
            key = {'kind':'numeric','values':[answer]}
            if style == 0:
                stem = f'计算：${expression}$。'
            elif style == 1:
                stem = (f'上午温度为 ${a}$℃，下午比上午变化 ${b}$℃（正数表示升温，负数表示降温）。下午温度为多少摄氏度？' if adding else
                        f'甲地气温为 ${a}$℃，乙地为 ${b}$℃。甲地气温减去乙地气温的差是多少摄氏度？')
                form = '情境应用'
            elif style == 2:
                stem = f'算式 ${expression}$ 的结果是（ ）。'
                value = int(number(expression))
                options = [str(value+d) for d in [0,1,-1,2]]
                turn = index // 4 % 4
                options = options[turn:] + options[:turn]
                kind, form = 'choice', '选择题'
                key = {'kind':'choice','values':[chr(65+options.index(str(value)))]}
            else:
                stem = f'若 ${a}{operation}x={answer}$，则 $x=$ ______。'
                answer = str(b)
                key = {'kind':'numeric','values':[answer]}
                form = '求缺项'
            digest = hashlib.sha256((version+'|'+topic['id']+'|basic_v1|'+stem).encode()).hexdigest()[:20]
            item_id = 'generated:' + digest
            generated[item_id] = {'id':item_id,'topic':topic['id'],'topics':[topic['id']],'title':topic['title'],'expression':stem,
                                  'grade':grade,'level':1 if style<3 else 2,'version':version,'options':options,'answer_kind':kind,'answer_count':1,
                                  'key':key,'form':form,'source':'系统基础变式（数值规则核验）','analysis':f'依据有理数{ "加法" if adding else "减法"}规则整理条件，按给定顺序计算。参考结果为 {answer}。',
                                  **({'target':'x'} if style==3 else {})}
    return generated
