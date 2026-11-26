export interface ChatModelChoice {
  model_id: string;
  model_version: number;
  reasoning_level: string;
}
export type ChatModelSelection = Partial<Record<"text" | "vision", ChatModelChoice>>;
export interface ChatModelEntry {
  id: string;
  name: string;
  provider_id: string;
  provider_label: string;
  version: number;
  supports_image: boolean;
  available: boolean;
  levels: string[];
  default_level: string;
}
export interface ChatModelsView {
  version: number;
  session: string;
  selection: ChatModelSelection;
  models: ChatModelEntry[];
  issues: string[];
}
