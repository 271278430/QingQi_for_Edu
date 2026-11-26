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
  [fileURLToPath(new URL("geometry_product_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let browser,
  stderr = "";
child.stderr.on("data", (v) => (stderr += v));
const checks = [];
async function check(name, fn) {
  await fn();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(Error(stderr)), 30000);
    lines.once("line", (l) => {
      clearTimeout(timer);
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
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } }),
    errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByLabel("上传题目图片").setInputFiles(setup.image);
  await page.getByLabel("待发送图片").getByRole("img").waitFor();
  async function send(q) {
    await page.getByLabel("你的学习问题", { exact: true }).fill(q);
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const result = await readTeachResponse(await waiting);
    assert(result.session);
    await page.waitForFunction(() => !document.querySelector("#edu-question").disabled);
    return result;
  }
  const first = await send("第（1）问：为什么要连接CD？请讲清楚当前这一步。");
  await check("relationship_explanation_shows_only_one_static_picture", async () => {
    assert.equal(first.response.visuals.length, 1);
    assert.equal(first.response.visuals[0].kind, "coordinates");
    assert.equal(await page.getByRole("button", { name: "播放动画", exact: true }).count(), 0);
    assert(!first.response.visuals.some((v) => /第（1）问.*第（1）问/.test(v.title)));
  });
  const dynamic = await send("第（1）问：请用动画解释旋转这一步为什么成立。");
  await check("explicit_process_request_shows_only_one_related_animation", async () => {
    assert.equal(dynamic.response.visuals.length, 1);
    assert.equal(dynamic.response.visuals[0].kind, "animation_scene");
    await page.getByRole("button", { name: "播放动画", exact: true }).last().waitFor();
    assert.equal(
      await page.locator("article.edu-message").last().locator(".edu-teaching-card").count(),
      1,
    );
  });
  await check("playback_changes_geometry_and_reaches_the_last_step", async () => {
    const figure = page.locator("[data-geometry-progress]").last();
    const before = await figure.locator("svg").innerHTML();
    await page.getByRole("button", { name: "播放动画", exact: true }).last().click();
    await page.waitForFunction(
      () =>
        Number(
          [...document.querySelectorAll("[data-geometry-progress]")]
            .at(-1)
            ?.getAttribute("data-geometry-progress"),
        ) > 0.55,
    );
    assert.notEqual(await figure.locator("svg").innerHTML(), before);
    await page.waitForFunction(
      () =>
        Number(
          [...document.querySelectorAll("[data-geometry-progress]")]
            .at(-1)
            ?.getAttribute("data-geometry-progress"),
        ) >= 1,
      {},
      { timeout: 30000 },
    );
  });
  await check("refresh_preserves_teaching_mode_with_one_visual_per_reply", async () => {
    await page.reload();
    await page.getByRole("button", { name: "播放动画", exact: true }).last().waitFor();
    const result = await send("继续讲这一步");
    assert.equal(result.response.route.teaching.mode, "explain");
    assert.equal(result.response.visuals.length, 1);
  });
  await page.screenshot({ path: "education/.local/reports/contextual-teaching-desktop.local.png" });
  await check("mobile_single_visual_and_annotation_controls_remain_usable", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    assert(await page.getByRole("button", { name: "标注图示", exact: true }).last().isVisible());
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    assert.deepEqual(errors, []);
  });
  await writeFile(
    "education/.local/reports/contextual-teaching-browser.local.json",
    JSON.stringify({ checks, passed: checks.length, errors, isolated: true }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
}
