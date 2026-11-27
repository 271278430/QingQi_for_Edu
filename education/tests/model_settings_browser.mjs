import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
const child = spawn(
  process.env.QINGQI_PYTHON,
  [fileURLToPath(new URL("./model_settings_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let browser, page;
const checks = [];
async function check(name, run) {
  await run();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(Error("fixture timeout")), 30000);
    lines.once("line", (l) => {
      clearTimeout(t);
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
  page = await browser.newPage({
    viewport: { width: 1440, height: 1100 },
  });
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  await page.getByRole("button", { name: "设置管理", exact: true }).click();
  await page.getByRole("tab", { name: "模型适配", exact: true }).click();
  await page.waitForFunction(
    () => getComputedStyle(document.body).margin === "0px",
  );
  await check(
    "zcode_original_provider_layout_and_fields_are_rendered",
    async () => {
      await page.locator("[data-model-provider-split-panel]").waitFor();
      await page.locator('[data-provider-source="ZCode"]').waitFor();
      assert.equal(
        await page
          .getByRole("heading", { name: "教学模型", exact: true })
          .count(),
        0,
      );
      await page.locator("[data-model-uses]").waitFor();
      assert.equal(
        await page
          .getByRole("button", { name: "应用教学模型", exact: true })
          .count(),
        0,
      );
    },
  );
  await page.getByRole("button", { name: "添加供应商", exact: true }).click();
  await page
    .getByTestId("model-provider-base-url-input")
    .fill(setup.model_base);
  await page.getByTestId("model-provider-api-key-input").fill(setup.key);
  await page.getByRole("button", { name: "保存连接", exact: true }).click();
  await page
    .getByText("设置已保存，新请求使用当前模型配置。", { exact: true })
    .waitFor();
  await check(
    "connection_is_persisted_without_exposing_saved_key",
    async () => {
      assert.equal(
        await page.getByTestId("model-provider-api-key-input").inputValue(),
        "",
      );
      assert(!(await page.locator("body").innerText()).includes(setup.key));
    },
  );
  async function addModel(id, image) {
    await page.getByRole("button", { name: "添加模型", exact: true }).click();
    const dialog = page.getByRole("dialog");
    await dialog.locator("input").first().fill(id);
    await dialog.locator("[data-model-advanced-trigger]").click();
    if (image)
      await dialog.locator('[data-model-input-modality="image"]').click();
    await dialog.getByRole("button", { name: "保存", exact: true }).click();
    await dialog.waitFor({ state: "hidden" });
  }
  await check(
    "zcode_model_editor_creates_two_models_under_one_connection",
    async () => {
      await addModel("text-local", false);
      await addModel("vision-local", true);
      assert.equal(await page.locator("[data-provider-model]").count(), 2);
      assert.equal(
        await page.locator('[data-model-input-capability="vision"]').count(),
        1,
      );
    },
  );
  await check(
    "zcode_model_test_and_vision_probe_use_saved_models",
    async () => {
      const model = page
        .locator("[data-provider-model]")
        .filter({ hasText: "vision-local" });
      await model
        .getByRole("button", { name: "测试图片识别", exact: true })
        .click();
      await page.getByText("图像识别测试通过。", { exact: true }).waitFor();
    },
  );
  await check(
    "model_edit_preserves_native_capability_and_unknown_save_can_retry",
    async () => {
      let row = page
        .locator("[data-provider-model]")
        .filter({ hasText: "text-local" });
      await row.getByLabel("支持原生工具调用", { exact: true }).click();
      await page.waitForFunction(
        () =>
          [...document.querySelectorAll("[data-provider-model]")]
            .find((row) => row.textContent.includes("text-local"))
            ?.querySelector("input[type=checkbox]")?.checked === false,
      );
      await page
        .getByText("设置已保存，新请求使用当前模型配置。", { exact: true })
        .waitFor();
      await page.route(
        "**/api/settings/model-providers",
        async (route) => {
          // times: 1 已移除拦截器；处理中 unroute 会先继续请求，造成二次处理。
          await route.abort("failed");
        },
        { times: 1 },
      );
      await row
        .getByRole("button", { name: "编辑模型配置", exact: true })
        .click();
      const dialog = page.getByRole("dialog");
      await dialog.locator("input").first().fill("text-updated");
      await dialog.getByRole("button", { name: "保存", exact: true }).click();
      await page
        .getByRole("button", {
          name: "重试上次保存",
          exact: true,
          includeHidden: true,
        })
        .waitFor();
      assert(
        (await dialog
          .locator("[data-model-settings-scroll]")
          .getAttribute("inert")) !== null,
      );
      await page.keyboard.press("Escape");
      await dialog.waitFor({ state: "hidden" });
      await page
        .getByRole("button", { name: "重试上次保存", exact: true })
        .click();
      row = page
        .locator("[data-provider-model]")
        .filter({ hasText: "text-updated" });
      await row.waitFor();
      assert.equal(
        await row.getByLabel("支持原生工具调用", { exact: true }).isChecked(),
        false,
      );
      await row
        .getByRole("button", { name: "编辑模型配置", exact: true })
        .click();
      await page
        .getByRole("dialog")
        .locator("input")
        .first()
        .fill("text-local");
      await page
        .getByRole("dialog")
        .getByRole("button", { name: "保存", exact: true })
        .click();
      await page.getByRole("dialog").waitFor({ state: "hidden" });
    },
  );
  await check(
    "delayed_settings_read_cannot_roll_back_successful_save",
    async () => {
      let release, ready;
      const held = new Promise((resolve) => (release = resolve));
      const captured = new Promise((resolve) => (ready = resolve));
      await page.route(
        "**/api/settings/models",
        async (route) => {
          const response = await route.fetch();
          ready();
          await held;
          await route.fulfill({ response });
        },
        { times: 1 },
      );
      await page.getByRole("button", { name: "刷新", exact: true }).click();
      await captured;
      await page.getByLabel("请求超时", { exact: true }).fill("17");
      await page.getByRole("button", { name: "保存连接", exact: true }).click();
      await page.waitForFunction(
        () =>
          document.querySelector('[aria-label="请求超时"]')?.value === "17" &&
          !document.querySelector('[aria-label="请求超时"]')?.disabled,
      );
      const releasedResponse = page.waitForResponse(
        (r) =>
          r.url().endsWith("/api/settings/models") &&
          r.request().method() === "GET",
      );
      release();
      await releasedResponse;
      await page.unroute("**/api/settings/models");
      assert.equal(
        await page.getByLabel("请求超时", { exact: true }).inputValue(),
        "17",
      );
    },
  );
  await page
    .locator("[data-provider-model]")
    .filter({ hasText: "text-local" })
    .getByRole("button", { name: "设为文本默认", exact: true })
    .click();
  await page
    .locator("[data-provider-model]")
    .filter({ hasText: "text-local" })
    .locator('[data-model-use-role="text"][aria-pressed="true"]')
    .waitFor();
  await page
    .locator("[data-provider-model]")
    .filter({ hasText: "vision-local" })
    .getByRole("button", { name: "设为图片默认", exact: true })
    .click();
  await page
    .locator("[data-provider-model]")
    .filter({ hasText: "vision-local" })
    .locator('[data-model-use-role="vision"][aria-pressed="true"]')
    .waitFor();
  await check("roles_select_concrete_models_and_survive_refresh", async () => {
    await page
      .getByText("设置已保存，新请求使用当前模型配置。", { exact: true })
      .waitFor();
    await page.reload();
    await page.waitForFunction(
      () => getComputedStyle(document.body).margin === "0px",
    );
    await page.getByRole("button", { name: "设置管理", exact: true }).click();
    await page.getByRole("tab", { name: "模型适配", exact: true }).click();
    await page
      .getByRole("button", { name: "自定义供应商", exact: true })
      .click();
    await page
      .locator("[data-provider-model]")
      .filter({ hasText: "text-local" })
      .locator('[data-model-use-role="text"][aria-pressed="true"]')
      .waitFor();
    await page
      .locator("[data-provider-model]")
      .filter({ hasText: "vision-local" })
      .locator('[data-model-use-role="vision"][aria-pressed="true"]')
      .waitFor();
    const view = await (
      await page.request.get(setup.base + "/api/settings/models")
    ).json();
    const chat = await (
      await page.request.get(setup.base + "/api/chat/models")
    ).json();
    assert.equal(chat.selection.text.model_id, view.selection.text_provider_id);
    assert.equal(
      chat.selection.vision.model_id,
      view.selection.vision_provider_id,
    );
  });
  await check(
    "source_provider_model_editor_is_accessible_on_mobile",
    async () => {
      await page.setViewportSize({ width: 390, height: 844 });
      assert(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      );
      assert.deepEqual(errors, []);
      await page.screenshot({
        path: fileURLToPath(
          new URL(
            "../.local/reports/model-settings-v8-mobile.png",
            import.meta.url,
          ),
        ),
        fullPage: true,
      });
    },
  );
  await page.setViewportSize({ width: 1440, height: 1100 });
  await check("provider_navigation_selection_matches_detail", async () => {
    await page
      .getByRole("button", { name: "自定义供应商", exact: true })
      .click();
    await page.waitForFunction(
      () =>
        document
          .querySelector('button[aria-label="自定义供应商"]')
          ?.getAttribute("aria-selected") === "true",
    );
    await page
      .locator('[data-provider-source="ZCode"]')
      .getByText("自定义供应商", { exact: true })
      .waitFor();
    assert.equal(await page.locator("[data-provider-model]").count(), 2);
  });
  await page.screenshot({
    path: fileURLToPath(
      new URL(
        "../.local/reports/model-settings-v8-desktop.png",
        import.meta.url,
      ),
    ),
    fullPage: false,
  });
  await writeFile(
    new URL(
      "../.local/reports/model-settings-browser-v8.local.json",
      import.meta.url,
    ),
    JSON.stringify(
      { passed: checks.length, checks, source_components: true },
      null,
      2,
    ),
  );
} catch (error) {
  if (page)
    process.stdout.write(
      JSON.stringify({
        dialog: await page
          .getByRole("dialog")
          .innerText()
          .catch(() => "no dialog"),
      }),
    );
  throw error;
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
