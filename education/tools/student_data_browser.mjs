import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const child = spawn(
  process.env.QINGQI_PYTHON || "python",
  [fileURLToPath(new URL("./student_data_server.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
const tests = [],
  errors = [];
let browser,
  stderr = "";
child.stderr.on("data", (data) => {
  stderr += data;
});
const check = async (name, action) => {
  await action();
  tests.push({ name, passed: true });
  process.stdout.write(JSON.stringify(tests.at(-1)) + "\n");
};
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`fixture timeout: ${stderr}`)), 30000);
    lines.once("line", (line) => {
      clearTimeout(timer);
      resolve(JSON.parse(line));
    });
    child.once("error", reject);
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
  await page.getByRole("navigation", { name: "主导航" }).waitFor();
  await check("four_student_features", async () => {
    assert.deepEqual(
      await page.getByRole("navigation", { name: "主导航" }).getByRole("button").allTextContents(),
      ["个性化辅导", "学习路径", "学情看板", "个性化练习"],
    );
    assert.equal(await page.getByText("教师演示", { exact: true }).count(), 0);
    assert.equal(await page.getByRole("combobox", { name: "当前学习者" }).count(), 0);
  });
  await page.getByRole("button", { name: "学情看板", exact: true }).click();
  await check("summary_precedes_graph_and_replaces_metadata_cards", async () => {
    const summary = page.getByRole("region", {
      name: "学情摘要",
      exact: true,
    });
    await summary.waitFor();
    assert.match(await summary.textContent(), /相对熟悉|优先巩固/);
    assert.match(await summary.textContent(), /历史画像/);
    assert.equal(await page.getByRole("heading", { name: "初始化学情", exact: true }).count(), 0);
    assert.equal(await page.getByRole("heading", { name: "本产品新练习", exact: true }).count(), 0);
    assert(
      (await summary.boundingBox()).y <
        (await page.getByRole("region", { name: "数学学情图谱" }).boundingBox()).y,
    );
    const original = await summary.textContent();
    await page.getByLabel("搜索知识点").fill("绝对值");
    assert.equal(await summary.textContent(), original);
    await page.getByLabel("搜索知识点").fill("");
    await page.getByText("数据依据", { exact: true }).click();
    assert.equal(await page.getByTestId("initial-attempts").textContent(), "89");
    assert.equal(await page.getByTestId("practice-attempts").textContent(), "0");
    assert.match(await page.getByTestId("initial-source").textContent(), /未关联/);
    await page.getByText("数据依据", { exact: true }).click();
    assert.equal(await page.getByTestId("initial-source").isVisible(), false);
    await summary.scrollIntoViewIfNeeded();
  });
  await check("learning_graph_visible_at_entry_with_initial_evidence", async () => {
    const map = page.getByRole("region", { name: "数学学情图谱" });
    await map.waitFor();
    assert((await map.boundingBox()).y < 450);
    assert((await map.getByRole("button", { name: /查看知识点/ }).count()) > 0);
    assert.equal(await page.getByTestId("profile-topic-count").textContent(), "71");
    // 到期复习随日期变化，比较当前 API 的证据，不固定旧截图的数量。
    const snapshot = await (await page.request.get(setup.base + "/api/learning")).json();
    const profiles = new Map(snapshot.topics.map((t) => [t.id, t]));
    const initial = snapshot.knowledge_map.nodes.filter((n) => n.initial);
    const ready = initial.filter(
      (n) => n.initial.status === "可进阶" && profiles.get(n.id)?.review?.status !== "due",
    ).length;
    const review = initial.filter(
      (n) => n.initial.status === "待巩固" || profiles.get(n.id)?.review?.status === "due",
    ).length;
    assert.equal(Number(await page.getByTestId("map-state-ready").textContent()), ready);
    assert.equal(Number(await page.getByTestId("map-state-review").textContent()), review);
    assert(await page.getByRole("button", { name: "练这个知识点", exact: true }).isEnabled());
    await map
      .getByRole("button", { name: /查看知识点/ })
      .first()
      .click();
    await page.getByRole("complementary", { name: "知识点学情详情" }).waitFor();
    assert.match(
      await page.getByRole("complementary", { name: "知识点学情详情" }).textContent(),
      /掌握估计|独立首次正确率/,
    );
  });
  await check("graph_search_group_sources_and_zoom", async () => {
    for (const state of ["ready", "review", "diagnose"])
      assert((await page.locator(`.edu-map-node[data-status="${state}"]`).count()) > 0);
    await page.getByRole("button", { name: "只看需要关注" }).click();
    assert.equal(await page.locator('.edu-map-node[data-status="ready"]').count(), 0);
    await page.getByRole("button", { name: "只看需要关注" }).click();
    await page.getByRole("button", { name: "展开数与式", exact: true }).click();
    assert.equal(await page.locator(".edu-map-node").count(), 22);
    await page.getByRole("button", { name: "全部知识", exact: true }).click();
    await page.getByLabel("搜索知识点").fill("绝对值");
    await page.getByRole("button", { name: /查看知识点 绝对值/ }).click();
    assert.match(
      await page.getByRole("complementary", { name: "知识点学情详情" }).textContent(),
      /绝对值/,
    );
    await page.getByLabel("搜索知识点").fill("");
    await page.getByRole("button", { name: "放大图谱" }).click();
    assert.match(await page.getByTestId("map-zoom").textContent(), /120/);
    await page.getByRole("button", { name: "复位图谱" }).click();
    await page.getByRole("combobox", { name: "学情来源" }).click();
    await page.getByRole("option", { name: "近期练习", exact: true }).click();
    await page
      .getByText("还没有新练习，切换到历史画像查看已导入的学情。", {
        exact: true,
      })
      .waitFor();
    await page.getByRole("combobox", { name: "学情来源" }).click();
    await page.getByRole("option", { name: "综合学情", exact: true }).click();
    await page.screenshot({
      path: fileURLToPath(new URL("../.local/reports/learning-map-desktop.png", import.meta.url)),
      fullPage: false,
    });
  });
  await check("graph_topic_routes_to_matching_practice", async () => {
    await page.getByLabel("搜索知识点").fill("绝对值");
    await page.getByRole("button", { name: /查看知识点 绝对值/ }).click();
    await page.getByRole("button", { name: "练这个知识点", exact: true }).click();
    await page.getByRole("heading", { name: "个性化练习", exact: true }).waitFor();
    const learning = await (await page.request.get(`${setup.base}/api/learning`)).json();
    assert.equal(learning.topics.find((topic) => topic.id === learning.goal.topic).title, "绝对值");
    assert.equal(learning.summary.attempts, 0);
    assert(learning.recommendations.length > 0);
    await page.getByRole("button", { name: "学情看板", exact: true }).click();
    await page.getByLabel("搜索知识点").fill("实数的大小比较");
    await page.getByRole("button", { name: /查看知识点 实数的大小比较/ }).click();
    assert.equal(
      await page.getByRole("button", { name: "练这个知识点", exact: true }).isEnabled(),
      false,
    );
    await page.getByLabel("搜索知识点").fill("");
    await page.setViewportSize({ width: 390, height: 844 });
    const graphView = await page.locator(".edu-map-viewport").boundingBox();
    if (graphView.y >= 500) {
      await page.screenshot({
        path: fileURLToPath(new URL("../.local/reports/learning-map-mobile-failure.png", import.meta.url)),
        fullPage: false,
      });
      process.stdout.write(JSON.stringify({ mobileGraph: graphView }) + "\n");
    }
    assert(graphView.y < 500);
    assert.equal(
      await page.evaluate(() => document.documentElement.scrollWidth > innerWidth),
      false,
    );
    await page.screenshot({
      path: fileURLToPath(new URL("../.local/reports/learning-map-mobile.png", import.meta.url)),
      fullPage: false,
    });
    await page.setViewportSize({ width: 1440, height: 960 });
  });
  await page.getByRole("button", { name: "学习路径", exact: true }).click();
  await page.getByText("调整目标与学习时间", { exact: true }).click();
  await page.getByRole("combobox", { name: "学习目标", exact: true }).click();
  await page.getByRole("option", { name: setup.first.title, exact: true }).click();
  await page.getByRole("button", { name: "保存学习目标", exact: true }).click();
  await page.getByText("已保存学习目标。", { exact: true }).waitFor();
  await page.getByRole("button", { name: "开始今日练习" }).click();
  await check("real_catalogue_choice_or_numeric_submission", async () => {
    const section = page.getByRole("region", { name: "当前练习" });
    await section.waitFor();
    if (setup.first.answer_kind === "choice")
      await page.getByRole("radio", { name: new RegExp(`^${setup.answer} `) }).check();
    else await page.getByLabel("我的答案").fill(setup.answer);
    await page.getByRole("button", { name: "核对答案" }).click();
    await page.getByText("答案正确", { exact: true }).waitFor();
    await page.reload();
    await page.getByRole("button", { name: "学情看板", exact: true }).click();
    const summary = page.getByRole("region", { name: "学情摘要", exact: true });
    await summary.waitFor();
    assert.match(await summary.textContent(), /已完成 1 次新练习/);
    assert.match(await summary.textContent(), /独立首次正确率 100%/);
    await page.getByText("数据依据", { exact: true }).click();
    assert.equal(await page.getByTestId("practice-attempts").textContent(), "1");
    assert.equal(await page.getByTestId("initial-attempts").textContent(), "89");
    await page.getByRole("figure", { name: "近七日练习趋势" }).waitFor();
    const day = page.locator('.edu-map-day[data-attempts="1"]');
    assert.equal(await day.count(), 1);
    assert.match(await day.getAttribute("aria-label"), /作答 1 次，答对 1 次/);
    await page.getByText("数据依据", { exact: true }).click();
  });
  await check("choice_controls_and_source_math_rendering", async () => {
    const bootstrap = await (await page.request.get(`${setup.base}/api/bootstrap`)).json();
    const response = await page.request.post(`${setup.base}/api/practice/start`, {
      headers: { Origin: setup.base, "X-Qingqi-CSRF": bootstrap.csrf },
      data: { item_id: setup.choice.id, request_id: "browser-choice" },
    });
    assert.equal(response.status(), 201);
    await page.reload();
    await page.getByRole("button", { name: "个性化练习", exact: true }).click();
    await page.getByRole("radio", { name: new RegExp(`^${setup.choice.answer} `) }).check();
    if (setup.choice.has_math) await page.locator(".katex").first().waitFor();
    await page.getByRole("button", { name: "核对答案" }).click();
    await page.getByText("答案正确", { exact: true }).waitFor();
  });
  await check("mobile_math_rendering_and_no_runtime_errors", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.getByRole("button", { name: "打开导航", exact: true }).click();
    await page.getByRole("button", { name: "个性化练习", exact: true }).click();
    await page.getByRole("region", { name: "当前练习" }).waitFor();
    assert.equal(
      await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 2),
      false,
    );
    assert.deepEqual(errors, []);
    await page.screenshot({
      path: fileURLToPath(new URL("../.local/reports/student-data-mobile.png", import.meta.url)),
      fullPage: true,
    });
    await page.setViewportSize({ width: 1440, height: 960 });
    await page.screenshot({
      path: fileURLToPath(new URL("../.local/reports/student-data-desktop.png", import.meta.url)),
      fullPage: true,
    });
  });
  await writeFile(
    new URL("../.local/reports/student-data-browser.json", import.meta.url),
    JSON.stringify({ passed: tests.length, scenarios: tests }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
