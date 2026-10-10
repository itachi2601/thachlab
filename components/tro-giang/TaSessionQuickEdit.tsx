"use client";

import { useState } from "react";
import { updateOwnSession, TA_EDIT_WINDOW_DAYS, type TaSessionListItem } from "@/lib/tro-giang/queries";
import { useToast } from "@/components/ui/Toast";

const cls = "mt-1 w-full rounded-xl border border-white/15 bg-white/5 px-3 py-2.5 text-white";

function isoDay(offset: number) {
  const d = new Date();
  d.setDate(d.getDate() + offset);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

/** Trợ giảng sửa lại ngày/giờ/lớp/số liệu của buổi chưa duyệt trong 7 ngày; DB (policy ta_sessions) khoá sau hạn. */
export default function TaSessionQuickEdit({
  session,
  onSaved,
  onCancel,
}: {
  session: TaSessionListItem;
  onSaved: () => void;
  onCancel: () => void;
}) {
  const toast = useToast();
  const [date, setDate] = useState(session.work_date);
  const [label, setLabel] = useState(session.class_label ?? "");
  const [start, setStart] = useState(session.start_time?.slice(0, 5) ?? "");
  const [end, setEnd] = useState(session.end_time?.slice(0, 5) ?? "");
  const [touches, setTouches] = useState(session.student_touches ?? 0);
  const [papers, setPapers] = useState(session.papers_graded ?? 0);
  const [busy, setBusy] = useState(false);

  async function save() {
    setBusy(true);
    try {
      await updateOwnSession(session.id, {
        work_date: date,
        class_label: label.trim() || null,
        start_time: start || null,
        end_time: end || null,
        ...(session.session_type === "lop" ? { student_touches: touches } : {}),
        ...(session.session_type === "chambai" ? { papers_graded: papers } : {}),
      });
      toast("success", "Đã sửa buổi. Thầy sẽ duyệt theo thông tin mới.");
      onSaved();
    } catch (e) {
      toast("error", (e as { message?: string })?.message ?? "Không lưu được");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mt-3 space-y-3 rounded-2xl border border-blue-400/30 bg-blue-500/5 p-4">
      <p className="text-xs text-slate-400">Sửa được đến khi thầy duyệt, tối đa {TA_EDIT_WINDOW_DAYS} ngày kể từ ngày làm.</p>
      <label className="block text-sm text-slate-300">
        Ngày làm
        <input type="date" className={cls} min={isoDay(-TA_EDIT_WINDOW_DAYS)} max={isoDay(0)} value={date} onChange={(e) => setDate(e.target.value)} />
      </label>
      {session.session_type !== "phudao" && (
        <label className="block text-sm text-slate-300">
          Lớp
          <input className={cls} value={label} onChange={(e) => setLabel(e.target.value)} />
        </label>
      )}
      {session.session_type !== "video" && (
        <div className="grid grid-cols-2 gap-3">
          <label className="text-sm text-slate-300">
            Bắt đầu
            <input type="time" className={cls} value={start} onChange={(e) => setStart(e.target.value)} />
          </label>
          <label className="text-sm text-slate-300">
            Kết thúc
            <input type="time" className={cls} value={end} onChange={(e) => setEnd(e.target.value)} />
          </label>
        </div>
      )}
      {session.session_type === "lop" && (
        <label className="block text-sm text-slate-300">
          Số lượt tiếp xúc
          <input type="number" min={0} step={1} className={cls} value={touches} onChange={(e) => setTouches(Number(e.target.value))} />
        </label>
      )}
      {session.session_type === "chambai" && (
        <label className="block text-sm text-slate-300">
          Số bài chấm
          <input type="number" min={1} step={1} className={cls} value={papers} onChange={(e) => setPapers(Number(e.target.value))} />
        </label>
      )}
      <div className="flex gap-3">
        <button type="button" disabled={busy || !date} onClick={save} className="min-h-11 rounded-xl bg-blue-600 px-5 text-sm font-semibold text-white disabled:opacity-50">
          {busy ? "Đang lưu…" : "Lưu"}
        </button>
        <button type="button" onClick={onCancel} className="min-h-11 px-4 text-sm text-slate-300">Hủy</button>
      </div>
    </div>
  );
}
