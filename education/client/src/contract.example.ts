import type { EducationService, Bootstrap } from "./contract.js";
import type { TeachingVisual } from "./teaching-visual.js";
export const identityAnimationExample: TeachingVisual = {
  id: "visual:identity-example",
  version: "visual_teaching_v4",
  title: "用试值理解恒成立",
  basis: "problem",
  provenance: "依据原方程推导",
  kind: "animation_scene",
  template: "identity_probe",
  duration: 14,
  range: [0, 2],
  extent: 2,
  params: { equation: "mx-8=5x+n", lesson_mode: "hint" },
  frames: [
    { at: 0, values: { phase: 0, probe: 0 } },
    { at: 14, values: { phase: 1, probe: 0 } },
  ],
  algebra_lesson: {
    version: "identity_lesson_v1",
    mode: "hint",
    equation: "mx-8=5x+n",
    rearranged: "(m-5)x=n+8",
    coefficient_symbol: "m-5",
    constant_symbol: "n+8",
    conditions: ["m-5=0", "n+8=0"],
    steps: [
      {
        at: 0,
        title: "整理方程",
        phase: "rearrange",
        explanation: "把含x的项放在一起。",
        formula: "(m-5)x=n+8",
      },
      {
        at: 1,
        title: "比较两个条件",
        phase: "conditions",
        explanation: "据此求参数。",
        formula: "m-5=0,n+8=0",
      },
    ],
  },
};
export const identityStoryExample: TeachingVisual = {
  ...identityAnimationExample,
  id: "visual:identity-story-example",
  version: "visual_teaching_v5",
  title: "双记录器的积分故事",
  params: {
    equation: "mx-8=5x+n",
    lesson_mode: "hint",
    scenario: "scorekeepers",
  },
  algebra_lesson: {
    ...identityAnimationExample.algebra_lesson!,
    story: {
      title: "双记录器的积分故事",
      setup: "两台记录器接受同一个输入，积分应始终相同。",
      domain_note: "输入可以为负数或分数。",
      left: { name: "蓝色记录器", rate: "m", offset: "-8", expression: "mx-8" },
      right: { name: "紫色记录器", rate: "5", offset: "n", expression: "5x+n" },
    },
    steps: [
      {
        at: 0,
        title: "比较初始积分",
        phase: "probe",
        probe: 0,
        accounts: ["-8", "n"],
        explanation: "x=0时比较固定部分。",
        formula: "-8=n",
      },
    ],
  },
};
export async function initializeStudent(
  service: EducationService,
): Promise<Bootstrap> {
  const identity = await service.get<Bootstrap>("/api/bootstrap");
  service.setCsrf(identity.csrf);
  return identity;
}

export const nonnegativeReasoningExample: TeachingVisual = {
  id: "visual:nonnegative-reasoning-example",
  version: "visual_teaching_v8",
  kind: "animation_scene",
  template: "nonnegative_reasoning",
  basis: "problem",
  provenance: "原题推理分镜",
  title: "非负和为零",
  duration: 20,
  range: [0, 1],
  extent: 1,
  params: {
    equation: String.raw`\sqrt{a-3}+|b+2|=0`,
    target: "a+b",
    lesson_mode: "hint",
  },
  frames: [
    { at: 0, values: { phase: 0 } },
    { at: 20, values: { phase: 1 } },
  ],
  reasoning_lesson: {
    version: "problem_reasoning_v1",
    kind: "nonnegative",
    mode: "hint",
    problem: String.raw`\sqrt{a-3}+|b+2|=0`,
    goal: "求 a+b",
    target: "a+b",
    terms: [String.raw`\sqrt{a-3}`, "|b+2|"],
    steps: [
      {
        at: 0,
        title: "确认非负项",
        scene: "read",
        given: "两项相加为零",
        action: "确认表达式各自非负",
        rule: "根式与绝对值均非负",
        formula: String.raw`\sqrt{a-3}\ge0,\quad |b+2|\ge0`,
      },
      {
        at: 1,
        title: "列出待求条件",
        scene: "conditions",
        given: "两项均为零",
        action: "按定义去掉外层",
        rule: "被开方数和绝对值内部量均为零",
        formula: String.raw`a-3=0,\quad b+2=0`,
      },
    ],
  },
};
