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
  [fileURLToPath(new URL("current_task_browser_server.py", import.meta.url))],
  { windowsHide: true, stdio: ["pipe", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
const checks = [],
  errors = [];
let stderr = "",
  browser;
child.stderr.on("data", (chunk) => {
  stderr += chunk;
});
async function check(name, fn) {
  await fn();
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
      reject(Error(`fixture exited ${code}: ${stderr}`));
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
    viewport: { width: 1366, height: 1000 },
  });
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(setup.base);
  // 等待页面完成首次鉴权，再使用同一cookie；并发bootstrap会让夹具拿到旧CSRF。
  await page.getByRole("textbox", { name: "你的学习问题" }).waitFor();
  const boot = await (
    await page.request.get(setup.base + "/api/bootstrap")
  ).json();
  const headers = { Origin: setup.base, "X-Qingqi-CSRF": boot.csrf };
  const assignment = await (
    await page.request.post(setup.base + "/api/practice/start", {
      data: { item_id: setup.item, request_id: "browser-task-source" },
      headers,
    })
  ).json();
  const story = await page.request.post(setup.base + "/api/teach", {
    data: {
      session: assignment.session,
      request: {
        question: "请用情景故事解释这道题，不给最终答案。",
        request_id: "browser-task-story",
      },
    },
    headers,
  });
  assert.equal(story.status(), 200, await story.text());
  await page.reload();
  await page.getByRole("textbox", { name: "你的学习问题" }).waitFor();
  const sourceDetail = await (
    await page.request.get(setup.base + "/api/session?id=" + assignment.session)
  ).json();
  await page
    .getByRole("button", { name: sourceDetail.session.title, exact: true })
    .click();
  async function send(question) {
    await page.getByRole("textbox", { name: "你的学习问题" }).fill(question);
    const response = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题" }).click();
    const value = await readTeachResponse(await response);
    await page
      .getByRole("button", { name: "发送学习问题" })
      .waitFor({ state: "visible" });
    assert.ok(value.response, JSON.stringify(value));
    return value.response;
  }
  let result, items;
  await check(
    "reported_request_shows_one_question_instead_of_old_story",
    async () => {
      result = await send("给出推荐一个类似的题目");
      assert.equal(
        result.student_tasks[0].items.length,
        1,
        JSON.stringify(result),
      );
      const card = page.getByRole("region", { name: "推荐练习" }).last();
      await card.waitFor();
      assert.equal(
        await card.getByRole("button", { name: "开始练习" }).count(),
        1,
      );
      assert.doesNotMatch(await card.textContent(), /情景教学|答案是|分别列出/);
      assert.equal(result.student_tasks[0].items.length, 1);
      assert.equal(result.visuals?.length ?? 0, 0);
    },
  );
  await check(
    "default_recommendation_is_three_distinct_cards_and_refresh_recovers",
    async () => {
      result = await send("不要讲解，再推荐类似的题目。");
      items = result.student_tasks[0].items;
      assert.equal(items.length, 3);
      const card = page.getByRole("region", { name: "推荐练习" }).last();
      assert.equal(
        await card.getByRole("button", { name: "开始练习" }).count(),
        3,
      );
      await page.reload();
      await page.getByRole("region", { name: "推荐练习" }).last().waitFor();
      assert.equal(
        await page
          .getByRole("region", { name: "推荐练习" })
          .last()
          .getByRole("button", { name: "开始练习" })
          .count(),
        3,
      );
    },
  );
  await check("mobile_cards_have_no_overflow_or_dead_actions", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    const card = page.getByRole("region", { name: "推荐练习" }).last();
    const buttons = card.getByRole("button", { name: "开始练习" });
    await buttons.first().scrollIntoViewIfNeeded();
    assert.ok(await buttons.first().isEnabled());
    assert.ok(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth + 2,
      ),
    );
    await page.screenshot({
      path: "education/.local/reports/current-task-mobile.local.png",
      fullPage: true,
    });
  });
  await check(
    "card_selection_opens_real_practice_without_counting_an_answer",
    async () => {
      await page
        .getByRole("region", { name: "推荐练习" })
        .last()
        .getByRole("button", { name: "开始练习" })
        .first()
        .click();
      await page
        .getByRole("heading", { name: "当前练习", exact: true })
        .waitFor();
      const learning = await (
        await page.request.get(setup.base + "/api/learning")
      ).json();
      assert.equal(learning.active.item.id, items[0].id);
      assert.equal(learning.active.feedback, null);
    },
  );
  await check("dashboard_result_opens_the_actual_learning_graph", async () => {
    await page.setViewportSize({ width: 1366, height: 1000 });
    await page
      .getByRole("navigation", { name: "主导航" })
      .getByRole("button", { name: "个性化辅导", exact: true })
      .click();
    await send("帮我看看学情，暂时不讲题。");
    await page
      .getByRole("button", { name: "查看学情图谱", exact: true })
      .last()
      .click();
    await page
      .getByRole("heading", { name: "学情看板", exact: true })
      .waitFor();
  });
  await check(
    "old_wrong_reply_is_folded_and_explicit_retry_has_a_new_identifier",
    async () => {
      await page
        .getByRole("navigation", { name: "主导航" })
        .getByRole("button", { name: "个性化辅导", exact: true })
        .click();
      await page
        .getByRole("button", { name: "旧版推荐记录", exact: true })
        .click();
      const retry = page.getByRole("button", {
        name: "重新执行这条请求",
        exact: true,
      });
      await retry.waitFor();
      assert.equal(
        await page
          .locator("details")
          .filter({ hasText: "查看原回复" })
          .getAttribute("open"),
        null,
      );
      const before = await (
        await page.request.get(
          setup.base + "/api/session?id=" + setup.legacy_session,
        )
      ).json();
      const response = page.waitForResponse((r) =>
        r.url().endsWith("/api/teach"),
      );
      await retry.click();
      await readTeachResponse(await response);
      const after = await (
        await page.request.get(
          setup.base + "/api/session?id=" + setup.legacy_session,
        )
      ).json();
      assert.equal(after.messages.length, before.messages.length + 1);
      assert.equal(after.messages[0].original_input.request_id, "legacy-query");
      assert.notEqual(
        after.messages.at(-1).original_input.request_id,
        "legacy-query",
      );
      assert.equal(
        after.messages.at(-1).response.student_tasks[0].status,
        "needs_source",
      );
    },
  );
  await check("browser_has_no_uncaught_render_errors", async () => {
    assert.deepEqual(errors, []);
  });
} finally {
  await browser?.close();
  child.stdin.end();
}
await writeFile(
  "education/.local/reports/current-task-browser.local.json",
  JSON.stringify({ checks, passed: checks.length }, null, 2),
);
