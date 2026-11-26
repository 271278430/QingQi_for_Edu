import { build } from "esbuild";
import { fileURLToPath } from "node:url";
import { randomUUID } from "node:crypto";
import { mkdir, rename, unlink, writeFile } from "node:fs/promises";
import { dirname } from "node:path";
import { setTimeout as sleep } from "node:timers/promises";

async function publishFile(temporary, target) {
  const delays = [50, 100, 200, 400];
  for (let attempt = 0; ; attempt++) {
    try {
      await rename(temporary, target);
      return;
    } catch (error) {
      // Windows 读者可能暂时占用入口；沿 ZCode atomicFileUtils 的发布边界有限重试，不删除旧入口。
      if (
        process.platform !== "win32" ||
        !["EPERM", "EBUSY", "EACCES"].includes(error.code) ||
        attempt >= delays.length
      )
        throw error;
      await sleep(delays[attempt]);
    }
  }
}

// 公共能力从同一源码构建，消除逐轮 TS 加载；不注册或执行被裁剪的 Coding 工具。
const result = await build({
  entryPoints: ["server", "index", "contract", "model-options"].map((name) =>
    fileURLToPath(new URL(`./src/${name}.ts`, import.meta.url)),
  ),
  outdir: fileURLToPath(new URL("./dist/", import.meta.url)),
  bundle: true,
  write: false,
  format: "esm",
  platform: "node",
  target: "node24",
  treeShaking: true,
  // 沿用上游 Node 打包边界，原生扩展与浏览器/TUI 能力不嵌入教育产物。
  external: [
    "@zcode/tui",
    "playwright-core",
    "koffi",
    "@napi-rs/keyring",
    "typescript",
  ],
  banner: {
    js: "import { createRequire as runtimeCreateRequire } from 'node:module'; const require = runtimeCreateRequire(import.meta.url);",
  },
  logLevel: "warning",
});

for (const file of result.outputFiles) {
  await mkdir(dirname(file.path), { recursive: true });
  const temporary = `${file.path}.${randomUUID()}.tmp`;
  try {
    // 重构建会与每轮启动同时发生；完整写入后原子替换，避免读取半个入口文件。
    await writeFile(temporary, file.contents);
    await publishFile(temporary, file.path);
  } finally {
    await unlink(temporary).catch((error) => {
      if (error.code !== "ENOENT") throw error;
    });
  }
}
