// Real browser -> HTTP owner -> durable checkpoint; no mocked API or model responses.
import { chromium } from "playwright-core";
import { readTeachResponse } from "./read_teach_response.mjs";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const child = spawn(
  process.env.QINGQI_PYTHON || "python",
  [fileURLToPath(new URL("./browser_recovery_server.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let startupError = "";
child.stderr.on("data", (value) => {
  startupError += value.toString();
});
const tests = [];
const errors = [];
let browser;
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("recovery fixture did not start")), 30000);
    lines.once("line", (line) => {
      clearTimeout(timer);
      resolve(JSON.parse(line));
    });
    child.once("exit", (code) => {
      clearTimeout(timer);
      reject(new Error(`fixture exited ${code}: ${startupError}`));
    });
    child.once("error", (error) => {
      clearTimeout(timer);
      reject(error);
    });
  });
  browser = await chromium.launch({
    channel: process.env.QINGQI_BROWSER_CHANNEL || "msedge",
    headless: true,
  });
  const page = await browser.newPage({
    viewport: { width: 1440, height: 960 },
  });
  page.on("pageerror", (error) => errors.push(error.message));
  for (const item of setup.cases) {
    await page.goto(setup.base);
    await page.getByRole("button", { name: item.name, exact: true }).click();
    await page.getByRole("button", { name: "继续此请求", exact: true }).waitFor();
    await page.reload();
    await page.getByRole("button", { name: item.name, exact: true }).click();
    const request = page.waitForRequest((value) => value.url().endsWith("/api/teach"));
    const response = page.waitForResponse((value) => value.url().endsWith("/api/teach"));
    await page.getByRole("button", { name: "继续此请求", exact: true }).click();
    const sent = (await request).postDataJSON();
    const result = await response;
    assert.equal(result.status(), 200, await result.text());
    assert.deepEqual(sent.request, item.request);
    const value = await readTeachResponse(result);
    assert.equal(value.response.teaching_action, item.expected);
    assert.equal(value.session.messages.at(-1).request_id, item.request.request_id);
    assert.equal(
      value.session.messages.at(-1).trace.events.filter((event) => event.kind === "tool_authorized")
        .length,
      1,
    );
    await page
      .getByRole("button", { name: "继续此请求", exact: true })
      .waitFor({ state: "hidden" });
    tests.push({ name: item.name, passed: true });
    process.stdout.write(JSON.stringify(tests.at(-1)) + "\n");
  }
  assert.deepEqual(errors, []);
} finally {
  await browser?.close();
  lines.close();
  child.kill();
  await writeFile(
    fileURLToPath(new URL("../.local/reports/browser-recovery-acceptance.json", import.meta.url)),
    JSON.stringify(
      {
        tests,
        pageErrors: errors,
        actualHTTP: true,
        scope: "offline durable recovery with original inputs",
        passed: tests.length === 2 && errors.length === 0,
      },
      null,
      2,
    ),
  );
}
