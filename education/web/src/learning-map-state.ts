import type { LearningMapNode, LearningOverview } from "./contract.js";

export type MapMode = "mixed" | "initial" | "recent";
export type DisplayNode = LearningMapNode & {
  status: "ready" | "review" | "diagnose" | "unseen";
  label: string;
  score: number | null;
  metric: string;
  source: string;
};
export const statusNames = {
  ready: "可进阶",
  review: "待巩固",
  diagnose: "待诊断",
  unseen: "尚无证据",
};
const rank = { review: 0, diagnose: 1, ready: 2, unseen: 3 };
export function displayNodes(data: LearningOverview, mode: MapMode): DisplayNode[] {
  const current = new Map(data.topics.map((topic) => [topic.id, topic]));
  return data.knowledge_map.nodes.map((node) => {
    const recent = current.get(node.id);
    if (mode !== "initial" && recent && recent.attempts > 0) {
      const due = recent.review?.status === "due";
      const status =
        due || recent.state === "needs_practice"
          ? "review"
          : recent.state === "steady"
            ? "ready"
            : "diagnose";
      return {
        ...node,
        status,
        label:
          due && recent.state !== "needs_practice"
            ? "待复习"
            : status === "diagnose"
              ? recent.state === "diagnose"
                ? "待诊断"
                : "练习中"
              : statusNames[status],
        score: recent.accuracy,
        metric: "独立首次正确率",
        source: "本产品近期练习",
      };
    }
    if (mode !== "recent" && node.initial) {
      const due = recent?.review?.status === "due";
      const status = due
        ? "review"
        : node.initial.status === "可进阶"
          ? "ready"
          : node.initial.status === "待巩固"
            ? "review"
            : "diagnose";
      return {
        ...node,
        status,
        label: due ? "建议复习" : statusNames[status],
        score: Math.round(node.initial.mastery * 100),
        metric: "掌握估计",
        source: "初始化画像",
      };
    }
    return {
      ...node,
      status: "unseen",
      label: statusNames.unseen,
      score: null,
      metric: "尚无独立作答证据",
      source: mode === "recent" ? "尚无本产品新练习" : "尚无画像或练习",
    };
  });
}
export function priority(a: DisplayNode, b: DisplayNode) {
  return (
    rank[a.status] - rank[b.status] ||
    Number(b.available) - Number(a.available) ||
    (a.score ?? 100) - (b.score ?? 100) ||
    a.title.localeCompare(b.title, "zh-CN")
  );
}
export type Point = { x: number; y: number };
function overviewNodes(nodes: DisplayNode[], limit: number, selected: string): DisplayNode[] {
  const ranked = [...nodes].sort(priority);
  const representatives = [
    nodes.find((node) => node.id === selected),
    ranked[0],
    ranked.find((node) => node.status === "ready"),
    ranked.find((node) => node.status === "diagnose"),
    ...ranked,
  ];
  return [
    ...new Map(
      representatives
        .filter((node): node is DisplayNode => node !== undefined)
        .map((node) => [node.id, node]),
    ).values(),
  ]
    .slice(0, limit)
    .sort(priority);
}
export function mapLayout(
  nodes: DisplayNode[],
  groups: LearningOverview["knowledge_map"]["groups"],
  width: number,
  group: string,
  selected = "",
) {
  if (group !== "all") {
    const columns = width < 600 ? 2 : Math.min(4, Math.floor(width / 200));
    return {
      width,
      height: Math.max(440, Math.ceil(nodes.length / columns) * 72 + 150),
      root: { x: width / 2, y: 38 },
      hubs: [] as { id: string; title: string; count: number; x: number; y: number }[],
      nodes: nodes.map((node, i) => ({
        ...node,
        x: (width / columns) * ((i % columns) + 0.5),
        y: 120 + Math.floor(i / columns) * 72,
      })),
    };
  }
  const compact = width < 700;
  const rows = Math.ceil(groups.length / 2);
  const height = Math.max(440, rows * 148 + 40);
  const hubs = groups.map((g, i) => ({
    ...g,
    x: width * (i % 2 === 0 ? (compact ? 0.25 : 0.36) : compact ? 0.75 : 0.64),
    y: 80 + Math.floor(i / 2) * 148,
  }));
  const placed = hubs.flatMap((hub, i) =>
    overviewNodes(
      nodes.filter((node) => node.group === hub.id),
      compact ? 1 : 4,
      selected,
    ).map((node, index) => ({
      ...node,
      x: compact ? hub.x : width * (i % 2 === 0 ? 0.13 : 0.87),
      y: compact ? hub.y + 46 : hub.y - 45 + index * 32,
    })),
  );
  return {
    width,
    height,
    root: { x: width / 2, y: compact ? 25 : height / 2 },
    hubs,
    nodes: placed,
  };
}
