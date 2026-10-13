"use client";

import { useEffect, useMemo, useState } from "react";
import { X } from "lucide-react";
import {
  fetchReadyTopics,
  REGISTER_DEADLINE_HOURS,
  REGISTER_MAX_TOPICS,
  type ReadyTopic,
  type TutoringSlot,
} from "@/services/tutoring";

/**
 * Chọn 1–3 chủ đề muốn học trước khi đăng ký buổi phụ đạo (thầy chốt 14/10/2026).
 * Trợ giảng nhận thông báo kèm chủ đề nên chuẩn bị đúng chỗ; chủ đề phải có đủ câu bài kiểm tra cuối buổi.
 * Chủ đề em đang hổng (suggestedTopicIds) lên đầu và được tick sẵn tối đa 3 (N2: ít thao tác nhất).
 */
export default function SlotTopicPicker({
  slot,
  classId,
  suggestedTopicIds,
  waitlist,
  busy,
  onConfirm,
  onClose,
}: {
  slot: TutoringSlot;
  classId: number;
  suggestedTopicIds: number[];
  /** true khi buổi đã đủ chỗ: nút xác nhận thành "Vào hàng chờ". */
  waitlist: boolean;
  busy: boolean;
  onConfirm: (topicIds: number[]) => void;
  onClose: () => void;
}) {
  const [topics, setTopics] = useState<ReadyTopic[] | null>(null);
  const [failed, setFailed] = useState(false);
  const [picked, setPicked] = useState<number[] | null>(null);

  useEffect(() => {
    let alive = true;
    fetchReadyTopics(classId)
      .then((list) => alive && setTopics(list))
      .catch(() => alive && setFailed(true));
    return () => {
      alive = false;
    };
  }, [classId]);

  const readyIds = useMemo(() => new Set((topics ?? []).filter((t) => t.ready).map((t) => t.topicId)), [topics]);
  const suggested = useMemo(
    () => suggestedTopicIds.filter((id) => readyIds.has(id)).slice(0, REGISTER_MAX_TOPICS),
    [suggestedTopicIds, readyIds],
  );
  const selected = picked ?? suggested;
  const suggestedSet = new Set(suggestedTopicIds);
  const mine = (topics ?? []).filter((t) => suggestedSet.has(t.topicId));
  const others = (topics ?? []).filter((t) => !suggestedSet.has(t.topicId));

  function toggle(id: number) {
    const cur = selected;
    if (cur.includes(id)) setPicked(cur.filter((x) => x !== id));
    else if (cur.length < REGISTER_MAX_TOPICS) setPicked([...cur, id]);
  }

  function row(t: ReadyTopic) {
    const on = selected.includes(t.topicId);
    const blocked = !t.ready || (!on && selected.length >= REGISTER_MAX_TOPICS);
    return (
      <button
        key={t.topicId}
        type="button"
        role="checkbox"
        aria-checked={on}
        disabled={blocked}
        onClick={() => toggle(t.topicId)}
        className={`flex min-h-11 w-full items-center gap-3 rounded-xl border p-3 text-left text-sm disabled:cursor-not-allowed disabled:opacity-45 ${
          on ? "border-primary bg-primary-soft font-semibold text-ink" : "border-line bg-panel text-ink hover:border-primary"
        }`}
      >
        <span
          aria-hidden
          className={`grid size-5 shrink-0 place-items-center rounded border text-[13px] ${on ? "border-primary bg-primary text-white" : "border-line-strong"}`}
        >
          {on ? "✓" : ""}
        </span>
        <span className="min-w-0 flex-1">{t.topicName}</span>
        {!t.ready && <span className="shrink-0 text-[13px] text-muted">Chưa có bài kiểm tra</span>}
      </button>
    );
  }

  const date = new Date(`${slot.workDate}T00:00:00`).toLocaleDateString("vi-VN", { weekday: "short", day: "2-digit", month: "2-digit" });

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-black/40 sm:items-center" role="dialog" aria-modal="true">
      <div className="flex max-h-[88vh] w-full max-w-lg flex-col rounded-t-2xl bg-panel sm:rounded-2xl">
        <div className="flex items-start gap-2 border-b border-line p-4">
          <div className="min-w-0 flex-1">
            <h3 className="font-display font-bold text-ink">Em muốn học chủ đề nào?</h3>
            <p className="mt-0.5 text-sm text-muted">
              {date} · {slot.startTime.slice(0, 5)}–{slot.endTime.slice(0, 5)}
              {slot.assistantName ? ` · ${slot.assistantName}` : ""}. Chọn tối đa {REGISTER_MAX_TOPICS} chủ đề; trợ giảng sẽ được báo trước để chuẩn bị.
            </p>
          </div>
          <button type="button" onClick={onClose} aria-label="Đóng" className="grid size-11 shrink-0 place-items-center rounded-full text-muted hover:bg-surface-2">
            <X size={18} />
          </button>
        </div>

        <div className="space-y-3 overflow-y-auto p-4">
          {failed && <p className="text-sm text-warn">Chưa tải được danh sách chủ đề, thử lại sau nhé.</p>}
          {!topics && !failed && <p className="text-sm text-muted">Đang tải…</p>}
          {mine.length > 0 && (
            <div className="space-y-1.5">
              <p className="text-[13px] font-bold uppercase tracking-wide text-muted">Em đang cần ôn</p>
              {mine.map(row)}
            </div>
          )}
          {others.length > 0 && (
            <details open={mine.length === 0}>
              <summary className="flex min-h-11 cursor-pointer items-center text-[13px] font-bold uppercase tracking-wide text-muted">
                Chủ đề khác ({others.length})
              </summary>
              <div className="space-y-1.5">{others.map(row)}</div>
            </details>
          )}
          <p className="text-[13px] text-muted">
            Đăng ký chốt trước giờ học {REGISTER_DEADLINE_HOURS} giờ. Cuối buổi em tự làm bài kiểm tra ngắn về đúng các chủ đề đã chọn.
          </p>
        </div>

        <div className="border-t border-line p-4">
          <button
            type="button"
            disabled={busy || selected.length === 0}
            onClick={() => onConfirm(selected)}
            className="min-h-11 w-full rounded-lg bg-primary py-2 text-sm font-bold text-white disabled:opacity-40"
          >
            {selected.length === 0
              ? "Chọn ít nhất 1 chủ đề"
              : `${waitlist ? "Vào hàng chờ" : "Đăng ký"} · ${selected.length} chủ đề`}
          </button>
        </div>
      </div>
    </div>
  );
}
