"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import type { LessonWorkedQuestion, WorkedTomDe } from "@/features/lessons/types";

/**
 * Tóm đề (Cho/Tìm) của một dạng bài tập mẫu (thử 3/11/2026) — dùng chung cho giải cùng hình (GiaiCungHinh) và giải
 * từng bước không có hình (TomDeKhung). < 1280: dòng "Tìm" (≤ 4 dòng) dính đầu khối, chạm mở lớp đè (không xô trang — D2, N8);
 * ≥ 1280: thẻ Cho/Tìm ở lề phải dính theo (CSS `.bt-tomde*` trong globals.css).
 */

export function getTomDe(q: LessonWorkedQuestion): WorkedTomDe | undefined {
  return q.tom_de?.cho?.length || q.tom_de?.tim?.length ? q.tom_de : undefined;
}

export function TomDeBody({ tomDe }: { tomDe: WorkedTomDe }) {
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

/** Dòng "Tìm" + lớp đè Cho/Tìm/Đề đầy đủ (điện thoại). Đặt trong một khối dính (`.cc-sticky`) để lớp đè neo theo. */
export function TomDeBar({ tomDe, problemHtml, open, setOpen }: { tomDe: WorkedTomDe; problemHtml?: string; open: boolean; setOpen: (o: boolean) => void }) {
  // đề trong lớp đè: bỏ hình (SVG chép hai lần trùng id marker; dạng có hình thì hình đã dính sẵn)
  const deChu = (problemHtml ?? "").replace(/<figure[\s\S]*?<\/figure>/g, "");
  // "Tìm" xuống tối đa 4 dòng (HS ảo Đ8 5/11: một dòng cắt "…" ở cả 8 dạng L10 → mất cái cần tìm, C2). Đo chiều cao thanh
  // ghi vào --cc-tim của khối dính để hình co lại đúng phần thanh cao thêm: cả khối dính giữ nguyên cỡ (N8, N1).
  // Dài hơn nữa thì "…" cuối dòng 4; chạm mở lớp đè có đủ Cho/Tìm/Đề.
  const barRef = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    const bar = barRef.current;
    if (!bar) return;
    const measure = () => bar.parentElement?.style.setProperty("--cc-tim", `${Math.round(bar.offsetHeight)}px`);
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(bar);
    return () => ro.disconnect();
  }, []);
  return (
    <>
      <button ref={barRef} type="button" className="bt-tomde-bar" aria-expanded={open} onClick={() => setOpen(!open)}>
        <span>
          {/* "Tìm:" nằm trong dòng chữ (không chiếm cột riêng) để mỗi dòng chứa nhiều chữ hơn; nbsp giữ "a)" với chữ sau
              nó và "·" với ý trước nó → dòng mới luôn mở đầu bằng một ý trọn "b) …" */}
          <b>Tìm: </b>
          <ContentHtml html={tomDe.tim.map((x) => x.replace(/^([a-dA-D]\))\s+/, "$1\u00a0")).join("\u00a0· ")} className="inline" />
        </span>
        <i aria-hidden="true">{open ? "▲" : "Đề ▼"}</i>
      </button>
      {open && (
        <div className="bt-tomde bt-tomde-pop">
          <TomDeBody tomDe={tomDe} />
          <h4>Đề đầy đủ</h4>
          <ContentHtml html={deChu} className="block" />
          <button type="button" className="bt-tomde-close" onClick={() => setOpen(false)}>
            Đóng
          </button>
        </div>
      )}
    </>
  );
}

/** Thẻ Cho/Tìm ở lề phải (≥ 1280; nhỏ hơn thì CSS ẩn). Phải là con trực tiếp của `.cc-split`. */
export function TomDeSide({ tomDe, top }: { tomDe: WorkedTomDe; top: number }) {
  return (
    <aside className="bt-tomde bt-tomde-side" style={{ top }} aria-label="Tóm đề">
      <TomDeBody tomDe={tomDe} />
    </aside>
  );
}

/** Đáy các thanh dính/cố định ở đầu trang (navbar, header bài) — để khối dính ngay dưới chúng. */
export function useStickyTop() {
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

/** Bọc lời giải từng bước của dạng KHÔNG có hình (`cong_cu`): dòng "Tìm" dính đầu khối + thẻ lề. Không có tom_de thì để nguyên. */
export function TomDeKhung({ q, children }: { q: LessonWorkedQuestion; children: ReactNode }) {
  const tomDe = getTomDe(q);
  const [open, setOpen] = useState(false);
  const top = useStickyTop();
  if (!tomDe) return <>{children}</>;
  return (
    <div className="cc-split bt-tomde-khung">
      <div className="cc-sticky" style={{ top }}>
        <TomDeBar tomDe={tomDe} problemHtml={q.problem_html} open={open} setOpen={setOpen} />
      </div>
      <TomDeSide tomDe={tomDe} top={top} />
      <div>{children}</div>
    </div>
  );
}
