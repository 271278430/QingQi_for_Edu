import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
import { readTeachResponse } from "./read_teach_response.mjs";
const browser = await chromium.launch({
  headless: true,
  executablePath: [
    "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
  ].find(existsSync),
});
const checks = [];
let child;
async function check(name, run) {
  await run();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
async function fixture(file) {
  child = spawn(process.env.QINGQI_PYTHON, [fileURLToPath(new URL(file, import.meta.url))], {
    windowsHide: true,
    stdio: ["ignore", "pipe", "pipe"],
  });
  let stderr = "";
  child.stderr.on("data", (c) => (stderr += c));
  const lines = createInterface({ input: child.stdout });
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(Error(stderr || "fixture timeout")), 30000);
    lines.once("line", (line) => {
      clearTimeout(timer);
      resolve(JSON.parse(line));
    });
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  return { page, setup };
}
try {
  let { page, setup } = await fixture("conversation_problem_fixture.py");
  await check("real_draft_is_visible_while_provider_is_still_streaming", async () => {
    await page.locator("#edu-question").fill("二次函数的顶点是什么？");
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const response = await waiting;
    const draft = page.getByTestId("tutor-stream-draft");
    try {
      await draft.waitFor({ timeout: 5000 });
    } catch (error) {
      process.stdout.write(
        JSON.stringify({
          status: response.status(),
          headers: response.headers(),
          events: await response.text(),
          visible: (await page.locator("body").innerText()).slice(-1200),
        }) + "\n",
      );
      throw error;
    }
    assert.match(await draft.innerText(), /顶点/);
    assert.notEqual(await page.locator("#edu-question").inputValue(), "");
    await page.waitForFunction(() => document.querySelector("#edu-question")?.value === "");
    assert.equal(await draft.count(), 0);
  });
  await page.close();
  child.kill();
  ({ page, setup } = await fixture("geometry_product_fixture.py"));
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  async function send(q) {
    await page.locator("#edu-question").fill(q);
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const result = await readTeachResponse(await waiting);
    await page.waitForFunction(() => document.querySelector("#edu-question")?.value === "");
    return result.response;
  }
  await page.getByLabel("上传题目图片").setInputFiles(setup.image);
  await page.getByLabel("待发送图片").getByRole("img").waitFor();
  const first = await send("请教我这道题。");
  assert.equal(first.tutoring_scope.active_part, 1);
  await check("mixed_request_shows_second_answer_and_third_guided_section", async () => {
    const value = await send("直接给我第二问答案，然后开始第三问教学。");
    assert.equal(value.tutoring_scope.active_part, 3);
    assert.match(value.text, /第（2）问.*参考解答[\s\S]*第（3）问.*启发式提示/);
    assert.equal(value.tutoring_scope.units[1].allow_final_answer, false);
    assert(!value.text.replaceAll(" ", "").includes("y=8"));
    assert.equal(value.teaching_action, "ask");
    await page
      // 等待Store提交后的article，不能截取done时会卸载的流式草稿div。
      .locator("article.edu-message")
      .filter({ hasText: "第（3）问" })
      .last()
      .screenshot({
        path: fileURLToPath(
          new URL("../.local/reports/scoped-tutoring-browser.png", import.meta.url),
        ),
      });
  });
  await check("refresh_and_next_turn_preserve_third_part", async () => {
    await page.reload();
    await page.locator("#edu-question").waitFor();
    const value = await send("继续教我下一步。");
    assert.equal(value.tutoring_scope.active_part, 3);
    assert.equal(value.teaching_action, "ask");
    assert(!value.text.includes("一般比值"));
    assert.deepEqual(errors, []);
  });
  await check("phone_layout_keeps_part_headers_readable", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    assert.equal(await page.getByRole("alert").count(), 0);
  });
  await writeFile(
    new URL("../.local/reports/scoped-stream-browser.local.json", import.meta.url),
    JSON.stringify({ passed: checks.length, checks, isolated: true }, null, 2),
  );
} finally {
  await browser.close();
  child?.kill();
}
