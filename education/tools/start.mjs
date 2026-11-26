import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
const service = fileURLToPath(new URL("../service/", import.meta.url));
const flash = process.argv.includes("--flash");
const demo = process.argv.includes("--demo");
const config = fileURLToPath(
  new URL(
    `../service/config/${flash ? "vision" : "models"}.local.json`,
    import.meta.url,
  ),
);
const accounts = fileURLToPath(
  new URL("../service/config/accounts.local.json", import.meta.url),
);
if (!demo && !existsSync(config)) {
  process.stderr.write(
    `Configure ${flash ? "vision" : "models"}.local.json first. See education/docs/operations.md.\n`,
  );
  process.exit(1);
}
// 完整模型入口复用既有隧道与凭据owner；不能只启动HTTP而漏建8B/27B连接。
const args = demo
  ? [
      fileURLToPath(new URL("./demo.py", import.meta.url)),
      "--port",
      process.env.QINGQI_PORT || "18774",
    ]
  : flash
    ? [
        "-m",
        "qingqi.product",
        "--port",
        process.env.QINGQI_PORT || "18774",
        "--origin",
        "http://127.0.0.1:18773",
        "--origin",
        "http://localhost:5173",
        "--origin",
        "http://127.0.0.1:5173",
      ]
    : [fileURLToPath(new URL("./run_models.py", import.meta.url))];
if (flash) {
  args.push("--config", config);
  if (existsSync(accounts)) args.push("--accounts", accounts);
}
// Windows复用双击启动器的PID归属和停止入口；CLI只启动，不再持有另一套常驻进程。
const windowsLauncher = process.platform === "win32" && !demo;
const launchArgs = windowsLauncher
  ? [
      "-NoProfile",
      "-ExecutionPolicy",
      "Bypass",
      "-File",
      fileURLToPath(new URL("./open-workspace.ps1", import.meta.url)),
      "-Mode",
      flash ? "flash" : "full",
      "-NoOpen",
    ]
  : args;
const child = spawn(
  windowsLauncher ? "powershell.exe" : process.env.QINGQI_PYTHON || "python",
  launchArgs,
  {
    cwd: service,
    env: {
      ...process.env,
      QINGQI_PORT: process.env.QINGQI_PORT || (flash ? "18774" : "18772"),
      PYTHONPATH: fileURLToPath(new URL("../service/src/", import.meta.url)),
      PYTHONIOENCODING: "utf-8",
    },
    stdio: "inherit",
    windowsHide: true,
    shell: false,
  },
);
child.on("error", () => {
  process.stderr.write(
    "Python 3.12+ required. Set QINGQI_PYTHON to its executable.\n",
  );
  process.exitCode = 1;
});
child.on("exit", (code) => {
  process.exitCode = code ?? 1;
});
if (!windowsLauncher) {
  process.on("SIGINT", () => child.kill());
  process.on("SIGTERM", () => child.kill());
}
