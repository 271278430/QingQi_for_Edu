import { useEffect, useRef, useState } from "react";
import { Button } from "@zcode/ui/button";
import { Input } from "@zcode/ui/input";
import { Textarea } from "@zcode/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@zcode/ui/dialog";
import { Settings, Network, RefreshCw, Save } from "lucide-react";
import type {
  EducationService,
  ManagementOverview,
  SystemSettings,
  HistoryClearResult,
} from "./contract.js";
import { EducationRequestError } from "./contract.js";
import { ArchitecturePanel } from "./architecture-panel.js";
import { ModelSettingsPanel } from "./model-settings.js";
import { errorText } from "./format.js";

export function SettingsPanel({
  service,
  canManage,
  dark,
  setDark,
  onSettings,
  onHistoryCleared,
  onModelsChanged,
}: {
  service: EducationService;
  canManage: boolean;
  dark: boolean;
  setDark: (v: boolean) => void;
  onSettings: (s: SystemSettings) => void;
  onHistoryCleared: () => void;
  onModelsChanged: () => void;
}) {
  const [tab, setTab] = useState("system");
  const [data, setData] = useState<ManagementOverview>();
  const [draft, setDraft] = useState<SystemSettings>();
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [revision, setRevision] = useState(0);
  const [pending, setPending] = useState<(SystemSettings & { request_id: string }) | null>(null);
  const [confirmClear, setConfirmClear] = useState(false);
  const [clearMessage, setClearMessage] = useState("");
  const [clearError, setClearError] = useState("");
  const [pendingClear, setPendingClear] = useState<{
    request_id: string;
    scope: "project";
  } | null>(null);
  const mounted = useRef(true);
  const acceptedVersion = useRef(-1);
  const inFlight = useRef(false);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  useEffect(() => {
    if (!canManage) return;
    const controller = new AbortController();
    setError("");
    service
      .get<ManagementOverview>("/api/settings", controller.signal)
      .then((value) => {
        if (!controller.signal.aborted && value.settings.version >= acceptedVersion.current) {
          acceptedVersion.current = value.settings.version;
          setData(value);
          // 同版本的后台刷新只更新状态，不能抹掉学生尚未提交的设置草稿。
          setDraft((current) =>
            current?.version === value.settings.version ? current : value.settings,
          );
          onSettings(value.settings);
        }
      })
      .catch((e) => {
        if (!controller.signal.aborted) setError(errorText(e));
      });
    return () => controller.abort();
  }, [service, canManage, revision, onSettings]);
  const save = async () => {
    if (!draft || inFlight.current || pendingClear) return;
    inFlight.current = true;
    const command = pending ?? { ...draft, request_id: crypto.randomUUID() };
    setPending(command);
    setBusy(true);
    setError("");
    setMessage("");
    try {
      const value = await service.post<SystemSettings>("/api/settings", command);
      acceptedVersion.current = value.version;
      // Store已接受的设置须通知工作区；用户离开子页不撤销已完成的写入。
      onSettings(value);
      if (!mounted.current) return;
      setPending(null);
      setDraft(value);
      setData((d) => (d ? { ...d, settings: value } : d));
      setMessage("设置已保存并生效。");
    } catch (e) {
      if (!mounted.current) return;
      if (
        e instanceof EducationRequestError &&
        e.code !== "invalid_response" &&
        [400, 403, 409].includes(e.status)
      )
        setPending(null);
      if (e instanceof EducationRequestError && e.code !== "invalid_response" && e.status === 409)
        setRevision((r) => r + 1);
      setError(errorText(e));
    } finally {
      inFlight.current = false;
      if (mounted.current) setBusy(false);
    }
  };
  const clearHistory = async () => {
    if (inFlight.current || pending) return;
    inFlight.current = true;
    const command = pendingClear ?? {
      request_id: crypto.randomUUID(),
      scope: "project" as const,
    };
    setPendingClear(command);
    setBusy(true);
    setClearError("");
    try {
      const result = await service.post<HistoryClearResult>("/api/settings/history/clear", command);
      onHistoryCleared();
      if (!mounted.current) return;
      setPendingClear(null);
      setConfirmClear(false);
      setClearMessage(
        result.already_applied ? "此前清理已完成，后来新建的记录已保留。" : "全部学习历史已清空。",
      );
      setRevision((r) => r + 1);
    } catch (e) {
      if (!mounted.current) return;
      // 明确拒绝没有副作用；未知网络结果须保留编号，重放不能再次清除新对话。
      if (
        e instanceof EducationRequestError &&
        e.code !== "invalid_response" &&
        [400, 403, 409].includes(e.status)
      )
        setPendingClear(null);
      setClearError(errorText(e));
    } finally {
      inFlight.current = false;
      if (mounted.current) setBusy(false);
    }
  };
  return (
    <div className="edu-settings p-5 md:p-8" aria-label="设置管理后台">
      <div className="mb-5">
        <h2 className="text-ui-xl font-semibold">设置管理</h2>
        <p className="mt-1 text-ui-caption text-foreground-subtle">
          学习界面设置、系统运行状态与项目架构。
        </p>
      </div>
      <div className="mb-5 flex flex-wrap gap-2" role="tablist" aria-label="设置分类">
        <Button
          role="tab"
          aria-selected={tab === "system"}
          variant={tab === "system" ? "secondary" : "ghost"}
          onClick={() => setTab("system")}
        >
          <Settings />
          系统管理
        </Button>
        {canManage && (
          <Button
            role="tab"
            aria-selected={tab === "models"}
            variant={tab === "models" ? "secondary" : "ghost"}
            onClick={() => setTab("models")}
          >
            模型适配
          </Button>
        )}
        {canManage && (
          <Button
            role="tab"
            aria-selected={tab === "architecture"}
            variant={tab === "architecture" ? "secondary" : "ghost"}
            onClick={() => setTab("architecture")}
          >
            <Network />
            项目架构
          </Button>
        )}
      </div>
      {tab === "models" && canManage ? (
        <ModelSettingsPanel
          service={service}
          onChanged={() => {
            setRevision((r) => r + 1);
            onModelsChanged();
          }}
        />
      ) : tab === "architecture" && canManage ? (
        <ArchitecturePanel service={service} />
      ) : (
        <div className="grid gap-5 lg:grid-cols-2">
          <section className="edu-card space-y-4">
            <h3 className="text-ui-lg font-semibold">界面偏好</h3>
            <div className="flex flex-wrap gap-2">
              <Button variant={!dark ? "secondary" : "outline"} onClick={() => setDark(false)}>
                浅色主题
              </Button>
              <Button variant={dark ? "secondary" : "outline"} onClick={() => setDark(true)}>
                深色主题
              </Button>
            </div>
          </section>
          {canManage && (
            <section className="edu-card space-y-4">
              <div className="flex items-center justify-between gap-2">
                <h3 className="text-ui-lg font-semibold">产品与服务设置</h3>
                <Button
                  variant="ghost"
                  disabled={busy || !!pending || !!pendingClear}
                  onClick={() => {
                    setMessage("");
                    setRevision((r) => r + 1);
                  }}
                >
                  <RefreshCw />
                  刷新设置
                </Button>
              </div>
              {draft ? (
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    void save();
                  }}
                  className="space-y-4"
                >
                  <label className="block text-ui-base">
                    产品名称
                    <Input
                      aria-label="产品名称"
                      className="mt-2"
                      value={draft.app_name}
                      maxLength={30}
                      disabled={busy || !!pending || !!pendingClear}
                      onChange={(e) => setDraft({ ...draft, app_name: e.target.value })}
                    />
                  </label>
                  <label className="block text-ui-base">
                    服务公告
                    <Textarea
                      aria-label="服务公告"
                      className="mt-2"
                      value={draft.notice}
                      maxLength={160}
                      disabled={busy || !!pending || !!pendingClear}
                      onChange={(e) => setDraft({ ...draft, notice: e.target.value })}
                    />
                  </label>
                  <label className="flex items-center gap-2 text-ui-base">
                    <input
                      type="checkbox"
                      aria-label="暂停新学习操作"
                      checked={draft.maintenance}
                      disabled={busy || !!pending}
                      onChange={(e) => setDraft({ ...draft, maintenance: e.target.checked })}
                    />
                    暂停新学习操作
                  </label>
                  <p className="text-ui-caption text-foreground-subtle">
                    开启后可继续查看已有记录，新的辅导和练习提交会暂停；在这里关闭即可恢复。
                  </p>
                  <Button type="submit" disabled={busy || !!pendingClear || !draft.app_name.trim()}>
                    <Save />
                    {busy ? "正在保存…" : pending ? "重试保存" : "保存设置"}
                  </Button>
                  {pending && !busy && (
                    <p className="text-ui-caption text-foreground-subtle">
                      请重试本次保存以确认结果。
                    </p>
                  )}
                </form>
              ) : (
                <p className="text-ui-caption">正在读取设置…</p>
              )}
              {error && (
                <p role="alert" className="text-ui-base text-destructive">
                  {error}
                </p>
              )}
              {message && (
                <p role="status" className="text-ui-base text-success">
                  {message}
                </p>
              )}
            </section>
          )}
          {canManage && data && (
            <section className="edu-card space-y-4 lg:col-span-2">
              <h3 className="text-ui-lg font-semibold">系统与数据状态</h3>
              <div className="grid gap-3 sm:grid-cols-3">
                {[
                  ["已加载数学图谱节点", data.catalogue.graph_nodes],
                  ["学情主题", data.catalogue.topics],
                  ["题库候选（含变式）", data.catalogue.questions],
                ].map(([label, value]) => (
                  <div key={label} className="rounded-lg border border-border p-3">
                    <p className="text-ui-caption text-foreground-subtle">{label}</p>
                    <p className="mt-1 text-ui-lg font-semibold">{value}</p>
                  </div>
                ))}
              </div>
              <p className="text-ui-caption text-foreground-subtle">
                其中筛选源题 {data.catalogue.source_items} 道，系统规则变式{" "}
                {data.catalogue.generated_items} 道；当前学生的完整可练题{" "}
                {data.catalogue.student_ready_items}{" "}
                道。节点数属于已加载数学索引，学情主题不等于图谱全量知识节点。
              </p>
              <p className="text-ui-caption">
                <strong>当前入口配置：</strong>
                {data.deployment?.label || "正在更新配置状态"}
              </p>
              <p className="text-ui-caption">
                已接入工具框架：{data.runtime}。具体调用以本轮轨迹为准。
              </p>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-ui-caption">
                  <thead>
                    <tr>
                      <th className="p-2">模型职责</th>
                      <th className="p-2">模型</th>
                      <th className="p-2">配置状态</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.models.map((m) => (
                      <tr key={m.id}>
                        <td className="p-2">{m.label}</td>
                        <td className="p-2">{m.model || "未配置"}</td>
                        <td className="p-2">
                          {m.enabled
                            ? m.credential_ready
                              ? "已配置，凭据就绪"
                              : "已启用，凭据未就绪"
                            : "未启用"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="text-ui-caption text-foreground-subtle">
                凭据就绪仅表示对应环境变量存在，未实时探测模型健康；不表示每轮都调用全部模型。Flash同时负责识图和自然对话。学情中的历史画像为示例初始化，新作答证据按学生隔离保存。
              </p>
              <details>
                <summary className="cursor-pointer text-ui-caption">当前学习空间的运行记录</summary>
                <p className="mt-2 text-ui-caption">
                  辅导请求 {data.counts.runs} · 记忆事件 {data.counts.episodes} · 练习任务{" "}
                  {data.counts.practice_assignments}
                </p>
                {data.recent_errors.map((e) => (
                  <p key={e.run_id} className="mt-1 text-ui-caption">
                    请求 {e.run_id}：{e.code}
                  </p>
                ))}
              </details>
            </section>
          )}
          {canManage && (
            <section className="edu-card space-y-3 lg:col-span-2">
              <h3 className="text-ui-lg font-semibold">学习历史管理</h3>
              <p className="text-ui-caption text-foreground-subtle">
                清空这个项目所有账户的学习会话、消息、作答、上传图片、对话记忆和工具/模型调用记录。两个服务入口共享同一份数据。教材、题库、初始学情画像和系统设置保留；导入历史会话与历史题不再展示。
              </p>
              <Button
                variant="outline"
                disabled={busy || !!pending}
                onClick={() => {
                  setClearError("");
                  setConfirmClear(true);
                }}
              >
                {pendingClear ? "重试清空历史" : "清空全部历史"}
              </Button>
              {clearMessage && (
                <p role="status" className="text-ui-base text-success">
                  {clearMessage}
                </p>
              )}
              {data?.history.suppress_imported && (
                <p className="text-ui-xs text-foreground-subtle">
                  历史导入已停用，重启不会重新生成已清理的历史。
                </p>
              )}
            </section>
          )}
        </div>
      )}
      <Dialog
        open={confirmClear}
        onOpenChange={(next) => {
          if (!busy) setConfirmClear(next);
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>清空全部学习历史</DialogTitle>
            <DialogDescription>
              这会删除本项目所有账户的学习历史及相关记忆，教材、题库和初始学情画像保留。删除后无法从页面恢复。
            </DialogDescription>
          </DialogHeader>
          {clearError && (
            <p role="alert" className="text-ui-base text-destructive">
              {clearError}
            </p>
          )}
          <div className="flex justify-end gap-2">
            <Button variant="outline" disabled={busy} onClick={() => setConfirmClear(false)}>
              取消
            </Button>
            <Button
              variant="destructive"
              disabled={busy || !!pending}
              onClick={() => void clearHistory()}
            >
              {busy ? "正在清空…" : "确认清空"}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
