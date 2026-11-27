import { Button } from "@zcode/ui/button";
import { RefreshCw, Square } from "lucide-react";
import type { ComponentProps } from "react";
import type { Message } from "./contract.js";
import { TutorIncompleteResponse } from "./tutor-extras.js";
import { retryBlocked } from "./format.js";

export function TurnStatus({
  item,
  busy,
  stopping,
  theme,
  onStop,
  onResume,
  onRestart,
}: {
  item: Message;
  busy: boolean;
  stopping: boolean;
  theme: ComponentProps<typeof TutorIncompleteResponse>["theme"];
  onStop: () => void;
  onResume: () => void;
  onRestart: () => void;
}) {
  const code = item.trace.error_code;
  const text =
    code === "turn_cancelled"
      ? "本轮生成已停止，原问题与未完成文字已保留。"
      : item.trace.running
        ? "本轮正在生成，可停止或等待完成。"
        : code === "model_truncated"
          ? "本轮输出预算已用完，可保留原题和标注重新回答。"
          : code === "model_protocol"
            ? "模型回复格式异常，原输入已保留，可以修改后重新提问。"
            : retryBlocked(code)
              ? "此请求已停止，记录已保留。模型结果无法安全重发，可以开始新的学习问题。"
              : "此请求尚未完成，可使用原输入与请求编号继续。";
  return (
    <div className="mt-3 text-ui-sm text-foreground-subtle">
      <TutorIncompleteResponse theme={theme} content={item.partial_response} />
      <p>{text}</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {item.trace.running && (
          <Button
            variant="outline"
            size="sm"
            disabled={busy || stopping}
            onClick={onStop}
          >
            <Square />
            停止这轮生成
          </Button>
        )}
        {!item.trace.running && !retryBlocked(code) && (
          <Button
            variant="outline"
            size="sm"
            disabled={busy}
            onClick={onResume}
          >
            <RefreshCw />
            继续此请求
          </Button>
        )}
        {["model_truncated", "turn_cancelled"].includes(code || "") && (
          <Button
            variant="outline"
            size="sm"
            disabled={busy}
            onClick={onRestart}
          >
            <RefreshCw />
            重新回答
          </Button>
        )}
      </div>
    </div>
  );
}
