import type {
  FunctionReasoning,
  NonnegativeReasoning,
  ProblemReasoningLesson,
} from "./problem-reasoning.js";

/** Read-only diagrams accepted by the teaching owner; no executable content. */
export type TeachingVisual = {
  id: string;
  version: string;
  title: string;
  basis: "problem" | "example";
  provenance: string;
  caption?: string;
  parent_id?: string;
  teaching_part?: number;
  presentation_role?: "picture" | "animation";
} & (
  | {
      kind: "reasoning_diagram";
      template: "function_reasoning" | "nonnegative_reasoning" | "identity_probe";
      params: Record<string, unknown>;
      reasoning_lesson?:
        | Pick<
            FunctionReasoning,
            "kind" | "mode" | "problem" | "given" | "cases" | "curve" | "derivative_curve"
          >
        | Pick<NonnegativeReasoning, "kind" | "mode" | "problem" | "term_curves" | "steps">;
      algebra_lesson?: {
        mode: "hint" | "solution";
        equation: string;
        rearranged: string;
        conditions: string[];
      };
    }
  | {
      kind: "number_line";
      points: { label: string; x: number }[];
      moves: { start: number; delta: number; end: number; label: string }[];
      range: [number, number];
    }
  | {
      kind: "coordinates";
      layout?: "geometry";
      points: CoordinatePoint[];
      extent: number;
      segments?: CoordinateSegment[];
      polygons?: { vertices: number[] }[];
      circles?: { center: number; radius: number }[];
    }
  | {
      kind: "function_plot";
      function: "linear" | "quadratic" | "cubic" | "square_root" | "absolute";
      a: number;
      b: number;
      c: number;
      d?: number;
      display?: FunctionDisplay;
      axis_labels?: { x: string; y: string };
      markers?: CoordinatePoint[];
      focus_interval?: [number, number];
      domain: [number, number];
      samples: { x: number; y: number }[];
      y_range: [number, number];
    }
  | {
      kind: "area_model";
      numerator: number;
      denominator: number;
      shape: "rectangle" | "circle";
      ratio: number;
    }
  | { kind: "table"; columns: string[]; rows: string[][] }
  | { kind: "bar_chart"; bars: { label: string; value: number }[] }
  | {
      kind: "scene";
      nodes: string[];
      edges: { source: number; target: number; label: string }[];
      mermaid: string;
    }
  | {
      kind: "animation_scene";
      template:
        | "absolute_distance"
        | "square_root"
        | "nonnegative_sum"
        | "number_line_motion"
        | "travel_motion"
        | "coordinate_drawing"
        | "fraction_fill"
        | "pythagorean"
        | "triangle_rotation"
        | "geometry_motion"
        | "identity_probe"
        | "function_reasoning"
        | "nonnegative_reasoning"
        | "function_trace";
      duration: number;
      frames: { at: number; values: Record<string, number> }[];
      range: [number, number];
      extent: number;
      inspection_steps?: { at: number; title: string; explanation: string }[];
      reasoning_lesson?: ProblemReasoningLesson;
      algebra_lesson?: {
        version: "identity_lesson_v1";
        mode: "hint" | "solution";
        equation: string;
        rearranged: string;
        coefficient_symbol: string;
        constant_symbol: string;
        conditions: string[];
        story?: {
          title: string;
          setup: string;
          domain_note: string;
          left: {
            name: string;
            rate: string;
            offset: string;
            expression: string;
          };
          right: {
            name: string;
            rate: string;
            offset: string;
            expression: string;
          };
        };
        steps: {
          at: number;
          title: string;
          explanation: string;
          formula: string;
          phase: "rearrange" | "probe" | "conditions" | "solution";
          probe?: number;
          accounts?: [string, string];
        }[];
      };
      params?: {
        k?: number;
        constant?: number;
        interval?: [number, number];
        target?: string;
        equation?: string;
        power?: number;
        units?: boolean;
        scenario?: "scorekeepers";
        side?: number;
        side_exact?: string;
        ratio?: number;
        ratio_exact?: string;
        ae?: number;
        from_x?: number;
        to_x?: number;
        labels?: Record<"a" | "b" | "c" | "d" | "e" | "f", string>;
        lesson_mode?: "hint" | "solution";
        lesson_goal?: "ratio" | "function";
        parameter?: string;
        x_variable?: string;
        y_variable?: string;
        numerator?: number;
        denominator?: number;
        points?: CoordinatePoint[];
        segments?: CoordinateSegment[];
      };
      geometry?: {
        points: CoordinatePoint[];
        segments: CoordinateSegment[];
        extent: number;
        polygons?: { vertices: number[] }[];
        circles?: { center: number; radius: number }[];
        bounds?: { xmin: number; xmax: number; ymin: number; ymax: number };
        ray_end?: { x: number; y: number };
        helpers?: CoordinatePoint[];
      };
      lesson?: {
        version: "geometry_lesson_v1";
        mode: "hint" | "solution";
        goal?: "ratio" | "function";
        method?: "perpendicular_similarity";
        helper_labels?: { h: string; k: string };
        coincidence_x?: number;
        symbols: { x: string; y: string };
        steps: {
          at: number;
          title: string;
          explanation: string;
          formula?: string;
        }[];
        motion_window: [number, number];
        rotation_fraction: number;
        domain?: { upper: number; upper_closed: boolean };
      };
      plot?: {
        function: "linear" | "quadratic" | "cubic";
        a: number;
        b: number;
        c: number;
        d?: number;
        display?: FunctionDisplay;
        markers?: CoordinatePoint[];
        focus_interval?: [number, number];
        domain: [number, number];
        samples: { x: number; y: number }[];
        y_range: [number, number];
      };
    }
);

export interface CoordinatePoint {
  label: string;
  x: number;
  y: number;
  x_tex?: string;
  y_tex?: string;
}
export interface FunctionDisplay {
  formula: string;
  domain: [string, string];
  markers: { x: string; y: string }[];
}
export interface CoordinateSegment {
  source: number;
  target: number;
  style: "solid" | "dashed";
  role: "edge" | "diagonal" | "auxiliary" | "connection";
  label?: string;
  length: number;
}
