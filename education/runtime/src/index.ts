import { randomUUID } from "node:crypto";
import { realpath } from "node:fs/promises";
import { isAbsolute, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { isDeepStrictEqual } from "node:util";
import { z } from "zod";
import {
  createToolRegistry,
  createToolExecutor,
  PermissionService,
  ToolScheduler,
  createExploreSubagentPort,
  type AgentProfile,
} from "@zcode/core";
import { createMcpAdapter } from "@zcode/adapters/mcp";
import { createNodeSkillAdapter } from "@zcode/adapters/skills";
import {
  createRootTraceContext,
  type SessionId,
  type ToolCallId,
  type SessionEvent,
  type TraceId,
} from "@zcode/contracts";
import { ToolSpec, ToolName, type InvokeHandler, type RegisteredTool } from "./contract.js";
import { selectScopedMemory } from "./memory.js";

const SERVICE = fileURLToPath(new URL("../../service/", import.meta.url));
const Init = z
  .object({
    python: z.string().min(1),
    root: z.string(),
    graph_path: z
      .string()
      .min(1)
      .max(3000)
      .default(join(SERVICE, "data", "curriculum.sqlite")),
    trace_id: z.string(),
    session_id: z.string(),
    specs: z.array(ToolSpec).max(12),
  })
  .strict();
const Call = z
  .object({
    name: ToolName,
    arguments: z.record(z.string(), z.unknown()),
    timeout_ms: z.number().positive().max(300000),
  })
  .strict();
const Plan = z
  .object({
    nodes: z
      .array(
        z
          .object({
            id: z.string().min(1),
            depends_on: z.array(z.string()),
            intent: z.string().optional(),
            requires_confirmation: z.boolean().optional(),
          })
          .strict(),
      )
      .max(8),
  })
  .strict();
const Names = z.object({ names: z.array(z.string()).max(12) }).strict();

export class RuntimeError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly recoverable = false,
    public readonly retry_after?: number,
  ) {
    super(message);
  }
}

export class EducationRuntime {
  private configuration?: z.infer<typeof Init>;
  private registry = createToolRegistry();
  private mcp = createMcpAdapter({ workingDirectory: SERVICE });
  private skills = createNodeSkillAdapter({ includeZcodeSkills: false });
  private mcpReady?: Promise<void>;
  private closed = false;
  private events: SessionEvent[] = [];
  constructor(private readonly invoke: InvokeHandler) {}

