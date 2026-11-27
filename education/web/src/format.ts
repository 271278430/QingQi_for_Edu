export const actionLabels: Record<string, string> = {
  ask: "引导思考",
  confirm: "已核验作答",
  explain: "分步讲解",
  give_answer: "参考解答",
  clarify: "需要补充信息",
  greet: "学习对话",
  chat: "学习对话",
  recommend: "相似练习",
  learning_path: "学习路径",
  learning_dashboard: "学情摘要",
};
export const toolLabels: Record<string, string> = {
  course_search: "检索课程图谱",
  course_context: "核对教材关联",
  review_arithmetic: "核验实际步骤",
  difficulty_candidates: "分析学习困难候选",
  worker_course8b: "课程导航 8B",
  worker_difficulty8b: "困难分类 8B",
  worker_review27b: "作答审查 27B",
};
export function errorText(error: unknown) {
  return error instanceof Error ? error.message : "暂时无法完成操作，请重试。";
}
export function retryBlocked(code?: string) {
  return (
    code === "model_unknown" ||
    code === "model_failed" ||
    code === "model_protocol" ||
    code === "model_truncated" ||
    code === "model_changed" ||
    code === "history_changed" ||
    code === "turn_cancelled"
  );
}
export function feedbackText(text: string, stepCount: number) {
  if (!stepCount) return text;
  // 显示层保留旧响应事实，仅把明确的协议编号转为学生可读的步骤编号。
  return text
    .replace(/step:(\d+)/g, (value, index: string) =>
      Number(index) < stepCount ? `第${Number(index) + 1}步作答` : value,
    )
    .replace(/第\s*0\s*步/g, "第1步");
}
export function sourceLabel(source: string) {
  return source === "current_student_work" ? "你本次提交的作答" : source;
}
export function evidenceLabel(ref: string) {
  const step = /^step:(\d+)$/.exec(ref);
  return step ? `第${Number(step[1]) + 1}步作答` : ref;
}
export function timeLabel(value: number) {
  return new Date(value * 1000).toLocaleString("zh-CN", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function historyText(event: { kind: string; text: string }) {
  if (event.kind === "student_work") {
    try {
      const work: unknown = JSON.parse(event.text);
      if (
        work &&
        typeof work === "object" &&
        "expression" in work &&
        "steps" in work &&
        Array.isArray(work.steps)
      ) {
        const lines = work.steps.map((step: unknown, i: number) =>
          step && typeof step === "object" && "equation" in step
            ? `${i + 1}. ${String(step.equation)}`
            : "",
        );
        return [`原题：${String(work.expression)}`, ...lines]
          .filter(Boolean)
          .join("\n");
      }
    } catch {
      // 旧历史可为纯文本；保留原记录，不根据显示转换改写服务端事实。
    }
  }
  return event.text;
}
