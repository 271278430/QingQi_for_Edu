"""Versioned numeric seed curriculum and evidence-derived learning projections.

These authored dependencies are independent of unverified graph candidates.
Practice performance is evidence for recommendations, not a mastery diagnosis.
"""
from datetime import datetime, timedelta, timezone
from fractions import Fraction
import re
import time

from .contracts import ContractError
from .domain_tools import number
from .teaching_responses import calculation_steps

VERSION = "numeric_seed_v1"
TOPICS = [
    {"id": "order", "title": "运算顺序", "requires": [], "objective": "分清先乘除、后加减，写出保持原题数值的步骤。"},
    {"id": "brackets", "title": "括号运算", "requires": ["order"], "objective": "先处理括号，并辨认括号改变的计算顺序。"},
    {"id": "fractions", "title": "分数运算", "requires": ["brackets"], "objective": "用通分或分数乘除计算，保持精确分数结果。"},
    {"id": "decimals", "title": "小数运算", "requires": ["order"], "objective": "正确计算有限小数，注意小数位与运算顺序。"},
    {"id": "signed", "title": "有理数符号", "requires": ["brackets"], "objective": "区分负号与减号，判断有理数运算的符号。"},
]
TOPIC_MAP = {t["id"]: t for t in TOPICS}
EXPRESSIONS = {
    "order": ["2+3*4", "18-12/3", "6*3-8/2", "24/3+2*5", "7+4*3-6", "30-4*5+8/2", "48/6*2+3", "5*6-18/3+2", "36/4+3*5-7"],
    "brackets": ["(2+3)*4", "18/(2+4)", "(8-3)*(2+1)", "24/(3+5)+2", "(7+5)/3+4", "(18-6)/(2+1)", "3*(12-(4+2))", "(20-8)/(5-2)+6", "(4+2)*(9-3)/4"],
    "fractions": ["1/2+1/4", "2/3-1/6", "3/4*2/3", "1/2/(3/4)", "2/5+3/10", "(1/2+1/3)*6", "5/6-1/4+1/3", "(3/4-1/8)/(5/8)", "2/3*(9/4)-1/2"],
    "decimals": ["1.2+0.35", "2.5*0.4", "3.6/0.9", "5.2-1.75", "0.8+1.2*3", "(2.4+1.6)/0.5", "7.5/2.5-0.6", "0.25*(3.2+4.8)", "6.4/(0.4*2)+1.25"],
    "signed": ["-3+5", "-4*(-2)", "6-(-3)", "(-12)/3+2", "-2*(3-5)", "(-3)*(-4)-5", "8/(-2)-(-6)", "(-2)*((-3)+7)", "(-18)/(-3)-2*(-4)"],
}
SCAFFOLDS = {
    "order": ("同一个算式里，加减和乘除的优先级有什么不同？你准备先处理哪部分？", ["先圈出乘除部分，暂时保留加减。", "分别算出乘除部分，代回原式；同级运算从左往右。", "检查每次变形是否保留了原式的每一项，再完成最后的加减。"]),
    "brackets": ("如果去掉括号，计算顺序会改变吗？括号在这道题里要求你先做什么？", ["从最内层括号开始，先处理它包住的算式。", "算完括号后，把结果作为一个整体代回，保留外面的运算。", "对照原式检查括号外的乘除与加减有没有遗漏。"]),
    "fractions": ("这一步的分母相同吗？你怎样在不改变分数值的情况下比较或相加？", ["先辨认当前是加减还是乘除；加减时检查是否需要通分。", "加减先通分；除以分数转为乘它的倒数，括号仍优先。", "约分时同时处理分子和分母，最后用最简分数表达结果。"]),
    "decimals": ("你估计结果会落在哪个范围？计算后的小数点位置能通过估算检查吗？", ["加减先对齐小数点；乘除先判断结果的大致大小。", "乘法注意小数位数，除法可把被除数和除数同倍扩大。", "计算后用数量级估算检查小数点，保留原有运算顺序。"]),
    "signed": ("这里的负号表示一个数的符号，还是减法？你能先判断结果的符号吗？", ["先区分一元负号与减号，再判断每部分运算的符号。", "乘除同号得正、异号得负；减去负数等价于加上它的相反数。", "把符号判断和绝对值计算分开，最后代回原式核查。"]),
}
LEVELS = [1, 1, 1, 2, 2, 2, 3, 3, 3]
BANK = {}
for topic in TOPICS:
    for index, expression in enumerate(EXPRESSIONS[topic["id"]]):
        item_id = f'{topic["id"]}-{index + 1}'
        socratic, hints = SCAFFOLDS[topic["id"]]
        BANK[item_id] = {"id": item_id, "topic": topic["id"], "title": topic["title"], "expression": expression,
                         "level": LEVELS[index], "socratic": socratic, "hints": hints, "version": VERSION}

def item(item_id):
    if item_id not in BANK:
        raise ContractError("unknown practice item")
    return BANK[item_id]

def public_item(entry):
    from .catalogue import complete_item
    usable = complete_item(entry)
    return {**{k: entry[k] for k in ("id", "topic", "title", "expression", "level", "version", "options", "answer_kind", "answer_count", "source") if k in entry}, 'usable': usable,
            **({'quality_note': '原题缺少图表或公式已被截断，历史记录保留，请选择一题完整的新练习。'} if not usable else {})}

