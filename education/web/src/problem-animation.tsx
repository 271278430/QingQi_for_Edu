import { useId } from "react";
import { Button } from "@zcode/ui/button";
import type {
  FunctionReasoning,
  NonnegativeReasoning,
  ReasoningCurve,
  TeachingVisual,
} from "./contract.js";
import type { AnimationState } from "./use-teaching-animation.js";
import { MathContent } from "./learning-content.js";
import { plotTicks } from "./plot-ticks.js";
import { numberTex } from "./math-number.js";

type Animation = Extract<TeachingVisual, { kind: "animation_scene" }>;
const clamp = (n: number) => Math.max(0, Math.min(1, n));

export function Curve({
  curve,
  zeros = [],
  activeX,
  highlight,
  interval,
  label,
}: {
  curve: ReasoningCurve;
  zeros?: { x: number; label: string }[];
  activeX?: number;
  highlight?: { x: number; y: number };
  interval?: [number, number];
  label?: string;
}) {
  const clip = useId().replace(/[^a-zA-Z0-9]/g, "");
  const [lo, hi] = curve.domain,
    [bottom, top] = curve.y_range;
  const x = (value: number) => 60 + ((value - lo) / (hi - lo)) * 530;
  const y = (value: number) => 285 - ((value - bottom) / (top - bottom)) * 250;
  const ticks = (values: { value: number; label: string }[]) =>
    values.filter((v, i) => values.findIndex((p) => Math.abs(p.value - v.value) < 1e-9) === i);
  const xTicks = ticks(
    curve.x_ticks ?? plotTicks(lo, hi).map((value) => ({ value, label: numberTex(value) })),
  );
  const yTicks = ticks(
    curve.y_ticks ?? plotTicks(bottom, top).map((value) => ({ value, label: numberTex(value) })),
  );
  const path = curve.samples
    .map((point, i) => `${i ? "L" : "M"}${x(point.x)} ${y(point.y)}`)
    .join(" ");
  const sampleIndex =
    activeX === undefined ? -1 : curve.samples.findIndex((point) => point.x >= activeX);
  const sample = curve.samples[sampleIndex],
    before = curve.samples[Math.max(0, sampleIndex - 1)];
  // 观察点只沿已批准采样折线插值；不能由UI推导新的参数或最值。
  const sampleY =
    sample && activeX !== undefined
      ? before.y +
        (sample.y - before.y) * clamp((activeX - before.x) / Math.max(1e-12, sample.x - before.x))
      : undefined;
  return (
    <div className="edu-curve-figure">
      <svg
        viewBox="0 0 640 330"
        className="edu-teaching-svg edu-reasoning-curve text-ui-caption"
        role="img"
        aria-label={label || "当前推理阶段的函数曲线"}
      >
        {label && (
          <text x="320" y="20" textAnchor="middle" className="edu-visual-label">
            {label}
          </text>
        )}
        <defs>
          <clipPath id={clip}>
            <rect x="60" y="35" width="530" height="250" />
          </clipPath>
        </defs>
        {interval && (
          <rect
            x={x(interval[0])}
            y="35"
            width={x(interval[1]) - x(interval[0])}
            height="250"
            className="edu-reasoning-interval"
            data-reasoning-interval
          />
        )}
        {xTicks.map((tick) => (
          <g key={tick.value} data-curve-x-tick={tick.value}>
            <line
              x1={x(tick.value)}
              x2={x(tick.value)}
              y1="35"
              y2="285"
              className="edu-visual-grid"
            />
            <foreignObject x={x(tick.value) - 40} y="289" width="80" height="35">
              <div className="edu-curve-tick text-ui-caption">
                <MathContent content={`$$${tick.label}$$`} />
              </div>
            </foreignObject>
          </g>
        ))}
        {yTicks
          .filter((tick) => tick.value >= bottom && tick.value <= top)
          .map((tick) => (
            <g key={tick.value} data-curve-y-tick={tick.value}>
              <line
                x1="60"
                x2="590"
                y1={y(tick.value)}
                y2={y(tick.value)}
                className="edu-visual-grid"
              />
              <foreignObject x="0" y={y(tick.value) - 14} width="54" height="30">
                <div className="edu-curve-tick text-ui-caption">
                  <MathContent content={`$$${tick.label}$$`} />
                </div>
              </foreignObject>
            </g>
          ))}
        <g clipPath={`url(#${clip})`}>
          <line x1="60" x2="590" y1={y(0)} y2={y(0)} className="edu-visual-axis" />
          {lo <= 0 && hi >= 0 && (
            <line x1={x(0)} x2={x(0)} y1="35" y2="285" className="edu-visual-axis" />
          )}
          <path d={path} className="edu-reasoning-function" />
          {zeros.map((zero, index) => (
            <g key={index} data-reasoning-zero={zero.x}>
              <circle cx={x(zero.x)} cy={y(0)} r="6" className="edu-visual-point" />
              <text
                x={x(zero.x)}
                y={y(0) - 15 - (index % 2) * 18}
                textAnchor="middle"
                className="edu-visual-label"
              >
                {zero.label}
              </text>
            </g>
          ))}
          {curve.markers.map((point, i) => (
            <circle
              key={i}
              data-curve-landmark={`${point.x},${point.y}`}
              cx={x(point.x)}
              cy={y(point.y)}
              r="5"
              className="edu-visual-point"
            />
          ))}
          {highlight && (
            <g data-reasoning-highlight={`${highlight.x},${highlight.y}`}>
              <line
                x1={x(highlight.x)}
                x2={x(highlight.x)}
                y1={y(0)}
                y2={y(highlight.y)}
                className="edu-reasoning-guide"
              />
              <circle
                cx={x(highlight.x)}
                cy={y(highlight.y)}
                r="8"
                className="edu-reasoning-selected-point"
              />
            </g>
          )}
          {sample && activeX !== undefined && (
            <g>
              <line
                x1={x(activeX)}
                x2={x(activeX)}
                y1="35"
                y2="285"
                className="edu-reasoning-guide"
                data-reasoning-cursor={activeX}
              />
              <circle
                cx={x(activeX)}
                cy={y(sampleY!)}
                r="6"
                className="edu-reasoning-selected-point"
                data-reasoning-linked-point={activeX}
              />
            </g>
          )}
        </g>
        <text x="590" y="328" textAnchor="end" className="edu-visual-label">
          {curve.axis_labels?.x ?? "x"}
        </text>
        <text x="60" y="22" className="edu-visual-label">
          {curve.axis_labels?.y ?? "f(x)"}
        </text>
      </svg>
      {curve.formula && (
        <MathContent
          content={`$${curve.formula.includes("=") ? curve.formula : `${curve.axis_labels?.y === "f′(x)" ? "f\\prime(x)" : curve.axis_labels?.y === "f(x)" ? "f(x)" : "y"}=${curve.formula}`}$`}
        />
      )}
      {curve.note && <p className="mt-2 text-ui-caption text-foreground-subtle">{curve.note}</p>}
      {curve.markers.length > 0 && (
        <div className="edu-curve-landmarks text-ui-caption">
          {curve.markers.map((point, i) => (
            <MathContent key={i} content={`$${point.label}$`} />
          ))}
        </div>
      )}
    </div>
  );
}

