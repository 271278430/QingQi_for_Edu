"""Bounded educational goal cues; ownership comes from the authenticated session."""
import re

TOPICS={
    '绝对值':r'绝对值|\|[^|]+\|', '平方根':r'根号|平方根|开方|\\sqrt|sqrt|√',
    '方程':r'方程|移项|代入', '不等式':r'不等式|不等号', '坐标':r'坐标|象限',
    '函数':r'函数', '几何':r'三角形|勾股|平行|垂直|角度', '有理数':r'有理数|正负|加减|数轴|相反数',
    '非负性':r'非负|不能为负', '路程':r'路程|速度|相遇|追及|距离',
    '分数':r'分数|分母|分子',
}
HELP=r'理解|解释|讲解|讲讲|明白|不懂|不会|疑惑|含义|定义|是什么|什么是|什么意思|提示|引导|追问|启发|思路|动画|演示|为什么|画|绘|划线|连起来|连接|辅助线|图示|图像'
NEW=r'开始新题|新问题|换(?:个|道|一道)题|取消|结束当前|换个话题'


def concepts(text):
    return [name for name,pattern in TOPICS.items() if re.search(pattern,text)]


def goal(question):
    if re.search(r'不(?:太)?(?:能)?理解|不(?:太)?明白|理解(?:不了|不清)|(?:帮|想|如何|怎么|能).*理解|含义|定义|概念|是什么|什么是|什么意思|^那.{1,50}呢|再举.*例',question):return 'concept'
    if re.search(r'从哪.*(?:开始|入手)|思路|切入|启发|提示',question):return 'hint'
    if re.search(r'核对|对吗|对不对|检查.*(?:答案|步骤|作答)',question):return 'check'
    if re.search(r'解释|讲解|讲讲|为什么|这一步|不会|不懂|疑惑|动画|演示|故事|情景|情境|场景',question):return 'step'
    if re.search(r'^(?:你好|谢谢|hello|thanks)[。！!\s]*$',question,re.I):return 'chat'
    return 'solve'


def is_teaching(question):
    return bool(concepts(question) and (re.search(HELP,question) or goal(question)=='concept' or re.search(r'直接|结果|计算|求值|算一下',question)))


def separate_calculation(question,entry):
    """Only clear new numeric tasks can override an owned problem."""
    if re.search(r'这(?:题|道题|一步)|原(?:题|练习)|刚才|上一步|返回|回到',question):return False
    compact=lambda s:re.sub(r'\s+', '',s).replace('×','*').replace('÷','/').replace('−','-')
    original=compact(entry.get('expression',''))
    scalar=re.search(r'(?:√\s*\d+(?:\.\d+)?|(?:sqrt|\\sqrt)\s*[({]\s*\d+(?:\.\d+)?\s*[)}]|\|\s*[+-]?\d+(?:\.\d+)?\s*\|)',question)
    if scalar and compact(scalar.group()) not in original:return True
    # 裸选项、单个答案和代数局部变形仍需按所属题核验；只识别完整的新数值运算。
    numeric=bool(re.fullmatch(r'[\d\s.+\-*/×÷()（）]+[。！？!?]?',question.strip()))
    return numeric and bool(re.search(r'[+*/×÷]|\d\s*-\s*\d',question)) and compact(question.rstrip('。！？!?')) != original


def refers_to_owned(question,entry):
    if re.search(NEW,question) or goal(question)=='chat':return False
    if not re.search(HELP,question):return False
    named=set(concepts(question)); known=set(concepts(entry.get('expression','')+' '+entry.get('title','')))
    # 明确询问另一知识领域时启用新教学上下文，不能把旧练习硬套到新概念。
    if named and known and not named&known and re.search(r'什么是|解释.*(?:函数|勾股|坐标|不等式)|讲讲',question):return False
    return bool(named&known or re.search(r'这个|这道题|这题|这一步|刚才|还是|仍然|我.*(?:理解|不懂|不会|疑惑)|解释.*(?:关系|步骤)',question))
