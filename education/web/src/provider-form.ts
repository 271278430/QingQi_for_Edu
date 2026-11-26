import type {
  ModelConfigObject,
  ProviderSettingsFormModel,
  ProviderSettingsFormProvider,
} from "@zcode/ui/model-provider-settings";
import type { ModelConnection, ModelDefinition } from "./contract.js";

export function defaultModelConfig(): ModelConfigObject {
  return {
    enabled: true,
    properties: {
      contextWindow: 128000,
      inputFormat: {
        supportsText: true,
        supportsImage: false,
        supportsVideo: false,
        supportsPdf: false,
        supportsAudio: false,
      },
      supportsToolCall: true,
      supportsJsonSchemaOutput: false,
    },
    optionSpecs: {
      maxOutputTokens: { max: 1600 },
      reasoningLevel: { values: ["default"], map: "{}" },
    },
  };
}
export function formModel(model: ModelDefinition): ProviderSettingsFormModel {
  const config = model.config as ModelConfigObject;
  return {
    kind: "candidate",
    modelId: model.model,
    builtin: false,
    personalConfig: config,
    config,
    inheritedConfig: config,
    useRecommendedConfig: false,
    hasPersonalConfig: true,
    executable: config.enabled !== false,
    selectable: config.enabled !== false,
  };
}
export function completeModelConfig(
  config: ModelConfigObject,
  base: ModelConfigObject = defaultModelConfig(),
): ModelConfigObject {
  const defaults = defaultModelConfig();
  // ZCode改名会返回 undefined 能力字段，代表该草稿未定义；不能覆盖已有 false 并触发后端默认 true。
  // 教育HTTP契约保存完整配置，只有已定义的草稿字段覆盖基线；false 和 0 仍是有效值。
  const defined = <T extends object>(value: T | null | undefined): Partial<T> =>
    Object.fromEntries(
      Object.entries(value ?? {}).filter(([, v]) => v !== undefined),
    ) as Partial<T>;
  return {
    ...defaults,
    ...defined(base),
    ...defined(config),
    properties: {
      ...defaults.properties,
      ...defined(base.properties),
      ...defined(config.properties),
      inputFormat: {
        ...defaults.properties?.inputFormat,
        ...defined(base.properties?.inputFormat),
        ...defined(config.properties?.inputFormat),
        supportsText: true,
      },
    },
    optionSpecs: {
      ...defaults.optionSpecs,
      ...defined(base.optionSpecs),
      ...defined(config.optionSpecs),
      maxOutputTokens: {
        ...defaults.optionSpecs?.maxOutputTokens,
        ...defined(base.optionSpecs?.maxOutputTokens),
        ...defined(config.optionSpecs?.maxOutputTokens),
      },
      reasoningLevel: {
        ...defaults.optionSpecs?.reasoningLevel,
        ...defined(base.optionSpecs?.reasoningLevel),
        ...defined(config.optionSpecs?.reasoningLevel),
      },
    },
  };
}
export function formProvider(connection: ModelConnection): ProviderSettingsFormProvider {
  return {
    providerId: connection.id,
    providerName: connection.display_name,
    enabled: true,
    executable: connection.credential_ready,
    hasPersonalConfig: !connection.readonly,
    personalConfig: {},
    config: {
      api: {
        type: connection.protocol === "openai" ? "openai-chat-completions" : "anthropic-messages",
        baseUrl: connection.base_url,
      },
    },
    models: connection.models.map(formModel),
  };
}
export function modelSelectionId(connection: ModelConnection, model: ModelDefinition) {
  return model.key === "main" ? connection.id : `${connection.id}~${model.key}`;
}
export function emptyConnection(): ModelConnection {
  return {
    id: `custom-${crypto.randomUUID()}`,
    display_name: "自定义供应商",
    base_url: "https://open.bigmodel.cn/api/paas/v4",
    protocol: "openai",
    requires_key: true,
    credential_ready: false,
    readonly: false,
    version: 0,
    timeout: 30,
    models: [],
  };
}
