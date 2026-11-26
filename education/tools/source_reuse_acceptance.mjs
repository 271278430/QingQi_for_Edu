// Actual browser + isolated HTTP owner; controlled rich text is not a model-quality test.
import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
import { readTeachResponse, readTeachEvents } from "./read_teach_response.mjs";

const reports = fileURLToPath(new URL("../.local/reports/", import.meta.url));
const child = spawn(
  process.env.QINGQI_PYTHON || "python",
  [fileURLToPath(new URL("./source_reuse_server.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let stderr = "";
child.stderr.on("data", (value) => {
  stderr += value;
});
const tests = [],
  errors = [],
  consoleErrors = [],
  resourceErrors = [];
let browser, page;
let expectingUnknown = false;
let expectedConflictResponses = 0;
async function check(name, run) {
  await run();
  tests.push({ name, passed: true });
  process.stdout.write(JSON.stringify(tests.at(-1)) + "\n");
}
async function choose(page, label, option) {
  await page.getByRole("combobox", { name: label, exact: true }).click();
  await page.getByRole("option", { name: option, exact: true }).click();
}
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("fixture start timeout")), 30000);
    lines.once("line", (line) => {
      clearTimeout(timer);
      resolve(JSON.parse(line));
    });
    child.once("error", (error) => {
      clearTimeout(timer);
      reject(error);
    });
    child.once("exit", (code) => {
      clearTimeout(timer);
      reject(new Error(`fixture exited ${code}: ${stderr}`));
    });
  });
  const executablePath = [
    "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
  ].find(existsSync);
  browser = await chromium.launch(
    executablePath ? { executablePath, headless: true } : { channel: "msedge", headless: true },
  );
  const context = await browser.newContext({
    viewport: { width: 1440, height: 960 },
  });
  await context.addInitScript(() => {
    if (!localStorage.getItem("zcode-theme")) localStorage.setItem("zcode-theme", "zai-light");
    if (!localStorage.getItem("zcode-locale-preference"))
      localStorage.setItem("zcode-locale-preference", "zh-CN");
  });
  page = await context.newPage();
  page.setDefaultTimeout(30000);
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (entry) => {
    if (entry.type() === "error" && !(expectingUnknown && entry.text().includes("status of 409")))
      consoleErrors.push(entry.text().slice(0, 1200));
  });
  page.on("response", (response) => {
    if (
      expectingUnknown &&
      response.status() === 409 &&
      new URL(response.url()).pathname === "/api/teach"
    ) {
      expectedConflictResponses++;
      return;
    }
    if (response.status() >= 400)
      resourceErrors.push({ url: new URL(response.url()).pathname, status: response.status() });
  });
  page.on("requestfailed", (request) => {
    // 只记录路径和原因，内嵌字体内容与凭据不进入验收日志。
    resourceErrors.push({
      url:
        new URL(request.url()).protocol === "data:" ? "data:font" : new URL(request.url()).pathname,
      error: request.failure()?.errorText,
    });
  });
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  await check("shared_theme_persistence_and_system", async () => {
    await page.getByRole("button", { name: "切换深色主题" }).click();
    assert.equal(await page.evaluate(() => localStorage.getItem("zcode-theme")), "zai-dark");
    await page.reload();
    await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
    assert(await page.locator("html").evaluate((e) => e.classList.contains("theme-zai-dark")));
    await page.evaluate(() => localStorage.setItem("zcode-theme", "system"));
    await page.emulateMedia({ colorScheme: "light" });
    await page.reload();
    await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
    assert(await page.locator("html").evaluate((e) => e.classList.contains("theme-zai-light")));
    await page.emulateMedia({ colorScheme: "dark" });
    await page.waitForFunction(() => document.documentElement.classList.contains("theme-zai-dark"));
    await page.emulateMedia({ colorScheme: "light" });
  });
  await check("shared_intl_normalizes_incomplete_english_preference", async () => {
    await page.evaluate(() => localStorage.setItem("zcode-locale-preference", "en-US"));
    await page.reload();
    await page.getByRole("button", { name: "新建学习对话", exact: true }).waitFor();
    assert(
      (await page.evaluate(() => localStorage.getItem("zcode-locale-preference"))).startsWith("zh"),
    );
  });
  await check("shared_select_identity_keyboard", async () => {
    const profile = page.getByRole("combobox", {
      name: "当前学习者",
      exact: true,
    });
    await profile.focus();
    await page.keyboard.press("Enter");
    await page.getByRole("option", { name: "学习者 B", exact: true }).waitFor();
    await page.getByRole("option", { name: "学习者 A", exact: true }).focus();
    await page.keyboard.press("ArrowDown");
    // Radix 在下一次任务中移动焦点；确认移动完成后再按 Enter，避免评测连按误选。
    await page.waitForFunction(() => document.activeElement?.textContent?.includes("学习者 B"));
    await page.keyboard.press("Enter");
    await profile.getByText("学习者 B", { exact: true }).waitFor();
    await choose(page, "当前学习者", "学习者 A");
  });
  await check("shared_message_math_code_table", async () => {
    await page.getByRole("button", { name: "新建学习对话", exact: true }).click();
    await page.getByLabel("你的学习问题", { exact: true }).fill("你好");
    const response = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    assert.equal((await response).status(), 200);
    const message = page.locator("article.edu-message").last();
    await message.locator(".katex").first().waitFor();
    assert((await message.locator(".katex").count()) >= 2);
    await page.evaluate(() => document.fonts.ready);
    assert(await page.evaluate(() => document.fonts.check("16px KaTeX_Main")));
    await message.getByRole("table").waitFor();
    await message.getByText("print(2 + 3)", { exact: true }).waitFor();
    assert.equal(
      await message.getByText("学习笔记", { exact: true }).evaluate((e) => e.tagName),
      "STRONG",
    );
    await page.screenshot({
      path: reports + "source-reuse-desktop.png",
      fullPage: true,
    });
  });
  await check("shared_composer_keeps_natural_http_input", async () => {
    await page.getByRole("button", { name: "新建学习对话", exact: true }).click();
    const question = "请帮我核对：2+2=4。";
    await page.getByLabel("你的学习问题", { exact: true }).fill(question);
    const response = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByLabel("你的学习问题", { exact: true }).press("Control+Enter");
    const received = await response;
    assert.equal(received.status(), 200);
    const result = await readTeachResponse(received);
    assert.equal(result.session.messages.at(-1).original_input.question, question);
    assert.equal(result.response.teaching_action, "confirm");
    await page.reload();
    await page.locator("article.edu-message").getByText(question, { exact: true }).waitFor();
  });
  await check("shared_controls_mobile", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    assert.equal(
      await page
        .getByLabel("你的学习问题", { exact: true })
        .evaluate((e) => getComputedStyle(e).fontSize),
      "16px",
    );
    await page.getByRole("button", { name: "打开导航" }).click();
    await page.keyboard.press("Escape");
    assert.equal(await page.locator(".edu-sidebar").getAttribute("data-open"), "false");
    await page.screenshot({
      path: reports + "source-reuse-mobile.png",
      fullPage: true,
    });
  });
  await check("recorded_unknown_disables_retry_after_reload", async () => {
    expectingUnknown = true;
    await page.setViewportSize({ width: 1440, height: 960 });
    await page.getByRole("button", { name: "新建学习对话", exact: true }).click();
    await page.getByLabel("你的学习问题", { exact: true }).fill("你好，模拟断连");
    const response = page.waitForResponse((r) => r.url().endsWith("/api/teach"));
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const received = await response;
    if (received.headers()["content-type"]?.includes("text/event-stream")) {
      const error = (await readTeachEvents(received)).at(-1);
      assert.equal(error.kind, "error");
      assert.equal(error.status, 409);
      assert.equal(error.error, "model_unknown");
      expectedConflictResponses++;
    } else assert.equal(received.status(), 409);
    await page.getByRole("alert").getByText("模型结果待核查，记录已保留。").waitFor();
    assert.equal(await page.getByRole("button", { name: "重试当前请求", exact: true }).count(), 0);
    await page.reload();
    await page.getByText(/此请求已停止，记录已保留。模型结果无法安全重发/).waitFor();
    assert.equal(await page.getByRole("button", { name: "继续此请求", exact: true }).count(), 0);
    assert.equal(expectedConflictResponses, 1);
    expectingUnknown = false;
  });
  assert.deepEqual(errors, []);
  assert.deepEqual(consoleErrors, []);
  assert.deepEqual(resourceErrors, []);
} catch (error) {
  if (page) await page.screenshot({ path: reports + "source-reuse-failure.png", fullPage: true });
  throw error;
} finally {
  await writeFile(
    reports + "source-reuse-acceptance.json",
    JSON.stringify(
      {
        passed:
          tests.length === 7 &&
          errors.length === 0 &&
          consoleErrors.length === 0 &&
          resourceErrors.length === 0,
        tests,
        pageErrors: errors,
        consoleErrors,
        resourceErrors,
        actualHTTP: true,
        modelResponsesMocked: true,
        purpose: "ZCode source reuse presentation and input contracts",
      },
      null,
      2,
    ),
  );
  if (browser) await browser.close();
  lines.close();
  child.kill();
}
