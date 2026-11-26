import type { EducationService, TeachingStreamEvent } from "./contract.js";
export class EducationRequestError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly status: number,
    public readonly recoverable: boolean,
    public readonly retryAfter?: number,
  ) {
    super(message);
  }
}
export function createEducationService(base = ""): EducationService {
  let csrf = "";
  const fetchResponse = async (
    path: string,
    options: RequestInit,
  ): Promise<Response> => {
    try {
      return await fetch(`${base}${path}`, options);
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") throw error;
      throw new EducationRequestError(
        "无法连接学习服务，请检查网络或服务是否启动。输入已保留。",
        "network_unavailable",
        0,
        true,
      );
    }
  };
  const responseJson = async (response: Response): Promise<unknown> => {
    try {
      const value: unknown = await response.json();
      if (!value || typeof value !== "object" || Array.isArray(value))
        throw new Error("invalid response object");
      return value;
    } catch {
      // 反向代理可能返回HTML；保留HTTP状态与未知写入语义，不能把解析异常当作可重新提交的新操作。
      throw new EducationRequestError(
        `服务暂时不可用（${response.status}），输入已保留，请重试。`,
        "invalid_response",
        response.ok ? 502 : response.status,
        true,
      );
    }
  };
  const request = async <T>(
    path: string,
    body?: unknown,
    signal?: AbortSignal,
  ): Promise<T> => {
    const response = await fetchResponse(path, {
      method: body === undefined ? "GET" : "POST",
      credentials: "include",
      signal,
      headers:
        body === undefined
          ? {}
          : { "Content-Type": "application/json", "X-Qingqi-CSRF": csrf },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    const value = await responseJson(response);
    if (!response.ok) {
      const error =
        value && typeof value === "object" && "message" in value
          ? String(value.message)
          : `请求失败（${response.status}）`;
      const fields =
        value && typeof value === "object"
          ? (value as Record<string, unknown>)
          : {};
      throw new EducationRequestError(
        error,
        String(fields.error ?? "request_failed"),
        response.status,
        fields.recoverable === true,
        typeof fields.retry_after === "number" ? fields.retry_after : undefined,
      );
    }
    return value as T;
  };
  return {
    get: (path, signal) => request(path, undefined, signal),
    post: (path, body) => request(path, body),
    stream: async <T>(
      path: string,
      body: unknown,
      onEvent: (event: TeachingStreamEvent) => void,
    ): Promise<T> => {
      const response = await fetchResponse(path, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-Qingqi-CSRF": csrf,
          Accept: "text/event-stream",
        },
        body: JSON.stringify(body),
      });
      if (
        !response.ok ||
        !response.headers.get("Content-Type")?.includes("text/event-stream")
      ) {
        const value = (await responseJson(response)) as Record<string, unknown>;
        if (!response.ok)
          throw new EducationRequestError(
            String(value.message || "请求失败"),
            String(value.error || "request_failed"),
            response.status,
            value.recoverable === true,
          );
        return value as T;
      }
      const reader = response.body?.getReader();
      if (!reader)
        throw new EducationRequestError(
          "回复流未建立，保留原请求后重试。",
          "stream_interrupted",
          409,
          true,
        );
      const decoder = new TextDecoder();
      let buffer = "",
        seq = 0,
        done = false;
      try {
        for (;;) {
          const piece = await reader.read();
          buffer += decoder.decode(piece.value, { stream: !piece.done });
          // SSE允许CRLF；也处理CR/LF分落在两次网络读取中的情况。
          buffer = buffer.replace(/\r\n/g, "\n");
          let index: number;
          while ((index = buffer.indexOf("\n\n")) >= 0) {
            const frame = buffer.slice(0, index);
            buffer = buffer.slice(index + 2);
            const data = frame
              .split("\n")
              .filter((line) => line.startsWith("data:"))
              .map((line) => line.slice(5).trimStart())
              .join("\n");
            if (!data) continue;
            const event = JSON.parse(data) as TeachingStreamEvent;
            if (
              event.seq !== seq + 1 ||
              ![
                "progress",
                "scope",
                "reset",
                "delta",
                "done",
                "error",
              ].includes(event.kind)
            )
              throw Error("invalid stream sequence");
            seq = event.seq;
            const requestId = (body as { request?: { request_id?: string } })
              ?.request?.request_id;
            if (requestId && event.request_id !== requestId)
              throw Error("stream request mismatch");
            if (event.kind === "error")
              throw new EducationRequestError(
                event.message || "本次辅导未完成",
                event.error || "request_failed",
                event.status || 502,
                event.recoverable === true,
              );
            onEvent(event);
            if (event.kind === "done") {
              done = true;
              return event.value as T;
            }
          }
          if (buffer.length > 2000000) throw Error("stream frame too large");
          if (piece.done) break;
        }
      } catch (error) {
        if (error instanceof EducationRequestError) throw error;
        throw new EducationRequestError(
          "回复连接中断，记录与输入已保留。可用原请求继续。",
          "stream_interrupted",
          409,
          true,
        );
      } finally {
        reader.releaseLock();
      }
      if (!done)
        throw new EducationRequestError(
          "回复尚未确认完成，记录与输入已保留。可用原请求继续。",
          "stream_interrupted",
          409,
          true,
        );
      throw Error("unreachable stream state");
    },
    setCsrf: (value) => {
      csrf = value;
    },
  };
}
