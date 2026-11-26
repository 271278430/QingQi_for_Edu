import type { AnimationState } from "./use-teaching-animation.js";
import { Button } from "@zcode/ui/button";
import { Pause, Play, RotateCcw, StepForward } from "lucide-react";
import type { TeachingVisual } from "./contract.js";
import {
  CoordinateFigure,
  FractionFigure,
  FunctionFigure,
  functionValue,
} from "./teaching-plots.js";
import {
  geometrySnapshot,
  GeometryAnimationFigure,
} from "./geometry-animation.js";
import { GeometryLesson } from "./geometry-lesson.js";
import { MathContent } from "./learning-content.js";
import { IdentityAnimation } from "./identity-animation.js";
import { ProblemAnimation } from "./problem-animation.js";
import { numberLabel } from "./math-number.js";

type Animation = Extract<TeachingVisual, { kind: "animation_scene" }>;
function valueAt(visual: Animation, progress: number) {
  const at = progress * visual.duration;
  const right = Math.max(
    1,
    visual.frames.findIndex((f) => f.at >= at),
  );
  const b = visual.frames[right] || visual.frames.at(-1)!;
  const a = visual.frames[Math.max(0, right - 1)];
  const ratio = Math.min(
    1,
    Math.max(0, (at - a.at) / Math.max(0.001, b.at - a.at)),
  );
  const result = Object.fromEntries(
    Object.keys(a.values).map((key) => [
      key,
      a.values[key] + (b.values[key] - a.values[key]) * ratio,
    ]),
  );
  // 插值后按同一个数学关系重算派生量，不能把面积或绝对值直接线性插成错误数值。
  if (visual.template === "square_root") result.area = result.side ** 2;
  if (visual.template === "absolute_distance")
    result.distance = Math.abs(result.value);
  if (visual.template === "nonnegative_sum") result.total = result.a + result.b;
  if (visual.template === "fraction_fill")
    result.filled = Math.floor(result.filled + 1e-9);
  if (visual.template === "pythagorean")
    result.reveal = Math.floor(result.reveal + 1e-9);
  return result;
}
function fmt(n: number) {
  return numberLabel(n);
}

function readout(visual: Animation, progress: number) {
  if (visual.reasoning_lesson)
    return visual.reasoning_lesson.mode === "hint"
      ? "沿原题条件推理，动画停在待求条件。"
      : "逐步核对原题推导，最终结果保持精确形式。";
  if (visual.template === "identity_probe")
    return visual.algebra_lesson?.mode === "solution"
      ? "按原方程推导，完整结果保留精确形式。"
      : "试值用于理解恒成立；动画中的推导不计作你的作答。";
  if (visual.template === "function_trace" && visual.plot) {
    const p = visual.plot,
      x = p.domain[0] + (p.domain[1] - p.domain[0]) * progress;
    const y = functionValue(p, x);
    const marker = p.markers?.findIndex((m) => Math.abs(m.x - x) < 1e-8) ?? -1;
    if (p.display && marker >= 0)
      return `曲线关键点：$x=${p.display.markers[marker].x}$ · $y=${p.display.markers[marker].y}$`;
    return `曲线上的当前点：x ${fmt(x)} · y ${fmt(y)}`;
  }
  if (
    visual.template === "triangle_rotation" ||
    visual.template === "geometry_motion"
  ) {
    const g = geometrySnapshot(visual, progress);
    if (!g) return "动画数据暂不可用";
    if (visual.lesson?.mode === "hint")
      return "先观察图中的约束与变化，再尝试解释；此图没有给出完整解法。";
    return `示例读数：DE ${fmt(g.de)} · DF ${fmt(g.df)} · DE/DF ${fmt(g.ratio)} · ${visual.template === "triangle_rotation" ? `旋转 ${fmt(g.degrees)}°` : `${visual.lesson?.symbols.x || "x"} ${fmt(g.x)} · ${visual.lesson?.symbols.y || "y"} ${fmt(g.y)}`}`;
  }
  const s = valueAt(visual, progress);
  if (visual.template === "absolute_distance")
    return `位置 ${fmt(s.value)} · 到零的距离 ${fmt(s.distance)}`;
  if (visual.template === "square_root")
    return `非负边长 ${fmt(s.side)} · 对应面积 ${fmt(s.area)}`;
  if (visual.template === "nonnegative_sum")
    return `甲项 ${fmt(s.a)} · 乙项 ${fmt(s.b)} · 总量 ${fmt(s.total)}`;
  if (visual.template === "number_line_motion")
    return `起点 ${fmt(s.start)} · 已移动 ${fmt(s.delta)} · 当前位置 ${fmt(s.value)}`;
  if (visual.template === "coordinate_drawing")
    return `已连接 ${Math.floor(s.visible_segments)} / ${visual.geometry?.segments.length || 0} 条线段`;
  if (visual.template === "fraction_fill")
    return `已涂色 ${s.filled} 份 / 共 ${s.denominator} 份`;
  if (visual.template === "pythagorean")
    return `两直角边正方形面积 ${fmt(s.a_area)} 和 ${fmt(s.b_area)} · 斜边正方形面积 ${fmt(s.c_area)}`;
  return `经过 ${fmt(s.time)} 秒 · 甲的位置 ${fmt(s.a)} 米 · 乙的位置 ${fmt(s.b)} 米`;
}

