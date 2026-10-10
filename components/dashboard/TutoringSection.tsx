"use client";

import { Users } from "lucide-react";
import {
  EXIT_COOLDOWN_HOURS,
  formatExitWait,
  NEED_STATUS_LABEL_STUDENT,
  needLabel,
  nextExitAttemptAt,
  WINDOW_QUIZ_PASS_PCT,
  WINDOW_QUIZ_QUESTION_COUNT,
  type ExitWindow,
  type NeedStatus,
  type TutoringNeed,
  type TutoringSlot,
  type WaitlistPosition,
} from "@/services/tutoring";

const NEED_TONE: Record<NeedStatus, string> = {
  open: "border-warn/30 bg-surface-2 text-warn",
  assigned: "border-primary/30 bg-surface-2 text-primary",
  tutored: "border-ok/30 bg-surface-2 text-ok",
  cleared: "border-ok/30 bg-surface-2 text-ok",
  dismissed: "border-line bg-surface-2 text-muted",
};

/** Cửa sổ kiểm tra cuối buổi còn mở VÀ có chủ đề của em — trang chủ dùng để quyết có hiện khối phụ đạo không. */
export function liveExitWindows(openWindows: ExitWindow[], needs: TutoringNeed[], nowMs: number): ExitWindow[] {
  return openWindows.filter(
    (w) => new Date(w.closesAt).getTime() > nowMs && needs.some((n) => w.topicIds.includes(n.topicId)),
  );
}

/**
 * MỘT khối "Phụ đạo" ở trang chủ HS (thầy chốt 7/10/2026): bài kiểm tra cuối buổi đang mở → chủ đề cần
 * mở khoá + nút Tự kiểm tra → buổi phụ đạo sắp tới có nút đăng ký. Trang chủ chỉ render khi có ít nhất
 * một trong ba (N3) — không còn khối lịch trống "Chưa có buổi nào được mở" như 3a42d5a92.
 * Không có nút nền đặc: nút nổi duy nhất của trang là ở thẻ "Hôm nay em làm gì" (B2).
 */
/** Số chủ đề cần mở khoá nhìn thấy ngay; còn lại gập sau "Xem thêm" (N2 ≤4 thao tác mỗi vùng). */
const VISIBLE_NEEDS = 3;

