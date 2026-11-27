import { useEffect, useId, useRef, useState } from "react";
import { Button } from "@zcode/ui/button";
import type { TeachingVisual } from "./contract.js";
import { numberLabel } from "./math-number.js";

type Visual = Extract<TeachingVisual, { kind: "number_line" }>;
function plainLabel(value: string) {
  return value
    .replace(/\$/g, "")
    .replace(/\\sqrt\{([^{}]+)\}/g, "√($1)")
    .replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, "($1)/($2)")
    .replace(/\\approx\s*/g, "≈")
    .replace(/\\to\s*/g, "→")
    .replace(/\\times\s*/g, "×");
}
function wrap(value: string, limit: number) {
  const rows: string[] = [];
  let line = "",
    count = 0;
  const size = (text: string) =>
    [...text].reduce((n, c) => n + (c.charCodeAt(0) > 255 ? 2 : 1), 0);
  for (const token of value.match(/\d+(?:\.\d+)?|[A-Za-z]+|./gu) || []) {
    const parts = size(token) > limit ? [...token] : [token];
    for (const part of parts) {
      if (count + size(part) > limit && line) {
        rows.push(line.trim());
        line = "";
        count = 0;
      }
      line += part;
      count += size(part);
    }
  }
  if (line) rows.push(line.trim());
  return rows;
}

