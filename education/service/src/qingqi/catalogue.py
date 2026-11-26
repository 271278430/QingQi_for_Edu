"""Read-only exercise catalogue port; mutable student evidence belongs to Store."""
import html
import json
import re
import sqlite3
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

from .contracts import ContractError
from . import learning


class _Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.blocked = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.blocked += 1
        if tag in {"p", "br", "div", "li"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.blocked = max(0, self.blocked - 1)

    def handle_data(self, data):
        if not self.blocked:
            self.parts.append(data)


def text(value):
    parser = _Text()
    parser.feed(str(value or ""))
    return html.unescape("".join(parser.parts)).strip()


def normalized(value):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text(value))).casefold()


def stem_key(value):
    value = text(value)
    value = re.sub(r'^\s*\d+[.、]\s*', '', value)
    value = re.sub(r'[（(]\s*[)）]\s*[。.?？]?\s*$', '', value)
    # 清理句读差异时保留小数点、数学运算和条件文字。
    value = re.sub(r'(?<=[\u4e00-\u9fff])[,.，。]', '，', value)
    return normalized(value)


def missing_context(value):
    # 旧索引只识别“如图”，漏掉“图1/图2”和缺表；标准答案不能补全题干。
    return bool(re.search(r'<img\b|!\[[^\]]*\]\(|如图|图中|图所示|下图|图\s*[（(]|图\s*[0-9一二三四五六七八九十]+|下表|如表|表中|表\s*\d+', str(value), re.I))


def incomplete_formula(value):
    if value.count('$') % 2:
        return True
    for formula in re.findall(r'\$([^$]+)\$', value):
        raw = formula.strip()
        # 源题被截为“4x-”时仍有标准答案；答案存在不能证明题干完整。
        if re.fullmatch(r'[0-9a-zA-Z\s.+*/()\-]+', raw) and re.search(r'[+*/\-]\s*$', raw):
            return True
    return False


def complete_item(entry):
    return all(not missing_context(value) and not incomplete_formula(value) for value in [entry['expression'], *entry.get('options', [])])


def answer_key(answer, options):
    values = answer if isinstance(answer, list) else [answer]
    if not values or any(v is None for v in values):
        return None
    values = [text(v) for v in values]
    if options and len(values) == 1:
        target = normalized(values[0])
        matches = [i for i, opt in enumerate(options) if normalized(opt) == target]
        if not matches and re.fullmatch(r"[a-z]", target) and ord(target) - 97 < len(options):
            matches = [ord(target) - 97]
        if len(matches) == 1:
            return {"kind": "choice", "values": [chr(65 + matches[0])]}
        return None
    pieces = [p.strip() for v in values for p in re.split(r"[;；]", v)]
    try:
        return {"kind": "numeric", "values": [str(learning.numeric_answer(p)) for p in pieces]}
    except ContractError:
        return None


class Catalogue:
    def __init__(self, root):
        registry = Path(root) / "catalogue.local.json"
        self.config = json.loads(registry.read_text(encoding="utf-8-sig")) if registry.exists() else {}
        self.db = None
        self.initial = {}
        self.history = []
        if not self.config:
            self.version, self.topics, self.bank = learning.VERSION, learning.TOPICS, learning.BANK
            self.coverage = "数学数值练习 · 5 个知识点 · 45 道种子题"
            return
        path = Path(self.config["path"]).resolve()
        if not path.is_relative_to(Path(__file__).resolve().parents[2] / "data"):
            raise ContractError("catalogue outside project data")
        self.db = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
        self.db.row_factory = sqlite3.Row
        meta = {r["key"]: json.loads(r["value"]) for r in self.db.execute("SELECT * FROM metadata")}
        self.version = meta["version"]
        if self.version != self.config["version"]:
            raise ContractError("catalogue version mismatch")
        self.initial = meta["student_initial"]
        self.history = meta["student_history"]
        self.topics = meta["topics"]
        paths = {r['id']:r['description'] for r in self.db.execute("SELECT id,description FROM nodes WHERE type='KnowledgeItem'")}
        self.topics = [dict(t, path=paths.get(t['id'], '数学基础')) for t in self.topics]
        self.bank = {r["id"]: json.loads(r["data"]) for r in self.db.execute("SELECT * FROM items WHERE eligible=1")}
        self.coverage = meta["coverage"]
        from .catalogue_variants import fill_arithmetic_gaps
        variants = fill_arithmetic_gaps(self.topics, self.bank, self.version, self.initial['grade'])
        self.bank.update(variants)
        if variants:
            self.coverage += f' · 系统基础变式 {len(variants)} 题（数值规则核验）'

    def close(self):
        if self.db:
            self.db.close()

    def item(self, item_id):
        if item_id not in self.bank:
            raise ContractError("该题暂不支持自动练习核验。")
        return self.bank[item_id]

    def grade(self, entry, submitted):
        if not self.config:
            return learning.numeric_answer(submitted) == learning.number(entry["expression"])
        key = entry["key"]
        if key["kind"] == "choice":
            value = normalized(submitted).upper()
            if value not in [chr(65+i) for i in range(len(entry["options"]))]:
                raise ContractError("请选择一个选项后提交。")
            return value == key["values"][0]
        from .practice_tutoring import identity_answer
        exact=identity_answer(entry)
        if exact:
            # 同一恒等式的“求幂”与“求个位”曾共享自动标注9；数值题按完整所求核验。
            return learning.numeric_answer(submitted)==exact['value']
        values = [str(learning.numeric_answer(p.strip())) for p in re.split(r"[;；]", submitted)]
        if len(values) != len(key["values"]):
            raise ContractError(f"请填写 {len(key['values'])} 个数值，多空之间用分号分隔。")
        return values == key["values"]

    def hint(self, entry, style, count, stage=None):
        if not self.config:
            return learning.hint(entry, style, count)
        if style == "explain":
            from .practice_tutoring import identity_answer,identity_lesson
            exact=identity_answer(entry)
            if exact:
                info=identity_lesson(entry)
                return f"由 ${info['equation']}$ 对任意 $x$ 成立，比较 $x$ 的系数得到 ${info['variable']}={info['known']}$，比较常数项得到 ${info['other_variable']}={info['other_known']}$。\n精确核验的参考结果：$"+exact['display']+'$。'+('本题仅求个位数字。' if exact['units'] else '本题求完整乘方，保留精确式，不用个位数字代替结果。')
            return "题库参考讲解（自动标注）：\n" + (entry["analysis"] or "先核对已知条件，再列出解题步骤。")
        from .practice_tutoring import guidance
        # 提示次数不能冒充学生已完成步骤；有精确分步的题只采用已核验进度。
        return guidance(entry, style, stage or 0,help_level=min(count,2),interactive=style!='heuristic')
