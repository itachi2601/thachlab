"use client";

import { useEffect, useRef, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import StepwiseSolution from "@/components/lessons/StepwiseSolution";
import GiaoThoaHaiNguon from "@/components/lessons/cong-cu/GiaoThoaHaiNguon";
import type { LessonWorkedQuestion, WorkedTool } from "@/features/lessons/types";

/**
 * Giải từng bước CÙNG hình (thầy góp ý 2/11/2026): trên điện thoại hình dính nửa trên màn hình, em làm từng bước ở
 * nửa dưới — làm bước nào thấy ngay hình của bước đó, không phải cuộn qua lại (N8 split-attention, Chandler & Sweller).
 * Mỗi lần chỉ một bước (N5); lời giải đầy đủ gập ở dưới cùng. Hình của bước chỉ vẽ khi em đã làm xong bước đó.
 * Mọi bước có câu hỏi đều tự làm (fading giau_het, thầy chốt 2/11 sau góp ý học sinh ảo: "4/6 bước chỉ đọc đáp số").
 */

function Hinh({ tool, layer }: { tool: WorkedTool; layer: number }) {
  if (tool.loai === "giao_thoa_2_nguon") return <GiaoThoaHaiNguon {...tool} layer={layer} />;
  return null;
}

/** Đáy các thanh dính/cố định ở đầu trang (navbar, header bài) — để hình dính ngay dưới chúng. */
function useStickyTop() {
  const [top, setTop] = useState(0);
  useEffect(() => {
    let raf = 0;
    const measure = () => {
      raf = 0;
      let t = 0;
      document.querySelectorAll<HTMLElement>("header, nav, .lesson-head").forEach((el) => {
        const cs = getComputedStyle(el), r = el.getBoundingClientRect();
        if ((cs.position === "sticky" || cs.position === "fixed") && r.top <= 1 && r.height > 0 && r.height < 200) t = Math.max(t, r.bottom);
      });
      setTop(Math.round(t));
    };
    const onScroll = () => {
      if (!raf) raf = requestAnimationFrame(measure);
    };
    measure();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      cancelAnimationFrame(raf);
    };
  }, []);
  return top;
}

export default function GiaiCungHinh({
  q,
  tool,
  color,
  jump,
  onAllOpen,
}: {
  q: LessonWorkedQuestion;
  tool: WorkedTool;
  color: string;
  jump: { idx: number; n: number } | null;
  onAllOpen: () => void;
}) {
  const n = q.buoc?.length ?? 0;
  const [step, setStep] = useState(0);
  const [opened, setOpened] = useState(0); // số bước đầu đã làm xong liên tiếp
  const [full, setFull] = useState(false);
  const top = useStickyTop();
  const splitRef = useRef<HTMLDivElement>(null);

  // gỡ rối từ bài tương tự: nhảy về đúng bước
  const [seenJump, setSeenJump] = useState(jump);
  if (jump !== seenJump) {
    setSeenJump(jump);
    if (jump) setStep(Math.min(Math.max(jump.idx, 0), n - 1));
  }

  const go = (i: number) => {
    setStep(i);
    // đưa hình về đúng chỗ (đỉnh khung ngay dưới thanh dính) để bước mới hiện ngay dưới hình, không bị hình che
    const dy = (splitRef.current?.getBoundingClientRect().top ?? top) - top;
    if (Math.abs(dy) > 4) window.scrollTo({ top: window.scrollY + dy, behavior: "instant" });
  };
  const layer = Math.min(opened, step + 1);
  const canNext = step + 1 < n && step + 1 <= opened;
  const title = q.buoc?.[step]?.tieu_de ?? "";
  // một dòng cố định dưới nút: nói vì sao ▶ khoá / đã mở / đã xong (L1 phản hồi, D2 nút không nhảy chỗ)
  const hint =
    step + 1 >= n
      ? opened >= n
        ? "✓ Xong cả bài — tự trình bày lại, rồi so với lời giải đầy đủ ở cuối."
        : "Trả lời bước này để hoàn thành."
      : canNext
        ? step + 1 === opened
          ? "Xong bước này — bấm ▶ sang bước tiếp."
          : "Bấm ▶ xem lại bước sau."
        : "Trả lời câu hỏi bên dưới để mở bước sau.";

  return (
    <div ref={splitRef} className="cc-split">
      <div className={full ? "cc-sticky cc-sticky--off" : "cc-sticky"} style={{ top }}>
        <Hinh tool={tool} layer={layer} />
        <div className="cc-stepper">
          <button type="button" aria-label="Bước trước" disabled={step <= 0} onClick={() => go(step - 1)}>
            ◀
          </button>
          <span className="cc-step-title">
            Bước {step + 1}/{n} · <ContentHtml html={title} className="inline" />
          </span>
          <button
            type="button"
            aria-label="Bước sau"
            disabled={!canNext}
            className={canNext && step + 1 === opened ? "cc-next-ready" : undefined}
            style={canNext ? { borderColor: color, color } : undefined}
            onClick={() => go(step + 1)}
          >
            ▶
          </button>
        </div>
        <p className="cc-hint" aria-live="polite">
          {hint}
        </p>
      </div>
      <div className="cc-steps">
        <StepwiseSolution q={q} color={color} jump={jump} onAllOpen={onAllOpen} onProgress={setOpened} only={step} fading="giau_het" />
      </div>
      <div className="bt-meo">
        <button type="button" className="bt-meo-head" aria-expanded={full} onClick={() => setFull((o) => !o)}>
          <span>Lời giải đầy đủ</span>
          <span aria-hidden="true">{full ? "▲" : "▼"}</span>
        </button>
        {full && (
          <div className="bt-meo-body">
            <ContentHtml html={q.solution_html ?? ""} className="block leading-relaxed" />
          </div>
        )}
      </div>
    </div>
  );
}
