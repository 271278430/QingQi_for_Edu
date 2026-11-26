// Current four-feature product: real browser -> teaching owner -> native tools.
import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const child = spawn(
  process.env.QINGQI_PYTHON || "python",
  [fileURLToPath(new URL("./four_feature_server.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
const tests = [],
  errors = [];
let browser,
  stderr = "";
child.stderr.on("data", (value) => {
  stderr += value;
});
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
    const timer = setTimeout(
      () => reject(new Error(`fixture timeout: ${stderr}`)),
      30000,
    );
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
  const executablePath = [
    "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
  ].find(existsSync);
  browser = await chromium.launch({ executablePath, headless: true });
  const page = await browser.newPage({
    viewport: { width: 1440, height: 960 },
  });
  page.setDefaultTimeout(30000);
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  async function submit(question) {
    await page.getByLabel("你的学习问题", { exact: true }).fill(question);
    const response = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "发送学习问题", exact: true })
      .click();
    const received = await response;
    assert.equal(received.status(), 200);
    const value = await received.json();
    await page.waitForFunction(() => {
      const input = document.querySelector("#edu-question");
      return input && input.value === "" && !input.disabled;
    });
    return value;
  }
  await check("socratic_heuristic_and_natural_step_continuation", async () => {
    assert.equal(await page.locator(".edu-composer textarea").count(), 1);
    assert.equal(
      await page.getByRole("combobox", { name: "辅导方式" }).count(),
      0,
    );
    assert.equal(
      await page.getByRole("button", { name: "添加题目与步骤" }).count(),
      0,
    );
    const bare = await submit("2+3*4");
    assert.equal(bare.session.messages.at(-1).input.expression, "2+3*4");
    const first = bare;
    assert.equal(first.response.teaching_action, "ask");
    assert(!first.response.text.includes("14"));
    const next = await submit("这道题请给我启发式提示");
    assert.equal(next.response.route.teaching.mode, "heuristic");
    assert.notEqual(first.response.text, next.response.text);
    assert.equal((await submit("20")).response.teaching_action, "ask");
    assert.equal((await submit("3*4=12")).response.teaching_action, "confirm");
    const finished = await submit("2+12=14");
    assert.equal(finished.response.teaching_action, "confirm");
    assert.equal(finished.session.messages.at(-1).input.expression, "2+3*4");
    assert.equal(
      await page
        .locator("article.edu-message")
        .last()
        .locator(".edu-user")
        .textContent(),
      "2+12=14",
    );
    await page.reload();
    await page
      .locator("article.edu-message")
      .last()
      .getByText("你提供的数值等式均通过核验", { exact: false })
      .waitFor();
  });
  await check(
    "auto_adapts_to_repeated_struggle_without_leaking_on_request",
    async () => {
      await page
        .getByRole("button", { name: "新建学习对话", exact: true })
        .click();
      assert.equal(
        (await submit("请给我提示，计算 2+3*4")).response.teaching_action,
        "ask",
      );
      const more = await submit(
        "这道题我还是不会，请分步讲解，但不要给最终答案",
      );
      assert.equal(more.response.teaching_action, "explain");
      assert(!more.response.text.includes("14"));
    },
  );
  await check("answer_check_and_student_isolation", async () => {
    const direct = await submit("直接核对 2+3*4 的答案");
    assert.equal(direct.response.teaching_action, "give_answer");
    assert(direct.response.text.includes("14"));
    await choose(page, "当前学习者", "学习者 B");
    assert.equal(await page.locator("article.edu-message").count(), 0);
    await choose(page, "当前学习者", "学习者 A");
  });
  await check("simple_conversation_is_mobile_operable", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    assert.equal(await page.locator(".edu-composer textarea").count(), 1);
    assert(
      await page.getByRole("button", { name: "发送学习问题" }).isVisible(),
    );
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
  });
  assert.deepEqual(errors, []);
  await writeFile(
    fileURLToPath(
      new URL("../.local/reports/four-feature-tutoring-browser.json", import.meta.url),
    ),
    JSON.stringify(
      { passed: tests.length, tests, errors, remote_inference: false },
      null,
      2,
    ),
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
