import { Button } from "@zcode/ui/button";
import { ArrowUpRight, BookOpenCheck } from "lucide-react";
import type { LearningOverview } from "./contract.js";
import { displayNodes, priority, statusNames, type DisplayNode } from "./learning-map-state.js";

export function LearningSummary({
  data,
  locked,
  onPractice,
}: {
  data: LearningOverview;
  locked: boolean;
  onPractice: (topic: string) => void;
}) {
  const nodes = displayNodes(data, "mixed");
  const counts = nodes.reduce(
    (value, node) => {
      value[node.status]++;
      return value;
    },
    { ready: 0, review: 0, diagnose: 0, unseen: 0 },
  );
  const known = nodes.length - counts.unseen;
  const focus =
    nodes.find((node) => node.topic_id === data.path.focus && node.available) ||
    nodes
      .filter(
        (node) => node.available && node.topic_id && ["review", "diagnose"].includes(node.status),
      )
      .sort(priority)[0] ||
    nodes.filter((node) => node.available && node.topic_id).sort(priority)[0];
  const byScore = (a: DisplayNode, b: DisplayNode) =>
    (b.score ?? 0) - (a.score ?? 0) || a.title.localeCompare(b.title, "zh-CN");
  const ready = nodes.filter((node) => node.status === "ready");
  const strengths = [
    ...ready.filter((node) => node.metric === "独立首次正确率").sort(byScore),
    ...ready.filter((node) => node.metric === "掌握估计").sort(byScore),
  ].slice(0, 2);
  const focusEvidence = data.topics.find((topic) => topic.id === focus?.topic_id);
  const next = !focus
    ? "先选择一个学习目标。"
    : focusEvidence?.review?.status === "due" && focusEvidence.state !== "needs_practice"
      ? `复测「${focus.title}」，确认能否独立完成。`
      : focus.status === "review"
        ? `先巩固「${focus.title}」，再用新题检验。`
        : focus.status === "ready"
          ? `挑战「${focus.title}」新题，再进阶。`
          : `先诊断「${focus.title}」，确认学习起点。`;
  const source = data.initial
    ? data.summary.attempts
      ? "综合学情"
      : "历史画像"
    : data.summary.attempts
      ? "近期练习"
      : "待建立学情";
  return (
    <section className="edu-card edu-learning-summary" aria-label="学情摘要">
      <div className="edu-summary-heading">
        <h3 className="text-ui-lg font-semibold">
          <BookOpenCheck className="size-4" />
          学情摘要
        </h3>
        <span className="text-ui-xs text-foreground-subtle">
          {source}
          {data.initial?.identity_link === "unlinked_example" ? " · 示例学生" : ""}
        </span>
        {focus?.topic_id && (
          <Button
            size="sm"
            disabled={locked}
            onClick={() => focus.topic_id && onPractice(focus.topic_id)}
          >
            {focus.status === "review"
              ? "开始巩固"
              : focus.status === "ready"
                ? "确认掌握"
                : "开始诊断"}
            <ArrowUpRight />
          </Button>
        )}
      </div>
      <p className="edu-summary-overview text-ui-sm" aria-live="polite">
        {data.summary.attempts
          ? `已完成 ${data.summary.attempts} 次新练习${data.summary.accuracy === null ? "，目前还没有独立首次作答证据" : `，独立首次正确率 ${data.summary.accuracy}%`}。`
          : known
            ? `已有 ${known} 个知识点记录。`
            : "还没有足够的作答证据。"}
        {next}
      </p>
      <p className="edu-summary-strength text-ui-sm">
        <span className="text-foreground-subtle">相对熟悉：</span>
        {strengths.length
          ? strengths.map((node) => node.title).join("、")
          : "仍需更多独立作答确认。"}
      </p>
      {data.review_overview &&
        (data.review_overview.recent_due_count > 0 ||
          data.review_overview.historical_due_count > 0 ||
          data.review_overview.next_at) && (
          <p className="text-ui-xs text-foreground-subtle" data-testid="review-overview">
            {[
              data.review_overview.recent_due_count > 0
                ? `新练习待复测 ${data.review_overview.recent_due_count} 个知识点`
                : null,
              data.review_overview.historical_due_count > 0
                ? `历史复习建议 ${data.review_overview.historical_due_count} 个`
                : null,
              data.review_overview.next_at
                ? `下次复测 ${new Date(data.review_overview.next_at * 1000).toLocaleDateString("zh-CN", { timeZone: "Asia/Shanghai", month: "long", day: "numeric" })}`
                : null,
            ]
              .filter(Boolean)
              .join(" · ")}
          </p>
        )}
      {known > 0 && (
        <div className="edu-summary-states text-ui-xs">
          {(["ready", "review", "diagnose"] as const).map((status) => (
            <span data-status={status} key={status}>
              <i className="edu-map-dot" />
              <strong data-testid={`map-state-${status}`}>{counts[status]}</strong>
              {statusNames[status]}
            </span>
          ))}
          <span className="text-foreground-subtle">
            画像知识点{" "}
            <strong data-testid="profile-topic-count">{data.knowledge_map.profile_topics}</strong>
          </span>
        </div>
      )}
    </section>
  );
}

export function LearningEvidence({ data }: { data: LearningOverview }) {
  return (
    <details className="edu-learning-evidence text-ui-xs text-foreground-subtle">
      <summary>数据依据</summary>
      <div className="edu-learning-evidence-body">
        <p data-testid="initial-source">
          {data.initial?.identity || "当前学情基于本产品中的实际作答。"}
        </p>
        {data.initial && (
          <p>
            历史画像日期 {data.initial.as_of.slice(0, 10)} · 历史作答{" "}
            <strong data-testid="initial-attempts">{data.initial.n_attempts}</strong> 次 ·
            数学历史会话 {data.initial.history_count}{" "}
            条。历史估计用于选择练习，当前水平由新作答确认。
          </p>
        )}
        {data.knowledge_map.profile_topics > data.knowledge_map.mapped_profile_topics && (
          <p>
            {data.knowledge_map.profile_topics - data.knowledge_map.mapped_profile_topics}{" "}
            个画像知识点的教材关系待补充，仍保留历史记录。
          </p>
        )}
        <p>
          新练习作答 <strong data-testid="practice-attempts">{data.summary.attempts}</strong>{" "}
          次，独立首次答对{" "}
          <strong data-testid="independent-correct">{data.summary.independent_correct}</strong>{" "}
          次，独立首次正确率{" "}
          <strong data-testid="independent-accuracy">
            {data.summary.accuracy === null ? "暂无数据" : `${data.summary.accuracy}%`}
          </strong>
          ，辅助与重做{" "}
          <strong data-testid="assisted-attempts">{data.summary.assisted_attempts}</strong>{" "}
          次。与历史画像分别累计。
        </p>
      </div>
    </details>
  );
}
