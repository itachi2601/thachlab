"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { timeAgo } from "@/lib/time-ago";
import type { AdminTodayBoard as BoardData } from "@/services/admin-today";

const EMPTY: BoardData = { tasks: [], notices: [], pendingJoins: 0, newBugs: 0, pendingEnrollments: 0, pendingTaSessions: 0, openTutoring: 0, failed: false };

export default function AdminTodayBoard() {
  const [board, setBoard] = useState<BoardData | null>(null);

  useEffect(() => {
    let cancelled = false;
    import("@/services/admin-today")
      .then(({ fetchAdminTodayBoard }) => fetchAdminTodayBoard())
      .then((data) => {
        if (!cancelled) setBoard(data);
      })
      .catch(() => {
        if (!cancelled) setBoard({ ...EMPTY, failed: true });
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (!board) {
    return <p className="mt-3 text-sm text-muted">Đang lấy việc hôm nay…</p>;
  }
  if (board.failed) {
    return <p className="mt-3 text-sm text-muted">Chưa tải được bảng việc hôm nay. Thử tải lại trang.</p>;
  }

  const quiet = board.tasks.length === 0 && board.notices.length === 0 && board.pendingJoins === 0 && board.newBugs === 0 &&
    board.pendingEnrollments === 0 && board.pendingTaSessions === 0 && board.openTutoring === 0;

  return (
    <div className="mt-4 border-t border-line pt-4">
      <h2 className="font-display text-lg font-bold text-ink">Cần làm hôm nay</h2>
      {quiet ? (
        <p className="mt-2 text-sm text-muted">Hôm nay không có việc chờ.</p>
      ) : (
        <ul className="mt-1 divide-y divide-line">
          {board.tasks.map((task) => (
            <li key={`task-${task.id}`}>
              <Link
                href={`/dashboard-thpt?tab=announcements&lop=${task.classId}`}
                className="flex min-h-12 items-center justify-between gap-3 py-3"
              >
                <span className="min-w-0">
                  <span className="block text-sm font-semibold text-ink">{task.className}</span>
                  <span className="mt-0.5 line-clamp-2 block text-sm text-muted">{task.body}</span>
                  <span className="mt-0.5 block text-xs text-muted">{timeAgo(task.createdAt)}</span>
                </span>
                <ChevronRight size={18} className="shrink-0 text-muted" aria-hidden />
              </Link>
            </li>
          ))}
          {board.pendingJoins > 0 && (
            <li>
              <Link href="/quan-tri/hoc-sinh?tab=pending" className="flex min-h-12 items-center justify-between gap-3 py-3">
                <span className="text-sm font-semibold text-ink">
                  {board.pendingJoins} học sinh chờ duyệt vào lớp
                </span>
                <ChevronRight size={18} className="shrink-0 text-muted" aria-hidden />
              </Link>
            </li>
          )}
          {board.newBugs > 0 && (
            <li>
              <Link href="/quan-tri/bao-loi" className="flex min-h-12 items-center justify-between gap-3 py-3">
                <span className="text-sm font-semibold text-ink">{board.newBugs} báo lỗi mới</span>
                <ChevronRight size={18} className="shrink-0 text-muted" aria-hidden />
              </Link>
            </li>
          )}
          {board.pendingEnrollments > 0 && (
            <li>
              <Link href="/dashboard-thpt?tab=enrollment" className="flex min-h-12 items-center justify-between gap-3 py-3">
                <span className="text-sm font-semibold text-ink">{board.pendingEnrollments} đăng ký khoá chờ duyệt</span>
                <ChevronRight size={18} className="shrink-0 text-muted" aria-hidden />
              </Link>
            </li>
          )}
          {board.pendingTaSessions > 0 && (
            <li>
              <Link href="/quan-tri/tro-giang" className="flex min-h-12 items-center justify-between gap-3 py-3">
                <span className="text-sm font-semibold text-ink">{board.pendingTaSessions} phiếu trợ giảng chờ duyệt</span>
                <ChevronRight size={18} className="shrink-0 text-muted" aria-hidden />
              </Link>
            </li>
          )}
          {board.openTutoring > 0 && (
            <li>
              <Link href="/dashboard-thpt?tab=alerts" className="flex min-h-12 items-center justify-between gap-3 py-3">
                <span className="text-sm font-semibold text-ink">{board.openTutoring} mục phụ đạo đang mở</span>
                <ChevronRight size={18} className="shrink-0 text-muted" aria-hidden />
              </Link>
            </li>
          )}
          {board.notices.map((notice) => (
            <li key={`notice-${notice.id}`}>
              <Link href={notice.href} className="flex min-h-12 items-center justify-between gap-3 py-3">
                <span className="min-w-0">
                  <span className="block text-sm font-semibold text-ink">{notice.title}</span>
                  {notice.body ? <span className="mt-0.5 line-clamp-2 block text-sm text-muted">{notice.body}</span> : null}
                  <span className="mt-0.5 block text-xs text-muted">{timeAgo(notice.createdAt)}</span>
                </span>
                <ChevronRight size={18} className="shrink-0 text-muted" aria-hidden />
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
