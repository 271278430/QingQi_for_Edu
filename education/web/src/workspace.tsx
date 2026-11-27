import { Button } from "@zcode/ui/button";
import { Textarea } from "@zcode/ui/textarea";
import { Input } from "@zcode/ui/input";
import { lazy, Suspense, useCallback } from "react";
import { ZCodeIntlProvider } from "@zcode/ui/intl";
import { TooltipProvider } from "@zcode/ui/tooltip";
import { EducationSelect } from "./controls.js";
import {
  BookOpen,
  Check,
  Clock,
  ChevronDown,
  FileText,
  GraduationCap,
  LoaderCircle,
  Menu,
  MessageSquare,
  Moon,
  Plus,
  RefreshCw,
  Search,
  Sun,
  X,
  Settings,
} from "lucide-react";
import type { EducationService, SystemSettings } from "./contract.js";

import { Login } from "./pages.js";
import { LearningPanel } from "./learning.js";
import { MathContent } from "./learning-content.js";
import { TutorExtras } from "./tutor-extras.js";
import { TutorMessageImages } from "./tutor-message-images.js";
import { errorText } from "./format.js";
import { useEducationWorkspace } from "./use-workspace.js";
import { SettingsPanel } from "./settings-panel.js";
import { ComposerModels } from "./composer-models.js";
import { ComposerActions } from "./composer-actions.js";
import { TurnStatus } from "./turn-status.js";
import { TutorReplyContent, tutoringLabel } from "./student-task-results.js";

// 共享消息模块含数学、代码与图表插件；按需加载，避免空白工作台预载全部模块。
const loadMessages = () => import("@zcode/ui/message");
const Message = lazy(() =>
  loadMessages().then((module) => ({ default: module.Message })),
);
const MessageContent = lazy(() =>
  loadMessages().then((module) => ({ default: module.MessageContent })),
);

export function EducationWorkspace({ service }: { service: EducationService }) {
  return (
    <ZCodeIntlProvider>
      {/* 上游代码块按钮依赖 Tooltip 上下文；缺失时整条 Markdown 会被错误边界降级。 */}
      <TooltipProvider>
        <EducationWorkspaceContent service={service} />
      </TooltipProvider>
    </ZCodeIntlProvider>
  );
}

