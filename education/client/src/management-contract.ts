/** Read-only projections and versioned commands owned by the authenticated server. */
export interface ModelStatus {
  id: string;
  label: string;
  model: string;
  enabled: boolean;
  credential_ready: boolean;
  supports_image?: boolean;
}
export interface ModelProvider {
  model_enabled: boolean;
  uses?: ModelRole[];
  id: string;
  display_name: string;
  model: string;
  base_url: string;
  protocol: "openai" | "anthropic";
  supports_image: boolean;
  supports_tools: boolean;
  requires_key: boolean;
  credential_ready: boolean;
  readonly: boolean;
  version: number;
  timeout: number;
  max_tokens: number;
  json_mode: boolean;
  credential_ref?: string;
  tests: Record<
    string,
    { success: boolean; tested_at: number; message: string; code?: string }
  >;
}
export type ModelRole =
  | "text"
  | "vision"
  | "course8b"
  | "difficulty8b"
  | "review27b";
export interface ModelSettingsView {
  version: number;
  scope: string;
  providers: ModelProvider[];
  connections: ModelConnection[];
  secret_storage: string;
  selection: {
    mode: "split" | "shared";
    text_provider_id: string | null;
    vision_provider_id: string | null;
    source: "custom" | "deployment";
    worker_provider_ids?: Partial<
      Record<"course8b" | "difficulty8b" | "review27b", string | null>
    >;
  };
}
export interface ModelDefinition {
  key: string;
  model: string;
  config: Record<string, unknown>;
}
export interface ModelConnection {
  origin?: "deployment" | "custom";
  id: string;
  display_name: string;
  base_url: string;
  protocol: "openai" | "anthropic";
  requires_key: boolean;
  credential_ready: boolean;
  readonly: boolean;
  version: number;
  timeout: number;
  credential_ref?: string;
  models: ModelDefinition[];
}
export interface SystemSettings {
  version: number;
  app_name: string;
  notice: string;
  maintenance: boolean;
}
export interface ManagementOverview {
  settings: SystemSettings;
  models: ModelStatus[];
  runtime: string;
  counts: Record<string, number>;
  catalogue: {
    topics: number;
    questions: number;
    graph_nodes: number;
    source_items: number;
    generated_items: number;
    student_ready_items: number;
    grade: string;
  };
  deployment: { profile: string; label: string; health_verified: boolean };
  architecture_version: string;
  sample: boolean;
  recent_errors: { run_id: number; code: string }[];
  history: { epoch: number; suppress_imported: boolean; updated: number };
}
export interface HistoryClearResult {
  epoch: number;
  deleted: Record<string, number>;
  already_applied: boolean;
}
export interface ArchitectureModule {
  id: string;
  title: string;
  group: string;
  owner: string;
  description: string;
  files: string[];
  interfaces: string[];
  reuse: string[];
  limits: string[];
  summary: string;
  status: "implemented" | "configured_optional";
  bindings: { file: string; symbol: string; verified: boolean }[];
  scope?: {
    inputs: string[];
    outputs: string[];
    responsibilities: string[];
    boundaries: string[];
    calls: string[];
    steps: { id: string; title: string; detail: string; interface: string }[];
  };
}
export interface ArchitectureOverview {
  version: string;
  modules: ArchitectureModule[];
  tools: { name: string; transport: string; effect: string }[];
  skills: { id: string; intents: string[] }[];
  models: ModelStatus[];
  systems: {
    id: string;
    title: string;
    description: string;
    modules: string[];
  }[];
  panorama: SystemPanorama;
}
export type PanoramaPoint = [number, number];
export type PanoramaEdgeKind = "call" | "read" | "write" | "constraint";
export interface PanoramaNode {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  kind:
    | "module"
    | "frame"
    | "compact"
    | "step"
    | "service"
    | "rail"
    | "process"
    | "terminal";
  module_id?: string;
  title?: string;
  lines: string[];
  title_align?: "end";
  footnote?: string;
  step_number?: number;
}
export interface PanoramaEdge {
  id: string;
  source: string;
  target: string;
  points: PanoramaPoint[];
  kind: PanoramaEdgeKind;
  heads: "none" | "end" | "both";
  label: string;
  label_at?: PanoramaPoint;
  bridge?: PanoramaPoint;
}
export interface SystemPanorama {
  width: number;
  height: number;
  title?: string;
  legend_y?: number;
  groups: {
    id: string;
    title: string;
    x: number;
    y: number;
    width: number;
    height: number;
  }[];
  nodes: PanoramaNode[];
  edges: PanoramaEdge[];
  legend: { kind: PanoramaEdgeKind; label: string }[];
}
