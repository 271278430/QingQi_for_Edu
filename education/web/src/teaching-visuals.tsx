import { lazy, Suspense, useId, useRef, useState, type ComponentProps } from "react";
import { Button } from "@zcode/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@zcode/ui/dialog";
import { ChevronDown, ChevronUp, Maximize2, Shapes, Pencil } from "lucide-react";
import type { TeachingVisual } from "./contract.js";
import { MathContent } from "./learning-content.js";
import { TeachingAnimation } from "./teaching-animation.js";
import { StaticReasoningDiagram } from "./static-reasoning-diagram.js";
import { useTeachingAnimation, type AnimationState } from "./use-teaching-animation.js";
import { CoordinateFigure, FunctionFigure, FractionFigure } from "./teaching-plots.js";
import { numberLabel } from "./math-number.js";
import {
  VisualAnnotation,
  snapshotVisual,
  type AnnotatedImage,
  type VisualReference,
} from "./visual-annotation.js";
type AnnotationProps = {
  reference?: VisualReference;
  onAnnotate?: (image: AnnotatedImage) => Promise<void>;
  locked?: boolean;
};
type TeachingTheme = ComponentProps<typeof MathContent>["theme"];

// 直接消费 ZCode 的公开产物组件；图表依然按需加载并使用上游的局部错误边界。
const Table = lazy(() =>
  import("@zcode/ui/artifact-presets").then((m) => ({
    default: m.ArtifactTable,
  })),
);
const Chart = lazy(() =>
  import("@zcode/ui/artifact-presets").then((m) => ({
    default: m.ArtifactChart,
  })),
);
const labels = {
  otherColumn: "其他",
  empty: "没有可展示的数据",
  itemsCount: (n: number) => `${n} 项`,
};
// 已接受数值不能按三位小数截断，小数题中的 0.0001 仍必须显示为 0.0001。
const format = numberLabel;

function NumberLine({ visual }: { visual: Extract<TeachingVisual, { kind: "number_line" }> }) {
  const [step, setStep] = useState(0);
  const id = useId();
  const [lo, hi] = visual.range;
  const x = (value: number) => 40 + ((value - lo) / (hi - lo)) * 560;
  const tickStep = Math.max(1, Math.ceil((hi - lo) / 12));
  const ticks = Array.from(
    { length: 14 },
    (_, i) => Math.ceil(lo / tickStep) * tickStep + i * tickStep,
  ).filter((t) => t <= hi);
  return (
    <div>
      <svg
        viewBox="0 0 640 240"
        role="img"
        aria-labelledby={`${id}-title ${id}-description`}
        className="edu-teaching-svg text-ui-caption"
      >
        <title id={`${id}-title`}>{visual.title}</title>
        <desc id={`${id}-description`}>
          数轴，
          {visual.points.map((p) => `${p.label} ${format(p.x)}`).join("，")}
          。点击演示下一步查看移动方向。
        </desc>
        <defs>
          <marker
            id={`${id}-arrow`}
            viewBox="0 0 8 8"
            refX="7"
            refY="4"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 0 L 8 4 L 0 8 z" fill="currentColor" />
          </marker>
        </defs>
        <line
          x1="28"
          y1="170"
          x2="615"
          y2="170"
          className="edu-visual-axis"
          markerEnd={`url(#${id}-arrow)`}
        />
        {ticks.map((t) => (
          <g key={t}>
            <line x1={x(t)} x2={x(t)} y1="164" y2="176" className="edu-visual-axis" />
            <text x={x(t)} y="199" textAnchor="middle" className="edu-visual-label">
              {format(t)}
            </text>
          </g>
        ))}
        {visual.points.map((p, i) => (
          <g key={i}>
            <circle cx={x(p.x)} cy="170" r="5" className="edu-visual-point" />
            <text x={x(p.x)} y="224" textAnchor="middle" className="edu-visual-label">
              {p.label} · {format(p.x)}
            </text>
          </g>
        ))}
        {visual.moves
          .slice(0, visual.presentation_role === "picture" ? visual.moves.length : step)
          .map((m, i) => {
            const a = x(m.start),
              b = x(m.end),
              top = 134 - i * 28;
            return (
              <g key={i} data-move-visible="true" className="edu-visual-move">
                <path
                  d={`M ${a} 158 Q ${(a + b) / 2} ${top - 45} ${b} 155`}
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  markerEnd={`url(#${id}-arrow)`}
                />
                <text x={(a + b) / 2} y={top - 23} textAnchor="middle">
                  {m.label} · {m.delta > 0 ? "+" : ""}
                  {format(m.delta)}
                </text>
                <circle cx={b} cy="170" r="5" fill="currentColor" />
                <text x={b} y="151" textAnchor="middle">
                  {format(m.end)}
                </text>
              </g>
            );
          })}
      </svg>
      {visual.moves.length > 0 && visual.presentation_role !== "picture" && (
        <div className="flex flex-wrap items-center gap-2 text-ui-xs text-foreground-subtle">
          <Button
            size="sm"
            variant="outline"
            disabled={step >= visual.moves.length}
            onClick={() => setStep((s) => Math.min(s + 1, visual.moves.length))}
          >
            演示下一步
          </Button>
          <Button size="sm" variant="ghost" disabled={step === 0} onClick={() => setStep(0)}>
            重置演示
          </Button>
          <span aria-live="polite">
            {step === 0 ? "先找到起点，再看移动方向" : `已演示 ${step} / ${visual.moves.length} 步`}
          </span>
        </div>
      )}
    </div>
  );
}

