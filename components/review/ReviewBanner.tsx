"use client";

import { useState } from "react";
import Link from "next/link";
import { ListChecks } from "lucide-react";
import { useAuth } from "@/components/auth/AuthProvider";
import { usePoll } from "@/components/quiz-live/shared";
import { getMyReviewState, type MyReviewState } from "@/services/review-session";
import { REVIEW_STUDENT_PATH } from "@/lib/review-link";

/**
 * Thẻ nhắc ở /lop-hoc: lớp em đang có buổi ôn tập theo chặng. Không có buổi ôn thì không hiện gì (và không chiếm chỗ).
 * Chỉ học sinh gọi RPC; hỏi lại mỗi 20 giây để em đang mở trang này thấy ngay khi giáo viên mở chặng.
 */
function Inner({ compact }: { compact: boolean }) {
  const [data, setData] = useState<MyReviewState | null>(null);
  usePoll(
    () => getMyReviewState(null),
    (last) => (last?.mode === "self" ? 60000 : 20000),
    (d) => setData(d),
  );
  if (!data || data.status === "finished") return null;
  const idx = data.current_stage;
  const due = data.due_at
    ? new Date(data.due_at).toLocaleString("vi-VN", { hour: "2-digit", minute: "2-digit", day: "2-digit", month: "2-digit" })
    : null;
  // Trang chương (26/10/2026, B2): một dòng phụ dưới "Học tiếp" — không phải banner thứ hai cạnh tranh.
  if (compact) {
    return (
      <Link href={REVIEW_STUDENT_PATH} className="class-task-row">
        <ListChecks size={18} className="shrink-0 text-primary" aria-hidden />
        <span className="class-task-title">{data.title}</span>
        <span className="class-task-sub">
          {data.mode === "self"
            ? `${data.stages.filter((s) => s.mine?.state === "passed").length}/${data.stages.length} chặng`
            : idx < 0
              ? "Chờ mở chặng 1"
              : `Chặng ${idx + 1}/${data.stages.length}`}
        </span>
        {data.mode === "self" && due && <span className="class-task-due">Hạn {due}</span>}
      </Link>
    );
  }
  return (
    <div className="mx-auto mb-4 w-full max-w-3xl px-4">
      <Link
        href={REVIEW_STUDENT_PATH}
        className="flex min-h-14 items-center gap-3 rounded-2xl border border-primary bg-primary-soft px-4 py-3 text-ink hover:bg-surface-2"
      >
        <ListChecks size={24} className="shrink-0 text-primary" aria-hidden />
        <span className="min-w-0 flex-1">
          <span className="block font-bold">{data.title}</span>
          <span className="block text-sm text-muted">
            {data.mode === "self"
              ? `Bài ôn ở nhà · ${data.stages.filter((s) => s.mine?.state === "passed").length}/${data.stages.length} chặng đã qua${
                  data.due_at ? ` · hạn ${new Date(data.due_at).toLocaleString("vi-VN", { hour: "2-digit", minute: "2-digit", day: "2-digit", month: "2-digit" })}` : ""
                }`
              : idx < 0
                ? "Chờ giáo viên mở chặng 1"
                : `Đang ở chặng ${idx + 1}/${data.stages.length} · bấm để vào làm`}
          </span>
        </span>
        <span aria-hidden className="text-xl font-bold text-primary">›</span>
      </Link>
    </div>
  );
}

export default function ReviewBanner({ compact = false }: { compact?: boolean } = {}) {
  const { profile } = useAuth();
  if (profile?.role !== "student") return null;
  return <Inner compact={compact} />;
}
