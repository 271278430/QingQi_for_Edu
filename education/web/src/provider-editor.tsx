import { useState } from "react";
import { Button } from "@zcode/ui/button";
import { Input } from "@zcode/ui/input";
import {
  ModelRowInput,
  ProviderCardHeader,
  ProviderConnectionSection,
  ProviderApiKeySection,
  ProviderModelMetadataDialog,
  useProviderModelDraft,
} from "@zcode/ui/model-provider-settings";
import type { ProviderSettingsFormModel } from "@zcode/ui/model-provider-settings";
import type {
  ModelConnection,
  ModelDefinition,
  ModelRole,
} from "./contract.js";
import { ModelUses } from "./model-uses.js";
import {
  completeModelConfig,
  defaultModelConfig,
  formModel,
  formProvider,
  modelSelectionId,
} from "./provider-form.js";

function AddModel({
  onClose,
  onSave,
  blocked,
}: {
  onClose: () => void;
  onSave: (model: ProviderSettingsFormModel) => Promise<void>;
  blocked: boolean;
}) {
  const initial = formModel({
    key: "new",
    model: "",
    config: defaultModelConfig() as Record<string, unknown>,
  });
  const editor = useProviderModelDraft({
    model: initial,
    open: true,
    scopeKey: "new-model",
  });
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const commit = async () => {
    const result = await editor.commit();
    if (result.status !== "commit") {
      setError(`请检查模型配置（${result.field}）`);
      return false;
    }
    setSaving(true);
    try {
      await onSave(result.model);
      onClose();
      return true;
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      return false;
    } finally {
      setSaving(false);
    }
  };
  return (
    <ProviderModelMetadataDialog
      educationScope
      mode="add"
      open
      draft={editor.draft}
      draftErrorMessage={error}
      inheritedConfig={initial.inheritedConfig}
      personalConfig={initial.personalConfig}
      onDraftChange={editor.change}
      onOpenChange={(open) => {
        if (!open && !saving) onClose();
      }}
      onCommit={commit}
      onRestore={() => {
        editor.reset(initial);
        setError(null);
      }}
      saving={saving || blocked}
    />
  );
}

