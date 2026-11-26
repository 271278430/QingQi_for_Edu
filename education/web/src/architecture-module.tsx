import { useState } from "react";
import { Button } from "@zcode/ui/button";
import type { ArchitectureModule, ArchitectureOverview } from "./contract.js";

export function ArchitectureModuleGuide({
  module,
  data,
  onSelect,
}: {
  module: ArchitectureModule;
  data: ArchitectureOverview;
  onSelect: (id: string) => void;
}) {
  const [active, setActive] = useState(0);
  const scope = module.scope;
  if (!scope) return null;
  const step = scope.steps[Math.min(active, scope.steps.length - 1)];
  return (
    <section className="edu-card space-y-5" aria-label="模块职责与内部流程">
      <div className="grid gap-4 md:grid-cols-3">
        <div>
          <h4 className="text-ui-base font-semibold">接收什么</h4>
          {scope.inputs.map((v) => (
            <p key={v} className="mt-2 text-ui-caption">
              {v}
            </p>
          ))}
        </div>
        <div>
          <h4 className="text-ui-base font-semibold">负责什么</h4>
          {scope.responsibilities.map((v) => (
            <p key={v} className="mt-2 text-ui-caption">
              {v}
            </p>
          ))}
        </div>
        <div>
          <h4 className="text-ui-base font-semibold">产出什么</h4>
          {scope.outputs.map((v) => (
            <p key={v} className="mt-2 text-ui-caption">
              {v}
            </p>
          ))}
        </div>
      </div>
      <div>
        <h4 className="mb-3 text-ui-base font-semibold">内部怎样组织</h4>
        <div className="flex flex-wrap gap-2" role="tablist" aria-label="模块内部步骤">
          {scope.steps.map((s, i) => (
            <Button
              key={s.id}
              role="tab"
              aria-selected={i === active}
              variant={i === active ? "secondary" : "outline"}
              onClick={() => setActive(i)}
            >
              {i + 1} · {s.title}
            </Button>
          ))}
        </div>
        <div role="tabpanel" className="mt-3 rounded-lg border border-border bg-background p-4">
          <h5 className="text-ui-lg font-semibold">{step.title}</h5>
          <p className="mt-2 text-ui-base">{step.detail}</p>
          <p className="mt-2 break-all text-ui-caption text-foreground-subtle">
            实际接口：{step.interface}
          </p>
        </div>
      </div>
      <div>
        <h4 className="text-ui-base font-semibold">与哪些模块协作</h4>
        <div className="mt-2 flex flex-wrap gap-2">
          {scope.calls.map((id) => (
            <Button key={id} variant="outline" onClick={() => onSelect(id)}>
              {data.modules.find((m) => m.id === id)?.title ?? id} →
            </Button>
          ))}
          {!scope.calls.length && (
            <p className="text-ui-caption text-foreground-subtle">
              提供只读资料，由其他业务模块调用。
            </p>
          )}
        </div>
      </div>
      <div>
        <h4 className="text-ui-base font-semibold">业务边界</h4>
        {scope.boundaries.map((v) => (
          <p key={v} className="mt-2 text-ui-caption text-foreground-subtle">
            {v}
          </p>
        ))}
      </div>
    </section>
  );
}
