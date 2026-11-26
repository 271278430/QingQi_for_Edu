import { useId } from "react";
import type { RefObject } from "react";
import {
  BookOpen,
  BrainCircuit,
  Database,
  GitBranch,
  Layers,
  MessageCircle,
  Monitor,
  Network,
  Route,
  Settings,
  ShieldCheck,
  Sparkles,
  Wrench,
  ChartNoAxesCombined,
  Image,
  ListChecks,
} from "lucide-react";
import type {
  ArchitectureOverview,
  PanoramaEdge,
  PanoramaNode,
  SystemPanorama,
} from "./contract.js";

function edgePath(edge: PanoramaEdge) {
  let path = `M ${edge.points[0].join(" ")}`;
  for (let i = 1; i < edge.points.length; i++) {
    const a = edge.points[i - 1],
      b = edge.points[i],
      bridge = edge.bridge;
    if (
      bridge &&
      a[1] === b[1] &&
      a[1] === bridge[1] &&
      a[0] < bridge[0] &&
      bridge[0] < b[0]
    )
      path += ` L ${bridge[0] - 6} ${bridge[1]} Q ${bridge[0]} ${bridge[1] - 8} ${bridge[0] + 6} ${bridge[1]}`;
    const c = edge.points[i + 1];
    if (c && !bridge) {
      const before = Math.hypot(b[0] - a[0], b[1] - a[1]);
      const after = Math.hypot(c[0] - b[0], c[1] - b[1]);
      const r = Math.min(8, before / 2, after / 2);
      if (r > 0) {
        const p = [
          b[0] - ((b[0] - a[0]) * r) / before,
          b[1] - ((b[1] - a[1]) * r) / before,
        ];
        const q = [
          b[0] + ((c[0] - b[0]) * r) / after,
          b[1] + ((c[1] - b[1]) * r) / after,
        ];
        path += ` L ${p.join(" ")} Q ${b.join(" ")} ${q.join(" ")}`;
        continue;
      }
    }
    path += ` L ${b.join(" ")}`;
  }
  return path;
}

const icons = {
  web: Monitor,
  permissions: ShieldCheck,
  management: Settings,
  tutoring: MessageCircle,
  path: Route,
  dashboard: ChartNoAxesCombined,
  practice: ListChecks,
  loop: BrainCircuit,
  routing: GitBranch,
  memory: Database,
  skills: Sparkles,
  tools: Wrench,
  models: Layers,
  visuals: Image,
  data: BookOpen,
  persistence: Network,
};

function Node({
  node,
  data,
  onSelect,
}: {
  node: PanoramaNode;
  data: ArchitectureOverview;
  onSelect: (id: string) => void;
}) {
  const module = data.modules.find((m) => m.id === node.module_id);
  const compact = node.kind === "step" || node.kind === "compact";
  const title = node.title ?? module?.title ?? "";
  const Icon = module ? icons[module.id as keyof typeof icons] : undefined;
  return (
    <g
      transform={`translate(${node.x} ${node.y})`}
      data-panorama-node={node.id}
      data-architecture-module={node.module_id}
      data-flow-step={node.step_number}
      className={`edu-panorama-node edu-panorama-node-${node.kind} edu-panorama-node-${node.id}`}
      role={module ? "button" : undefined}
      tabIndex={module ? 0 : undefined}
      aria-label={
        node.step_number
          ? `${String(node.step_number).padStart(2, "0")} ${title}`
          : module?.title
      }
      onClick={module ? () => onSelect(module.id) : undefined}
      onKeyDown={
        module
          ? (e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onSelect(module.id);
              }
            }
          : undefined
      }
    >
      {node.kind === "rail" ? (
        <path
          d={`M 0 1 H ${node.width}`}
          className="edu-panorama-line edu-panorama-line-call"
        />
      ) : (
        <>
          <rect
            data-node-shape
            width={node.width}
            height={node.height}
            rx={node.kind === "terminal" ? 16 : 12}
          />
          {node.step_number && (
            <>
              <circle cx={20} cy={20} r={12} className="edu-flow-step-badge" />
              <text
                data-node-text
                x={20}
                y={24}
                textAnchor="middle"
                className="text-ui-caption font-semibold edu-flow-step-number"
              >
                {String(node.step_number).padStart(2, "0")}
              </text>
            </>
          )}
          {Icon && !node.step_number && (
            <Icon
              x={16}
              y={12}
              width={18}
              height={18}
              className="edu-panorama-icon"
              aria-hidden="true"
            />
          )}
          <text
            data-node-text
            x={
              node.title_align === "end"
                ? node.width - 16
                : node.step_number || Icon
                  ? 44
                  : 16
            }
            y={compact ? 27 : 26}
            textAnchor={node.title_align === "end" ? "end" : "start"}
            className={`${compact || node.title_align === "end" ? "text-ui-base" : "text-ui-lg"} font-semibold edu-panorama-name`}
          >
            {title}
          </text>
          {node.lines.map((line, i) => (
            <text
              key={line}
              data-node-text
              x={16}
              y={48 + i * 18}
              className="text-ui-caption edu-panorama-description"
            >
              {line}
            </text>
          ))}
          {node.footnote && (
            <text
              data-node-text
              x={node.width / 2}
              y={node.height - 15}
              textAnchor="middle"
              className="text-ui-xs edu-panorama-description"
            >
              {node.footnote}
            </text>
          )}
        </>
      )}
    </g>
  );
}

