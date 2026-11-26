import { useState, type CSSProperties } from "react";
import { Button } from "@zcode/ui/button";
import { Input } from "@zcode/ui/input";
import {
  Check,
  CircleHelp,
  Flag,
  GraduationCap,
  Navigation,
  Route,
  Settings2,
  X,
} from "lucide-react";
import { EducationSelect } from "./controls.js";
import type { LearningOverview, PracticeItem } from "./contract.js";

const labels: Record<string, string> = {
  diagnose: "待诊断",
  needs_practice: "需巩固",
  practicing: "练习中",
  steady: "近期稳定",
  waiting: "先修待练",
};
export function LearningRoute({
  data,
  locked,
  onStart,
  onGoal,
  onRoute,
}: {
  data: LearningOverview;
  locked: boolean;
  onStart: (item: PracticeItem) => void;
  onGoal: (topic: string, minutes: number) => Promise<boolean>;
  onRoute: (route: string) => void;
}) {
  const [topic, setTopic] = useState(data.goal.topic);
  const [minutes, setMinutes] = useState(String(data.goal.minutes));
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [selected, setSelected] = useState<{ route: string; topic: string } | null>(null);
  const routes = data.path.routes;
  const detail = routes
    .find((r) => r.id === selected?.route)
    ?.steps.find((s) => s.topic === selected?.topic);
  const evidence = data.topics.find((t) => t.id === detail?.topic);
  const destination = data.topics.find((t) => t.id === data.goal.topic)?.title || "当前目标";
  const next = data.recommendations[0];
  const stageCount = Math.max(1, ...routes.map((r) => r.steps.length));
  const rowY = (index: number) =>
    routes.length === 1 ? 48 : 18 + (index * 60) / (routes.length - 1);
  const stageX = (index: number) => (stageCount === 1 ? 65 : 32 + (index * 57) / (stageCount - 1));
  const mobileX = (index: number) => ((index + 0.5) * 100) / routes.length;
  const mobileY = (index: number) => 32 + (index * 52) / Math.max(1, stageCount - 1);
  const position = (x: number, y: number, mx: number, my: number) =>
    ({
      "--branch-x": `${x}%`,
      "--branch-y": `${y}%`,
      "--branch-mx": `${mx}%`,
      "--branch-my": `${my}%`,
    }) as CSSProperties;
  return (
    <section className="edu-branch-map text-ui-base" aria-label="学习路线地图">
      <header className="edu-branch-header">
        <div className="min-w-0">
          <h2 className="flex items-center gap-2 text-ui-xl font-semibold">
            <Route className="size-5" />
            学习路径
          </h2>
          <p className="mt-2 text-ui-sm text-foreground-subtle">
            选择一条适合你的路线，个性化练习会跟随它匹配。
          </p>
        </div>
        <details
          className="edu-branch-settings"
          open={settingsOpen}
          onToggle={(e) => setSettingsOpen(e.currentTarget.open)}
          onKeyDown={(e) => {
            if (e.key === "Escape") setSettingsOpen(false);
          }}
        >
          <summary className="flex cursor-pointer items-center gap-2 text-ui-sm">
            <Settings2 className="size-4" />
            调整目标与学习时间
          </summary>
          <form
            onSubmit={async (e) => {
              e.preventDefault();
              // 保存成功由新快照确认；失败保留表单和输入，避免遮挡下一步操作。
              if (await onGoal(topic, Number(minutes))) setSettingsOpen(false);
            }}
          >
            <label className="text-ui-sm">
              学习目标
              <EducationSelect
                label="学习目标"
                value={topic}
                onValueChange={setTopic}
                disabled={locked}
                options={data.topics
                  .filter(
                    (t) =>
                      t.id === data.goal.topic ||
                      data.knowledge_map.nodes.some((n) => n.topic_id === t.id && n.available),
                  )
                  .map((t) => ({ value: t.id, label: t.title }))}
              />
            </label>
            <label className="text-ui-sm">
              每日学习分钟
              <Input
                aria-label="每日学习分钟"
                className="text-mobile-input-safe"
                type="number"
                min={10}
                max={45}
                value={minutes}
                onChange={(e) => setMinutes(e.target.value)}
                disabled={locked}
                required
              />
            </label>
            <Button disabled={locked}>保存学习目标</Button>
          </form>
          {settingsOpen && (
            <Button type="button" variant="ghost" onClick={() => setSettingsOpen(false)}>
              收起设置
            </Button>
          )}
        </details>
      </header>
      <div className="edu-branch-toolbar">
        <span className="flex min-w-0 items-center gap-2 text-ui-sm">
          <Flag className="size-4 shrink-0" />
          目标：<strong data-testid="route-destination">{destination}</strong>
        </span>
        <span className="text-ui-xs text-foreground-subtle">每日 {data.goal.minutes} 分钟</span>
        <Button disabled={locked || !next} onClick={() => next && onStart(next)}>
          开始今日练习
        </Button>
      </div>
      <div
        className="edu-branch-canvas"
        role="group"
        aria-label="可选学习路线"
        style={
          {
            "--route-columns": stageCount,
            "--route-mobile-height": `${Math.max(900, stageCount * 240)}px`,
          } as CSSProperties
        }
      >
        <svg
          className="edu-branch-lines edu-branch-desktop"
          viewBox="0 0 1000 600"
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          {routes.map((r, ri) =>
            r.steps.map((s, si) => {
              const x1 = si === 0 ? 70 : stageX(si - 1) * 10,
                y1 = si === 0 ? 300 : rowY(ri) * 6;
              const x2 = stageX(si) * 10,
                y2 = rowY(ri) * 6;
              return (
                <path
                  key={`${r.id}:${s.topic}`}
                  data-selected={r.id === data.path.selected_route}
                  d={`M ${x1} ${y1} C ${(x1 + x2) / 2} ${y1}, ${(x1 + x2) / 2} ${y2}, ${x2} ${y2}`}
                  vectorEffect="non-scaling-stroke"
                />
              );
            }),
          )}
        </svg>
        <svg
          className="edu-branch-lines edu-branch-mobile"
          viewBox="0 0 400 900"
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          {routes.map((r, ri) =>
            r.steps.map((s, si) => {
              const x1 = si === 0 ? 200 : mobileX(ri) * 4,
                y1 = si === 0 ? 90 : mobileY(si - 1) * 9;
              const x2 = mobileX(ri) * 4,
                y2 = mobileY(si) * 9;
              return (
                <path
                  key={`${r.id}:${s.topic}`}
                  data-selected={r.id === data.path.selected_route}
                  d={`M ${x1} ${y1} C ${x1} ${(y1 + y2) / 2}, ${x2} ${(y1 + y2) / 2}, ${x2} ${y2}`}
                  vectorEffect="non-scaling-stroke"
                />
              );
            }),
          )}
        </svg>
        <div className="edu-branch-origin" style={position(7, 50, 50, 10)}>
          <span>
            <GraduationCap className="size-6" />
          </span>
          <p className="mt-2 text-ui-sm">我的学情</p>
        </div>
        {routes.map((r, ri) => (
          <div key={r.id}>
            <button
              type="button"
              className="edu-branch-choice text-ui-sm"
              style={position(20, rowY(ri) - 8, mobileX(ri), 24)}
              data-testid="route-choice"
              data-route={r.id}
              aria-label={`选择${r.title}路线`}
              title={r.description}
              aria-pressed={r.id === data.path.selected_route}
              disabled={locked || !r.steps.some((s) => s.has_practice)}
              onClick={() => {
                if (r.id !== data.path.selected_route) onRoute(r.id);
              }}
            >
              {r.id === data.path.selected_route && <Check className="size-3.5" />}
              {r.title}
            </button>
            {r.steps.map((step, si) => {
              const current = r.id === data.path.selected_route && step.topic === data.path.focus;
              const Icon = current
                ? Navigation
                : step.review?.status === "due"
                  ? CircleHelp
                  : step.state === "steady"
                    ? Check
                    : step.topic === data.goal.topic
                      ? Flag
                      : CircleHelp;
              return (
                <button
                  key={step.topic}
                  type="button"
                  className="edu-branch-node"
                  style={position(stageX(si), rowY(ri), mobileX(ri), mobileY(si))}
                  data-testid="route-station"
                  data-route={r.id}
                  data-topic={step.topic}
                  data-state={step.state}
                  aria-current={current ? "step" : undefined}
                  aria-label={`查看${step.title}（${r.title}）学习详情`}
                  onClick={() => setSelected({ route: r.id, topic: step.topic })}
                >
                  <span className="edu-branch-lamp">
                    <Icon className="size-5" />
                  </span>
                  {current && <span className="edu-branch-here text-ui-xs">当前重点</span>}
                  <span className="edu-branch-title text-ui-sm font-medium">{step.title}</span>
                  <span className="text-ui-xs text-foreground-subtle">
                    {step.review?.status === "due" && step.state !== "needs_practice"
                      ? "待复习"
                      : labels[step.state] || "待确认"}
                  </span>
                </button>
              );
            })}
          </div>
        ))}
      </div>
      {detail && (
        <div className="edu-branch-insight" role="region" aria-label="地图节点说明">
          <Button
            variant="ghost"
            size="icon"
            className="float-right"
            aria-label="关闭节点说明"
            onClick={() => setSelected(null)}
          >
            <X />
          </Button>
          <h3 className="text-ui-base font-semibold">{detail.title}</h3>
          <p className="mt-2 text-ui-sm text-foreground-subtle">{detail.objective}</p>
          <p className="mt-2 text-ui-sm text-foreground-subtle">{detail.reason}</p>
          {detail.checkpoint && (
            <p className="mt-2 text-ui-sm text-foreground-subtle">下一步：{detail.checkpoint}</p>
          )}
          <p className="mt-2 text-ui-xs text-foreground-subtle">
            {evidence?.independent_attempts && evidence.accuracy != null
              ? `近期独立首次正确率 ${evidence.accuracy}%（${evidence.recent_independent_attempts ?? evidence.independent_attempts} 次作答）`
              : "尚无足够独立作答，先诊断确认起点。"}
            {evidence?.initial
              ? ` 历史掌握估计 ${Math.round(evidence.initial.mastery * 100)}%，需用新作答确认。`
              : ""}
          </p>
          {evidence?.review?.due_at && (
            <p className="mt-2 text-ui-xs text-foreground-subtle">
              {evidence.review.status === "due" ? "复测已到期" : "复测日期"}：
              {new Date(evidence.review.due_at * 1000).toLocaleDateString("zh-CN", {
                timeZone: "Asia/Shanghai",
              })}
              。{evidence.review.reason}
            </p>
          )}
        </div>
      )}
      <footer className="edu-branch-footer" data-testid="adaptive-plan">
        {data.goal.route && data.goal.route !== data.path.selected_route && (
          <p className="mb-2 text-ui-xs text-foreground-subtle">
            当前可用链路已调整，先按「{data.path.route_title}」匹配练习。
          </p>
        )}
        <p className="text-ui-sm">
          <strong className="text-icon-blue">已选择：{data.path.route_title}</strong> ·{" "}
          {data.path.today_items} 道练习，约 {data.path.today_minutes} 分钟
        </p>
        {data.path.route_reason && (
          <p className="mt-2 text-ui-sm text-foreground-subtle" data-testid="route-reason">
            {data.path.route_reason}
          </p>
        )}
        <p className="mt-2 text-ui-xs text-foreground-subtle">
          蓝线是已选路线，灰线是可选路线；地图展示近期学习顺序，今日练习按时间安排。
          {!next ? "暂缺可用新题，可以调整目标。" : "先用独立诊断确认起点，练习后重新匹配学情。"}
        </p>
        {data.initial && (
          <p className="mt-1 text-ui-xs text-foreground-subtle">
            教材先修关系仅为建议候选，可按课堂进度自主选择。
          </p>
        )}
      </footer>
    </section>
  );
}
