import { useEffect, useState } from "react";
import { Button } from "@zcode/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@zcode/ui/dialog";
import { Maximize2, RefreshCw } from "lucide-react";
import type { ArchitectureOverview, EducationService } from "./contract.js";
import { errorText } from "./format.js";
import { ArchitectureCanvas } from "./architecture-board.js";
import { ArchitectureModuleGuide } from "./architecture-module.js";

export function ArchitecturePanel({ service }: { service: EducationService }) {
  const [data, setData] = useState<ArchitectureOverview>();
  const [selected, setSelected] = useState("");
  const [expanded, setExpanded] = useState(false);
  const [error, setError] = useState("");
  const [revision, setRevision] = useState(0);
  const selectModule = (id: string) => {
    setExpanded(false);
    setSelected(id);
  };
  useEffect(() => {
    const controller = new AbortController();
    setError("");
    service
      .get<ArchitectureOverview>(
        "/api/settings/architecture",
        controller.signal,
      )
      .then((value) => {
        if (!controller.signal.aborted) setData(value);
      })
      .catch((e) => {
        if (!controller.signal.aborted) setError(errorText(e));
      });
    return () => controller.abort();
  }, [service, revision]);
  if (error)
    return (
      <div role="alert" className="edu-card text-ui-base">
        {error}
        <Button variant="outline" onClick={() => setRevision((r) => r + 1)}>
          <RefreshCw />
          重新读取架构
        </Button>
      </div>
    );
  if (!data) return <p className="text-ui-base">正在读取项目模块…</p>;
  const module = data.modules.find((m) => m.id === selected);
  return (
    <section
      className="edu-architecture"
      aria-label="项目架构"
      data-architecture-ready="true"
    >
      <div className="mb-4">
        <h2 className="text-ui-xl font-semibold">项目架构</h2>
        <p className="mt-1 text-ui-caption text-foreground-subtle">
          一张图展示模块关系、Agent
          Loop和状态归属。点击模块查看输入、处理、输出与源码。
        </p>
      </div>
      <section className="edu-card" aria-label="系统关系">
        <div className="flex items-center justify-between gap-2">
          <h3 className="text-ui-lg font-semibold">系统关系</h3>
          <Button variant="outline" size="sm" onClick={() => setExpanded(true)}>
            <Maximize2 />
            放大架构图
          </Button>
        </div>
        <div
          className="edu-architecture-figure mt-4"
          data-architecture-board
          data-architecture-diagram="system"
        >
          <ArchitectureCanvas
            data={data}
            diagram={data.panorama}
            onSelect={selectModule}
          />
        </div>
      </section>
      <details className="edu-card mt-4 text-ui-base">
        <summary className="cursor-pointer font-medium">
          源码来源与状态边界
        </summary>
        <div className="mt-3 space-y-2 text-ui-caption">
          <p>
            ZCode提供工具注册与执行、调度、权限、MCP、Skills、前台子任务、有界记忆召回和Web组件。教育业务负责原题绑定、教学策略、数学核验、学习证据、路径与三题推荐。
          </p>
          <p>
            Store是唯一可写状态所有者；Web只拥有草稿、选择和播放进度。图谱与题库只读，聊天和提示不计作独立作答成绩。
          </p>
        </div>
      </details>
      <Dialog open={expanded} onOpenChange={setExpanded}>
        <DialogContent className="edu-architecture-dialog sm:max-w-6xl">
          <DialogHeader>
            <DialogTitle>系统关系</DialogTitle>
            <DialogDescription>
              保留原始字号，可滚动、缩放和下载。
            </DialogDescription>
          </DialogHeader>
          <ArchitectureCanvas
            data={data}
            diagram={data.panorama}
            onSelect={selectModule}
          />
        </DialogContent>
      </Dialog>
      <Dialog
        open={Boolean(module)}
        onOpenChange={(open) => {
          if (!open) setSelected("");
        }}
      >
        <DialogContent className="edu-architecture-dialog sm:max-w-5xl">
          <DialogHeader>
            <DialogTitle>{module?.title}</DialogTitle>
            <DialogDescription>{module?.owner}</DialogDescription>
          </DialogHeader>
          {module && (
            <>
              <ArchitectureModuleGuide
                key={module.id}
                module={module}
                data={data}
                onSelect={selectModule}
              />
              <details className="edu-card text-ui-base">
                <summary className="cursor-pointer font-medium">
                  源码、接口与复用
                </summary>
                <div className="mt-3 space-y-4 text-ui-caption">
                  <div>
                    <h4 className="font-semibold">已核对入口</h4>
                    <ul className="mt-2 space-y-1">
                      {module.bindings.map((b) => (
                        <li key={b.file + b.symbol}>
                          <code>{b.symbol}</code> ·{" "}
                          <span className="break-all text-foreground-subtle">
                            {b.file}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold">关键接口</h4>
                    <ul className="mt-2 space-y-1">
                      {module.interfaces.map((i) => (
                        <li key={i}>
                          <code className="break-all">{i}</code>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold">复用与适配</h4>
                    {module.reuse.map((s) => (
                      <p key={s} className="mt-1">
                        {s}
                      </p>
                    ))}
                  </div>
                </div>
              </details>
            </>
          )}
        </DialogContent>
      </Dialog>
    </section>
  );
}
