import { useEffect, useLayoutEffect, useRef, useState, type PointerEvent } from "react";
import { Button } from "@zcode/ui/button";
import { Input } from "@zcode/ui/input";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@zcode/ui/dialog";
import {
  Pencil,
  Minus,
  Circle,
  Type,
  Undo2,
  Redo2,
  Trash2,
  Send,
  LoaderCircle,
} from "lucide-react";

type Tool = "pen" | "line" | "circle" | "text";
type Point = { x: number; y: number };
type Stroke = { tool: Tool; color: string; points: Point[]; text: string };
export type VisualReference = { run_id: number; visual_index: number };
export type AnnotatedImage = { file: File; reference: VisualReference };

function loadImage(url: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error("教学图快照无法读取，请关闭后重试。"));
    img.src = url;
  });
}

/** Freeze the currently visible SVG frame and inline its actual ZCode theme styles. */
export async function snapshotVisual(root: HTMLElement): Promise<string> {
  const candidates = [...root.querySelectorAll("svg")].filter((node) => {
    const box = node.getBoundingClientRect();
    return box.width > 80 && box.height > 60;
  });
  const figures = candidates.filter(
    (node) => !candidates.some((parent) => parent !== node && parent.contains(node)),
  );
  if (!figures.length) {
    const chart = root.querySelector("canvas");
    if (chart && chart.width && chart.height) return chart.toDataURL("image/png");
    throw new Error("图示尚未加载完成，请稍后再标注。");
  }
  if (figures.length === 1) return snapshotSvg(figures[0], root);
  // 多幅曲线属于同一张推理图，必须完整合成；取最大SVG会丢失另一项或另一种情形。
  const boxes = figures.map((svg) => svg.getBoundingClientRect());
  const left = Math.min(...boxes.map((box) => box.left)),
    top = Math.min(...boxes.map((box) => box.top));
  const width = Math.max(...boxes.map((box) => box.right)) - left,
    height = Math.max(...boxes.map((box) => box.bottom)) - top;
  const scale = Math.min(2, 1600 / width, 2400 / height);
  const canvas = document.createElement("canvas");
  canvas.width = Math.ceil(width * scale);
  canvas.height = Math.ceil(height * scale);
  const context = canvas.getContext("2d");
  if (!context) throw new Error("当前浏览器无法创建画布。");
  context.fillStyle = getComputedStyle(root.closest(".edu-teaching-card") || root).backgroundColor;
  context.fillRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < figures.length; i++) {
    const picture = await loadImage(await snapshotSvg(figures[i], root));
    const box = boxes[i];
    context.drawImage(
      picture,
      (box.left - left) * scale,
      (box.top - top) * scale,
      box.width * scale,
      box.height * scale,
    );
  }
  return canvas.toDataURL("image/png");
}

