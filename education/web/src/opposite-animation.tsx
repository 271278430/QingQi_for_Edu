import { numberLabel } from "./math-number.js";

export function OppositeAnimation({
  value,
  reveal,
  range,
  title,
}: {
  value: number;
  reveal: number;
  range: [number, number];
  title: string;
}) {
  const x = (n: number) => 45 + ((n - range[0]) / (range[1] - range[0])) * 550;
  const center = x(0),
    right = x(value),
    left = x(-value);
  return (
    <svg
      viewBox="0 0 640 260"
      role="img"
      aria-label={title}
      className="edu-animation-svg edu-teaching-svg text-ui-caption"
      data-opposite-value={value}
      data-opposite-mirror={-value}
    >
      <line x1="35" x2="610" y1="150" y2="150" className="edu-visual-axis" />
      <line
        x1={center}
        x2={center}
        y1="90"
        y2="205"
        className="edu-visual-axis"
        strokeDasharray="5 4"
      />
      <text x={center} y="222" textAnchor="middle" className="edu-visual-label">
        原点 0
      </text>
      {value > 1e-8 ? (
        <>
          <circle cx={left} cy="150" r="8" className="edu-visual-point" />
          <circle cx={right} cy="150" r="8" className="edu-visual-point" />
          <text
            x={left}
            y="185"
            textAnchor="middle"
            className="edu-visual-label"
          >
            {numberLabel(-value)}
          </text>
          <text
            x={right}
            y="185"
            textAnchor="middle"
            className="edu-visual-label"
          >
            {numberLabel(value)}
          </text>
        </>
      ) : (
        <circle cx={center} cy="150" r="8" className="edu-visual-point" />
      )}
      <text x="320" y="42" textAnchor="middle" className="edu-visual-label">
        两点关于原点对称
      </text>
      <text x="320" y="67" textAnchor="middle" className="edu-visual-label">
        相反方向 · 同样距离
      </text>
      {reveal >= 0.4 && (
        <>
          <line
            x1={left}
            x2={center}
            y1="118"
            y2="118"
            className="edu-visual-axis"
            strokeDasharray="5 4"
          />
          <line
            x1={center}
            x2={right}
            y1="118"
            y2="118"
            className="edu-visual-axis"
            strokeDasharray="5 4"
          />
          <text x="320" y="98" textAnchor="middle" className="edu-visual-label">
            左右两段虚线等长
          </text>
        </>
      )}
      {reveal >= 0.75 && (
        <text x="320" y="248" textAnchor="middle" className="edu-visual-label">
          相反数相加：{numberLabel(value)} + ({numberLabel(-value)}) = 0
        </text>
      )}
    </svg>
  );
}
