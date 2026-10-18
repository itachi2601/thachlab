"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ChevronDown } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import QuestionCard from "@/components/exams/QuestionCard";
import { fetchMyLatestMistakes, type MistakeReviewItem } from "@/services/lessons";

/**
 * Các câu vừa sai kèm lời giải. Hai chỗ dùng, cùng một tên "Kho bẫy" (17/10/2026):
 *  - variant "vault": nằm trong thẻ Kho bẫy ở /luyen-tap (chỗ chính).
 *  - mặc định: khối thu gọn ở trang lớp, có link về Kho bẫy.
 */
export default function MistakeReviewPanel({ variant = "class" }: { variant?: "class" | "vault" }) {
  const { session } = useAuth();
  const [mistakes, setMistakes] = useState<MistakeReviewItem[] | null>(null);
  const [open, setOpen] = useState(false);
  const [visibleCount, setVisibleCount] = useState(5);

  useEffect(() => {
    if (!session) return;
    fetchMyLatestMistakes(session.user.id).then(setMistakes).catch(() => setMistakes([]));
  }, [session]);

  if (!session || !mistakes?.length) return null;
  const preview = Math.min(5, mistakes.length);
  const vault = variant === "vault";
  const listId = vault ? "vault-mistake-list" : "mistake-review-list";
  return (
    <section className={vault ? "mt-3 border-t border-line/60 pt-1" : "class-mistake"}>
      <button
        type="button"
        onClick={() => setOpen((current) => !current)}
        aria-expanded={open}
        aria-controls={listId}
        className={vault ? "flex min-h-11 w-full items-center justify-between gap-2 text-left text-sm font-semibold text-primary" : "class-mistake-toggle"}
      >
        <span>{vault ? `Xem lại ${preview} câu vừa sai (có lời giải)` : `Kho bẫy · Ôn ${preview} câu vừa sai`}</span>
        <ChevronDown size={18} className={open ? (vault ? "rotate-180 transition" : "is-open") : vault ? "transition" : ""} aria-hidden />
      </button>
      {!vault && (
        <Link href="/luyen-tap#kho-bay" className="inline-flex min-h-11 items-center text-sm text-primary hover:underline">
          Mở Kho bẫy để ôn cách quãng →
        </Link>
      )}
      {open && (
        <div id={listId} className="space-y-5 pb-2">
          {mistakes.slice(0, visibleCount).map((item) => (
            <div key={`${item.examId}-${item.questionIndex}`}>
              <p className="mb-2 text-sm font-semibold text-ink">{item.examTitle}</p>
              <QuestionCard index={item.questionIndex + 1} question={item.question} response={item.response} review />
            </div>
          ))}
          {visibleCount < mistakes.length && (
            <button type="button" onClick={() => setVisibleCount((count) => count + 5)} className="w-full rounded-xl border border-line px-4 py-3 text-sm font-semibold text-ink hover:border-line-strong">
              Xem thêm {Math.min(5, mistakes.length - visibleCount)} câu
            </button>
          )}
        </div>
      )}
    </section>
  );
}

/**
 * Chip một dòng ở trang lớp (18/10/2026, thay khối gập tại chỗ): "Kho bẫy · 5" → /luyen-tap#kho-bay.
 * Chưa có câu sai thì không hiện gì (N3).
 */
export function MistakeVaultChip() {
  const { session } = useAuth();
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!session) return;
    fetchMyLatestMistakes(session.user.id).then((rows) => setCount(rows.length)).catch(() => setCount(0));
  }, [session]);
  if (!session || count === 0) return null;
  // Số lớn (hàng trăm) không giúp em chọn gì, chỉ gây ngợp → trần 20+.
  const shown = count > 20 ? "20+" : String(count);
  return (
    <Link href="/luyen-tap#kho-bay" className="class-chip" title={`Ôn ${shown} câu vừa sai`}>
      Kho bẫy · {shown}
    </Link>
  );
}
