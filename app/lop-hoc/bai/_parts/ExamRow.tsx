"use client";

import Link from "next/link";
import ExamQrButton from "@/components/exams/ExamQrButton";
import { formatTypeCounts } from "@/features/lessons/types";
import { type LessonExamMeta } from "@/services/lessons";

/** Một đề: tên, thời gian + số câu, trạng thái, nút làm bài. */
export function ExamRow({
  examId,
  itemId,
  exam,
  score,
  loggedIn,
  metaStatus,
  statusLabel,
  passed,
  teacherView = false,
  showQr = false,
}: {
  examId: number;
  itemId?: number | null;
  exam: LessonExamMeta | undefined;
  score: number | undefined;
  loggedIn: boolean;
  /** Trạng thái tải thông tin đề (chỉ có ý nghĩa khi đã đăng nhập) — phân biệt đang tải/lỗi/không thấy đề với chưa đăng nhập. */
  metaStatus: "loading" | "error" | "ready";
  /** Nhãn Đạt/Chưa đạt/Chờ chấm/Đã nộp — chỉ có khi mục này đã tính được trạng thái. */
  statusLabel?: string;
  passed?: boolean;
  teacherView?: boolean;
  /**
   * Hiện số đề + nút "Mã QR" (chiếu lên bảng) — dành cho đề KIỂM TRA (bài kiểm tra chương,
   * giữa/cuối kì). Đề luyện tập không cần: thầy không chiếu QR cho đề luyện.
   */
  showQr?: boolean;
}) {
  if (!exam) {
    const notice = !loggedIn
      ? "Đăng nhập để xem đề"
      : metaStatus === "loading"
        ? "Đang tải…"
        : metaStatus === "error"
          ? "Không tải được, thử tải lại trang"
          : "Đề không khả dụng";
    return (
      <div className="lesson-exam">
        <div>
          <p className="lesson-block-title">Đề kiểm tra</p>
        </div>
        {loggedIn ? (
          <span className="lesson-muted">{notice}</span>
        ) : (
          <Link href="/dang-nhap" className="lesson-btn-ghost">
            {notice}
          </Link>
        )}
      </div>
    );
  }

  const counts = formatTypeCounts(exam.type_counts);
  const attempted = score !== undefined;

  return (
    <div className="lesson-exam">
      <div>
        <p className="lesson-block-title">{exam.title}</p>
        <p className="lesson-block-sub">
          {exam.duration_minutes} phút · {counts || `${exam.question_count} câu`}
          {showQr && (
            // Số đề để em gõ tay ở trang Quét mã khi camera hỏng / mã trên bảng bị lấp (N3).
            <span className="rounded-full border border-line px-2 py-0.5 font-mono text-[11px] font-semibold tracking-wide text-muted">
              Mã đề #{examId}
            </span>
          )}
          {!teacherView && (
            <span
              className={
                attempted && passed !== false ? "lesson-status-done" : attempted ? "lesson-status" : "lesson-status"
              }
            >
              {attempted ? `${statusLabel ?? "Đã làm"} · ${score} điểm` : "Chưa làm"}
            </span>
          )}
        </p>
      </div>
      <div className="flex shrink-0 flex-wrap items-stretch gap-2">
        <Link
          href={`/kiem-tra/lam?id=${examId}${itemId ? `&item=${itemId}` : ""}`}
          className={attempted && !teacherView ? "lesson-btn-ghost" : "lesson-btn"}
        >
          {teacherView ? "Xem đề và đáp án" : attempted ? "Làm lại" : "Làm bài"}
        </Link>
        {showQr && <ExamQrButton examId={examId} title={exam.title} />}
      </div>
    </div>
  );
}
