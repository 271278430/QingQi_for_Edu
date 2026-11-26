import { useState } from "react";
import { Attachments, Attachment, AttachmentPreview } from "@zcode/ui/attachments";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@zcode/ui/dialog";

export function TutorMessageImages({
  images,
}: {
  images: { id: string; name: string; url: string }[];
}) {
  const [opened, setOpened] = useState<(typeof images)[number] | null>(null);
  if (!images.length) return null;
  return (
    <>
      <Attachments className="mb-3 ml-0 max-w-full" aria-label="本条消息的图片">
        {images.map((image) => (
          <Attachment
            key={image.id}
            // 题干常在纸面顶部；完整适配避免上游居中裁切让数学题缩略图看起来空白。
            className="size-28 sm:size-36 [&_img]:object-contain"
            data={{
              type: "file",
              id: image.id,
              filename: image.name,
              mediaType: "image/jpeg",
              url: image.url,
            }}
            onOpen={() => setOpened(image)}
            openLabel={`放大查看 ${image.name}`}
          >
            <AttachmentPreview />
          </Attachment>
        ))}
      </Attachments>
      <Dialog
        open={Boolean(opened)}
        onOpenChange={(open) => {
          if (!open) setOpened(null);
        }}
      >
        <DialogContent className="sm:max-w-3xl">
          <DialogHeader>
            <DialogTitle>{opened?.name || "图片预览"}</DialogTitle>
            <DialogDescription>查看这条学习消息附带的完整图片。</DialogDescription>
          </DialogHeader>
          {opened && (
            <img
              src={opened.url}
              alt={opened.name}
              className="max-h-[70dvh] w-full object-contain"
            />
          )}
        </DialogContent>
      </Dialog>
    </>
  );
}
