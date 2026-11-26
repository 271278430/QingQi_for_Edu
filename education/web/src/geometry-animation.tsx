import { useId } from "react";
import type { TeachingVisual } from "./contract.js";
type Animation = Extract<TeachingVisual, { kind: "animation_scene" }>;

export function geometryStep(visual: Animation, progress: number) {
  return (visual.lesson?.steps || []).reduce(
    (last, step, index) => (step.at <= progress + 1e-9 ? index : last),
    0,
  );
}
export function geometrySnapshot(visual: Animation, progress: number) {
  const p = visual.params;
  if (!p?.side || !p.labels) return null;
  const a = p.side,
    rotation = visual.template === "triangle_rotation";
  const window = visual.lesson?.motion_window;
  const motion = window
    ? Math.max(0, Math.min(1, (progress - window[0]) / (window[1] - window[0]))) *
      visual.lesson!.rotation_fraction
    : progress;
  const r = rotation ? 1 : p.ratio!;
  const x = rotation ? p.ae! : p.from_x! + (p.to_x! - p.from_x!) * motion;
  const t = a - x,
    dx = a / (1 + r),
    dy = (a * r) / (1 + r);
  const f = (dx * dx + dy * dy - dx * t) / dy;
  const canonical = [
    [a, 0],
    [0, a],
    [0, 0],
    [dx, dy],
    [t, 0],
    [0, f],
  ];
  const display = ([u, v]: number[]) => [(a - u + v) / Math.SQRT2, (a - u - v) / Math.SQRT2];
  const names = [p.labels.a, p.labels.b, p.labels.c, p.labels.d, p.labels.e, p.labels.f];
  const points = canonical.map((point, i) => ({ label: names[i], xy: display(point) }));
  const angle = (-Math.PI / 2) * motion;
  if (rotation)
    for (const i of [0, 4, 2]) {
      const [u, v] = canonical[i],
        du = u - dx,
        dv = v - dy;
      points.push({
        label: points[i].label + "′",
        xy: display([
          dx + du * Math.cos(angle) - dv * Math.sin(angle),
          dy + du * Math.sin(angle) + dv * Math.cos(angle),
        ]),
      });
    }
  if (!rotation)
    for (const helper of visual.geometry?.helpers || [])
      points.push({ label: helper.label, xy: [helper.x, helper.y] });
  // 同一构造每帧重新计算交点；步骤时间不等于数学旋转或动点的进度。
  const de = Math.hypot(t - dx, dy),
    df = Math.hypot(dx, f - dy);
  const distance = (i: number, j: number) =>
    Math.hypot(points[i].xy[0] - points[j].xy[0], points[i].xy[1] - points[j].xy[1]);
  // 两组点都重合才走退化分支，不能在小比例时仅凭x的绝对误差误判。
  const coincident =
    !rotation && points.length >= 8 && distance(4, 6) < a * 1e-9 && distance(5, 7) < a * 1e-9;
  return {
    points,
    x,
    y: a - f,
    de,
    df,
    ratio: de / df,
    coincident,
    degrees: rotation ? motion * 90 : 90,
  };
}
export function GeometryAnimationFigure({
  visual,
  progress,
}: {
  visual: Animation;
  progress: number;
}) {
  const id = useId();
  const s = geometrySnapshot(visual, progress);
  if (!s || !visual.params?.side) return <p>动画缺少构图数据，请重新发送请求。</p>;
  const rotation = visual.template === "triangle_rotation",
    step = geometryStep(visual, progress);
  const rotating = rotation && (!visual.lesson || step >= 2);
  const completed = visual.lesson?.mode === "solution" && step === 4;
  const coordinates =
    !rotation &&
    visual.lesson?.mode === "solution" &&
    !visual.lesson.method &&
    (step === 1 || step === 2);
  const helpers = !rotation && Boolean(visual.geometry?.helpers?.length) && step >= 1;
  const a = visual.params.side;
  // 分别按轨迹宽高适配，避免一个extent让三角形被挤到画面下方，留出标签余量。
  const bounds = visual.geometry?.bounds || {
    xmin: 0,
    xmax: a * Math.SQRT2,
    ymin: 0,
    ymax: Math.max(a, visual.extent - 1),
  };
  const unit = Math.min(
    520 / Math.max(0.01, bounds.xmax - bounds.xmin),
    260 / Math.max(0.01, bounds.ymax - bounds.ymin),
  );
  const ox = (640 - (bounds.xmax - bounds.xmin) * unit) / 2;
  const world = ([u, v]: number[]) => [
    ox + (u - bounds.xmin) * unit,
    307 - (v - bounds.ymin) * unit,
  ];
  const xy = (i: number) => world(s.points[i].xy),
    x = (i: number) => xy(i)[0],
    y = (i: number) => xy(i)[1];
  const polygon = (indices: number[]) => indices.map((i) => xy(i).join(",")).join(" ");
  const visible = s.points.map((_, i) => i).filter((i) => i < 6 || rotating || helpers);
  const coincides = (i: number, j: number) => {
    if (
      !rotation &&
      ((i === 4 && j === 6) || (i === 6 && j === 4) || (i === 5 && j === 7) || (i === 7 && j === 5))
    )
      return s.coincident;
    return (
      Math.hypot(s.points[i].xy[0] - s.points[j].xy[0], s.points[i].xy[1] - s.points[j].xy[1]) <
      a * 1e-9
    );
  };
  const tick = (u: number, v: number, label: string, count = 1) => {
    const [dx, dy] = [x(v) - x(u), y(v) - y(u)],
      length = Math.hypot(dx, dy);
    const cx = (x(u) + x(v)) / 2,
      cy = (y(u) + y(v)) / 2;
    return (
      // 不同的等长组用不同数量刻痕，不能让AD=CD与DE=DF被误读为四条边都相等。
      <g key={label} data-length-mark={label} data-length-count={count}>
        {Array.from({ length: count }, (_, i) => {
          const shift = (i - (count - 1) / 2) * 5,
            px = cx + (dx / length) * shift,
            py = cy + (dy / length) * shift;
          return (
            <line
              key={i}
              x1={px - (dy / length) * 6}
              x2={px + (dy / length) * 6}
              y1={py + (dx / length) * 6}
              y2={py - (dx / length) * 6}
              className={completed ? "edu-geometry-match" : "edu-geometry-auxiliary"}
            />
          );
        })}
      </g>
    );
  };
  const rightAngle = (u: number, v: number, center = 3) => {
    const du = Math.hypot(x(u) - x(center), y(u) - y(center)),
      dv = Math.hypot(x(v) - x(center), y(v) - y(center));
    const p = [((x(u) - x(center)) / du) * 12, ((y(u) - y(center)) / du) * 12],
      q = [((x(v) - x(center)) / dv) * 12, ((y(v) - y(center)) / dv) * 12];
    if (du < 1e-8 || dv < 1e-8) return null;
    return (
      <polyline
        data-geometry-right-angle="true"
        points={`${x(center) + p[0]},${y(center) + p[1]} ${x(center) + p[0] + q[0]},${y(center) + p[1] + q[1]} ${x(center) + q[0]},${y(center) + q[1]}`}
        fill="none"
        className="edu-geometry-auxiliary"
      />
    );
  };
  return (
    <div data-geometry-progress={progress} className="edu-geometry-figure">
      <div className="edu-geometry-canvas">
        <svg
          viewBox="0 0 640 355"
          role="img"
          aria-label={visual.title}
          className="edu-teaching-svg text-ui-caption"
        >
          <defs>
            <marker
              id={`${id}-arrow`}
              viewBox="0 0 8 8"
              refX="7"
              refY="4"
              markerWidth="5"
              markerHeight="5"
              orient="auto"
            >
              <path d="M0,0 L8,4 L0,8 Z" className="edu-geometry-arrow" />
            </marker>
          </defs>
          <polygon points={polygon([0, 1, 2])} className="edu-geometry-fill edu-geometry-context" />
          {visual.geometry?.ray_end && (
            <line
              data-geometry-ray="true"
              x1={x(2)}
              y1={y(2)}
              x2={world([visual.geometry.ray_end.x, visual.geometry.ray_end.y])[0]}
              y2={world([visual.geometry.ray_end.x, visual.geometry.ray_end.y])[1]}
              markerEnd={`url(#${id}-arrow)`}
              className="edu-geometry-line"
              strokeDasharray="5 4"
            />
          )}
          {rotating && (
            <>
              <polygon points={polygon([2, 3, 5])} className="edu-geometry-fill" />
              <polygon
                points={polygon([6, 3, 7])}
                className="edu-geometry-secondary-fill"
                data-rotating-triangle="true"
              />
              <line
                data-rotating-edge="true"
                x1={x(6)}
                y1={y(6)}
                x2={x(8)}
                y2={y(8)}
                className="edu-geometry-auxiliary"
                strokeDasharray="5 4"
              />
              <path
                data-rotation-arrow="true"
                d={`M${x(3) - 30},${y(3)} A30,30 0 0,1 ${x(3)},${y(3) - 30}`}
                fill="none"
                markerEnd={`url(#${id}-arrow)`}
                className="edu-geometry-auxiliary"
              />
            </>
          )}
          {helpers && (
            <>
              {[6, 7].map((i) => (
                <line
                  key={i}
                  data-geometry-foot={i === 6 ? "h" : "k"}
                  x1={x(3)}
                  y1={y(3)}
                  x2={x(i)}
                  y2={y(i)}
                  className="edu-geometry-auxiliary"
                  strokeDasharray="5 4"
                />
              ))}
              {rightAngle(3, step >= 2 && !s.coincident ? 4 : 0, 6)}
              {rightAngle(3, step >= 2 && !s.coincident ? 5 : 1, 7)}
              {step >= 2 && !s.coincident && (
                <g data-similar-triangles="true">
                  <polygon points={polygon([3, 6, 4])} className="edu-geometry-fill" />
                  <polygon points={polygon([3, 7, 5])} className="edu-geometry-secondary-fill" />
                </g>
              )}
            </>
          )}
          {coordinates &&
            [0, 1].map((i) => (
              <line
                key={i}
                data-geometry-coordinate-axis={i === 0 ? "CA" : "CB"}
                x1={x(2)}
                y1={y(2)}
                x2={x(i)}
                y2={y(i)}
                className="edu-geometry-auxiliary"
                markerEnd={`url(#${id}-arrow)`}
              />
            ))}
          {(visual.geometry?.segments || [])
            .filter(
              (line) =>
                line.label !== visual.params!.labels!.c + visual.params!.labels!.d ||
                !visual.lesson ||
                (step >= 1 && (rotation || !visual.lesson?.method)),
            )
            .map((line, i) => (
              <line
                key={i}
                x1={x(line.source)}
                y1={y(line.source)}
                x2={x(line.target)}
                y2={y(line.target)}
                data-geometry-segment={line.label || i}
                data-geometry-auxiliary={line.role === "auxiliary" ? "true" : undefined}
                className={`edu-geometry-line edu-geometry-${line.role} ${completed && rotation && [line.target, line.source].includes(3) && [line.target, line.source].some((i) => i === 4 || i === 5) ? "edu-geometry-match" : ""}`}
                strokeDasharray={line.style === "dashed" ? "6 4" : undefined}
              />
            ))}
          {rotation && step >= 1 && (
            <>
              {tick(0, 3, "AD")}
              {tick(2, 3, "CD")}
            </>
          )}
          {completed && rotation && (
            <>
              {tick(3, 4, "DE", 2)}
              {tick(3, 5, "DF", 2)}
            </>
          )}
          {rotation && step === 1 ? rightAngle(0, 2) : (!rotation || step >= 3) && rightAngle(4, 5)}
          {rightAngle(0, 1, 2)}
          {!rotation &&
            coordinates &&
            step === 2 &&
            [4, 5].map((i) => (
              <line
                key={i}
                data-geometry-vector={i === 4 ? "DE" : "DF"}
                x1={x(3)}
                y1={y(3)}
                x2={x(i)}
                y2={y(i)}
                className="edu-geometry-auxiliary"
                markerEnd={`url(#${id}-arrow)`}
              />
            ))}
          {visible.map((i) => (
            <g key={s.points[i].label} data-geometry-point={s.points[i].label}>
              <circle cx={x(i)} cy={y(i)} r="4" className="edu-visual-point" />
            </g>
          ))}
        </svg>
        {/* 标签用HTML字体令牌，不随SVG缩到手机上只有几像素；位置仍读取同一几何快照。 */}
        {visible
          .filter((i) => visible.find((j) => coincides(i, j)) === i)
          .map((i) => (
            <span
              key={i}
              aria-hidden="true"
              data-geometry-label={s.points[i].label}
              className="edu-geometry-point-label text-ui-caption"
              style={{
                left: `${((x(i) + (i === 2 ? -18 : i === 5 ? 18 : i === 0 || i === 4 ? -14 : 8)) / 640) * 100}%`,
                top: `${((y(i) + ([0, 1, 3, 6, 7].includes(i) ? 22 : -12)) / 355) * 100}%`,
              }}
            >
              {visible
                .filter((j) => coincides(i, j))
                .map((j) => s.points[j].label)
                .join(" = ")}
            </span>
          ))}
      </div>
      <div className="edu-geometry-legend text-ui-xs">
        <span>
          <i />
          原题图形与指定射线
        </span>
        <span>
          <i />
          {coordinates
            ? `坐标轴沿${visual.params.labels!.c}${visual.params.labels!.a}、${visual.params.labels!.c}${visual.params.labels!.b}`
            : rotation
              ? "辅助线／旋转像"
              : "垂直关系／辅助线"}
        </span>
        {completed && rotation && (
          <span>
            <i />
            对应等长边
          </span>
        )}
      </div>
    </div>
  );
}