export default function TutoringSection({
  needs,
  slots,
  windows,
  windowDone,
  nowMs,
  lastExitAttempt,
  myRegistrations,
  myWaitlist,
  busySlotId,
  onQuiz,
  onToggleSlot,
}: {
  needs: TutoringNeed[];
  slots: TutoringSlot[];
  /** Đã lọc bằng liveExitWindows. */
  windows: ExitWindow[];
  windowDone: Set<string>;
  nowMs: number;
  lastExitAttempt: Map<number, string>;
  myRegistrations: Set<number>;
  myWaitlist: Map<number, WaitlistPosition>;
  busySlotId: number | null;
  onQuiz: (need: TutoringNeed, window?: ExitWindow) => void;
  onToggleSlot: (slot: TutoringSlot) => void;
}) {
  const renderNeed = (need: TutoringNeed) => {
    const wait = nextExitAttemptAt(lastExitAttempt.get(need.id), nowMs);
    return (
      <div key={need.id} className="flex flex-wrap items-center gap-1.5">
        <span className={`rounded-full border px-3 py-1 text-[13px] font-semibold ${NEED_TONE[need.status]}`}>
          {needLabel(need)} · {NEED_STATUS_LABEL_STUDENT[need.status]}
        </span>
        <button
          type="button"
          onClick={() => onQuiz(need)}
          disabled={wait !== null}
          className="min-h-11 rounded-full border border-line-strong px-4 py-2 text-[13px] font-semibold text-ink hover:border-primary hover:text-primary disabled:cursor-not-allowed disabled:opacity-40"
        >
          {wait ? `Lượt tiếp theo mở lúc ${formatExitWait(wait)}` : "Tự kiểm tra"}
        </button>
      </div>
    );
  };

  return (
    <section className="rounded-2xl border border-line bg-panel p-4 sm:p-5">
      <div className="flex items-center gap-2">
        <Users size={18} className="text-primary" />
        <h2 className="font-display font-bold text-ink">Phụ đạo</h2>
      </div>
      <div className="mt-3 space-y-4">
        {windows.map((w) => {
          const mine = needs.filter((n) => w.topicIds.includes(n.topicId));
          const minutesLeft = Math.max(1, Math.ceil((new Date(w.closesAt).getTime() - nowMs) / 60000));
          return (
            <div key={w.id} className="rounded-xl border border-primary/40 bg-primary-soft p-3">
              <p className="text-sm font-bold text-ink">Bài kiểm tra cuối buổi đã mở</p>
              <p className="mt-0.5 text-sm text-ink">
                Em tự làm một mình, {WINDOW_QUIZ_QUESTION_COUNT} câu, đạt từ {WINDOW_QUIZ_PASS_PCT}%. Còn khoảng {minutesLeft} phút.
              </p>
              <div className="mt-2 space-y-2">
                {mine.map((need) => {
                  const done = windowDone.has(`${w.id}|${need.id}`);
                  return (
                    <button
                      key={need.id}
                      type="button"
                      disabled={done}
                      onClick={() => onQuiz(need, w)}
                      className="flex min-h-11 w-full items-center justify-between gap-3 rounded-xl border border-primary/30 bg-panel p-3 text-left text-sm font-semibold text-ink hover:bg-surface-2 disabled:opacity-50"
                    >
                      <span className="min-w-0 truncate">{needLabel(need)}</span>
                      <span className="shrink-0 text-[13px] text-primary">{done ? "Đã làm" : "Bắt đầu"}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}

        {needs.length > 0 && (
          <div>
            <p className="mb-2 text-[13px] font-bold uppercase tracking-wide text-muted">Chủ đề cần mở khoá</p>
            <p className="mb-2 text-sm text-muted">
              Mở khoá bằng cách đăng ký buổi bên dưới, hoặc tự kiểm tra (đạt từ 80%, hai lượt cách nhau {EXIT_COOLDOWN_HOURS} giờ).
            </p>
            <div className="space-y-1.5">
              {needs.slice(0, VISIBLE_NEEDS).map((need) => renderNeed(need))}
            </div>
            {needs.length > VISIBLE_NEEDS && (
              <details className="mt-1.5">
                <summary className="inline-flex min-h-11 cursor-pointer items-center text-[13px] font-semibold text-ink hover:text-primary">
                  Xem thêm {needs.length - VISIBLE_NEEDS} chủ đề
                </summary>
                <div className="mt-1.5 space-y-1.5">{needs.slice(VISIBLE_NEEDS).map((need) => renderNeed(need))}</div>
              </details>
            )}
          </div>
        )}
        {slots.length > 0 && (
          <div>
            <p className="mb-2 text-[13px] font-bold uppercase tracking-wide text-muted">Buổi phụ đạo sắp tới</p>
            <div className="space-y-2">
              {slots.map((slot) => {
                const registered = myRegistrations.has(slot.id);
                const full = slot.registeredCount >= slot.capacity && !registered;
                const waiting = myWaitlist.get(slot.id);
                return (
                  <div key={slot.id} className="rounded-xl border border-line bg-surface-2 p-3">
                    <div className="flex flex-wrap items-center gap-2">
                      <strong className="text-sm text-ink">
                        {new Date(`${slot.workDate}T00:00:00`).toLocaleDateString("vi-VN", {
                          weekday: "short",
                          day: "2-digit",
                          month: "2-digit",
                        })}{" "}
                        · {slot.startTime.slice(0, 5)}–{slot.endTime.slice(0, 5)}
                      </strong>
                      <span className="text-[13px] text-slate-500">{slot.assistantName}</span>
                      <span className="ml-auto text-[13px] text-slate-500">
                        {slot.registeredCount}/{slot.capacity}
                      </span>
                    </div>
                    {slot.note && <p className="mt-1 text-[13px] text-muted">{slot.note}</p>}
                    {waiting && (
                      <p className="mt-1 text-[13px] text-warn">
                        Em đang ở hàng chờ: thứ {waiting.position}/{waiting.total}. Có chỗ trống em sẽ được xếp vào tự động.
                      </p>
                    )}
                    <button
                      type="button"
                      onClick={() => onToggleSlot(slot)}
                      disabled={busySlotId === slot.id}
                      className={`mt-2 min-h-11 w-full rounded-lg border py-2 text-sm font-bold disabled:opacity-40 ${
                        registered || waiting
                          ? "border-line-strong text-muted"
                          : full
                            ? "border-warn/40 text-warn"
                            : "border-primary text-primary hover:bg-primary-soft"
                      }`}
                    >
                      {registered ? "Huỷ đăng ký" : waiting ? "Rời hàng chờ" : full ? "Đã đủ chỗ — vào hàng chờ" : "Đăng ký"}
                    </button>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
