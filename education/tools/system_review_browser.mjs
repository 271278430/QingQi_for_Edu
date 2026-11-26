// Review current interactions using the maintained browser scenarios.
// The old function_trace contract was replaced by source-bound reasoning lessons.
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { readFile, writeFile } from "node:fs/promises";
const scenarios = [
  ["problem_reasoning_browser.mjs", "problem-reasoning-browser.local.json"],
  ["interaction_inventory_browser.mjs", "interaction-inventory-browser.json"],
];
const results = [];
for (const [script, report] of scenarios) {
  await new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [fileURLToPath(new URL(script, import.meta.url))], {
      windowsHide: true,
      stdio: "inherit",
    });
    child.once("error", reject);
    child.once("exit", (code) => (code === 0 ? resolve() : reject(Error(`${script}: ${code}`))));
  });
  const data = JSON.parse(
    await readFile(new URL(`../.local/reports/${report}`, import.meta.url), "utf8"),
  );
  results.push({ scenario: script, passed: data.passed, report });
}
await writeFile(
  new URL("../.local/reports/system-review-browser.local.json", import.meta.url),
  JSON.stringify({ scenarios: results, isolated: true, real_inference: false }, null, 2),
);
