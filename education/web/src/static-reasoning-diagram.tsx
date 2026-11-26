import type { TeachingVisual } from "./contract.js";
import { Curve } from "./problem-animation.js";
import { MathContent } from "./learning-content.js";

type Diagram = Extract<TeachingVisual, { kind: "reasoning_diagram" }>;
export function StaticReasoningDiagram({ visual }: { visual: Diagram }) {
  const lesson = visual.reasoning_lesson;
  if (lesson?.kind === "function")
    return (
      <div data-static-reasoning="function" className="min-w-0 space-y-3">
        <MathContent content={`**当前原题：** $${lesson.problem}$`} />
        {lesson.mode === "hint" ? (
          <>
            <p className="text-ui-sm text-foreground-subtle">
              先比较最低点与横轴的位置。横轴使用 x/r，r 尚未求出；保留原题函数族，观察零点数量。
            </p>
            {lesson.cases.map((item, i) => (
              <Curve
                key={i}
                curve={item.curve}
                highlight={item.minimum}
                label={`${item.label}：${item.root_count} 个正零点（横轴 x/r）`}
              />
            ))}
          </>
        ) : (
          <>
            {lesson.curve && (
              <Curve
                curve={lesson.curve}
                interval={lesson.given.interval}
                label="原题函数：区间内候选点与最值"
              />
            )}
            {lesson.derivative_curve && (
              <Curve
                curve={lesson.derivative_curve}
                interval={lesson.given.interval}
                label="导函数：符号决定函数增减"
              />
            )}
          </>
        )}
      </div>
    );
  if (lesson?.kind === "nonnegative")
    return (
      <div data-static-reasoning="nonnegative" className="min-w-0 space-y-3">
        <MathContent content={`**原式：** $${lesson.problem}$`} />
        <p className="text-ui-sm text-foreground-subtle">
          {lesson.mode === "hint"
            ? "两幅曲线分别用各自的一次式作横轴，观察根式与绝对值的函数值都非负；变量本身可以为负。"
            : "两幅曲线的横轴分别对应原题中的两个变量，圆点表示各表达式归零的位置；变量本身可以为负。"}
        </p>
        {lesson.term_curves?.map((term, i) => (
          <Curve
            key={i}
            curve={term.curve}
            highlight={lesson.mode === "solution" ? term.zero : undefined}
            label={i === 0 ? "根式项：函数值不小于零" : "绝对值项：函数值不小于零"}
          />
        ))}
        <MathContent
          content={`**接下来使用的条件：** $${lesson.steps.find((step) => step.scene === "conditions")?.formula || lesson.steps[1]?.formula || ""}$`}
        />
      </div>
    );
  const algebra = visual.algebra_lesson;
  if (algebra)
    return (
      <div data-static-reasoning="identity" className="min-w-0 space-y-3">
        <svg
          viewBox="0 0 640 330"
          role="img"
          aria-label="恒成立的变化项与固定项"
          className="edu-teaching-svg"
        >
          <text x="320" y="28" textAnchor="middle" className="edu-visual-label">
            让同一个输入下的两边始终相等
          </text>
          <rect
            x="30"
            y="48"
            width="580"
            height="62"
            rx="8"
            className="edu-visual-grid"
            fill="none"
          />
          <text x="320" y="84" textAnchor="middle" className="edu-visual-label">
            {algebra.equation}
          </text>
          <path
            d="M320 115 L320 142 M315 136 L320 142 L325 136"
            className="edu-visual-axis"
            fill="none"
          />
          <rect
            x="30"
            y="153"
            width="580"
            height="62"
            rx="8"
            className="edu-visual-grid"
            fill="none"
          />
          <text x="320" y="188" textAnchor="middle" className="edu-visual-label">
            {algebra.rearranged}
          </text>
          <text x="160" y="254" textAnchor="middle" className="edu-visual-label">
            x 改变 → 比较变化项
          </text>
          <text x="465" y="254" textAnchor="middle" className="edu-visual-label">
            x=0 → 比较固定项
          </text>
          <text x="320" y="298" textAnchor="middle" className="edu-visual-label">
            对所有 x 成立，才是恒等关系
          </text>
        </svg>
        <MathContent content={`$${algebra.conditions.join("\\quad ")}$`} />
      </div>
    );
  return <p className="text-ui-sm text-foreground-subtle">图解缺少原题构造，请重新提问。</p>;
}
