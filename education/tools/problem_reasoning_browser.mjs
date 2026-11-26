import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
import { readTeachResponse } from "./read_teach_response.mjs";

const child = spawn(
  process.env.QINGQI_PYTHON,
  [fileURLToPath(new URL("conversation_problem_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let stderr = "",
  browser;
child.stderr.on("data", (chunk) => {
  stderr += chunk;
});
const checks = [],
  errors = [];
async function check(name, run) {
  await run();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(Error(stderr || "fixture timeout")), 30000);
    lines.once("line", (line) => {
      clearTimeout(timer);
      resolve(JSON.parse(line));
    });
    child.once("exit", (code) => {
      clearTimeout(timer);
      reject(Error(`fixture ${code}: ${stderr}`));
    });
  });
  browser = await chromium.launch({
    headless: true,
    executablePath: [
      "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
      "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    ].find(existsSync),
  });
  const page = await browser.newPage({
    viewport: { width: 1500, height: 1100 },
  });
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  async function send(question) {
    await page.locator("#edu-question").fill(question);
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const response = await waiting;
    assert.equal(response.status(), 200);
    await page.waitForFunction(() => document.querySelector("#edu-question")?.value === "");
    return (await readTeachResponse(response)).response;
  }
  await page.getByLabel("上传题目图片").setInputFiles(setup.image);
  await page.getByLabel("待发送图片").getByRole("img").waitFor();
  const result = await send("请用动画针对原题完整讲解，直接给答案。");
  const animation = page.locator('[data-teaching-animation="function_reasoning"]').first();
  const slider = animation.getByRole("slider");
  async function seek(phase) {
    const at = result.visuals
      .find((v) => v.kind === "animation_scene")
      .reasoning_lesson.steps.find((s) => s.scene === phase).at;
    await slider.evaluate((input, value) => {
      Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set.call(
        input,
        String(Math.round(value * 1000)),
      );
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
    }, at);
    await animation.locator(`[data-reasoning-scene="${phase}"]`).waitFor();
  }
  await check("original_function_and_goal_are_visible", async () => {
    await animation.waitFor();
    assert.equal(result.visuals.length, 1);
    assert.equal(result.visuals.filter((v) => v.kind === "animation_scene").length, 1);
    assert.match(await animation.locator(".edu-reasoning-header").innerText(), /2.*x.*a.*x.*1/s);
    assert.equal(await page.getByRole("alert").count(), 0);
    assert.equal(await animation.locator(".katex-error").count(), 0);
    assert.equal(
      await animation.locator('[data-reasoning-scene="read"] [data-curve-landmark]').count(),
      3,
    );
    assert((await animation.locator("[data-curve-x-tick]").count()) >= 4);
    assert((await animation.locator("[data-curve-y-tick]").count()) >= 3);
    await animation
      .locator(".edu-reasoning-scene .edu-curve-figure")
      .first()
      .screenshot({
        path: fileURLToPath(
          new URL("../.local/reports/curve-first-function-overview.png", import.meta.url),
        ),
      });
    const negativeTick = animation.locator('[data-curve-x-tick="-1"]');
    assert.equal(await negativeTick.locator(".katex").count(), 1);
    assert.equal(await negativeTick.locator("annotation").textContent(), "−1");
  });
  await check("three_zero_cases_show_actual_intersections_and_can_be_selected", async () => {
    await seek("cases");
    for (const count of [0, 1, 2]) {
      await animation.getByRole("button", { name: `观察${count}个正零点`, exact: true }).click();
      await animation.locator(`[data-root-count="${count}"][data-active="true"]`).waitFor();
      assert.equal(
        await animation
          .getByRole("button", { name: `观察${count}个正零点`, exact: true })
          .getAttribute("aria-pressed"),
        "true",
      );
      assert.equal(
        await animation.locator(`[data-root-count="${count}"] [data-reasoning-zero]`).count(),
        count,
      );
    }
    assert.equal(await animation.locator(".edu-reasoning-case").count(), 1);
    const formula = await animation
      .getByTestId("reasoning-step-formula")
      .locator("annotation")
      .textContent();
    assert(formula.includes(String.fromCharCode(92) + "to"));
    assert(formula.includes(String.fromCharCode(92) + "infty"));
    await animation.locator(".edu-reasoning-lesson").screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/reasoning-function-zero-cases.png", import.meta.url),
      ),
    });
  });
  await check("parameter_elimination_matches_the_original_problem", async () => {
    await seek("solve");
    assert.match(await animation.getByTestId("reasoning-step-title").innerText(), /消元/);
    const lesson = result.visuals.find((v) => v.kind === "animation_scene").reasoning_lesson;
    const solveStep = lesson.steps.findIndex((step) => step.scene === "solve");
    const from = lesson.steps[solveStep].at,
      to = lesson.steps[solveStep + 1].at;
    for (const [part, title] of [
      [0.01, "由导数条件表示参数"],
      [0.34, "回到函数条件消元"],
      [0.68, "取正根并回代参数"],
    ]) {
      await slider.evaluate(
        (input, value) => {
          Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set.call(
            input,
            String(Math.round(value * 1000)),
          );
          input.dispatchEvent(new Event("input", { bubbles: true }));
        },
        from + (to - from) * part,
      );
      assert.equal(await animation.getByTestId("elimination-action").innerText(), title);
    }
    assert.match(await animation.locator(".edu-reasoning-result").innerText(), /r.*1.*a.*3/s);
    assert.equal(await animation.locator(".katex-error").count(), 0);
  });
  await check("derivative_animation_links_two_graphs_and_signs", async () => {
    await seek("derivative");
    assert.equal(await animation.locator(".edu-reasoning-curve").count(), 2);
    assert.equal(await animation.locator("[data-reasoning-cursor]").count(), 2);
    assert.equal(await animation.locator("[data-reasoning-linked-point]").count(), 2);
    assert.equal(await animation.locator('[data-sign="+"]').count(), 1);
    assert.equal(await animation.locator('[data-sign="-"]').count(), 1);
  });
  await check("candidate_selection_highlights_the_mathematically_correct_point", async () => {
    await seek("extrema");
    await animation.getByRole("button", { name: "比较候选点0", exact: true }).click();
    assert.equal(
      await animation
        .locator("[data-reasoning-highlight]")
        .getAttribute("data-reasoning-highlight"),
      "0,1",
    );
    await animation.locator(".edu-reasoning-lesson").screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/reasoning-function-extrema.png", import.meta.url),
      ),
    });
  });
  await check("one_play_reaches_the_actual_final_result", async () => {
    await animation.getByRole("button", { name: "重置动画", exact: true }).click();
    await animation.getByRole("button", { name: "播放动画", exact: true }).click();
    await page.waitForFunction(
      () =>
        document
          .querySelector('[data-teaching-animation="function_reasoning"]')
          ?.getAttribute("data-animation-progress") === "1",
      null,
      { timeout: 30000 },
    );
    await animation.locator('[data-reasoning-scene="result"]').waitFor();
    assert.match(await animation.locator(".edu-reasoning-result").innerText(), /−3/);
    await animation.getByRole("button", { name: "比较候选点-1", exact: true }).click();
    await animation.locator('[data-reasoning-scene="extrema"]').waitFor();
  });
  await check("zoom_uses_the_same_problem_and_progress", async () => {
    const card = page.locator(".edu-teaching-card").filter({ has: animation }).first();
    await card.getByRole("button", { name: "放大图示", exact: true }).click();
    const dialog = page.getByRole("dialog");
    await dialog.locator('[data-teaching-animation="function_reasoning"]').waitFor();
    const values = await page
      .locator('[data-teaching-animation="function_reasoning"]')
      .evaluateAll((nodes) => nodes.map((n) => n.getAttribute("data-animation-progress")));
    assert.equal(new Set(values).size, 1);
    await page.keyboard.press("Escape");
    await dialog.waitFor({ state: "hidden" });
  });
  await check("refresh_keeps_the_same_accepted_reasoning_animation", async () => {
    await page.reload();
    await animation.waitFor();
    assert.equal(await page.getByRole("alert").count(), 0);
    assert.equal(await animation.locator(".katex-error").count(), 0);
  });
  await page.getByRole("button", { name: "新建学习对话", exact: true }).click();
  const nn = await send(
    "已知 $\\sqrt{2a-1}+|3b+2|=0$，求 $a+b$。请用动画完整演示解题步骤，直接给答案。",
  );
  const nonnegative = page.locator('[data-teaching-animation="nonnegative_reasoning"]').first();
  async function seekN(scene) {
    const at = nn.visuals
      .find((v) => v.kind === "animation_scene")
      .reasoning_lesson.steps.find((s) => s.scene === scene).at;
    await nonnegative.getByRole("slider").evaluate((input, value) => {
      Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set.call(
        input,
        String(Math.round(value * 1000)),
      );
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
    }, at);
    await nonnegative.locator(`[data-reasoning-scene="${scene}"]`).waitFor();
  }
  await check("nonnegative_animation_explains_the_actual_expression_contradiction", async () => {
    await nonnegative.waitFor();
    await seekN("positive_left");
    assert.equal(await nonnegative.locator('[data-contradiction="true"]').count(), 1);
    assert.match(
      await nonnegative.locator(".edu-reasoning-terms").innerText(),
      /2.*a.*1.*3.*b.*2/s,
    );
    assert.equal(
      await nonnegative.locator(".edu-reasoning-term-curves .edu-reasoning-curve").count(),
      2,
    );
    assert.equal(await nonnegative.locator("[data-reasoning-cursor]").count(), 1);
    assert.equal(
      await nonnegative.locator(".edu-reasoning-placeholder,.edu-reasoning-positive").count(),
      0,
    );
    await nonnegative.locator(".edu-reasoning-lesson").screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/reasoning-nonnegative-contradiction.png", import.meta.url),
      ),
    });
  });
  await check("equation_operations_show_fractional_parameters_without_decimal_noise", async () => {
    await seekN("solve_variable");
    assert.equal(await nonnegative.locator(".edu-reasoning-equal-operations").count(), 1);
    const finalStep = nn.visuals
      .find((v) => v.kind === "animation_scene")
      .reasoning_lesson.steps.at(-1).at;
    await nonnegative.getByRole("slider").evaluate((input, value) => {
      Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set.call(
        input,
        String(Math.round(value * 1000)),
      );
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.dispatchEvent(new Event("change", { bubbles: true }));
    }, finalStep);
    await nonnegative.locator('[data-reasoning-scene="result"]').waitFor();
    assert.match(await nonnegative.locator(".edu-reasoning-result").innerText(), /6/);
    assert.equal(await nonnegative.locator(".katex-error").count(), 0);
    await nonnegative.locator(".edu-reasoning-lesson").screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/reasoning-nonnegative-result.png", import.meta.url),
      ),
    });
  });
  await check("phone_and_reduced_motion_preserve_steps_and_formula_readability", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.emulateMedia({ reducedMotion: "reduce" });
    await nonnegative.getByRole("button", { name: "重置动画", exact: true }).click();
    await nonnegative.getByRole("button", { name: "演示下一步", exact: true }).click();
    await nonnegative.locator('[data-reasoning-scene="positive_left"]').waitFor();
    assert.equal(
      await nonnegative.getByRole("button", { name: "播放动画", exact: true }).isEnabled(),
      false,
    );
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    assert.deepEqual(errors, []);
    await page.screenshot({
      path: fileURLToPath(new URL("../.local/reports/reasoning-mobile.png", import.meta.url)),
    });
  });
  await check("static_nonnegative_curves_use_distinct_variable_axes", async () => {
    await page.setViewportSize({ width: 1500, height: 1100 });
    await page.getByRole("button", { name: "新建学习对话", exact: true }).click();
    const result = await send(
      "已知 $\\sqrt{2a-1}+|3b+2|=0$，求 $a+b$。不要动画，画函数图并直接给答案。",
    );
    assert.equal(result.visuals.length, 1);
    assert.equal(result.visuals[0].kind, "reasoning_diagram");
    await page.getByRole("img", { name: "根式项：函数值不小于零", exact: true }).waitFor();
    await page.getByRole("img", { name: "绝对值项：函数值不小于零", exact: true }).waitFor();
    assert.equal(await page.locator("[data-teaching-animation]").count(), 0);
    assert.equal(await page.locator(".katex-error").count(), 0);
    assert.equal(await page.getByRole("alert").count(), 0);
    assert.deepEqual(errors, []);
  });
  await writeFile(
    new URL("../.local/reports/problem-reasoning-browser.local.json", import.meta.url),
    JSON.stringify({ passed: checks.length, checks, isolated: true }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
}
