import { useCallback, useEffect, useRef, useState } from "react";
import { resolveTheme, useTheme } from "@zcode/ui/useTheme";
import { useZCodeIntl } from "@zcode/ui/intl";
import type {
  Bootstrap,
  Detail,
  EducationService,
  Message,
  Session,
  TeachingRequest,
  HistoricalPractice,
  PracticeAssignment,
  TutorImage,
  TeachingScope,
  TeachingStopResult,
} from "./contract.js";
import type { ImageDraft } from "./tutor-extras.js";
import { EducationRequestError } from "./contract.js";
import { errorText, retryBlocked } from "./format.js";
import {
  createChatComposerAttachment,
  serializeChatComposerAttachment,
  revokeChatComposerAttachment,
} from "@zcode/ui/chat-attachments";
import type { AnnotatedImage } from "./visual-annotation.js";
import { useChatModels } from "./use-chat-models.js";
type TeachingJob = { session: string; request: TeachingRequest };
type ActiveTurn = { job?: TeachingJob };
export function useEducationWorkspace(service: EducationService) {
  const [boot, setBoot] = useState<Bootstrap | null>(null);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [detail, setDetail] = useState<Detail | null>(null);
  const [view, setView] = useState("chat");
  const [question, setQuestion] = useState("");
  const [draftImages, setDraftImages] = useState<ImageDraft[]>([]);
  const [imagePreparing, setImagePreparing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [stopping, setStopping] = useState(false);
  const activeTurn = useRef<ActiveTurn | null>(null);
  const [openingSession, setOpeningSession] = useState(false);
  const [initializing, setInitializing] = useState(true);
  const [error, setError] = useState("");
  const [streamDraft, setStreamDraft] = useState("");
  const [streamStatus, setStreamStatus] = useState("");
  const [streamScope, setStreamScope] = useState<TeachingScope>();
  const [requestErrorCode, setRequestErrorCode] = useState<string>();
  const [pending, setPending] = useState<{
    session: string;
    request: TeachingRequest;
  } | null>(null);
  const [sideOpen, setSideOpen] = useState(false);
  const [historySearch, setHistorySearch] = useState("");
  const [showHistoryAll, setShowHistoryAll] = useState(false);
  const chatModels = useChatModels(
    service,
    boot?.profile || "",
    detail?.session.id || "",
    boot?.authenticated === true,
  );
  useEffect(() => {
    document.title = `${boot?.settings?.app_name || "清启"} · 学习工作台`;
  }, [boot?.settings?.app_name]);
  const { theme, setTheme } = useTheme();
  const { locale, setLocale } = useZCodeIntl();
  const dark = resolveTheme(theme) === "dark";
  // 教育文案和数学教学目前只有完整中文版本；不能用局部导航翻译冒充完整英文产品。
  useEffect(() => {
    if (locale !== "zh-CN") setLocale("zh-CN");
  }, [locale, setLocale]);
  const setDark = (next: boolean) => setTheme(next ? "zai-dark" : "zai-light");
  const generation = useRef(0);
  const selection = useRef(0);
  const bottom = useRef<HTMLDivElement>(null);
  const labels = {
    chat: "个性化辅导",
    path: "学习路径",
    dashboard: "学情看板",
    practice: "个性化练习",
    new: "新建学习对话",
    title: "学习工作台",
  };
  const refresh = useCallback(
    async (current: number) => {
      const a = await service.get<{ sessions: Session[] }>("/api/sessions");
      if (generation.current === current) setSessions(a.sessions);
      return a.sessions;
    },
    [service],
  );
  const initialize = useCallback(async () => {
    const current = ++generation.current;
    setError("");
    setInitializing(true);
    try {
      const value = await service.get<Bootstrap>("/api/bootstrap");
      if (generation.current !== current) return;
      service.setCsrf(value.csrf);
      setBoot(value);
      if (value.authenticated) {
        const list = await refresh(current);
        const firstSession = list[0];
        if (firstSession && generation.current === current) {
          const first = await service.get<Detail>(
            `/api/session?id=${encodeURIComponent(firstSession.id)}`,
          );
          if (generation.current === current) setDetail(first);
        }
      }
    } catch (e) {
      if (generation.current === current) setError(errorText(e));
    } finally {
      if (generation.current === current) setInitializing(false);
    }
  }, [service, refresh]);
  useEffect(() => {
    const lifecycle = generation;
    void initialize();
    return () => {
      // 生命周期计数器使卸载前发出的异步响应失效；它不是DOM ref。
      lifecycle.current++;
    };
  }, [initialize]);
  useEffect(() => {
    const list = bottom.current?.parentElement;
    const viewport = list?.closest<HTMLElement>(".edu-messages");
    if (!list || !viewport || view !== "chat") return;
    let follow = true;
    const scroll = () => {
      if (follow) viewport.scrollTop = viewport.scrollHeight;
    };
    // 图形懒加载后高度仍会变化；只在跟随底部时调整，不能把学生从历史阅读处拉走。
    const wheel = (e: WheelEvent) => {
      if (e.deltaY < 0) follow = false;
    };
    const stop = () => {
      follow = false;
    };
    const key = (e: KeyboardEvent) => {
      if (["ArrowUp", "PageUp", "Home"].includes(e.key)) follow = false;
    };
    const moved = () => {
      if (
        viewport.scrollHeight - viewport.clientHeight - viewport.scrollTop <
        32
      )
        follow = true;
    };
    const observer = new ResizeObserver(scroll);
    observer.observe(list);
    scroll();
    viewport.addEventListener("wheel", wheel, { passive: true });
    viewport.addEventListener("touchstart", stop, { passive: true });
    viewport.addEventListener("keydown", key);
    viewport.addEventListener("scroll", moved, { passive: true });
    return () => {
      observer.disconnect();
      viewport.removeEventListener("wheel", wheel);
      viewport.removeEventListener("touchstart", stop);
      viewport.removeEventListener("keydown", key);
      viewport.removeEventListener("scroll", moved);
    };
  }, [detail?.messages.length, busy, view]);
  useEffect(() => {
    const closeDrawers = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setSideOpen(false);
      }
    };
    document.addEventListener("keydown", closeDrawers);
    return () => document.removeEventListener("keydown", closeDrawers);
  }, []);
  const clearProjection = useCallback(() => {
    activeTurn.current = null;
    setStopping(false);
    selection.current++;
    setDetail(null);
    setOpeningSession(false);
    setSessions([]);
    setPending(null);
    setQuestion("");
    setDraftImages([]);
    setImagePreparing(false);
    setHistorySearch("");
    setShowHistoryAll(false);
    setError("");
  }, []);
  const historyCleared = useCallback(() => {
    // 清理成功即失效旧会话与回包，防止已删除的消息重新进入当前页面。
    const current = ++generation.current;
    clearProjection();
    setRequestErrorCode(undefined);
    setStreamDraft("");
    setStreamStatus("");
    setStreamScope(undefined);
    setBusy(false);
    void refresh(current).catch((e) => {
      if (generation.current === current) setError(errorText(e));
    });
  }, [clearProjection, refresh]);
  const openSession = async (id: string, draftQuestion = "") => {
    const current = generation.current;
    const seq = ++selection.current;
    // 会话读取完成前旧detail仍存在；锁定输入，防止新草稿发给旧会话。
    setOpeningSession(true);
    setError("");
    setStreamDraft("");
    setStreamScope(undefined);
    setRequestErrorCode(undefined);
    setView("chat");
    setSideOpen(false);
    try {
      const value = await service.get<Detail>(
        `/api/session?id=${encodeURIComponent(id)}`,
      );
      if (generation.current === current && selection.current === seq) {
        setDetail(value);
        setQuestion(draftQuestion);
        setPending(null);
        setDraftImages([]);
        return true;
      }
    } catch (e) {
      if (generation.current === current) setError(errorText(e));
    } finally {
      if (generation.current === current && selection.current === seq)
        setOpeningSession(false);
    }
    return false;
  };
  const newSession = async () => {
    if (busy) return;
    const current = generation.current;
    // 新会话接受前锁定输入，避免图片草稿被稍后返回的新会话响应清掉。
    setBusy(true);
    setError("");
    try {
      const value = await service.post<Session>("/api/sessions", {});
      if (generation.current === current) {
        selection.current++;
        setDetail({ session: value, messages: [] });
        setPending(null);
        setDraftImages([]);
        setView("chat");
        setSideOpen(false);
        await refresh(current);
      }
    } catch (e) {
      if (generation.current === current) setError(errorText(e));
    } finally {
      if (generation.current === current) setBusy(false);
    }
  };
  const switchProfile = async (profile: string) => {
    const current = ++generation.current;
    clearProjection();
    setBusy(true);
    try {
      const value = await service.post<Bootstrap>("/api/profile", { profile });
      if (generation.current === current) {
        service.setCsrf(value.csrf);
        setBoot(value);
        setView("chat");
        await refresh(current);
      }
    } catch (e) {
      if (generation.current === current) setError(errorText(e));
    } finally {
      if (generation.current === current) setBusy(false);
    }
  };
  const attachAnnotation = async ({ file, reference }: AnnotatedImage) => {
    if (busy || openingSession || imagePreparing || pending)
      throw new Error("当前请求处理中，请完成后再返回标注。");
    if (draftImages.length >= 3)
      throw new Error("输入框已有三张图片，请先移除一张。");
    if (
      draftImages.some(
        (image) =>
          image.visualContext &&
          image.visualContext.run_id !== reference.run_id,
      )
    )
      throw new Error("请分别讨论不同题目的标注。");
    const current = generation.current,
      selected = selection.current;
    const attachment = createChatComposerAttachment(file);
    setImagePreparing(true);
    try {
      const value = await serializeChatComposerAttachment(attachment);
      // 异步闭包中的detail仍是旧值；用会话选择序号防止标注落入刚切换的会话。
      if (current !== generation.current || selected !== selection.current)
        throw new Error("学习会话已切换，标注没有添加到其他会话。");
      if (value.kind !== "image" || !value.dataBase64)
        throw new Error("标注图片无法读取，笔迹已保留。");
      setDraftImages((images) => [
        ...images,
        {
          requestId: attachment.id,
          name: value.filename.slice(0, 80),
          dataUrl: `data:${value.mimeType};base64,${value.dataBase64}`,
          visualContext: reference,
        },
      ]);
      setQuestion(
        (q) =>
          q ||
          "我在这张教学图上做了标注，请结合原题讨论标记的位置，先给我一点提示。",
      );
    } finally {
      revokeChatComposerAttachment(attachment);
      if (current === generation.current) setImagePreparing(false);
    }
  };
  const send = async (
    retry = false,
    recovered?: { session: string; request: TeachingRequest },
  ) => {
    if (
      activeTurn.current ||
      busy ||
      initializing ||
      openingSession ||
      imagePreparing ||
      (!retry && chatModels.blocked) ||
      (!retry && !question.trim() && !draftImages.length)
    )
      return;
    if (retry && !recovered && retryBlocked(requestErrorCode)) return;
    // 同步在途引用只关联当前发送，防止同一帧双击越过 React 的 busy 更新。
    const turn: ActiveTurn = {};
    activeTurn.current = turn;
    const current = generation.current,
      selected = selection.current;
    const isCurrent = () =>
      current === generation.current &&
      selected === selection.current &&
      activeTurn.current === turn;
    let job = recovered ?? (retry ? pending : null);
    setBusy(true);
    setError("");
    setStreamDraft("");
    setStreamStatus("正在识别本次教学任务…");
    setStreamScope(undefined);
    setRequestErrorCode(undefined);
    try {
      if (recovered) setPending(recovered);
      if (!job) {
        const modelSelection = chatModels.snapshot();
        // 先登记会话，再上传附件；上传期间预选的模型保存到实际会话，不丢在旧的空会话草稿里。
        let session = detail?.session;
        if (!session) {
          session = await service.post<Session>("/api/sessions", {
            model_selection: modelSelection,
          });
          if (!isCurrent()) return;
          setDetail({ session, messages: [] });
        }
        const imageIds: string[] = [];
        for (const image of draftImages) {
          const accepted = image.uploadedId
            ? { id: image.uploadedId }
            : await service.post<TutorImage>("/api/tutor/images", {
                request_id: image.requestId,
                name: image.name,
                data_url: image.dataUrl,
              });
          if (!isCurrent()) return;
          imageIds.push(accepted.id);
          setDraftImages((value) =>
            value.map((item) =>
              item.requestId === image.requestId
                ? { ...item, uploadedId: accepted.id }
                : item,
            ),
          );
        }
        job = {
          session: session.id,
          request: {
            request_id: crypto.randomUUID(),
            question:
              question.trim() ||
              "请引导我理解这张题目图片，先不要直接给最终答案。",
            mode: "auto",
            model_selection: modelSelection,
            ...(imageIds.length ? { images: imageIds } : {}),
            ...(draftImages.find((image) => image.visualContext)?.visualContext
              ? {
                  visual_context: draftImages.find(
                    (image) => image.visualContext,
                  )!.visualContext,
                }
              : {}),
          },
        };
        setPending(job);
      }
      turn.job = job;
      const value = service.stream
        ? await service.stream<{ session: Detail }>(
            "/api/teach",
            job,
            (event) => {
              // 流文字是临时投影；仅同一generation可更新，done的Store投影才成为历史。
              if (!isCurrent()) return;
              if (event.kind === "scope" && event.scope) {
                setStreamScope({
                  ...event.scope,
                  active_part: event.part ?? event.scope.active_part,
                });
                setStreamStatus(`正在辅导第（${event.part}）问`);
              }
              if (event.kind === "progress")
                setStreamStatus(event.text || "正在思考…");
              if (event.kind === "reset") setStreamDraft(event.text || "");
              if (event.kind === "delta")
                setStreamDraft((text) => text + (event.text || ""));
            },
          )
        : await service.post<{ session: Detail }>("/api/teach", job);
      if (isCurrent()) {
        setDetail(value.session);
        setPending(null);
        setQuestion("");
        setDraftImages([]);
        setStreamDraft("");
        setStreamStatus("");
        setStreamScope(undefined);
        await refresh(current);
      }
    } catch (e) {
      if (isCurrent()) {
        setError(
          e instanceof EducationRequestError && e.code === "turn_cancelled"
            ? ""
            : errorText(e),
        );
        setRequestErrorCode(
          e instanceof EducationRequestError ? e.code : undefined,
        );
        // 已知回复格式失败不能重发同编号；保留文字和图片，让学生编辑新问题。
        if (
          e instanceof EducationRequestError &&
          [
            "model_protocol",
            "model_truncated",
            "model_changed",
            "turn_cancelled",
          ].includes(e.code)
        )
          setPending(null);
        // 失败消息也由Store投影接管，避免只看见上一轮回复；读失败时保留当前流式草稿。
        if (job) {
          try {
            const snapshot = await service.get<Detail>(
              `/api/session?id=${encodeURIComponent(job.session)}`,
            );
            if (isCurrent()) {
              setDetail(snapshot);
              if (
                snapshot.messages.some(
                  (item) =>
                    item.request_id === job?.request.request_id &&
                    item.partial_response,
                )
              ) {
                setStreamDraft("");
                setStreamScope(undefined);
              }
            }
          } catch {
            /* 原失败原因优先，展示链路异常不能吞掉输入或草稿。 */
          }
        }
      }
    } finally {
      const live = activeTurn.current === turn;
      if (live) activeTurn.current = null;
      if (live && current === generation.current) {
        setBusy(false);
        setStopping(false);
        setStreamStatus("");
      }
    }
  };
  const stopCurrent = async () => {
    const turn = activeTurn.current;
    if (!turn?.job || stopping) return;
    setStopping(true);
    try {
      const result = await service.post<TeachingStopResult>(
        "/api/teach/stop",
        turn.job,
      );
      if (activeTurn.current === turn)
        setStreamStatus(
          result.status === "completed" ? "回复已完成。" : "正在停止生成…",
        );
    } catch (e) {
      if (activeTurn.current === turn) {
        setError(errorText(e));
        setStopping(false);
      }
    }
  };
  const stopMessage = async (item: Message) => {
    if (
      !detail ||
      busy ||
      openingSession ||
      activeTurn.current ||
      !item.trace.running
    )
      return;
    const current = generation.current,
      seq = selection.current;
    const turn: ActiveTurn = {
      job: { session: detail.session.id, request: item.original_input },
    };
    activeTurn.current = turn;
    setBusy(true);
    setStopping(true);
    setError("");
    const live = () =>
      activeTurn.current === turn &&
      current === generation.current &&
      seq === selection.current;
    try {
      await service.post<TeachingStopResult>("/api/teach/stop", turn.job);
      for (let n = 0; n < 40; n++) {
        const snapshot = await service.get<Detail>(
          `/api/session?id=${encodeURIComponent(detail.session.id)}`,
        );
        if (!live()) return;
        setDetail(snapshot);
        const target = snapshot.messages.find(
          (m) => m.request_id === item.request_id,
        );
        if (!target?.trace.running) {
          if (target?.trace.error_code === "turn_cancelled") {
            if (pending?.request.request_id === item.request_id)
              setPending(null);
            setRequestErrorCode("turn_cancelled");
          }
          return;
        }
        await new Promise((resolve) => setTimeout(resolve, 200));
      }
      if (live())
        setError("停止请求已接受，任务仍在退出；稍后重新打开会话查看结果。");
    } catch (e) {
      if (live()) setError(errorText(e));
    } finally {
      if (live()) {
        activeTurn.current = null;
        setBusy(false);
        setStopping(false);
      }
    }
  };
  const pickHistorical = async (item: HistoricalPractice) => {
    if (busy || openingSession || pending) return;
    const current = generation.current;
    const seq = selection.current;
    // 选题准入期间锁定输入，避免选题和旧会话发送同时完成后互相覆盖。
    setBusy(true);
    try {
      const session =
        item.session ||
        (
          await service.post<PracticeAssignment>("/api/practice/start", {
            item_id: item.item.id,
            request_id: crypto.randomUUID(),
          })
        ).session;
      if (current !== generation.current || seq !== selection.current) return;
      const draft =
        item.source === "对话推荐"
          ? "这道题我想先自己试试，请先给一点提示。"
          : "返回原练习，我想复习这道历史题，请先和我讨论解题思路。";
      if (await openSession(session, draft)) {
        await refresh(current);
        if (item.source === "对话推荐" && current === generation.current)
          setView("practice");
      }
    } finally {
      if (current === generation.current) setBusy(false);
    }
  };
  const messages = detail?.messages ?? [];
  const resumeMessage = (item: Message) => {
    // 展示投影可能补充已解析的算式；恢复必须使用原提交，避免输入指纹变化被拒绝。
    if (detail && !item.response && !retryBlocked(item.trace.error_code))
      void send(true, {
        session: detail.session.id,
        request: item.original_input,
      });
  };
  const restartMessage = (item: Message) => {
    if (
      !detail ||
      chatModels.blocked ||
      item.response ||
      !["model_truncated", "turn_cancelled"].includes(
        item.trace.error_code || "",
      )
    )
      return;
    // 明确重新回答是新尝试，不能重放已截断的付费调用；原题和标注引用保持不变。
    void send(true, {
      session: detail.session.id,
      request: {
        ...item.original_input,
        model_selection: chatModels.snapshot(),
        request_id: crypto.randomUUID(),
      },
    });
  };
  const repeatStudentTask = (item: Message) => {
    if (!detail || chatModels.blocked || !item.response?.task_notice) return;
    // 旧失败结果保持原样；学生点击后以当前配置发起一个有新编号的查询。
    void send(true, {
      session: detail.session.id,
      request: {
        ...item.original_input,
        model_selection: chatModels.snapshot(),
        request_id: crypto.randomUUID(),
      },
    });
  };

  return {
    chatModels,
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
    busy: busy || initializing || openingSession,
    openingSession,
    streamDraft,
    streamStatus,
    streamScope,
    error,
    requestErrorCode,
    retryAllowed: !retryBlocked(requestErrorCode),
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
  };
}
