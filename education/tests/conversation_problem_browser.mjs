import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
const child = spawn(
  process.env.QINGQI_PYTHON,
  [fileURLToPath(new URL("./conversation_problem_fixture.py", import.meta.url))],
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
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  page.setDefaultTimeout(30000);
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  async function send(q) {
    await page.getByLabel("你的学习问题", { exact: true }).fill(q);
    const wait = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const r = await wait;
    assert.equal(r.status(), 200);
    await page.waitForFunction(
      () =>
        !document.querySelector("#edu-question")?.disabled &&
        document.querySelector("#edu-question")?.value === "",
    );
    return (await r.json()).response;
  }
  await page.getByLabel("上传题目图片").setInputFiles(setup.image);
  await page.getByLabel("待发送图片").getByRole("img").waitFor();
  await send("直接给完整的答案");
  const result = await send("给出关键可视化教学动画");
  await check("reported_followup_creates_two_actual_function_animations", async () => {
    assert.equal(result.visuals.length, 2);
    await page.locator('[data-teaching-animation="function_trace"]').nth(1).waitFor();
    assert(result.text.includes("−3"));
  });
  const card = page.locator('[data-teaching-visual="animation_scene"]').first();
  const animation = card.locator('[data-teaching-animation="function_trace"]');
  await check("each_key_step_uses_actual_cubic_point", async () => {
    for (const [i, step] of result.visuals[0].inspection_steps.entries()) {
      await animation.getByRole("button", { name: `函数关键步骤 ${i + 1}`, exact: true }).click();
      const p = await animation
        .locator("[data-function-cursor]")
        .evaluate((e) => ({ x: Number(e.dataset.functionX), y: Number(e.dataset.functionY) }));
      assert(Math.abs(p.x - (-1.3 + 2.6 * step.at)) < 1e-8);
      assert(Math.abs(p.y - (2 * p.x ** 3 - 3 * p.x ** 2 + 1)) < 1e-8);
    }
    assert.equal(await animation.locator("[data-function-marker]").count(), 4);
    assert.equal(await animation.locator("[data-function-focus]").count(), 1);
  });
  await check("playback_stops_on_mathematical_checkpoint", async () => {
    await animation.getByRole("button", { name: "重置动画", exact: true }).click();
    await animation.getByRole("button", { name: "播放动画", exact: true }).click();
    await animation.locator('[data-function-step="1"]').waitFor();
    assert.equal(await animation.getByRole("button", { name: "暂停动画", exact: true }).count(), 0);
    await animation.getByRole("button", { name: "演示下一步", exact: true }).click();
    assert.equal(
      await animation.locator("[data-function-step]").getAttribute("data-function-step"),
      "2",
    );
  });
  await check("manual_pause_keeps_the_same_function_point", async () => {
    await animation.getByRole("button", { name: "函数关键步骤 2", exact: true }).click();
    await animation.getByRole("button", { name: "播放动画", exact: true }).click();
    await page.waitForFunction(
      () =>
        Number(
          document
            .querySelector('[data-teaching-animation="function_trace"] [data-function-cursor]')
            ?.getAttribute("data-function-x"),
        ) > -0.999,
    );
    await animation.getByRole("button", { name: "暂停动画", exact: true }).click();
    const before = await animation
      .locator("[data-function-cursor]")
      .getAttribute("data-function-x");
    await page.evaluate(
      () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))),
    );
    assert.equal(
      await animation.locator("[data-function-cursor]").getAttribute("data-function-x"),
      before,
    );
    await animation.getByRole("button", { name: "函数关键步骤 3", exact: true }).click();
  });
  await check("zoom_shares_same_progress_and_reset", async () => {
    await card.getByRole("button", { name: "放大图示", exact: true }).click();
    const dialog = page.getByRole("dialog");
    await dialog.waitFor();
    assert.equal(
      await dialog.locator("[data-function-step]").getAttribute("data-function-step"),
      "2",
    );
    await dialog.getByRole("button", { name: "重置动画", exact: true }).click();
    await page.keyboard.press("Escape");
    await dialog.waitFor({ state: "hidden" });
    assert.equal(
      await animation.locator("[data-function-step]").getAttribute("data-function-step"),
      "0",
    );
  });
  await check("collapse_expand_preserves_function_and_steps", async () => {
    await card.getByRole("button", { name: "收起图示", exact: true }).click();
    await card.getByRole("button", { name: "展开图示", exact: true }).click();
    assert.equal(
      await animation.locator("[data-function-step]").getAttribute("data-function-step"),
      "0",
    );
  });
  await check("exact_above_question_does_not_request_reupload", async () => {
    const r = await send("就是上面那道题");
    assert(r.text.includes("−3"));
    assert.notEqual(r.teaching_action, "clarify");
  });
  await page.reload();
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  await check("accepted_animation_replays_after_refresh", async () => {
    await page.locator('[data-teaching-animation="function_trace"]').first().waitFor();
    assert.equal(await page.locator('[data-teaching-animation="function_trace"]').count(), 2);
  });
  await page
    .locator('[data-teaching-animation="function_trace"]')
    .first()
    .getByRole("button", { name: "函数关键步骤 4", exact: true })
    .click();
  await page.setViewportSize({ width: 1440, height: 1800 });
  await page
    .locator('[data-teaching-visual="animation_scene"]')
    .first()
    .screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/conversation-function-animation.png", import.meta.url),
      ),
    });
  await check("mobile_readout_and_steps_remain_usable", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page
      .locator('[data-teaching-animation="function_trace"]')
      .first()
      .getByRole("button", { name: "演示下一步", exact: true })
      .click();
  });
  await check("reduced_motion_uses_steps_without_continuous_playback", async () => {
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.waitForFunction(
      () =>
        document.querySelector(
          '[data-teaching-animation="function_trace"] button[aria-label="播放动画"]',
        )?.disabled === true,
    );
    assert(
      await page
        .locator('[data-teaching-animation="function_trace"]')
        .first()
        .getByRole("button", { name: "播放动画", exact: true })
        .isDisabled(),
    );
  });
  await check("no_browser_errors", async () => assert.deepEqual(errors, []));
  await writeFile(
    new URL("../.local/reports/conversation-browser.local.json", import.meta.url),
    JSON.stringify({ passed: checks.length, checks }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