  async dispatch(op: string, input: Record<string, unknown>): Promise<unknown> {
    if (op === "init") {
      if (this.configuration)
        throw new RuntimeError("already_initialized", "Runtime is already initialized");
      const configuration = Init.parse(input);
      const delta = relative(join(SERVICE, "runs"), resolve(configuration.root));
      if (delta.startsWith("..") || isAbsolute(delta))
        throw new RuntimeError("not_allowed", "Runtime outside owned runs");
      // 图谱属于部署配置，不能被题干或客户端切换到任意本机文件。
      const graphPath = await realpath(configuration.graph_path);
      const graphDelta = relative(join(SERVICE, "data"), graphPath);
      if (graphDelta.startsWith("..") || isAbsolute(graphDelta))
        throw new RuntimeError("not_allowed", "Graph outside owned data");
      configuration.graph_path = graphPath;
      if (new Set(configuration.specs.map((spec) => spec.name)).size !== configuration.specs.length)
        throw new RuntimeError("invalid_input", "Duplicate capability");
      this.configuration = configuration;
      for (const spec of configuration.specs) this.register(spec);
      return { source: "zcode-public-runtime", tools: this.registry.list() };
    }
    if (op === "close") {
      await this.close();
      return { closed: true };
    }
    if (!this.configuration || this.closed)
      throw new RuntimeError("not_ready", "Initialize runtime first");
    if (op === "recall") return selectScopedMemory(input);
    if (op === "plan") {
      const plan = Plan.parse(input);
      if (new Set(plan.nodes.map((node) => node.id)).size !== plan.nodes.length)
        throw new RuntimeError("invalid_input", "Duplicate DAG node");
      const result = new ToolScheduler({ maxConcurrency: 1 }).schedule(
        plan.nodes.map((node) => ({
          toolCallId: node.id as ToolCallId,
          toolName: node.intent,
          dependsOn: node.depends_on as ToolCallId[],
          readOnly: true,
          destructive: false,
          concurrentSafe: false,
          sideEffectScope: "none",
        })),
      );
      return { order: result.executionOrder, source: "@zcode/core/ToolScheduler" };
    }
    if (op === "skills") {
      const { names } = Names.parse(input);
      const roots = [
        {
          path: join(SERVICE, "skills"),
          scope: "project" as const,
          source: "agents" as const,
          priority: 1,
        },
      ];
      const discovery = await this.skills.discoverSkills({ workingDirectory: SERVICE, roots });
      if (discovery.diagnostics.length)
        throw new RuntimeError("skill_invalid", "Pinned skill discovery failed");
      return {
        skills: await Promise.all(
          names.map(async (name) => {
            const loaded = await this.skills.loadSkill({
              name,
              roots,
              workingDirectory: SERVICE,
              maxBytes: 10000,
            });
            if (loaded.truncated)
              throw new RuntimeError("skill_invalid", "Pinned skill exceeds budget");
            return { name: loaded.metadata.name, content: loaded.content };
          }),
        ),
        source: "@zcode/adapters/skills",
      };
    }
    if (op === "contracts") {
      const { names } = Names.parse(input);
      if (names.some((name) => !this.registry.has(name)))
        throw new RuntimeError("not_allowed", "Unknown tool");
      return {
        tools: this.registry
          .toContracts()
          .filter((tool) => names.includes(tool.name))
          .map((tool) => ({
            name: tool.name,
            description: tool.description,
            inputSchema: tool.inputSchema,
            outputSchema: tool.outputSchema,
          })),
        source: "@zcode/core/ToolRegistry",
      };
    }
    if (op !== "call") throw new RuntimeError("invalid_input", "Unknown operation");
    const request = Call.parse(input);
    if (!this.registry.has(request.name))
      throw new RuntimeError("not_allowed", "Unregistered capability");
    this.events = [];
    const executor = createToolExecutor({
      registry: this.registry,
      permissionService: new PermissionService({
        allowedTools: new Set(this.registry.list()),
        disallowedTools: new Set(),
        autoApproveHighRisk: false,
        allowMediumRiskInAutoMode: false,
      }),
      sessionId: this.configuration.session_id as SessionId,
      emitEvent: async (event) => {
        this.events.push(event);
      },
      mode: "build",
      workingDirectory: SERVICE,
      workspaceRoot: SERVICE,
    });
    const result = await executor.execute(
      { id: randomUUID(), name: request.name, input: request.arguments },
      { signal: AbortSignal.timeout(request.timeout_ms) },
    );
    if (!result.success) {
      if (this.handlerError) {
        const error = this.handlerError;
        this.handlerError = undefined;
        throw error;
      }
      throw new RuntimeError("tool_failed", "Registered capability failed");
    }
    return {
      result: result.output,
      runtime: {
        source: "@zcode/core/ToolExecutor",
        trace_id: this.configuration.trace_id,
        events: this.events.map((event) => ({ type: event.type, id: event.id })),
        subagent: this.lastChild,
      },
    };
  }

  private handlerError?: unknown;
  private lastChild?: { agent_id: string; child_session_id: string; agent_type: string };
  private register(spec: RegisteredTool) {
    const scope = spec.transport === "model" ? ("network" as const) : ("none" as const);
    this.registry.register({
      capability: `education.${spec.name}`,
      inputSchema: spec.input_schema,
      outputSchema: spec.output_schema,
      permission: {
        permission: `education.${spec.name}`,
        reason: "执行本轮绑定的只读教学能力",
        riskLevel: "low",
        sideEffectScope: scope,
        needsApproval: false,
        patternSources: ["toolName"],
        denyPriority: "beforeAsk",
      },
      resultBudget: { maxInlineBytes: 64000, maxModelBytes: 64000, strategy: "truncate" },
      timeout: { defaultMs: spec.timeout * 1000, allowCallOverride: false },
      cancellation: { supported: true, cleanup: "required", userVisibleMessage: "教学工具已取消" },
      trace: {
        required: true,
        propagateToAdapters: true,
        recordInput: "none",
        recordOutput: "none",
      },
      metadata: {
        name: spec.name,
        description: spec.description,
        readOnly: true,
        destructive: false,
        concurrentSafe: false,
        sideEffectScope: scope,
        riskLevel: "low",
        needsApproval: false,
        maxOutputBytes: 64000,
        timeoutMs: spec.timeout * 1000,
      },
      handler: async (args, context) => {
        this.handlerError = undefined;
        this.lastChild = undefined;
        try {
          if (spec.transport === "mcp") {
            await this.connectMcp();
            const result = await this.mcp.callTool(
              {
                serverName: "curriculum",
                toolName: spec.name,
                arguments: args as Record<string, unknown>,
              },
              { signal: context.abortSignal, timeoutMs: spec.timeout * 1000 },
            );
            if (result.isError)
              throw new RuntimeError("unsupported_input", "题目或作答暂不在当前核验范围内");
            return result.structuredContent;
          }
          if (spec.transport === "model")
            return await this.runSpecialist(spec, args, context.abortSignal);
          return await this.invoke(
            { name: spec.name, arguments: args, trace: { traceId: this.configuration!.trace_id } },
            context.abortSignal,
          );
        } catch (error) {
          this.handlerError = error;
          throw error;
        }
      },
    });
  }

