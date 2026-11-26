import { useId } from "react";
import type { TeachingVisual } from "./contract.js";
import { MathContent } from "./learning-content.js";
import { numberLabel, numberTex } from "./math-number.js";
import { plotTicks } from "./plot-ticks.js";
type Coordinate = Extract<TeachingVisual, { kind: "coordinates" }>;

// 动画当前点、读数和曲线使用同一函数，避免三次函数被旧二次公式计算。
export function functionValue(
  visual: {
    function: "linear" | "quadratic" | "cubic" | "square_root" | "absolute";
    a: number;
    b: number;
    c: number;
    d?: number;
  },
  x: number,
) {
  return visual.function === "square_root"
    ? Math.sqrt(Math.max(0, visual.a * x + visual.b))
    : visual.function === "absolute"
      ? Math.abs(visual.a * x + visual.b)
      : visual.function === "linear"
        ? visual.a * x + visual.b
        : visual.function === "quadratic"
          ? (visual.a * x + visual.b) * x + visual.c
          : ((visual.a * x + visual.b) * x + visual.c) * x + (visual.d ?? 0);
}

export function CoordinateFigure({
  visual,
  progress = 1,
}: {
  visual: Coordinate;
  progress?: number;
}) {
  const id = useId();
  const geometry = visual.layout === "geometry";
  const xmin = Math.min(...visual.points.map((p) => p.x)),
    xmax = Math.max(...visual.points.map((p) => p.x));
  const ymin = Math.min(...visual.points.map((p) => p.y)),
    ymax = Math.max(...visual.points.map((p) => p.y));
  const unit = geometry
    ? Math.min(
        540 / Math.max(1e-9, xmax - xmin),
        280 / Math.max(1e-9, ymax - ymin),
      )
    : 155 / visual.extent;
  const step = Math.max(1, Math.ceil(visual.extent / 4));
  const ticks = Array.from(
    { length: 2 * Math.floor(visual.extent / step) + 1 },
    (_, i) => (i - Math.floor(visual.extent / step)) * step,
  );
  const x = (v: number) =>
      geometry
        ? 50 + (540 - (xmax - xmin) * unit) / 2 + (v - xmin) * unit
        : 320 + v * unit,
    y = (v: number) =>
      geometry
        ? 330 - (280 - (ymax - ymin) * unit) / 2 - (v - ymin) * unit
        : 190 - v * unit;
  const segments = visual.segments || [];
  // 关键帧之间沿真实端点延长当前线段，避免所谓动画只是整条线突然出现。
  const drawn = Math.min(
    segments.length,
    Math.max(0, progress * segments.length),
  );
  const shown = Math.ceil(drawn - 1e-8);
  return (
    <div>
      <svg
        viewBox="0 0 640 380"
        role="img"
        aria-labelledby={`${id}-title`}
        className="edu-teaching-svg text-ui-caption"
      >
        <title id={`${id}-title`}>{visual.title}</title>
        {!geometry && (
          <>
            {ticks.map((t) => (
              <g key={t} className="edu-visual-grid">
                <line x1={x(t)} x2={x(t)} y1="35" y2="345" />
                <line x1="165" x2="475" y1={y(t)} y2={y(t)} />
              </g>
            ))}
            <line
              x1="150"
              x2="493"
              y1="190"
              y2="190"
              className="edu-visual-axis"
            />
            <line
              x1="320"
              x2="320"
              y1="22"
              y2="358"
              className="edu-visual-axis"
            />
            <text x="500" y="194" className="edu-visual-label">
              x
            </text>
            <text x="330" y="26" className="edu-visual-label">
              y
            </text>
            {ticks.map((t) => (
              <g key={t} className="edu-visual-label">
                <text x={x(t)} y="208" textAnchor="middle">
                  {t}
                </text>
                {t !== 0 && (
                  <text x="310" y={y(t) + 4} textAnchor="end">
                    {t}
                  </text>
                )}
              </g>
            ))}
          </>
        )}
        {(visual.polygons || []).map((polygon, i) => (
          <polygon
            key={i}
            points={polygon.vertices
              .map((n) => `${x(visual.points[n].x)},${y(visual.points[n].y)}`)
              .join(" ")}
            className="edu-geometry-fill"
          />
        ))}
        {(visual.circles || []).map((circle, i) => (
          <circle
            key={i}
            cx={x(visual.points[circle.center].x)}
            cy={y(visual.points[circle.center].y)}
            r={circle.radius * unit}
            className="edu-geometry-circle"
          />
        ))}
        {segments.slice(0, shown).map((s, i) => (
          <g key={i} data-coordinate-segment={`${s.source}-${s.target}`}>
            <line
              x1={x(visual.points[s.source].x)}
              y1={y(visual.points[s.source].y)}
              x2={
                x(visual.points[s.source].x) +
                (x(visual.points[s.target].x) - x(visual.points[s.source].x)) *
                  Math.min(1, drawn - i)
              }
              y2={
                y(visual.points[s.source].y) +
                (y(visual.points[s.target].y) - y(visual.points[s.source].y)) *
                  Math.min(1, drawn - i)
              }
              className={`edu-geometry-line edu-geometry-${s.role}`}
              strokeDasharray={s.style === "dashed" ? "6 4" : undefined}
            />
            {s.label &&
              ![
                visual.points[s.source].label + visual.points[s.target].label,
                visual.points[s.target].label + visual.points[s.source].label,
              ].includes(s.label) &&
              drawn - i >= 1 && (
                <text
                  x={
                    (x(visual.points[s.source].x) +
                      x(visual.points[s.target].x)) /
                      2 +
                    7
                  }
                  y={
                    (y(visual.points[s.source].y) +
                      y(visual.points[s.target].y)) /
                      2 -
                    8
                  }
                  className="edu-visual-label"
                >
                  {s.label}
                </text>
              )}
          </g>
        ))}
        {visual.points.map((p, i) => (
          <g key={i} data-coordinate-point={p.label}>
            <circle
              cx={x(p.x)}
              cy={y(p.y)}
              r="5"
              className="edu-visual-point"
            />
            <text x={x(p.x) + 8} y={y(p.y) - 8} className="edu-visual-label">
              {p.label}
            </text>
          </g>
        ))}
      </svg>
      {geometry && (
        <details className="mt-2">
          <summary className="cursor-pointer text-ui-xs text-foreground-subtle">
            绘图坐标（精确形式）
          </summary>
          <div data-coordinate-readout>
            <MathContent
              content={visual.points
                .map(
                  (p) =>
                    `$${p.label}(${p.x_tex ?? numberTex(p.x)}, ${p.y_tex ?? numberTex(p.y)})$`,
                )
                .join(" · ")}
            />
          </div>
        </details>
      )}
      {!geometry && (
        <div
          className="mt-2 text-ui-caption text-foreground"
          data-coordinate-readout
        >
          <MathContent
            content={visual.points
              .map(
                (p) =>
                  `$${p.label}(${p.x_tex ?? numberTex(p.x)}, ${p.y_tex ?? numberTex(p.y)})$`,
              )
              .join(" · ")}
          />
        </div>
      )}
    </div>
  );
}

