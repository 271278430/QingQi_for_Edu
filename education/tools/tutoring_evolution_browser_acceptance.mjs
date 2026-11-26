import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile, mkdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const child = spawn(
  process.env.QINGQI_PYTHON || "python",
  [fileURLToPath(new URL("./tutoring_evolution_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
const checks = [],
  errors = [];
let browser,
  stderr = "";
child.stderr.on("data", (v) => {
  stderr += v;
});
async function check(name, fn) {
  await fn();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(stderr)), 30000);
    lines.once("line", (l) => {
      clearTimeout(timer);
      resolve(JSON.parse(l));
    });
    child.once("error", reject);
  });
  browser = await chromium.launch({
    executablePath: [
      "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
      "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    ].find(existsSync),
    headless: true,
  });
  const page = await browser.newPage({ viewport: { width: 1365, height: 950 } });
  page.setDefaultTimeout(30000);
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  async function submit(q) {
    await page.getByLabel("你的学习问题", { exact: true }).fill(q);
    const wait = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const r = await wait;
    assert.equal(r.status(), 200);
    await page.waitForFunction(() => {
      const e = document.querySelector("#edu-question");
      return e && !e.disabled && e.value === "";
    });
    return r.json();
  }
  await check("clear_concept_question_answered_in_chat", async () => {
    const r = await submit("我不太理解绝对值，能告诉我怎么理解吗？");
    assert.equal(r.response.teaching_action, "explain");
    assert(r.response.text.includes("距离"));
    assert(!r.response.text.includes("你希望查询"));
  });
  await check("concept_followup_stays_in_simple_dialogue", async () => {
    const r = await submit("那负数呢？");
    assert.equal(r.response.teaching_action, "explain");
    assert(!r.response.text.includes("请提供"));
  });
  await check("animation_play_pause_step_seek_reset", async () => {
    await submit("请用距离动画演示绝对值。");
    const player = page.locator('[data-teaching-animation="absolute_distance"]').last();
    await player.waitFor();
    await player.getByRole("button", { name: "播放动画", exact: true }).click();
    await player.getByRole("button", { name: "暂停动画", exact: true }).waitFor();
    await player.getByRole("button", { name: "暂停动画", exact: true }).click();
    await player.getByRole("button", { name: "演示下一步", exact: true }).click();
    assert(Number(await player.getByLabel("动画进度").inputValue()) > 0);
    await player.getByLabel("动画进度").press("End");
    await player.getByRole("button", { name: "重置动画", exact: true }).click();
    assert.equal(await player.getByLabel("动画进度").inputValue(), "0");
    assert.match(await player.getByTestId("animation-readout").textContent(), /位置 -4.*距离 4/);
    await player.getByLabel("动画进度").press("End");
    assert.match(await player.getByTestId("animation-readout").textContent(), /位置 4.*距离 4/);
  });
  for (const [word, template] of [
    ["开方", "square_root"],
    ["非负", "nonnegative_sum"],
    ["加减", "number_line_motion"],
    ["路程", "travel_motion"],
  ])
    await check("render_" + template, async () => {
      await submit(`请用${word}动画帮助理解。`);
      await page
        .locator(`[data-teaching-animation="${template}"] svg.edu-animation-svg`)
        .last()
        .waitFor();
      const player = page.locator(`[data-teaching-animation="${template}"]`).last();
      await player.getByLabel("动画进度").press("End");
      const expected = {
        square_root: /边长 4.*面积 16/,
        nonnegative_sum: /甲项 0.*乙项 0.*总量 0/,
        number_line_motion: /起点 -2.*移动 4.*当前位置 2/,
        travel_motion: /8 秒.*甲的位置 8 米.*乙的位置 32 米/,
      };
      assert.match(await player.getByTestId("animation-readout").textContent(), expected[template]);
    });
  await mkdir(fileURLToPath(new URL("../.local/reports/tutoring-evolution-browser/", import.meta.url)), {
    recursive: true,
  });
  await check("refresh_same_animation_without_model_generation", async () => {
    await page.reload();
    await page.locator('[data-teaching-animation="travel_motion"]').waitFor();
    assert.equal(await page.locator("[data-teaching-animation]").count(), 5);
  });
  await check("mobile_dark_reduced_motion_and_dialog", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.emulateMedia({ colorScheme: "dark", reducedMotion: "reduce" });
    await page.reload();
    const player = page.locator('[data-teaching-animation="travel_motion"]').last();
    await player.waitFor();
    await player.scrollIntoViewIfNeeded();
    assert(await player.getByRole("button", { name: "播放动画", exact: true }).isDisabled());
    const card = page.locator('[data-teaching-visual="animation_scene"]').last();
    await card.getByRole("button", { name: "放大图示", exact: true }).click();
    await page.getByRole("dialog").locator("[data-teaching-animation]").waitFor();
    await page.screenshot({
      animations: "disabled",
      path: fileURLToPath(
        new URL("../.local/reports/tutoring-evolution-browser/mobile-animation.png", import.meta.url),
      ),
    });
    await page.keyboard.press("Escape");
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    assert.deepEqual(errors, []);
  });
  await check("text_protocol_failure_keeps_editable_draft", async () => {
    const q = "测试持续空回复，请简短解释绝对值。";
    await page.getByLabel("你的学习问题", { exact: true }).fill(q);
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const r = await waiting;
    assert.equal(r.status(), 502);
    assert.equal((await r.json()).error, "model_protocol");
    await page.waitForFunction(() => !document.querySelector("#edu-question")?.disabled);
    assert.equal(await page.getByLabel("你的学习问题", { exact: true }).inputValue(), q);
    assert(!((await page.locator("body").textContent()) ?? "").includes("账户、会话归属"));
  });
} finally {
  await browser?.close();
  child.kill();
  await writeFile(
    new URL("../.local/reports/tutoring-evolution-browser-acceptance.json", import.meta.url),
    JSON.stringify({ passed: checks.length, checks, errors, realModel: false }, null, 2),
  );
}