function FunctionScene({
  lesson,
  scene,
  local,
  start,
  end,
  animation,
}: {
  lesson: FunctionReasoning;
  scene: string;
  local: number;
  start: number;
  end: number;
  animation: AnimationState;
}) {
  if (scene === "cases") {
    const selected = Math.min(2, Math.floor(local * 3));
    return (
      <div>
        <div className="edu-reasoning-case-options">
          {lesson.cases.map((item, i) => (
            <Button
              key={item.root_count}
              size="sm"
              variant={selected === i ? "default" : "outline"}
              onClick={() => animation.seek(start + ((end - start) * (i + 0.01)) / 3)}
              aria-label={`观察${item.root_count}个正零点`}
              aria-pressed={selected === i}
            >
              {item.root_count} 个正零点
            </Button>
          ))}
        </div>
        <div className="edu-reasoning-cases">
          {lesson.cases
            .filter((_, i) => i === selected)
            .map((item) => (
              <section
                key={item.root_count}
                className="edu-reasoning-case"
                data-active="true"
                data-root-count={item.root_count}
              >
                <h4 className="text-ui-sm font-semibold">{item.label}</h4>
                <Curve
                  curve={item.curve}
                  zeros={item.zeros.map((x) => ({ x, label: "零点" }))}
                  highlight={item.minimum}
                />
                <p className="text-ui-xs">
                  {item.root_count === 0
                    ? "最低处仍为正，无法碰到横轴"
                    : item.root_count === 1
                      ? "接触后返回正值，只出现一次"
                      : "先穿过再穿回，出现两次"}
                </p>
              </section>
            ))}
        </div>
      </div>
    );
  }
  if (scene === "solve" && lesson.elimination)
    return (
      <div>
        <Curve
          curve={lesson.root_curve}
          zeros={[{ x: lesson.positive_stationary.x, label: "正驻点 r" }]}
          highlight={lesson.positive_stationary}
        />
        <p className="text-ui-sm font-semibold" data-testid="elimination-action">
          {lesson.elimination[Math.min(2, Math.floor(local * 3))].title}
        </p>
        <p className="text-ui-sm">
          {lesson.elimination[Math.min(2, Math.floor(local * 3))].action}
        </p>
        <div className="edu-reasoning-equation text-ui-base">
          <MathContent
            content={`$$${lesson.elimination[Math.min(2, Math.floor(local * 3))].formula}$$`}
          />
        </div>
        {local >= 2 / 3 && (
          <div className="edu-reasoning-result text-ui-lg">
            <MathContent
              content={`$r=${lesson.solved?.root},\\quad ${lesson.given.parameter}=${lesson.solved?.parameter}$`}
            />
          </div>
        )}
      </div>
    );
  if (scene === "derivative" && lesson.derivative_curve && lesson.curve) {
    const activeX =
      lesson.given.interval[0] + (lesson.given.interval[1] - lesson.given.interval[0]) * local;
    return (
      <div>
        <p className="text-ui-sm font-semibold">原函数：看它升高还是降低</p>
        <Curve curve={lesson.curve} activeX={activeX} interval={lesson.given.interval} />
        <p className="text-ui-sm font-semibold">导函数：同一个 x 的导数符号</p>
        <Curve curve={lesson.derivative_curve} activeX={activeX} interval={lesson.given.interval} />
        <div className="edu-reasoning-signs">
          {lesson.signs?.map((sign, i) => (
            <span
              key={i}
              data-sign={sign.sign}
              data-active={sign.from <= activeX && activeX <= sign.to}
              className="text-ui-sm"
            >
              {sign.sign === "+" ? "导数为正 → 函数增加" : "导数为负 → 函数减少"}
            </span>
          ))}
        </div>
      </div>
    );
  }
  if ((scene === "extrema" || scene === "result") && lesson.candidates && lesson.curve) {
    const selected =
      scene === "result"
        ? -1
        : Math.min(lesson.candidates.length - 1, Math.floor(local * lesson.candidates.length));
    const active = lesson.candidates[selected];
    const comparisonIndex = lesson.steps.findIndex((step) => step.scene === "extrema");
    const comparisonStart = lesson.steps[comparisonIndex].at,
      comparisonEnd = lesson.steps[comparisonIndex + 1].at;
    return (
      <div>
        <Curve curve={lesson.curve} highlight={active} interval={lesson.given.interval} />
        <div className="edu-reasoning-candidates">
          {lesson.candidates.map((candidate, i) => (
            <Button
              key={i}
              variant={selected === i ? "default" : "outline"}
              aria-label={`比较候选点${candidate.x}`}
              onClick={() =>
                animation.seek(
                  comparisonStart +
                    ((comparisonEnd - comparisonStart) * (i + 0.01)) / lesson.candidates!.length,
                )
              }
            >
              <span className="text-ui-sm">
                <MathContent content={`$f(${candidate.x_label})=${candidate.y_label}$`} />
                {candidate.role}
              </span>
            </Button>
          ))}
        </div>
        {scene === "result" && (
          <div className="edu-reasoning-result text-ui-lg">
            <MathContent
              content={`最大值 $${lesson.solved?.maximum}$ 与最小值 $${lesson.solved?.minimum}$ 相加，得到 $${lesson.solved?.sum}$。`}
            />
          </div>
        )}
      </div>
    );
  }
  if (scene === "read")
    return (
      <div>
        <p className="text-ui-sm font-semibold">
          {lesson.mode === "solution"
            ? "原题函数：相切零点与区间最值"
            : "参数未确定：比较原题函数族的形状"}
        </p>
        <Curve
          curve={lesson.curve ?? lesson.cases[0].curve}
          highlight={lesson.curve ? lesson.positive_stationary : lesson.cases[0].minimum}
          interval={lesson.curve ? lesson.given.interval : undefined}
          zeros={
            lesson.curve && lesson.negative_root
              ? [
                  { x: lesson.negative_root.x, label: "负零点（不计入）" },
                  { x: lesson.positive_stationary.x, label: "唯一正零点（相切）" },
                ]
              : []
          }
        />
        <p className="text-ui-sm">
          {lesson.curve
            ? "曲线在正零点处接触横轴后返回；阴影区间内比较标出的端点与驻点。播放会解释为什么原题条件确定这条曲线。"
            : "当前形状的最低处高于横轴，没有正零点。切换三种情形，比较最低点位置怎样改变正零点数量。"}
        </p>
        <div className="edu-reasoning-known text-ui-sm">
          <MathContent
            content={`本题 $f(0)=${lesson.given.constant}>0$；最值只看 $[${lesson.given.interval.join(",")}]$。`}
          />
        </div>
      </div>
    );
  const zeros =
    scene === "factor" && lesson.solved && lesson.negative_root
      ? [
          { x: lesson.negative_root.x, label: "负零点" },
          { x: lesson.positive_stationary.x, label: "正重根" },
        ]
      : [{ x: lesson.positive_stationary.x, label: "正驻点 r" }];
  return (
    <div>
      <Curve curve={lesson.root_curve} zeros={zeros} highlight={lesson.positive_stationary} />
      <p className="text-ui-sm">
        {scene === "factor"
          ? "负零点穿过横轴；正重根只接触横轴。原题只要求正半轴的零点数量。"
          : "接触横轴与切线水平必须发生在同一个正驻点 r。图形用来解释这个条件，参数稍后由等式求出。"}
      </p>
      {scene === "read" && (
        <div className="edu-reasoning-known text-ui-sm">
          <MathContent
            content={`本题 $f(0)=${lesson.given.constant}>0$；求最值的区间是 $[${lesson.given.interval.join(",")}]$。`}
          />
        </div>
      )}
    </div>
  );
}

