"use client";

// Phiếu buổi CNC lớp đảo ngược (cnc_lessons id flip-1…flip-12, sinh từ content/lesson-samples/cnc-phieu-buoi/build.mjs).
// Một trang một buổi (N1): mục tiêu · tối trước (link #muc-N) · nhịp 300 phút · nộp cuối buổi · cổng.
// Chọn buổi bằng lưới 6×2 nút 44px (D2, D4 — lộ hết 12 buổi ở 360px), không tab cuộn ngang.
import { useEffect, useState } from "react";
import Link from "next/link";
import ContentHtml from "@/components/exams/ContentHtml";
import { fetchCncLesson, type CncLesson } from "@/services/cnc-lessons";

const SESSION_COUNT = 12;

function readSessionNo(): number {
  const n = Number(new URLSearchParams(window.location.search).get("so"));
  return Number.isInteger(n) && n >= 1 && n <= SESSION_COUNT ? n : 1;
}

export default function CncSessionSheet() {
  const [no, setNo] = useState<number | null>(null);
  const [sheet, setSheet] = useState<CncLesson | null | "error">(null);

  useEffect(() => {
    const sync = () => {
      setSheet(null);
      setNo(readSessionNo());
    };
    sync();
    window.addEventListener("popstate", sync);
    return () => window.removeEventListener("popstate", sync);
  }, []);

  useEffect(() => {
    if (no === null) return;
    let cancelled = false;
    fetchCncLesson(`flip-${no}`)
      .then((row) => !cancelled && setSheet(row ?? "error"))
      .catch(() => !cancelled && setSheet("error"));
    return () => {
      cancelled = true;
    };
  }, [no]);

  const choose = (n: number) => {
    window.history.pushState(null, "", `/lop-hoc/cnc/buoi/?so=${n}`);
    setSheet(null);
    setNo(n);
    window.scrollTo({ top: 0 });
  };

  return (
    <div className="cnc-shell lesson-shell lesson-shell--cttc">
      <div className="mx-auto w-full max-w-[680px] px-4 py-6">
        <Link href="/lop-hoc/cnc" className="lesson-link min-h-[44px]">
          ← Bài học Gia công CNC
        </Link>
        <nav aria-label="Chọn buổi" className="mt-2 grid grid-cols-6 gap-2">
          {Array.from({ length: SESSION_COUNT }, (_, i) => i + 1).map((n) => (
            <button
              key={n}
              type="button"
              aria-current={n === no ? "page" : undefined}
              onClick={() => choose(n)}
              className={`min-h-[44px] rounded-xl border text-sm font-semibold ${
                n === no ? "border-primary bg-primary/10 text-primary" : "border-line text-slate-500"
              }`}
            >
              {n}
            </button>
          ))}
        </nav>
        {sheet === null && <p className="mt-6 text-sm text-slate-500">Đang tải phiếu buổi…</p>}
        {sheet === "error" && <p className="mt-6 text-sm text-slate-500">Chưa có phiếu cho buổi này.</p>}
        {sheet && sheet !== "error" && (
          <article className="mt-5">
            <p className="text-sm font-semibold text-primary">Phiếu buổi · {sheet.duration}</p>
            <h1 className="mt-1 font-display text-xl font-semibold text-ink">{sheet.title}</h1>
            <ContentHtml html={sheet.bodyHtml} className="cnc-detailed-content cnc-session-sheet" />
          </article>
        )}
      </div>
    </div>
  );
}
