import { z } from "zod";
export const TOOL_NAMES = [
  "course_search",
  "course_context",
  "review_arithmetic",
  "difficulty_candidates",
  "worker_course8b",
  "worker_difficulty8b",
  "worker_review27b",
  "render_teaching_visual",
  "solve_geometry",
  "analyze_function",
  "recommend_practice",
  "preview_learning_path",
  "read_learning_dashboard",
] as const;
export const ToolName = z.enum(TOOL_NAMES);
export const Frame = z
  .object({
    id: z.number().int(),
    op: z.enum([
      "init",
      "skills",
      "plan",
      "recall",
      "contracts",
      "call",
      "close",
    ]),
    input: z.record(z.string(), z.unknown()),
  })
  .strict();
export const ToolSpec = z
  .object({
    name: ToolName,
    description: z.string(),
    input_schema: z.record(z.string(), z.unknown()),
    output_schema: z.record(z.string(), z.unknown()),
    transport: z.enum(["mcp", "local", "model"]),
    timeout: z.number().positive(),
    version: z.string(),
    effect: z.literal("read"),
    retries: z.number().int().nonnegative(),
  })
  .strict();
export type RegisteredTool = z.infer<typeof ToolSpec>;
export interface HandlerRequest {
  name: string;
  arguments: unknown;
  trace: { agentId?: string; childSessionId?: string; traceId: string };
}
export type InvokeHandler = (
  request: HandlerRequest,
  signal?: AbortSignal,
) => Promise<unknown>;
export interface RuntimeFailure {
  code: string;
  message: string;
  recoverable: boolean;
  retry_after?: number;
}
