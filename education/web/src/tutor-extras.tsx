import { useEffect, useRef, useState, type ComponentProps } from "react";
import { Button } from "@zcode/ui/button";
import { Input } from "@zcode/ui/input";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@zcode/ui/dialog";
import { ImagePlus, History, LoaderCircle, Search } from "lucide-react";
import {
  createChatComposerAttachment,
  serializeChatComposerAttachment,
  revokeChatComposerAttachment,
} from "@zcode/ui/chat-attachments";
import {
  Attachments,
  Attachment,
  AttachmentPreview,
  AttachmentRemove,
} from "@zcode/ui/attachments";
import type { EducationService, HistoricalPractice } from "./contract.js";
import { MathContent } from "./learning-content.js";
import { errorText } from "./format.js";

export function TutorIncompleteResponse({
  content,
  theme,
}: {
  content?: string;
  theme?: ComponentProps<typeof MathContent>["theme"];
}) {
  if (!content) return null;
  return (
    <div data-testid="tutor-incomplete-reply" className="edu-assistant mb-3">
      <p className="mb-2 text-ui-caption">
        回复未完成 · 这段内容尚未作为正式解答保存
      </p>
      <MathContent theme={theme} content={content} />
    </div>
  );
}

export type ImageDraft = {
  requestId: string;
  name: string;
  dataUrl: string;
  uploadedId?: string;
  visualContext?: { run_id: number; visual_index: number };
};
export function TutorExtras({
  service,
  images,
  locked,
  onImages,
  onRemove,
  onPick,
  onPreparing,
}: {
  service: EducationService;
  images: ImageDraft[];
  locked: boolean;
  onImages: (images: ImageDraft[]) => void;
  onRemove: (id: string) => void;
  onPick: (item: HistoricalPractice) => Promise<void>;
  onPreparing: (value: boolean) => void;
}) {
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<HistoricalPractice[]>([]);
  const [query, setQuery] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const lifecycle = useRef(0);
  const imageInput = useRef<HTMLInputElement>(null);
  useEffect(() => {
    const current = lifecycle;
    return () => {
      current.current++;
      onPreparing(false);
    };
  }, [onPreparing]);
  const loadHistory = async () => {
    const current = lifecycle.current;
    setOpen(true);
    setBusy(true);
    setError("");
    try {
      const value = await service.get<{ items: HistoricalPractice[] }>(
        "/api/practice/history",
      );
      if (current === lifecycle.current) setItems(value.items);
    } catch (e) {
      if (current === lifecycle.current) setError(errorText(e));
    } finally {
      if (current === lifecycle.current) setBusy(false);
    }
  };
  const read = async (files: FileList | null) => {
    const current = lifecycle.current;
    if (!files) return;
    setError("");
    if (files.length + images.length > 3) {
      setError("每次最多上传三张图片。");
      return;
    }
    setBusy(true);
    try {
      const drafts: ImageDraft[] = [];
      onPreparing(true);
      for (const file of Array.from(files)) {
        if (
          !["image/png", "image/jpeg", "image/webp"].includes(file.type) ||
          file.size > 8 * 1024 * 1024
        )
          throw new Error("请选择 8 MB 以内的 PNG、JPEG 或 WebP 图片。");
        const attachment = createChatComposerAttachment(file);
        try {
          // 复用上游真实内容序列化，预览并不能证明模型收到了图片。
          const serialized = await serializeChatComposerAttachment(attachment);
          if (serialized.kind !== "image" || !serialized.dataBase64)
            throw new Error("图片缺少可读取内容。");
          drafts.push({
            requestId: attachment.id,
            name: serialized.filename.slice(0, 80),
            dataUrl: `data:${serialized.mimeType};base64,${serialized.dataBase64}`,
          });
        } finally {
          revokeChatComposerAttachment(attachment);
        }
      }
      if (current === lifecycle.current) onImages(drafts);
    } catch (e) {
      if (current === lifecycle.current) setError(errorText(e));
    } finally {
      if (current === lifecycle.current) {
        setBusy(false);
        onPreparing(false);
      }
    }
  };
  const filtered = items.filter((item) =>
    (item.item.title + item.item.expression).includes(query.trim()),
  );
  return (
    <>
      <div className="mb-2 flex flex-wrap items-center gap-2">
        <Button
          variant="ghost"
          size="sm"
          type="button"
          disabled={locked || busy || images.length >= 3}
          onClick={() => imageInput.current?.click()}
        >
          <ImagePlus />
          上传图片
        </Button>
        <input
          ref={imageInput}
          className="hidden"
          type="file"
          accept="image/png,image/jpeg,image/webp"
          multiple
          aria-label="上传题目图片"
          disabled={locked || busy || images.length >= 3}
          onChange={(e) => {
            void read(e.target.files);
            e.target.value = "";
          }}
        />
        <Button
          variant="ghost"
          size="sm"
          type="button"
          disabled={locked || busy}
          onClick={() => void loadHistory()}
        >
          <History />
          历史题目
        </Button>
        {busy && <LoaderCircle className="edu-spin size-4" />}
      </div>
      {error && !open && (
        <p
          role="alert"
          className="mb-2 text-ui-sm text-warning-surface-foreground"
        >
          {error}
        </p>
      )}
      {images.length > 0 && (
        <Attachments className="mb-3 ml-0" aria-label="待发送图片">
          {images.map((image) => (
            <Attachment
              key={image.requestId}
              className="[&_img]:object-contain"
              data={{
                type: "file",
                id: image.requestId,
                url: image.dataUrl,
                filename: image.name,
                mediaType: "image/jpeg",
              }}
              onRemove={() => onRemove(image.requestId)}
            >
              <AttachmentPreview />
              <AttachmentRemove
                label={`移除图片 ${image.name}`}
                className="opacity-100"
                disabled={locked}
              />
            </Attachment>
          ))}
        </Attachments>
      )}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-h-[85dvh] overflow-y-auto sm:max-w-2xl">
          <DialogHeader>
            <DialogTitle>选择历史题目</DialogTitle>
            <DialogDescription>
              从做过的题开始，接着讨论思路与疑惑。
            </DialogDescription>
          </DialogHeader>
          <div className="relative">
            <Search className="absolute left-3 top-2.5 size-4 text-foreground-subtle" />
            <Input
              className="pl-9 text-mobile-input-safe"
              aria-label="搜索历史题目"
              placeholder="搜索知识点或题干"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
          {error && (
            <div role="alert" className="text-ui-sm">
              <p>{error}</p>
              <Button
                size="sm"
                variant="outline"
                disabled={busy}
                onClick={() => void loadHistory()}
              >
                重新读取历史题目
              </Button>
            </div>
          )}
          {!busy && !filtered.length && (
            <p className="text-ui-sm text-foreground-subtle">
              {items.length
                ? "没有匹配的题目。"
                : "还没有可继续讨论的完整历史题。完成练习后会出现在这里。"}
            </p>
          )}
          {filtered.map((item) => (
            <article className="edu-card" key={item.item.id}>
              <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
                <span className="text-ui-sm font-medium">
                  {item.item.title}
                </span>
                <span className="text-ui-xs text-foreground-subtle">
                  {item.source}
                  {item.correct === null
                    ? ""
                    : item.correct
                      ? " · 已答对"
                      : " · 待巩固"}
                </span>
              </div>
              <MathContent content={item.item.expression} />
              <Button
                size="sm"
                className="mt-3"
                disabled={busy || item.item.usable === false}
                onClick={async () => {
                  setBusy(true);
                  try {
                    await onPick(item);
                    setOpen(false);
                  } catch (e) {
                    setError(errorText(e));
                  } finally {
                    setBusy(false);
                  }
                }}
              >
                讨论这道题
              </Button>
              {item.item.usable === false && (
                <p className="mt-2 text-ui-sm">{item.item.quality_note}</p>
              )}
            </article>
          ))}
        </DialogContent>
      </Dialog>
    </>
  );
}
