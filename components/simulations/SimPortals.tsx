"use client";

import { useEffect, useRef, useState, type RefObject } from "react";
import { createPortal } from "react-dom";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import { SIMULATIONS } from "./registry";

/**
 * Dựng mô phỏng React vào các thẻ giữ chỗ <div class="tl-sim" data-sim="id"> nằm trong HTML bài học.
 * HTML lưu DB không được chứa <script>, nên mô phỏng không nằm trong HTML mà là component có sẵn trong
 * repo; thẻ chỉ mang id. ContentHtml thay cả khối DOM khi KaTeX tải xong, nên MutationObserver quét lại
 * thẻ sau mỗi lần DOM đổi và gắn lại portal vào đúng nút mới. Chỉ mount khi thẻ cách màn hình < 300px.
 */
export default function SimPortals({ rootRef, htmlKey }: { rootRef: RefObject<HTMLElement | null>; htmlKey: string }) {
  const [slots, setSlots] = useState<HTMLElement[]>([]);
  const [near, setNear] = useState<Set<HTMLElement>>(() => new Set());
  const io = useRef<IntersectionObserver | null>(null);

  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    const scan = () => {
      const found = Array.from(root.querySelectorAll<HTMLElement>("[data-sim]")).filter((el) => el.dataset.sim && el.dataset.sim in SIMULATIONS);
      setSlots((prev) => (prev.length === found.length && prev.every((el, i) => el === found[i]) ? prev : found));
    };
    scan();
    const mo = new MutationObserver(scan);
    mo.observe(root, { childList: true, subtree: true });
    return () => mo.disconnect();
  }, [rootRef, htmlKey]);

  useEffect(() => {
    if (typeof IntersectionObserver === "undefined") {
      // trình duyệt quá cũ: mount luôn, không chờ cuộn tới
      const all = new Set(slots);
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setNear(all);
      return;
    }
    const obs = new IntersectionObserver(
      (entries) => {
        const hit = entries.filter((e) => e.isIntersecting).map((e) => e.target as HTMLElement);
        if (hit.length) setNear((prev) => new Set([...prev, ...hit]));
      },
      { rootMargin: "300px 0px" },
    );
    io.current = obs;
    slots.forEach((el) => obs.observe(el));
    return () => obs.disconnect();
  }, [slots]);

  return (
    <>
      {slots.map((el) => {
        const Sim = SIMULATIONS[el.dataset.sim ?? ""];
        if (!Sim || !near.has(el)) return null;
        return createPortal(
          <LazyErrorBoundary fallback={<p className="tl-sim__loading">Không tải được mô phỏng. Thử tải lại trang.</p>}>
            <Sim />
          </LazyErrorBoundary>,
          el,
          el.dataset.sim,
        );
      })}
    </>
  );
}
