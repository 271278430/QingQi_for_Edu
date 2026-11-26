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
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`fixture timeout: ${stderr}`)), 30000);
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
  await check("only_four_product_navigation_entries", async () => {
    assert.deepEqual(
      await page.getByRole("navigation", { name: "主导航" }).getByRole("button").allTextContents(),
      ["个性化辅导", "学习路径", "学情看板", "个性化练习"],
    );
    assert.equal(await page.getByText("模型连接", { exact: true }).count(), 0);
    assert.equal(await page.getByText("学习依据与过程", { exact: true }).count(), 0);
  });
  await check("path_goal_saved_and_practice_started", async () => {
    await page.getByRole("button", { name: "学习路径", exact: true }).click();
    await page.getByText("调整目标与学习时间", { exact: true }).click();
    await page.getByRole("combobox", { name: "学习目标", exact: true }).click();
    await page.getByRole("option", { name: "分数运算", exact: true }).click();
    await page.getByLabel("每日学习分钟").fill("15");
    await page.getByRole("button", { name: "保存学习目标" }).click();
    await page.getByText("已保存学习目标。").waitFor();
    assert.match(await page.getByTestId("adaptive-plan").textContent(), /独立诊断/);
    const map = page.getByRole("region", { name: "学习路线地图", exact: true });
    await map.waitFor();
    const current = await (await page.request.get(`${setup.base}/api/learning`)).json();
    assert.equal(
      await map.getByTestId("route-station").count(),
      current.path.routes.reduce((n, r) => n + r.steps.length, 0),
    );
    assert.equal(
      await page.getByRole("progressbar", { name: "独立首次正确率", exact: true }).count(),
      0,
    );
    await page.getByRole("button", { name: "开始今日练习" }).click();
    await page.getByRole("heading", { name: "当前练习", exact: true }).waitFor();
  });
  await check("distinct_hints_and_verified_answer", async () => {
    assert.equal(await page.getByRole("button", { name: "苏格拉底追问", exact: true }).count(), 0);
    await page.getByRole("button", { name: "给我一点提示", exact: true }).click();
    await page.getByRole("status", { name: "练习提示" }).waitFor();
    const first = await page.getByRole("status", { name: "练习提示" }).textContent();
    await page.getByRole("button", { name: "给我一点提示", exact: true }).click();
    await page.waitForFunction(
      (old) => document.querySelector('[aria-label="练习提示"]')?.textContent !== old,
      first,
    );
    const current = await (await page.request.get(`${setup.base}/api/learning`)).json();
    await page.getByLabel("我的答案", { exact: true }).fill(setup.answers[current.active.item.id]);
    await page.getByRole("button", { name: "核对答案", exact: true }).click();
    await page.getByText("答案正确", { exact: true }).waitFor();
    await page.getByText("本题使用过提示或辅导，计入辅助练习。").waitFor();
    await page.reload();
    await page.getByRole("button", { name: "个性化练习", exact: true }).click();
    await page.getByText("答案正确", { exact: true }).waitFor();
  });
  await check("three_purpose_cards_and_renew_preserves_grades", async () => {
    const before = await (await page.request.get(`${setup.base}/api/learning`)).json();
    assert.equal(await page.getByTestId("recommendation-card").count(), 3);
    assert.equal(new Set(before.recommendations.map((i) => i.topic)).size, 3);
    const ids = before.recommendations.map((i) => i.id);
    await page.getByRole("button", { name: "换一组", exact: true }).click();
    await page.getByText("已更新本组三题。", { exact: true }).waitFor();
    const after = await (await page.request.get(`${setup.base}/api/learning`)).json();
    assert.equal(after.summary.attempts, before.summary.attempts);
    assert.notDeepEqual(
      after.recommendations.map((i) => i.id),
      ids,
    );
    assert.equal(await page.getByTestId("recommendation-card").count(), 3);
    await page.reload();
    await page.getByRole("button", { name: "个性化练习", exact: true }).click();
    const restored = await (await page.request.get(`${setup.base}/api/learning`)).json();
    assert.deepEqual(restored.recommendations, after.recommendations);
  });
  await check("dashboard_is_actual_evidence_and_mobile_operable", async () => {
    await page.getByRole("button", { name: "学情看板", exact: true }).click();
    await page.getByRole("heading", { name: "学情看板", exact: true }).waitFor();
    await page.getByText("运算顺序", { exact: true }).first().waitFor();
    const summary = page.getByRole("region", { name: "学情摘要", exact: true });
    assert.match(await summary.textContent(), /已完成 1 次新练习/);
    assert.match(await summary.textContent(), /还没有独立首次作答证据/);
    await page.getByText("数据依据", { exact: true }).click();
    assert.equal(await page.getByTestId("assisted-attempts").textContent(), "1");
    assert.equal(await page.getByTestId("independent-correct").textContent(), "0");
    await page.getByText("数据依据", { exact: true }).click();
    await page.setViewportSize({ width: 390, height: 844 });
    await page.getByRole("button", { name: "打开导航", exact: true }).click();
    await page.getByRole("button", { name: "个性化练习", exact: true }).click();
    await page.getByRole("heading", { name: "当前练习", exact: true }).waitFor();
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.screenshot({
      path: fileURLToPath(new URL("../.local/reports/four-feature-mobile.png", import.meta.url)),
      fullPage: true,
    });
    await page.setViewportSize({ width: 1440, height: 960 });
    await page.screenshot({
      path: fileURLToPath(new URL("../.local/reports/four-feature-desktop.png", import.meta.url)),
      fullPage: true,
    });
  });
  assert.deepEqual(errors, []);
  await writeFile(
    fileURLToPath(new URL("../.local/reports/four-feature-browser.json", import.meta.url)),
    JSON.stringify({ passed: tests.length, tests, errors, remote_inference: false }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
