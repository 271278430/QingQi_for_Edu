import { Button } from "@zcode/ui/button";
import { ArrowUp, Square, LoaderCircle } from "lucide-react";

export function ComposerActions({
  canStop,
  stopping,
  disabled,
  onStop,
}: {
  canStop: boolean;
  stopping: boolean;
  disabled: boolean;
  onStop: () => void;
}) {
  return canStop ? (
    <Button
      type="button"
      size="lg"
      variant="secondary"
      className="shrink-0"
      disabled={stopping}
      aria-label="停止生成"
      onClick={onStop}
    >
      {stopping ? <LoaderCircle className="animate-spin" /> : <Square />}
      <span className="hidden sm:inline">{stopping ? "停止中" : "停止"}</span>
    </Button>
  ) : (
    <Button
      type="submit"
      size="lg"
      className="shrink-0"
      disabled={disabled}
      aria-label="发送学习问题"
    >
      <ArrowUp />
      发送
    </Button>
  );
}