function AnimationPlot({
  visual,
  progress,
}: {
  visual: Animation;
  progress: number;
}) {
  if (visual.template === "function_trace" && visual.plot)
    return (
      <FunctionFigure
        visual={{ ...visual, ...visual.plot, kind: "function_plot" }}
        progress={progress}
      />
    );
  if (
    visual.template === "triangle_rotation" ||
    visual.template === "geometry_motion"
  )
    return <GeometryAnimationFigure visual={visual} progress={progress} />;
  const s = valueAt(visual, progress);
  if (visual.template === "coordinate_drawing" && visual.geometry)
    return (
      <CoordinateFigure
        visual={{ ...visual, ...visual.geometry, kind: "coordinates" }}
        progress={s.visible_segments / visual.geometry.segments.length}
      />
    );
  if (visual.template === "fraction_fill")
    return <FractionFigure numerator={s.filled} denominator={s.denominator} />;
  if (visual.template === "pythagorean") {
    const unit = 240 / (s.a + s.b + s.c),
      ax = 190,
      ay = 280,
      bx = ax,
      by = ay - s.a * unit,
      cx = ax + s.b * unit,
      cy = ay;
    const vx = s.a * unit,
      vy = -s.b * unit;
    return (
      <svg
        viewBox="0 0 640 440"
        role="img"
        aria-label={visual.title}
        className="edu-teaching-svg text-ui-caption"
      >
        <polygon
          points={`${ax},${ay} ${bx},${by} ${cx},${cy}`}
          className="edu-geometry-fill"
        />
        {s.reveal >= 1 && (
          <rect
            x={bx - s.a * unit}
            y={by}
            width={s.a * unit}
            height={s.a * unit}
            className="edu-fraction-filled"
          />
        )}
        {s.reveal >= 2 && (
          <rect
            x={ax}
            y={ay}
            width={s.b * unit}
            height={s.b * unit}
            className="edu-geometry-secondary-fill"
          />
        )}
        {s.reveal >= 3 && (
          <polygon
            points={`${bx},${by} ${cx},${cy} ${cx + vx},${cy + vy} ${bx + vx},${by + vy}`}
            className="edu-geometry-fill"
          />
        )}
        <path
          d={`M ${ax} ${ay} L ${bx} ${by} L ${cx} ${cy} Z`}
          className="edu-geometry-line"
          fill="none"
        />
        <text
          x={ax - 20}
          y={ay - (s.a * unit) / 2}
          className="edu-visual-label"
        >
          {fmt(s.a)}
        </text>
        <text
          x={ax + (s.b * unit) / 2}
          y={ay - 12}
          className="edu-visual-label"
        >
          {fmt(s.b)}
        </text>
        <text
          x={bx + (s.b * unit) / 2 + 10}
          y={by + (s.a * unit) / 2 - 10}
          className="edu-visual-label"
        >
          {fmt(s.c)}
        </text>
      </svg>
    );
  }
  const x = (n: number) =>
    45 + ((n - visual.range[0]) / (visual.range[1] - visual.range[0])) * 550;
  const line = (
    <>
      <line x1="35" x2="610" y1="155" y2="155" className="edu-visual-axis" />
      <text x={x(0)} y="180" textAnchor="middle" className="edu-visual-label">
        0
      </text>
    </>
  );
  return (
    <svg
      viewBox="0 0 640 240"
      role="img"
      aria-label={visual.title}
      className="edu-animation-svg edu-teaching-svg text-ui-caption"
    >
      {visual.template === "absolute_distance" && (
        <>
          {line}
          <rect
            x={Math.min(x(0), x(s.value))}
            y="131"
            width={Math.abs(x(0) - x(s.value))}
            height="9"
            rx="4"
            className="edu-visual-point"
          />
          <circle cx={x(s.value)} cy="155" r="7" className="edu-visual-point" />
          <text
            x={x(s.value)}
            y="206"
            textAnchor="middle"
            className="edu-visual-label"
          >
            {fmt(s.value)}
          </text>
          <text x="45" y="48" className="edu-visual-label">
            到零的距离：{fmt(s.distance)} · 距离始终非负
          </text>
        </>
      )}
      {visual.template === "number_line_motion" && (
        <>
          {line}
          <line
            x1={x(s.start)}
            x2={x(s.value)}
            y1="115"
            y2="115"
            className="edu-visual-axis"
            strokeWidth="3"
          />
          <circle cx={x(s.start)} cy="155" r="4" className="edu-visual-point" />
          <circle cx={x(s.value)} cy="155" r="8" className="edu-visual-point" />
          <text x="45" y="48" className="edu-visual-label">
            起点 {fmt(s.start)} · 当前 {fmt(s.value)}
          </text>
          <text
            x={x(s.value)}
            y="190"
            textAnchor="middle"
            className="edu-visual-label"
          >
            {fmt(s.value)}
          </text>
        </>
      )}
      {visual.template === "square_root" &&
        (() => {
          const maxSide = Math.max(
            1,
            ...visual.frames.map((f) => f.values.side),
          );
          const size = (s.side / maxSide) * 155;
          return (
            <>
              <rect
                x="230"
                y={205 - size}
                width={size}
                height={size}
                rx="2"
                className="edu-animation-square"
              />
              <text x="40" y="45" className="edu-visual-label">
                面积：{fmt(s.area)} · 非负边长：{fmt(s.side)}
              </text>
              <text x="230" y="225" className="edu-visual-label">
                平方与算术平方根相互对应
              </text>
            </>
          );
        })()}
      {visual.template === "nonnegative_sum" && (
        <>
          <text x="45" y="42" className="edu-visual-label">
            两项都非负 · 总量：{fmt(s.total)}
          </text>
          {[s.a, s.b].map((v, i) => (
            <g key={i}>
              <rect
                x="80"
                y={85 + i * 55}
                width={(v / visual.extent) * 420}
                height="28"
                rx="5"
                className={i ? "edu-animation-second" : "edu-visual-point"}
              />
              <text x="45" y={105 + i * 55} className="edu-visual-label">
                {i ? "乙" : "甲"}
              </text>
              <text
                x={88 + (v / visual.extent) * 420}
                y={105 + i * 55}
                className="edu-visual-label"
              >
                {fmt(v)}
              </text>
            </g>
          ))}
          <text x="45" y="216" className="edu-visual-label">
            观察：总量为零时，两项分别是多少？
          </text>
        </>
      )}
      {visual.template === "travel_motion" && (
        <>
          <text x="40" y="40" className="edu-visual-label">
            时间 {fmt(s.time)} 秒 · 位置单位：米
          </text>
          {[s.a, s.b].map((v, i) => (
            <g key={i}>
              <line
                x1="35"
                x2="610"
                y1={115 + i * 80}
                y2={115 + i * 80}
                className="edu-visual-axis"
              />
              <g
                transform={`translate(${x(v)} ${95 + i * 80})`}
                className="edu-animation-traveller"
              >
                <circle cx="0" cy="-16" r="6" />
                <path
                  d="M 0 -10 L 0 6 M -8 -3 L 8 -3 M 0 6 L -7 18 M 0 6 L 7 18"
                  fill="none"
                  strokeWidth="2"
                />
              </g>
              <text
                x={x(v)}
                y={139 + i * 80}
                textAnchor="middle"
                className="edu-visual-label"
              >
                {i ? "乙" : "甲"} · {fmt(v)} 米
              </text>
            </g>
          ))}
        </>
      )}
    </svg>
  );
}

