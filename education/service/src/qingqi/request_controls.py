"""Pure imperative scope for student presentation and interaction preferences."""
import re

# “别”只有独立命令或命令上下文才是否定；不能截取“分别/特别/区别”的词内字符。
NEGATION=r'(?:不用|不要|无需|不必|不需要|不想|不许|先不|暂时不|(?:请|先|暂时|千万|你|您|现在|这次|还是|记得|麻烦|也|还|再)别|(?<!\w)别)'


def strip_denied(question,target,*,distance=8):
    pattern=NEGATION+r'[^，,。；;！？\n]{0,'+str(distance)+r'}?(?:'+target+r')'
    return re.sub(pattern,'',question),bool(re.search(pattern,question))


def negated_before(question,start):
    # “不要给完整解答”的“给”曾让否定失效；只跨邻近命令词，不跨句号或其他小问。
    return bool(re.search(NEGATION+r'(?:再|给我|给出|给|告诉我|提供|直接|先|马上|的|这题|本题|正确|标准|参考|最终|\s){0,8}$',question[max(0,start-32):start]))


def answer_directives(question):
    """Ordered current-turn commands; quoted teaching/data text is not permission."""
    def quoted(match):
        prefix=question[max(0,match.start()-16):match.start()]
        # “请解释某句话”仍是引用数据，礼貌前缀不能把被讨论的命令变成答案许可。
        adopted=bool(re.search(r'(?:改成|改为|采用|使用|切换到)\s*$',prefix) and not re.search(r'解释|分析|讨论|含义|什么意思',prefix))
        return match[0] if adopted else ' '*len(match[0])
    text=re.sub(r'“[^”\n]*”|"[^"\n]*"|‘[^’\n]*’|\x27[^\x27\n]*\x27',quoted,question)
    # 完整过程的否定和“直接核对表达式的答案”也属于同一许可边界，恢复时不能换教法。
    target=r'(?:解题(?:过程|步骤)|答案|解答|结果|解法)'
    modifiers=r'(?:这道题|这套题|这题|本题|题目|第\s*[（(]?[1-9一二三四五六七八九]\s*[）)]?(?:小)?(?:问|题)|各问|各题|的|正确|最终|完整|参考|所有|全部|标准|一个|都|全|\s)'
    patterns=[r'(?:给我|给出|告诉我|提供|报出|公布|给)'+modifiers+r'{0,10}'+target,
              r'(?:把|将)?[^，,。；;！？\n]{0,16}?'+target+r'(?:的|都|全|全部|所有|完整|正确|直接|这次|现在|先|\s){0,6}(?:给我|给出|告诉我|提供|公布|报出|说出来)',
              r'(?:只要|只需|需要|我要|我想要|想看)'+modifiers+r'{0,6}'+target,
              r'完整(?:解答|答案|解法)',
              r'(?:直接|马上|请直接)(?:核对|检查)[^，,。；;！？\n]{0,24}?'+target]
    events=[]
    denied=list(re.finditer(r'(?:'+NEGATION+r'|不(?=给|提供|告诉|公布|报出))[^，,。；;！？\n]{0,20}?'+target+r'(?!过程|步骤)',text))
    denied+=list(re.finditer(r'(?:只要|只需|仅要|仅给)[^，,。；;！？\n]{0,10}?(?:提示|线索|启发)',text))
    denied+=list(re.finditer(target+r'[^，,。；;！？\n]{0,6}?(?:'+NEGATION+r'|不(?=给|告诉|报出|公布))[^，,。；;！？\n]{0,6}?(?:给|告诉|报出|公布)',text))
    events.extend({'at':m.end(),'allowed':False,'text':question[m.start():m.end()]} for m in denied)
    for pattern in patterns:
        for m in re.finditer(pattern,text):
            if negated_before(text,m.start()) or any(d.start()<=m.start()<d.end() or d.start()>=m.start() and d.end()<=m.end() for d in denied):continue
            events.append({'at':m.end(),'allowed':True,'text':question[m.start():m.end()]})
    return sorted(events,key=lambda event:(event['at'],not event['allowed']))
