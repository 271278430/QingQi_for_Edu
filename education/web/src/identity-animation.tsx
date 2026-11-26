import type { TeachingVisual } from "./contract.js";
import { MathContent } from "./learning-content.js";
type Animation = Extract<TeachingVisual, { kind: "animation_scene" }>;

export function IdentityAnimation({ visual, index }: { visual: Animation; index: number }) {
  const lesson = visual.algebra_lesson;
  if (!lesson) return <p>动画缺少原方程，请重新发送问题。</p>;
  const step = lesson.steps[index];
  const complete = step.phase === "conditions" || step.phase === "solution";
  const copies = complete ? 0 : (step.probe ?? 1);
  const story = lesson.story;
  return (
    <div
      className="edu-identity-lesson"
      data-identity-phase={step.phase}
      data-identity-probe={step.probe ?? ""}
    >
      <div className="edu-identity-header">
        <p className="text-ui-xs text-foreground-subtle">
          {story ? story.title : "同一条方程 · 每个 x 都必须成立"}
        </p>
        <MathContent content={`$$${story ? lesson.equation : lesson.rearranged}$$`} />
      </div>
      <div className="edu-identity-body">
        <div>
          {story ? (
            <div className="edu-story-recorders" data-testid="story-recorders">
              <p className="text-ui-sm">{story.setup}</p>
              <svg
                viewBox="0 0 620 120"
                className="edu-teaching-svg"
                role="img"
                aria-label="同一个输入送入两台积分记录器"
              >
                <rect
                  x="238"
                  y="8"
                  width="144"
                  height="46"
                  rx="12"
                  className="edu-identity-resolved"
                />
                <text x="310" y="37" textAnchor="middle" className="edu-visual-label">
                  {step.probe === undefined ? "同一个输入 x" : `输入 x = ${step.probe}`}
                </text>
                <path
                  d="M310 54 V76 H150 V108 M310 76 H470 V108"
                  className="edu-story-input-lines"
                />
                {[150, 470].map((x) => (
                  <path
                    key={x}
                    d={`M${x - 6} 98 L${x} 108 L${x + 6} 98`}
                    className="edu-story-input-lines"
                  />
                ))}
              </svg>
              <div className="edu-story-accounts">
                {[story.left, story.right].map((account, i) => (
                  <section
                    key={account.name}
                    className={`edu-story-account edu-story-account-${i}`}
                    aria-label={account.name}
                  >
                    <h4 className="text-ui-base font-semibold">{account.name}</h4>
                    <div className="text-ui-sm">
                      <MathContent
                        content={`每单位调整 $${account.rate}$ · 初始积分 $${account.offset}$`}
                      />
                    </div>
                    <div className="edu-story-total text-ui-lg" data-testid={`story-account-${i}`}>
                      <MathContent content={`$$${step.accounts?.[i] ?? account.expression}$$`} />
                    </div>
                  </section>
                ))}
              </div>
              <p className="edu-story-domain text-ui-xs text-foreground-subtle">
                {story.domain_note}
              </p>
            </div>
          ) : (
            <svg
              viewBox="0 0 620 250"
              className="edu-teaching-svg edu-identity-svg"
              role="img"
              aria-label="改变x时的系数拼片与固定常数"
            >
              <text x="170" y="30" textAnchor="middle" className="edu-visual-label">
                随 x 改变的部分
              </text>
              <text x="475" y="30" textAnchor="middle" className="edu-visual-label">
                始终相同的常数
              </text>
              {copies === 0 ? (
                <text x="170" y="115" textAnchor="middle" className="edu-identity-zero">
                  0
                </text>
              ) : (
                Array.from({ length: copies }, (_, i) => (
                  <g key={`${step.at}-${i}`}>
                    <rect
                      x={copies === 1 ? 118 : 62 + i * 114}
                      y="64"
                      width="102"
                      height="76"
                      rx="16"
                      className="edu-identity-coefficient"
                    />
                    <text
                      x={copies === 1 ? 169 : 113 + i * 114}
                      y="107"
                      textAnchor="middle"
                      className="edu-identity-tile-label"
                    >
                      {step.phase === "rearrange" ? "系数 × x" : "系数块"}
                    </text>
                  </g>
                ))
              )}
              <text x="323" y="112" textAnchor="middle" className="edu-identity-equals">
                =
              </text>
              <rect
                x="419"
                y="64"
                width="112"
                height="76"
                rx="16"
                className={complete ? "edu-identity-resolved" : "edu-identity-constant"}
              />
              <text x="475" y="108" textAnchor="middle" className="edu-identity-tile-label">
                {complete ? "0" : "固定常数"}
              </text>
              <text x="170" y="171" textAnchor="middle" className="edu-visual-label">
                {complete
                  ? "系数必须为 0"
                  : step.phase === "rearrange"
                    ? "份数由 x 决定"
                    : `${copies} 份同样的系数`}
              </text>
              <text x="475" y="171" textAnchor="middle" className="edu-visual-label">
                {complete ? "常数也必须为 0" : "换一个 x，它也不改变"}
              </text>
              <line x1="140" x2="480" y1="218" y2="218" className="edu-visual-axis" />
              {[0, 1, 2].map((probe) => (
                <g key={probe}>
                  <circle
                    cx={140 + probe * 170}
                    cy="218"
                    r={step.probe === probe ? 9 : 5}
                    className={step.probe === probe ? "edu-visual-point" : "edu-identity-probe"}
                  />
                  <text
                    x={140 + probe * 170}
                    y="244"
                    textAnchor="middle"
                    className="edu-visual-label"
                  >
                    x = {probe}
                  </text>
                </g>
              ))}
            </svg>
          )}
          {!story && (
            <div className="edu-identity-key text-ui-sm">
              <MathContent
                content={
                  step.phase === "rearrange"
                    ? `蓝色部分表示 $(${lesson.coefficient_symbol})x$，右边是固定的 $${lesson.constant_symbol}$。`
                    : complete
                      ? "两个条件必须同时满足，才能对每个 x 都成立。"
                      : `每块表示 $${lesson.coefficient_symbol}$，固定常数表示 $${lesson.constant_symbol}$。`
                }
              />
            </div>
          )}
        </div>
        <section className="edu-identity-step" aria-label="当前恒等式教学步骤">
          <h4 className="text-ui-lg font-semibold" data-testid="identity-lesson-step">
            {step.title}
          </h4>
          <p className="mt-3 text-ui-sm">{step.explanation}</p>
          <div className="edu-identity-formula text-ui-base">
            <MathContent content={`$$${step.formula}$$`} />
          </div>
          {complete && lesson.mode === "hint" && (
            <p className="text-ui-sm text-foreground-subtle">
              接下来由你试着求出参数，最后的结果先保留。
            </p>
          )}
        </section>
      </div>
    </div>
  );
}