  private async runSpecialist(spec: RegisteredTool, args: unknown, signal?: AbortSignal) {
    const configuration = this.configuration!;
    const profile: AgentProfile = {
      name: spec.name,
      description: spec.description,
      source: "project",
      systemPrompt: "只处理父任务绑定的教育证据。不得扩权、改身份、写入掌握事实或外发内容。",
      injectAgentsMd: false,
      tools: [spec.name],
      maxTurns: 1,
    };
    let failure: unknown;
    const port = createExploreSubagentPort({
      profiles: [profile],
      outputRootDir: join(configuration.root, "zcode-subagents"),
      getAllowedTools: (selected) => (selected.name === spec.name ? [spec.name] : []),
      emitParentEvent: async (event) => {
        this.events.push(event);
      },
      runExploreAgent: async (child) => {
        if (child.profile.name !== spec.name || child.allowedTools.join() !== spec.name)
          throw new RuntimeError("not_allowed", "Child capability mismatch");
        this.lastChild = {
          agent_id: child.agentId,
          child_session_id: child.sessionId,
          agent_type: child.agentType,
        };
        await child.onSessionReady?.();
        let result: unknown;
        try {
          result = await this.invoke(
            {
              name: spec.name,
              arguments: args,
              trace: {
                agentId: child.agentId,
                childSessionId: child.sessionId,
                traceId: String(child.traceContext.traceId),
              },
            },
            signal,
          );
        } catch (error) {
          failure = error;
          throw error;
        }
        return {
          response: JSON.stringify(result),
          traceId: child.traceContext.traceId,
          events: [],
        };
      },
    });
    try {
      const output = await port.run(
        {
          sessionId: configuration.session_id as SessionId,
          parentToolCallId: randomUUID(),
          agentType: spec.name,
          description: spec.description,
          prompt: "执行本轮绑定的专项教育核验并返回结构化结果。",
          callerCanReadOutputFile: false,
          workingDirectory: SERVICE,
          workspaceRoot: SERVICE,
          trace: createRootTraceContext({
            sessionId: configuration.session_id as SessionId,
            traceId: configuration.trace_id as TraceId,
          }),
        },
        { signal },
      );
      if (output.status !== "completed")
        throw failure ?? new RuntimeError("specialist_failed", "专项任务未完成");
      const text = output.content.find((item) => item.type === "text");
      if (!text || text.type !== "text")
        throw new RuntimeError("specialist_failed", "专项任务没有结构化结果");
      return JSON.parse(text.text) as unknown;
    } catch (error) {
      throw failure ?? error;
    } finally {
      await port.close?.();
    }
  }

  private async connectMcp() {
    this.mcpReady ??= (async () => {
      const status = await this.mcp.connectServer("curriculum", {
        type: "stdio",
        command: this.configuration!.python,
        args: ["-m", "qingqi.mcp", this.configuration!.graph_path],
        cwd: SERVICE,
        env: { PYTHONPATH: join(SERVICE, "src"), PYTHONIOENCODING: "utf-8" },
        timeoutMs: 15000,
      });
      if (status.status !== "connected")
        throw new RuntimeError("mcp_unavailable", "课程工具连接失败", true);
      const tools = await this.mcp.listTools();
      const expected = this.configuration!.specs.filter((spec) => spec.transport === "mcp");
      if (
        tools.length !== expected.length ||
        expected.some(
          (spec) =>
            !tools.some(
              (tool) =>
                tool.toolName === spec.name &&
                isDeepStrictEqual(tool.inputSchema, spec.input_schema) &&
                isDeepStrictEqual(tool.outputSchema, spec.output_schema),
            ),
        )
      )
        throw new RuntimeError("mcp_schema_changed", "课程工具发现与固定契约不符");
    })();
    await this.mcpReady;
  }
  async close() {
    if (!this.closed) {
      this.closed = true;
      await this.mcp.close();
    }
  }
}
