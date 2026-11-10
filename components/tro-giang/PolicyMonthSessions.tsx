"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { SESSION_TYPE_META, STATUS_META } from "@/lib/tro-giang/constants";
import { formatHours } from "@/lib/tro-giang/format";
import TaSessionQuickEdit from "@/components/tro-giang/TaSessionQuickEdit";
import TaAppeals from "@/components/tro-giang/TaAppeals";
import {
  canTaEditInReopen,
  canTaEditSession,
  fetchMonthSessions,
  fetchReopenWindow,
  type TaReopenWindow,
  type TaSessionListItem,
} from "@/lib/tro-giang/queries";

function fmtUntil(iso: string) {
  return new Date(iso).toLocaleString("vi-VN", { hour: "2-digit", minute: "2-digit", day: "2-digit", month: "2-digit", timeZone: "Asia/Ho_Chi_Minh" });
}

/** Danh sách từng buổi của trợ giảng trong tháng; trong đợt thầy mở lại tháng thì sửa được mọi buổi để rà trước khi chốt sổ. */
export default function PolicyMonthSessions({ assistantId, month, onChanged }: { assistantId: string; month: string; onChanged?: () => void }) {
  const [sessions, setSessions] = useState<TaSessionListItem[] | null>(null);
  const [reopen, setReopen] = useState<TaReopenWindow | null>(null);
  const [editingId, setEditingId] = useState<string | null>(null);

  const load = useCallback(() => {
    fetchMonthSessions(assistantId, month).then(setSessions).catch(() => setSessions([]));
  }, [assistantId, month]);

  useEffect(() => {
    load();
    fetchReopenWindow().then(setReopen).catch(() => setReopen(null));
  }, [load]);

  const reopenThisMonth = reopen && reopen.month.slice(0, 7) === month.slice(0, 7) ? reopen : null;

  return (
    <section className="space-y-3">
      <h2 className="text-lg font-bold text-white">Các buổi đã ghi trong tháng</h2>
      {reopenThisMonth && (
        <p className="rounded-xl border border-amber-400/40 bg-amber-500/10 p-4 text-sm text-amber-100">
          Thầy mở lại tháng {month.slice(5, 7)}/{month.slice(0, 4)} để các bạn rà lần cuối, hạn đến <b>{fmtUntil(reopenThisMonth.until)}</b>.
          Kiểm từng buổi: ngày, lớp, giờ, số lượt/số bài. Sai thì bấm &quot;Sửa buổi này&quot;; buổi đã duyệt mà sửa sẽ về Chờ duyệt để thầy duyệt lại.
          Thiếu buổi thì <Link href="/tro-giang/ghi" className="underline">ghi thêm</Link>; thắc mắc khác thì gửi khiếu nại cuối mục. Hết hạn, công tháng này khoá để thầy chốt sổ.
        </p>
      )}
      {sessions === null ? (
        <p className="text-slate-400">Đang tải…</p>
      ) : sessions.length === 0 ? (
        <p className="rounded-xl border border-dashed border-white/15 p-4 text-sm text-slate-400">Chưa có buổi nào trong tháng.</p>
      ) : (
        <ul className="flex flex-col gap-2.5">
          {sessions.map((s) => {
            const typeMeta = SESSION_TYPE_META[s.session_type];
            const statusMeta = STATUS_META[s.status];
            const StatusIcon = statusMeta.icon;
            const inReopen = canTaEditInReopen(s, reopenThisMonth);
            const editable = inReopen || canTaEditSession(s);
            return (
              <li key={s.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="flex items-start gap-3">
                  <div className="min-w-0 flex-1">
                    <p className="font-medium text-white">
                      {new Date(`${s.work_date}T00:00:00`).toLocaleDateString("vi-VN")} · {typeMeta.label}
                      {s.phudao_students?.length ? ` · ${s.phudao_students.join(", ")}` : s.class_label ? ` · ${s.class_label}` : ""}
                    </p>
                    <p className="mt-0.5 text-sm text-slate-400">
                      {s.start_time && s.end_time ? `${s.start_time.slice(0, 5)}–${s.end_time.slice(0, 5)}` : ""}
                      {s.hours ? ` · ${formatHours(s.hours)} giờ` : ""}
                      {s.session_type === "lop" && s.student_touches != null ? ` · ${s.student_touches} lượt` : ""}
                      {s.papers_graded ? ` · ${s.papers_graded} bài` : ""}
                    </p>
                    {s.status === "rejected" && s.reject_reason && <p className="mt-1 text-sm text-red-300">Lý do: {s.reject_reason}</p>}
                  </div>
                  <span className={`flex shrink-0 items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-bold ${statusMeta.className}`}>
                    <StatusIcon size={13} />
                    {statusMeta.label}
                  </span>
                </div>
                {editable && editingId !== s.id && (
                  <button type="button" onClick={() => setEditingId(s.id)} className="mt-2 min-h-11 text-sm font-semibold text-blue-300 underline">
                    Sửa buổi này
                  </button>
                )}
                {editingId === s.id && (
                  <TaSessionQuickEdit
                    session={s}
                    minDate={inReopen ? `${month.slice(0, 7)}-01` : undefined}
                    hint={inReopen ? `Sửa được đến ${fmtUntil(reopenThisMonth!.until)}. Buổi đã duyệt sửa xong sẽ về Chờ duyệt.` : undefined}
                    onCancel={() => setEditingId(null)}
                    onSaved={() => {
                      setEditingId(null);
                      load();
                      onChanged?.();
                    }}
                  />
                )}
              </li>
            );
          })}
        </ul>
      )}
      <TaAppeals key={sessions?.length ?? 0} assistantId={assistantId} month={`${month.slice(0, 7)}-01`} canSubmit={!!reopenThisMonth} />
    </section>
  );
}
