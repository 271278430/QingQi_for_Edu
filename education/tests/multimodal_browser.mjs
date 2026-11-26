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
  [fileURLToPath(new URL("./multimodal_browser_server.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
const tests = [],
  errors = [];
let browser,
  stderr = "";
child.stderr.on("data", (v) => {
  stderr += v;
});
const check = async (name, run) => {
  await run();
  tests.push({ name, passed: true });
  process.stdout.write(JSON.stringify(tests.at(-1)) + "\n");
};
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(
      () => reject(new Error(stderr || "fixture timeout")),
      30000,
    );
    lines.once("line", (l) => {
      clearTimeout(timer);
      resolve(JSON.parse(l));
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
  const page = await browser.newPage({
    viewport: { width: 1440, height: 960 },
  });
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  await page.getByRole("button", { name: "新建学习对话", exact: true }).click();
  await page.waitForFunction(
    () =>
      !document.querySelector("#edu-question")?.disabled &&
      !document.querySelector(".edu-question-reference"),
  );
  await check("image_picker_preview_and_removal", async () => {
    await page.getByLabel("上传题目图片").setInputFiles(setup.image);
    const preview = page.getByLabel("待发送图片");
    await preview.getByRole("img").waitFor();
    await page
      .getByRole("button", { name: "移除图片 equation.png", exact: true })
      .click();
    assert.equal(await preview.count(), 0);
    await page.getByLabel("上传题目图片").setInputFiles(setup.image);
    await preview.getByRole("img").waitFor();
    assert.equal(
      await preview
        .getByRole("img")
        .evaluate((image) => getComputedStyle(image).objectFit),
      "contain",
    );
  });
  await check(
    "image_only_send_renders_owned_photo_transcription_and_guidance",
    async () => {
      const waiting = page.waitForResponse(
        (r) =>
          r.url().endsWith("/api/teach") && r.request().method() === "POST",
      );
      await page
        .getByRole("button", { name: "发送学习问题", exact: true })
        .click();
      const response = await waiting;
      assert.equal(response.status(), 200);
      await page
        .getByText("图片识别的题目 · 可在对话中纠正", { exact: true })
        .waitFor();
      await page.locator(".edu-user img").waitFor();
      assert.match(
        await page.locator(".edu-user img").getAttribute("src"),
        /^\/api\/tutor\/image\?id=/,
      );
      assert.match((await readTeachResponse(response)).response.text, /3x/);
    },
  );
  await check("image_followup_is_natural_conversation", async () => {
    await page.getByLabel("你的学习问题", { exact: true }).fill("x=4");
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "发送学习问题", exact: true })
      .click();
    assert.equal(
      (await readTeachResponse(await waiting)).response.teaching_action,
      "confirm",
    );
    await page.waitForFunction(() => {
      const input = document.querySelector("#edu-question");
      return input && input.value === "" && !input.disabled;
    });
    await page.screenshot({
      path: fileURLToPath(
        new URL(
          "../.local/reports/multimodal-tutor-desktop.png",
          import.meta.url,
        ),
      ),
      fullPage: true,
    });
  });
  await check("table_image_receives_natural_description", async () => {
    await page
      .getByRole("button", { name: "新建学习对话", exact: true })
      .click();
    await page.waitForFunction(
      () => !document.querySelector("#edu-question")?.disabled,
    );
    await page.getByLabel("上传题目图片").setInputFiles(setup.table);
    await page.getByLabel("待发送图片").getByRole("img").waitFor();
    await page
      .getByLabel("你的学习问题", { exact: true })
      .fill("分析一下这个图片中的表格表达了什么");
    const waiting = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "发送学习问题", exact: true })
      .click();
    const response = await waiting;
    assert.equal(response.status(), 200);
    assert.equal(
      (await readTeachResponse(response)).response.teaching_action,
      "explain",
    );
    await page.waitForFunction(
      () => !document.querySelector("#edu-question")?.disabled,
    );
    await page.getByText(/这是一张统计表/).waitFor();
    await page.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/image-upload-repaired.png", import.meta.url),
      ),
      fullPage: true,
    });
  });
  await check(
    "four_image_selection_is_rejected_without_partial_draft",
    async () => {
      await page
        .getByRole("button", { name: "新建学习对话", exact: true })
        .click();
      await page.waitForFunction(
        () => !document.querySelector("#edu-question")?.disabled,
      );
      await page
        .getByLabel("上传题目图片")
        .setInputFiles([setup.image, setup.table, setup.second, setup.image]);
      await page.getByText("每次最多上传三张图片。", { exact: true }).waitFor();
      assert.equal(await page.getByLabel("待发送图片").count(), 0);
    },
  );
  await check(
    "three_images_move_with_text_into_pending_and_accepted_message",
    async () => {
      await page.getByLabel("上传题目图片").setInputFiles(setup.image);
      await page.getByLabel("待发送图片").getByRole("img").waitFor();
      await page
        .getByLabel("上传题目图片")
        .setInputFiles([setup.table, setup.second]);
      await page.waitForFunction(
        () =>
          document.querySelectorAll('[aria-label="待发送图片"] img').length ===
          3,
      );
      await page
        .getByLabel("你的学习问题", { exact: true })
        .fill("一起分析这三张图片中的表格和方程");
      let release;
      const gate = new Promise((resolve) => {
        release = resolve;
      });
      await page.route("**/api/teach", async (route) => {
        await gate;
        await route.continue();
      });
      const waiting = page.waitForResponse(
        (r) =>
          r.url().endsWith("/api/teach") && r.request().method() === "POST",
      );
      try {
        await page
          .getByRole("button", { name: "发送学习问题", exact: true })
          .click();
        await page.waitForFunction(
          () =>
            document.querySelectorAll(
              '.edu-user [aria-label="本条消息的图片"] img',
            ).length === 3,
        );
        assert.match(
          await page.locator(".edu-user").textContent(),
          /一起分析这三张图片/,
        );
        assert.equal(await page.getByLabel("待发送图片").count(), 0);
        await page.waitForFunction(() =>
          [
            ...document.querySelectorAll(
              '.edu-user [aria-label="本条消息的图片"] img',
            ),
          ].every((image) => image.complete && image.naturalWidth > 0),
        );
        await page.screenshot({
          path: fileURLToPath(
            new URL(
              "../.local/reports/three-images-pending.png",
              import.meta.url,
            ),
          ),
          fullPage: true,
        });
      } finally {
        release();
      }
      const response = await waiting;
      assert.equal(response.status(), 200);
      const result = await readTeachResponse(response);
      assert.equal(result.session.messages.at(-1).images.length, 3);
      await page.waitForFunction(
        () =>
          !document.querySelector("#edu-question")?.disabled &&
          document.querySelector("#edu-question")?.value === "",
      );
      await page.unroute("**/api/teach");
      assert.equal(await page.locator(".edu-user img").count(), 3);
      const names = await page
        .locator(".edu-user img")
        .evaluateAll((nodes) => nodes.map((n) => n.alt));
      assert.deepEqual(names, [
        "equation.png",
        "table.png",
        "second-equation.png",
      ]);
      assert(
        await page
          .locator(".edu-user img")
          .evaluateAll((nodes) =>
            nodes.every(
              (image) => getComputedStyle(image).objectFit === "contain",
            ),
          ),
      );
      await page
        .getByRole("button", { name: "放大查看 table.png", exact: true })
        .press("Enter");
      await page
        .getByRole("dialog")
        .getByRole("img", { name: "table.png", exact: true })
        .waitFor();
      await page.waitForFunction(() => {
        const image = document.querySelector('[role="dialog"] img');
        return (
          image &&
          image.complete &&
          image.naturalWidth > 0 &&
          image.clientHeight > 0
        );
      });
      await page.getByRole("dialog").evaluate(async (element) => {
        await Promise.all(
          element.getAnimations().map((animation) => animation.finished),
        );
      });
      await page.screenshot({
        path: fileURLToPath(
          new URL(
            "../.local/reports/three-images-preview.png",
            import.meta.url,
          ),
        ),
        fullPage: true,
      });
      await page.keyboard.press("Escape");
      // Escape 后共享 Dialog 有退出动画；等待真正关闭，避免把过渡帧误存为最终消息截图。
      await page.getByRole("dialog").waitFor({ state: "hidden" });
      await page.waitForFunction(() =>
        [...document.querySelectorAll(".edu-user img")].every(
          (image) => image.complete && image.naturalWidth > 0,
        ),
      );
      await page.screenshot({
        path: fileURLToPath(
          new URL(
            "../.local/reports/three-images-message.png",
            import.meta.url,
          ),
        ),
        fullPage: true,
      });
      await page.reload();
      await page.waitForFunction(
        () => document.querySelectorAll(".edu-user img").length === 3,
      );
      assert.deepEqual(
        await page
          .locator(".edu-user img")
          .evaluateAll((nodes) => nodes.map((n) => n.alt)),
        names,
      );
    },
  );
  await check(
    "history_search_and_selection_reuses_practice_reference",
    async () => {
      await page.getByRole("button", { name: "历史题目", exact: true }).click();
      await page
        .getByRole("heading", { name: "选择历史题目", exact: true })
        .waitFor();
      await page.getByLabel("搜索历史题目").fill(setup.history_title);
      const actual = page
        .getByRole("dialog")
        .locator("article")
        .filter({ hasText: "本产品作答" });
      await actual
        .getByRole("button", { name: "讨论这道题", exact: true })
        .click();
      await page.getByRole("region", { name: "正在讨论的题目" }).waitFor();
      assert(
        !(
          await page.getByLabel("你的学习问题", { exact: true }).inputValue()
        ).includes("题目："),
      );
    },
  );
  await check(
    "model_protocol_error_keeps_draft_editable_without_permission_banner",
    async () => {
      await page.getByLabel("上传题目图片").setInputFiles(setup.image);
      await page.getByLabel("待发送图片").getByRole("img").waitFor();
      await page
        .getByLabel("你的学习问题", { exact: true })
        .fill("分析这个图片的表格，空回复");
      const waiting = page.waitForResponse(
        (r) =>
          r.url().endsWith("/api/teach") && r.request().method() === "POST",
      );
      await page
        .getByRole("button", { name: "发送学习问题", exact: true })
        .click();
      const response = await waiting;
      assert.equal(response.status(), 200);
      const failure = (await response.text())
        .split("\n\n")
        .filter((v) => v.startsWith("data: "))
        .map((v) => JSON.parse(v.slice(6)))
        .at(-1);
      assert.equal(failure.kind, "error");
      assert.equal(failure.status, 502);
      assert.equal(failure.error, "model_protocol");
      await page.waitForFunction(
        () => !document.querySelector("#edu-question")?.disabled,
      );
      assert.equal(
        await page.getByLabel("你的学习问题", { exact: true }).inputValue(),
        "分析这个图片的表格，空回复",
      );
      assert.equal(
        await page
          .getByRole("button", { name: "重试当前请求", exact: true })
          .count(),
        0,
      );
      assert.equal(
        await page.getByText(/账户、会话归属或操作权限不符/).count(),
        0,
      );
      await page
        .getByRole("button", { name: "移除图片 equation.png", exact: true })
        .click();
    },
  );
  await check(
    "recognition_schema_error_preserves_photo_and_allows_new_request",
    async () => {
      await page
        .getByRole("button", { name: "新建学习对话", exact: true })
        .click();
      // 新建会话仍会清理旧草稿；必须等它完成，再选择本轮图片。
      await page.waitForFunction(
        () => !document.querySelector("#edu-question")?.disabled,
      );
      await page.getByLabel("上传题目图片").setInputFiles(setup.image);
      await page.getByLabel("待发送图片").getByRole("img").waitFor();
      let uploads = 0;
      page.on("request", (request) => {
        if (
          request.url().endsWith("/api/tutor/images") &&
          request.method() === "POST"
        )
          uploads++;
      });
      await page
        .getByLabel("你的学习问题", { exact: true })
        .fill("解这道题，测试识别回显");
      const failed = page.waitForResponse(
        (r) =>
          r.url().endsWith("/api/teach") && r.request().method() === "POST",
      );
      await page
        .getByRole("button", { name: "发送学习问题", exact: true })
        .click();
      const failureResponse = await failed;
      assert.equal(
        failureResponse.request().postDataJSON().request.images.length,
        1,
      );
      assert.equal(failureResponse.status(), 200);
      const failure = (await failureResponse.text())
        .split("\n\n")
        .filter((v) => v.startsWith("data: "))
        .map((v) => JSON.parse(v.slice(6)))
        .at(-1);
      assert.equal(failure.kind, "error");
      assert.equal(failure.status, 502);
      await page.waitForFunction(
        () => !document.querySelector("#edu-question")?.disabled,
      );
      assert.equal(
        await page
          .getByRole("button", { name: "重试当前请求", exact: true })
          .count(),
        0,
      );
      assert.equal(
        await page.getByLabel("待发送图片").getByRole("img").count(),
        1,
      );
      assert.equal(
        await page.getByText(/unknown.*input|required_output_schema/).count(),
        0,
      );
      await page
        .getByLabel("你的学习问题", { exact: true })
        .fill("重新引导我理解这道题");
      const accepted = page.waitForResponse(
        (r) =>
          r.url().endsWith("/api/teach") && r.request().method() === "POST",
      );
      await page
        .getByRole("button", { name: "发送学习问题", exact: true })
        .click();
      assert.equal((await accepted).status(), 200);
      await page.waitForFunction(
        () =>
          !document.querySelector("#edu-question")?.disabled &&
          document.querySelector("#edu-question")?.value === "",
      );
      assert.equal(uploads, 1);
      assert.equal(await page.getByLabel("待发送图片").count(), 0);
      await page.locator(".edu-user img").last().waitFor();
    },
  );
  await check("composer_and_history_fit_mobile_dark_theme", async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    const darkSwitch = page.getByRole("button", {
      name: "切换深色主题",
      exact: true,
    });
    if (await darkSwitch.count()) await darkSwitch.click();
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    await page.getByRole("button", { name: "历史题目", exact: true }).click();
    await page.getByRole("dialog").waitFor();
    assert(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    );
    await page.screenshot({
      path: fileURLToPath(
        new URL(
          "../.local/reports/multimodal-history-mobile.png",
          import.meta.url,
        ),
      ),
      fullPage: true,
    });
  });
  assert.deepEqual(errors, []);
  await writeFile(
    fileURLToPath(
      new URL("../.local/reports/multimodal-browser.json", import.meta.url),
    ),
    JSON.stringify(
      { passed: tests.length, tests, errors, real_model: false },
      null,
      2,
    ),
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
