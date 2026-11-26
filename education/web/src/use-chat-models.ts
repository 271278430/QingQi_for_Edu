import { useCallback, useEffect, useRef, useState } from "react";
import type { ChatModelSelection, ChatModelsView, EducationService } from "./contract.js";
import { errorText } from "./format.js";

export function useChatModels(
  service: EducationService,
  profile: string,
  session: string,
  enabled: boolean,
) {
  const key = `${profile}:${session}`;
  const [state, setState] = useState<{ key: string; view: ChatModelsView }>();
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const sequence = useRef(0);
  const locked = useRef(false);
  const refreshQueued = useRef(false);
  const load = useCallback(async () => {
    if (locked.current) {
      refreshQueued.current = true;
      return;
    }
    const seq = ++sequence.current;
    setLoading(true);
    setError("");
    try {
      const view = await service.get<ChatModelsView>(
        `/api/chat/models?session=${encodeURIComponent(session)}`,
      );
      if (sequence.current === seq) setState({ key, view });
    } catch (e) {
      if (sequence.current === seq) setError(errorText(e));
    } finally {
      if (sequence.current === seq) setLoading(false);
    }
  }, [service, key, session]);
  useEffect(() => {
    const counter = sequence;
    locked.current = false;
    refreshQueued.current = false;
    setSaving(false);
    setLoading(false);
    if (enabled) void load();
    return () => {
      counter.current++;
    };
  }, [enabled, load]);
  const view = state?.key === key ? state.view : undefined;
  const save = async (selection: ChatModelSelection) => {
    if (!view || locked.current || loading) return;
    const seq = ++sequence.current;
    locked.current = true;
    setSaving(true);
    setError("");
    try {
      const accepted = await service.post<ChatModelsView>("/api/chat/models", {
        session,
        selection,
        version: view.version,
        request_id: crypto.randomUUID(),
      });
      if (seq === sequence.current) setState({ key, view: accepted });
    } catch (e) {
      // 保存结果未知时不能以旧选择继续发送；重新读取Owner确认，草稿仍保留。
      if (seq === sequence.current) setError(errorText(e));
    } finally {
      if (seq === sequence.current) {
        locked.current = false;
        setSaving(false);
        if (refreshQueued.current) {
          refreshQueued.current = false;
          void load();
        }
      }
    }
  };
  const snapshot = () => {
    if (!view || saving || loading || error || view.issues.length)
      throw new Error(error || "模型选择尚未就绪，请重新读取或选择模型。");
    // 与ZCode composerSubmissionConfig相同：上传前冻结本轮选择，不读取后来的菜单草稿。
    return Object.freeze(
      Object.fromEntries(
        Object.entries(view.selection).map(([role, choice]) => [
          role,
          Object.freeze({ ...choice }),
        ]),
      ),
    ) as ChatModelSelection;
  };
  return {
    view,
    saving,
    loading,
    error,
    load,
    save,
    snapshot,
    blocked: !view || saving || loading || !!error || !!view.issues.length,
  };
}
