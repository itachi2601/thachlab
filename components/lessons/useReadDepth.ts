"use client";

import { useEffect, useRef } from "react";
import { logReadDepth } from "@/services/learning-events";

/**
 * Đo một lượt đọc mục lý thuyết: mốc <h3> sâu nhất (1-based) đã vào màn hình khi đang mở, và số câu
 * `.tl-quiz` đã bấm (khoá = `name` của radio, như TheoryRpBar). Không gọi mạng lúc tải — chỉ gửi khi
 * ẩn tab hoặc đóng/rời mục, qua hàng đợi log_learning_events.
 */
export function useReadDepth(opts: {
  itemId: number;
  active: boolean;
  h3Total: number;
  quizTotal: number;
  rootRef: React.RefObject<HTMLElement | null>;
  /** Đổi khi danh sách đoạn đang mở đổi → quan sát lại. */
  openKey: string;
}) {
  const { itemId, active, h3Total, quizTotal, rootRef, openKey } = opts;
  const h3Max = useRef(0);
  const quizNames = useRef<Set<string>>(new Set());
  const sent = useRef("");

  // Gửi khi ẩn tab / rời mục; bỏ qua nếu chưa đọc gì hoặc số không đổi từ lần gửi trước.
  useEffect(() => {
    if (!active) return;
    h3Max.current = 0;
    quizNames.current = new Set();
    sent.current = "";
    const send = () => {
      // Câu đã chọn từ lượt trước được ContentHtml khôi phục mà không phát `change` → gom thêm từ DOM.
      rootRef.current
        ?.querySelectorAll<HTMLInputElement>('.tl-quiz input[type="radio"]:checked')
        .forEach((r) => r.name && quizNames.current.add(r.name));
      const quizDone = quizNames.current.size;
      if (h3Max.current === 0 && quizDone === 0) return;
      const key = `${h3Max.current}/${quizDone}`;
      if (key === sent.current) return;
      sent.current = key;
      logReadDepth({ itemId, h3Max: h3Max.current, h3Total, quizDone, quizTotal });
    };
    const onVisibility = () => {
      if (document.visibilityState === "hidden") send();
    };
    document.addEventListener("visibilitychange", onVisibility);
    window.addEventListener("pagehide", send);
    return () => {
      document.removeEventListener("visibilitychange", onVisibility);
      window.removeEventListener("pagehide", send);
      send();
    };
  }, [active, itemId, h3Total, quizTotal, rootRef]);

  useEffect(() => {
    const root = rootRef.current;
    if (!root || !active || quizTotal === 0) return;
    const onChange = (e: Event) => {
      const input = e.target as HTMLInputElement | null;
      if (input?.type === "radio" && input.name && input.closest(".tl-quiz")) quizNames.current.add(input.name);
    };
    root.addEventListener("change", onChange);
    return () => root.removeEventListener("change", onChange);
  }, [rootRef, active, quizTotal]);

  useEffect(() => {
    const root = rootRef.current;
    if (!root || !active || h3Total === 0) return;
    const targets = Array.from(root.querySelectorAll<HTMLElement>('.theory-section[data-open="1"]'));
    if (targets.length === 0) return;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (!e.isIntersecting) continue;
          const idx = Number((e.target as HTMLElement).dataset.index);
          if (Number.isInteger(idx) && idx + 1 > h3Max.current) h3Max.current = Math.min(idx + 1, h3Total);
        }
      },
      // Mốc tính là "đã tới" khi đầu đoạn vào nửa trên màn hình, giống vùng ghi vị trí đọc của TheoryBlock.
      { rootMargin: "0px 0px -50% 0px", threshold: 0 },
    );
    targets.forEach((t) => observer.observe(t));
    return () => observer.disconnect();
  }, [rootRef, active, h3Total, openKey]);
}
