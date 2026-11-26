// Current education acceptance inventory. Separate from paid inference and production checks.
import { spawn } from "node:child_process";
import { readFile, mkdir, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
const manifest = JSON.parse(
  await readFile(new URL("review_manifest.json", import.meta.url), "utf8"),
);
const reportDir = new URL("../.local/reports/full-review/", import.meta.url);
await mkdir(reportDir, { recursive: true });
const filter = process.argv[2];
const previous =
  filter === "--failed"
    ? JSON.parse(
        await readFile(
          new URL("../.local/reports/review-all.local.json", import.meta.url),
          "utf8",
        ),
      )
    : undefined;
const suites = manifest.suites.filter((s) =>
  previous
    ? !previous.suites.some((r) => r.script === s.script) ||
      previous.suites.some((r) => r.script === s.script && !r.passed)
    : !filter || s.script.includes(filter),
);
if (!suites.length) throw Error("No matching current suite");
const results = previous
  ? previous.suites.filter((r) => !suites.some((s) => s.script === r.script))
  : [];
let index = 0;
async function worker() {
  while (index < suites.length) {
    const suite = suites[index++];
    const began = Date.now();
    const outcome = await new Promise((resolve) => {
      const executable = suite.script.endsWith(".py")
        ? process.env.QINGQI_PYTHON
        : process.execPath;
      if (!executable)
        return resolve({ code: -1, log: "QINGQI_PYTHON is required" });
      const child = spawn(
        executable,
        [fileURLToPath(new URL(suite.script, import.meta.url))],
        {
          windowsHide: true,
          stdio: ["ignore", "pipe", "pipe"],
        },
      );
      let log = "";
      const append = (chunk) => {
        log = (log + chunk.toString()).slice(-400000);
      };
      child.stdout.on("data", append);
      child.stderr.on("data", append);
      const deadline = setTimeout(() => child.kill(), 300000);
      child.once("error", (e) => {
        clearTimeout(deadline);
        resolve({ code: -1, log: e.message });
      });
      child.once("exit", (code) => {
        clearTimeout(deadline);
        resolve({ code: code ?? -1, log });
      });
    });
    await writeFile(new URL(suite.script + ".log", reportDir), outcome.log);
    const result = {
      ...suite,
      passed: outcome.code === 0,
      exit_code: outcome.code,
      seconds: Math.round((Date.now() - began) / 100) / 10,
      named_checks: [...outcome.log.matchAll(/"name"\s*:/g)].length,
    };
    results.push(result);
    process.stdout.write(JSON.stringify(result) + "\n");
    await writeFile(
      new URL(
        "review-all.local.json",
        new URL("../.local/reports/", import.meta.url),
      ),
      JSON.stringify(
        {
          version: manifest.version,
          scope: manifest.scope,
          suites: results,
          complete:
            results.length ===
            (previous ? manifest.suites.length : suites.length),
          retry_history: previous?.suites.filter((r) => !r.passed),
        },
        null,
        2,
      ),
    );
  }
}
await Promise.all([worker(), worker(), worker()]);
process.stdout.write(
  JSON.stringify({
    suites: results.length,
    passed: results.filter((r) => r.passed).length,
    failed: results.filter((r) => !r.passed).map((r) => r.script),
    controlled_inference: true,
  }) + "\n",
);
if (results.some((r) => !r.passed)) process.exitCode = 1;
