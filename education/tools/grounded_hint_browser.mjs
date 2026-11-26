import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
import { readTeachResponse } from "./read_teach_response.mjs";

const child = spawn(
  process.env.QINGQI_PYTHON || "python",
  [fileURLToPath(new URL("grounded_hint_browser_server.py", import.meta.url))],
  { windowsHide: true, stdio: ["pipe", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let stderr = "",
  browser;
const checks = [],
  errors = [];
child.stderr.on("data", (chunk) => {
  stderr += chunk;
});
async function check(name, run) {
  await run();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(
      () => reject(new Error(stderr || "fixture timeout")),
      30000,
    );
    lines.once("line", (line) => {
      clearTimeout(timer);
      resolve(JSON.parse(line));
    });
    child.once("exit", (code) => {
      clearTimeout(timer);
      reject(new Error(`fixture exited ${code}: ${stderr}`));
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
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  const boot = await (
    await page.request.get(setup.base + "/api/bootstrap")
  ).json();
  const started = await page.request.post(setup.base + "/api/practice/start", {
    data: { item_id: setup.item, request_id: "browser-start" },
    headers: { Origin: setup.base, "X-Qingqi-CSRF": boot.csrf },
  });
  assert.equal(started.status(), 201);
  await page.reload();
  await page
    .getByRole("navigation", { name: "主导航" })
    .getByRole("button", { name: "个性化练习", exact: true })
    .click();
  const hint = page.getByRole("status", { name: "练习提示" });
  await page.getByRole("heading", { name: "当前练习", exact: true }).waitFor();
  await check(
    "practice_has_one_hint_button_and_no_socratic_button",
    async () => {
      assert.equal(
        await page
          .getByRole("button", { name: "苏格拉底追问", exact: true })
          .count(),
        0,
      );
      assert.equal(
        await page
          .getByRole("button", { name: "给我一点提示", exact: true })
          .count(),
        1,
      );
    },
  );
  let first, second;
  await check("hint_is_grounded_in_displayed_equation", async () => {
    await page
      .getByRole("button", { name: "给我一点提示", exact: true })
      .click();
    await hint.waitFor();
    first = await hint.textContent();
    assert.match(first, /m.*5|n.*8/s);
    assert.doesNotMatch(first, /抓住|掌握|中间结果代回/);
    assert.doesNotMatch(first, /[?？]|告诉我|你能|请给出|看这张/);
  });
  await check("continued_hint_deepens_help_and_refresh_replays", async () => {
    await page
      .getByRole("button", { name: "给我一点提示", exact: true })
      .click();
    await page.waitForFunction(
      (old) =>
        document.querySelector('[aria-label="练习提示"]')?.textContent !== old,
      first,
    );
    second = await hint.textContent();
    assert.match(second, /0.*1/s);
    const beforeReload = await (
      await page.request.get(setup.base + "/api/learning")
    ).json();
    await page.reload();
    await page
      .getByRole("navigation", { name: "主导航" })
      .getByRole("button", { name: "个性化练习", exact: true })
      .click();
    await hint.locator(".katex").first().waitFor();
    const afterReload = await (
      await page.request.get(setup.base + "/api/learning")
    ).json();
    assert.equal(afterReload.active.guidance, beforeReload.active.guidance);
    assert.equal(await hint.locator(".katex-error").count(), 0);
    await page.screenshot({
      path: fileURLToPath(
        new URL(
          "../.local/reports/grounded-hint-practice.png",
          import.meta.url,
        ),
      ),
    });
  });
  await check(
    "mentor_continues_same_problem_without_fake_student_conclusion",
    async () => {
      await page
        .getByRole("button", { name: "和导师一起做", exact: true })
        .click();
      await page.getByRole("region", { name: "正在讨论的题目" }).waitFor();
      await page.locator("#edu-question").fill("继续给我提示");
      const responseWait = page.waitForResponse(
        (r) =>
          r.url().endsWith("/api/teach") && r.request().method() === "POST",
      );
      await page
        .getByRole("button", { name: "发送学习问题", exact: true })
        .click();
      const response = await responseWait;
      assert.equal(response.status(), 200);
      const result = await readTeachResponse(response);
      assert.match(result.response.text, /m-5/);
      assert.doesNotMatch(result.response.text, /你已经|抓住|掌握/);
      await page.locator(".is-assistant").last().waitFor();
      await page.screenshot({
        path: fileURLToPath(
          new URL(
            "../.local/reports/grounded-hint-dialogue.png",
            import.meta.url,
          ),
        ),
      });
    },
  );
  await check("known_failed_hint_unlocks_a_new_request", async () => {
    await page
      .getByRole("navigation", { name: "主导航" })
      .getByRole("button", { name: "个性化练习", exact: true })
      .click();
    await page.route(
      "**/api/practice/hint",
      (route) =>
        route.fulfill({
          status: 502,
          json: {
            error: "model_protocol",
            message: "该提示已停止，请重新请求。",
          },
        }),
      { times: 1 },
    );
    await page
      .getByRole("button", { name: "给我一点提示", exact: true })
      .click();
    await page
      .getByRole("alert")
      .getByText("该提示已停止，请重新请求。", { exact: true })
      .waitFor();
    assert.equal(
      await page
        .getByRole("button", { name: "重试此操作", exact: true })
        .count(),
      0,
    );
    assert.equal(
      await page
        .getByRole("button", { name: "给我一点提示", exact: true })
        .isEnabled(),
      true,
    );
    const retry = page.waitForResponse(
      (r) =>
        r.url().endsWith("/api/practice/hint") &&
        r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "给我一点提示", exact: true })
      .click();
    assert.equal((await retry).status(), 200);
    await page.waitForFunction(() =>
      Array.from(document.querySelectorAll("button")).some(
        (button) =>
          button.textContent?.trim() === "给我一点提示" && !button.disabled,
      ),
    );
  });
  await check(
    "mobile_hint_and_three_recommendations_remain_usable",
    async () => {
      await page.setViewportSize({ width: 390, height: 844 });
      await page.getByRole("button", { name: "打开导航", exact: true }).click();
      await page
        .getByRole("navigation", { name: "主导航" })
        .getByRole("button", { name: "个性化练习", exact: true })
        .click();
      await page
        .getByRole("button", { name: "给我一点提示", exact: true })
        .waitFor();
      assert.equal(await page.getByTestId("recommendation-card").count(), 3);
      assert(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      );
      const data = await (
        await page.request.get(setup.base + "/api/learning")
      ).json();
      assert.equal(data.summary.attempts, 0);
      assert.deepEqual(errors, []);
    },
  );
  await writeFile(
    new URL(
      "../.local/reports/grounded-hint-browser.local.json",
      import.meta.url,
    ),
    JSON.stringify({ passed: checks.length, checks, isolated: true }, null, 2),
  );
} finally {
  await browser?.close();
  child.stdin.end();
}