function NumberLine({
  line,
  local,
}: {
  line: NonNullable<NonnegativeReasoning["number_line"]>;
  local: number;
}) {
  const [lo, hi] = line.range,
    x = (value: number) => 35 + ((value - lo) / (hi - lo)) * 450;
  const segments = line.positions.length - 1;
  return (
    <svg
      viewBox="0 0 520 160"
      className="edu-teaching-svg"
      role="img"
      aria-label="按原题所求依次代入并计算"
    >
      <line x1="30" x2="490" y1="94" y2="94" className="edu-visual-axis" />
      {line.ticks.map((tick) => (
        <g key={tick.value}>
          <line
            x1={x(tick.value)}
            x2={x(tick.value)}
            y1="88"
            y2="100"
            className="edu-visual-axis"
          />
          <text x={x(tick.value)} y="124" textAnchor="middle" className="edu-visual-label">
            {tick.label}
          </text>
        </g>
      ))}
      {line.positions.slice(1).map((to, i) => {
        const from = line.positions[i],
          amount = clamp(local * segments - i),
          end = from + (to - from) * amount;
        return (
          <g key={i} data-number-line-term={i}>
            <line
              x1={x(from)}
              x2={x(end)}
              y1={32 + i * 17}
              y2={32 + i * 17}
              className="edu-reasoning-function"
            />
            {amount > 0.98 && (
              <path
                d={`M${x(to) - (to >= from ? 8 : -8)} ${25 + i * 17} L${x(to)} ${32 + i * 17} L${x(to) - (to >= from ? 8 : -8)} ${39 + i * 17}`}
                className="edu-reasoning-function"
              />
            )}
          </g>
        );
      })}
    </svg>
  );
}

