import { createInterface } from "node:readline";
import { Frame, type HandlerRequest } from "./contract.js";
import { EducationRuntime, RuntimeError } from "./index.js";

const MAX_FRAME_BYTES = 512000;
const callbacks = new Map<
  number,
  { resolve: (value: unknown) => void; reject: (error: unknown) => void }
>();
let callbackId = 0;
const write = (value: unknown) => {
  const raw = JSON.stringify(value);
  if (Buffer.byteLength(raw) > MAX_FRAME_BYTES)
    throw new RuntimeError("output_too_large", "Runtime output exceeds bound");
  process.stdout.write(raw + "\n");
};
const runtime = new EducationRuntime(
  (request: HandlerRequest, signal?: AbortSignal) =>
    new Promise((resolve, reject) => {
      const id = ++callbackId;
      const abort = () => {
        callbacks.delete(id);
        // 本地符号计算与远程模型的结果未知语义不同，不能都显示为“专项模型超时”。
        const model = request.name.startsWith("worker_");
        reject(
          new RuntimeError(
            model ? "model_unknown" : "tool_timeout",
            model
              ? "专项模型结果未确认，已阻止静默重发。"
              : "教学图形计算超时，进度已保留，可继续当前请求。",
            !model,
          ),
        );
      };
      if (signal?.aborted) {
        abort();
        return;
      }
      signal?.addEventListener("abort", abort, { once: true });
      callbacks.set(id, {
        resolve: (value) => {
          signal?.removeEventListener("abort", abort);
          resolve(value);
        },
        reject: (error) => {
          signal?.removeEventListener("abort", abort);
          reject(error);
        },
      });
      write({ callback: id, ...request });
    }),
);
let active = false;
const lines = createInterface({ input: process.stdin, crlfDelay: Infinity });
lines.on("line", (line) => {
  void (async () => {
    let id: number | null = null;
    try {
      if (Buffer.byteLength(line) > MAX_FRAME_BYTES)
        throw new RuntimeError("invalid_input", "Frame too large");
      const value: unknown = JSON.parse(line);
      if (value && typeof value === "object" && "callback" in value) {
        const item = value as {
          callback: number;
          result?: unknown;
          error?: {
            code: string;
            message: string;
            recoverable?: boolean;
            retry_after?: number;
          };
        };
        const pending = callbacks.get(item.callback);
        if (!pending) return;
        callbacks.delete(item.callback);
        if (item.error)
          pending.reject(
            new RuntimeError(
              item.error.code,
              item.error.message,
              item.error.recoverable,
              item.error.retry_after,
            ),
          );
        else pending.resolve(item.result);
        return;
      }
      const frame = Frame.parse(value);
      id = frame.id;
      if (active)
        throw new RuntimeError("busy", "Runtime command already active", true);
      active = true;
      try {
        write({ id, result: await runtime.dispatch(frame.op, frame.input) });
      } finally {
        active = false;
      }
    } catch (error) {
      write({
        id,
        error:
          error instanceof RuntimeError
            ? {
                code: error.code,
                message: error.message,
                recoverable: error.recoverable,
                retry_after: error.retry_after,
              }
            : {
                code: "runtime_invalid",
                message: "教育后台能力契约无效",
                recoverable: false,
              },
      });
    }
  })();
});
lines.on("close", () => {
  for (const item of callbacks.values())
    item.reject(new RuntimeError("closed", "Runtime closed"));
  void runtime.close().catch(() => {
    process.exitCode = 1;
  });
});
