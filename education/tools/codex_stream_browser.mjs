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
  [fileURLToPath(new URL("codex_stream_fixture.py", import.meta.url))],
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
  const page = await browser.newPage({
      viewport: { width: 1440, height: 1000 },
    }),
    errors = [],
    requests = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("request", (r) => {
    if (r.url().endsWith("/api/teach") && r.method() === "POST") requests.push(r.postDataJSON());
  });
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  await page.getByLabel("上传题目图片").setInputFiles(setup.image);
  await page.getByLabel("待发送图片").getByRole("img").waitFor();
  const initialWait = page.waitForResponse(
    (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
  );
  await page.getByLabel("你的学习问题", { exact: true }).fill("教我这道题");
  await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
  const first = await readTeachResponse(await initialWait);
  await page.waitForFunction(
    () =>
      !document.querySelector("#edu-question").disabled &&
      document.querySelector("#edu-question").value === "",
  );
  async function annotate(question) {
    await page.getByRole("button", { name: "标注图示", exact: true }).first().click();
    const canvas = page.locator("[data-annotation-canvas]");
    await canvas.waitFor();
    const box = await canvas.boundingBox();
    await page.mouse.move(box.x + box.width * 0.3, box.y + box.height * 0.4);
    await page.mouse.down();
    await page.mouse.move(box.x + box.width * 0.7, box.y + box.height * 0.4);
    await page.mouse.up();
    await page.getByRole("button", { name: "返回对话", exact: true }).click();
    await canvas.waitFor({ state: "detached" });
    await page.getByLabel("待发送图片").getByRole("img").waitFor();
    await page.getByLabel("你的学习问题", { exact: true }).fill(question);
  }
  await annotate("这根辅助线是否有帮助，先给一点提示");
  await check("unpunctuated_provider_delta_appears_while_request_is_still_open", async () => {
    const before = (await (await page.request.get(setup.stats)).json()).calls;
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const response = await waiting;
    const draft = page.getByTestId("tutor-stream-draft");
    await draft.waitFor({ timeout: 5000 });
    await page.waitForFunction(() =>
      document
        .querySelector('[data-testid="tutor-stream-draft"]')
        ?.textContent.includes("先看红色辅助线"),
    );
    assert(!(await page.getByLabel("你的学习问题", { exact: true }).isEnabled()));
    assert(!(await draft.innerText()).includes("不要把这段内部推理"));
    const value = await readTeachResponse(response);
    assert.equal(value.response.teaching_action, "ask");
    await page.waitForFunction(() => document.querySelector("#edu-question").value === "");
    assert.equal(await draft.count(), 0);
    const stats = await (await page.request.get(setup.stats)).json();
    assert.equal(
      stats.calls,
      before + 1,
      "streaming length-only overrun caused another full model request",
    );
    assert(stats.reasoning_efforts.every((value) => value === "high"));
  });
  await annotate("请模拟截断后继续讨论这根辅助线，不要给完整答案");
  await check("truncation_preserves_this_turn_snapshot_and_unaccepted_text", async () => {
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    await page.getByRole("alert").filter({ hasText: "输出预算" }).waitFor();
    await page.getByTestId("tutor-incomplete-reply").waitFor();
    await page.waitForFunction(() => !document.querySelector("#edu-question").disabled);
    assert(
      (await page.getByTestId("tutor-incomplete-reply").innerText()).includes("先看红色辅助线"),
    );
    const message = page.locator("article.edu-message").last();
    assert((await message.innerText()).includes("请模拟截断"));
    assert.equal(await message.getByRole("button", { name: "继续此请求", exact: true }).count(), 0);
    assert((await requests.at(-1).request.visual_context.run_id) === first.response.run_id);
  });
  const failed = requests.at(-1);
  await check("refresh_keeps_the_failed_partial_reply_without_accepting_it", async () => {
    await page.reload();
    await page.getByTestId("tutor-incomplete-reply").waitFor();
    assert((await page.getByTestId("tutor-incomplete-reply").innerText()).includes("回复未完成"));
  });
  await check("explicit_restart_uses_a_new_id_and_the_same_original_annotation", async () => {
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page
      .locator("article.edu-message")
      .last()
      .getByRole("button", { name: "重新回答", exact: true })
      .click();
    const value = await readTeachResponse(await waiting);
    assert.equal(value.response.teaching_action, "ask");
    const next = requests.at(-1);
    assert.notEqual(next.request.request_id, failed.request.request_id);
    assert.deepEqual(next.request.visual_context, failed.request.visual_context);
    assert.deepEqual(next.request.images, failed.request.images);
    assert.equal(next.request.question, failed.request.question);
    await page.waitForFunction(() => !document.querySelector("#edu-question").disabled);
    assert.deepEqual(errors, []);
  });
  await writeFile(
    "education/.local/reports/codex-stream-browser.local.json",
    JSON.stringify({ passed: checks.length, checks, pageErrors: errors }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