function NonnegativeScene({
  lesson,
  scene,
  local,
  index,
}: {
  lesson: NonnegativeReasoning;
  scene: string;
  local: number;
  index: number;
}) {
  if (scene === "solve_variable" && lesson.variables) {
    const count =
      lesson.steps.slice(0, index + 1).filter((step) => step.scene === "solve_variable").length - 1;
    const variable = lesson.variables[count];
    const phase = Math.min(2, Math.floor(local * 3));
    const equation = [variable.equation, variable.intermediate, variable.solved_equation][phase];
    const operation = phase === 0 ? variable.operation1 : variable.operation2;
    return (
      <div>
        <p className="text-ui-sm font-semibold">
          {phase === 0
            ? "原条件得到的方程"
            : phase === 1
              ? "对等式两边执行相同运算"
              : "定位求出的变量值"}
        </p>
        <div className="edu-reasoning-equation text-ui-xl">
          <MathContent content={`$$${equation}$$`} />
        </div>
        {phase < 2 && (
          <div className="edu-reasoning-equal-operations">
            <div className="text-ui-lg">
              <MathContent content={`左边 $${operation || "+0"}$`} />
            </div>
            <div className="text-ui-lg">
              <MathContent content={`右边 $${operation || "+0"}$`} />
            </div>
          </div>
        )}
        {phase === 2 && (
          <div className="edu-reasoning-result text-ui-lg">
            <MathContent
              content={`$${variable.name}=${variable.label}$，变量值可以是负数或分数；原来的非负表达式仍等于零。`}
            />
          </div>
        )}
      </div>
    );
  }
  if ((scene === "combine" || scene === "result") && lesson.number_line)
    return (
      <div>
        <p className="text-ui-sm">按原题所求代入。每条箭头是一项实际贡献，向右为正，向左为负。</p>
        {lesson.term_curves && (
          <div className="edu-reasoning-term-curves">
            {lesson.term_curves.map((term, i) => (
              <Curve key={i} curve={term.curve} highlight={term.zero} />
            ))}
          </div>
        )}
        <NumberLine line={lesson.number_line} local={scene === "result" ? 1 : local} />
        <div className="edu-reasoning-result text-ui-lg">
          <MathContent content={`$${lesson.target}=${lesson.solved?.result}$`} />
        </div>
      </div>
    );
  if (lesson.term_curves) {
    const positive = scene === "positive_left" ? 0 : scene === "positive_right" ? 1 : -1;
    const zero = scene === "zero" || scene === "conditions";
    return (
      <div>
        <div className="edu-reasoning-terms edu-reasoning-term-curves">
          {lesson.term_curves.map((term, i) => (
            <section key={i} className="edu-reasoning-term" data-positive-term={positive === i}>
              <MathContent content={`$$${lesson.terms[i]}$$`} />
              <Curve
                curve={term.curve}
                highlight={zero ? term.zero : undefined}
                activeX={
                  positive === i
                    ? term.zero.x + (term.positive.x - term.zero.x) * (0.1 + 0.9 * local)
                    : undefined
                }
              />
              <p className="text-ui-caption">
                {zero
                  ? "只有标出的零点使这一项等于0"
                  : positive === i
                    ? "离开零点后，曲线上这一项的值大于0"
                    : i === 0
                      ? "根式的实数定义域内，曲线都在横轴上方或横轴上"
                      : "V形曲线始终在横轴上方或横轴上"}
              </p>
            </section>
          ))}
        </div>
        <p
          className={`text-ui-sm ${positive >= 0 ? "edu-reasoning-conflict" : "edu-reasoning-known"}`}
          data-contradiction={positive >= 0}
        >
          {positive >= 0
            ? "曲线上这一项已经大于0，另一项又不能为负，总和就大于0，与原题矛盾。"
            : zero
              ? "两条曲线必须各自到达零点；两张图的横轴不同，分别列出内部一次式等于0。"
              : "图形展示原题两项的非负性；变量a、b本身可以为负，不能把变量值和函数值混淆。"}
        </p>
      </div>
    );
  }
  const positive = scene === "positive_left" ? 0 : scene === "positive_right" ? 1 : -1;
  const zero = scene === "zero" || scene === "conditions";
  return (
    <div>
      <div className="edu-reasoning-terms">
        {lesson.terms.map((term, i) => (
          <section key={term} data-positive-term={positive === i} className="edu-reasoning-term">
            <MathContent content={`$$${term}$$`} />
            <svg
              viewBox="0 0 220 150"
              className="edu-teaching-svg"
              role="img"
              aria-label={
                zero ? "该表达式必须为零" : positive === i ? "假设这一非负项为正" : "这一项不能为负"
              }
            >
              <line x1="20" x2="200" y1="120" y2="120" className="edu-visual-axis" />
              {positive === i ? (
                <rect
                  x="72"
                  y={120 - (25 + 75 * local)}
                  width="76"
                  height={25 + 75 * local}
                  rx="8"
                  className="edu-reasoning-positive"
                />
              ) : (
                !zero && (
                  <rect
                    x="72"
                    y="55"
                    width="76"
                    height="65"
                    rx="8"
                    className="edu-reasoning-placeholder"
                  />
                )
              )}
              <text x="110" y="144" textAnchor="middle" className="edu-visual-label">
                {zero ? "= 0" : positive === i ? "> 0（假设）" : "≥ 0"}
              </text>
            </svg>
          </section>
        ))}
      </div>
      <p
        className={`text-ui-sm ${positive >= 0 ? "edu-reasoning-conflict" : "edu-reasoning-known"}`}
        data-contradiction={positive >= 0}
      >
        {positive >= 0
          ? "正的一项加上非负的一项，总和必然大于零，与原条件总和为零矛盾。"
          : zero
            ? "任意一项为正都会矛盾，因此两个表达式必须同时为零。"
            : "高度只示意非负性质，尚未求出表达式或变量的数值。"}
      </p>
    </div>
  );
}

