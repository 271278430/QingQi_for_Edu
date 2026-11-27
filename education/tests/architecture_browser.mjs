import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { fileURLToPath, pathToFileURL } from "node:url";
import { writeFile } from "node:fs/promises";
import assert from "node:assert/strict";
import { geometryFailures } from "./architecture_geometry.mjs";
import { saveFullDiagram } from "./save_full_diagram.mjs";
const child = spawn(
  process.env.QINGQI_PYTHON,
  [fileURLToPath(new URL("conversation_problem_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let browser;
const checks = [];
async function check(name, run) {
  await run();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(Error("fixture timeout")), 30000);
    lines.once("line", (line) => {
      clearTimeout(t);
      resolve(JSON.parse(line));
    });
  });
  browser = await chromium.launch({
    headless: true,
    executablePath:
      "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  });
  const page = await browser.newPage({
    viewport: { width: 1600, height: 1100 },
  });
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("button", { name: "设置管理", exact: true }).click();
  await page.getByRole("tab", { name: "项目架构", exact: true }).click();
  await page.locator("[data-architecture-ready]").waitFor();
  const data = await (
    await page.request.get(setup.base + "/api/settings/architecture")
  ).json();
  const svg = page.locator("svg[data-system-panorama]");
  await check("single_system_map_has_sixteen_verified_modules", async () => {
    assert.equal(data.version, "source_architecture_v15");
    assert.equal(data.modules.length, 16);
    assert(
      data.modules.every(
        (m) =>
          m.bindings.length &&
          m.bindings.every((b) => b.verified) &&
          m.scope.steps.length,
      ),
    );
    assert(!("request_flow" in data) && !("business_flow" in data));
    assert.equal(
      await page
        .getByRole("tab", { name: "输入输出流程", exact: true })
        .count(),
      0,
    );
    assert.equal(
      await page.getByRole("tab", { name: "四功能流程", exact: true }).count(),
      0,
    );
    assert.equal(await page.locator("svg[data-system-panorama]").count(), 1);
  });
  await check(
    "agent_loop_has_actual_decide_call_observe_return_cycle",
    async () => {
      for (const [a, b] of [
        ["decision", "action"],
        ["action", "observe"],
        ["observe", "decision"],
        ["decision", "validation"],
        ["validation", "accepted"],
        ["accepted", "persistence"],
      ])
        assert(
          data.panorama.edges.some(
            (e) => e.source === a && e.target === b && e.heads === "end",
          ),
          a + " to " + b,
        );
    },
  );
  await check(
    "map_is_readable_without_collisions_and_exports_svg",
    async () => {
      await saveFullDiagram(
        browser,
        svg,
        new URL(
          "../.local/reports/architecture-v15-system.png",
          import.meta.url,
        ),
      );
      assert.deepEqual(await geometryFailures(svg, data.panorama), []);
      const download = page.waitForEvent("download");
      await page
        .getByRole("button", { name: "下载架构SVG", exact: true })
        .click();
      const file = fileURLToPath(
        new URL(
          "../.local/reports/architecture-v15-system.svg",
          import.meta.url,
        ),
      );
      await (await download).saveAs(file);
      const full = await browser.newPage({
        viewport: { width: data.panorama.width, height: data.panorama.height },
      });
      await full.goto(pathToFileURL(file).href);
      await full
        .locator("svg")
        .first()
        .screenshot({
          path: fileURLToPath(
            new URL(
              "../.local/reports/architecture-v15-export.png",
              import.meta.url,
            ),
          ),
        });
      await full.close();
    },
  );
  await check("all_modules_open_scope_instead_of_more_diagrams", async () => {
    for (const m of data.modules) {
      await svg.locator('[data-architecture-module="' + m.id + '"]').click();
      const dialog = page.getByRole("dialog");
      await dialog
        .getByRole("heading", { name: m.title, exact: true })
        .waitFor();
      await dialog
        .getByRole("region", { name: "模块职责与内部流程" })
        .waitFor();
      assert.equal(await page.locator("svg[data-system-panorama]").count(), 1);
      await page.keyboard.press("Escape");
      await dialog.waitFor({ state: "hidden" });
    }
  });
  await check("zoom_reset_expanded_map_and_keyboard", async () => {
    await page.getByRole("button", { name: "放大全景", exact: true }).click();
    assert.equal(await svg.getAttribute("data-panorama-zoom"), "1.25");
    await page.getByRole("button", { name: "原始字号", exact: true }).click();
    await page.getByRole("button", { name: "放大架构图", exact: true }).click();
    await page
      .getByRole("dialog")
      .locator("svg[data-system-panorama]")
      .waitFor();
    await page.keyboard.press("Escape");
    await page.getByRole("dialog").waitFor({ state: "hidden" });
    await svg.locator('[data-architecture-module="loop"]').focus();
    await page.keyboard.press("Enter");
    await page
      .getByRole("dialog")
      .getByRole("heading", { name: "Agent Loop", exact: true })
      .waitFor();
    await page.keyboard.press("Escape");
  });
  await check("light_dark_and_mobile_preserve_map", async () => {
    await page.evaluate(() => {
      document.documentElement.classList.remove("theme-zai-dark", "dark");
      document.documentElement.classList.add("theme-zai-light");
    });
    await saveFullDiagram(
      browser,
      svg,
      new URL("../.local/reports/architecture-v13-light.png", import.meta.url),
    );
    assert.deepEqual(await geometryFailures(svg, data.panorama), []);
    await page.setViewportSize({ width: 390, height: 844 });
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    await page.screenshot({
      path: fileURLToPath(
        new URL(
          "../.local/reports/architecture-v13-mobile.png",
          import.meta.url,
        ),
      ),
    });
    assert.deepEqual(errors, []);
  });
  await writeFile(
    new URL(
      "../.local/reports/architecture-v13-browser.local.json",
      import.meta.url,
    ),
    JSON.stringify({ passed: checks.length, checks, modules: 16 }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
