import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

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
    const timer = setTimeout(
      () => reject(Error(stderr || "fixture timeout")),
      30000,
    );
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
    viewport: { width: 1440, height: 1000 },
  });
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  await page.getByLabel("上传题目图片").setInputFiles(setup.image);
  await page.getByLabel("待发送图片").getByRole("img").waitFor();
  await page.locator("#edu-question").fill("分别给出动画和情景教学");
  let failedId;
  await page.route(
    "**/api/teach",
    async (route) => {
      failedId = route.request().postDataJSON().request.request_id;
      await route.fulfill({
        status: 502,
        contentType: "application/json",
        body: JSON.stringify({
          error: "model_protocol",
          message:
            "模型回复未符合本次教学要求，该请求已停止。记录已保留，请编辑后作为新问题发送。",
          recoverable: false,
        }),
      });
    },
    { times: 1 },
  );
  await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
  await check(
    "failed_request_keeps_image_and_editable_text_for_new_command",
    async () => {
      await page.getByRole("alert").waitFor();
      assert.equal(
        await page.locator("#edu-question").inputValue(),
        "分别给出动画和情景教学",
      );
      assert.equal(
        await page.getByLabel("待发送图片").getByRole("img").count(),
        1,
      );
      await page
        .getByRole("button", { name: "发送学习问题", exact: true })
        .waitFor({ state: "visible" });
    },
  );
  const waiting = page.waitForResponse(
    (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
  );
  await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
  const result = await waiting;
  assert.equal(result.status(), 200);
  assert.notEqual(result.request().postDataJSON().request.request_id, failedId);
  const accepted = (await result.json()).response;
  const animations = page.locator('[data-teaching-animation="function_trace"]');
  await check(
    "reported_image_request_renders_both_animation_and_story",
    async () => {
      await animations.nth(1).waitFor();
      assert.equal(accepted.visuals.length, 2);
      assert.match(accepted.text, /情景教学[\s\S]*相切[\s\S]*动画/);
      assert.equal(await page.getByRole("alert").count(), 0);
      assert.equal(await page.locator(".katex-error").count(), 0);
      assert.equal(await page.getByLabel("待发送图片").count(), 0);
      assert.equal(
        await page
          .locator(".edu-message")
          .getByRole("img", { name: "cubic.png", exact: true })
          .count(),
        1,
      );
      await page.screenshot({
        path: fileURLToPath(
          new URL(
            "../.local/reports/combined-presentation-desktop.png",
            import.meta.url,
          ),
        ),
      });
    },
  );
  const first = animations.first();
  await check(
    "one_play_reaches_the_end_and_step_controls_remain_usable",
    async () => {
      await first
        .getByRole("button", { name: "播放动画", exact: true })
        .click();
      await page.waitForFunction(
        () =>
          document
            .querySelector('[data-teaching-animation="function_trace"]')
            ?.getAttribute("data-animation-progress") === "1",
        null,
        { timeout: 22000 },
      );
      await first
        .getByRole("button", { name: "演示上一步", exact: true })
        .click();
      await first
        .getByRole("button", { name: "播放动画", exact: true })
        .waitFor();
      assert.notEqual(await first.getAttribute("data-animation-progress"), "1");
    },
  );
  await check(
    "refresh_restores_uploaded_picture_story_and_two_figures",
    async () => {
      await page.reload();
      await animations.nth(1).waitFor();
      assert.equal(await page.getByRole("alert").count(), 0);
      assert.equal(
        await page
          .locator(".edu-message")
          .getByRole("img", { name: "cubic.png", exact: true })
          .count(),
        1,
      );
      assert.equal(await page.locator(".katex-error").count(), 0);
    },
  );
  await check("phone_layout_has_no_overflow_or_runtime_error", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    assert.deepEqual(errors, []);
    await page.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/combined-presentation-mobile.png", import.meta.url),
      ),
    });
  });
  await writeFile(
    new URL(
      "../.local/reports/combined-presentation-browser.local.json",
      import.meta.url,
    ),
    JSON.stringify({ passed: checks.length, checks, isolated: true }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
}
