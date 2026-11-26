import { Button } from "@zcode/ui/button";
import { ChartNoAxesCombined } from "lucide-react";
import type { LearningOverview } from "./contract.js";

export function LearningTrend({
  days,
  onPractice,
}: {
  days: LearningOverview["daily"];
  onPractice: () => void;
}) {
  const total = days.reduce((sum, day) => sum + day.attempts, 0);
  const peak = Math.max(1, ...days.map((day) => day.attempts));
  return (
    <section className="edu-card edu-learning-trend" aria-label="近七日学习记录">
      <div className="edu-dashboard-heading">
        <h3 className="text-ui-lg font-medium">近七日练习</h3>
        <span className="text-ui-xs text-foreground-subtle">本产品实际作答 · {total} 次</span>
      </div>
      {total ? (
        <figure aria-label="近七日练习趋势">
          <div className="edu-map-daily">
            {days.map((day) => (
              <div
                key={day.date}
                className="edu-map-day"
                data-attempts={day.attempts}
                aria-label={`${day.date} 作答 ${day.attempts} 次，答对 ${day.correct} 次`}
              >
                <span className="text-ui-xs tabular-nums">{day.attempts}</span>
                <div className="edu-map-day-track" aria-hidden="true">
                  <i
                    className="edu-map-day-total"
                    style={{ height: `${(100 * day.attempts) / peak}%` }}
                  />
                  <i
                    className="edu-map-day-correct"
                    style={{ height: `${(100 * day.correct) / peak}%` }}
                  />
                </div>
                <span className="text-ui-xs text-foreground-subtle">
                  {day.date.slice(5).replace("-", "/")}
                </span>
              </div>
            ))}
          </div>
          <figcaption className="text-ui-xs text-foreground-subtle edu-map-trend-legend">
            <span>
              <i className="edu-map-day-total" />
              总作答
            </span>
            <span>
              <i className="edu-map-day-correct" />
              答对（含辅助与重做）
            </span>
          </figcaption>
        </figure>
      ) : (
        <div className="edu-map-trend-empty">
          <ChartNoAxesCombined className="size-7 text-foreground-subtle" />
          <p className="text-ui-sm text-foreground-subtle">
            完成新练习后，这里会展示每天的作答变化。
          </p>
          <Button variant="outline" size="sm" onClick={onPractice}>
            开始一次练习
          </Button>
        </div>
      )}
    </section>
  );
}
