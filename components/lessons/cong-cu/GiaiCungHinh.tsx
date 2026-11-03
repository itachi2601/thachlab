"use client";

import { useEffect, useRef, useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import StepwiseSolution from "@/components/lessons/StepwiseSolution";
import GiaoThoaHaiNguon from "@/components/lessons/cong-cu/GiaoThoaHaiNguon";
import SoDoVecto from "@/components/lessons/cong-cu/SoDoVecto";
import type { LessonWorkedQuestion, WorkedTomDe, WorkedTool } from "@/features/lessons/types";

/**
 * Giải từng bước CÙNG hình (thầy góp ý 2/11/2026): trên điện thoại hình dính nửa trên màn hình, em làm từng bước ở
 * nửa dưới — làm bước nào thấy ngay hình của bước đó, không phải cuộn qua lại (N8 split-attention, Chandler & Sweller).
 * Mỗi lần chỉ một bước (N5); lời giải đầy đủ gập ở dưới cùng. Hình của bước chỉ vẽ khi em đã làm xong bước đó.
 * Mọi bước có câu hỏi đều tự làm (fading giau_het, thầy chốt 2/11 sau góp ý học sinh ảo: "4/6 bước chỉ đọc đáp số").
 */

function Hinh({ tool, layer }: { tool: WorkedTool; layer: number }) {
  if (tool.loai === "giao_thoa_2_nguon") return <GiaoThoaHaiNguon {...tool} layer={layer} />;
  if (tool.loai === "so_do_vecto" || tool.loai === "thanh_moment") return <SoDoVecto {...tool} layer={layer} />;
  return null;
}

function TomDeBody({ tomDe }: { tomDe: WorkedTomDe }) {
  return (
    <>
      <h4>Cho</h4>
      <ul>
        {tomDe.cho.map((x, i) => (
          <li key={i}>
            <ContentHtml html={x} className="inline" />
          </li>
        ))}
      </ul>
      <h4>Tìm</h4>
      <ul>
        {tomDe.tim.map((x, i) => (
          <li key={i}>
            <ContentHtml html={x} className="inline" />
          </li>
        ))}
      </ul>
    </>
  );
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
  const [deOpen, setDeOpen] = useState(false); // tóm đề mở đè lên (điện thoại)
  const top = useStickyTop();
  const splitRef = useRef<HTMLDivElement>(null);

  // gỡ rối từ bài tương tự: nhảy về đúng bước
  const [seenJump, setSeenJump] = useState(jump);
  if (jump !== seenJump) {
    setSeenJump(jump);
    if (jump) setStep(Math.min(Math.max(jump.idx, 0), n - 1));
  }

  // đưa hình về đúng chỗ (đỉnh khung ngay dưới thanh dính) để bước hiện ngay dưới hình, không bị hình che
  const align = () => {
    const dy = (splitRef.current?.getBoundingClientRect().top ?? top) - top;
    if (Math.abs(dy) > 4) window.scrollTo({ top: window.scrollY + dy, behavior: "instant" });
  };
  const go = (i: number) => {
    setStep(i);
    setDeOpen(false);
    align();
  };

  // Vừa trả lời đúng bước đang làm: lời giải ngắn của bước hiện ở đầu khung bước. Nếu lúc gõ trang đã cuộn (bàn phím
  // điện thoại đẩy ô nhập lên) thì phần đó nằm dưới hình dính → cuộn về cho thấy (HS ảo 2/11: "lời giải bị đẩy khỏi tầm mắt").
  const prevOpened = useRef(opened);
  useEffect(() => {
    const was = prevOpened.current;
    prevOpened.current = opened;
    if (opened <= was || opened !== step + 1) return;
    const el = document.activeElement;
    if (el instanceof HTMLElement && splitRef.current?.contains(el)) el.blur(); // đóng bàn phím trước khi đo
    const fix = () => {
      const stick = splitRef.current?.querySelector(".cc-sticky")?.getBoundingClientRect().bottom ?? 0;
      const stepsTop = splitRef.current?.querySelector(".cc-steps")?.getBoundingClientRect().top ?? stick;
      if (stepsTop < stick - 4) align();
    };
    const t = setTimeout(fix, 60), t2 = setTimeout(fix, 450); // lần 2: sau khi bàn phím đóng, khung nhìn đổi cỡ
    return () => {
      clearTimeout(t);
      clearTimeout(t2);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [opened]);
  const layer = Math.min(opened, step + 1);
  const tomDe = q.tom_de?.cho?.length || q.tom_de?.tim?.length ? q.tom_de : undefined;
  // đề trong lớp đè: bỏ hình mô phỏng (đã có hình dính; SVG chép hai lần trùng id marker)
  const deChu = (q.problem_html ?? "").replace(/<figure[\s\S]*?<\/figure>/g, "");
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
        {/* Tóm đề (thử 3/11): một dòng "Tìm" ở ĐẦU khối dính (thầy 3/11: để dưới nút thì bị thanh điều hướng đáy che) — số liệu "Cho" đã nằm trên hình (N4); chạm thì đè lên, trang không xô (D2, N8) */}
        {tomDe && (
          <button type="button" className="bt-tomde-bar" aria-expanded={deOpen} onClick={() => setDeOpen((o) => !o)}>
            <b>Tìm:</b>
            <span>
              <ContentHtml html={tomDe.tim.join(" · ")} className="inline" />
            </span>
            <i aria-hidden="true">{deOpen ? "▲" : "Đề ▼"}</i>
          </button>
        )}
        {tomDe && deOpen && (
          <div className="bt-tomde bt-tomde-pop">
            <TomDeBody tomDe={tomDe} />
            <h4>Đề đầy đủ</h4>
            <ContentHtml html={deChu} className="block" />
            <button type="button" className="bt-tomde-close" onClick={() => setDeOpen(false)}>
              Đóng
            </button>
          </div>
        )}
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
      {tomDe && (
        <aside className="bt-tomde bt-tomde-side" style={{ top }} aria-label="Tóm đề">
          <TomDeBody tomDe={tomDe} />
        </aside>
      )}
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