async function snapshotSvg(svg: SVGSVGElement, root: HTMLElement): Promise<string> {
  const clone = svg.cloneNode(true) as SVGSVGElement;
  const nodes = [svg, ...svg.querySelectorAll("*")];
  const copies = [clone, ...clone.querySelectorAll("*")];
  const properties = [
    "fill",
    "stroke",
    "stroke-width",
    "stroke-dasharray",
    "opacity",
    "font-family",
    "font-size",
    "font-weight",
    "color",
    "text-anchor",
  ];
  nodes.forEach((node, i) => {
    const styles = getComputedStyle(node);
    properties.forEach((property) =>
      (copies[i] as SVGElement).style.setProperty(property, styles.getPropertyValue(property)),
    );
  });
  // Mermaid的HTML标签转成纯SVG文字，避免foreignObject让导出的画布不可读取。
  clone.querySelectorAll("foreignObject").forEach((node) => {
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    const width = Number(node.getAttribute("width")) || 160,
      height = Number(node.getAttribute("height")) || 30;
    text.setAttribute("x", String((Number(node.getAttribute("x")) || 0) + width / 2));
    text.setAttribute("y", String((Number(node.getAttribute("y")) || 0) + height / 2));
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("dominant-baseline", "middle");
    text.setAttribute("fill", getComputedStyle(root).color);
    text.textContent = (node.textContent || "").trim().slice(0, 180);
    node.replaceWith(text);
  });
  const box = svg.viewBox.baseVal;
  const width = box.width || svg.clientWidth,
    height = box.height || svg.clientHeight;
  if (!width || !height) throw new Error("图示尚未完成布局，请稍后重试。");
  clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  clone.setAttribute("width", String(width));
  clone.setAttribute("height", String(height));
  // 学生端CSP只允许本机/data图片；快照使用同一data通道，不放宽为任意blob或外部地址。
  const url =
    "data:image/svg+xml;charset=utf-8," +
    encodeURIComponent(new XMLSerializer().serializeToString(clone));
  const image = await loadImage(url);
  const canvas = document.createElement("canvas");
  canvas.width = Math.min(1600, Math.ceil(width * 2));
  canvas.height = Math.ceil((height * canvas.width) / width);
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("当前浏览器无法创建画布。");
  // 主题颜色可由CSS Color 4表达，不能靠rgb字符串猜深色，否则白色标签会落到白底。
  const background = getComputedStyle(root.closest(".edu-teaching-card") || root).backgroundColor;
  ctx.fillStyle =
    background !== "rgba(0, 0, 0, 0)" && background !== "transparent"
      ? background
      : document.documentElement.classList.contains("dark")
        ? "#202020"
        : "#ffffff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL("image/png");
}

function paint(ctx: CanvasRenderingContext2D, stroke: Stroke) {
  const start = stroke.points[0],
    end = stroke.points[stroke.points.length - 1];
  if (!start) return;
  ctx.strokeStyle = stroke.color;
  ctx.fillStyle = stroke.color;
  ctx.lineWidth = Math.max(4, ctx.canvas.width / 240);
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.beginPath();
  if (stroke.tool === "text") {
    ctx.font = `${Math.max(30, ctx.canvas.width / 30)}px sans-serif`;
    ctx.fillText(stroke.text, start.x, start.y);
  } else if (stroke.tool === "circle") {
    ctx.ellipse(
      (start.x + end.x) / 2,
      (start.y + end.y) / 2,
      Math.max(1, Math.abs(end.x - start.x) / 2),
      Math.max(1, Math.abs(end.y - start.y) / 2),
      0,
      0,
      2 * Math.PI,
    );
    ctx.stroke();
  } else {
    ctx.moveTo(start.x, start.y);
    (stroke.tool === "line" ? [end] : stroke.points.slice(1)).forEach((p) => ctx.lineTo(p.x, p.y));
    ctx.stroke();
  }
}

function repaint(
  canvas: HTMLCanvasElement,
  image: HTMLImageElement,
  strokes: Stroke[],
  draft?: Stroke,
) {
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(image, 0, 0);
  strokes.forEach((stroke) => paint(ctx, stroke));
  if (draft) paint(ctx, draft);
}

