import { useState } from "react";
import { Button } from "@zcode/ui/button";
import { Input } from "@zcode/ui/input";
import { ArrowUpRight, CircleHelp, Search, Target } from "lucide-react";
import { EducationSelect } from "./controls.js";
import { LearningMapCanvas } from "./learning-map-canvas.js";
import { LearningTrend } from "./learning-trend.js";
import { LearningSummary, LearningEvidence } from "./learning-summary.js";
import {
  displayNodes,
  priority,
  statusNames,
  type DisplayNode,
  type MapMode,
} from "./learning-map-state.js";
import type { LearningOverview } from "./contract.js";

const groupOrder = [
  "数与式",
  "方程与不等式",
  "图形的性质",
  "函数",
  "图形的变化",
  "统计与概率",
  "数学基础",
];
export function LearningDashboard({
  data,
  locked,
  onNavigate,
  onPractice,
}: {
  data: LearningOverview;
  locked: boolean;
  onNavigate: (view: string) => void;
  onPractice: (topic: string) => void;
}) {
  const [mode, setMode] = useState<MapMode>("mixed");
  const [group, setGroup] = useState("all");
  const [query, setQuery] = useState("");
  const [attention, setAttention] = useState(false);
  const [selectedId, setSelectedId] = useState("");
  const nodes = displayNodes(data, mode);
  const visible = nodes.filter(
    (node) =>
      (group === "all" || node.group === group) &&
      (!attention || node.status === "review" || node.status === "diagnose") &&
      (!query.trim() || (node.title + node.path).includes(query.trim())),
  );
  const selected =
    visible.find((node) => node.id === selectedId) ||
    visible.find((node) => node.topic_id === data.path.focus) ||
    [...visible].sort(priority)[0];
  const groups = [...data.knowledge_map.groups].sort(
    (a, b) => groupOrder.indexOf(a.title) - groupOrder.indexOf(b.title),
  );
  const activeGroup = query.trim() || attention ? "filtered" : group;
  return (
    <div className="edu-dashboard">
      <div className="edu-dashboard-heading">
        <div>
          <h2 className="text-ui-xl font-semibold">学情看板</h2>
        </div>
      </div>
      <LearningSummary data={data} locked={locked} onPractice={onPractice} />
      <section className="edu-map-card" aria-label="数学学情图谱">
        <div className="edu-map-toolbar">
          <div>
            <h3 className="text-ui-lg font-semibold">数学知识图谱</h3>
            <p className="mt-1 text-ui-xs text-foreground-subtle">
              点选知识节点，查看学情与练习建议
            </p>
          </div>
          <div className="edu-map-filters">
            <label className="edu-map-search">
              <Search className="size-4" />
              <Input
                aria-label="搜索知识点"
                placeholder="搜索知识点"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="text-mobile-input-safe"
              />
            </label>
            <EducationSelect
              label="学情来源"
              value={mode}
              onValueChange={(value) => setMode(value as MapMode)}
              options={[
                { value: "mixed", label: "综合学情" },
                { value: "initial", label: "历史画像" },
                { value: "recent", label: "近期练习" },
              ]}
            />
          </div>
        </div>
        <div className="edu-map-groupbar">
          <div className="edu-map-groups" role="group" aria-label="知识分区">
            <Button
              variant={group === "all" ? "secondary" : "ghost"}
              size="sm"
              onClick={() => setGroup("all")}
              aria-pressed={group === "all"}
            >
              全部知识
            </Button>
            {groups.map((g) => (
              <Button
                key={g.id}
                variant={group === g.id ? "secondary" : "ghost"}
                size="sm"
                onClick={() => setGroup(g.id)}
                aria-pressed={group === g.id}
              >
                {g.title}
              </Button>
            ))}
          </div>
          <Button
            variant={attention ? "secondary" : "ghost"}
            size="sm"
            aria-pressed={attention}
            onClick={() => setAttention((value) => !value)}
          >
            <Target className="size-3.5" />
            只看需要关注
          </Button>
        </div>
        {mode === "recent" && !data.summary.attempts && (
          <p className="edu-map-notice text-ui-sm">
            还没有新练习，切换到历史画像查看已导入的学情。
          </p>
        )}
        <div className="edu-map-content">
          <div className="min-w-0">
            {visible.length ? (
              <LearningMapCanvas
                key={`${activeGroup}-${mode}-${query}-${attention}`}
                nodes={visible}
                groups={groups}
                edges={data.knowledge_map.edges}
                group={activeGroup}
                selected={selected?.id || ""}
                onSelect={setSelectedId}
                onGroup={setGroup}
              />
            ) : (
              <div className="edu-map-empty text-ui-base">
                <CircleHelp className="size-7" />
                <p>没有匹配的知识点。</p>
                <Button
                  variant="outline"
                  onClick={() => {
                    setQuery("");
                    setAttention(false);
                    setGroup("all");
                  }}
                >
                  查看全部知识
                </Button>
              </div>
            )}
            <div className="edu-map-legend text-ui-xs text-foreground-subtle">
              {Object.entries(statusNames).map(([key, label]) => (
                <span key={key} data-status={key}>
                  <i className="edu-map-dot" />
                  {label}
                </span>
              ))}
              <span>实线：知识分类 · 虚线：先修候选</span>
            </div>
          </div>
          <NodeDetail
            node={selected}
            data={data}
            locked={locked}
            onPractice={onPractice}
            onNavigate={onNavigate}
          />
        </div>
      </section>
      {data.daily.some((day) => day.attempts > 0) && (
        <LearningTrend days={data.daily} onPractice={() => onNavigate("practice")} />
      )}
      <LearningEvidence data={data} />
    </div>
  );
}

