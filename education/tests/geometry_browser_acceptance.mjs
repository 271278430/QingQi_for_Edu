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
  [fileURLToPath(new URL("./geometry_product_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let stderr = "",
  browser;
child.stderr.on("data", (v) => (stderr += v));
const checks = [];
async function check(name, run) {
  await run();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(Error(stderr)), 30000);
    lines.once("line", (l) => {
      clearTimeout(t);
      resolve(JSON.parse(l));
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
    viewport: { width: 1440, height: 1000 },
  });
  page.setDefaultTimeout(30000);
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  async function send(question) {
    await page.getByLabel("你的学习问题", { exact: true }).fill(question);
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const response = await waiting;
    assert.equal(response.status(), 200);
    await page.waitForFunction(
      () =>
        !document.querySelector("#edu-question")?.disabled &&
        document.querySelector("#edu-question")?.value === "",
    );
    return readTeachResponse(response);
  }
  await check("image_hint_is_grounded", async () => {
    await page.getByLabel("上传题目图片").setInputFiles(setup.image);
    await page.getByLabel("待发送图片").getByRole("img").waitFor();
    const r = await send("解这道题");
    assert.equal(r.response.controller, "grounded_symbolic_geometry_v1");
    assert(!r.response.text.includes("8 - 2 x"));
  });
  await check("reported_full_answer_and_two_animations_render", async () => {
    const r = await send("我想要你直接给我完整答案，并且附上合适的动画教学");
    assert.equal(r.response.visuals.length, 2);
    await page.locator('[data-teaching-animation="triangle_rotation"]').waitFor();
    await page.locator('[data-teaching-animation="geometry_motion"]').waitFor();
    assert((await page.locator(".edu-message .katex").count()) > 8);
    assert.equal(await page.getByRole("alert").count(), 0);
  });
  const rotation = page.locator('[data-teaching-animation="triangle_rotation"]').last();
  await check("rotation_play_pause_step_seek_reset", async () => {
    await rotation.getByRole("button", { name: "播放动画", exact: true }).click();
    await page.waitForFunction(
      () =>
        Number(
          document
            .querySelector('[data-teaching-animation="triangle_rotation"] [data-geometry-progress]')
            ?.getAttribute("data-geometry-progress"),
        ) > 0,
    );
    await rotation.getByRole("button", { name: "暂停动画", exact: true }).click();
    const before = await rotation
      .locator("[data-geometry-progress]")
      .getAttribute("data-geometry-progress");
    await page.evaluate(
      () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))),
    );
    assert.equal(
      await rotation.locator("[data-geometry-progress]").getAttribute("data-geometry-progress"),
      before,
    );
    await rotation.getByLabel("动画进度").press("End");
    const pairs = [
      ["A′", "C"],
      ["E′", "F"],
      ["C′", "B"],
    ];
    for (const [a, b] of pairs) {
      const read = async (label) =>
        rotation
          .locator(`[data-geometry-point="${label}"] circle`)
          .evaluate((e) => [e.getAttribute("cx"), e.getAttribute("cy")].map(Number));
      const p = await read(a),
        q = await read(b);
      assert(Math.hypot(p[0] - q[0], p[1] - q[1]) < 1e-6);
    }
    await rotation.getByRole("button", { name: "重置动画", exact: true }).click();
    await rotation.getByRole("button", { name: "演示下一步", exact: true }).click();
    assert(
      Number(
        await rotation.locator("[data-geometry-progress]").getAttribute("data-geometry-progress"),
      ) > 0,
    );
  });
  await check("expanded_animation_shares_original_progress", async () => {
    await rotation.getByLabel("动画进度").press("End");
    const card = page.locator('[data-teaching-visual="animation_scene"]').filter({ has: rotation });
    await card.getByRole("button", { name: "放大图示", exact: true }).click();
    const dialog = page.getByRole("dialog");
    await dialog.waitFor();
    assert.equal(
      await dialog.locator("[data-geometry-progress]").getAttribute("data-geometry-progress"),
      "1",
    );
    await dialog.getByRole("button", { name: "重置动画", exact: true }).click();
    await page.keyboard.press("Escape");
    await dialog.waitFor({ state: "hidden" });
    assert.equal(
      await rotation.locator("[data-geometry-progress]").getAttribute("data-geometry-progress"),
      "0",
    );
  });
  await check("proof_steps_are_real_and_playback_continues", async () => {
    await rotation.getByRole("button", { name: "重置动画", exact: true }).click();
    assert.equal(await rotation.getByRole("group", { name: "教学步骤" }).count(), 0);
    assert.equal(await rotation.locator("[data-geometry-auxiliary]").count(), 0);
    await rotation.getByRole("button", { name: "演示下一步", exact: true }).click();
    await page.waitForFunction(
      () =>
        document
          .querySelector('[data-teaching-animation="triangle_rotation"] [data-geometry-progress]')
          ?.getAttribute("data-geometry-progress") === "0.18",
    );
    assert.equal(
      Number(
        await rotation.locator("[data-geometry-progress]").getAttribute("data-geometry-progress"),
      ),
      0.18,
    );
    await rotation.locator("[data-geometry-auxiliary]").waitFor({ state: "attached" });
    assert.notEqual(
      await rotation
        .locator("[data-geometry-auxiliary]")
        .evaluate((e) => getComputedStyle(e).stroke),
      "none",
    );
    await rotation.getByRole("button", { name: "演示上一步", exact: true }).click();
    await page.waitForFunction(
      () =>
        document
          .querySelector('[data-teaching-animation="triangle_rotation"] [data-geometry-progress]')
          ?.getAttribute("data-geometry-progress") === "0",
    );
    await rotation.getByRole("button", { name: "播放动画", exact: true }).click();
    await rotation.getByTestId("geometry-lesson-step").filter({ hasText: "添加辅助线" }).waitFor();
    assert.equal(await rotation.getByRole("button", { name: "暂停动画", exact: true }).count(), 1);
    await rotation.getByRole("button", { name: "暂停动画", exact: true }).click();
    await rotation.getByLabel("动画进度").press("End");
    await rotation
      .getByTestId("geometry-lesson-step")
      .filter({ hasText: "对应边得结论" })
      .waitFor();
    assert((await rotation.locator(".katex").count()) > 0);
    assert.equal(await rotation.locator('[data-length-mark="AD"] line').count(), 1);
    assert.equal(await rotation.locator('[data-length-mark="CD"] line').count(), 1);
    assert.equal(await rotation.locator('[data-length-mark="DE"] line').count(), 2);
    assert.equal(await rotation.locator('[data-length-mark="DF"] line').count(), 2);
    await rotation.screenshot({
      path: fileURLToPath(new URL("../.local/reports/geometry-lesson-proof.png", import.meta.url)),
    });
  });
  const motion = page.locator('[data-teaching-animation="geometry_motion"]').last();
  await check("motion_respects_perpendicular_relation_and_domain_endpoint", async () => {
    await motion.getByLabel("动画进度").press("End");
    const read = async (label) =>
      motion
        .locator(`[data-geometry-point="${label}"] circle`)
        .evaluate((e) => [e.getAttribute("cx"), e.getAttribute("cy")].map(Number));
    const d = await read("D"),
      e = await read("E"),
      f = await read("F"),
      b = await read("B");
    assert(Math.abs((e[0] - d[0]) * (f[0] - d[0]) + (e[1] - d[1]) * (f[1] - d[1])) < 1e-6);
    assert(Math.hypot(f[0] - b[0], f[1] - b[1]) < 1e-6);
    assert((await motion.getByTestId("animation-readout").innerText()).includes("x 4"));
    await motion.locator("[data-geometry-ray]").waitFor();
    assert.equal(await motion.getByRole("group", { name: "教学步骤" }).count(), 0);
    await motion.screenshot({
      path: fileURLToPath(new URL("../.local/reports/geometry-motion-endpoint.png", import.meta.url)),
    });
  });
  await check("geometric_motion_and_function_cursor_are_synchronized", async () => {
    await motion.getByLabel("动画进度").press("Home");
    for (let i = 0; i < 3; i++)
      await motion.getByRole("button", { name: "演示下一步", exact: true }).click();
    const slider = await motion.getByLabel("动画进度").boundingBox();
    await page.mouse.click(slider.x + slider.width * 0.65, slider.y + slider.height / 2);
    const readout = await motion.getByTestId("animation-readout").innerText();
    const [x, y] = [...readout.matchAll(/(?:x|y)\s+≈?(-?[\d.]+)/g)].map((m) => Number(m[1]));
    const cursor = motion.locator("[data-function-cursor]");
    assert(Math.abs(Number(await cursor.getAttribute("data-function-x")) - x) < 0.011);
    assert(Math.abs(Number(await cursor.getAttribute("data-function-y")) - y) < 0.011);
    assert(Math.abs(y - (8 - 2 * x)) < 0.021);
    assert.equal(
      await motion.locator('[data-function-endpoint="left"]').getAttribute("data-boundary"),
      "open",
    );
    assert.equal(
      await motion.locator('[data-function-endpoint="right"]').getAttribute("data-boundary"),
      "closed",
    );
    await motion.screenshot({
      path: fileURLToPath(new URL("../.local/reports/geometry-lesson-function.png", import.meta.url)),
    });
  });
  await check("geometric_animations_fit_mobile_and_refresh", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.reload();
    await page.locator('[data-teaching-animation="geometry_motion"]').last().waitFor();
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    assert.deepEqual(errors, []);
  });
  await check("static_geometry_and_all_connections_are_real", async () => {
    const r = await send("请画出原题的几何示意图。");
    assert.equal(r.response.visuals[0].points.length, 6);
    const connected = await send("请把图中的点全部连起来。");
    assert.equal(connected.response.visuals[0].segments.length, 15);
    const figure = page.locator('[data-teaching-visual="coordinates"]').last();
    assert.equal(await figure.locator("[data-coordinate-segment]").count(), 15);
  });
  await check("explicit_function_animation_follows_equation_and_shared_progress", async () => {
    const r = await send("请用动画画一次函数 y=2x+1，不用讲解。");
    const v = r.response.visuals[0];
    assert.equal(v.template, "function_trace");
    assert.equal(v.params.a, 2);
    assert.equal(v.params.b, 1);
    const animation = page.locator('[data-teaching-animation="function_trace"]').last();
    await animation.getByLabel("动画进度").press("Home");
    const start = await animation.locator("[data-function-cursor]").getAttribute("cx");
    await animation.getByLabel("动画进度").press("End");
    const end = await animation.locator("[data-function-cursor]").getAttribute("cx");
    assert(Number(end) > Number(start));
    const readout = await animation.getByTestId("animation-readout").textContent();
    const [x, y] = [...readout.matchAll(/(?:x|y)\s+(-?[\d.]+)/g)].map((m) => Number(m[1]));
    assert.equal(y, 2 * x + 1);
  });
  await check("explicit_fraction_animation_fills_exact_three_of_four", async () => {
    const r = await send("请用动画演示分数 3/4，不用讲解。");
    assert.equal(r.response.visuals[0].params.numerator, 3);
    assert.equal(r.response.visuals[0].params.denominator, 4);
    const animation = page.locator('[data-teaching-animation="fraction_fill"]').last();
    await animation.getByLabel("动画进度").press("End");
    assert.match(
      await animation.getByTestId("animation-readout").textContent(),
      /已涂色 3 份 \/ 共 4 份/,
    );
    await animation.getByRole("img", { name: "涂色 3 份，共 4 份" }).waitFor();
    await page.reload();
    await page.locator('[data-teaching-animation="fraction_fill"]').last().waitFor();
    assert.deepEqual(errors, []);
  });
  await check("explicit_description_restores_owned_prior_image_after_other_function", async () => {
    const r = await send("只描述这张图片的内容，不要解题。");
    assert.equal(r.response.controller, "glm_vision_text_controller");
    assert(r.response.text.includes("不展开证明"));
    assert.equal(await page.getByRole("alert").count(), 0);
  });
  await check("second_question_uses_length_ratio_steps_and_mobile_formula", async () => {
    const r = await send("请把第（2）问的完整解题步骤做成动画。");
    assert.equal(r.response.visuals.length, 1);
    assert.equal(r.response.visuals[0].lesson.goal, "ratio");
    const card = page.locator('[data-teaching-animation="geometry_motion"]').last();
    for (let i = 0; i < 3; i++)
      await card.getByRole("button", { name: "演示下一步", exact: true }).click();
    await card.getByTestId("geometry-lesson-step").filter({ hasText: "相似得到长度比" }).waitFor();
    assert((await card.locator(".katex").count()) > 0);
    assert.equal(await card.locator("[data-function-cursor]").count(), 0);
    assert.equal(await card.locator("[data-geometry-foot]").count(), 2);
    await card.getByRole("button", { name: "查看垂足重合位置" }).click();
    await card.getByTestId("geometry-lesson-step").filter({ hasText: "重合时" }).waitFor();
    const p = async (label) =>
      card
        .locator(`[data-geometry-point="${label}"] circle`)
        .evaluate((e) => [e.getAttribute("cx"), e.getAttribute("cy")].map(Number));
    for (const [a, b] of [
      ["E", "H"],
      ["F", "K"],
    ]) {
      const u = await p(a),
        v = await p(b);
      assert(Math.hypot(u[0] - v[0], u[1] - v[1]) < 1e-6);
    }
    assert.equal(await card.locator("[data-similar-triangles]").count(), 0);
    await page.setViewportSize({ width: 390, height: 844 });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    const section = page
      .locator('[data-teaching-visual="animation_scene"]')
      .filter({ has: card })
      .last();
    await section.getByRole("button", { name: "放大图示", exact: true }).click();
    const dialog = page.getByRole("dialog");
    await dialog.getByTestId("geometry-lesson-step").filter({ hasText: "重合时" }).waitFor();
    await dialog.screenshot({
      path: fileURLToPath(new URL("../.local/reports/geometry-lesson-ratio-mobile.png", import.meta.url)),
    });
    await page.keyboard.press("Escape");
    assert.deepEqual(errors, []);
  });
} finally {
  await browser?.close();
  child.kill();
  await writeFile(
    new URL("../.local/reports/geometry-browser-acceptance.json", import.meta.url),
    JSON.stringify({ passed: checks.length, checks, real_model: false }, null, 2),
  );
}