export function NumberLine({ visual }: { visual: Visual }) {
  const [step, setStep] = useState(0),
    id = useId(),
    root = useRef<HTMLDivElement>(null);
  const [metrics, setMetrics] = useState({ width: 640, font: 13 });
  useEffect(() => {
    const element = root.current;
    if (!element) return;
    const measure = () => {
      const width = Math.max(
        320,
        Math.min(640, Math.floor(element.clientWidth || 640)),
      );
      const font = Number.parseFloat(getComputedStyle(element).fontSize) || 13;
      setMetrics((old) =>
        old.width === width && old.font === font ? old : { width, font },
      );
    };
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(element);
    return () => observer.disconnect();
  }, []);
  const { width, font } = metrics,
    [lo, hi] = visual.range;
  const x = (v: number) => 40 + ((v - lo) / (hi - lo)) * (width - 80);
  const gap = Math.max(26, font * 2.2 + 6),
    laneEnds: number[] = [];
  const positions = visual.points
    .map((p, i) => ({ index: i, x: x(p.x), lane: 0 }))
    .sort((a, b) => a.x - b.x);
  for (const p of positions) {
    let lane = laneEnds.findIndex((end) => p.x - end >= gap);
    if (lane < 0) lane = laneEnds.length;
    p.lane = lane;
    laneEnds[lane] = p.x;
  }
  const labelGap = Math.max(24, font * 1.6),
    axisY = 170;
  const shown = visual.moves.slice(
    0,
    visual.presentation_role === "picture" ? visual.moves.length : step,
  );
  const tickCount = Math.max(
    3,
    Math.min(8, Math.floor((width - 80) / (font * 6))),
  );
  const tickStep = Math.max(1, Math.ceil((hi - lo) / tickCount));
  const ticks = Array.from(
    { length: tickCount + 2 },
    (_, i) => Math.ceil(lo / tickStep) * tickStep + i * tickStep,
  ).filter((v) => v <= hi);
  const positionLabel = (value: number) => {
    for (const point of visual.points) {
      if (Math.abs(point.x - value) > 1e-8) continue;
      const declared = /(?:≈|=)\s*([−-]?\d+(?:\.\d+)?)/.exec(
        plainLabel(point.label),
      );
      if (
        declared &&
        Math.abs(Number(declared[1].replace("−", "-")) - value) < 1e-8
      )
        return declared[1];
    }
    return numberLabel(value);
  };
  const legends = visual.points
    .map((point, i) => {
      const label = plainLabel(point.label);
      const approx = /(?:≈|=)\s*([−-]?\d+(?:\.\d+)?)/.exec(label);
      const containsValue =
        approx &&
        Math.abs(Number(approx[1].replace("−", "-")) - point.x) < 1e-8;
      return `P${i + 1}：${label}${containsValue ? "" : " · 位置 " + numberLabel(point.x)}`;
    })
    .concat(
      shown.map((move, i) => {
        const label = plainLabel(move.label);
        const transition =
          /([−-]?\d+(?:\.\d+)?)\s*(?:→|->)\s*([−-]?\d+(?:\.\d+)?)/.exec(label);
        // 旧图标签已含端点映射时只保留一份，避免完整说明行再次重复同一组数字。
        const described =
          transition &&
          Math.abs(Number(transition[1].replace("−", "-")) - move.start) <
            1e-8 &&
          Math.abs(Number(transition[2].replace("−", "-")) - move.end) < 1e-8;
        return `M${i + 1}：${label}${described ? "" : " · " + positionLabel(move.start) + " → " + positionLabel(move.end)}`;
      }),
    );
  let rowY =
    axisY + 55 + Math.max(0, laneEnds.length - 1) * labelGap + labelGap + 8;
  const rows = legends.map((label, i) => {
    const lines = wrap(
      label,
      Math.max(12, Math.floor((width - 60) / (font * 0.65))),
    );
    const row = { lines, y: rowY, key: i };
    rowY += lines.length * labelGap + 8;
    return row;
  });
  return (
    <div ref={root} className="text-ui-caption">
      <svg
        viewBox={`0 0 ${width} ${rowY + 12}`}
        role="img"
        data-number-line="true"
        aria-labelledby={`${id}-title ${id}-description`}
        className="edu-teaching-svg text-ui-caption"
      >
        <title id={`${id}-title`}>{visual.title}</title>
        <desc id={`${id}-description`}>数轴。{legends.join("；")}</desc>
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
            <path d="M0 0 L8 4 L0 8z" fill="currentColor" />
          </marker>
        </defs>
        <line
          x1="28"
          x2={width - 25}
          y1={axisY}
          y2={axisY}
          className="edu-visual-axis"
          markerEnd={`url(#${id}-arrow)`}
        />
        {ticks.map((t) => (
          <g key={t}>
            <line
              x1={x(t)}
              x2={x(t)}
              y1={axisY - 6}
              y2={axisY + 6}
              className="edu-visual-axis"
            />
            <text
              x={x(t)}
              y={axisY + 29}
              textAnchor="middle"
              className="edu-visual-label"
            >
              {numberLabel(t)}
            </text>
          </g>
        ))}
        {positions.map((p) => (
          <g key={p.index}>
            <circle cx={p.x} cy={axisY} r="5" className="edu-visual-point" />
            <text
              x={p.x}
              y={axisY + 55 + p.lane * labelGap}
              textAnchor="middle"
              className="edu-visual-label"
              data-point-id={`P${p.index + 1}`}
            >
              P{p.index + 1}
            </text>
          </g>
        ))}
        {shown.map((move, i) => {
          const a = x(move.start),
            b = x(move.end),
            top = 134 - i * 28;
          return (
            <g key={i} data-move-visible="true" className="edu-visual-move">
              <path
                d={`M${a} ${axisY - 12} Q${(a + b) / 2} ${top - 45} ${b} ${axisY - 15}`}
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                markerEnd={`url(#${id}-arrow)`}
              />
              <text x={(a + b) / 2} y={top - 23} textAnchor="middle">
                M{i + 1}
              </text>
              <circle cx={b} cy={axisY} r="5" fill="currentColor" />
            </g>
          );
        })}
        {/* 长标签逐行放在图内，避免近邻点重叠，同时保证标注快照保留完整数学信息。 */}
        {rows.map((row) => (
          <text
            key={row.key}
            x="30"
            y={row.y}
            className="edu-visual-label"
            data-number-line-legend="true"
          >
            {row.lines.map((line, i) => (
              <tspan key={i} x="30" dy={i ? labelGap : 0}>
                {line}
              </tspan>
            ))}
          </text>
        ))}
      </svg>
      {!!visual.moves.length && visual.presentation_role !== "picture" && (
        <div className="flex flex-wrap items-center gap-2 text-ui-xs text-foreground-subtle">
          <Button
            size="sm"
            variant="outline"
            disabled={step >= visual.moves.length}
            onClick={() => setStep((s) => Math.min(s + 1, visual.moves.length))}
          >
            演示下一步
          </Button>
          <Button
            size="sm"
            variant="ghost"
            disabled={!step}
            onClick={() => setStep(0)}
          >
            重置演示
          </Button>
          <span aria-live="polite">
            {step
              ? `已演示 ${step} / ${visual.moves.length} 步`
              : "先找到起点，再看移动方向"}
          </span>
        </div>
      )}
    </div>
  );
}
