// Repeatable full student flow for the reported question and evidence-based route map.
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
  [fileURLToPath(new URL("./history_tutor_browser_server.py", import.meta.url))],
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
async function check(name, action) {
  await action();
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
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  page.setDefaultTimeout(30000);
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  const send = async (question) => {
    if (question) await page.getByLabel("你的学习问题", { exact: true }).fill(question);
    const result = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const response = await result;
    assert.equal(response.status(), 200);
    await page.waitForFunction(() => !document.querySelector("#edu-question")?.disabled);
    return readTeachResponse(response);
  };
  await check("exact_history_picker_to_sent_owned_question", async () => {
    await page.getByRole("button", { name: "历史题目", exact: true }).click();
    await page.getByLabel("搜索历史题目").fill(setup.title);
    const actual = page.getByRole("dialog").locator("article").filter({ hasText: "本产品作答" });
    await actual.getByRole("button", { name: "讨论这道题", exact: true }).click();
    await page.getByRole("region", { name: "正在讨论的题目" }).waitFor();
    // 启动时可已显示同一题，等待历史选择命令真正填入草稿后再点击发送。
    await page.waitForFunction(
      () =>
        document.querySelector("#edu-question")?.value ===
        "返回原练习，我想复习这道历史题，请先和我讨论解题思路。",
    );
    assert.equal(
      await page.getByLabel("你的学习问题", { exact: true }).inputValue(),
      "返回原练习，我想复习这道历史题，请先和我讨论解题思路。",
    );
    const result = await send();
    assert.equal(result.response.teaching_action, "ask");
    assert.match(result.response.text, /第二个方程|16/);
    assert.doesNotMatch(result.response.text, /你希望查询|请提供/);
    // 公式由 ZCode 数学组件渲染，DOM 文本不会保留原始美元分隔符。
    await page.getByText("你准备怎样写出代入后的等式？", { exact: false }).waitFor();
  });
  await check("masked_symbols_render_through_zcode_math_content", async () => {
    const reference = page.getByRole("region", { name: "正在讨论的题目" });
    assert.equal(await reference.locator(".katex-error").count(), 0);
    assert((await reference.locator(".katex").count()) >= 4);
    assert.doesNotMatch(await reference.innerText(), /\$[★■]\$/);
    const assistant = page.locator(".is-assistant").last();
    assert(await assistant.count());
    assert.doesNotMatch(await assistant.innerText(), /\$[★■]\$/);
  });
  await check("intermediate_work_checks_same_question_after_refresh", async () => {
    const response = await send("y=4");
    assert.equal(response.response.teaching_action, "confirm");
    await page.reload();
    await page.getByRole("region", { name: "正在讨论的题目" }).waitFor();
    const follow = await send("★=10");
    assert.equal(follow.response.teaching_action, "confirm");
    const before = await (await page.request.get(setup.base + "/api/learning")).json();
    const final = await send("A");
    assert.equal(final.response.teaching_action, "confirm");
    const after = await (await page.request.get(setup.base + "/api/learning")).json();
    assert.equal(after.summary.attempts, before.summary.attempts + 1);
    await page.screenshot({
      path: fileURLToPath(new URL("../.local/reports/history-tutor-desktop.png", import.meta.url)),
      fullPage: true,
    });
  });
  await page.getByRole("button", { name: "学习路径", exact: true }).click();
  await check("route_map_choice_persists_and_controls_three_items", async () => {
    const choice = page.getByTestId("route-choice").filter({ hasText: "补弱优先" });
    await choice.click();
    await page.getByText("已选择路线，个性化练习已重新匹配。").waitFor();
    const view = await (await page.request.get(setup.base + "/api/learning")).json();
    assert.equal(view.path.selected_route, "foundation");
    assert.equal(view.recommendations.length, 3);
    assert.equal(view.recommendations[0].topic, view.path.focus);
    assert.equal(view.path.steps.length, 5);
    assert.doesNotMatch(
      await page.getByRole("region", { name: "学习路线地图" }).innerText(),
      /平方根/,
    );
    const station = page.getByTestId("route-station").filter({ hasText: "绝对值" }).first();
    await station.click();
    await page.getByRole("region", { name: "地图节点说明" }).waitFor();
    assert.match(await page.getByRole("region", { name: "地图节点说明" }).innerText(), /教材|先修/);
    assert.match(await page.getByRole("region", { name: "地图节点说明" }).innerText(), /下一步/);
    await page.reload();
    await page.getByRole("button", { name: "学习路径", exact: true }).click();
    assert.equal(
      await page
        .getByTestId("route-choice")
        .filter({ hasText: "补弱优先" })
        .getAttribute("aria-pressed"),
      "true",
    );
  });
  for (const [name, width, height] of [
    ["desktop", 1440, 960],
    ["narrow", 1024, 900],
    ["mobile", 390, 844],
  ]) {
    await check("five_station_map_fits_" + name, async () => {
      await page.setViewportSize({ width, height });
      if (name === "mobile") {
        const dark = page.getByRole("button", { name: "切换深色主题", exact: true });
        if (await dark.count()) await dark.click();
      }
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      const bounds = await page.getByTestId("route-station").evaluateAll((nodes) =>
        nodes.map((node) => ({
          route: node.dataset.route,
          ...JSON.parse(JSON.stringify(node.getBoundingClientRect())),
        })),
      );
      for (const box of bounds) assert(box.left >= 0 && box.right <= width);
      for (const [i, a] of bounds.entries())
        for (const b of bounds.slice(i + 1))
          assert(
            !(a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top),
            "route nodes overlap",
          );
      await page.screenshot({
        path: fileURLToPath(
          new URL(`../.local/reports/evidence-route-${name}.png`, import.meta.url),
        ),
        fullPage: true,
      });
    });
  }
  assert.deepEqual(errors, []);
  await writeFile(
    fileURLToPath(new URL("../.local/reports/history-tutor-browser.json", import.meta.url)),
    JSON.stringify({ passed: tests.length, tests, errors, real_model: false }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
