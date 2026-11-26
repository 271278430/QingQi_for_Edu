import { useEffect, useRef, useState } from "react";
import { Button } from "@zcode/ui/button";
import { Input } from "@zcode/ui/input";
import {
  Check,
  Target,
  Layers,
  RotateCcw,
  ChevronRight,
  LoaderCircle,
  MessageSquare,
  RefreshCw,
} from "lucide-react";
import { errorText, retryBlocked } from "./format.js";
import type {
  EducationService,
  LearningOverview,
  PracticeAssignment,
  PracticeItem,
} from "./contract.js";
import { EducationRequestError } from "./contract.js";
import { MathContent } from "./learning-content.js";
import { LearningDashboard } from "./learning-dashboard.js";
import { LearningRoute } from "./learning-route.js";
type Job = { path: string; body: Record<string, unknown>; nextView?: string };
export function LearningPanel({
  view,
  service,
  onNavigate,
  onTutor,
  onChanged,
}: {
  view: string;
  service: EducationService;
  onNavigate: (view: string) => void;
  onTutor: (assignment: PracticeAssignment) => Promise<void>;
  onChanged: () => void;
}) {
  const [data, setData] = useState<LearningOverview | null>(null);
  const [answer, setAnswer] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [pending, setPending] = useState<Job | null>(null);
  const [reload, setReload] = useState(0);
  const generation = useRef(0);
  const inFlight = useRef(false);
  const currentView = useRef(view);
  useEffect(() => {
    currentView.current = view;
    setStatus("");
  }, [view]);
  useEffect(() => {
    const lifecycle = generation;
    const current = ++lifecycle.current;
    const abort = new AbortController();
    service
      .get<LearningOverview>("/api/learning", abort.signal)
      .then((value) => {
        if (generation.current === current) {
          setData(value);
        }
      })
      .catch((e) => {
        if (!abort.signal.aborted) setError(errorText(e));
      });
    // 生命周期计数器撤销旧学生/页面的请求投影；它不引用 DOM 节点。
    return () => {
      lifecycle.current++;
      abort.abort();
    };
  }, [service, reload]);

  const execute = async (job: Job) => {
    if (inFlight.current) return false;
    inFlight.current = true;
    const current = generation.current;
    setBusy(true);
    setError("");
    setStatus("");
    setPending(job);
    try {
      await service.post(job.path, job.body);
      const value = await service.get<LearningOverview>("/api/learning");
      if (generation.current !== current) return false;
      setData(value);
      setPending(null);
      if (job.path === "/api/learning/goal") setStatus("已保存学习目标。");
      if (job.path === "/api/learning/route") setStatus("已选择路线，个性化练习已重新匹配。");
      if (job.path === "/api/practice/recommendations") setStatus("已更新本组三题。");
      if (job.path === "/api/practice/answer") setAnswer("");
      onChanged();
      // 用户在等待中主动切页后，迟到结果只能更新数据，不能抢回导航。
      if (currentView.current === view) {
        if (job.path === "/api/practice/start" && view !== "practice") onNavigate("practice");
        if (job.nextView) onNavigate(job.nextView);
      }
      return true;
    } catch (e) {
      if (generation.current === current) {
        setError(errorText(e));
        // 服务明确拒绝输入时允许更正；网络未知结果保留原编号，防止重复统计。
        if (
          e instanceof EducationRequestError &&
          e.code !== "invalid_response" &&
          ([400, 403, 422].includes(e.status) || retryBlocked(e.code))
        )
          setPending(null);
      }
      return false;
    } finally {
      inFlight.current = false;
      if (generation.current === current) setBusy(false);
    }
  };
  const start = (item: PracticeItem) =>
    void execute({
      path: "/api/practice/start",
      body: { item_id: item.id, request_id: crypto.randomUUID() },
    });
  const requestHint = (style: string) => {
    if (data?.active)
      void execute({
        path: "/api/practice/hint",
        body: {
          assignment_id: data.active.id,
          style,
          request_id: crypto.randomUUID(),
        },
      });
  };
  const locked = busy || Boolean(pending);
  const errorBanner = error && (
    <div className="edu-card mb-4 text-ui-sm" role="alert">
      <p>{error}</p>
      {pending && (
        <Button
          className="mt-3"
          disabled={busy}
          variant="outline"
          onClick={() => void execute(pending)}
        >
          <RefreshCw />
          重试此操作
        </Button>
      )}
      {!pending && (
        <Button
          className="mt-3"
          variant="outline"
          onClick={() => {
            setError("");
            setReload((value) => value + 1);
          }}
        >
          <RefreshCw />
          重新读取学习记录
        </Button>
      )}
    </div>
  );
  if (!data)
    return (
      <div className="edu-page">
        {errorBanner || (
          <p role="status" className="text-ui-base">
            正在读取学习记录…
          </p>
        )}
      </div>
    );
  const active = data.active;
  const activeUsable = active?.item.usable !== false;
  const focusTitle = data.topics.find((item) => item.id === data.path.focus)?.title || "当前目标";
  const nextItem = data.recommendations[0];
  const purposeIcons = [Target, RotateCcw, Layers];
  const recommendations = (
    <div className="grid gap-3 xl:grid-cols-3" aria-label="本组推荐">
      {data.recommendations.map((item, index) => (
        <article
          className="edu-card flex min-w-0 flex-col"
          key={item.id}
          data-testid="recommendation-card"
        >
          <div className="mb-3 flex flex-wrap items-center gap-2">
            <span className="edu-status text-ui-sm text-brand">
              {(() => {
                const Icon = purposeIcons[index] || Target;
                return <Icon className="size-4" />;
              })()}
              {index + 1} · {item.purpose || "匹配练习"}
            </span>
            <span className="text-ui-xs text-foreground-subtlest">{item.kind}</span>
          </div>
          <p className="text-ui-sm text-foreground-subtle">
            {item.title} · {item.level === 1 ? "基础" : item.level === 2 ? "进阶" : "综合"}
          </p>
          <div className="my-3">
            <MathContent content={item.expression} />
          </div>
          {item.options?.length ? (
            <p className="mb-3 text-ui-xs text-foreground-subtlest">开始练习后查看选项并作答</p>
          ) : null}
          <p className="mb-4 text-ui-sm text-foreground-subtle">{item.reason}</p>
          <Button
            className="mt-auto self-start"
            variant={index === 0 ? "default" : "outline"}
            disabled={locked}
            onClick={() => start(item)}
          >
            练这道题
            <ChevronRight />
          </Button>
        </article>
      ))}
      {!data.recommendations.length && (
        <p className="text-ui-base text-foreground-subtle">
          当前知识点暂没有可用的新题。可以选择其他学习目标，或到复习间隔后再练。
        </p>
      )}
    </div>
  );
  return (
    <div className="edu-page">
      {errorBanner}
      {status && (
        <p className="mb-4 text-ui-sm" role="status">
          {status}
        </p>
      )}
      {view === "path" && (
        <LearningRoute
          key={`${data.goal.topic}:${data.goal.minutes}:${data.path.selected_route}:${data.path.focus}`}
          data={data}
          locked={locked}
          onStart={start}
          onGoal={(topic, minutes) =>
            execute({
              path: "/api/learning/goal",
              body: { topic, minutes },
            })
          }
          onRoute={(route) =>
            void execute({
              path: "/api/learning/route",
              body: { route, request_id: crypto.randomUUID() },
            })
          }
        />
      )}
      {view === "dashboard" && (
        <LearningDashboard
          data={data}
          locked={locked}
          onNavigate={onNavigate}
          onPractice={(target) =>
            void execute({
              path: "/api/learning/goal",
              body: { topic: target, minutes: data.goal.minutes },
              nextView: "practice",
            })
          }
        />
      )}
      {view === "practice" && (
        <>
          <h2 className="text-ui-xl font-semibold">个性化练习</h2>
          <p className="my-3 text-ui-base text-foreground-subtle">每组三题，会随你的新作答调整。</p>
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3 text-ui-sm">
            <span className="edu-status" data-testid="practice-selected-route">
              当前路线：{data.path.route_title}
            </span>
            <Button variant="ghost" size="sm" onClick={() => onNavigate("path")}>
              更换路线
            </Button>
          </div>
          {active && (
            <section className="edu-card mb-6" aria-label="当前练习">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h3 className="text-ui-lg font-semibold">当前练习</h3>
                <span className="edu-status text-ui-xs">{active.item.title}</span>
              </div>
              <div className="my-5">
                <MathContent content={active.item.expression} />
              </div>
              <p className="mb-3 text-ui-sm text-foreground-subtle">
                {active.item.answer_kind === "choice"
                  ? "选择一个选项，也可以先和导师讨论思路。"
                  : `写出数值、分数或精确乘方${(active.item.answer_count || 1) > 1 ? "，多空按题目顺序用分号分隔" : ""}，也可以先和导师讨论步骤。`}
              </p>
              {active.item.source && (
                <details className="mb-3 text-ui-xs text-foreground-subtle">
                  <summary className="cursor-pointer">题目来源</summary>
                  <p className="mt-2">{active.item.source}</p>
                </details>
              )}
              {!activeUsable && (
                <p
                  role="status"
                  className="my-3 rounded-md bg-warning-surface p-3 text-ui-sm text-warning-surface-foreground"
                >
                  {active.item.quality_note}
                </p>
              )}
              {activeUsable && !active.feedback?.correct && (
                <form
                  className="flex flex-wrap gap-3"
                  onSubmit={(e) => {
                    e.preventDefault();
                    void execute({
                      path: "/api/practice/answer",
                      body: {
                        assignment_id: active.id,
                        answer: answer.trim(),
                        request_id: crypto.randomUUID(),
                      },
                    });
                  }}
                >
                  {active.item.answer_kind === "choice" ? (
                    <fieldset className="w-full space-y-3" disabled={locked}>
                      <legend className="mb-2 text-ui-sm">我的选项</legend>
                      {active.item.options?.map((option, index) => (
                        <label
                          key={index}
                          className="flex min-w-0 items-start gap-3 rounded-md border border-border p-3 text-ui-base"
                        >
                          <input
                            type="radio"
                            name="practice-choice"
                            value={String.fromCharCode(65 + index)}
                            checked={answer === String.fromCharCode(65 + index)}
                            onChange={(e) => setAnswer(e.target.value)}
                            aria-label={`${String.fromCharCode(65 + index)} ${option}`}
                          />
                          <span>{String.fromCharCode(65 + index)}.</span>
                          <MathContent content={option} />
                        </label>
                      ))}
                    </fieldset>
                  ) : (
                    <Input
                      className="edu-field text-mobile-input-safe min-w-0 flex-1"
                      aria-label="我的答案"
                      placeholder={
                        (active.item.answer_count || 1) > 1 ? "例如：2；3/4" : "例如：14、1.5、3/4"
                      }
                      value={answer}
                      maxLength={120}
                      onChange={(e) => setAnswer(e.target.value)}
                      disabled={locked}
                      required
                    />
                  )}
                  <Button disabled={locked || !answer.trim()}>
                    <Check />
                    核对答案
                  </Button>
                </form>
              )}
              {active.feedback && (
                <div
                  className={`mt-4 rounded-md p-4 ${active.feedback.correct ? "bg-success-surface text-success-surface-foreground" : "bg-warning-surface text-warning-surface-foreground"}`}
                  aria-live="polite"
                >
                  <p className="text-ui-base font-medium">
                    {active.feedback.correct ? "答案正确" : "再想一步"}
                  </p>
                  <p className="mt-2 text-ui-sm">你的答案：{active.feedback.submitted}</p>
                  <p className="mt-2 text-ui-sm">{active.feedback.text}</p>
                  {active.feedback.correct && (
                    <p className="mt-2 text-ui-sm text-foreground-subtle">
                      {active.feedback.independent_first
                        ? "独立首次答对，已更新学习记录。"
                        : "本题使用过提示或辅导，计入辅助练习。"}
                    </p>
                  )}
                  {active.feedback.correct && nextItem && (
                    <Button className="mt-4" disabled={locked} onClick={() => start(nextItem)}>
                      继续下一题
                      <ChevronRight />
                    </Button>
                  )}
                </div>
              )}
              <div className="mt-4 flex flex-wrap gap-2">
                {activeUsable && !active.feedback?.correct && (
                  <>
                    <Button
                      variant="outline"
                      disabled={locked}
                      onClick={() => requestHint("heuristic")}
                    >
                      给我一点提示
                    </Button>
                    <Button
                      variant="ghost"
                      disabled={locked}
                      onClick={() => void onTutor(active).catch((e) => setError(errorText(e)))}
                    >
                      <MessageSquare />
                      和导师一起做
                    </Button>
                  </>
                )}
                {activeUsable && active.feedback && (
                  <Button variant="ghost" disabled={locked} onClick={() => requestHint("explain")}>
                    查看分步讲解
                  </Button>
                )}
              </div>
              {active.guidance && (
                <div
                  className="mt-4 rounded-md bg-secondary p-4 text-ui-base"
                  role="status"
                  aria-label="练习提示"
                >
                  <MathContent content={active.guidance} />
                </div>
              )}
            </section>
          )}
          <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
            <div>
              <h3 className="text-ui-lg font-semibold">接下来练什么</h3>
              <p className="mt-1 text-ui-sm text-foreground-subtle">当前重点：{focusTitle}</p>
            </div>
            <Button
              variant="outline"
              disabled={locked}
              onClick={() =>
                void execute({
                  path: "/api/practice/recommendations",
                  body: { request_id: crypto.randomUUID() },
                })
              }
            >
              <RefreshCw />
              换一组
            </Button>
          </div>
          {data.recommendation_info?.message &&
            data.recommendations.length < data.recommendation_info.requested && (
              <p className="mb-4 text-ui-sm text-foreground-subtle">
                {data.recommendation_info.message}
              </p>
            )}
          {recommendations}
        </>
      )}
      {busy && (
        <p className="mt-3 flex items-center gap-2 text-ui-sm" role="status">
          <LoaderCircle className="edu-spin size-4" />
          正在保存学习记录…
        </p>
      )}
    </div>
  );
}
