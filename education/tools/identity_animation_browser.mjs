import { chromium } from "playwright-core";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { existsSync } from "node:fs";
import { writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const child = spawn(
  process.env.QINGQI_PYTHON || "python",
  [
    fileURLToPath(
      new URL("identity_animation_browser_server.py", import.meta.url),
    ),
  ],
  { windowsHide: true, stdio: ["pipe", "pipe", "pipe"] },
);
const lines = createInterface({ input: child.stdout });
let stderr = "",
  browser;
const checks = [],
  errors = [];
child.stderr.on("data", (chunk) => {
  stderr += chunk;
});
async function check(name, run) {
  await run();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
}
try {
  const setup = await new Promise((resolve, reject) => {
    const timer = setTimeout(
      () => reject(new Error(stderr || "fixture timeout")),
      30000,
    );
    lines.once("line", (line) => {
      clearTimeout(timer);
      resolve(JSON.parse(line));
    });
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
    viewport: { width: 1440, height: 1000 },
  });
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  const boot = await (
    await page.request.get(setup.base + "/api/bootstrap")
  ).json();
  const started = await page.request.post(setup.base + "/api/practice/start", {
    data: { item_id: setup.item, request_id: "browser-identity" },
    headers: { Origin: setup.base, "X-Qingqi-CSRF": boot.csrf },
  });
  assert.equal(started.status(), 201);
  const assignment = await started.json();
  await page.reload();
  await page
    .getByRole("navigation", { name: "主导航" })
    .getByRole("button", { name: "个性化练习", exact: true })
    .click();
  await page.getByRole("button", { name: "和导师一起做", exact: true }).click();
  await page
    .getByRole("region", { name: "正在讨论的题目", exact: true })
    .waitFor();
  await page.waitForFunction(() =>
    document.querySelector("#edu-question")?.value?.includes("返回原练习"),
  );
  await page.locator("#edu-question").fill("能给动画的教学方式吗");
  const sent = page.waitForResponse(
    (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
  );
  await page.getByRole("button", { name: "发送学习问题", exact: true }).click();
  const result = await sent;
  assert.equal(result.status(), 200);
  const response = (await result.json()).response;
  const animation = page
    .locator('[data-teaching-animation="identity_probe"]')
    .first();
  await check("reported_request_renders_owned_math_animation", async () => {
    await animation.waitFor();
    await animation.locator(".katex").first().waitFor();
    assert.equal(response.visuals[0].algebra_lesson.equation, "mx-8=5x+n");
    assert.equal(await page.getByRole("alert").count(), 0);
    assert.equal(await animation.locator(".katex-error").count(), 0);
    assert.match(await animation.innerText(), /系数|常数/);
  });
  await check("one_play_reaches_last_step_without_stopping", async () => {
    await animation
      .getByRole("button", { name: "播放动画", exact: true })
      .click();
    await page.waitForFunction(
      () =>
        Number(
          document
            .querySelector('[data-teaching-animation="identity_probe"]')
            ?.getAttribute("data-animation-progress"),
        ) > 0.4,
    );
    assert.equal(
      await animation
        .getByRole("button", { name: "暂停动画", exact: true })
        .count(),
      1,
    );
    await page.waitForFunction(
      () =>
        document
          .querySelector('[data-teaching-animation="identity_probe"]')
          ?.getAttribute("data-animation-progress") === "1",
      null,
      { timeout: 25000 },
    );
    assert.equal(
      await animation.getByTestId("identity-lesson-step").innerText(),
      "得到两个参数条件",
    );
    assert.match(
      await animation.locator(".edu-identity-formula").innerText(),
      /m.*5.*0.*n.*8.*0/s,
    );
    await page.screenshot({
      path: fileURLToPath(
        new URL("../.local/reports/identity-animation-complete.png", import.meta.url),
      ),
    });
  });
  await check(
    "next_and_previous_show_complete_neighboring_probe_steps",
    async () => {
      await animation
        .getByRole("button", { name: "重置动画", exact: true })
        .click();
      await animation
        .getByRole("button", { name: "演示下一步", exact: true })
        .click();
      await page.waitForFunction(
        () =>
          document
            .querySelector("[data-identity-probe]")
            ?.getAttribute("data-identity-probe") === "0",
      );
      await animation
        .getByRole("button", { name: "播放动画", exact: true })
        .waitFor();
      assert.equal(
        await animation.getByTestId("identity-lesson-step").innerText(),
        "先用x=0检验",
      );
      await animation
        .getByRole("button", { name: "演示下一步", exact: true })
        .click();
      await page.waitForFunction(
        () =>
          document
            .querySelector("[data-identity-probe]")
            ?.getAttribute("data-identity-probe") === "1",
      );
      await animation
        .getByRole("button", { name: "播放动画", exact: true })
        .waitFor();
      await animation
        .getByRole("button", { name: "演示上一步", exact: true })
        .click();
      await page.waitForFunction(
        () =>
          document
            .querySelector("[data-identity-probe]")
            ?.getAttribute("data-identity-probe") === "0",
      );
      await animation
        .getByRole("button", { name: "播放动画", exact: true })
        .waitFor();
    },
  );
  await check("zoom_and_pause_share_the_same_progress", async () => {
    await page.getByRole("button", { name: "放大图示", exact: true }).click();
    const dialog = page.getByRole("dialog");
    await dialog
      .locator('[data-teaching-animation="identity_probe"]')
      .waitFor();
    const values = await page
      .locator('[data-teaching-animation="identity_probe"]')
      .evaluateAll((nodes) =>
        nodes.map((n) => n.getAttribute("data-animation-progress")),
      );
    assert.equal(new Set(values).size, 1);
    await dialog.getByRole("button", { name: "播放动画", exact: true }).click();
    await dialog.getByRole("button", { name: "暂停动画", exact: true }).click();
    const paused = await page
      .locator('[data-teaching-animation="identity_probe"]')
      .evaluateAll((nodes) =>
        nodes.map((n) => n.getAttribute("data-animation-progress")),
      );
    assert.equal(new Set(paused).size, 1);
    await page.keyboard.press("Escape");
  });
  await check(
    "refresh_replays_same_figure_and_both_themes_remain_readable",
    async () => {
      await page.reload();
      await animation.waitFor();
      const detail = await (
        await page.request.get(
          setup.base + "/api/session?id=" + assignment.session,
        )
      ).json();
      assert(
        detail.messages.some(
          (m) => m.response?.visuals?.[0]?.id === response.visuals[0].id,
        ),
      );
      for (const theme of ["light", "dark"]) {
        const desired = theme === "light" ? "切换浅色主题" : "切换深色主题";
        const opposite = theme === "light" ? "切换深色主题" : "切换浅色主题";
        if (
          await page.getByRole("button", { name: desired, exact: true }).count()
        )
          await page
            .getByRole("button", { name: desired, exact: true })
            .click();
        await page
          .getByRole("button", { name: opposite, exact: true })
          .waitFor();
        assert.equal(await animation.locator(".katex-error").count(), 0);
        await animation.locator(".edu-identity-lesson").screenshot({
          path: fileURLToPath(
            new URL(
              `../.local/reports/identity-animation-${theme}.png`,
              import.meta.url,
            ),
          ),
        });
      }
    },
  );
  await check(
    "mobile_and_reduced_motion_keep_manual_steps_usable",
    async () => {
      await page.setViewportSize({ width: 390, height: 844 });
      await page.emulateMedia({ reducedMotion: "reduce" });
      await animation
        .getByRole("button", { name: "播放动画", exact: true })
        .waitFor();
      assert.equal(
        await animation
          .getByRole("button", { name: "播放动画", exact: true })
          .isEnabled(),
        false,
      );
      await animation
        .getByRole("button", { name: "演示下一步", exact: true })
        .click();
      assert.equal(
        await animation.getByTestId("identity-lesson-step").innerText(),
        "先用x=0检验",
      );
      assert(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      );
      assert.equal(await animation.locator(".katex-error").count(), 0);
      assert.deepEqual(errors, []);
      const learning = await (
        await page.request.get(setup.base + "/api/learning")
      ).json();
      assert.equal(learning.summary.attempts, 0);
      await page.screenshot({
        path: fileURLToPath(
          new URL("../.local/reports/identity-animation-mobile.png", import.meta.url),
        ),
      });
    },
  );
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.emulateMedia({ reducedMotion: "no-preference" });
  const send = async (question) => {
    await page.locator("#edu-question").fill(question);
    const response = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "发送学习问题", exact: true })
      .click();
    const result = await response;
    assert.equal(result.status(), 200);
    return (await result.json()).response;
  };
  const storyResponse = await send("你不能创建情景故事来教学吗");
  const story = page
    .locator('[data-teaching-animation="identity_probe"]')
    .filter({ has: page.getByTestId("story-recorders") })
    .last();
  await check(
    "reported_story_changes_the_actual_figure_and_keeps_question",
    async () => {
      assert.equal(storyResponse.teaching_action, "explain");
      await story.getByTestId("story-recorders").waitFor();
      await page
        .getByRole("region", { name: "正在讨论的题目", exact: true })
        .waitFor();
      assert.match(await story.innerText(), /蓝色记录器[\s\S]*紫色记录器/);
      assert.match(await story.innerText(), /负数或分数/);
      assert.equal(await story.locator(".katex-error").count(), 0);
    },
  );
  await check(
    "story_steps_change_both_original_equation_accounts",
    async () => {
      await story
        .getByRole("button", { name: "演示下一步", exact: true })
        .click();
      await story
        .getByRole("button", { name: "播放动画", exact: true })
        .waitFor();
      assert.match(
        await story.getByTestId("story-account-0").innerText(),
        /[−-]8/,
      );
      assert.match(await story.getByTestId("story-account-1").innerText(), /n/);
      await story
        .getByRole("button", { name: "演示下一步", exact: true })
        .click();
      await story
        .getByRole("button", { name: "播放动画", exact: true })
        .waitFor();
      assert.match(
        await story.getByTestId("story-account-0").innerText(),
        /m.*8/s,
      );
      assert.match(
        await story.getByTestId("story-account-1").innerText(),
        /n.*5/s,
      );
      await story
        .locator(".edu-identity-lesson")
        .screenshot({
          path: fileURLToPath(
            new URL("../.local/reports/story-context-desktop.png", import.meta.url),
          ),
        });
    },
  );
  await check("story_play_runs_through_all_remaining_steps", async () => {
    await story.getByRole("button", { name: "重置动画", exact: true }).click();
    await story.getByRole("button", { name: "播放动画", exact: true }).click();
    await page.waitForFunction(
      () =>
        [
          ...document.querySelectorAll(
            '[data-teaching-animation="identity_probe"]',
          ),
        ]
          .filter((n) => n.querySelector('[data-testid="story-recorders"]'))
          .at(-1)
          ?.getAttribute("data-animation-progress") === "1",
      null,
      { timeout: 25000 },
    );
    assert.equal(
      await story.getByTestId("identity-lesson-step").innerText(),
      "把故事转回两个数学条件",
    );
  });
  await check(
    "screenshot_previous_problem_correction_continues_story_without_clarifying",
    async () => {
      const followed = await send("题目就是上一个题目");
      assert.equal(followed.teaching_action, "explain");
      assert.match(followed.text, /积分/);
      assert.equal(followed.visuals?.length ?? 0, 0);
      await page
        .getByRole("region", { name: "正在讨论的题目", exact: true })
        .waitFor();
      assert.equal(
        await page
          .getByText("请说一下你想理解的数学概念，或贴出题目和卡住的一步。", {
            exact: true,
          })
          .count(),
        0,
      );
    },
  );
  await check(
    "story_refresh_zoom_themes_and_mobile_preserve_the_resource",
    async () => {
      await page.reload();
      await story.getByTestId("story-recorders").waitFor();
      const detail = await (
        await page.request.get(
          setup.base + "/api/session?id=" + assignment.session,
        )
      ).json();
      assert.equal(detail.practice.id, assignment.id);
      assert(
        detail.messages.some(
          (m) => m.response?.visuals?.[0]?.id === storyResponse.visuals[0].id,
        ),
      );
      const card = page
        .locator(".edu-teaching-card")
        .filter({ has: page.getByTestId("story-recorders") })
        .last();
      await card.getByRole("button", { name: "放大图示", exact: true }).click();
      await page.getByRole("dialog").getByTestId("story-recorders").waitFor();
      const progress = await page
        .getByTestId("story-recorders")
        .evaluateAll((nodes) =>
          nodes.map((n) =>
            n
              .closest("[data-teaching-animation]")
              ?.getAttribute("data-animation-progress"),
          ),
        );
      assert.equal(new Set(progress).size, 1);
      await page.keyboard.press("Escape");
      await page.getByRole("dialog").waitFor({ state: "hidden" });
      for (const theme of ["light", "dark"]) {
        const toggle = page.getByRole("button", {
          name: theme === "light" ? "切换浅色主题" : "切换深色主题",
          exact: true,
        });
        if (await toggle.count()) await toggle.click();
        await page.getByRole("button", { name: theme === "light" ? "切换深色主题" : "切换浅色主题", exact: true }).waitFor();
        await story.getByTestId("story-recorders").waitFor();
        await story.scrollIntoViewIfNeeded();
        await page.screenshot({
            animations: "disabled",
            path: fileURLToPath(
              new URL(`../.local/reports/story-context-${theme}.png`, import.meta.url),
            ),
          });
      }
      await page.setViewportSize({ width: 390, height: 844 });
      assert(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      );
      assert.equal(await story.locator(".katex-error").count(), 0);
      await story.scrollIntoViewIfNeeded();
      await page.screenshot({
          animations: "disabled",
          path: fileURLToPath(
            new URL("../.local/reports/story-context-mobile.png", import.meta.url),
          ),
        });
      assert.deepEqual(errors, []);
      assert.equal(
        (await (await page.request.get(setup.base + "/api/learning")).json())
          .summary.attempts,
        0,
      );
    },
  );
  await writeFile(
    new URL(
      "../.local/reports/identity-animation-browser.local.json",
      import.meta.url,
    ),
    JSON.stringify({ passed: checks.length, checks, isolated: true }, null, 2),
  );
} finally {
  await browser?.close();
  child.stdin.end();
}
