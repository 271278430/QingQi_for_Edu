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
  [fileURLToPath(new URL("owned_visual_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["pipe", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout }),
  checks = [],
  errors = [];
let browser,
  stderr = "";
child.stderr.on("data", (v) => (stderr += v));
async function check(name, action) {
  await action();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
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
    viewport: { width: 1366, height: 960 },
  });
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(setup.base);
  await page.getByRole("textbox", { name: "你的学习问题" }).waitFor();
  await check(
    "reported_message_delivers_animation_instead_of_output_budget_error",
    async () => {
      const response = page.waitForResponse(
        (r) =>
          r.url().endsWith("/api/teach") && r.request().method() === "POST",
      );
      await page
        .getByRole("button", { name: "重新回答", exact: true })
        .last()
        .click();
      const value = await readTeachResponse(await response);
      assert.equal(value.response.visuals[0].template, "opposite_numbers");
      await page
        .locator('[data-teaching-animation="opposite_numbers"]')
        .waitFor();
      assert.equal(value.session.messages.at(-1).trace.error_code, null);
      assert(
        value.session.messages.some(
          (m) =>
            m.request_id === "old-truncated-animation" &&
            m.trace.error_code === "model_truncated",
        ),
      );
    },
  );
  const animation = page
    .locator('[data-teaching-animation="opposite_numbers"]')
    .last();
  await check(
    "play_advances_both_points_continuously_to_the_final_relation",
    async () => {
      await animation
        .getByRole("button", { name: "播放动画", exact: true })
        .click();
      await page.waitForFunction(
        () => {
          const progress = Number(
            document
              .querySelector('[data-teaching-animation="opposite_numbers"]')
              .getAttribute("data-animation-progress"),
          );
          return progress > 0 && progress < 1;
        },
        {},
        { timeout: 6000 },
      );
      const progress = Number(
        await animation.getAttribute("data-animation-progress"),
      );
      assert(progress > 0 && progress < 1);
      const plot = animation.locator("[data-opposite-value]");
      // 两个连续动画读数必须在同一帧读取，分别await可能取到前后帧，误报对称关系。
      assert(
        await plot.evaluate(
          (node) =>
            Math.abs(
              Number(node.getAttribute("data-opposite-value")) +
                Number(node.getAttribute("data-opposite-mirror")),
            ) < 1e-10,
        ),
      );
      await page.waitForFunction(
        () =>
          Number(
            document
              .querySelector('[data-teaching-animation="opposite_numbers"]')
              .getAttribute("data-animation-progress"),
          ) >= 0.999,
        {},
        { timeout: 17000 },
      );
      assert((await animation.innerText()).includes("和为 0"));
    },
  );
  await check(
    "previous_and_next_show_meaningful_explanation_stages",
    async () => {
      await animation
        .getByRole("button", { name: "演示上一步", exact: true })
        .click();
      await page.waitForTimeout(3500);
      assert(
        Number(await animation.getAttribute("data-animation-progress")) < 1,
      );
      await animation
        .getByRole("button", { name: "演示下一步", exact: true })
        .click();
      await page.waitForFunction(
        () =>
          Number(
            document
              .querySelector('[data-teaching-animation="opposite_numbers"]')
              .getAttribute("data-animation-progress"),
          ) >= 0.999,
        {},
        { timeout: 6000 },
      );
    },
  );
  await check("refresh_keeps_animation_and_current_question", async () => {
    await page.reload();
    await page
      .locator('[data-teaching-animation="opposite_numbers"]')
      .waitFor();
    assert(await page.getByText("正在讨论", { exact: false }).count());
  });
  await check("mobile_has_no_overflow_or_render_failure", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    assert.deepEqual(errors, []);
    await page
      .locator('[data-teaching-animation="opposite_numbers"]')
      .last()
      .scrollIntoViewIfNeeded();
    await page.screenshot({
      path: "education/.local/reports/owned-visual-mobile.png",
    });
  });
} finally {
  await browser?.close();
  child.stdin.end();
  lines.close();
}
await writeFile(
  "education/.local/reports/owned-visual-browser.local.json",
  JSON.stringify({ checks, passed: checks.length }, null, 2),
);