export function TeachingAnimation({
  visual,
  animation,
}: {
  visual: Animation;
  animation: AnimationState;
}) {
  const { progress, playing, reduced, seek, toggle, playTo } = animation;
  const duration = visual.duration;
  const steps =
    visual.reasoning_lesson?.steps ??
    visual.algebra_lesson?.steps ??
    visual.lesson?.steps ??
    visual.inspection_steps;
  const currentStep = steps
    ? steps.reduce((latest, s, i) => (s.at <= progress + 0.001 ? i : latest), 0)
    : 0;
  return (
    <div
      data-teaching-animation={visual.template}
      data-animation-progress={progress}
      data-current-step={currentStep}
    >
      {visual.reasoning_lesson ? (
        <ProblemAnimation
          visual={visual}
          animation={animation}
          index={currentStep}
        />
      ) : visual.algebra_lesson ? (
        <IdentityAnimation visual={visual} index={currentStep} />
      ) : visual.lesson ? (
        <GeometryLesson visual={visual} animation={animation} />
      ) : (
        <AnimationPlot visual={visual} progress={progress} />
      )}
      {visual.inspection_steps &&
        currentStep > 0 &&
        currentStep < visual.inspection_steps.length - 1 && (
          <div
            className="mt-2 text-ui-caption"
            data-function-step={currentStep}
          >
            <MathContent
              content={visual.inspection_steps[currentStep].explanation}
            />
          </div>
        )}
      {/* SVG随视口缩放，HTML说明保持字体令牌大小，手机上也能核对同一帧数值。 */}
      <div
        data-testid="animation-readout"
        className="mt-2 text-ui-caption text-foreground"
        aria-live="off"
      >
        <MathContent content={readout(visual, progress)} />
      </div>
      <div className="mt-2 flex flex-wrap items-center gap-2">
        {steps && (
          <Button
            size="sm"
            variant="ghost"
            aria-label="演示上一步"
            disabled={playing || progress === 0}
            onClick={() =>
              playTo(
                steps.filter((s) => s.at < progress - 0.001).at(-1)?.at ?? 0,
              )
            }
          >
            上一步
          </Button>
        )}
        <Button
          size="sm"
          variant="outline"
          aria-label={playing ? "暂停动画" : "播放动画"}
          disabled={reduced}
          onClick={toggle}
        >
          {playing ? <Pause /> : <Play />}
          {playing ? "暂停" : "播放"}
        </Button>
        <Button
          size="sm"
          variant="ghost"
          aria-label="演示下一步"
          disabled={
            playing ||
            progress === 1 ||
            Boolean(steps && currentStep === steps.length - 1)
          }
          onClick={() => {
            const nextStep = steps?.find((s) => s.at > progress + 0.001);
            if (nextStep) {
              playTo(nextStep.at);
              return;
            }
            const next = visual.frames.find(
              (f) => f.at / duration > progress + 0.001,
            );
            playTo(next ? next.at / duration : 1);
          }}
        >
          <StepForward />
          下一步
        </Button>
        <Button
          size="sm"
          variant="ghost"
          aria-label="重置动画"
          onClick={() => seek(0)}
        >
          <RotateCcw />
          重播
        </Button>
        <span className="text-ui-xs text-foreground-subtle" aria-live="polite">
          {playing
            ? "正在演示"
            : progress === 1
              ? "演示完成"
              : "先观察，再尝试解释"}
        </span>
      </div>
      <input
        className="edu-animation-progress mt-3 w-full"
        type="range"
        aria-label="动画进度"
        min="0"
        max="1000"
        step="1"
        value={Math.round(progress * 1000)}
        onChange={(event) => seek(Number(event.target.value) / 1000)}
      />
      {reduced && (
        <p className="mt-1 text-ui-xs text-foreground-subtle">
          已按减少动态设置使用逐步演示。
        </p>
      )}
    </div>
  );
}
