// Isolated real browser, function-call HTTP fixture and actual ZCode renderers.
import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile, mkdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const child = spawn(
  process.env.QINGQI_PYTHON || "python",
  [fileURLToPath(new URL("./visual_teaching_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
const checks = [],
  errors = [];
let browser,
  stderr = "";
child.stderr.on("data", (value) => {
  stderr += value;
});
async function check(name, fn) {
  await fn();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`fixture timeout: ${stderr}`)), 30000);
    lines.once("line", (line) => {
      clearTimeout(timer);
      resolve(JSON.parse(line));
    });
    child.once("error", reject);
    child.once("exit", (code) => {
      clearTimeout(timer);
      reject(new Error(`fixture ${code}: ${stderr}`));
    });
  });
  browser = await chromium.launch({
    executablePath: [
      "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
      "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    ].find(existsSync),
    headless: true,
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  page.setDefaultTimeout(30000);
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  async function submit(question) {
    await page.getByLabel("你的学习问题", { exact: true }).fill(question);
    const received = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const response = await received;
    assert.equal(response.status(), 200);
    await page.waitForFunction(() => {
      const input = document.querySelector("#edu-question");
      return input && !input.disabled && input.value === "";
    });
    return response.json();
  }
  await check("image_question_visual_in_assistant_message", async () => {
    await page.locator('input[type="file"]').setInputFiles({
      name: "geometry.png",
      mimeType: "image/png",
      buffer: Buffer.from(setup.image, "base64"),
    });
    await page
      .getByRole("button", { name: "发送学习问题", exact: true })
      .waitFor({ state: "visible" });
    await submit("请用数轴例子帮助理解，不要直接给答案。");
    await page.locator('[data-teaching-visual="number_line"] svg.edu-teaching-svg').waitFor();
    assert.equal(
      await page.locator(".edu-message").last().locator('[aria-label="本条消息的图片"]').count(),
      1,
    );
  });
  await check("number_line_step_reset_collapse_and_dialog", async () => {
    const card = page.locator('[data-teaching-visual="number_line"]').last();
    await card.getByRole("button", { name: "演示下一步", exact: true }).click();
    assert.equal(await card.locator('[data-move-visible="true"]').count(), 1);
    await card.getByRole("button", { name: "重置演示", exact: true }).click();
    assert.equal(await card.locator('[data-move-visible="true"]').count(), 0);
    await card.getByRole("button", { name: "收起图示", exact: true }).click();
    assert.equal(await card.locator("svg.edu-teaching-svg").count(), 0);
    await card.getByRole("button", { name: "展开图示", exact: true }).click();
    await card.getByRole("button", { name: "放大图示", exact: true }).click();
    await page.getByRole("dialog").locator("svg.edu-teaching-svg").waitFor();
    await page.keyboard.press("Escape");
    await page.getByRole("dialog").waitFor({ state: "hidden" });
  });
  for (const [word, kind, selector] of [
    ["坐标", "coordinates", "svg.edu-teaching-svg"],
    ["表格", "table", "table"],
    ["柱状", "bar_chart", ".recharts-wrapper"],
    ["情景", "scene", "[data-mermaid-block] svg"],
  ]) {
    await check(`upstream_or_parameterized_${kind}`, async () => {
      await submit(`请用${word}帮助理解当前题目。`);
      await page.locator(`[data-teaching-visual="${kind}"]`).last().locator(selector).waitFor();
    });
  }
  await check("two_figures_and_plain_text_optional", async () => {
    await submit("请用两张数轴和表格帮助理解。");
    assert.equal(
      await page.locator(".edu-message").last().locator("[data-teaching-visual]").count(),
      2,
    );
    await submit("普通对话：我今天有点累，先聊聊学习。");
    assert.equal(
      await page.locator(".edu-message").last().locator("[data-teaching-visual]").count(),
      0,
    );
  });
  await check("refresh_keeps_figures_and_only_four_navigation_items", async () => {
    await page.reload();
    await page.locator('[data-teaching-visual="number_line"]').first().waitFor();
    assert.equal(await page.locator("[data-teaching-visual]").count(), 7);
    for (const name of ["个性化辅导", "学习路径", "学情看板", "个性化练习"])
      assert.equal(await page.getByRole("button", { name, exact: true }).count(), 1);
  });
  await mkdir(fileURLToPath(new URL("../.local/reports/visual-teaching-browser", import.meta.url)), {
    recursive: true,
  });
  await check("desktop_light_figures_visible", async () => {
    const switchLight = page.getByRole("button", { name: "切换浅色主题", exact: true });
    if (await switchLight.count()) await switchLight.click();
    const line = page.locator('[data-teaching-visual="number_line"]').first();
    await line.scrollIntoViewIfNeeded();
    await line.getByRole("button", { name: "演示下一步", exact: true }).click();
    const bounds = await line.locator("svg.edu-teaching-svg").boundingBox();
    assert(bounds.width > 300 && bounds.height > 50);
    await line.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/visual-teaching-browser/number-line-light.png", import.meta.url),
      ),
    });
    const table = page.locator('[data-teaching-visual="table"]').first();
    await table.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/visual-teaching-browser/table-light.png", import.meta.url),
      ),
    });
    const chart = page.locator('[data-teaching-visual="bar_chart"]').first();
    await chart.locator(".recharts-wrapper").waitFor();
    await chart.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/visual-teaching-browser/chart-light.png", import.meta.url),
      ),
    });
  });
  await page.screenshot({
    path: fileURLToPath(new URL("../.local/reports/visual-teaching-browser/desktop.png", import.meta.url)),
  });
  await check("mobile_dark_no_horizontal_overflow", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.emulateMedia({ colorScheme: "dark", reducedMotion: "reduce" });
    const switchDark = page.getByRole("button", { name: "切换深色主题", exact: true });
    if (await switchDark.count()) await switchDark.click();
    await page.reload();
    await page.locator('[data-teaching-visual="scene"] [data-mermaid-block] svg').waitFor();
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    const card = page.locator('[data-teaching-visual="scene"]').last();
    await card.scrollIntoViewIfNeeded();
    await card.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/visual-teaching-browser/scene-card.png", import.meta.url),
      ),
    });
    await page.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/visual-teaching-browser/mobile-dark.png", import.meta.url),
      ),
    });
    await card.getByRole("button", { name: "放大图示", exact: true }).click();
    await page.getByRole("dialog").locator("[data-mermaid-block] svg").waitFor();
    await page.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/visual-teaching-browser/mobile-dialog.png", import.meta.url),
      ),
    });
    await page.keyboard.press("Escape");
    assert.deepEqual(errors, []);
  });
} finally {
  await browser?.close();
  child.kill();
  await writeFile(
    new URL("../.local/reports/visual-teaching-browser-acceptance.json", import.meta.url),
    JSON.stringify(
      { passed: checks.length, checks, page_errors: errors, realModel: false },
      null,
      2,
    ),
  );
}
