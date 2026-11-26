export interface PracticeItem {
  id: string;
  topic: string;
  title: string;
  expression: string;
  level: number;
  version: string;
  reason?: string;
  options?: string[];
  answer_kind?: string;
  answer_count?: number;
  source?: string;
  usable?: boolean;
  quality_note?: string;
  purpose?: string;
  kind?: string;
  group?: string;
}
export interface LearningSummary {
  turns: number;
  attempts: number;
  items: number;
  independent_attempts: number;
  independent_correct: number;
  assisted_attempts: number;
  accuracy: number | null;
}

interface TaskResult {
  status:
    | "ok"
    | "needs_source"
    | "no_candidates"
    | "limited_supply"
    | "unknown_topic";
  text: string;
}
export type StudentTask =
  | (TaskResult & { kind: "recommend"; items: PracticeItem[] })
  | (TaskResult & {
      kind: "learning_dashboard";
      summary?: LearningSummary;
      topics?: {
        id: string;
        title: string;
        state: string;
        attempts?: number;
        accuracy?: number | null;
      }[];
    })
  | (TaskResult & {
      kind: "learning_path";
      path?: {
        summary?: string;
        route_title?: string;
        steps: {
          topic: string;
          title: string;
          state: string;
          reason: string;
          role?: string;
          has_practice?: boolean;
        }[];
      };
    });