function NodeDetail({
  node,
  data,
  locked,
  onPractice,
  onNavigate,
}: {
  node?: DisplayNode;
  data: LearningOverview;
  locked: boolean;
  onPractice: (id: string) => void;
  onNavigate: (view: string) => void;
}) {
  const current = data.topics.find((topic) => topic.id === node?.id);
  return (
    <aside className="edu-map-detail" aria-label="知识点学情详情">
      {node ? (
        <>
          <p className="text-ui-xs text-foreground-subtle">知识点学情详情</p>
          <h3 className="mt-3 text-ui-lg font-semibold">{node.title}</h3>
          <p className="mt-2 text-ui-xs text-foreground-subtle">
            {node.path.split("/").slice(0, 2).join(" / ")}
          </p>
          <div className="edu-map-score" data-status={node.status}>
            <span className="text-ui-xl font-semibold">
              {node.score === null ? "—" : `${node.score}%`}
            </span>
            <span className="text-ui-sm">{node.metric}</span>
            <span className="edu-status text-ui-xs">{node.label}</span>
          </div>
          <p className="text-ui-xs text-foreground-subtle">当前显示：{node.source}</p>
          <dl className="edu-map-evidence text-ui-sm">
            {node.initial && node.metric !== "掌握估计" && (
              <div>
                <dt>历史掌握估计</dt>
                <dd>{node.initial ? `${Math.round(node.initial.mastery * 100)}%` : "暂无画像"}</dd>
              </div>
            )}
            {node.initial && (
              <div>
                <dt>历史作答</dt>
                <dd>{node.initial ? `${node.initial.practice_count} 次` : "暂无画像"}</dd>
              </div>
            )}
            {node.initial && (
              <div>
                <dt>历史正确率</dt>
                <dd>{node.initial ? `${Math.round(node.initial.accuracy * 100)}%` : "—"}</dd>
              </div>
            )}
            {!!current?.attempts && (
              <div>
                <dt>本产品新作答</dt>
                <dd>{current?.attempts || 0} 次</dd>
              </div>
            )}
            {current?.accuracy != null && (
              <div>
                <dt>独立首次正确率</dt>
                <dd>{current?.accuracy == null ? "暂无数据" : `${current.accuracy}%`}</dd>
              </div>
            )}
          </dl>
          <div className="edu-map-advice text-ui-sm">
            <p className="font-medium">下一步建议</p>
            <p className="mt-2 text-foreground-subtle">
              {node.status === "ready"
                ? "已有表现较好，换一道新题确认能否独立完成，再逐步进阶。"
                : node.status === "review"
                  ? "先巩固这一知识点，记录自己的步骤；卡住时先请求一项提示。"
                  : "先完成一题诊断，结合自己的思路确认学习起点。"}
            </p>
          </div>
          <Button
            className="mt-4 w-full"
            disabled={locked || !node.available || !node.topic_id}
            onClick={() => node.topic_id && onPractice(node.topic_id)}
          >
            练这个知识点
            <ArrowUpRight />
          </Button>
          {!node.available && (
            <p className="mt-2 text-ui-xs text-foreground-subtle">
              暂无可自动核验的同年级题目，可以在个性化辅导中上传你的题目。
            </p>
          )}
          <Button variant="ghost" className="mt-2 w-full" onClick={() => onNavigate("path")}>
            查看学习路径
          </Button>
          <p className="mt-4 text-ui-xs text-foreground-subtlest">
            画像估计与教材先修候选均需进一步确认，不代表教师认定的掌握结论。
          </p>
        </>
      ) : (
        <p className="text-ui-sm text-foreground-subtle">选择一个节点查看学情。</p>
      )}
    </aside>
  );
}