def numeric_answer(answer):
    # 只接受学生给出的数值；提交原算式不能绕过独立作答，避免将复制题目视作答对。
    value = answer.strip()
    power=re.fullmatch(r'(\([+-]?\d{1,15}(?:/\d{1,15})?\)|[+-]?\d{1,15})\s*\^\s*(\d{1,4})',value)
    if power:
        try:base=Fraction(power[1].strip('()'));exponent=int(power[2])
        except (ValueError,ZeroDivisionError):raise ContractError('乘方底数必须是数值或有效分数。') from None
        if exponent>4096 or max(abs(base.numerator).bit_length(),base.denominator.bit_length())*exponent>4096:
            raise ContractError('乘方超过当前精确核验范围，请使用较小的数值表达式。')
        # -3^2表示-(3^2)，(-3)^2才表示负数底数的平方；不能隐式补括号改写答案。
        return -(abs(base)**exponent) if base<0 and not power[1].startswith('(') else base**exponent
    if not re.fullmatch(r"[+-]?\d{1,15}(?:\.\d{1,15})?(?:\s*/\s*[+-]?\d{1,15})?", value):
        raise ContractError("请填写数值、分数或精确乘方，例如 14、1.5、3/4、(-3)^4。")
    try:
        if "/" in value:
            a, b = value.split("/")
            return Fraction(a.strip()) / Fraction(b.strip())
        return Fraction(value)
    except (ValueError, ZeroDivisionError):
        raise ContractError("分数的分母不能为零。") from None

def hint(entry, style, count):
    if style == "socratic":
        return entry["socratic"] if count == 0 else "你能把自己的理由写成一步等式，再核查等号两边吗？" + entry["socratic"]
    if style == "explain":
        return calculation_steps(entry["expression"])
    return entry["hints"][min(count, len(entry["hints"]) - 1)]

def learning_projection(goal, events, active, turns, *, now=None, catalogue=None, initial=None):
    topics = catalogue.topics if catalogue else TOPICS
    bank = catalogue.bank if catalogue else BANK
    version = catalogue.version if catalogue else VERSION
    initial = initial or {}
    initial_topics = initial.get('topics', {})
    now = time.time() if now is None else now
    grades = [e for e in events if e["kind"] == "answer"]
    by_topic = {t["id"]: [] for t in topics}
    for e in grades:
        for topic_id in e['data'].get('topics', [e['data']['topic']]):
            if topic_id in by_topic:
                by_topic[topic_id].append(e)
    from .learning_evidence import topic_evidence, review_overview
    profiles = [topic_evidence(topic, by_topic[topic['id']], bank, initial_topics.get(topic['id']), now) for topic in topics]
    used = {}
    for e in grades:
        used[e["data"]["item_id"]] = e
    from .adaptive_learning import build_plan, eligible_pool, recommend
    eligible = eligible_pool(bank, initial, events, active, now)
    eligible_topics = {e['topic'] for e in eligible}
    available_levels = {n:min(e['level'] for e in eligible if e['topic'] == n) for n in eligible_topics}
    plan = build_plan(goal, profiles, bank, initial, now, authored=not bool(catalogue and catalogue.config), available_topics=eligible_topics)
    from .learning_branches import branch_plan
    # 综合题关系只用当前年级完整题；跨年级共标签不能支撑学生的拓展链。
    from .catalogue import complete_item
    route_bank = {i:e for i,e in bank.items() if complete_item(e) and (not initial or e.get('grade') == initial.get('grade'))}
    plan = branch_plan(plan, goal, profiles, eligible_topics, now, authored=not bool(catalogue and catalogue.config), bank=route_bank, available_levels=available_levels)
    recommendations, recommendation_info = recommend(goal, profiles, bank, initial, events, active, plan, now, version, public_item)
    china = timezone(timedelta(hours=8))
    today = datetime.fromtimestamp(now, china).date()
    daily = []
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        selected = [e for e in grades if datetime.fromtimestamp(e["at"], china).date() == day]
        daily.append({"date": day.isoformat(), "attempts": len(selected), "correct": sum(e["data"]["correct"] for e in selected)})
    independent = [e for e in grades if e["data"]["independent"]]
    from .learning_map import project_map
    from .catalogue import complete_item
    available = {e['topic'] for e in bank.values() if complete_item(e) and (not initial or e.get('grade') == initial.get('grade'))}
    return {"version": version, "goal": goal, "topics": profiles, "recommendations": recommendations, "active": active,
            "path": {**plan, "today_minutes": min(goal["minutes"] // 5, len(recommendations)) * 5, "today_items": min(goal["minutes"] // 5, len(recommendations))},
            "recommendation_info": recommendation_info,
            "summary": {"turns": turns, "attempts": len(grades), "items": len(used), "independent_attempts": len(independent),
                        "independent_correct": sum(e["data"]["correct"] for e in independent), "assisted_attempts": len(grades) - len(independent),
                        "accuracy": round(100 * sum(e["data"]["correct"] for e in independent) / len(independent)) if independent else None},
            "daily": daily, "coverage": catalogue.coverage if catalogue else "数学数值练习 · 5 个知识点 · 45 道种子题",
            "knowledge_map": project_map(profiles, initial, available), "review_overview": review_overview(profiles),
            **({'initial': {k:initial[k] for k in ('identity','grade','subject','as_of','n_attempts','history_count','identity_link','source')}} if initial else {})}
