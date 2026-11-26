import { useState, type ReactNode, type ComponentProps } from "react";
import { Button } from "@zcode/ui/button";
import { ArrowRight, BookOpen } from "lucide-react";
import type { HistoricalPractice, StudentTask, Response } from "./contract.js";
import { MathContent } from "./learning-content.js";
import { errorText, feedbackText, actionLabels } from "./format.js";
import { TeachingVisuals } from "./teaching-visuals.js";

export function tutoringLabel(response: Response) {
  return response.task_notice
    ? "任务未完成"
    : response.route?.teaching?.label || actionLabels[response.teaching_action];
}

export function TutorReplyContent({
  response,
  stepCount,
  theme,
  locked,
  onRepeat,
  onPick,
  onNavigate,
  onAnnotate,
}: {
  response: Response;
  stepCount: number;
  theme?: ComponentProps<typeof MathContent>["theme"];
  locked: boolean;
  onRepeat: () => void;
  onPick: (item: HistoricalPractice) => Promise<void>;
  onNavigate: (view: "path" | "dashboard") => void;
  onAnnotate: ComponentProps<typeof TeachingVisuals>["onAnnotate"];
}) {
  return (
    <StudentTaskNotice
      notice={response.task_notice}
      locked={locked}
      onRepeat={onRepeat}
    >
      <MathContent
        theme={theme}
        content={feedbackText(response.text, stepCount)}
      />
      <TeachingVisuals
        theme={theme}
        visuals={response.visuals}
        runId={response.run_id}
        onAnnotate={onAnnotate}
        locked={locked}
      />
      <StudentTaskResults
        tasks={response.student_tasks}
        locked={locked}
        onPick={onPick}
        onNavigate={onNavigate}
      />
    </StudentTaskNotice>
  );
}

export function StudentTaskNotice({
  notice,
  locked,
  onRepeat,
  children,
}: {
  notice?: string;
  locked: boolean;
  onRepeat: () => void;
  children: ReactNode;
}) {
  if (!notice) return children;
  return (
    <div className="space-y-3">
      <p role="status" className="text-ui-sm text-foreground-subtle">
        {notice}
      </p>
      <Button size="sm" variant="outline" disabled={locked} onClick={onRepeat}>
        重新执行这条请求
      </Button>
      <details className="text-ui-sm">
        <summary className="cursor-pointer text-foreground-subtle">
          查看原回复
        </summary>
        <div className="mt-3">{children}</div>
      </details>
    </div>
  );
}

export function StudentTaskResults({
  tasks,
  locked,
  onPick,
  onNavigate,
}: {
  tasks?: StudentTask[];
  locked: boolean;
  onPick: (item: HistoricalPractice) => Promise<void>;
  onNavigate: (view: "path" | "dashboard") => void;
}) {
  const [choosing, setChoosing] = useState(false);
  const [error, setError] = useState("");
  return tasks?.map((task, index) => (
    <section
      key={`${task.kind}-${index}`}
      aria-label={
        task.kind === "recommend"
          ? "推荐练习"
          : task.kind === "learning_path"
            ? "学习路线预览"
            : "当前学情摘要"
      }
      className="mt-4 space-y-3"
    >
      {task.kind === "recommend" &&
        task.items.map((item, i) => (
          <article key={item.id} className="edu-card min-w-0">
            <div className="mb-3 flex flex-wrap items-center gap-2 text-ui-sm text-foreground-subtle">
              <BookOpen className="size-4" />
              <span>
                练习 {i + 1} · {item.title}
              </span>
            </div>
            <MathContent content={item.expression} />
            {item.options?.map((option, n) => (
              <MathContent key={n} content={option} />
            ))}
            <p className="mt-3 text-ui-sm text-foreground-subtle">
              {item.reason}
            </p>
            <Button
              className="mt-3"
              size="sm"
              disabled={locked || choosing || item.usable === false}
              onClick={async () => {
                setChoosing(true);
                setError("");
                try {
                  await onPick({
                    item,
                    session: null,
                    source: "对话推荐",
                    correct: null,
                    last_at: null,
                  });
                } catch (e) {
                  setError(errorText(e));
                } finally {
                  setChoosing(false);
                }
              }}
            >
              开始练习
              <ArrowRight className="size-4" />
            </Button>
          </article>
        ))}
      {task.kind === "learning_dashboard" && task.summary && (
        <div className="edu-card">
          <p className="text-ui-sm">
            独立作答 {task.summary.independent_attempts} 次 · 正确率{" "}
            {task.summary.accuracy === null
              ? "待积累"
              : `${task.summary.accuracy}%`}
          </p>
          {task.topics?.map((topic) => (
            <p
              className="mt-2 text-ui-sm text-foreground-subtle"
              key={topic.id}
            >
              {topic.title} ·{" "}
              {topic.attempts ? `${topic.attempts} 次作答` : "等待新作答验证"}
            </p>
          ))}
          <Button
            className="mt-3"
            size="sm"
            variant="outline"
            disabled={locked || choosing}
            onClick={() => onNavigate("dashboard")}
          >
            查看学情图谱
            <ArrowRight />
          </Button>
        </div>
      )}
      {task.kind === "learning_path" && task.path && (
        <div className="edu-card">
          <p className="font-medium text-ui-sm">
            {task.path.route_title || "当前学习路线"}
          </p>
          <ol className="mt-3 space-y-3 border-l border-border pl-4">
            {task.path.steps.map((step, n) => (
              <li key={`${step.topic}-${n}`} className="text-ui-sm">
                <p>{step.title}</p>
                <p className="text-foreground-subtle">{step.reason}</p>
              </li>
            ))}
          </ol>
          <Button
            className="mt-3"
            size="sm"
            variant="outline"
            disabled={locked || choosing}
            onClick={() => onNavigate("path")}
          >
            打开路径地图
            <ArrowRight />
          </Button>
        </div>
      )}
      {error && (
        <p role="alert" className="text-ui-sm text-destructive">
          {error}
        </p>
      )}
    </section>
  ));
}
