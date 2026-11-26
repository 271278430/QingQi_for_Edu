import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { fileURLToPath } from "node:url";
import { writeFile } from "node:fs/promises";
import assert from "node:assert/strict";

const child = spawn(
  process.env.QINGQI_PYTHON,
  [fileURLToPath(new URL("product_usability_server.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let browser, page;
const checks = [];
const check = async (name, run) => {
  await run();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
};
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(Error("fixture timeout")), 30000);
    lines.once("line", (line) => {
      clearTimeout(timer);
      resolve(JSON.parse(line));
    });
  });
  browser = await chromium.launch({
    headless: true,
    executablePath: "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  });
  page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  const navigate = async (name) =>
    page
      .getByRole("navigation", { name: "主导航" })
      .getByRole("button", { name, exact: true })
      .click();
  const settings = async () => page.getByRole("button", { name: "设置管理", exact: true }).click();
  await check("student_surface_has_only_complete_controls", async () => {
    assert.equal(await page.getByRole("button", { name: "切换界面语言", exact: true }).count(), 0);
    assert.equal(await page.getByText("学生学习空间", { exact: true }).count(), 0);
    await page.getByRole("button", { name: "上传图片", exact: true }).waitFor();
    await page.getByRole("button", { name: "历史题目", exact: true }).waitFor();
    await page.evaluate(() => localStorage.setItem("zcode-locale-preference", "en-US"));
    await page.reload();
    await page.getByRole("button", { name: "新建学习对话", exact: true }).waitFor();
    assert(
      (await page.evaluate(() => localStorage.getItem("zcode-locale-preference"))).startsWith("zh"),
    );
  });
  await check("conversation_switch_locks_input_until_owned_detail_is_ready", async () => {
    await page.waitForFunction(() => !document.querySelector("#edu-question")?.disabled);
    await page.getByLabel("你的学习问题", { exact: true }).fill("上一段对话的未发送草稿");
    let release, entered;
    const held = new Promise((r) => (release = r)),
      ready = new Promise((r) => (entered = r));
    await page.route(
      "**/api/session?*",
      async (route) => {
        const response = await route.fetch();
        entered();
        await held;
        await route.fulfill({ response });
      },
      { times: 1 },
    );
    await page.getByTestId("history-item").nth(1).click();
    await ready;
    assert(await page.getByLabel("你的学习问题", { exact: true }).isDisabled());
    assert(await page.getByRole("button", { name: "发送学习问题", exact: true }).isDisabled());
    const arrival = page.waitForResponse(
      (r) => r.url().includes("/api/session?") && r.request().method() === "GET",
    );
    release();
    await arrival;
    await page.waitForFunction(
      () =>
        document.querySelector("#edu-question")?.value === "" &&
        !document.querySelector("#edu-question")?.disabled,
    );
  });
  await check("learning_navigation_preserves_unsubmitted_answer", async () => {
    await navigate("个性化练习");
    await page.getByRole("region", { name: "当前练习", exact: true }).waitFor();
    const answer = page.getByLabel("我的答案", { exact: true });
    const radio = page.locator('input[name="practice-choice"]').first();
    const numeric = await answer.count();
    if (numeric) await answer.fill("3/4");
    else await radio.check();
    await navigate("学习路径");
    await page.getByRole("region", { name: "学习路线地图", exact: true }).waitFor();
    await navigate("个性化练习");
    if (numeric) assert.equal(await answer.inputValue(), "3/4");
    else assert(await radio.isChecked());
    assert.equal(await page.getByTestId("recommendation-card").count(), 3);
    await page.screenshot({
      path: fileURLToPath(new URL("../.local/reports/solid-practice-desktop.png", import.meta.url)),
      fullPage: true,
    });
  });
  await check("dashboard_exposes_actions_without_empty_noise", async () => {
    await navigate("学情看板");
    await page.getByRole("region", { name: "学情摘要", exact: true }).waitFor();
    await page.locator(".edu-map-node").first().waitFor();
    assert.equal(await page.getByText(/新练习待复测 0 个知识点/).count(), 0);
    await page.getByLabel("搜索知识点").fill("不存在的知识点_solid");
    await page.getByText("没有匹配的知识点。", { exact: true }).waitFor();
    await page.getByRole("button", { name: "查看全部知识", exact: true }).click();
    await page.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/solid-dashboard-desktop.png", import.meta.url),
      ),
      fullPage: true,
    });
  });
  await check("same_version_read_preserves_settings_draft", async () => {
    await settings();
    await page.getByLabel("产品名称", { exact: true }).waitFor();
    let release, entered;
    const held = new Promise((r) => (release = r)),
      ready = new Promise((r) => (entered = r));
    await page.route(
      "**/api/settings",
      async (route) => {
        const response = await route.fetch();
        entered();
        await held;
        await route.fulfill({ response });
      },
      { times: 1 },
    );
    await page.getByRole("button", { name: "刷新设置", exact: true }).click();
    await ready;
    await page.getByLabel("产品名称", { exact: true }).fill("草稿不会被读取抹掉");
    const arrival = page.waitForResponse(
      (r) => r.url().endsWith("/api/settings") && r.request().method() === "GET",
    );
    release();
    await arrival;
    await page.waitForFunction(
      () => document.querySelector('[aria-label="产品名称"]')?.value === "草稿不会被读取抹掉",
    );
  });
  await check("old_read_cannot_roll_back_saved_system_settings", async () => {
    let release, entered;
    const held = new Promise((r) => (release = r)),
      ready = new Promise((r) => (entered = r));
    await page.route("**/api/settings", async (route) => {
      if (route.request().method() !== "GET") return route.continue();
      const response = await route.fetch();
      entered();
      await held;
      await route.fulfill({ response });
    });
    await page.getByRole("button", { name: "刷新设置", exact: true }).click();
    await ready;
    await page.getByLabel("产品名称", { exact: true }).fill("保存的新名称");
    await page.getByRole("button", { name: "保存设置", exact: true }).click();
    await page.getByText("设置已保存并生效。", { exact: true }).waitFor();
    const arrival = page.waitForResponse(
      (r) => r.url().endsWith("/api/settings") && r.request().method() === "GET",
    );
    release();
    await arrival;
    await page.unroute("**/api/settings");
    assert.equal(await page.getByLabel("产品名称", { exact: true }).inputValue(), "保存的新名称");
  });
  await check("save_notifies_workspace_after_settings_unmount", async () => {
    let release, entered;
    const held = new Promise((r) => (release = r)),
      ready = new Promise((r) => (entered = r));
    await page.route("**/api/settings", async (route) => {
      if (route.request().method() !== "POST") return route.continue();
      const response = await route.fetch();
      entered();
      await held;
      await route.fulfill({ response });
    });
    await page.getByLabel("产品名称", { exact: true }).fill("清启");
    await page.getByRole("button", { name: "保存设置", exact: true }).click();
    await ready;
    await navigate("个性化练习");
    const arrival = page.waitForResponse(
      (r) => r.url().endsWith("/api/settings") && r.request().method() === "POST",
    );
    release();
    await arrival;
    await page.unroute("**/api/settings");
    await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  });
  await check("desktop_and_phone_navigation_are_meaningful", async () => {
    await page.setViewportSize({ width: 900, height: 900 });
    assert.equal(
      await page.getByRole("button", { name: "打开导航", exact: true }).isVisible(),
      false,
    );
    await page.setViewportSize({ width: 390, height: 844 });
    const opener = page.getByRole("button", { name: "打开导航", exact: true });
    await opener.click();
    await page
      .getByRole("button", { name: "关闭导航遮罩", exact: true })
      .click({ position: { x: 370, y: 400 } });
    await page.waitForFunction(
      () => document.querySelector(".edu-sidebar")?.dataset.open === "false",
    );
    await opener.click();
    await page.keyboard.press("Escape");
    await page.waitForFunction(
      () => document.querySelector(".edu-sidebar")?.dataset.open === "false",
    );
    await opener.click();
    await navigate("学情看板");
    assert.equal(await opener.getAttribute("aria-expanded"), "false");
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await page.screenshot({
      path: fileURLToPath(new URL("../.local/reports/solid-dashboard-mobile.png", import.meta.url)),
      fullPage: true,
    });
  });
  await check("themes_and_settings_core_functions_remain_available", async () => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.getByRole("button", { name: /切换.*色主题/ }).click();
    await settings();
    for (const tab of ["模型适配", "项目架构", "系统管理"]) {
      await page.getByRole("tab", { name: tab, exact: true }).click();
    }
    await page.getByRole("button", { name: "清空全部历史", exact: true }).click();
    await page.getByRole("dialog").getByRole("button", { name: "取消", exact: true }).click();
    assert.deepEqual(errors, []);
  });
  await check("proxy_error_is_readable_and_save_retry_keeps_original_command", async () => {
    await page.route(
      "**/api/settings",
      (route) =>
        route.fulfill({
          status: 503,
          contentType: "text/html",
          body: "<h1>Upstream unavailable</h1>",
        }),
      { times: 1 },
    );
    await page.getByRole("button", { name: "刷新设置", exact: true }).click();
    await page
      .getByRole("alert")
      .getByText(/服务暂时不可用/)
      .waitFor();
    await page.getByRole("button", { name: "刷新设置", exact: true }).click();
    await page.getByRole("alert").waitFor({ state: "hidden" });
    const commands = [];
    const record = (request) => {
      if (request.url().endsWith("/api/settings") && request.method() === "POST")
        commands.push(request.postDataJSON());
    };
    page.on("request", record);
    await page.getByLabel("服务公告", { exact: true }).fill("隔离验收公告");
    await page.route(
      "**/api/settings",
      (route) =>
        route.fulfill({ status: 503, contentType: "text/html", body: "<h1>Unavailable</h1>" }),
      { times: 1 },
    );
    await page.getByRole("button", { name: "保存设置", exact: true }).click();
    await page.getByRole("button", { name: "重试保存", exact: true }).waitFor();
    assert(await page.getByLabel("服务公告", { exact: true }).isDisabled());
    await page.getByRole("button", { name: "重试保存", exact: true }).click();
    await page.getByText("设置已保存并生效。", { exact: true }).waitFor();
    page.off("request", record);
    assert.equal(commands.length, 2);
    assert.deepEqual(commands[0], commands[1]);
    assert.deepEqual(errors, []);
  });
  await writeFile(
    new URL("../.local/reports/solid-web-browser.local.json", import.meta.url),
    JSON.stringify({ passed: checks.length, checks, isolated: true }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