function Figure({
  visual,
  theme,
  animation,
}: {
  visual: TeachingVisual;
  theme?: TeachingTheme;
  animation?: AnimationState;
}) {
  if (visual.kind === "reasoning_diagram") return <StaticReasoningDiagram visual={visual} />;
  if (visual.kind === "animation_scene")
    return animation ? (
      <TeachingAnimation visual={visual} animation={animation} />
    ) : (
      <p>动画未准备好。</p>
    );
  if (visual.kind === "number_line") return <NumberLine visual={visual} />;
  if (visual.kind === "coordinates") return <CoordinateFigure visual={visual} />;
  if (visual.kind === "function_plot") return <FunctionFigure visual={visual} />;
  if (visual.kind === "area_model")
    return (
      <FractionFigure
        numerator={visual.numerator}
        denominator={visual.denominator}
        shape={visual.shape}
      />
    );
  if (visual.kind === "scene")
    return (
      <div className="edu-scene-figure">
        <MathContent theme={theme} content={`\`\`\`mermaid\n${visual.mermaid}\n\`\`\``} />
      </div>
    );
  if (visual.kind === "table")
    return (
      <Suspense fallback={<p className="text-ui-sm text-foreground-subtle">正在展示表格…</p>}>
        <Table
          labels={labels}
          spec={{
            columns: visual.columns.map((label, i) => ({
              label,
              field: `c${i}`,
            })),
          }}
          items={visual.rows.map((row, i) => ({
            sequence: i,
            siteId: visual.id,
            ordinal: i,
            item: Object.fromEntries(row.map((value, j) => [`c${j}`, value])),
          }))}
        />
      </Suspense>
    );
  return (
    <Suspense fallback={<p className="text-ui-sm text-foreground-subtle">正在展示图表…</p>}>
      <Chart
        labels={labels}
        spec={{
          type: "bar",
          x: { field: "label", label: "对象" },
          y: { field: "value", label: "数值" },
        }}
        items={visual.bars.map((bar, i) => ({
          sequence: i,
          siteId: visual.id,
          ordinal: i,
          item: bar,
        }))}
      />
    </Suspense>
  );
}

