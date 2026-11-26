// Observe live entry files during the complete build, including declaration generation.
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile, readdir, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../../", import.meta.url));
const outputs = ["server", "index", "contract"].map((name) =>
  fileURLToPath(new URL(`../runtime/dist/${name}.js`, import.meta.url)),
);
const digest = async (path) => createHash("sha256").update(await readFile(path)).digest("hex");
const before = await Promise.all(outputs.map(digest));
const child = spawn(process.execPath, ["tmp/pnpm10/package/bin/pnpm.cjs", "--dir", "education/runtime", "build"], {
  cwd: root, windowsHide: true, stdio: ["ignore", "pipe", "pipe"],
});
let completed = false, errors = "", reads = 0;
child.stderr.on("data", (value) => { errors += value; });
child.stdout.resume();
const done = new Promise((resolve, reject) => {
  child.once("error", reject);
  child.once("exit", (code) => { completed = true; resolve(code); });
});
try {
  while (!completed) {
    assert.deepEqual(await Promise.all(outputs.map(digest)), before, "build exposed an incomplete or intermediate executable");
    reads += outputs.length;
    await new Promise((resolve) => setTimeout(resolve, 40));
  }
  assert.equal(await done, 0, errors);
  assert(reads >= 3);
  const leftovers = (await readdir(fileURLToPath(new URL("../runtime/dist/", import.meta.url)))).filter((name) => /\.js\.[\da-f-]+\.tmp$/.test(name));
  assert.deepEqual(leftovers, []);
  const report = { passed: 3, concurrent_entry_reads: reads, complete_build: true, checks: ["public entries present", "no intermediate executables during build", "temporary outputs cleaned"] };
  await writeFile(fileURLToPath(new URL("../.local/reports/runtime-build-acceptance.json", import.meta.url)), JSON.stringify(report, null, 2));
  process.stdout.write(JSON.stringify(report) + "\n");
} finally {
  if (!completed) child.kill();
}
