import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
const child = spawn(
  process.env.QINGQI_PYTHON || "python",
  [fileURLToPath(new URL("./visual_tasks_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
const checks = [],
  errors = [];
let stderr = "",
  browser;
child.stderr.on("data", (v) => (stderr += v));
async function check(name, fn) {
  await fn();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error(stderr)), 30000);
    lines.once("line", (line) => {
      clearTimeout(timeout);
      resolve(JSON.parse(line));
    });
    child.once("error", reject);
  });
  browser = await chromium.launch({
    headless: true,
    executablePath: [
      "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
      "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    ].find(existsSync),
  });
  const page = await browser.newPage({
    viewport: { width: 1365, height: 950 },
  });
  page.setDefaultTimeout(30000);
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  async function submit(q) {
    await page.getByLabel("你的学习问题", { exact: true }).fill(q);
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "发送学习问题", exact: true })
      .click();
    const r = await waiting;
    assert.equal(r.status(), 200);
    await page.waitForFunction(() => {
      const e = document.querySelector("#edu-question");
      return e && !e.disabled && e.value === "";
    });
    return r.json();
  }
  await check("reported_square_really_connects_three_segments", async () => {
    await submit("你可以把这个坐标系的图片中的点都给我划线连起来吗");
    const plot = page.locator('[data-teaching-visual="coordinates"]').last();
    assert.equal(await plot.locator("[data-coordinate-segment]").count(), 3);
    assert.equal(await plot.locator("[data-coordinate-point]").count(), 3);
    await page.waitForFunction(() => {
      const svg = document.querySelector(
        '[data-teaching-visual="coordinates"] svg',
      );
      const viewport = document.querySelector(".edu-messages");
      if (!svg || !viewport) return false;
      const box = viewport.getBoundingClientRect();
      return [...svg.querySelectorAll("[data-coordinate-point] circle")].every(
        (p) => {
          const b = p.getBoundingClientRect();
          return b.top >= box.top && b.bottom <= box.bottom;
        },
      );
    });
    await page.screenshot({
      animations: "disabled",
      path: fileURLToPath(
        new URL("../.local/reports/visual-v3-connected-desktop.png", import.meta.url),
      ),
      fullPage: true,
    });
  });
  await check("stepwise_socratic_reply_has_combined_label", async () => {
    const r = await submit("能一步步苏格拉底式的讲解吗");
    assert.equal(r.response.route.teaching.label, "逐步引导");
    assert.equal(r.response.teaching_action, "ask");
    await page.getByText("逐步引导", { exact: true }).last().waitFor();
    await page
      .locator(".edu-message .katex")
      .filter({ hasText: "AB" })
      .last()
      .waitFor();
    await page
      .locator(".edu-message .katex")
      .filter({ hasText: "C(1" })
      .last()
      .waitFor();
    assert(
      !(await page.locator(".edu-message").last().innerText()).includes(
        "C(1,-2)$$",
      ),
    );
  });
  await check("drawing_animation_really_reveals_edges", async () => {
    await submit("请把图上的点逐条连起来，用动画展示。");
    const p = page
      .locator('[data-teaching-animation="coordinate_drawing"]')
      .last();
    assert.equal(await p.locator("[data-coordinate-segment]").count(), 0);
    await p.getByLabel("动画进度").press("ArrowRight");
    const growing = p.locator("[data-coordinate-segment] line").first();
    const partial = await growing.evaluate((line) => ({
      start: Number(line.getAttribute("x1")),
      end: Number(line.getAttribute("x2")),
    }));
    assert(partial.end > partial.start && partial.end - partial.start < 155);
    await p.getByRole("button", { name: "重置动画", exact: true }).click();
    await p.getByRole("button", { name: "演示下一步", exact: true }).click();
    assert.equal(await p.locator("[data-coordinate-segment]").count(), 1);
    await p.getByLabel("动画进度").press("End");
    assert.equal(await p.locator("[data-coordinate-segment]").count(), 3);
    await p.getByRole("button", { name: "重置动画", exact: true }).click();
    assert.equal(await p.locator("[data-coordinate-segment]").count(), 0);
  });
  await page.getByRole("button", { name: "新建学习对话", exact: true }).click();
  for (const [q, kind] of [
    ["请画一次函数示例图。", "function_plot"],
    ["请画二次函数示例图。", "function_plot"],
    ["请画分数面积图。", "area_model"],
    ["请画带辅助线的三角形几何图。", "coordinates"],
  ])
    await check("actual_" + q, async () => {
      await submit(q);
      await page
        .locator(`[data-teaching-visual="${kind}"] svg`)
        .last()
        .waitFor();
      if (kind === "function_plot")
        assert((await page.locator("[data-function-y-tick]").count()) >= 2);
    });
  for (const [q, template] of [
    ["请用分数动画解释。", "fraction_fill"],
    ["请用勾股动画解释。", "pythagorean"],
  ])
    await check("actual_" + template, async () => {
      await submit(q);
      const p = page.locator(`[data-teaching-animation="${template}"]`).last();
      await p.getByLabel("动画进度").press("End");
      assert(
        (await p.getByTestId("animation-readout").textContent()).length > 8,
      );
    });
  await check("new_plots_fit_mobile_and_persist", async () => {
    await page.reload();
    await page.locator('[data-teaching-animation="pythagorean"]').waitFor();
    await page.setViewportSize({ width: 390, height: 844 });
    await page.emulateMedia({ colorScheme: "dark", reducedMotion: "reduce" });
    await page.reload();
    const p = page.locator('[data-teaching-animation="pythagorean"]').last();
    await p.scrollIntoViewIfNeeded();
    assert(
      await p
        .getByRole("button", { name: "播放动画", exact: true })
        .isDisabled(),
    );
    await page.screenshot({
      animations: "disabled",
      path: fileURLToPath(
        new URL("../.local/reports/visual-v3-mobile.png", import.meta.url),
      ),
      fullPage: true,
    });
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    assert.deepEqual(errors, []);
  });
} finally {
  await browser?.close();
  child.kill();
  await writeFile(
    new URL("../.local/reports/visual-tasks-v3-browser.json", import.meta.url),
    JSON.stringify(
      { passed: checks.length, checks, errors, real_model: false },
      null,
      2,
    ),
  );
}
