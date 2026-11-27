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
  [fileURLToPath(new URL("instruction_visual_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["pipe", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout }),
  checks = [],
  errors = [];
let browser,
  stderr = "",
  stressChild,
  stressLines;
child.stderr.on("data", (v) => (stderr += v));
async function check(name, fn) {
  await fn();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
async function overlaps(svg) {
  return svg.evaluate((node) => {
    const labels = [...node.querySelectorAll("text")]
      .filter((n) => n.getBoundingClientRect().width > 0)
      .map((n) => ({ text: n.textContent, box: n.getBBox() }));
    const bad = [];
    for (let i = 0; i < labels.length; i++)
      for (let j = i + 1; j < labels.length; j++) {
        const a = labels[i].box,
          b = labels[j].box;
        if (
          a.x < b.x + b.width - 1 &&
          a.x + a.width > b.x + 1 &&
          a.y < b.y + b.height - 1 &&
          a.y + a.height > b.y + 1
        )
          bad.push([labels[i].text, labels[j].text]);
      }
    return bad;
  });
}
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(
      () => reject(Error(stderr || "fixture timeout")),
      20000,
    );
    lines.once("line", (line) => {
      clearTimeout(timer);
      resolve(JSON.parse(line));
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
    viewport: { width: 1280, height: 960 },
  });
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(setup.base);
  await page.getByRole("textbox", { name: "你的学习问题" }).waitFor();
  const svg = page.locator("[data-number-line]").last();
  await check(
    "reported_legacy_number_line_has_no_overlapping_text",
    async () => {
      await svg.waitFor();
      assert.deepEqual(await overlaps(svg), []);
      assert((await svg.textContent()).includes("2.061"));
    },
  );
  await check("complete_answer_and_redraw_are_both_delivered", async () => {
    await page
      .getByRole("textbox", { name: "你的学习问题" })
      .fill("重新画过一张图给我，并且这次给我把这道题的答案全部给我");
    const request = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "发送学习问题", exact: true })
      .click();
    const value = await readTeachResponse(await request);
    assert(value.response.route.teaching.allow_final_answer);
    assert.equal(value.response.teaching_action, "give_answer");
    assert(value.response.text.includes(setup.answer));
    assert.equal(value.response.visuals.length, 1);
    await page
      .getByRole("button", { name: "发送学习问题", exact: true })
      .waitFor();
    await page.locator("[data-number-line]").last().waitFor();
  });
  await check(
    "redrawn_chart_keeps_given_numbers_and_never_adds_a_fake_addition_rule",
    async () => {
      const current = page.locator("[data-number-line]").last();
      assert.deepEqual(await overlaps(current), []);
      assert((await current.textContent()).includes("2.061"));
      assert(!(await current.textContent()).includes("+≈12.92"));
      assert.equal(
        (
          (
            await current
              .locator("[data-number-line-legend]")
              .last()
              .textContent()
          ).match(/1\.436/g) || []
        ).length,
        1,
      );
      await current.screenshot({
        path: "education/.local/reports/number-line-desktop.png",
      });
    },
  );
  await check("mobile_labels_wrap_without_overflow", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.waitForTimeout(200);
    assert.deepEqual(
      await overlaps(page.locator("[data-number-line]").last()),
      [],
    );
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    await page
      .locator("[data-number-line]")
      .last()
      .screenshot({ path: "education/.local/reports/number-line-mobile.png" });
  });
  await check("annotation_snapshot_keeps_complete_legend", async () => {
    await page
      .getByRole("button", { name: "标注图示", exact: true })
      .last()
      .click();
    const canvas = page.getByRole("dialog").locator("canvas");
    await canvas.waitFor();
    assert(await canvas.evaluate((n) => n.height > 300 && n.width > 300));
    const box = await canvas.boundingBox();
    await page.mouse.move(box.x + 20, box.y + 20);
    await page.mouse.down();
    await page.mouse.move(box.x + 65, box.y + 65, { steps: 4 });
    await page.mouse.up();
    await page.getByRole("button", { name: "返回对话", exact: true }).click();
    await page.getByLabel("待发送图片").getByRole("img").waitFor();
  });
  await check("eight_nearby_points_and_long_labels_stay_readable", async () => {
    stressChild = spawn(
      process.env.QINGQI_PYTHON,
      [
        fileURLToPath(
          new URL("instruction_visual_fixture.py", import.meta.url),
        ),
        "stress",
      ],
      { windowsHide: true, stdio: ["pipe", "pipe", "pipe"] },
    );
    stressLines = createInterface({ input: stressChild.stdout });
    const stress = await new Promise((resolve, reject) => {
      const timer = setTimeout(
        () => reject(Error("stress fixture timeout")),
        20000,
      );
      stressLines.once("line", (line) => {
        clearTimeout(timer);
        resolve(JSON.parse(line));
      });
    });
    const other = await browser.newPage({
      viewport: { width: 390, height: 844 },
    });
    other.on("pageerror", (e) => errors.push(e.message));
    await other.goto(stress.base);
    const figure = other.locator("[data-number-line]").last();
    await figure.waitFor();
    await other.waitForTimeout(200);
    assert.deepEqual(await overlaps(figure), []);
    assert.equal(await figure.locator("[data-point-id]").count(), 8);
    assert(
      await figure.evaluate(
        (n) =>
          n.getBoundingClientRect().height / n.viewBox.baseVal.height > 0.8,
      ),
    );
    assert(
      await other.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    await other.close();
  });
  await check("no_uncaught_render_errors", async () =>
    assert.deepEqual(errors, []),
  );
} finally {
  await browser?.close();
  child.stdin.end();
  stressChild?.stdin.end();
  stressLines?.close();
  lines.close();
}
await writeFile(
  "education/.local/reports/number-line-browser.local.json",
  JSON.stringify({ checks, passed: checks.length }, null, 2),
);
