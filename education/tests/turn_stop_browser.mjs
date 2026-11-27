import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const child = spawn(
  process.env.QINGQI_PYTHON,
  [fileURLToPath(new URL("turn_stop_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["pipe", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let browser,
  stderr = "";
const checks = [],
  errors = [],
  requests = [];
child.stderr.on("data", (v) => {
  stderr += v;
});
async function check(name, fn) {
  await fn();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const t = setTimeout(
      () => reject(Error(stderr || "fixture timeout")),
      30000,
    );
    lines.once("line", (line) => {
      clearTimeout(t);
      resolve(JSON.parse(line));
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
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("request", (r) => {
    if (r.url().endsWith("/api/teach") && r.method() === "POST")
      requests.push(r.postDataJSON());
  });
  await page.goto(setup.base);
  await page.getByRole("textbox", { name: "你的学习问题" }).waitFor();
  const input = page.getByRole("textbox", { name: "你的学习问题" });
  async function stats() {
    return (await page.request.get(setup.stats)).json();
  }
  async function waitCalls(n) {
    for (let i = 0; i < 100; i++) {
      if ((await stats()).calls >= n) return;
      await new Promise((r) => setTimeout(r, 100));
    }
    throw Error("model was not entered");
  }
  async function waitUnlocked() {
    await page.waitForFunction(
      () => !document.querySelector("#edu-question")?.disabled,
    );
  }
  await check("double_submit_admits_only_one_live_request", async () => {
    await input.fill("二次函数的顶点是什么？");
    await input.evaluate((element) => {
      const form = element.closest("form");
      form.requestSubmit();
      form.requestSubmit();
    });
    await waitCalls(1);
    assert.equal(requests.length, 1);
    await page
      .getByText("二次函数的顶点是抛物线转弯的位置。", { exact: false })
      .last()
      .waitFor();
  });
  await check(
    "stop_button_cancels_server_and_keeps_editable_input",
    async () => {
      await page.getByRole("button", { name: "停止生成", exact: true }).click();
      await waitUnlocked();
      assert.equal(await input.inputValue(), "二次函数的顶点是什么？");
      const detail = await (
        await page.request.get(
          setup.base + "/api/session?id=" + requests[0].session,
        )
      ).json();
      assert.equal(detail.messages.at(-1).trace.error_code, "turn_cancelled");
      assert.equal(detail.messages.at(-1).trace.running, false);
      assert.ok(detail.messages.at(-1).partial_response);
      assert.ok((await stats()).closed >= 1);
      assert.equal(
        await page
          .getByRole("button", { name: "继续此请求", exact: true })
          .count(),
        0,
      );
    },
  );
  await check("reload_can_stop_an_owned_running_message", async () => {
    await input.fill("继续解释二次函数的顶点是什么？");
    await page.getByRole("button", { name: "发送学习问题" }).click();
    await waitCalls(2);
    await page.reload();
    const stop = page.getByRole("button", {
      name: "停止这轮生成",
      exact: true,
    });
    await stop.waitFor();
    await stop.click();
    await waitUnlocked();
    const detail = await (
      await page.request.get(
        setup.base + "/api/session?id=" + requests[1].session,
      )
    ).json();
    assert.equal(detail.messages.at(-1).trace.error_code, "turn_cancelled");
    assert.equal(detail.messages.at(-1).trace.running, false);
    assert.ok((await stats()).closed >= 2);
  });
  await check("mobile_can_stop_before_first_visible_token", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    await input.fill("二次函数的顶点是什么？等待首字");
    await page.getByRole("button", { name: "发送学习问题" }).click();
    await waitCalls(3);
    const stop = page.getByRole("button", { name: "停止生成", exact: true });
    await stop.click();
    await waitUnlocked();
    const detail = await (
      await page.request.get(
        setup.base + "/api/session?id=" + requests[2].session,
      )
    ).json();
    assert.equal(detail.messages.at(-1).trace.error_code, "turn_cancelled");
    assert.equal(detail.messages.at(-1).partial_response, undefined);
    assert.ok(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth + 2,
      ),
    );
    await page.screenshot({
      path: "education/.local/reports/turn-stop-mobile.local.png",
      fullPage: true,
    });
  });
  await check(
    "explicit_restart_is_available_without_automatic_replay",
    async () => {
      assert.equal(requests.length, 3);
      assert.equal((await stats()).calls, 3);
      assert.ok(
        await page
          .getByRole("button", { name: "重新回答", exact: true })
          .last()
          .isEnabled(),
      );
    },
  );
  await check("cancellation_has_no_render_or_raw_thinking_errors", async () => {
    assert.deepEqual(errors, []);
    assert.ok(
      !(await page.locator("body").innerText()).includes("synthetic thinking"),
    );
  });
} finally {
  await browser?.close();
  child.stdin.end();
}
await writeFile(
  "education/.local/reports/turn-stop-browser.local.json",
  JSON.stringify({ checks, passed: checks.length }, null, 2),
);
