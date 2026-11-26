import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
import { readTeachResponse } from "./read_teach_response.mjs";

const child = spawn(
  process.env.QINGQI_PYTHON,
  [fileURLToPath(new URL("composer_models_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let browser,
  stderr = "";
child.stderr.on("data", (v) => (stderr += v));
const checks = [];
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
    child.once("exit", () => {
      clearTimeout(timer);
      reject(Error(stderr));
    });
  });
  browser = await chromium.launch({
    headless: true,
    executablePath: [
      "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
      "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    ].find(existsSync),
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } }),
    errors = [],
    requests = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("request", (r) => {
    if (r.url().endsWith("/api/teach") && r.method() === "POST") requests.push(r.postDataJSON());
  });
  await page.goto(setup.base);
  const text = () => page.getByTestId("composer-model-text"),
    vision = () => page.getByTestId("composer-model-vision");
  await text().waitFor();
  async function level(role, value) {
    await page.getByTestId(`composer-model-${role}`).click();
    const saved = page.waitForResponse(
      (r) => r.url().endsWith("/api/chat/models") && r.request().method() === "POST",
    );
    await page.getByRole("slider", { name: "推理档位" }).fill(String(value));
    assert.equal((await saved).status(), 200);
    await page.keyboard.press("Escape");
    await page.waitForFunction(
      (role) => !document.querySelector(`[data-testid="composer-model-${role}"]`).disabled,
      role,
    );
  }
  const session = () =>
    page.request
      .get(setup.base + "/api/sessions")
      .then((r) => r.json())
      .then((v) => v.sessions[0]?.id);
  async function send(question) {
    await page.getByLabel("你的学习问题", { exact: true }).fill(question);
    const wait = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const data = await readTeachResponse(await wait);
    assert.ok(data.session);
    await page.waitForFunction(
      () =>
        !document.querySelector("#edu-question").disabled &&
        document.querySelector("#edu-question").value === "",
    );
    return data;
  }
  await check("zcode_menu_defaults_high_and_keeps_composer_draft", async () => {
    assert.ok((await text().innerText()).includes("高"));
    await page.getByLabel("你的学习问题", { exact: true }).fill("二次函数的顶点是什么？");
    await level("text", 0);
    assert.ok((await text().innerText()).includes("低"));
    assert.equal(
      await page.getByLabel("你的学习问题", { exact: true }).inputValue(),
      "二次函数的顶点是什么？",
    );
  });
  await check("frozen_low_survives_image_upload_and_new_session", async () => {
    await page.getByLabel("上传题目图片").setInputFiles(setup.image);
    await page.getByLabel("待发送图片").getByRole("img").waitFor();
    let releaseImage, enterImage;
    const imageGate = new Promise((resolve) => {
      releaseImage = resolve;
    });
    const imageEntered = new Promise((resolve) => {
      enterImage = resolve;
    });
    await page.route("**/api/tutor/images", async (route) => {
      enterImage();
      await imageGate;
      await route.continue();
    });
    const sending = send("教我图片中的题目");
    sending.catch(() => {});
    await imageEntered;
    await page.waitForFunction(
      () => document.querySelector('[data-testid="composer-model-vision"]')?.disabled === false,
    );
    await level("vision", 0);
    releaseImage();
    await sending;
    await page.unroute("**/api/tutor/images");
    const request = requests.at(-1).request;
    assert.equal(request.model_selection.text.reasoning_level, "low");
    assert.equal(request.model_selection.vision.reasoning_level, "high");
    assert.equal(request.images.length, 1);
    assert.ok((await text().innerText()).includes("低"));
    assert.ok(
      (await vision().innerText()).includes("低"),
      "upload-time selection must survive in the new session",
    );
  });
  const previous = await session();
  await check("refresh_and_session_isolation_preserve_explicit_low", async () => {
    await page.reload();
    await text().waitFor();
    assert.ok((await text().innerText()).includes("低"));
    await page.getByRole("button", { name: "新建学习对话", exact: true }).click();
    await page.waitForFunction(() =>
      document.querySelector('[data-testid="composer-model-text"]')?.textContent.includes("高"),
    );
    assert.notEqual(await session(), previous);
  });
  await check("choosing_configured_model_reuses_zcode_menu", async () => {
    await text().click();
    await page.getByRole("menuitemradio").filter({ hasText: "gated-model" }).click();
    await page.keyboard.press("Escape");
    await page
      .waitForFunction(
        () =>
          document
            .querySelector('[data-testid="composer-model-text"]')
            ?.textContent.includes("gated-model"),
        undefined,
        { timeout: 5000 },
      )
      .catch(async (e) => {
        process.stdout.write(
          JSON.stringify({
            button: await text().innerText(),
            view: await (
              await page.request.get(setup.base + "/api/chat/models?session=" + (await session()))
            ).json(),
            alerts: await page.getByRole("alert").allTextContents(),
          }),
        );
        await page.screenshot({ path: "education/.local/reports/composer-debug.local.png" });
        throw e;
      });
  });
  await check("switching_effort_during_generation_only_changes_next_turn", async () => {
    await page.getByLabel("你的学习问题", { exact: true }).fill("二次函数的顶点是什么？");
    const wait = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
    const response = await wait;
    let started = false;
    for (let i = 0; i < 50; i++) {
      if ((await (await page.request.get(setup.control)).json()).started) {
        started = true;
        break;
      }
      await page.waitForTimeout(100);
    }
    assert.ok(started, "gated provider did not start");
    await text().click();
    const saved = page.waitForResponse(
      (r) => r.url().endsWith("/api/chat/models") && r.request().method() === "POST",
    );
    await page.getByRole("slider", { name: "推理档位" }).fill("0");
    assert.equal((await saved).status(), 200);
    await page.keyboard.press("Escape");
    await page.request.post(setup.control);
    assert.ok((await readTeachResponse(response)).session);
    await page.waitForFunction(() => !document.querySelector("#edu-question").disabled);
    assert.equal(requests.at(-1).request.model_selection.text.reasoning_level, "high");
    await send("顶点和对称轴有什么关系？");
    assert.equal(requests.at(-1).request.model_selection.text.reasoning_level, "low");
  });
  await check("mobile_menu_remains_usable", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.getByRole("button", { name: /切换.*主题/ }).click();
    await vision().click();
    await page.getByRole("slider", { name: "推理档位" }).waitFor();
    await page.keyboard.press("Escape");
    assert.ok(await page.getByRole("button", { name: "发送学习问题", exact: true }).isVisible());
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    assert.deepEqual(errors, []);
  });
  await page.screenshot({ path: "education/.local/reports/composer-models-mobile.local.png" });
  await writeFile(
    "education/.local/reports/composer-models-browser.local.json",
    JSON.stringify({ checks, passed: checks.length, errors, isolated: true }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
}
