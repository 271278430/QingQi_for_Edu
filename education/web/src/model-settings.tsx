import { useEffect, useRef, useState } from "react";
import { Button } from "@zcode/ui/button";
import { ModelProviderSectionLayout } from "@zcode/ui/model-provider-settings";
import type { ModelProviderNavGroup } from "@zcode/ui/model-provider-settings";
import type {
  EducationService,
  ModelConnection,
  ModelDefinition,
  ModelSettingsView,
} from "./contract.js";
import { EducationRequestError } from "./contract.js";
import { EducationSelect } from "./controls.js";
import { errorText } from "./format.js";
import {
  defaultModelConfig,
  emptyConnection,
  formProvider,
  modelSelectionId,
} from "./provider-form.js";
import { ProviderEditor } from "./provider-editor.js";

type PendingCommand = { path: string; body: Record<string, unknown> };
const NO_PROVIDER_REORDER: ReadonlySet<string> = new Set();
export function ModelSettingsPanel({
  service,
  onChanged,
}: {
  service: EducationService;
  onChanged: () => void;
}) {
  const [data, setData] = useState<ModelSettingsView>();
  const [selection, setSelection] = useState<ModelSettingsView["selection"]>();
  const [selected, setSelected] = useState("");
  const [created, setCreated] = useState<ModelConnection>();
  const [revision, setRevision] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [pending, setPending] = useState<PendingCommand>();
  const [discovered, setDiscovered] = useState<{ id: string; supports_image: boolean | null }[]>(
    [],
  );
  const mounted = useRef(true);
  const acceptedVersion = useRef(-1);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  useEffect(() => {
    const abort = new AbortController();
    service
      .get<ModelSettingsView>("/api/settings/models", abort.signal)
      .then((view) => {
        if (abort.signal.aborted || view.version < acceptedVersion.current) return;
        acceptedVersion.current = view.version;
        setData(view);
        setSelection(view.selection);
        setSelected((id) =>
          view.connections.some((p) => p.id === id) ? id : (view.connections[0]?.id ?? ""),
        );
      })
      .catch((e) => {
        if (!abort.signal.aborted) setError(errorText(e));
      });
    return () => abort.abort();
  }, [service, revision]);
  const command = async (path: string, body: Record<string, unknown>) => {
    if (busy) throw new Error("请等待当前操作完成");
    const current = pending ?? { path, body };
    setPending(current);
    setBusy(true);
    setError("");
    setMessage("");
    try {
      const view = await service.post<ModelSettingsView>(current.path, current.body);
      acceptedVersion.current = view.version;
      onChanged();
      if (mounted.current) {
        setData(view);
        setSelection(view.selection);
        setPending(undefined);
        setCreated(undefined);
        setMessage("设置已保存，新请求使用当前模型配置。");
      }
    } catch (e) {
      if (mounted.current) {
        setError(errorText(e));
        if (
          e instanceof EducationRequestError &&
          e.code !== "invalid_response" &&
          [400, 403, 409].includes(e.status)
        ) {
          setPending(undefined);
          if (e.status === 409) setRevision((value) => value + 1);
        }
      }
      throw e;
    } finally {
      if (mounted.current) setBusy(false);
    }
  };
  if (!data || !selection)
    return (
      <div className="edu-card text-ui-base">
        {error || "读取供应商设置…"}
        <Button onClick={() => setRevision((value) => value + 1)}>重新读取</Button>
      </div>
    );
  const connections = created ? [...data.connections, created] : data.connections;
  const connection = connections.find((p) => p.id === selected) ?? connections[0];
  const save = (provider: ModelConnection, key = "") =>
    command("/api/settings/model-providers", {
      request_id: crypto.randomUUID(),
      version: data.version,
      operation: "upsert",
      provider: {
        id: provider.id,
        display_name: provider.display_name,
        base_url: provider.base_url,
        protocol: provider.protocol,
        requires_key: provider.requires_key,
        timeout: Math.min(60, provider.timeout),
        models: provider.models,
        model: "",
        supports_image: false,
        supports_tools: true,
        max_tokens: 1600,
        json_mode: false,
        credential_ref: provider.credential_ref ?? "",
        key_action: !provider.requires_key ? "clear" : key ? "replace" : "keep",
        api_key: key,
      },
    });
  const probe = async (model: ModelDefinition, kind: "text" | "vision") => {
    if (!connection || busy) throw new Error("请等待当前操作完成");
    setBusy(true);
    setError("");
    try {
      const result = await service.post<{ success: boolean; message: string }>(
        "/api/settings/models/test",
        { provider_id: modelSelectionId(connection, model), kind },
      );
      if (mounted.current) setMessage(result.message);
      return result;
    } catch (e) {
      if (mounted.current) setError(errorText(e));
      throw e;
    } finally {
      if (mounted.current) setBusy(false);
    }
  };
  const groups: ModelProviderNavGroup[] = [
    {
      id: "custom",
      title: "模型供应商",
      items: connections.map((p) => ({
        key: p.id,
        type: "custom",
        label: p.display_name,
        provider: formProvider(p),
        statusActive: p.credential_ready,
      })),
    },
  ];
  const options = (vision: boolean) => [
    { value: "", label: "未选择" },
    ...data.providers
      .filter(
        (p) => p.model && p.model_enabled && p.credential_ready && (!vision || p.supports_image),
      )
      .map((p) => ({ value: p.id, label: `${p.display_name} · ${p.model}` })),
  ];
  return (
    <section aria-label="模型适配" className="space-y-5" data-zcode-model-settings="true">
      <div className="edu-card space-y-4">
        <h3 className="text-ui-lg font-semibold">教学模型</h3>
        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2">
            <p className="text-ui-base">文本导师</p>
            <EducationSelect
              label="文本导师"
              value={selection.text_provider_id ?? ""}
              options={options(false)}
              disabled={busy || !!pending}
              onValueChange={(id) => setSelection({ ...selection, text_provider_id: id || null })}
            />
          </div>
          <div className="space-y-2">
            <p className="text-ui-base">图片理解模型</p>
            <EducationSelect
              label="图片理解模型"
              value={selection.vision_provider_id ?? ""}
              options={options(true)}
              disabled={busy || !!pending}
              onValueChange={(id) => setSelection({ ...selection, vision_provider_id: id || null })}
            />
          </div>
        </div>
        <p className="text-ui-caption text-foreground-subtle">
          同一多模态模型可同时承担文本与图片教学。
        </p>
        <div className="flex flex-wrap gap-2">
          <Button
            disabled={busy || !!pending}
            onClick={() =>
              void command("/api/settings/model-selection", {
                request_id: crypto.randomUUID(),
                version: data.version,
                mode:
                  selection.text_provider_id &&
                  selection.text_provider_id === selection.vision_provider_id
                    ? "shared"
                    : "split",
                text_provider_id: selection.text_provider_id,
                vision_provider_id: selection.vision_provider_id,
              }).catch(() => undefined)
            }
          >
            应用教学模型
          </Button>
          <Button
            variant="outline"
            disabled={busy || !!pending}
            onClick={() =>
              void command("/api/settings/model-selection", {
                request_id: crypto.randomUUID(),
                version: data.version,
                mode: "deployment",
              }).catch(() => undefined)
            }
          >
            恢复部署模型
          </Button>
        </div>
      </div>
      {message && (
        <p role="status" className="text-ui-base">
          {message}
        </p>
      )}
      {pending && !busy && (
        <Button onClick={() => void command(pending.path, pending.body).catch(() => undefined)}>
          重试上次保存
        </Button>
      )}
      <ModelProviderSectionLayout
        description="配置供应商连接，在供应商下添加和测试模型。"
        refreshLabel="刷新"
        loadingLabel="处理中"
        presetLoading={false}
        customLoading={busy || !!pending}
        onRefresh={() => {
          if (!busy) setRevision((value) => value + 1);
        }}
        addProviderLabel="添加供应商"
        onAddProvider={() => {
          if (busy || pending) return;
          const provider = emptyConnection();
          setCreated(provider);
          setSelected(provider.id);
          setError("");
          setDiscovered([]);
        }}
        navigationGroups={groups}
        reorderableProviderIds={NO_PROVIDER_REORDER}
        selectedNodeKey={selected}
        onSelectNavItem={(item) => {
          if (!busy && !pending) {
            setSelected(item.key);
            setDiscovered([]);
            setError("");
            setMessage("");
          }
        }}
      >
        {connection && (
          <ProviderEditor
            key={`${connection.id}:${connection.version}`}
            connection={connection}
            selectionIds={[data.selection.text_provider_id, data.selection.vision_provider_id]}
            busy={busy || !!pending}
            error={error}
            onSave={save}
            onDelete={() =>
              command("/api/settings/model-providers", {
                request_id: crypto.randomUUID(),
                version: data.version,
                operation: "delete",
                provider_id: connection.id,
              })
            }
            onCopy={() => {
              const copy = {
                ...connection,
                id: `custom-${crypto.randomUUID()}`,
                display_name: connection.display_name + " · 复制",
                readonly: false,
                timeout: Math.min(60, connection.timeout),
                version: 0,
                credential_ready: false,
                credential_ref: connection.readonly ? connection.id : "",
              };
              setCreated(copy);
              setSelected(copy.id);
            }}
            onTest={probe}
            onDiscover={async () => {
              setBusy(true);
              setError("");
              try {
                const result = await service.post<{
                  models: { id: string; supports_image: boolean | null }[];
                }>("/api/settings/models/discover", { provider_id: connection.id });
                if (mounted.current) {
                  setDiscovered(result.models);
                  setMessage(`读取到 ${result.models.length} 个模型`);
                }
              } catch (error) {
                if (mounted.current) setError(errorText(error));
                throw error;
              } finally {
                if (mounted.current) setBusy(false);
              }
            }}
          />
        )}
        {!!discovered.length && connection && (
          <div className="mt-5 flex flex-wrap gap-2">
            {discovered.map((model) => (
              <Button
                key={model.id}
                variant="outline"
                disabled={
                  busy || connection.readonly || connection.models.some((m) => m.model === model.id)
                }
                onClick={() => {
                  const defaults = defaultModelConfig();
                  const config = {
                    ...defaults,
                    properties: {
                      ...defaults.properties,
                      inputFormat: {
                        ...defaults.properties?.inputFormat,
                        supportsImage: model.supports_image === true,
                      },
                    },
                  };
                  void save({
                    ...connection,
                    models: [
                      ...connection.models,
                      {
                        key: crypto.randomUUID(),
                        model: model.id,
                        config: config as Record<string, unknown>,
                      },
                    ],
                  }).catch(() => undefined);
                }}
              >
                添加 {model.id}
              </Button>
            ))}
          </div>
        )}
      </ModelProviderSectionLayout>
    </section>
  );
}
