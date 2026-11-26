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
  [fileURLToPath(new URL("./product_usability_server.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
const tests = [],
  errors = [];
let browser,
  page,
  stderr = "";
child.stderr.on("data", (v) => {
  stderr += v;
});
async function check(name, run) {
  await run();
  tests.push({ name, passed: true });
  process.stdout.write(JSON.stringify(tests.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(stderr || "fixture timeout")), 30000);
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
    headless: true,
    executablePath: [
      "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
      "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    ].find(existsSync),
  });
  page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  const history = page.getByRole("region", { name: "最近学习对话" });
  await check("history_is_compact_searchable_and_expandable", async () => {
    await history.getByTestId("history-item").first().waitFor();
    assert.equal(await history.locator('[data-testid="history-item"]').count(), 6);
    await page.getByLabel("搜索学习对话").fill("复习记录 3");
    assert.equal(await history.locator('[data-testid="history-item"]').count(), 1);
    await page.getByLabel("搜索学习对话").fill("");
    await page.getByRole("button", { name: /全部历史/ }).click();
    assert.equal(await history.locator('[data-testid="history-item"]').count(), 9);
    await page.getByRole("button", { name: "收起历史" }).click();
  });
  async function submit(text) {
    await page.getByLabel("你的学习问题", { exact: true }).fill(text);
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const response = await waiting;
    assert.equal(response.status(), 200);
    const result = await readTeachResponse(response);
    await page.waitForFunction(() => {
      const e = document.querySelector("#edu-question");
      return e && e.value === "" && !e.disabled;
    });
    return result;
  }
  await check("practice_to_chat_keeps_owned_math_question_without_duplicate_prompt", async () => {
    await page.getByRole("button", { name: "个性化练习", exact: true }).click();
    await page.getByRole("button", { name: "和导师一起做", exact: true }).click();
    // 转入会话是异步读取；确认原题和预填草稿后再模拟发送，不能读取旧会话的空草稿。
    await page.waitForFunction(
      () =>
        document.querySelector("#edu-question")?.value ===
          "返回原练习，请引导我思考这道题，先不要给最终答案。" &&
        !document.querySelector("#edu-question")?.disabled,
    );
    const draft = await page.getByLabel("你的学习问题", { exact: true }).inputValue();
    assert(!draft.includes("3x+m"));
    const reference = page.getByRole("region", { name: "正在讨论的题目" });
    await reference.locator(".katex").first().waitFor();
    assert.match(await reference.textContent(), /和谐方程/);
    const guided = await submit(draft);
    assert.match(guided.response.text, /4x/);
    assert(!guided.response.text.includes("请提供具体问题"));
    await submit("我先看 $4x-2=x+10$，请给我一点提示。");
    await page.locator(".edu-user .katex").first().waitFor();
  });
  await check("natural_steps_finish_and_return_to_practice", async () => {
    assert.equal((await submit("x=5")).response.teaching_action, "ask");
    assert.equal((await submit("x=4")).response.teaching_action, "confirm");
    assert.equal((await submit("另一个方程的解 x=-4")).response.teaching_action, "confirm");
    assert.equal((await submit("我的最终答案是 m=22")).response.teaching_action, "confirm");
    await page.getByRole("button", { name: "返回练习", exact: true }).click();
    await page.getByText("答案正确", { exact: true }).waitFor();
    await page.getByRole("button", { name: "继续下一题", exact: true }).waitFor();
    assert.equal(await page.getByTestId("recommendation-card").count(), 3);
  });
  await check("path_leads_with_action_and_hides_adjustments", async () => {
    await page.getByRole("button", { name: "学习路径", exact: true }).click();
    await page.getByTestId("adaptive-plan").waitFor();
    assert.equal(await page.getByLabel("每日学习分钟").isVisible(), false);
    await page.getByText("调整目标与学习时间", { exact: true }).click();
    assert.equal(await page.getByLabel("每日学习分钟").isVisible(), true);
    await page.getByText("调整目标与学习时间", { exact: true }).click();
  });
  await check("one_map_contains_distinct_routes_and_node_selection_does_not_write", async () => {
    const before = await (await page.request.get(setup.base + "/api/learning")).json();
    const map = page.getByRole("region", { name: "学习路线地图", exact: true });
    assert.equal(await map.count(), 1);
    assert.equal(await page.locator(".edu-page .edu-card").count(), 0);
    assert.equal(await page.getByRole("complementary", { name: "学习站点详情" }).count(), 0);
    assert.equal(await map.getByTestId("route-choice").count(), before.path.routes.length);
    assert(before.path.routes.length >= 2);
    assert.equal(
      await map.getByTestId("route-station").count(),
      before.path.routes.reduce((n, r) => n + r.steps.length, 0),
    );
    const route = before.path.routes[0],
      step = route.steps[0];
    await map
      .getByRole("button", { name: `查看${step.title}（${route.title}）学习详情`, exact: true })
      .press("Enter");
    await page
      .getByRole("region", { name: "地图节点说明", exact: true })
      .getByRole("heading", { name: step.title, exact: true })
      .waitFor();
    assert.deepEqual(
      (await (await page.request.get(setup.base + "/api/learning")).json()).goal,
      before.goal,
    );
    await page.getByRole("button", { name: "关闭节点说明", exact: true }).click();
  });
  await check("branch_selection_changes_practice_and_survives_refresh", async () => {
    const before = await (await page.request.get(setup.base + "/api/learning")).json();
    const alternative = before.path.routes.find((r) => r.id !== before.path.selected_route);
    await page
      .getByRole("button", { name: `选择${alternative.title}路线`, exact: true })
      .press("Enter");
    await page.getByText("已选择路线，个性化练习已重新匹配。", { exact: true }).waitFor();
    const after = await (await page.request.get(setup.base + "/api/learning")).json();
    assert.equal(after.path.selected_route, alternative.id);
    assert.notDeepEqual(after.recommendations, before.recommendations);
    assert.equal(after.summary.attempts, before.summary.attempts);
    await page.getByRole("button", { name: "个性化练习", exact: true }).click();
    await page.getByTestId("practice-selected-route").waitFor();
    assert.match(
      await page.getByTestId("practice-selected-route").textContent(),
      new RegExp(alternative.title),
    );
    assert.equal(await page.getByTestId("recommendation-card").count(), 3);
    await page.reload();
    await page.getByRole("button", { name: "学习路径", exact: true }).click();
    await page.getByRole("button", { name: `选择${alternative.title}路线`, exact: true }).waitFor();
    assert.equal(
      await page
        .getByRole("button", { name: `选择${alternative.title}路线`, exact: true })
        .getAttribute("aria-pressed"),
      "true",
    );
    assert.equal(
      await page
        .locator('[data-testid="route-station"][aria-current="step"]')
        .getAttribute("data-topic"),
      after.path.focus,
    );
    const dark = page.getByRole("button", { name: "切换深色主题", exact: true });
    if (await dark.count()) await dark.click();
    await page.locator(".edu-page").evaluate((e) => e.scrollTo(0, 0));
    await page.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/learning-branches-desktop-dark.png", import.meta.url),
      ),
      fullPage: true,
    });
    const light = page.getByRole("button", { name: "切换浅色主题", exact: true });
    if (await light.count()) await light.click();
    await page.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/learning-branches-desktop-light.png", import.meta.url),
      ),
      fullPage: true,
    });
  });
  await check("dashboard_summary_and_focus_use_same_learning_snapshot", async () => {
    const data = await (await page.request.get(setup.base + "/api/learning")).json();
    await page.getByRole("button", { name: "学情看板", exact: true }).click();
    const summary = page.getByRole("region", { name: "学情摘要" });
    await summary.waitFor();
    assert.match(await summary.textContent(), /已完成 1 次新练习/);
    const reviewText = await summary.getByTestId("review-overview").textContent();
    if (data.review_overview.recent_due_count > 0)
      assert.match(
        reviewText,
        new RegExp(`新练习待复测 ${data.review_overview.recent_due_count} 个知识点`),
      );
    else assert.doesNotMatch(reviewText, /新练习待复测 0/);
    if (data.review_overview.historical_due_count > 0)
      assert.match(
        reviewText,
        new RegExp(`历史复习建议 ${data.review_overview.historical_due_count} 个`),
      );
    assert.equal(
      data.review_overview.due_count,
      data.topics.filter((t) => t.review.status === "due").length,
    );
    const expected = data.topics.find((t) => t.id === data.path.focus).title;
    assert.equal(
      await page
        .getByRole("complementary", { name: "知识点学情详情" })
        .getByRole("heading")
        .textContent(),
      expected,
    );
    await page.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/product-dashboard-desktop.png", import.meta.url),
      ),
      fullPage: true,
    });
  });
  await check("four_views_fit_mobile_and_both_themes", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    for (const theme of ["light", "dark"]) {
      const switcher = page.getByRole("button", {
        name: theme === "dark" ? "切换深色主题" : "切换浅色主题",
        exact: true,
      });
      if (await switcher.count()) await switcher.click();
      for (const label of ["个性化辅导", "学习路径", "学情看板", "个性化练习"]) {
        await page.getByRole("button", { name: "打开导航", exact: true }).click();
        await page
          .getByRole("navigation", { name: "主导航" })
          .getByRole("button", { name: label, exact: true })
          .click();
        if (label === "个性化辅导") await page.locator(".edu-composer").waitFor();
        else {
          // edu-page 也用于加载占位；等待业务内容，避免把空白加载页当成移动端验收证据。
          await page.getByRole("heading", { name: label, exact: true }).waitFor();
          if (label === "学习路径") {
            const map = page.getByRole("region", { name: "学习路线地图", exact: true });
            await map.getByTestId("route-station").first().waitFor();
            const current = await (await page.request.get(setup.base + "/api/learning")).json();
            assert.equal(
              await map.getByTestId("route-station").count(),
              current.path.routes.reduce((n, r) => n + r.steps.length, 0),
            );
            assert(
              await page.getByRole("button", { name: "开始今日练习", exact: true }).isVisible(),
            );
          }
          if (label === "学情看板")
            await page.getByRole("region", { name: "学情摘要", exact: true }).waitFor();
          await page.locator(".edu-page").evaluate((element) => element.scrollTo(0, 0));
        }
        assert(
          await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),
          label + " overflow",
        );
        const shot =
          label === "学情看板"
            ? "dashboard"
            : label === "个性化辅导"
              ? "tutor"
              : label === "学习路径"
                ? "path"
                : "practice";
        await page.screenshot({
          path: fileURLToPath(
            new URL(`../.local/reports/product-${shot}-mobile-${theme}.png`, import.meta.url),
          ),
          fullPage: true,
        });
      }
    }
  });
  assert.deepEqual(errors, []);
  await writeFile(
    fileURLToPath(new URL("../.local/reports/product-usability-browser.json", import.meta.url)),
    JSON.stringify({ passed: tests.length, tests, errors, remote_inference: false }, null, 2),
  );
} catch (error) {
  if (page) {
    await page.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/product-usability-failure.png", import.meta.url),
      ),
      fullPage: true,
    });
    await writeFile(
      fileURLToPath(new URL("../../tmp/product-usability-failure.local.json", import.meta.url)),
      JSON.stringify(
        { error: String(error), errors, state: await page.locator("body").innerText() },
        null,
        2,
      ),
    );
  }
  throw error;
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
