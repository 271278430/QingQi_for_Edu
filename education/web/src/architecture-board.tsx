import { useRef, useState } from "react";
import { ZoomIn, ZoomOut, Download, Scan } from "lucide-react";
import { Button } from "@zcode/ui/button";
import type { ArchitectureOverview, SystemPanorama } from "./contract.js";
import { ArchitectureSvg } from "./architecture-svg.js";

function exportSvg(svg: SVGSVGElement, diagram: SystemPanorama, title: string) {
  const clone = svg.cloneNode(true) as SVGSVGElement;
  const original = [svg, ...Array.from(svg.querySelectorAll("*"))];
  const copied = [clone, ...Array.from(clone.querySelectorAll("*"))];
  const properties = [
    "fill",
    "stroke",
    "stroke-width",
    "stroke-dasharray",
    "font-family",
    "font-size",
    "font-weight",
    "text-anchor",
    "paint-order",
    "opacity",
    "filter",
  ];
  original.forEach((element, i) => {
    const computed = getComputedStyle(element);
    properties.forEach((property) =>
      (copied[i] as SVGElement).style.setProperty(
        property,
        computed.getPropertyValue(property),
      ),
    );
  });
  // 导出解析主题与字体，不依赖应用CSS；缩放只影响阅读，不改变独立SVG画布。
  clone.style.width = "";
  clone.style.minWidth = "";
  clone.style.maxWidth = "";
  clone.style.height = "";
  clone.setAttribute("width", String(diagram.width));
  clone.setAttribute("height", String(diagram.height));
  const url = URL.createObjectURL(
    new Blob([new XMLSerializer().serializeToString(clone)], {
      type: "image/svg+xml;charset=utf-8",
    }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = `清启-${title}.svg`;
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function ArchitectureCanvas({
  data,
  diagram,
  onSelect,
}: {
  data: ArchitectureOverview;
  diagram?: SystemPanorama;
  onSelect: (id: string) => void;
}) {
  const [zoom, setZoom] = useState(1);
  const svg = useRef<SVGSVGElement>(null);
  const viewport = useRef<HTMLDivElement>(null);
  if (!diagram)
    return (
      <p role="status" className="text-ui-base">
        系统图正在更新，请刷新页面或重新读取架构。
      </p>
    );
  return (
    <div className="edu-architecture-canvas">
      <div className="edu-panorama-toolbar flex flex-wrap items-center justify-between gap-2">
        <p className="text-ui-caption text-foreground-subtle">
          箭头表示执行、读取与提交；Loop中的回路表示观察结果后继续决策。宽图可左右滚动。
        </p>
        <div className="flex flex-wrap items-center gap-1">
          <Button
            variant="ghost"
            size="sm"
            aria-label="缩小全景"
            disabled={zoom <= 0.4}
            onClick={() => setZoom((v) => Math.max(0.4, v - 0.25))}
          >
            <ZoomOut />
          </Button>
          <span className="text-ui-xs tabular-nums">
            {Math.round(zoom * 100)}%
          </span>
          <Button
            variant="ghost"
            size="sm"
            aria-label="放大全景"
            disabled={zoom >= 2}
            onClick={() => setZoom((v) => Math.min(2, v + 0.25))}
          >
            <ZoomIn />
          </Button>
          <Button
            variant="outline"
            size="sm"
            aria-label="适应宽度"
            onClick={() => {
              if (viewport.current)
                setZoom(
                  Math.min(
                    2,
                    Math.max(
                      0.25,
                      viewport.current.clientWidth / diagram.width,
                    ),
                  ),
                );
            }}
          >
            <Scan />
            适应宽度
          </Button>
          <Button
            variant="ghost"
            size="sm"
            aria-label="原始字号"
            onClick={() => setZoom(1)}
          >
            原始字号
          </Button>
          <Button
            variant="outline"
            size="sm"
            aria-label="下载架构SVG"
            onClick={() => {
              if (svg.current)
                exportSvg(svg.current, diagram, diagram.title ?? "项目架构");
            }}
          >
            <Download />
            SVG
          </Button>
        </div>
      </div>
      <div
        ref={viewport}
        className="edu-panorama-viewport"
        role="region"
        aria-label="可缩放系统架构图"
      >
        <ArchitectureSvg
          data={data}
          diagram={diagram}
          zoom={zoom}
          svgRef={svg}
          onSelect={onSelect}
        />
      </div>
    </div>
  );
}