function AnimatedVisualCard({
  visual,
  theme,
  ...annotation
}: {
  visual: Extract<TeachingVisual, { kind: "animation_scene" }>;
  theme?: TeachingTheme;
} & AnnotationProps) {
  const animation = useTeachingAnimation(visual.duration);
  return <VisualCard visual={visual} theme={theme} animation={animation} {...annotation} />;
}
function VisualCard({
  visual,
  theme,
  animation,
  reference,
  onAnnotate,
  locked,
}: {
  visual: TeachingVisual;
  theme?: TeachingTheme;
  animation?: AnimationState;
} & AnnotationProps) {
  const [expanded, setExpanded] = useState(true);
  const [opened, setOpened] = useState(false);
  const contentId = useId();
  const content = useRef<HTMLDivElement>(null);
  const [snapshot, setSnapshot] = useState("");
  const [preparing, setPreparing] = useState(false);
  const [annotationError, setAnnotationError] = useState("");
  const mark = async () => {
    if (!content.current || locked || preparing) return;
    setPreparing(true);
    setAnnotationError("");
    animation?.pause();
    try {
      setSnapshot(await snapshotVisual(content.current));
    } catch (e) {
      setAnnotationError(e instanceof Error ? e.message : "图示无法读取。");
    } finally {
      setPreparing(false);
    }
  };
  return (
    <section
      className="edu-teaching-card"
      data-teaching-visual={visual.kind}
      aria-label={visual.title}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="mb-1 flex items-center gap-1.5 text-ui-xs text-foreground-subtle">
            <Shapes className="size-3.5" />
            {visual.kind === "animation_scene"
              ? "教学动画 · 按步骤观察"
              : "讲解图 · 关键条件与结构"}{" "}
            <span className="edu-visual-basis">
              {visual.kind === "coordinates" && visual.layout === "geometry"
                ? "原题示意"
                : visual.basis === "example"
                  ? "相似例子"
                  : "原题条件"}
            </span>
          </p>
          <h3 className="text-ui-sm font-medium">{visual.title}</h3>
        </div>
        <div className="flex shrink-0 gap-1">
          {reference && onAnnotate && visual.kind !== "table" && (
            <Button
              variant="ghost"
              size="icon-sm"
              aria-label="标注图示"
              disabled={locked || preparing || !expanded}
              onClick={() => void mark()}
            >
              <Pencil className="size-4" />
            </Button>
          )}
          <Button
            variant="ghost"
            size="icon-sm"
            aria-label="放大图示"
            onClick={() => setOpened(true)}
          >
            <Maximize2 className="size-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon-sm"
            aria-label={expanded ? "收起图示" : "展开图示"}
            aria-expanded={expanded}
            aria-controls={contentId}
            onClick={() => {
              if (expanded) animation?.pause();
              setExpanded((s) => !s);
            }}
          >
            {expanded ? <ChevronUp className="size-4" /> : <ChevronDown className="size-4" />}
          </Button>
        </div>
      </div>
      {expanded && (
        <div ref={content} id={contentId} className="mt-3 min-w-0">
          <Figure visual={visual} theme={theme} animation={animation} />
          {visual.caption && <MathContent content={visual.caption} theme={theme} />}
          <p className="mt-3 text-ui-xs text-foreground-subtlest">{visual.provenance}</p>
        </div>
      )}
      {annotationError && (
        <p role="alert" className="text-ui-sm text-danger">
          {annotationError}
        </p>
      )}
      {snapshot && reference && onAnnotate && (
        <VisualAnnotation
          snapshot={snapshot}
          title={visual.title}
          reference={reference}
          onClose={() => setSnapshot("")}
          onReturn={onAnnotate}
        />
      )}
      <Dialog
        open={opened}
        onOpenChange={(open) => {
          setOpened(open);
          if (!open && !expanded) animation?.pause();
        }}
      >
        <DialogContent className="edu-teaching-dialog sm:max-w-4xl">
          <DialogHeader>
            <DialogTitle>{visual.title}</DialogTitle>
            <DialogDescription>{visual.provenance}</DialogDescription>
          </DialogHeader>
          <div className="min-w-0 overflow-auto">
            <Figure visual={visual} theme={theme} animation={animation} />
            {visual.caption && <MathContent content={visual.caption} theme={theme} />}
          </div>
        </DialogContent>
      </Dialog>
    </section>
  );
}

export function TeachingVisuals({
  visuals,
  theme,
  runId,
  onAnnotate,
  locked,
}: {
  visuals?: TeachingVisual[];
  theme?: TeachingTheme;
  runId?: number;
  onAnnotate?: (image: AnnotatedImage) => Promise<void>;
  locked?: boolean;
}) {
  if (!visuals?.length) return null;
  return (
    <div className="mt-4 grid min-w-0 gap-3" aria-label="本条回复的辅助图示">
      {visuals.map((visual, index) =>
        visual.kind === "animation_scene" ? (
          <AnimatedVisualCard
            key={visual.id}
            visual={visual}
            theme={theme}
            reference={runId ? { run_id: runId, visual_index: index } : undefined}
            onAnnotate={onAnnotate}
            locked={locked}
          />
        ) : (
          <VisualCard
            key={visual.id}
            visual={visual}
            theme={theme}
            reference={runId ? { run_id: runId, visual_index: index } : undefined}
            onAnnotate={onAnnotate}
            locked={locked}
          />
        ),
      )}
    </div>
  );
}
