"""Four-feature acceptance through real HTTP/SQLite. No paid model inference."""
import http.cookiejar
import json
import sys
import threading
import urllib.error
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "service/src"))
from qingqi.agent import PROJECT
from qingqi.product import server
from qingqi.domain_tools import number
from qingqi.learning import BANK

results = []
root = PROJECT / "runs/four-features" / uuid.uuid4().hex
instance = server(0, root=root)
thread = threading.Thread(target=instance.serve_forever, daemon=True)
thread.start()

class Client:
    def __init__(self):
        self.base = f"http://127.0.0.1:{instance.server_port}"
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.csrf = self.get("/api/bootstrap")["csrf"]
    def get(self, path):
        with self.opener.open(self.base + path, timeout=30) as response:
            return json.load(response)
    def post(self, path, body, csrf=True):
        headers = {"Origin": self.base, "Content-Type": "application/json"}
        if csrf:
            headers["X-Qingqi-CSRF"] = self.csrf
        request = urllib.request.Request(self.base + path, data=json.dumps(body).encode(), headers=headers)
        with self.opener.open(request, timeout=30) as response:
            return json.load(response)

def check(name, action):
    action()
    results.append({"name": name, "passed": True})
    print(json.dumps(results[-1]), flush=True)

def expect_error(action, code):
    try:
        action()
    except urllib.error.HTTPError as error:
        assert error.code == code, (error.code, code)
        return
    raise AssertionError("expected rejection")

def assert_that(value):
    assert value