export function ArchitectureSvg({
  data,
  diagram,
  zoom,
  svgRef,
  onSelect,
}: {
  data: ArchitectureOverview;
  diagram: SystemPanorama;
  zoom: number;
  svgRef: RefObject<SVGSVGElement | null>;
  onSelect: (id: string) => void;
}) {
  const identifier = useId().replace(/[^a-zA-Z0-9_-]/g, "");
  const p = diagram;
  const marker = (kind: string) => `pano-${identifier}-${kind}`;
  return (
    <svg
      ref={svgRef}
      xmlns="http://www.w3.org/2000/svg"
      viewBox={`0 0 ${p.width} ${p.height}`}
      width={p.width}
      height={p.height}
      className="edu-panorama-svg"
      style={{ width: `${zoom * p.width}px`, minWidth: `${zoom * p.width}px` }}
      data-system-panorama
      data-panorama-zoom={zoom}
      data-panorama-view="system"
      aria-label={p.title ?? "教育Agent系统架构全景图"}
    >
      <title>{p.title ?? "教育Agent系统架构全景图"}</title>
      <desc>
        Web四功能通过权限入口连接Agent
        Loop和学习服务；工具、模型、Skills与记忆支撑执行，Store负责唯一持久化，图示读取已接受结果。
      </desc>
      <defs>
        {p.legend.map(({ kind }) => (
          <marker
            key={kind}
            id={marker(kind)}
            viewBox="0 0 10 10"
            refX={9}
            refY={5}
            markerWidth={7}
            markerHeight={7}
            orient="auto-start-reverse"
          >
            <path
              d="M 0 0 L 10 5 L 0 10 z"
              className={`edu-panorama-arrow edu-panorama-arrow-${kind}`}
            />
          </marker>
        ))}
      </defs>
      <rect
        width={p.width}
        height={p.height}
        className="edu-panorama-background"
      />
      <text
        x={30}
        y={26}
        className="text-ui-xl font-semibold edu-panorama-name"
        data-diagram-heading
      >
        {p.title}
      </text>
      {p.groups.map((group) => (
        <g key={group.id} data-architecture-system={group.id}>
          <rect
            x={group.x}
            y={group.y}
            width={group.width}
            height={group.height}
            rx={12}
            className="edu-panorama-layer"
          />
        </g>
      ))}
      {p.nodes
        .filter((n) => n.kind === "frame")
        .map((node) => (
          <Node key={node.id} node={node} data={data} onSelect={onSelect} />
        ))}
      {p.edges.map((edge) => (
        <g key={edge.id} data-panorama-edge={edge.id}>
          {edge.bridge && (
            <path
              d={`M ${edge.bridge[0] - 6} ${edge.bridge[1]} Q ${edge.bridge[0]} ${edge.bridge[1] - 8} ${edge.bridge[0] + 6} ${edge.bridge[1]}`}
              className="edu-panorama-bridge"
            />
          )}
          <path
            d={edgePath(edge)}
            className={`edu-panorama-line edu-panorama-line-${edge.kind}`}
            markerEnd={
              edge.heads !== "none" ? `url(#${marker(edge.kind)})` : undefined
            }
            markerStart={
              edge.heads === "both" ? `url(#${marker(edge.kind)})` : undefined
            }
          />
          {edge.label && edge.label_at && (
            <g>
              <rect
                x={
                  edge.label_at[0] -
                  (Array.from(edge.label).reduce(
                    (n, c) => n + (c.charCodeAt(0) > 255 ? 12 : 7),
                    0,
                  ) +
                    16) /
                    2
                }
                y={edge.label_at[1] - 14}
                width={
                  Array.from(edge.label).reduce(
                    (n, c) => n + (c.charCodeAt(0) > 255 ? 12 : 7),
                    0,
                  ) + 16
                }
                height={20}
                rx={6}
                className="edu-panorama-label-background"
              />
              <text
                x={edge.label_at[0]}
                y={edge.label_at[1]}
                data-edge-label
                textAnchor="middle"
                className={`text-ui-caption edu-panorama-edge-label edu-panorama-label-${edge.kind}`}
              >
                {edge.label}
              </text>
            </g>
          )}
        </g>
      ))}
      {p.groups.map((group) => (
        <text
          key={group.id}
          x={group.x + 16}
          y={group.y + 24}
          className="text-ui-base font-semibold edu-panorama-layer-name"
        >
          {group.title}
        </text>
      ))}
      {p.nodes
        .filter((n) => n.kind !== "frame")
        .map((node) => (
          <Node key={node.id} node={node} data={data} onSelect={onSelect} />
        ))}
      {p.legend.map(({ kind, label }, i) => (
        <g
          key={kind}
          transform={`translate(${30 + (i * (p.width - 60)) / p.legend.length} ${p.legend_y ?? p.height - 54})`}
        >
          <path
            d="M 0 0 H 44"
            className={`edu-panorama-line edu-panorama-line-${kind}`}
            markerEnd={`url(#${marker(kind)})`}
          />
          <text
            x={57}
            y={4}
            className="text-ui-caption edu-panorama-description"
          >
            {label}
          </text>
        </g>
      ))}
      <text
        x={30}
        y={p.height - 6}
        className="text-ui-xs edu-panorama-description"
        data-diagram-note
      >
        箭头表示处理方向，分支按条件执行。模块节点可点击；源码与完整边界见模块说明。
      </text>
    </svg>
  );
}
