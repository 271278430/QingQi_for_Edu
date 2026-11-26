import type { TeachingVisual } from "./teaching-visual.js";
export interface TeachingScope {
  version: string;
  available_parts: number[];
  active_part: number;
  units: {
    part: number;
    mode: string;
    label: string;
    allow_final_answer: boolean;
  }[];
}
export interface TeachingStreamEvent {
  kind: "progress" | "scope" | "reset" | "delta" | "done" | "error";
  seq: number;
  request_id: string;
  text?: string;
  prefix?: string;
  scope?: TeachingScope;
  part?: number;
  value?: unknown;
  error?: string;
  message?: string;
  status?: number;
  recoverable?: boolean;
}
/** Student-visible reply and strategy; the full TeachingPlan stays with the owner. */
export interface TeachingRoute {
  intents?: string[];
  teaching?: {
    label?: string;
    mode?: string;
    reason?: string;
    display_mode?: string;
  };
}

export interface TeachingResponse {
  run_id?: number;
  text: string;
  route?: TeachingRoute;
  teaching_action: string;
  evidence_refs: string[];
  step_refs: number[];
  model_inference?: boolean;
  cache_hit?: boolean;
  visuals?: TeachingVisual[];
  visual_version?: string;
  tutoring_scope?: TeachingScope;
  [key: string]: unknown;
}