export function VisualAnnotation({
  snapshot,
  title,
  reference,
  onClose,
  onReturn,
}: {
  snapshot: string;
  title: string;
  reference: VisualReference;
  onClose: () => void;
  onReturn: (image: AnnotatedImage) => Promise<void>;
}) {
  const canvas = useRef<HTMLCanvasElement>(null);
  const [image, setImage] = useState<HTMLImageElement>();
  const [tool, setTool] = useState<Tool>("pen");
  const [color, setColor] = useState("#ef4444");
  const [text, setText] = useState("?");
  const [history, setHistory] = useState<{
    strokes: Stroke[];
    undone: Stroke[];
    draft?: Stroke;
  }>({ strokes: [], undone: [] });
  // 草稿和提交笔迹使用同一状态队列，快速move/up批处理也能提交最后完整的一笔。
  const draft = history.draft;
  const activePointer = useRef<number | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const alive = useRef(true);
  useEffect(() => {
    alive.current = true;
    void loadImage(snapshot)
      .then((value) => {
        if (alive.current) setImage(value);
      })
      .catch((e) => {
        if (alive.current) setError(e.message);
      });
    return () => {
      alive.current = false;
      activePointer.current = null;
    };
  }, [snapshot]);
  useLayoutEffect(() => {
    const target = canvas.current;
    if (!target || !image) return;
    // 高频移动只在浏览器帧重绘，避免每个事件都擦除、重画整张教学图。
    const frame = requestAnimationFrame(() => repaint(target, image, history.strokes, draft));
    return () => cancelAnimationFrame(frame);
  }, [image, history.strokes, draft]);
  const point = (event: PointerEvent<HTMLCanvasElement>): Point | undefined => {
    const target = event.currentTarget,
      box = target.getBoundingClientRect();
    if (box.width <= 0 || box.height <= 0) return;
    return {
      x: Math.max(
        0,
        Math.min(target.width, ((event.clientX - box.left) * target.width) / box.width),
      ),
      y: Math.max(
        0,
        Math.min(target.height, ((event.clientY - box.top) * target.height) / box.height),
      ),
    };
  };
  const finish = (event: PointerEvent<HTMLCanvasElement>, cancelled = false) => {
    if (activePointer.current !== event.pointerId) return;
    // currentTarget在事件回调结束后会被React清空，必须先取坐标，再进入延迟状态更新。
    const end = cancelled ? undefined : point(event);
    activePointer.current = null;
    if (event.currentTarget.hasPointerCapture(event.pointerId))
      event.currentTarget.releasePointerCapture(event.pointerId);
    setHistory((h) => {
      if (!h.draft) return h;
      if (cancelled) return { ...h, draft: undefined };
      const stroke = h.draft;
      const last = end || stroke.points[stroke.points.length - 1];
      return {
        strokes: [
          ...h.strokes,
          {
            ...stroke,
            points: stroke.tool === "pen" ? [...stroke.points, last] : [stroke.points[0], last],
          },
        ],
        undone: [],
      };
    });
  };
  const send = async () => {
    if (busy || !canvas.current || !image || draft || !history.strokes.length) return;
    setBusy(true);
    setError("");
    try {
      // 最后一帧可能尚未绘制；导出前同步刷新，不能漏掉刚抬笔或刚撤销的内容。
      repaint(canvas.current, image, history.strokes);
      const blob = await new Promise<Blob>((resolve, reject) =>
        canvas.current!.toBlob(
          (b) => (b ? resolve(b) : reject(new Error("标注图片导出失败，笔迹已保留。"))),
          "image/png",
        ),
      );
      await onReturn({
        file: new File([blob], `标注-${title.slice(0, 36)}.png`, {
          type: "image/png",
        }),
        reference,
      });
      if (alive.current) onClose();
    } catch (e) {
      if (alive.current) setError(e instanceof Error ? e.message : "返回对话失败，笔迹已保留。");
    } finally {
      if (alive.current) setBusy(false);
    }
  };
  const tools: { value: Tool; label: string; Icon: typeof Pencil }[] = [
    { value: "pen", label: "画笔", Icon: Pencil },
    { value: "line", label: "直线", Icon: Minus },
    { value: "circle", label: "圈选", Icon: Circle },
    { value: "text", label: "文字标记", Icon: Type },
  ];
  return (
    <Dialog
      open
      onOpenChange={(open) => {
        if (!open && !busy) onClose();
      }}
    >
      <DialogContent
        className="sm:max-w-4xl max-h-[92dvh] overflow-auto"
        onInteractOutside={(e) => {
          if (busy) e.preventDefault();
        }}
      >
        <DialogHeader>
          <DialogTitle>标注教学图</DialogTitle>
          <DialogDescription>
            在当前画面上画线、圈选或标记。返回后附加到输入框，发送时与原题一起讨论。
          </DialogDescription>
        </DialogHeader>
        <div role="toolbar" aria-label="图示标注工具" className="flex flex-wrap items-center gap-2">
          {tools.map(({ value, label, Icon }) => (
            <Button
              key={value}
              size="sm"
              variant={tool === value ? "default" : "outline"}
              aria-pressed={tool === value}
              disabled={busy}
              onClick={() => setTool(value)}
            >
              <Icon className="size-4" />
              {label}
            </Button>
          ))}
          <label className="text-ui-xs flex gap-1 items-center">
            颜色
            <input
              aria-label="画笔颜色"
              type="color"
              value={color}
              disabled={busy}
              onChange={(e) => setColor(e.target.value)}
            />
          </label>
          {tool === "text" && (
            <Input
              aria-label="标记文字"
              className="w-28"
              maxLength={40}
              value={text}
              disabled={busy}
              onChange={(e) => setText(e.target.value)}
            />
          )}
          <Button
            size="icon-sm"
            variant="ghost"
            aria-label="撤销标注"
            disabled={busy || !history.strokes.length}
            onClick={() =>
              setHistory((h) => ({
                strokes: h.strokes.slice(0, -1),
                undone: [...h.undone, h.strokes[h.strokes.length - 1]],
              }))
            }
          >
            <Undo2 className="size-4" />
          </Button>
          <Button
            size="icon-sm"
            variant="ghost"
            aria-label="重做标注"
            disabled={busy || !history.undone.length}
            onClick={() =>
              setHistory((h) => ({
                strokes: [...h.strokes, h.undone[h.undone.length - 1]],
                undone: h.undone.slice(0, -1),
              }))
            }
          >
            <Redo2 className="size-4" />
          </Button>
          <Button
            size="icon-sm"
            variant="ghost"
            aria-label="清空标注"
            disabled={busy || !history.strokes.length}
            onClick={() => setHistory({ strokes: [], undone: [] })}
          >
            <Trash2 className="size-4" />
          </Button>
        </div>
        {error && (
          <p role="alert" className="text-ui-sm text-danger">
            {error}
          </p>
        )}
        {!image ? (
          <p className="text-ui-sm">正在准备画布…</p>
        ) : (
          <canvas
            ref={canvas}
            width={image.width}
            height={image.height}
            data-annotation-canvas
            data-strokes={history.strokes.length}
            data-draft-points={draft?.points.length || 0}
            className="w-full rounded border border-border touch-none"
            style={{ cursor: tool === "text" ? "text" : "crosshair" }}
            aria-label="教学图标注画布"
            onPointerDown={(event) => {
              if (
                busy ||
                history.strokes.length >= 120 ||
                activePointer.current !== null ||
                !event.isPrimary ||
                event.button !== 0
              )
                return;
              const start = point(event);
              if (!start) return;
              event.preventDefault();
              const stroke = {
                tool,
                color,
                text: text.trim() || "?",
                points: [start],
              };
              if (tool === "text")
                setHistory((h) => ({
                  strokes: [...h.strokes, stroke],
                  undone: [],
                }));
              else {
                event.currentTarget.setPointerCapture(event.pointerId);
                activePointer.current = event.pointerId;
                setHistory((h) => ({ ...h, draft: stroke }));
              }
            }}
            onPointerMove={(event) => {
              if (busy || activePointer.current !== event.pointerId) return;
              // 只捕获普通坐标值；不能把合成事件带进setState函数。
              const next = point(event);
              if (!next) return;
              setHistory((h) =>
                h.draft
                  ? {
                      ...h,
                      draft: {
                        ...h.draft,
                        points:
                          h.draft.tool === "pen"
                            ? [
                                ...(h.draft.points.length >= 300
                                  ? h.draft.points.filter((_p, index) => index % 2 === 0)
                                  : h.draft.points),
                                next,
                              ]
                            : [h.draft.points[0], next],
                      },
                    }
                  : h,
              );
            }}
            onPointerUp={(event) => finish(event)}
            onPointerCancel={(event) => finish(event, true)}
            onLostPointerCapture={(event) => finish(event, true)}
          />
        )}
        <div className="flex justify-end gap-2">
          <Button variant="ghost" disabled={busy} onClick={onClose}>
            取消
          </Button>
          <Button
            disabled={busy || !image || !!draft || !history.strokes.length}
            onClick={() => void send()}
          >
            {busy ? <LoaderCircle className="size-4 animate-spin" /> : <Send className="size-4" />}
            返回对话
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
