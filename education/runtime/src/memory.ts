import {
  createMemoryRecallState,
  filterMemorySelections,
  recordRecalledMemories,
  canStartMemoryRecall,
  MEMORY_RECALL_SESSION_CHARACTER_LIMIT,
} from "@zcode/core/memory";
import { z } from "zod";

const MemoryInput = z
  .object({
    episodes: z.array(z.record(z.string(), z.unknown())).max(100),
    facts: z.array(z.record(z.string(), z.unknown())).max(30),
  })
  .strict();
export function selectScopedMemory(value: unknown) {
  // 授权过滤先由唯一 SQLite owner 完成；这里只接受本轮只读候选，不扫描全局文件。
  const memory = MemoryInput.parse(value);
  const candidates = [
    ...memory.facts
      .slice(0, 2)
      .map((data, index) => ({ kind: "facts" as const, data, filename: `fact-${index}` })),
    ...memory.episodes.map((data, index) => ({
      kind: "episodes" as const,
      data,
      filename: `episode-${index}`,
    })),
    ...memory.facts
      .slice(2)
      .map((data, index) => ({ kind: "facts" as const, data, filename: `fact-${index + 2}` })),
  ];
  const state = createMemoryRecallState();
  const manifest = candidates.map((item) => ({
    filename: item.filename,
    filePath: item.filename,
    mtimeMs: Number(item.data.at ?? 0) * 1000,
  }));
  const selected = canStartMemoryRecall(state)
    ? filterMemorySelections({
        manifest,
        recalledPaths: state.recalledPaths,
        selectedFilenames: [...new Set(candidates.map((item) => item.filename))],
      })
    : [];
  const output: { episodes: Record<string, unknown>[]; facts: Record<string, unknown>[] } = {
    episodes: [],
    facts: [],
  };
  for (const entry of selected) {
    const candidate = candidates.find((item) => item.filename === entry.filename)!;
    const content = JSON.stringify(candidate.data);
    // 上游预算判断只检查已累计字符；加入整条记忆前需验证新总量，不能截断事实。
    if (!canStartMemoryRecall(state)) break;
    if (state.recalledContentCharacters + content.length > MEMORY_RECALL_SESSION_CHARACTER_LIMIT)
      continue;
    recordRecalledMemories(state, [
      {
        content,
        filePath: entry.filePath,
        header: entry.filename,
        mtimeMs: entry.mtimeMs,
        sizeBytes: Buffer.byteLength(content),
      },
    ]);
    output[candidate.kind].push(candidate.data);
  }
  return {
    ...output,
    recall_metrics: {
      source: "@zcode/core/memory",
      candidates: candidates.length,
      selected: output.episodes.length + output.facts.length,
      characters: state.recalledContentCharacters,
    },
  };
}
