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
