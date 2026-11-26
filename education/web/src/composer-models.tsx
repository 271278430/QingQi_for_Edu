import { ModelConfigSelect, type ModelSelectGroup } from "@zcode/ui/model-config-select";
import { Button } from "@zcode/ui/button";
import type { useChatModels } from "./use-chat-models.js";

const labels: Record<string, string> = {
  default: "默认",
  low: "低",
  medium: "中",
  high: "高",
  max: "最高",
};
export function ComposerModels({
  models,
  onManage,
  canManage,
  disabled = false,
}: {
  models: ReturnType<typeof useChatModels>;
  onManage: () => void;
  canManage: boolean;
  disabled?: boolean;
}) {
  const { view, saving, loading, error, load, save } = models;
  if (!view)
    return (
      <div className="text-ui-xs text-foreground-subtle" role="status">
        {error || "正在读取模型…"}
        {error && (
          <Button type="button" variant="ghost" onClick={() => void load()}>
            重新读取
          </Button>
        )}
      </div>
    );
  if (!view.models.length)
    return (
      <span className="text-ui-xs text-foreground-subtle">
        本地辅导
        {canManage && (
          <Button type="button" variant="ghost" onClick={onManage}>
            配置模型
          </Button>
        )}
      </span>
    );
  return (
    <div className="flex min-w-0 flex-wrap items-center gap-1" data-testid="composer-models">
      {(["text", "vision"] as const).map((role) => {
        const choice = view.selection[role];
        const current = view.models.find((m) => m.id === choice?.model_id);
        const entries = view.models.filter((m) => role === "text" || m.supports_image);
        const groups: ModelSelectGroup[] = [];
        for (const model of entries) {
          let group = groups.find((g) => g.key === model.provider_id);
          if (!group) {
            group = { key: model.provider_id, label: model.provider_label, items: [] };
            groups.push(group);
          }
          group.items.push({
            key: model.id,
            value: model.id,
            name: model.name,
            supportsVisionInput: model.supports_image,
            badgeLabel: model.available ? undefined : "不可用",
          });
        }
        const prefix = role === "text" ? "文本" : "图片";
        const title = current?.name || (choice ? "模型已失效" : "未选择");
        return (
          <ModelConfigSelect
            key={role}
            modelGroups={groups}
            normalizedValue={choice?.model_id || ""}
            triggerLabel={`${prefix} · ${title}${choice ? ` · ${labels[choice.reasoning_level] || choice.reasoning_level}` : ""}`}
            triggerLabelPrefix={`${prefix} · `}
            triggerLabelPrefixClassName="mr-1"
            triggerLabelValue={title}
            labelVisibilityClassName="inline-flex"
            triggerClassName="max-w-64"
            triggerTestId={`composer-model-${role}`}
            showManageModelsAction={canManage}
            onManageModels={onManage}
            manageModelsLabel="配置模型"
            lockReasonMessage="请先配置凭据并启用模型"
            isItemLocked={(id) => !entries.find((m) => m.id === id)?.available}
            onValueChange={(id) => {
              const model = entries.find((m) => m.id === id);
              if (model)
                void save({
                  [role]: {
                    model_id: id,
                    model_version: model.version,
                    reasoning_level: model.default_level,
                  },
                });
            }}
            disabled={disabled || saving || loading}
            pending={saving}
            pendingLabel="保存中"
            focusSelectorOnClose="#edu-question"
            contentSide="top"
            composerOptions={
              current && choice && current.levels.length > 1
                ? {
                    providerLabel: current.provider_label,
                    modelsLabel: "模型",
                    effortLabel: "推理档位",
                    selectModelLabel: "选择已配置模型",
                    levels: current.levels.map((value) => ({
                      value,
                      label: labels[value] || value,
                    })),
                    value: choice.reasoning_level,
                    onValueChange: (value) => {
                      void save({
                        [role]: { ...choice, reasoning_level: value },
                      });
                    },
                  }
                : undefined
            }
          />
        );
      })}
      {(error || view.issues.length > 0) && (
        <span className="text-ui-xs text-destructive" role="alert">
          {error || view.issues[0]}
          <Button type="button" variant="ghost" disabled={saving} onClick={() => void load()}>
            重新读取
          </Button>
        </span>
      )}
    </div>
  );
}
