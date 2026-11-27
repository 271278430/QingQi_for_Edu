// Read-only smoke of the two installed product entries, keeping student history and grades intact.
import { chromium } from "playwright-core";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
const browser = await chromium.launch({
  headless: true,
  executablePath: [
    "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
  ].find(existsSync),
});
const checks = [];
try {
  for (const port of [18772, 18774]) {
    const page = await browser.newPage({
      viewport: { width: 1440, height: 960 },
    });
    const errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.goto(`http://127.0.0.1:${port}/`);
    await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
    const before = await (
      await page.request.get(`http://127.0.0.1:${port}/api/learning`)
    ).json();
    for (const [name, target] of [
      ["学情看板", ".edu-map-viewport"],
      ["学习路径", ".edu-branch-map"],
      ["个性化练习", '[data-testid="recommendation-card"]'],
      ["个性化辅导", "#edu-question"],
    ]) {
      await page
        .getByRole("navigation", { name: "主导航", exact: true })
        .getByRole("button", { name, exact: true })
        .click();
      await page.locator(target).first().waitFor();
      if (name === "个性化练习")
        assert.equal(await page.getByTestId("recommendation-card").count(), 3);
      if (name === "学情看板")
        await page.screenshot({
          path: fileURLToPath(
            new URL(
              `../.local/reports/deployed-${port}-dashboard.png`,
              import.meta.url,
            ),
          ),
          fullPage: false,
        });
      checks.push({ name: `${port}_${name}`, passed: true });
    }
    await page.getByTestId("composer-model-text").waitFor();
    await page.getByTestId("composer-model-vision").waitFor();
    const chatModels = await (
      await page.request.get(`http://127.0.0.1:${port}/api/chat/models`)
    ).json();
    assert(chatModels.models.length > 0);
    assert(
      chatModels.models.every(
        (m) =>
          !Object.hasOwn(m, "base_url") &&
          !Object.hasOwn(m, "api_key") &&
          !Object.hasOwn(m, "config"),
      ),
    );
    assert(
      chatModels.models
        .filter((m) => m.levels.includes("high"))
        .every((m) => m.default_level === "high"),
    );
    await page.getByTestId("composer-model-vision").click();
    await page.getByRole("menu").first().waitFor();
    await page.keyboard.press("Escape");
    checks.push({ name: `${port}_对话框选模与安全目录`, passed: true });
    await page.getByRole("button", { name: "设置管理", exact: true }).click();
    await page.getByRole("tab", { name: "系统管理", exact: true }).waitFor();
    checks.push({ name: `${port}_设置管理`, passed: true });
    await page.getByRole("tab", { name: "模型适配", exact: true }).click();
    await page
      .getByRole("heading", { name: "模型配置", exact: true })
      .waitFor();
    await page.locator("[data-model-uses]").waitFor();
    const models = await (
      await page.request.get(`http://127.0.0.1:${port}/api/settings/models`)
    ).json();
    assert.equal(
      await page
        .getByRole("heading", { name: "教学模型", exact: true })
        .count(),
      0,
    );
    assert(models.connections.every((p) => !p.readonly));
    assert(models.providers.length > 0 && models.selection);
    assert(
      models.providers.every(
        (p) =>
          !Object.hasOwn(p, "api_key") && !Object.hasOwn(p, "encrypted_key"),
      ),
    );
    checks.push({ name: `${port}_模型适配双角色与密钥隐藏`, passed: true });
    await page.getByRole("tab", { name: "项目架构", exact: true }).click();
    await page.locator("[data-architecture-ready]").waitFor();
    const arch = await (
      await page.request.get(
        `http://127.0.0.1:${port}/api/settings/architecture`,
      )
    ).json();
    assert.equal(arch.modules.length, 16);
    assert.equal(arch.version, "source_architecture_v15");
    assert(!arch.request_flow && !arch.business_flow);
    assert(
      arch.modules.every(
        (m) =>
          m.scope.inputs.length &&
          m.scope.outputs.length &&
          m.scope.steps.every((s) => s.detail.length > 25 && s.interface),
      ),
    );
    const map = page.locator("svg[data-system-panorama]");
    assert.equal(await map.getAttribute("data-panorama-view"), "system");
    assert.equal(await map.locator("[data-architecture-module]").count(), 16);
    assert(
      arch.panorama.edges.some(
        (e) => e.source === "observe" && e.target === "decision",
      ),
    );
    checks.push({ name: `${port}_系统关系与真实Loop`, passed: true });
    await map.locator('[data-architecture-module="loop"]').click();
    const moduleDialog = page.getByRole("dialog");
    await moduleDialog
      .getByRole("heading", { name: "Agent Loop", exact: true })
      .waitFor();
    await moduleDialog
      .getByRole("tab", { name: "4 · 观察结果再决策", exact: true })
      .click();
    await moduleDialog.getByText(/ZCode执行工具后校验结果Schema/).waitFor();
    await page.keyboard.press("Escape");
    await moduleDialog.waitFor({ state: "hidden" });
    checks.push({ name: `${port}_模块职责与源码`, passed: true });
    await page.getByRole("button", { name: "放大架构图", exact: true }).click();
    await page
      .getByRole("dialog")
      .locator("svg[data-system-panorama]")
      .waitFor();
    await page.keyboard.press("Escape");
    await page.getByRole("dialog").waitFor({ state: "hidden" });
    checks.push({ name: `${port}_架构放大与关闭`, passed: true });
    const after = await (
      await page.request.get(`http://127.0.0.1:${port}/api/learning`)
    ).json();
    assert.deepEqual(after.summary, before.summary);
    assert.deepEqual(errors, []);
    await page.setViewportSize({ width: 390, height: 844 });
    await page.getByRole("button", { name: "打开导航", exact: true }).click();
    await page
      .getByRole("navigation", { name: "主导航", exact: true })
      .getByRole("button", { name: "学情看板", exact: true })
      .click();
    await page.getByRole("region", { name: "学情摘要", exact: true }).waitFor();
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    await page.close();
  }
  await writeFile(
    new URL(
      "../.local/reports/product-deployment-browser.local.json",
      import.meta.url,
    ),
    JSON.stringify({ passed: checks.length, checks, read_only: true }, null, 2),
  );
  process.stdout.write(
    JSON.stringify({ passed: checks.length, real_deployed_entries: true }) +
      "\n",
  );
} finally {
  await browser.close();
}
