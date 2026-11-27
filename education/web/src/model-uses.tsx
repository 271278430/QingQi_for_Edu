import { Button } from "@zcode/ui/button";
import { Check } from "lucide-react";
import type { ModelRole } from "./contract.js";

const labels: Record<ModelRole, string> = {
  text: "文本默认",
  vision: "图片默认",
  course8b: "课程导航",
  difficulty8b: "学情分析",
  review27b: "答案审查",
};

export function ModelUses({
  roles,
  uses,
  supportsImage,
  available,
  busy,
  onUse,
}: {
  roles: ModelRole[];
  uses: ModelRole[];
  supportsImage: boolean;
  available: boolean;
  busy: boolean;
  onUse: (role: ModelRole, remove: boolean) => Promise<void>;
}) {
  return (
    <div
      className="flex flex-wrap items-center gap-2 border-t border-border px-3 py-2"
      data-model-uses="true"
      aria-label="型号默认用途"
    >
      <span className="text-ui-xs text-foreground-subtle">用途</span>
      {roles.map((role) => {
        const active = uses.includes(role),
          required = role === "text" || role === "vision";
        return (
          <Button
            key={role}
            size="sm"
            variant={active ? "secondary" : "ghost"}
            data-model-use-role={role}
            aria-label={active ? labels[role] : `设为${labels[role]}`}
            aria-pressed={active}
            title={
              role === "vision" && !supportsImage
                ? "此型号尚未声明图片输入能力"
                : active && !required
                  ? "点击取消这项可选用途"
                  : undefined
            }
            disabled={
              busy ||
              (!active &&
                (!available || (role === "vision" && !supportsImage))) ||
              (active && required)
            }
            onClick={() => void onUse(role, active).catch(() => undefined)}
          >
            {active && <Check className="size-3" />}
            {active ? labels[role] : `设为${labels[role]}`}
          </Button>
        );
      })}
    </div>
  );
}