try:
    client = Client()
    overview = client.get("/api/learning")
    item = overview["recommendations"][0]
    check("cold_start_is_diagnostic_and_no_answer", lambda: assert_that(overview["summary"]["attempts"] == 0 and item["reason"] and "answer" not in item and overview["path"]["steps"][0]["state"] == "diagnose"))
    check("invalid_goal_and_csrf_rejected", lambda: (expect_error(lambda: client.post("/api/learning/goal", {"topic": "invented", "minutes": 20}), 400), expect_error(lambda: client.post("/api/learning/goal", {"topic": "fractions", "minutes": 90}), 400), expect_error(lambda: client.post("/api/learning/goal", {"topic": "fractions", "minutes": 20}, False), 403)))
    client.post("/api/learning/goal", {"topic": "fractions", "minutes": 15})
    goal = client.get("/api/learning")
    check("goal_persists_and_path_is_scoped_and_budgeted", lambda: assert_that(goal["goal"]["topic"] == "fractions" and goal["goal"]["minutes"] == 15 and goal["goal"]["route"] == "adaptive" and goal["path"]["today_minutes"] <= 15 and {s["topic"] for s in goal["path"]["steps"]} == {"order", "brackets", "fractions"}))
    start = {"item_id": item["id"], "request_id": "start-one"}
    assignment = client.post("/api/practice/start", start)
    check("start_is_idempotent_and_unsubmitted_answer_hidden", lambda: assert_that(client.post("/api/practice/start", start)["id"] == assignment["id"] and "answer" not in assignment and "answer" not in json.dumps(client.get("/api/learning")["active"])))
    check("start_payload_conflict_rejected", lambda: expect_error(lambda: client.post("/api/practice/start", {**start, "item_id": list(BANK)[-1]}), 403))
    wrong = {"assignment_id": assignment["id"], "request_id": "wrong-one", "answer": "99999"}
    feedback = client.post("/api/practice/answer", wrong)
    check("wrong_attempt_updates_dashboard_and_next_reason", lambda: assert_that(not feedback["correct"] and "correct_answer" not in feedback and client.get("/api/learning")["summary"]["attempts"] == 1 and any(t["attempts"] == 1 for t in client.get("/api/learning")["topics"])))
    check("grade_retry_does_not_double_count", lambda: assert_that(client.post("/api/practice/answer", wrong) == feedback and client.get("/api/learning")["summary"]["attempts"] == 1))
    check("grade_conflict_and_expression_answer_rejected", lambda: (expect_error(lambda: client.post("/api/practice/answer", {**wrong, "answer": "14"}), 403), expect_error(lambda: client.post("/api/practice/answer", {**wrong, "request_id": "copy-expression", "answer": item["expression"]}), 400)))
    hint = client.post("/api/practice/hint", {"assignment_id": assignment["id"], "request_id": "hint-one", "style": "socratic"})
    hint2 = client.post("/api/practice/hint", {"assignment_id": assignment["id"], "request_id": "hint-two", "style": "heuristic"})
    check("socratic_and_heuristic_hints_are_distinct_without_solution", lambda: assert_that(hint["text"] != hint2["text"] and "correct_answer" not in hint and "correct_answer" not in hint2))
    answer = str(number(BANK[item["id"]]["expression"]))
    corrected = client.post("/api/practice/answer", {**wrong, "request_id": "corrected-one", "answer": answer})
    check("hinted_or_corrected_work_is_not_independent_first_success", lambda: assert_that(corrected["correct"] and not corrected["independent_first"] and client.get("/api/learning")["summary"]["independent_correct"] == 0))
    check("assisted_success_keeps_new_foundation_variants", lambda: assert_that(client.get("/api/learning")["recommendations"][0]["level"] == 1 and client.get("/api/learning")["recommendations"][0]["id"] != item["id"]))
    fractional = next(v for v in BANK.values() if number(v["expression"]).denominator > 1)
    fresh = client.post("/api/practice/start", {"item_id": fractional["id"], "request_id": "start-fraction"})
    value = number(fractional["expression"])
    exact = client.post("/api/practice/answer", {"assignment_id": fresh["id"], "request_id": "fraction-answer", "answer": f"{value.numerator * 2}/{value.denominator * 2}"})
    check("equivalent_fraction_is_exact_and_independent", lambda: assert_that(exact["correct"] and exact["independent_first"]))
    check("refresh_restores_active_feedback", lambda: assert_that(client.get("/api/learning")["active"]["id"] == fresh["id"] and client.get("/api/learning")["active"]["feedback"]["correct"]))
    other = Client()
    other.post("/api/profile", {"profile": "student-b"})
    check("learning_and_assignment_student_isolation", lambda: (assert_that(other.get("/api/learning")["summary"]["attempts"] == 0), expect_error(lambda: other.post("/api/practice/answer", {"assignment_id": fresh["id"], "request_id": "other", "answer": "0"}), 403), expect_error(lambda: other.post("/api/practice/hint", {"assignment_id": fresh["id"], "request_id": "other-hint", "style": "explain"}), 403)))
    bracket_items = [x for x in BANK.values() if x["topic"] == "brackets"]
    for index, entry in enumerate([bracket_items[0], bracket_items[1], bracket_items[3]]):
        work = client.post("/api/practice/start", {"item_id": entry["id"], "request_id": f"independent-{index}"})
        client.post("/api/practice/answer", {"assignment_id": work["id"], "request_id": f"independent-answer-{index}", "answer": str(number(entry["expression"]))})
    state = next(t for t in client.get("/api/learning")["topics"] if t["id"] == "brackets")
    check("distinct_independent_evidence_adjusts_learning_path", lambda: assert_that(state["state"] == "steady" and state["independent_correct"] == 3))
    tutor_session = client.post("/api/sessions", {})["id"]
    def teach(question, **fields):
        return client.post("/api/teach", {"session": tutor_session, "request": {"request_id": uuid.uuid4().hex, "question": question, **fields}})["response"]
    socratic = teach("请引导我", expression="2+3*4", mode="socratic")
    heuristic = teach("请给一点提示", expression="2+3*4", mode="heuristic")
    check("tutor_modes_are_distinct_and_do_not_reveal_answer", lambda: assert_that(socratic["text"] != heuristic["text"] and "14" not in heuristic["text"] and heuristic["route"]["teaching"]["mode"] == "heuristic"))
    wrong_short = teach("20", mode="heuristic")
    part = teach("3*4=12", mode="heuristic")
    finished = teach("2+12=14", mode="heuristic")
    recorded = client.get("/api/session?id=" + tutor_session)["messages"][-1]
    check("natural_short_answer_and_steps_keep_original_problem", lambda: assert_that(wrong_short["teaching_action"] == "ask" and part["teaching_action"] == "confirm" and finished["teaching_action"] == "confirm" and recorded["input"]["expression"] == "2+3*4"))
    practice = client.post("/api/practice/start", {"item_id": "decimals-1", "request_id": "tutor-practice-start"})
    client.post("/api/teach", {"session": practice["session"], "request": {"request_id": "tutor-practice-prompt", "question": "请提示我", "expression": "1.2+0.35", "mode": "socratic"}})
    client.post("/api/teach", {"session": practice["session"], "request": {"request_id": "tutor-practice-answer", "question": "1.55"}})
    evidence = client.get("/api/learning")["active"]["feedback"]
    check("verified_tutor_answer_updates_same_practice_evidence", lambda: assert_that(evidence["correct"] and not evidence["independent_first"]))
    for entry in BANK.values():
        number(entry["expression"])
        assert entry["hints"] and entry["socratic"]
    check("entire_seed_bank_is_numeric_and_has_teaching_scaffolds", lambda: assert_that(len(BANK) == 45))
finally:
    instance.shutdown()
    instance.server_close()
    thread.join(2)

target = PROJECT.parent / ".local/reports/four-feature-acceptance.json"
target.write_text(json.dumps({"passed": len(results), "tests": results, "remote_inference": False}, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"passed": len(results), "report": str(target)}, ensure_ascii=False))
