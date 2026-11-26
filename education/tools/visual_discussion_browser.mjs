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
  [fileURLToPath(new URL("./geometry_product_fixture.py", import.meta.url))],
  { windowsHide: true, stdio: ["ignore", "pipe", "pipe"] },
);
let errors = "",
  browser;
child.stderr.on("data", (v) => (errors += v));
const lines = createInterface({ input: child.stdout });
const checks = [];
const check = async (name, action) => {
  await action();
  checks.push({ name, passed: true });
  process.stdout.write(JSON.stringify(checks.at(-1)) + "\n");
};
try {
  const setup = await new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(Error(errors)), 30000);
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
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1000 },
  });
  const pageErrors = [];
  page.on("pageerror", (e) => pageErrors.push(e.message));
  const submissions = [];
  page.on("request", (r) => {
    if (r.url().endsWith("/api/teach") && r.method() === "POST")
      submissions.push(r.postDataJSON());
  });
  await page.goto(setup.base);
  await page.getByRole("heading", { name: "清启", exact: true }).waitFor();
  const send = async (question) => {
    if (question)
      await page.getByLabel("你的学习问题", { exact: true }).fill(question);
    const wait = page.waitForResponse(
      (r) => r.url().endsWith("/api/teach") && r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "发送学习问题", exact: true })
      .click();
    const response = await wait;
    const result = await readTeachResponse(response);
    await page.waitForFunction(
      () =>
        !document.querySelector("#edu-question").disabled &&
        document.querySelector("#edu-question").value === "",
    );
    return result;
  };
  await page.getByLabel("上传题目图片").setInputFiles(setup.image);
  await page.getByLabel("待发送图片").getByRole("img").waitFor();
  const first = await send("解这道题");
  await check(
    "default_socratic_diagram_uses_exact_coordinate_readout",
    async () => {
      assert.equal(first.response.teaching_action, "ask");
      await page
        .getByText("绘图坐标（精确形式）", { exact: true })
        .first()
        .click();
      const readout = page.locator("[data-coordinate-readout]").first();
      await readout.waitFor();
      const text = await readout.innerText();
      assert(text.includes("2"));
      assert(!/\d+\.\d{3,}/.test(text));
      assert((await readout.locator(".katex").count()) > 0);
      assert(
        (await readout.locator("annotation").allTextContents()).some((text) =>
          text.includes("\\sqrt"),
        ),
      );
    },
  );
  const open = async (
    card = page.getByRole("button", { name: "标注图示", exact: true }).first(),
  ) => {
    await card.click();
    try {
      await page.locator("[data-annotation-canvas]").waitFor({ timeout: 5000 });
    } catch (e) {
      console.error(
        JSON.stringify({
          alerts: await page.getByRole("alert").allTextContents(),
          pageErrors,
          dialogues: await page.getByRole("dialog").count(),
        }),
      );
      await page.screenshot({
        path: "education/.local/reports/annotation-failure.png",
      });
      throw e;
    }
  };
  const draw = async (tool) => {
    await page.getByRole("button", { name: tool, exact: true }).click();
    const box = await page.locator("[data-annotation-canvas]").boundingBox();
    await page.mouse.move(box.x + box.width * 0.3, box.y + box.height * 0.35);
    await page.mouse.down();
    await page.mouse.move(box.x + box.width * 0.5, box.y + box.height * 0.55, {
      steps: 6,
    });
    await page.mouse.move(box.x + box.width * 0.65, box.y + box.height * 0.35, {
      steps: 5,
    });
    await page.mouse.up();
  };
  await check("pen_line_circle_text_undo_redo_and_clear", async () => {
    await open();
    for (const tool of ["画笔", "直线", "圈选"]) await draw(tool);
    await page.getByRole("button", { name: "文字标记", exact: true }).click();
    await page.getByLabel("标记文字").fill("这条辅助线?");
    const box = await page.locator("[data-annotation-canvas]").boundingBox();
    await page.mouse.click(box.x + box.width * 0.4, box.y + box.height * 0.25);
    assert.equal(
      await page
        .locator("[data-annotation-canvas]")
        .getAttribute("data-strokes"),
      "4",
    );
    await page.getByRole("button", { name: "撤销标注" }).click();
    assert.equal(
      await page
        .locator("[data-annotation-canvas]")
        .getAttribute("data-strokes"),
      "3",
    );
    await page.getByRole("button", { name: "重做标注" }).click();
    assert.equal(
      await page
        .locator("[data-annotation-canvas]")
        .getAttribute("data-strokes"),
      "4",
    );
    await page.getByRole("button", { name: "清空标注" }).click();
    assert.equal(
      await page
        .locator("[data-annotation-canvas]")
        .getAttribute("data-strokes"),
      "0",
    );
    assert(
      await page
        .getByRole("button", { name: "返回对话", exact: true })
        .isDisabled(),
    );
  });
  await check(
    "batched_pointer_moves_do_not_crash_the_annotation_workspace",
    async () => {
      await page.getByRole("button", { name: "画笔", exact: true }).click();
      const box = await page.locator("[data-annotation-canvas]").boundingBox();
      await page.mouse.move(box.x + box.width * 0.2, box.y + box.height * 0.4);
      await page.mouse.down();
      await page.evaluate(() => {
        const canvas = document.querySelector("[data-annotation-canvas]");
        const box = canvas.getBoundingClientRect();
        for (let i = 0; i < 180; i++) {
          canvas.dispatchEvent(
            new PointerEvent("pointermove", {
              bubbles: true,
              pointerId: 1,
              pointerType: "mouse",
              isPrimary: true,
              buttons: 1,
              clientX: box.x + box.width * (0.2 + i / 400),
              clientY: box.y + box.height * (0.4 + 0.15 * Math.sin(i / 9)),
            }),
          );
        }
        canvas.dispatchEvent(
          new PointerEvent("pointerup", {
            bubbles: true,
            pointerId: 1,
            pointerType: "mouse",
            isPrimary: true,
            clientX: box.x + box.width * (0.2 + 179 / 400),
            clientY: box.y + box.height * (0.4 + 0.15 * Math.sin(179 / 9)),
          }),
        );
      });
      await page.mouse.up();
      await page.waitForTimeout(100);
      process.stdout.write(
        JSON.stringify({ batched_pointer_errors: pageErrors }) + "\n",
      );
      assert.deepEqual(pageErrors, []);
      assert.equal(
        await page
          .locator("[data-annotation-canvas]")
          .getAttribute("data-strokes"),
        "1",
      );
      const endpoint = await page
        .locator("[data-annotation-canvas]")
        .evaluate((c) => {
          const x = c.width * (0.2 + 179 / 400);
          const y = c.height * (0.4 + 0.15 * Math.sin(179 / 9));
          return [
            ...c
              .getContext("2d")
              .getImageData(Math.floor(x), Math.floor(y), 1, 1).data,
          ];
        });
      assert(
        endpoint[0] > 190 && endpoint[1] < 130 && endpoint[2] < 130,
        "rapid pointerup lost the final red endpoint",
      );
      await page.getByRole("button", { name: "清空标注" }).click();
    },
  );
  await check(
    "long_curve_cancel_and_capture_loss_keep_the_original_and_committed_marks",
    async () => {
      await page.getByRole("button", { name: "画笔", exact: true }).click();
      const canvas = page.locator("[data-annotation-canvas]");
      const box = await canvas.boundingBox();
      await page.mouse.move(box.x + box.width * 0.15, box.y + box.height * 0.3);
      await page.mouse.down();
      const measurements = await page.evaluate(async () => {
        const c = document.querySelector("[data-annotation-canvas]");
        const box = c.getBoundingClientRect();
        let paints = 0;
        const ctx = c.getContext("2d"),
          original = ctx.clearRect;
        ctx.clearRect = function (...args) {
          paints++;
          return original.apply(this, args);
        };
        for (let batch = 0; batch < 12; batch++) {
          for (let i = 0; i < 100; i++) {
            const t = (batch * 100 + i) / 1199;
            c.dispatchEvent(
              new PointerEvent("pointermove", {
                bubbles: true,
                pointerId: 1,
                pointerType: "mouse",
                isPrimary: true,
                buttons: 1,
                clientX: box.x + box.width * (0.15 + t * 0.7),
                clientY:
                  box.y + box.height * (0.3 + 0.15 * Math.sin(t * Math.PI * 8)),
              }),
            );
          }
          await new Promise((resolve) => requestAnimationFrame(resolve));
        }
        const points = Number(c.dataset.draftPoints);
        ctx.clearRect = original;
        return { paints, points };
      });
      assert(measurements.points > 100 && measurements.points <= 301);
      assert(
        measurements.paints <= 24,
        "pointer events caused unbounded whole-image repaints",
      );
      await page.mouse.up();
      await page.waitForTimeout(50);
      assert.equal(await canvas.getAttribute("data-strokes"), "1");
      const committed = await canvas.evaluate((c) => c.toDataURL());
      for (const interruption of ["cancel", "capture_loss"]) {
        await page.mouse.move(
          box.x + box.width * 0.4,
          box.y + box.height * 0.6,
        );
        await page.mouse.down();
        await page.mouse.move(
          box.x + box.width * 0.7,
          box.y + box.height * 0.7,
        );
        await canvas.evaluate((c, interruption) => {
          if (interruption === "cancel")
            c.dispatchEvent(
              new PointerEvent("pointercancel", {
                bubbles: true,
                pointerId: 1,
                pointerType: "mouse",
                isPrimary: true,
              }),
            );
          else c.releasePointerCapture(1);
        }, interruption);
        await page.mouse.move(
          box.x + box.width * 0.72,
          box.y + box.height * 0.7,
        );
        await page.mouse.up();
        await page.waitForTimeout(50);
        assert.equal(await canvas.getAttribute("data-strokes"), "1");
        assert.equal(await canvas.evaluate((c) => c.toDataURL()), committed);
      }
      process.stdout.write(
        JSON.stringify({ continuous_drawing: measurements, pageErrors }) + "\n",
      );
      assert.deepEqual(pageErrors, []);
      await page.getByRole("button", { name: "撤销标注" }).click();
      assert.equal(await canvas.getAttribute("data-strokes"), "0");
      await page.getByRole("button", { name: "重做标注" }).click();
      assert.equal(await canvas.getAttribute("data-strokes"), "1");
      await page.getByRole("button", { name: "清空标注" }).click();
    },
  );
  await check(
    "png_contains_original_diagram_and_visible_marks_without_model_call",
    async () => {
      await draw("直线");
      const count = submissions.length;
      const pixels = await page
        .locator("[data-annotation-canvas]")
        .evaluate((canvas) => {
          const data = canvas
            .getContext("2d")
            .getImageData(0, 0, canvas.width, canvas.height).data;
          let red = 0,
            blue = 0;
          for (let i = 0; i < data.length; i += 4) {
            if (data[i] > 190 && data[i + 1] < 130 && data[i + 2] < 130) red++;
            if (
              data[i + 2] > 120 &&
              data[i + 2] > data[i] + 40 &&
              data[i + 2] > data[i + 1] + 15
            )
              blue++;
          }
          return { red, blue };
        });
      process.stdout.write(
        JSON.stringify({ annotation_pixels: pixels }) + "\n",
      );
      await page.screenshot({
        path: "education/.local/reports/annotation-pixels.png",
      });
      assert(pixels.red > 100 && pixels.blue > 100);
      await page.screenshot({
        path: fileURLToPath(
          new URL(
            "../.local/reports/annotation-editor-desktop.png",
            import.meta.url,
          ),
        ),
      });
      await page.getByRole("button", { name: "返回对话", exact: true }).click();
      await page
        .locator("[data-annotation-canvas]")
        .waitFor({ state: "detached" });
      await page.getByLabel("待发送图片").getByRole("img").waitFor();
      assert.equal(submissions.length, count);
      const src = await page
        .getByLabel("待发送图片")
        .getByRole("img")
        .getAttribute("src");
      assert(src.startsWith("data:image/png;base64,"));
      await writeFile(
        "education/.local/reports/annotation-returned.png",
        Buffer.from(src.split(",")[1], "base64"),
      );
    },
  );
  await check(
    "annotated_png_is_sent_with_owned_original_problem_reference",
    async () => {
      const result = await send();
      assert.deepEqual(submissions.at(-1).request.visual_context, {
        run_id: first.response.run_id,
        visual_index: 0,
      });
      assert.equal(result.response.controller, "glm_vision_text_controller");
      assert.equal(result.response.teaching_action, "ask");
      assert(result.response.text.includes("标注"));
      assert.equal(result.session.messages.at(-1).images.length, 1);
      assert.equal(await page.getByRole("alert").count(), 0);
    },
  );
  await check(
    "animation_frame_can_be_paused_annotated_and_cancelled_on_mobile",
    async () => {
      const animated = await send("直接给第（1）问完整答案，并配合动画演示。");
      process.stdout.write(
        JSON.stringify({
          animation_response: {
            controller: animated.response.controller,
            visuals: animated.response.visuals?.map((v) => ({
              kind: v.kind,
              template: v.template,
            })),
          },
          visible_buttons: await page
            .locator("[data-teaching-visual]")
            .last()
            .getByRole("button")
            .allTextContents(),
        }) + "\n",
      );
      await page.screenshot({
        path: "education/.local/reports/animation-annotation-debug.png",
      });
      const card = page
        .locator('[data-teaching-visual="animation_scene"]')
        .last();
      await card
        .getByRole("button", { name: "演示下一步", exact: true })
        .click();
      await page.setViewportSize({ width: 390, height: 844 });
      await open(card.getByRole("button", { name: "标注图示", exact: true }));
      await draw("画笔");
      const mobileCanvas = page.locator("[data-annotation-canvas]");
      await mobileCanvas.scrollIntoViewIfNeeded();
      await mobileCanvas.evaluate((c) =>
        c.addEventListener(
          "pointerdown",
          (e) => {
            window.annotationTouchId = e.pointerId;
          },
          { once: true },
        ),
      );
      const touchBox = await mobileCanvas.boundingBox();
      const touch = await page.context().newCDPSession(page);
      await touch.send("Emulation.setTouchEmulationEnabled", { enabled: true });
      await touch.send("Input.dispatchTouchEvent", {
        type: "touchStart",
        touchPoints: [
          {
            x: touchBox.x + touchBox.width * 0.3,
            y: touchBox.y + touchBox.height * 0.4,
          },
        ],
      });
      await page.waitForFunction(() => window.annotationTouchId !== undefined);
      await mobileCanvas.evaluate((c) => {
        const box = c.getBoundingClientRect();
        for (let i = 0; i < 80; i++)
          c.dispatchEvent(
            new PointerEvent("pointermove", {
              bubbles: true,
              pointerId: window.annotationTouchId,
              pointerType: "touch",
              isPrimary: true,
              buttons: 1,
              clientX: box.x + box.width * (0.3 + i / 300),
              clientY: box.y + box.height * 0.4,
            }),
          );
        c.dispatchEvent(
          new PointerEvent("pointercancel", {
            bubbles: true,
            pointerId: window.annotationTouchId,
            pointerType: "touch",
            isPrimary: true,
          }),
        );
      });
      await touch.send("Input.dispatchTouchEvent", {
        type: "touchEnd",
        touchPoints: [],
      });
      await touch.detach();
      await page.waitForTimeout(50);
      assert.equal(await mobileCanvas.getAttribute("data-strokes"), "1");
      const before = await page
        .locator("[data-annotation-canvas]")
        .evaluate((c) => c.toDataURL());
      await page.waitForTimeout(200);
      assert.equal(
        await page
          .locator("[data-annotation-canvas]")
          .evaluate((c) => c.toDataURL()),
        before,
      );
      const box = await page.locator("[role=dialog]").boundingBox();
      assert(box.x >= 0 && box.x + box.width <= 392);
      await page.screenshot({
        path: fileURLToPath(
          new URL(
            "../.local/reports/annotation-editor-mobile.png",
            import.meta.url,
          ),
        ),
      });
      await page.getByRole("button", { name: "取消", exact: true }).click();
      assert.equal(await page.getByLabel("待发送图片").count(), 0);
    },
  );
  await check(
    "delayed_export_cannot_attach_to_a_newly_selected_session",
    async () => {
      await page.setViewportSize({ width: 1440, height: 1000 });
      await open();
      await draw("直线");
      // 延迟真实FileReader回调，再触发会话选择，核验旧闭包不会把附件写入新会话。
      await page.evaluate(() => {
        const original = FileReader.prototype.readAsDataURL;
        window.releaseAnnotationRead = undefined;
        FileReader.prototype.readAsDataURL = function (file) {
          FileReader.prototype.readAsDataURL = original;
          window.releaseAnnotationRead = () => original.call(this, file);
        };
      });
      await page.getByRole("button", { name: "返回对话", exact: true }).click();
      await page.waitForFunction(() => Boolean(window.releaseAnnotationRead));
      const selected = page.waitForResponse(
        (r) =>
          r.url().endsWith("/api/sessions") && r.request().method() === "POST",
      );
      await page
        .getByRole("button", {
          name: "新建学习对话",
          exact: true,
          includeHidden: true,
        })
        .evaluate((button) => button.click());
      await selected;
      await page.waitForFunction(
        () => !document.querySelector("#edu-question").disabled,
      );
      await page.evaluate(() => window.releaseAnnotationRead());
      await page.waitForTimeout(150);
      assert.equal(await page.getByLabel("待发送图片").count(), 0);
      assert.equal(
        await page.getByLabel("你的学习问题", { exact: true }).inputValue(),
        "",
      );
    },
  );
  assert.deepEqual(pageErrors, []);
  await writeFile(
    fileURLToPath(
      new URL(
        "../.local/reports/visual-discussion-browser.local.json",
        import.meta.url,
      ),
    ),
    JSON.stringify({ passed: checks.length, checks, pageErrors }, null, 2),
  );
} finally {
  await browser?.close();
  child.kill();
  lines.close();
}
