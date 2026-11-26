import { useEffect, useRef, useState } from "react";
import { Button } from "@zcode/ui/button";
import { Minus, Plus, Scan } from "lucide-react";
import type { LearningOverview } from "./contract.js";
import { mapLayout, statusNames, type DisplayNode, type Point } from "./learning-map-state.js";

const line = (a: Point, b: Point) =>
  `M${a.x},${a.y} C${(a.x + b.x) / 2},${a.y} ${(a.x + b.x) / 2},${b.y} ${b.x},${b.y}`;
export function LearningMapCanvas({
  nodes,
  groups,
  edges,
  group,
  selected,
  onSelect,
  onGroup,
}: {
  nodes: DisplayNode[];
  groups: LearningOverview["knowledge_map"]["groups"];
  edges: LearningOverview["knowledge_map"]["edges"];
  group: string;
  selected: string;
  onSelect: (id: string) => void;
  onGroup: (id: string) => void;
}) {
  const viewport = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(960);
  const [zoom, setZoom] = useState(1);
  useEffect(() => {
    const element = viewport.current;
    if (!element) return;
    const measure = () => setWidth(Math.max(300, Math.round(element.clientWidth)));
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(element);
    return () => observer.disconnect();
  }, []);
  const layout = mapLayout(nodes, groups, width, group, selected);
  const locations = new Map(layout.nodes.map((node) => [node.id, node]));
  const centerTitle =
    group === "all" ? "数学学情" : groups.find((g) => g.id === group)?.title || "知识点";
  return (
    <div>
      <div className="edu-map-viewport" ref={viewport} aria-label="图谱浏览区域">
        <div style={{ width: layout.width * zoom, height: layout.height * zoom }}>
          <div
            className="edu-map-surface"
            style={{
              width: layout.width,
              height: layout.height,
              transform: `scale(${zoom})`,
            }}
          >
            <svg
              className="edu-map-lines"
              width={layout.width}
              height={layout.height}
              aria-hidden="true"
            >
              {layout.hubs.map((hub) => (
                <path key={hub.id} d={line(layout.root, hub)} className="edu-map-membership" />
              ))}
              {layout.nodes.map((node) => (
                <path
                  key={node.id}
                  d={line(layout.hubs.find((hub) => hub.id === node.group) || layout.root, node)}
                  className="edu-map-membership"
                />
              ))}
              {group !== "all" &&
                edges.map((edge) => {
                  const a = locations.get(edge.source),
                    b = locations.get(edge.target);
                  return a && b ? (
                    <path
                      key={`${edge.source}-${edge.target}`}
                      d={line(a, b)}
                      className="edu-map-prerequisite"
                    />
                  ) : null;
                })}
            </svg>
            <div
              className={`edu-map-root ${width < 700 || group !== "all" ? "edu-map-root-compact" : ""}`}
              style={{ left: layout.root.x, top: layout.root.y }}
            >
              <span className="text-ui-sm font-medium">{centerTitle}</span>
              {group === "all" && width >= 700 && (
                <span className="text-ui-xs text-foreground-subtle">知识连接</span>
              )}
            </div>
            {layout.hubs.map((hub) => (
              <button
                key={hub.id}
                type="button"
                className="edu-map-hub"
                style={{ left: hub.x, top: hub.y }}
                onClick={() => onGroup(hub.id)}
                aria-label={`展开${hub.title}`}
              >
                <span className="text-ui-sm font-medium">{hub.title}</span>
                <span className="text-ui-xs text-foreground-subtle">{hub.count} 个知识点</span>
                <span className="edu-map-hub-distribution" aria-hidden="true">
                  {Object.keys(statusNames).map((status) => (
                    <i
                      key={status}
                      data-status={status}
                      style={{
                        flexGrow: nodes.filter(
                          (node) => node.group === hub.id && node.status === status,
                        ).length,
                      }}
                    />
                  ))}
                </span>
              </button>
            ))}
            {layout.nodes.map((node) => (
              <button
                key={node.id}
                type="button"
                className={`edu-map-node ${group !== "all" ? "edu-map-node-full" : ""}`}
                data-status={node.status}
                data-selected={node.id === selected}
                style={{ left: node.x, top: node.y }}
                onClick={() => onSelect(node.id)}
                aria-label={`查看知识点 ${node.title}，${node.label}${node.score === null ? "" : `，${node.metric} ${node.score}%`}`}
                aria-pressed={node.id === selected}
                title={node.title}
              >
                <span className="edu-map-dot" />
                <span className="edu-map-node-title text-ui-xs">{node.title}</span>
                {node.score !== null && (
                  <span className="text-ui-xs tabular-nums">{node.score}%</span>
                )}
              </button>
            ))}
          </div>
        </div>
      </div>
      <div className="edu-map-footer text-ui-xs text-foreground-subtle">
        <p>
          {group === "all"
            ? `概览展示 ${layout.nodes.length} 个代表节点，点击分区展开全部。`
            : `本分区 ${nodes.length} 个节点，可滚动查看。`}
        </p>
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="icon"
            aria-label="缩小图谱"
            disabled={zoom <= 0.6}
            onClick={() => setZoom((value) => Math.max(0.6, +(value - 0.2).toFixed(1)))}
          >
            <Minus />
          </Button>
          <span className="min-w-10 text-center" data-testid="map-zoom">
            {Math.round(zoom * 100)}%
          </span>
          <Button
            variant="ghost"
            size="icon"
            aria-label="放大图谱"
            disabled={zoom >= 1.8}
            onClick={() => setZoom((value) => Math.min(1.8, +(value + 0.2).toFixed(1)))}
          >
            <Plus />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            aria-label="复位图谱"
            onClick={() => {
              setZoom(1);
              viewport.current?.scrollTo({ left: 0, top: 0 });
            }}
          >
            <Scan />
          </Button>
        </div>
      </div>
    </div>
  );
}
