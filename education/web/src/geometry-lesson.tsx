import { Button } from "@zcode/ui/button";
import type { TeachingVisual } from "./contract.js";
import type { AnimationState } from "./use-teaching-animation.js";
import { MathContent } from "./learning-content.js";
import { FunctionFigure } from "./teaching-plots.js";
import { geometrySnapshot, geometryStep, GeometryAnimationFigure } from "./geometry-animation.js";
type Animation = Extract<TeachingVisual, { kind: "animation_scene" }>;

export function GeometryLesson({
  visual,
  animation,
}: {
  visual: Animation;
  animation: AnimationState;
}) {
  const lesson = visual.lesson;
  if (!lesson) return <GeometryAnimationFigure visual={visual} progress={animation.progress} />;
  const index = geometryStep(visual, animation.progress),
    step = lesson.steps[index];
  const s = geometrySnapshot(visual, animation.progress);
  const coincidence = s?.coincident;
  const exceptional = coincidence && index >= 2 && lesson.goal === "ratio";
  const labels = visual.params?.labels;
  const formula = exceptional
    ? lesson.mode === "solution" && labels && lesson.helper_labels
      ? `${labels.d}${labels.e}=${labels.d}${lesson.helper_labels.h},\\quad ${labels.d}${labels.f}=${labels.d}${lesson.helper_labels.k}`
      : undefined
    : step.formula;
  const portion =
    lesson.coincidence_x !== undefined &&
    visual.params?.from_x !== undefined &&
    visual.params.to_x !== undefined
      ? (lesson.coincidence_x - visual.params.from_x) / (visual.params.to_x - visual.params.from_x)
      : -1;
  return (
    <div className="edu-geometry-lesson">
      <div className="edu-geometry-lesson-body">
        <GeometryAnimationFigure visual={visual} progress={animation.progress} />
        <section className="edu-geometry-step-copy" aria-label="当前教学步骤">
          <p className="text-ui-xs text-foreground-subtle">
            第 {index + 1} / {lesson.steps.length} 步 ·{" "}
            {lesson.mode === "hint" ? "先尝试推理" : "解题过程"}
          </p>
          <h4 className="mt-2 text-ui-lg font-semibold" data-testid="geometry-lesson-step">
            {exceptional ? "重合时直接比较垂距" : step.title}
          </h4>
          <p className="mt-2 text-ui-sm">
            {exceptional
              ? "此刻两组点重合，直接比较两条垂距，不使用退化三角形的相似。"
              : step.explanation}
          </p>
          {index >= 2 &&
            !exceptional &&
            s &&
            lesson.coincidence_x !== undefined &&
            s.coincident && (
              <p className="mt-2 text-ui-sm text-foreground-subtle">
                此刻动点与垂足重合，直接比较垂距；不使用退化三角形的相似。
              </p>
            )}
          {index >= 2 && portion >= 0 && portion <= 1 && (
            <Button
              size="sm"
              variant="ghost"
              aria-label="查看垂足重合位置"
              onClick={() =>
                animation.seek(
                  lesson.motion_window[0] +
                    portion * (lesson.motion_window[1] - lesson.motion_window[0]),
                )
              }
            >
              查看垂足重合位置
            </Button>
          )}
          {formula && (
            <div className="edu-geometry-formula text-ui-base">
              <MathContent content={`$$\\begin{gathered}${formula}\\end{gathered}$$`} />
            </div>
          )}
          {index >= 3 && visual.plot && s && lesson.domain && (
            <div className="edu-geometry-function">
              <p className="mt-3 text-ui-xs text-foreground-subtle">
                横轴 {lesson.symbols.x}＝{labels?.a}
                {labels?.e}，纵轴 {lesson.symbols.y}＝{labels?.b}
                {labels?.f} · 与动点同步
              </p>
              <FunctionFigure
                visual={{ ...visual, ...visual.plot, kind: "function_plot" }}
                progress={
                  (s.x - visual.plot.domain[0]) / (visual.plot.domain[1] - visual.plot.domain[0])
                }
                endpoints={{ left: "open", right: lesson.domain.upper_closed ? "closed" : "open" }}
                variables={lesson.symbols}
                showCaption={false}
              />
              <p className="text-ui-xs text-foreground-subtle">
                亮点与动点同步；空心端点不取，实心端点可取。
              </p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
