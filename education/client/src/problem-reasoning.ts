export interface ReasoningStep {
  at: number;
  title: string;
  scene: string;
  given: string;
  action: string;
  rule: string;
  formula: string;
}
export interface ReasoningCurve {
  domain: [number, number];
  y_range: [number, number];
  samples: { x: number; y: number }[];
  markers: { x: number; y: number; label: string }[];
  formula?: string;
  axis_labels?: { x: string; y: string };
  x_ticks?: { value: number; label: string }[];
  y_ticks?: { value: number; label: string }[];
  note?: string;
}
interface ReasoningBase {
  version: "problem_reasoning_v1";
  mode: "hint" | "solution";
  problem: string;
  goal: string;
  steps: ReasoningStep[];
}
export interface FunctionReasoning extends ReasoningBase {
  kind: "function";
  given: {
    k: number;
    constant: number;
    parameter: string;
    interval: [number, number];
  };
  cases: {
    label: string;
    root_count: number;
    minimum: { x: number; y: number };
    curve: ReasoningCurve;
    zeros: number[];
  }[];
  curve?: ReasoningCurve;
  root_curve: ReasoningCurve;
  derivative_curve?: ReasoningCurve;
  elimination?: { title: string; action: string; formula: string }[];
  positive_stationary: { x: number; y: number };
  negative_root?: { x: number; y: number };
  signs?: { from: number; to: number; sign: "+" | "-" }[];
  candidates?: {
    x: number;
    y: number;
    x_label: string;
    y_label: string;
    role: string;
  }[];
  solved?: {
    parameter: string;
    root: string;
    negative_root: string;
    minimum: string;
    maximum: string;
    sum: string;
  };
}
export interface NonnegativeReasoning extends ReasoningBase {
  kind: "nonnegative";
  target: string;
  terms: [string, string];
  term_curves?: {
    expression: string;
    curve: ReasoningCurve;
    zero: { x: number; y: number };
    positive: { x: number; y: number };
  }[];
  variables?: {
    name: string;
    value: number;
    label: string;
    equation: string;
    intermediate: string;
    solved_equation: string;
    operation1: string;
    operation2: string;
  }[];
  solved?: { variables: Record<string, string>; result?: string };
  number_line?: {
    range: [number, number];
    positions: number[];
    ticks: { value: number; label: string }[];
  };
}
export type ProblemReasoningLesson = FunctionReasoning | NonnegativeReasoning;