export function FunctionFigure({
  visual,
  progress,
  endpoints,
  variables,
  showCaption = true,
}: {
  visual: Extract<TeachingVisual, { kind: "function_plot" }>;
  progress?: number;
  endpoints?: { left: "open" | "closed"; right: "open" | "closed" };
  variables?: { x: string; y: string };
  showCaption?: boolean;
}) {
  const labels = variables ?? visual.axis_labels ?? { x: "x", y: "y" };
  const [xmin, xmax] = visual.domain,
    [ymin, ymax] = visual.y_range;
  const x = (n: number) => 50 + ((n - xmin) / (xmax - xmin)) * 540,
    y = (n: number) => 325 - ((n - ymin) / (ymax - ymin)) * 285;
  const grid = plotTicks(xmin, xmax);
  const raw = (ymax - ymin) / 6,
    power = 10 ** Math.floor(Math.log10(raw));
  const tickStep =
    power *
    (raw / power <= 1 ? 1 : raw / power <= 2 ? 2 : raw / power <= 5 ? 5 : 10);
  const yTicks = Array.from(
    {
      length: Math.max(
        1,
        Math.floor(ymax / tickStep) - Math.ceil(ymin / tickStep) + 1,
      ),
    },
    (_, i) => (Math.ceil(ymin / tickStep) + i) * tickStep,
  );
  const xAxis = Math.max(40, Math.min(325, y(0))),
    yAxis = Math.max(50, Math.min(590, x(0)));
  const currentX = xmin + (xmax - xmin) * (progress ?? 1);
  const currentY = functionValue(visual, currentX);
  const samples =
    progress === undefined
      ? visual.samples
      : [
          ...visual.samples.filter((p) => p.x < currentX),
          { x: currentX, y: currentY },
        ];
  const coefficients =
    visual.function === "linear"
      ? [visual.a, visual.b]
      : visual.function === "quadratic"
        ? [visual.a, visual.b, visual.c]
        : [visual.a, visual.b, visual.c, visual.d ?? 0];
  const expression =
    coefficients
      .map((value, i) => {
        if (!value) return "";
        const degree = coefficients.length - i - 1;
        return `${i && value > 0 ? "+" : ""}${degree && Math.abs(value) === 1 ? (value < 0 ? "−" : "") : numberTex(value)}${degree ? `${labels.x}${degree > 1 ? `^{${degree}}` : ""}` : ""}`;
      })
      .join("")
      .replace(/^\+/, "") || "0";
  const formula = `${labels.y} = ${visual.display?.formula ?? expression}`;
  return (
    <div>
      <svg
        viewBox="0 0 640 380"
        role="img"
        aria-label={visual.title}
        className="edu-teaching-svg text-ui-caption"
      >
        {visual.focus_interval && (
          <rect
            data-function-focus="true"
            x={x(visual.focus_interval[0])}
            y="40"
            width={x(visual.focus_interval[1]) - x(visual.focus_interval[0])}
            height="285"
            className="edu-geometry-fill"
          />
        )}
        {grid.map((v, i) => (
          <g key={i}>
            <line
              x1={x(v)}
              x2={x(v)}
              y1="40"
              y2="325"
              className="edu-visual-grid"
            />
            <text
              x={x(v)}
              y="347"
              textAnchor="middle"
              className="edu-visual-label"
            >
              {Number(v.toFixed(2))}
            </text>
          </g>
        ))}
        {yTicks.map((v, i) => (
          <g key={i} data-function-y-tick={v}>
            <line
              x1="50"
              x2="590"
              y1={y(v)}
              y2={y(v)}
              className="edu-visual-grid"
            />
            <text
              x={yAxis - 8}
              y={y(v) - 4}
              textAnchor="end"
              className="edu-visual-label"
            >
              {Number(v.toPrecision(6))}
            </text>
          </g>
        ))}
        <line
          x1="40"
          x2="608"
          y1={xAxis}
          y2={xAxis}
          className="edu-visual-axis"
        />
        <line
          x1={yAxis}
          x2={yAxis}
          y1="28"
          y2="335"
          className="edu-visual-axis"
        />
        <text x="612" y={xAxis + 4} className="edu-visual-label">
          {labels.x}
        </text>
        <text x={yAxis + 10} y="28" className="edu-visual-label">
          {labels.y}
        </text>
        {(endpoints || visual.markers) && progress !== undefined && (
          <path
            data-function-reference="true"
            d={visual.samples
              .map((p, i) => `${i ? "L" : "M"} ${x(p.x)} ${y(p.y)}`)
              .join(" ")}
            fill="none"
            className="edu-geometry-curve edu-function-reference"
          />
        )}
        <path
          d={samples
            .map((p, i) => `${i ? "L" : "M"} ${x(p.x)} ${y(p.y)}`)
            .join(" ")}
          fill="none"
          className="edu-geometry-curve"
        />
        {visual.markers?.map((point, i) => (
          <g key={i} data-function-marker={point.x}>
            <circle
              cx={x(point.x)}
              cy={y(point.y)}
              r="5"
              className="edu-visual-point"
            />
            <text
              x={x(point.x)}
              y={y(point.y) + (i % 2 ? 20 : -12)}
              textAnchor="middle"
              className="edu-visual-label"
            >
              {visual.function === "square_root" ||
              visual.function === "absolute"
                ? "零点"
                : visual.display
                  ? `P${i + 1}`
                  : `(${numberLabel(point.x)}, ${numberLabel(point.y)})`}
            </text>
          </g>
        ))}
        {progress !== undefined && (
          <circle
            data-function-cursor="true"
            data-function-x={currentX}
            data-function-y={currentY}
            cx={x(currentX)}
            cy={y(currentY)}
            r="5"
            className="edu-visual-point"
          />
        )}
        {endpoints &&
          (["left", "right"] as const).map((end) => {
            const point =
              end === "left" ? visual.samples[0] : visual.samples.at(-1)!;
            return (
              <circle
                key={end}
                data-function-endpoint={end}
                data-boundary={endpoints[end]}
                cx={x(point.x)}
                cy={y(point.y)}
                r="5"
                className={`edu-function-${endpoints[end]}`}
              />
            );
          })}
      </svg>
      {showCaption && (
        <MathContent
          content={`$${formula}$ · ${labels.x}${endpoints ? " 的取值范围" : " 的显示范围"} $${endpoints?.left === "open" ? "(" : "["}${visual.display?.domain[0] ?? numberTex(xmin)}, ${visual.display?.domain[1] ?? numberTex(xmax)}${endpoints?.right === "open" ? ")" : "]"}$`}
        />
      )}
      {visual.markers && (
        <ul className="mt-2 grid gap-1 text-ui-caption text-foreground-subtle">
          {visual.markers.map((p, i) => (
            <li key={i}>
              <MathContent
                content={`${visual.display ? `P${i + 1} ` : ""}$(${visual.display?.markers[i]?.x ?? numberTex(p.x)}, ${visual.display?.markers[i]?.y ?? numberTex(p.y)})$ · ${p.label}`}
              />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export function FractionFigure({
  numerator,
  denominator,
  shape = "rectangle",
}: {
  numerator: number;
  denominator: number;
  shape?: "rectangle" | "circle";
}) {
  const cells = Array.from({ length: denominator }, (_, i) => i);
  const point = (a: number) =>
    `${320 + 100 * Math.cos(a)},${140 + 100 * Math.sin(a)}`;
  return (
    <div>
      <svg
        viewBox="0 0 640 280"
        role="img"
        aria-label={`涂色 ${numerator} 份，共 ${denominator} 份`}
        className="edu-teaching-svg text-ui-caption"
      >
        {shape === "rectangle" ? (
          cells.map((i) => (
            <rect
              key={i}
              x={40 + (i * 560) / denominator}
              y="85"
              width={560 / denominator}
              height="110"
              className={
                i < numerator ? "edu-fraction-filled" : "edu-fraction-empty"
              }
            />
          ))
        ) : denominator === 1 ? (
          <circle
            cx="320"
            cy="140"
            r="100"
            className={numerator ? "edu-fraction-filled" : "edu-fraction-empty"}
          />
        ) : (
          cells.map((i) => {
            const a = -Math.PI / 2 + (2 * Math.PI * i) / denominator,
              b = -Math.PI / 2 + (2 * Math.PI * (i + 1)) / denominator;
            return (
              <path
                key={i}
                d={`M 320,140 L ${point(a)} A 100,100 0 ${b - a > Math.PI ? 1 : 0},1 ${point(b)} Z`}
                className={
                  i < numerator ? "edu-fraction-filled" : "edu-fraction-empty"
                }
              />
            );
          })
        )}
      </svg>
      <p className="mt-2 text-ui-caption text-foreground">
        涂色 {numerator} 份 / 共 {denominator} 份
      </p>
    </div>
  );
}
