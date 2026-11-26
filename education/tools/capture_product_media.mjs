import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { fileURLToPath } from "node:url";
import { mkdir, writeFile } from "node:fs/promises";
import { saveFullDiagram } from "./save_full_diagram.mjs";
import assert from "node:assert/strict";
const child = spawn(
  process.env.QINGQI_PYTHON,
  [fileURLToPath(new URL("demo_media_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["pipe", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let browser;
const destination = new URL("../docs/media/", import.meta.url);
await mkdir(destination, { recursive: true });
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
    executablePath:
      "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  });
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1000 },
  });
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  const boot = await (
    await page.request.get(setup.base + "/api/bootstrap")
  ).json();
  const post = async (path, data) => {
    const r = await page.request.post(setup.base + path, {
      data,
      headers: { Origin: setup.base, "X-Qingqi-CSRF": boot.csrf },
    });
    assert(r.ok(), path + " " + r.status());
    return r.json();
  };
  for (const [i, [id, answer]] of Object.entries(setup.answers).entries()) {
    const a = await post("/api/practice/start", {
      item_id: id,
      request_id: "media-start-" + i,
    });
    await post("/api/practice/answer", {
      assignment_id: a.id,
      answer: i === 1 ? "0" : answer,
      request_id: "media-answer-" + i,
    });
  }
  await page.reload();
  await page.evaluate(() => {
    document.documentElement.classList.remove("dark", "theme-zai-dark");
    document.documentElement.classList.add("theme-zai-light");
  });
  for (const [name, target, file] of [
    ["学情看板", ".edu-map-viewport", "dashboard.png"],
    ["学习路径", ".edu-branch-map", "learning-path.png"],
    ["个性化练习", '[data-testid="recommendation-card"]', "practice.png"],
  ]) {
    await page
      .getByRole("navigation", { name: "主导航", exact: true })
      .getByRole("button", { name, exact: true })
      .click();
    await page.locator(target).first().waitFor();
    await page.mouse.move(0, 0);
    await page.screenshot({ path: fileURLToPath(new URL(file, destination)) });
  }
  await page
    .getByRole("navigation", { name: "主导航", exact: true })
    .getByRole("button", { name: "个性化辅导", exact: true })
    .click();
  await page.getByRole("button", { name: "新建学习对话", exact: true }).click();
  await page
    .locator("#edu-question")
    .fill(
      "已知 f(x)=x³-ax²+4，在(0,∞)内有且仅有一个零点，在[-1,2]求最值。请用动画完整演示解题过程，直接给出分析。",
    );
  await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
  await page.locator(".is-assistant").last().waitFor({ timeout: 90000 });
  await page
    .getByRole("button", { name: "播放动画", exact: true })
    .first()
    .waitFor({ timeout: 90000 });
  await page.locator(".edu-messages").evaluate((e) => {
    e.scrollTop = 0;
  });
  await page.mouse.move(0, 0);
  await page.screenshot({
    path: fileURLToPath(new URL("tutoring.png", destination)),
  });
  const canvas = page.locator(".edu-reasoning-lesson").last();
  await mkdir(new URL("../../.local/reports/media-frames/", destination), {
    recursive: true,
  });
  const titles = [];
  for (let i = 0; i < 12; i++) {
    await page
      .getByRole("slider", { name: "动画进度", exact: true })
      .first()
      .evaluate(
        (input, value) => {
          Object.getOwnPropertyDescriptor(
            HTMLInputElement.prototype,
            "value",
          ).set.call(input, String(value));
          input.dispatchEvent(new Event("input", { bubbles: true }));
          input.dispatchEvent(new Event("change", { bubbles: true }));
        },
        Math.round((i * 1000) / 11),
      );
    await page.waitForFunction(
      (value) =>
        Math.abs(
          Number(
            document
              .querySelector("[data-teaching-animation]")
              ?.getAttribute("data-animation-progress"),
          ) -
            value / 1000,
        ) < 0.002,
      Math.round((i * 1000) / 11),
    );
    titles.push(await canvas.getByTestId("reasoning-step-title").innerText());
    await saveFullDiagram(
      browser,
      canvas.locator("svg.edu-reasoning-curve").first(),
      new URL(
        "../../.local/reports/media-frames/" +
          String(i).padStart(2, "0") +
          ".png",
        destination,
      ),
    );
  }
  await writeFile(
    new URL("../../.local/reports/media-frames/titles.json", destination),
    JSON.stringify(titles),
  );
  assert.deepEqual(errors, []);
  process.stdout.write(
    JSON.stringify({ screenshots: 4, animation_frames: 12, synthetic: true }) +
      "\n",
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
