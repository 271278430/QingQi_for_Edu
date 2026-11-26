import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
const child = spawn(
  process.env.QINGQI_PYTHON,
  [fileURLToPath(new URL("./product_usability_server.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let stderr = "",
  browser;
child.stderr.on("data", (v) => (stderr += v));
const checks = [],
  inventory = {};
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
  });
  page.setDefaultTimeout(30000);
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  const learning = async () => (await page.request.get(setup.base + "/api/learning")).json();
  const collect = async (name) => {
    inventory[name] = await page
      .locator('button,input,summary,[role="combobox"]')
      .evaluateAll((nodes) =>
        nodes
          .filter((n) => n.getClientRects().length)
          .map((n) => ({
            label:
              n.getAttribute("aria-label") ||
              n.textContent?.trim() ||
              n.getAttribute("placeholder"),
            type: n.getAttribute("type") || n.tagName.toLowerCase(),
            disabled: n.disabled || false,
          })),
      );
  };
  await check("initial_learning_fetch_failure_can_retry_without_page_reload", async () => {
    await page.route("**/api/learning", (r) => r.abort("failed"), {
      times: 1,
    });
    await page.getByRole("button", { name: "学情看板", exact: true }).click();
    await page.getByRole("alert").waitFor();
    await page.getByRole("button", { name: "重新读取学习记录", exact: true }).click();
    await page.getByRole("region", { name: "学情摘要", exact: true }).waitFor();
  });
  await check("all_graph_sources_groups_search_and_empty_reset", async () => {
    for (const mode of ["历史画像", "近期练习", "综合学情"]) {
      await page.getByRole("combobox", { name: "学情来源", exact: true }).click();
      await page.getByRole("option", { name: mode, exact: true }).click();
    }
    const groups = page.getByRole("group", { name: "知识分区", exact: true }).getByRole("button");
    const labels = (await groups.allTextContents()).map((v) => v.trim());
    for (const label of labels) {
      await page
        .getByRole("group", { name: "知识分区", exact: true })
        .getByRole("button", { name: label, exact: true })
        .click();
      assert((await page.locator(".edu-map-node").count()) > 0);
    }
    await page.getByRole("button", { name: "全部知识", exact: true }).click();
    await page.getByRole("button", { name: "只看需要关注", exact: true }).click();
    assert.equal(await page.locator('.edu-map-node[data-status="ready"]').count(), 0);
    await page.getByRole("button", { name: "只看需要关注", exact: true }).click();
    await page.getByLabel("搜索知识点").fill("不存在的知识点_xyz");
    await page.getByText("没有匹配的知识点。", { exact: true }).waitFor();
    await page.getByRole("button", { name: "查看全部知识", exact: true }).click();
    assert.equal(await page.getByLabel("搜索知识点").inputValue(), "");
  });
  await check("graph_zoom_limits_reset_and_evidence_disclosure", async () => {
    while (await page.getByRole("button", { name: "放大图谱", exact: true }).isEnabled())
      await page.getByRole("button", { name: "放大图谱", exact: true }).click();
    assert((await page.getByTestId("map-zoom").innerText()).includes("180"));
    while (await page.getByRole("button", { name: "缩小图谱", exact: true }).isEnabled())
      await page.getByRole("button", { name: "缩小图谱", exact: true }).click();
    assert((await page.getByTestId("map-zoom").innerText()).includes("60"));
    await page.getByRole("button", { name: "复位图谱", exact: true }).click();
    assert((await page.getByTestId("map-zoom").innerText()).includes("100"));
    await page.getByText("数据依据", { exact: true }).click();
    await page.getByTestId("initial-source").waitFor();
    await page.getByText("数据依据", { exact: true }).click();
    await collect("dashboard");
  });
  await check("all_route_choices_nodes_and_goal_input_validation", async () => {
    await page.getByRole("button", { name: "学习路径", exact: true }).click();
    await page.getByRole("region", { name: "学习路线地图", exact: true }).waitFor();
    const routeIds = await page
      .getByTestId("route-choice")
      .evaluateAll((nodes) => nodes.map((n) => n.getAttribute("data-route")));
    for (const route of routeIds) {
      const choice = page.locator(`[data-testid="route-choice"][data-route="${route}"]`);
      if (await choice.isEnabled()) {
        const current = await learning();
        if (current.path.selected_route !== route) {
          const response = page.waitForResponse(
            (r) => r.url().endsWith("/api/learning/route") && r.request().method() === "POST",
          );
          await choice.click();
          assert.equal((await response).status(), 200);
        }
        await page.waitForFunction(
          (route) =>
            document
              .querySelector(`[data-testid="route-choice"][data-route="${route}"]`)
              ?.getAttribute("aria-pressed") === "true",
          route,
        );
      }
    }
    const nodes = page.getByTestId("route-station");
    for (let i = 0; i < (await nodes.count()); i++) {
      await nodes.nth(i).click();
      await page.getByRole("region", { name: "地图节点说明", exact: true }).waitFor();
      await page.getByRole("button", { name: "关闭节点说明", exact: true }).click();
    }
    await page.getByText("调整目标与学习时间", { exact: true }).click();
    await page.getByRole("button", { name: "收起设置", exact: true }).click();
    assert.equal(await page.getByLabel("每日学习分钟").isVisible(), false);
    await page.getByText("调整目标与学习时间", { exact: true }).click();
    await page.getByLabel("每日学习分钟").press("Escape");
    assert.equal(await page.getByLabel("每日学习分钟").isVisible(), false);
    await page.getByText("调整目标与学习时间", { exact: true }).click();
    const minutes = page.getByLabel("每日学习分钟");
    await minutes.fill("9");
    assert.equal(await minutes.evaluate((n) => n.checkValidity()), false);
    await minutes.fill("46");
    assert.equal(await minutes.evaluate((n) => n.checkValidity()), false);
    await minutes.fill("20");
    const save = page.waitForResponse(
      (r) => r.url().endsWith("/api/learning/goal") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "保存学习目标", exact: true }).click();
    assert.equal((await save).status(), 200);
    await page.getByText("已保存学习目标。", { exact: true }).waitFor();
    assert.equal(await page.getByLabel("每日学习分钟").isVisible(), false);
    await collect("path");
  });
  await check("late_start_response_does_not_override_newer_navigation", async () => {
    let release, entered;
    const gate = new Promise((r) => (release = r));
    const started = new Promise((r) => (entered = r));
    await page.route(
      "**/api/practice/start",
      async (r) => {
        entered();
        await gate;
        await r.continue();
      },
      { times: 1 },
    );
    await page.getByRole("button", { name: "开始今日练习", exact: true }).click();
    await started;
    await page.getByRole("button", { name: "学情看板", exact: true }).click();
    release();
    await page.getByRole("region", { name: "学情摘要", exact: true }).waitFor();
    await page.waitForFunction(
      () => !document.querySelector('[aria-label="知识点学情详情"] button')?.disabled,
    );
    assert.equal(await page.getByRole("heading", { name: "当前练习", exact: true }).count(), 0);
    assert(await page.getByRole("heading", { name: "学情看板", exact: true }).isVisible());
    await page.unroute("**/api/practice/start");
  });
  await check("accepted_practice_post_followed_by_failed_refresh_replays_once", async () => {
    await page.getByRole("button", { name: "个性化练习", exact: true }).click();
    await page.getByRole("heading", { name: "当前练习", exact: true }).waitFor();
    const before = await learning();
    await page.route("**/api/learning", (r) => r.abort("failed"), {
      times: 1,
    });
    await page.getByRole("button", { name: "换一组", exact: true }).click();
    await page.getByRole("button", { name: "重试此操作", exact: true }).waitFor();
    const acceptedSnapshot = await learning();
    await page.getByRole("button", { name: "重试此操作", exact: true }).click();
    await page.getByText("已更新本组三题。", { exact: true }).waitFor();
    const after = await learning();
    assert.equal(before.summary.attempts, after.summary.attempts);
    assert.equal(after.recommendation_info.batch_id, acceptedSnapshot.recommendation_info.batch_id);
    assert.deepEqual(after.recommendations, acceptedSnapshot.recommendations);
    assert.equal(await page.getByTestId("recommendation-card").count(), 3);
    await collect("practice");
  });
  await check("chat_keyboard_theme_and_mobile_navigation", async () => {
    await page.getByRole("button", { name: "新建学习对话", exact: true }).click();
    await page.waitForFunction(() => !document.querySelector("#edu-question")?.disabled);
    const box = page.getByLabel("你的学习问题", { exact: true });
    await box.fill("你好");
    await box.press("Shift+Enter");
    assert((await box.inputValue()).includes("\n"));
    await box.fill("你好");
    const answer = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await box.press("Control+Enter");
    assert.equal((await answer).status(), 200);
    await page.waitForFunction(() => document.querySelector("#edu-question")?.value === "");
    assert.equal(await page.getByRole("button", { name: "切换界面语言", exact: true }).count(), 0);
    const switcher = page.getByRole("button", { name: /切换.*色主题/ });
    await switcher.click();
    await collect("chat");
    await page.setViewportSize({ width: 390, height: 844 });
    await page.getByRole("button", { name: "打开导航", exact: true }).click();
    await page.getByRole("button", { name: "关闭导航", exact: true }).click();
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    assert.deepEqual(errors, []);
  });
} finally {
  await browser?.close();
  child.kill();
  await writeFile(
    new URL("../.local/reports/interaction-inventory-browser.json", import.meta.url),
    JSON.stringify({ passed: checks.length, checks, inventory }, null, 2),
  );
}