export function ProblemAnimation({
  visual,
  animation,
  index,
}: {
  visual: Animation;
  animation: AnimationState;
  index: number;
}) {
  const lesson = visual.reasoning_lesson;
  if (!lesson) return null;
  const step = lesson.steps[index],
    next = lesson.steps[index + 1];
  const end = next?.at ?? 1,
    local = end > step.at ? clamp((animation.progress - step.at) / (end - step.at)) : 1;
  return (
    <div
      className="edu-reasoning-lesson"
      data-reasoning-kind={lesson.kind}
      data-reasoning-scene={step.scene}
    >
      <div className="edu-reasoning-header">
        <p className="text-ui-xs text-foreground-subtle">本题条件与所求</p>
        <MathContent content={`$$${lesson.problem}$$`} />
        <MathContent content={lesson.goal} />
      </div>
      <div className="edu-reasoning-body">
        <div className="edu-reasoning-scene">
          {lesson.kind === "function" ? (
            <FunctionScene
              lesson={lesson}
              scene={step.scene}
              local={local}
              start={step.at}
              end={end}
              animation={animation}
            />
          ) : (
            <NonnegativeScene lesson={lesson} scene={step.scene} local={local} index={index} />
          )}
        </div>
        <section className="edu-reasoning-step" aria-label="当前原题推理步骤">
          <h4 className="text-ui-lg font-semibold" data-testid="reasoning-step-title">
            {step.title}
          </h4>
          <div className="edu-reasoning-given text-ui-sm">
            <span className="text-ui-xs text-foreground-subtle">使用的条件</span>
            <MathContent content={step.given} />
          </div>
          <div className="edu-reasoning-action text-ui-sm">
            <span className="text-ui-xs text-foreground-subtle">这一步做什么</span>
            <MathContent content={step.action} />
          </div>
          <div className="edu-reasoning-formula text-ui-base" data-testid="reasoning-step-formula">
            <MathContent content={`$$${step.formula}$$`} />
          </div>
          <div className="text-ui-sm">
            <span className="text-ui-xs text-foreground-subtle">为什么成立</span>
            <MathContent content={step.rule} />
          </div>
          {index === lesson.steps.length - 1 && lesson.mode === "hint" && (
            <p className="mt-3 text-ui-sm text-foreground-subtle">
              已得到可继续求解的条件；参数与最终所求由你尝试。
            </p>
          )}
        </section>
      </div>
    </div>
  );
}