function EducationWorkspaceContent({ service }: { service: EducationService }) {
  const {
    boot,
    setBoot,
    sessions,
    detail,
    view,
    setView,
    question,
    setQuestion,
    draftImages,
    setDraftImages,
    imagePreparing,
    setImagePreparing,
    pickHistorical,
    busy,
    openingSession,
    streamDraft,
    streamStatus,
    streamScope,
    error,
    requestErrorCode,
    retryAllowed,
    setError,
    pending,
    setPending,
    sideOpen,
    setSideOpen,
    historySearch,
    setHistorySearch,
    showHistoryAll,
    setShowHistoryAll,
    dark,
    setDark,
    theme,
    generation,
    bottom,
    labels,
    refresh,
    initialize,
    clearProjection,
    historyCleared,
    newSession,
    openSession,
    switchProfile,
    send,
    stopping,
    stopCurrent,
    stopMessage,
    attachAnnotation,
    messages,
    resumeMessage,
    restartMessage,
    repeatStudentTask,
    chatModels,
  } = useEducationWorkspace(service);
  const { load: reloadChatModels } = chatModels;
  const updateSystemSettings = useCallback(
    (value: SystemSettings) => {
      setBoot((current) =>
        current ? { ...current, settings: value } : current,
      );
    },
    [setBoot],
  );
  const updateModelCapabilities = useCallback(() => {
    void reloadChatModels();
    void service
      .get<{
        models: NonNullable<typeof boot>["models"];
        mode: NonNullable<typeof boot>["mode"];
      }>("/api/bootstrap")
      .then((value) =>
        setBoot((current) =>
          current
            ? { ...current, models: value.models, mode: value.mode }
            : current,
        ),
      )
      .catch((e) => setError(errorText(e)));
  }, [service, setBoot, setError, reloadChatModels]);
  // 同题旧记录只在默认列表合并展示；全部历史与搜索保留每一条真实会话。
  const uniqueHistory = sessions.filter(
    (item, index) =>
      !item.practice_item ||
      sessions.findIndex(
        (other) => other.practice_item === item.practice_item,
      ) === index,
  );
  const history = historySearch.trim()
    ? sessions.filter((item) =>
        item.title
          .toLocaleLowerCase()
          .includes(historySearch.trim().toLocaleLowerCase()),
      )
    : showHistoryAll
      ? sessions
      : uniqueHistory.slice(0, 6);
  if (!boot)
    return (
      <div className="grid min-h-dvh place-items-center bg-background p-8 text-ui-base text-foreground">
        <div className="text-center">
          <GraduationCap className="mx-auto mb-4 size-8" />
          <p>{error || "正在打开清启学习工作台…"}</p>
          {error && (
            <Button className="mt-4" onClick={() => void initialize()}>
              <RefreshCw />
              重新连接
            </Button>
          )}
        </div>
      </div>
    );
  if (!boot.authenticated)
    return (
      <Login
        service={service}
        onSuccess={(value) => {
          service.setCsrf(value.csrf);
          setBoot(value);
          void refresh(generation.current).catch((e) => setError(errorText(e)));
        }}
        error={error}
      />
    );
  return (
    <div className="education text-ui-base">
      {sideOpen && (
        <button
          type="button"
          className="edu-nav-backdrop"
          aria-label="关闭导航遮罩"
          tabIndex={-1}
          onClick={() => setSideOpen(false)}
        />
      )}
      <aside id="edu-sidebar" className="edu-sidebar" data-open={sideOpen}>
        <div className="flex items-center gap-3">
          <span className="edu-logo">
            <GraduationCap className="size-5" />
          </span>
          <div>
            <h1 className="text-ui-lg font-semibold">
              {boot.settings?.app_name || "清启"}
            </h1>
            <p className="text-ui-xs text-foreground-subtlest">
              个性化学习助手
            </p>
          </div>
          <Button
            className="edu-mobile-button ml-auto"
            variant="ghost"
            size="icon"
            aria-label="关闭导航"
            onClick={() => setSideOpen(false)}
          >
            <X />
          </Button>
        </div>
        <Button
          variant="outline"
          size="lg"
          className="w-full justify-start"
          onClick={() => void newSession()}
          disabled={busy}
        >
          <Plus />
          {labels.new}
        </Button>
        <nav className="space-y-1" aria-label="主导航">
          {[
            ["chat", MessageSquare, labels.chat],
            ["path", BookOpen, labels.path],
            ["dashboard", Clock, labels.dashboard],
            ["practice", FileText, labels.practice],
          ].map(([key, Icon, label]) => {
            const NavIcon = Icon as typeof MessageSquare;
            return (
              <Button
                key={String(key)}
                variant={view === key ? "secondary" : "ghost"}
                size="lg"
                className="w-full justify-start gap-3"
                aria-current={view === key ? "page" : undefined}
                onClick={() => {
                  setView(String(key));
                  setSideOpen(false);
                }}
              >
                <NavIcon />
                {String(label)}
              </Button>
            );
          })}
        </nav>
        <div
          className="min-h-0 flex-1 overflow-y-auto"
          role="region"
          aria-label="最近学习对话"
        >
          <p className="mb-3 px-2 text-ui-xs text-foreground-subtle">
            最近的学习对话
          </p>
          {!!sessions.length && (
            <label className="relative mb-3 block">
              <Search className="pointer-events-none absolute left-2 top-2.5 size-3.5 text-foreground-subtle" />
              <Input
                aria-label="搜索学习对话"
                placeholder="搜索学习对话"
                value={historySearch}
                className="pl-7 text-mobile-input-safe"
                onChange={(e) => setHistorySearch(e.target.value)}
              />
            </label>
          )}
          {sessions.length ? (
            history.map((item) => (
              <Button
                key={item.id}
                data-testid="history-item"
                title={item.title}
                variant={
                  detail?.session.id === item.id && view === "chat"
                    ? "secondary"
                    : "ghost"
                }
                size="lg"
                className="mb-1 w-full justify-start"
                disabled={busy}
                onClick={() => void openSession(item.id)}
              >
                <MessageSquare className="size-3.5" />
                <span className="truncate">{item.title}</span>
              </Button>
            ))
          ) : (
            <p className="px-2 text-ui-sm text-foreground-subtlest">
              开始对话后自动保存在这里。
            </p>
          )}
          {sessions.length > 6 && !historySearch.trim() && (
            <Button
              variant="ghost"
              size="sm"
              className="mt-2 w-full justify-start text-foreground-subtle"
              onClick={() => setShowHistoryAll(!showHistoryAll)}
            >
              <ChevronDown className={showHistoryAll ? "rotate-180" : ""} />
              {showHistoryAll ? "收起历史" : `全部历史 · ${sessions.length}`}
            </Button>
          )}
          {historySearch.trim() && !history.length && (
            <p className="px-2 text-ui-sm text-foreground-subtle">
              没有匹配的对话。
            </p>
          )}
        </div>
        <div className="space-y-3 border-t border-border pt-4">
          <Button
            className="w-full justify-start"
            variant={view === "settings" ? "secondary" : "ghost"}
            aria-current={view === "settings" ? "page" : undefined}
            onClick={() => {
              setView("settings");
              setSideOpen(false);
            }}
          >
            <Settings />
            设置管理
          </Button>
          {boot.demo && boot.profiles.length > 1 ? (
            <EducationSelect
              label="当前学习者"
              className="w-full"
              disabled={busy}
              value={boot.profile}
              onValueChange={(value) => void switchProfile(value)}
              options={boot.profiles.map((item) => ({
                value: item.id,
                label: item.name,
              }))}
            />
          ) : boot.demo ? (
            <p className="text-ui-sm text-foreground-subtle">{boot.name}</p>
          ) : (
            <div className="flex justify-between">
              <span>{boot.name}</span>
              <Button
                variant="ghost"
                disabled={busy}
                onClick={() => {
                  generation.current++;
                  clearProjection();
                  service
                    .post("/api/logout", {})
                    .then(() => initialize())
                    .catch((e) => setError(errorText(e)));
                }}
              >
                退出
              </Button>
            </div>
          )}
        </div>
      </aside>
      <main className="edu-main">
        <header className="edu-header">
          <div className="flex min-w-0 items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              className="edu-mobile-button"
              aria-label="打开导航"
              aria-expanded={sideOpen}
              aria-controls="edu-sidebar"
              onClick={() => setSideOpen(true)}
            >
              <Menu />
            </Button>
            <div className="min-w-0">
              <p className="truncate text-ui-lg font-medium">
                {view === "chat"
                  ? labels.title
                  : view === "settings"
                    ? "设置管理"
                    : labels[view as "path" | "dashboard" | "practice"]}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              aria-label={dark ? "切换浅色主题" : "切换深色主题"}
              onClick={() => setDark(!dark)}
            >
              {dark ? <Sun /> : <Moon />}
            </Button>
          </div>
        </header>
        {(boot.settings?.notice || boot.settings?.maintenance) && (
          <div
            className="mx-5 mt-3 rounded-md border border-border p-3 text-ui-caption"
            role="status"
          >
            {boot.settings.maintenance
              ? "系统维护中，已有学习记录可继续查看。 "
              : ""}
            {boot.settings.notice}
          </div>
        )}
        {error && (
          <div
            role="alert"
            className="mx-5 mt-4 flex flex-wrap items-center gap-3 rounded-md bg-destructive-surface p-3 text-ui-base text-destructive-surface-foreground"
          >
            <span className="flex-1">{error}</span>
            {requestErrorCode === "model_truncated" && (
              <Button
                variant="outline"
                disabled={busy}
                onClick={() => void send(false)}
              >
                <RefreshCw />
                重新回答
              </Button>
            )}
            {pending && retryAllowed && (
              <Button
                variant="outline"
                disabled={busy}
                onClick={() => void send(true)}
              >
                <RefreshCw />
                重试当前请求
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setError("");
                setPending(null);
              }}
            >
              关闭
            </Button>
          </div>
        )}
        {view === "chat" && (
          <div className="edu-body">
            <section className="edu-conversation">
              {openingSession && (
                <p
                  role="status"
                  className="mx-5 mt-3 text-ui-sm text-foreground-subtle"
                >
                  正在读取这段学习对话…
                </p>
              )}
              {detail?.practice && (
                <section
                  className="edu-question-reference"
                  aria-label="正在讨论的题目"
                >
                  <div className="mb-2 flex items-center justify-between gap-3">
                    <p className="text-ui-sm font-medium">
                      正在讨论 · {detail.practice.item.title}
                    </p>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setView("practice")}
                    >
                      返回练习
                    </Button>
                  </div>
                  <details open={!messages.length} key={detail.practice.id}>
                    <summary className="cursor-pointer text-ui-xs text-foreground-subtle">
                      原题与选项
                    </summary>
                    <div className="edu-question-content mt-2">
                      <MathContent content={detail.practice.item.expression} />
                      {detail.practice.item.options?.map((option, index) => (
                        <div className="mt-2 flex gap-2" key={index}>
                          <span className="text-ui-base">
                            {String.fromCharCode(65 + index)}.
                          </span>
                          <MathContent content={option} />
                        </div>
                      ))}
                    </div>
                  </details>
                  {detail.practice.item.usable === false && (
                    <p className="mt-2 text-ui-sm text-warning-surface-foreground">
                      {detail.practice.item.quality_note}
                    </p>
                  )}
                </section>
              )}
              <div className="edu-messages" aria-live="polite">
                <div className="edu-message-list">
                  <Suspense
                    fallback={
                      <p
                        className="text-ui-sm text-foreground-subtle"
                        role="status"
                      >
                        正在加载学习内容…
                      </p>
                    }
                  >
                    {!messages.length && !busy && (
                      <div className="mx-auto max-w-2xl pt-8">
                        <h2 className="text-ui-xl font-semibold">
                          把困惑说出来，一起找到下一步。
                        </h2>
                        <p className="mt-3 max-w-lg text-ui-base leading-relaxed text-foreground-subtle">
                          直接贴题目、说思路或告诉我哪里卡住了。我们可以一起想，也可以帮你核对答案。
                        </p>
                      </div>
                    )}
                    {messages.map((item) => (
                      <article className="edu-message" key={item.request_id}>
                        <Message from="user">
                          <MessageContent className="edu-user text-ui-base">
                            <TutorMessageImages images={item.images || []} />
                            <MathContent
                              theme={theme}
                              content={item.original_input.question}
                            />
                            {item.recognized_question && (
                              <details className="mt-3 border-t border-border pt-2">
                                <summary className="cursor-pointer text-ui-xs text-foreground-subtle">
                                  图片识别的题目 · 可在对话中纠正
                                </summary>
                                <div className="mt-2">
                                  <MathContent
                                    content={item.recognized_question}
                                  />
                                </div>
                              </details>
                            )}
                          </MessageContent>
                        </Message>
                        {item.response ? (
                          <Message from="assistant" className="mt-5">
                            <MessageContent className="w-full">
                              <div className="mb-3 flex items-center gap-2">
                                <span className="edu-logo size-6">
                                  <GraduationCap className="size-3.5" />
                                </span>
                                <span className="font-medium">清启</span>
                                {item.response.tutoring_scope && (
                                  <span className="text-ui-xs text-foreground-subtle">
                                    当前辅导第（
                                    {item.response.tutoring_scope.active_part}
                                    ）问
                                  </span>
                                )}
                                <span className="text-ui-xs text-foreground-subtlest">
                                  {tutoringLabel(item.response)}
                                </span>
                                {item.response.teaching_action ===
                                  "confirm" && (
                                  <Check className="size-3.5 text-success" />
                                )}
                              </div>
                              {/* 助手也走同一数学适配，避免原题正常而模型回复仍显示 $■$。 */}
                              <TutorReplyContent
                                response={item.response}
                                stepCount={item.input.steps?.length ?? 0}
                                theme={theme}
                                locked={
                                  busy ||
                                  openingSession ||
                                  imagePreparing ||
                                  Boolean(pending)
                                }
                                onRepeat={() => repeatStudentTask(item)}
                                onPick={pickHistorical}
                                onNavigate={setView}
                                onAnnotate={attachAnnotation}
                              />
                            </MessageContent>
                          </Message>
                        ) : (
                          <TurnStatus
                            item={item}
                            busy={busy}
                            stopping={stopping}
                            theme={theme}
                            onStop={() => void stopMessage(item)}
                            onResume={() => resumeMessage(item)}
                            onRestart={() => restartMessage(item)}
                          />
                        )}
                      </article>
                    ))}
                    {busy && (
                      <div className="edu-message text-ui-base">
                        {/* 刷新侧栏也会占用 busy；只有实际待提交输入才能显示为用户消息。 */}
                        {pending &&
                          !messages.some(
                            (item) =>
                              item.request_id === pending.request.request_id,
                          ) && (
                            <Message from="user">
                              <MessageContent className="edu-user">
                                {/* 临时气泡使用本次已上传草稿；接受后由历史消息接管，不能只显示文字。 */}
                                <TutorMessageImages
                                  images={draftImages
                                    .filter(
                                      (image) =>
                                        image.uploadedId &&
                                        pending.request.images?.includes(
                                          image.uploadedId,
                                        ),
                                    )
                                    .map((image) => ({
                                      id: image.requestId,
                                      name: image.name,
                                      url: image.dataUrl,
                                    }))}
                                />
                                <MathContent
                                  theme={theme}
                                  content={pending.request.question}
                                />
                              </MessageContent>
                            </Message>
                          )}
                        <p className="mt-5 flex items-center gap-2 text-foreground-subtle">
                          <LoaderCircle className="edu-spin size-4" />
                          {streamStatus ||
                            (pending
                              ? "正在核对问题与学习依据…"
                              : "正在更新学习对话…")}
                        </p>
                      </div>
                    )}
                  </Suspense>
                  {/* 临时流独立于历史消息的懒加载边界，首次打开也能立即看到真实增量。 */}
                  {!!streamDraft && (busy || !!requestErrorCode) && (
                    <div className="edu-message">
                      <div
                        data-testid="tutor-stream-draft"
                        className="edu-assistant"
                      >
                        <p className="mb-2 text-ui-caption text-foreground-subtle">
                          {!busy
                            ? "回复未完成"
                            : streamScope
                              ? `当前辅导第（${streamScope.active_part}）问`
                              : "清启正在回复"}
                        </p>
                        <MathContent
                          theme={theme}
                          content={streamDraft}
                          streaming={busy}
                        />
                      </div>
                    </div>
                  )}
                  <div ref={bottom} />
                </div>
              </div>
              <form
                className="edu-composer"
                onSubmit={(e) => {
                  e.preventDefault();
                  void send();
                }}
              >
                <label className="sr-only" htmlFor="edu-question">
                  你的学习问题
                </label>
                <TutorExtras
                  key={boot.profile}
                  service={service}
                  images={busy && pending ? [] : draftImages}
                  locked={busy || Boolean(pending)}
                  onPreparing={setImagePreparing}
                  onImages={(images) =>
                    setDraftImages((value) => [...value, ...images].slice(0, 3))
                  }
                  onRemove={(id) =>
                    setDraftImages((value) =>
                      value.filter((image) => image.requestId !== id),
                    )
                  }
                  onPick={pickHistorical}
                />
                <Textarea
                  id="edu-question"
                  aria-label="你的学习问题"
                  className="min-h-12 max-h-44 border-0 bg-transparent px-0 text-ui-base focus-visible:ring-0"
                  rows={2}
                  maxLength={2000}
                  placeholder="描述你的困惑，或贴出需要核对的题目…"
                  value={question}
                  disabled={busy || Boolean(pending)}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
                      e.preventDefault();
                      void send();
                    }
                  }}
                />
                <div className="mt-3 flex items-center justify-between gap-3 border-t border-border pt-3">
                  <ComposerModels
                    disabled={busy && !detail?.session}
                    models={chatModels}
                    canManage={boot.can_manage === true}
                    onManage={() => setView("settings")}
                  />
                  <ComposerActions
                    canStop={busy && Boolean(pending)}
                    stopping={stopping}
                    onStop={() => void stopCurrent()}
                    disabled={
                      busy ||
                      chatModels.blocked ||
                      imagePreparing ||
                      Boolean(pending) ||
                      (!question.trim() && !draftImages.length)
                    }
                  />
                </div>
              </form>
            </section>
          </div>
        )}
        {view === "settings" && (
          <SettingsPanel
            key={boot.profile}
            service={service}
            canManage={boot.can_manage === true}
            dark={dark}
            setDark={setDark}
            onSettings={updateSystemSettings}
            onHistoryCleared={historyCleared}
            onModelsChanged={updateModelCapabilities}
          />
        )}
        {view !== "chat" && view !== "settings" && (
          <LearningPanel
            key={boot.profile}
            view={view}
            service={service}
            onNavigate={setView}
            onChanged={() => {
              void refresh(generation.current).catch((e) =>
                setError(errorText(e)),
              );
            }}
            onTutor={async (assignment) => {
              await openSession(
                assignment.session,
                "返回原练习，请引导我思考这道题，先不要给最终答案。",
              );
            }}
          />
        )}
      </main>
    </div>
  );
}
