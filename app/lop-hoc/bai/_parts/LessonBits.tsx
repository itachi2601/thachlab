"use client";

import Link from "next/link";
import { Home } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { type LessonItem } from "@/features/lessons/types";

/** Vòng tiến độ bằng SVG thuần — không thêm thư viện, không request. */
export function ProgressRing({ percent, size = 52 }: { percent: number; size?: number }) {
  const r = (size - 6) / 2;
  const c = 2 * Math.PI * r;
  const value = Math.max(0, Math.min(100, percent));
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--lesson-line)" strokeWidth="5" />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={r}
        fill="none"
        stroke="var(--lesson-accent)"
        strokeWidth="5"
        strokeLinecap="round"
        strokeDasharray={`${(c * value) / 100} ${c}`}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="central"
        fill="var(--color-ink)"
        fontSize={size * 0.27}
        fontWeight="700"
      >
        {Math.round(value)}%
      </text>
    </svg>
  );
}

/** Hạn nộp bài tập về nhà, vd "20:00 · 25/09/2026". */
export function formatDue(iso: string) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return `${d.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })} · ${d.toLocaleDateString("vi-VN")}`;
}

/** "N dạng bài kèm lời giải" đếm theo dạng có cấu trúc (problem_html); mục cũ đi kèm (bài tự luận…) đếm riêng. */
export function workedSubtitle(item: LessonItem): string {
  if (item.kind !== "bai_tap_mau" || item.questions.length === 0) return item.subtitle ?? "";
  const dang = item.questions.filter((q) => q.problem_html).length;
  const them = item.questions.length - dang;
  if (dang === 0 || them === 0) return item.subtitle ?? "";
  return `${dang} dạng bài kèm lời giải · ${them} mục bài tập thêm`;
}

/** Khung xương trong lúc chờ bài học — cùng lớp bố cục (lesson-shell/lesson-layout) để nội dung về không nhảy. */
export function LessonLoginWall({ title }: { title: string }) {
  const next =
    typeof window === "undefined" ? "" : encodeURIComponent(window.location.pathname + window.location.search);
  return (
    <div className="mx-auto max-w-xl px-4 py-16 text-center">
      <h1 className="text-xl font-bold text-slate-900">{title || "Bài học"}</h1>
      <p className="mt-3 text-base text-slate-700">
        Bài này dành cho thành viên. Tạo tài khoản <strong>miễn phí</strong> trong 1 phút để học tiếp — không cần thẻ,
        không mất phí.
      </p>
      <div className="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-center">
        <Link
          href={`/dang-ky/?next=${next}`}
          className="inline-flex min-h-12 items-center justify-center rounded-lg bg-blue-600 px-6 font-semibold text-white"
        >
          Tạo tài khoản miễn phí
        </Link>
        <Link
          href={`/dang-nhap/?next=${next}`}
          className="inline-flex min-h-12 items-center justify-center rounded-lg border border-slate-300 px-6 font-semibold text-slate-800"
        >
          Tôi đã có tài khoản
        </Link>
      </div>
    </div>
  );
}

export function LessonSkeleton() {
  return (
    <div className="lesson-shell" aria-busy="true" aria-label="Đang tải bài học">
      <div className="lesson-layout animate-pulse">
        <aside className="lesson-nav" aria-hidden="true">
          <div className="h-4 w-28 rounded bg-white/10" />
          <div className="mt-6 space-y-3">
            {Array.from({ length: 4 }, (_, i) => (
              <div key={i} className="h-4 w-full rounded bg-white/5" />
            ))}
          </div>
        </aside>
        <div className="lesson-main">
          <div className="h-3 w-24 rounded bg-white/10" />
          <div className="mt-4 h-8 w-3/4 rounded bg-white/10" />
          <div className="mt-3 h-4 w-1/2 rounded bg-white/5" />
          <div className="mt-8 space-y-5">
            {Array.from({ length: 3 }, (_, i) => (
              <div key={i} className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <div className="h-5 w-1/3 rounded bg-white/10" />
                <div className="mt-4 h-4 w-full rounded bg-white/5" />
                <div className="mt-2 h-4 w-5/6 rounded bg-white/5" />
                <div className="mt-2 h-4 w-2/3 rounded bg-white/5" />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

/** Lối thoát khỏi trang bài: thanh đáy toàn site bị ẩn ở đây, nên cần một nút về lại 5 nút chính (Hôm nay…). */
export function LessonHomeLink() {
  const { session } = useAuth();
  return (
    <Link
      href={session ? "/tai-khoan" : "/"}
      className="lesson-bottom-link lesson-bottom-home"
      aria-label="Về trang chính"
    >
      <Home size={18} aria-hidden />
    </Link>
  );
}
