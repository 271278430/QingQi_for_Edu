import type { TeachingResponse as Response } from "./teaching-decision.js";
import type { ModelStatus, SystemSettings } from "./management-contract.js";
export type { TeachingVisual } from "./teaching-visual.js";
export type * from "./problem-reasoning.js";
export type {
  TeachingRoute,
  TeachingResponse as Response,
  TeachingScope,
  TeachingStreamEvent,
} from "./teaching-decision.js";
export type * from "./management-contract.js";
export type * from "./chat-model-contract.js";
export interface Bootstrap {
  can_manage?: boolean;
  settings?: SystemSettings;
  authenticated: boolean;
  demo: boolean;
  profile: string;
  name: string;
  role: string;
  csrf: string;
  profiles: { id: string; name: string; role: string }[];
  mode: string;
  models: ModelStatus[];
  product: string;
}
export interface Session {
  id: string;
  title: string;
  created?: number;
  updated?: number;
  practice_item?: string;
}
export interface Evidence {
  ref: string;
  text: string;
  source: string;
}
export interface TeachingRequest {
  request_id: string;
  question: string;
  expression?: string;
  steps?: { equation: string }[];
  course_query?: string;
  subject?: string;
  mode?: string;
  history?: { kind: string; text: string }[];
  images?: string[];
  visual_context?: { run_id: number; visual_index: number };
  model_selection?: import("./chat-model-contract.js").ChatModelSelection;
}
export interface TutorImage {
  id: string;
  name: string;
  url: string;
  width: number;
  height: number;
}
export interface HistoricalPractice {
  item: PracticeItem;
  session: string | null;
  source: string;
  correct: boolean | null;
  last_at: number | null;
}
export interface Message {
  request_id: string;
  input: TeachingRequest;
  original_input: TeachingRequest;
  response: Response | null;
  partial_response?: string;
  images?: TutorImage[];
  recognized_question?: string;
  phase: string;
  trace: {
    skills: string[];
    observations: {
      tool: string;
      result: { evidence?: Evidence[]; [key: string]: unknown };
    }[];
    context: { [key: string]: unknown };
    route: {
      intents?: string[];
      teaching?: { reason?: string; [key: string]: unknown };
      [key: string]: unknown;
    } | null;
    events: { kind: string; at: number }[];
    error?: string;
    error_code?: string;
  };
}
export interface Detail {
  session: Session;
  messages: Message[];
  practice?: PracticeAssignment | null;
}
export interface Memory {
  episodes: {
    kind: string;
    text: string;
    provenance: string;
    at: number;
    session: string;
  }[];
  facts: {
    fact_key: string;
    value: string;
    source: string;
    trust: string;
    version: number;
    at: number;
  }[];
}
export interface Course {
  id: string;
  title: string;
  scope: string;
  type: string;
  source: string;
}
export interface CourseContext {
  title: string;
  scope: string;
  ancestors: { id: string; title: string; type: string; relation: string }[];
  prerequisite_candidates: { id: string; title: string; status: string }[];
  evidence: Evidence[];
}
export interface Dashboard {
  turns: number;
  sessions: number;
  verified_correct: number;
  nodes: number;
  edges: number;
}
export interface EducationService {
  get<T>(path: string, signal?: AbortSignal): Promise<T>;
  post<T>(path: string, body: unknown): Promise<T>;
  setCsrf(value: string): void;
  stream?<T>(
    path: string,
    body: unknown,
    onEvent: (event: import("./teaching-decision.js").TeachingStreamEvent) => void,
  ): Promise<T>;
}

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
export interface PracticeFeedback {
  correct: boolean;
  independent: boolean;
  unassisted?: boolean;
  independent_first: boolean;
  submitted: string;
  text: string;
}
export interface PracticeAssignment {
  id: string;
  session: string;
  item: PracticeItem;
  feedback: PracticeFeedback | null;
  guidance: string;
  hint_count: number;
}
export interface LearningOverview {
  version: string;
  coverage: string;
  goal: { topic: string; minutes: number; route?: string };
  topics: {
    id: string;
    title: string;
    objective: string;
    requires: string[];
    attempts: number;
    independent_attempts: number;
    independent_correct: number;
    recent_independent_attempts?: number;
    recent_independent_correct?: number;
    evidence_days?: number;
    review?: LearningReview;
    accuracy: number | null;
    state: string;
    last_at: number | null;
    initial?: {
      mastery: number;
      confidence: number;
      practice_count: number;
      accuracy: number;
      status: string;
      last_practiced_at: string;
    };
  }[];
  path: {
    focus: string;
    selected_route: string;
    route_title: string;
    routes: {
      id: string;
      title: string;
      description: string;
      focus: string;
      steps: LearningOverview["path"]["steps"];
      edges?: { source: string; target: string; kind: string; label: string }[];
    }[];
    steps: {
      topic: string;
      title: string;
      objective: string;
      state: string;
      reason: string;
      role?: string;
      has_practice?: boolean;
      checkpoint?: string;
      review?: LearningReview;
    }[];
    summary?: string;
    next_check?: string;
    route_reason?: string;
    today_minutes: number;
    today_items: number;
  };
  summary: {
    turns: number;
    attempts: number;
    items: number;
    independent_attempts: number;
    independent_correct: number;
    assisted_attempts: number;
    accuracy: number | null;
  };
  daily: { date: string; attempts: number; correct: number }[];
  recommendations: PracticeItem[];
  recommendation_info?: {
    batch_id: string;
    requested: number;
    available: number;
    message: string;
  };
  active: PracticeAssignment | null;
  review_overview?: {
    due_count: number;
    recent_due_count: number;
    historical_due_count: number;
    next_at: number | null;
  };
  knowledge_map: {
    nodes: LearningMapNode[];
    groups: { id: string; title: string; count: number }[];
    edges: { source: string; target: string; kind: string }[];
    profile_topics: number;
    mapped_profile_topics: number;
    relation_source: string;
  };
  initial?: {
    identity: string;
    grade: string;
    subject: string;
    as_of: string;
    n_attempts: number;
    history_count: number;
    identity_link: string;
    source: string;
  };
}

export interface LearningMapNode {
  id: string;
  title: string;
  group: string;
  path: string;
  topic_id: string | null;
  available: boolean;
  initial?: NonNullable<LearningOverview["topics"][number]["initial"]>;
}

export interface LearningReview {
  status: "none" | "scheduled" | "due";
  due_at: number | null;
  interval_days: number | null;
  passed_checks: number;
  source: string;
  reason: string;
}
