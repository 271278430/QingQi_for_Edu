import { useEffect, useRef, useState } from "react";

export function useTeachingAnimation(duration: number) {
  const [progress, setProgress] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [target, setTarget] = useState(1);
  const [reduced, setReduced] = useState(false);
  const current = useRef(0);
  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => {
      setReduced(media.matches);
      if (media.matches) setPlaying(false);
    };
    update();
    media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);
  useEffect(() => {
    if (!playing || reduced) return;
    const start = performance.now(),
      from = current.current;
    const direction = target >= from ? 1 : -1;
    let frame = 0;
    const tick = (now: number) => {
      const position = from + (direction * (now - start)) / (duration * 1000);
      const next = direction > 0 ? Math.min(target, position) : Math.max(target, position);
      current.current = next;
      setProgress(next);
      if (next === target) setPlaying(false);
      else frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [playing, reduced, duration, target]);
  const seek = (value: number) => {
    const next = Math.max(0, Math.min(1, value));
    current.current = next;
    setProgress(next);
    setPlaying(false);
  };
  const toggle = () => {
    if (playing) setPlaying(false);
    else {
      setTarget(1);
      if (current.current === 1) {
        current.current = 0;
        setProgress(0);
      }
      setPlaying(true);
    }
  };
  const playTo = (value: number) => {
    const next = Math.max(0, Math.min(1, value));
    if (reduced || Math.abs(next - current.current) < 1e-9) {
      seek(next);
      return;
    }
    // 同一个进度owner负责向前/向后播放相邻教学段，不新增播放器状态副本。
    setTarget(next);
    setPlaying(true);
  };
  return {
    progress,
    playing,
    reduced,
    seek,
    toggle,
    playTo,
    pause: () => setPlaying(false),
  };
}
export type AnimationState = ReturnType<typeof useTeachingAnimation>;