export function ProviderEditor({
  connection,
  selectionIds,
  roles,
  modelUses,
  availableModels,
  onUse,
  busy,
  error,
  onSave,
  onDelete,
  onCopy,
  onTest,
  onDiscover,
}: {
  connection: ModelConnection;
  selectionIds: (string | null)[];
  roles: ModelRole[];
  modelUses: Record<string, ModelRole[]>;
  availableModels: Set<string>;
  onUse: (
    model: ModelDefinition,
    role: ModelRole,
    remove: boolean,
  ) => Promise<void>;
  busy: boolean;
  error: string;
  onSave: (connection: ModelConnection, key?: string) => Promise<void>;
  onDelete: () => Promise<void>;
  onCopy: () => void;
  onTest: (
    model: ModelDefinition,
    kind: "text" | "vision",
  ) => Promise<{ success: boolean; message: string }>;
  onDiscover: () => Promise<void>;
}) {
  const [draft, setDraft] = useState(connection);
  const [key, setKey] = useState("");
  const [keyVisible, setKeyVisible] = useState(false);
  const [editingName, setEditingName] = useState(false);
  const [adding, setAdding] = useState(false);
  const provider = formProvider(draft);
  const updateModels = async (models: ModelDefinition[]) => {
    await onSave({ ...draft, models }, key);
    setKey("");
  };
  const save = async () => {
    await onSave(draft, key);
    setKey("");
  };
  const active = draft.models.some((model) =>
    selectionIds.includes(modelSelectionId(draft, model)),
  );
  return (
    <section
      aria-label="供应商详情"
      data-provider-source="ZCode"
      className="space-y-6"
    >
      <ProviderCardHeader
        actionsVisible={!busy}
        providerName={draft.display_name}
        editingName={editingName}
        nameValue={draft.display_name}
        nameEditable={!draft.readonly}
        onNameChange={(display_name) => setDraft({ ...draft, display_name })}
        onNameBlur={() => setEditingName(false)}
        onNameKeyDown={(e) => {
          if (e.key === "Enter") setEditingName(false);
        }}
        onStartEditName={() => setEditingName(true)}
        onDelete={
          !draft.readonly && !active
            ? () => void onDelete().catch(() => undefined)
            : undefined
        }
      />
      {connection.origin === "deployment" && (
        <p className="text-ui-caption text-foreground-subtle">
          已同步本机模型配置，可在此编辑。默认用途作用于系统配置，对话框仍可单独选模。
        </p>
      )}
      {error && (
        <p role="alert" className="text-ui-base">
          {error}
        </p>
      )}
      <fieldset disabled={busy} className="space-y-4">
        <ProviderConnectionSection
          provider={provider}
          readOnly={draft.readonly}
          apiFormat={
            draft.protocol === "openai"
              ? "openai-chat-completions"
              : "anthropic-messages"
          }
          apiFormatOptions={["openai-chat-completions", "anthropic-messages"]}
          baseUrlValue={draft.base_url}
          onApiFormatChange={(type) =>
            setDraft({
              ...draft,
              protocol: type === "anthropic-messages" ? "anthropic" : "openai",
            })
          }
          onBaseUrlChange={(base_url) => setDraft({ ...draft, base_url })}
          onBaseUrlBlur={() => undefined}
        />
        <ProviderApiKeySection
          apiKeyValue={key}
          apiKeyVisible={keyVisible}
          readOnly={draft.readonly || !draft.requires_key}
          onApiKeyChange={setKey}
          onApiKeyBlur={() => undefined}
          onToggleApiKeyVisibility={() => setKeyVisible((value) => !value)}
        />
        <p className="text-ui-caption text-foreground-subtle">
          {!draft.requires_key
            ? "此连接使用无需 API Key 的服务"
            : draft.credential_ready
              ? "已有加密凭据，留空保留"
              : "配置供应商的 API Key"}
        </p>
        {!draft.readonly && (
          <label className="flex items-center gap-2 text-ui-base">
            <input
              type="checkbox"
              checked={draft.requires_key}
              onChange={(e) =>
                setDraft({ ...draft, requires_key: e.target.checked })
              }
            />
            接口需要 API Key
          </label>
        )}
        {!draft.readonly && (
          <label className="block text-ui-caption">
            请求超时（秒）
            <Input
              aria-label="请求超时"
              type="number"
              min={1}
              max={90}
              value={draft.timeout}
              onChange={(e) =>
                setDraft({ ...draft, timeout: Number(e.target.value) })
              }
            />
          </label>
        )}
        <div className="flex flex-wrap gap-2">
          {!draft.readonly && (
            <Button onClick={() => void save().catch(() => undefined)}>
              保存连接
            </Button>
          )}
          <Button variant="outline" onClick={onCopy}>
            复制供应商
          </Button>
          <Button
            variant="outline"
            onClick={() => void onDiscover().catch(() => undefined)}
          >
            读取模型列表
          </Button>
        </div>
      </fieldset>
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-ui-lg font-medium">模型</h3>
          {!draft.readonly && (
            <Button
              variant="outline"
              disabled={busy}
              onClick={() => setAdding(true)}
            >
              添加模型
            </Button>
          )}
        </div>
        {draft.models.map((model) => (
          <article
            key={model.key}
            data-provider-model={model.key}
            className="rounded-lg border border-border"
          >
            <fieldset disabled={busy}>
              <ModelRowInput
                educationScope
                readOnly={draft.readonly}
                disabled={busy}
                model={formModel(model)}
                providerId={draft.id}
                providerName={draft.display_name}
                settingsRevision={connection.version}
                onCommit={async (next) =>
                  updateModels(
                    draft.models.map((item) =>
                      item.key === model.key
                        ? {
                            ...item,
                            model: next.modelId,
                            config: completeModelConfig(
                              next.config,
                              model.config as Parameters<
                                typeof completeModelConfig
                              >[0],
                            ) as Record<string, unknown>,
                          }
                        : item,
                    ),
                  )
                }
                onDelete={
                  !draft.readonly &&
                  !selectionIds.includes(modelSelectionId(draft, model))
                    ? () =>
                        void updateModels(
                          draft.models.filter((item) => item.key !== model.key),
                        ).catch(() => undefined)
                    : undefined
                }
                onEnabledChange={
                  !draft.readonly
                    ? (enabled) =>
                        void updateModels(
                          draft.models.map((item) =>
                            item.key === model.key
                              ? { ...item, config: { ...item.config, enabled } }
                              : item,
                          ),
                        ).catch(() => undefined)
                    : undefined
                }
                onTest={async () => {
                  const result = await onTest(model, "text");
                  return result.success
                    ? { success: true }
                    : {
                        success: false,
                        error: {
                          code: "model-unavailable",
                          message: result.message,
                        },
                      };
                }}
              />
              {!draft.readonly && (
                <label className="flex items-center gap-2 px-3 pb-3 text-ui-caption">
                  <input
                    type="checkbox"
                    checked={
                      (model.config.properties as Record<string, unknown>)
                        ?.supportsToolCall !== false
                    }
                    onChange={(e) =>
                      void updateModels(
                        draft.models.map((item) =>
                          item.key === model.key
                            ? {
                                ...item,
                                config: {
                                  ...item.config,
                                  properties: {
                                    ...(item.config.properties as Record<
                                      string,
                                      unknown
                                    >),
                                    supportsToolCall: e.target.checked,
                                  },
                                },
                              }
                            : item,
                        ),
                      ).catch(() => undefined)
                    }
                  />
                  支持原生工具调用
                </label>
              )}
            </fieldset>
            <ModelUses
              roles={roles}
              uses={modelUses[modelSelectionId(connection, model)] ?? []}
              supportsImage={
                !!(
                  model.config.properties as {
                    inputFormat?: { supportsImage?: boolean };
                  }
                )?.inputFormat?.supportsImage
              }
              available={availableModels.has(
                modelSelectionId(connection, model),
              )}
              busy={busy}
              onUse={(role, remove) => onUse(model, role, remove)}
            />
            {(
              model.config.properties as {
                inputFormat?: { supportsImage?: boolean };
              }
            )?.inputFormat?.supportsImage && (
              <Button
                variant="ghost"
                disabled={busy}
                onClick={() =>
                  void onTest(model, "vision").catch(() => undefined)
                }
              >
                测试图片识别
              </Button>
            )}
          </article>
        ))}
        {!draft.models.length && (
          <p className="text-ui-base text-foreground-subtle">
            添加一个模型，然后选择其教学角色。
          </p>
        )}
      </div>
      {adding && (
        <AddModel
          blocked={busy}
          onClose={() => setAdding(false)}
          onSave={(model) =>
            updateModels([
              ...draft.models,
              {
                key: crypto.randomUUID(),
                model: model.modelId,
                config: completeModelConfig(model.config) as Record<
                  string,
                  unknown
                >,
              },
            ])
          }
        />
      )}
    </section>
  );
}
