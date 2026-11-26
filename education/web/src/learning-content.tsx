import { lazy, Suspense, type ComponentProps } from "react";

const Response = lazy(() =>
  import("@zcode/ui/message").then((module) => ({
    default: module.MessageResponse,
  })),
);

export function MathContent({
  content,
  theme,
  streaming = false,
}: {
  content: string;
  theme?: ComponentProps<typeof Response>["theme"];
  streaming?: boolean;
}) {
  // 上游为了区分美元金额不解析单独的 Unicode 图形符号；教育题中的遮盖符号需映射为 TeX。
  const symbols: Record<string, string> = {
    "★": "\\bigstar",
    "■": "\\blacksquare",
    "□": "\\square",
    "●": "\\bullet",
  };
  const geometry =
    /线段|三角形|正方形|横坐标|纵坐标|坐标系|水平|竖直|邻边|对角线/.test(
      content,
    );
  const displayed = content
    .split(/(```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]*`)/g)
    .map((part, index) =>
      index % 2
        ? part
        : part
            // 真实回复曾出现 $C(1,-2)$$；只修复明确的行内结尾，不触碰代码/块级公式。
            .replace(
              /(?<![\\$])\$([^$\n]+)\$\$(?=[，。；、！？\s]|$)/g,
              (_, math: string) => `$${math}$`,
            )
            .replace(
              /(?<![\\$])\$([★■□●])\$(?!\$)/g,
              (_, symbol: string) => `$${symbols[symbol]}$`,
            )
            .replace(
              /(?<![\\$])\$([A-Z]{2,3})\$(?!\$)/g,
              (original, name: string) =>
                geometry ? `$\\mathrm{${name}}$` : original,
            ),
    )
    .join("");
  return (
    <div className="min-w-0 break-words text-ui-base [&_pre]:overflow-x-auto">
      <Suspense fallback={<p className="whitespace-pre-wrap">{content}</p>}>
        {/* 流式草稿启用上游未闭合Markdown解析；已接受历史继续使用静态模式。 */}
        <Response theme={theme} streaming={streaming}>
          {displayed}
        </Response>
      </Suspense>
    </div>
  );
}
