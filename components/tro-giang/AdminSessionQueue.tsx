"use client";

import { useCallback, useEffect, useState } from "react";
import { AlertTriangle, Check, X } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { SESSION_TYPE_META } from "@/lib/tro-giang/constants";
import { formatHours } from "@/lib/tro-giang/format";
import {
  approveSessions,
  fetchPendingSessions,
  fetchTouchBaselines,
  rejectSession,
  type TaPendingSession,
} from "@/lib/tro-giang/queries";

/** Cao hơn 1,5 lần trung bình của chính bạn đó thì nhấn mạnh để giáo viên đối chiếu ngẫu nhiên. */
const ANOMALY_RATIO = 1.5;

function detailLine(s: TaPendingSession): string {
  if (s.session_type === "lop")
    return `${s.student_touches ?? 0} lượt chạm${s.touch_names?.length ? ` · ${s.touch_names.join(", ")}` : ""}`;
  if (s.session_type === "phudao") {
    const students = s.phudao_students?.length
      ? `${s.phudao_students.length} em (${s.phudao_students.join(", ")})`
      : "chưa ghi tên em nào";
    return `${students} · ${s.homework_given || "chưa ghi bài giao"} · ${s.student_recap_ok ? "HS trình bày lại được" : "HS chưa trình bày lại được"}`;
  }
  if (s.session_type === "chambai") return `${s.papers_graded ?? 0} bài đã chấm`;
  if (s.session_type === "video") return `${s.video_tier === "dung_ky" ? "Dựng kỹ" : "Đơn giản"} · ${s.video_url ?? "chưa có link"}`;
  return "";
}

export default function AdminSessionQueue({ onChanged }: { onChanged?: () => void }) {
  const toast = useToast();
  const [rows, setRows] = useState<TaPendingSession[] | null>(null);
  const [baselines, setBaselines] = useState<Map<string, number>>(new Map());
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [rejectingId, setRejectingId] = useState<string | null>(null);
  const [rejectReason, setRejectReason] = useState("");
  const [busy, setBusy] = useState(false);

  const reload = useCallback(() => {
    fetchPendingSessions()
      .then((data) => {
        setRows(data);
        setSelected(new Set());
      })
      .catch(() => setRows([]));
    fetchTouchBaselines().then(setBaselines).catch(() => {});
  }, []);

  useEffect(reload, [reload]);

  async function approveSelected() {
    setBusy(true);
    try {
      await approveSessions([...selected]);
      toast("success", `Đã duyệt ${selected.size} buổi.`);
      reload();
      onChanged?.();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không duyệt được.");
    } finally {
      setBusy(false);
    }
  }

  async function confirmReject(id: string) {
    if (!rejectReason.trim()) {
      toast("error", "Nhập lý do từ chối để trợ giảng biết cần sửa gì.");
      return;
    }
    setBusy(true);
    try {
      await rejectSession(id, rejectReason.trim());
      toast("success", "Đã từ chối buổi này.");
      setRejectingId(null);
      setRejectReason("");
      reload();
      onChanged?.();
    } catch (error) {
      toast("error", error instanceof Error ? error.message : "Không từ chối được.");
    } finally {
      setBusy(false);
    }
  }

  if (rows === null) return <p className="text-slate-400">Đang tải hàng chờ duyệt…</p>;

  if (rows.length === 0)
    return (
      <p className="rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-slate-500">
        Không còn buổi nào chờ duyệt. Buổi mới trợ giảng ghi sẽ xuất hiện ở đây.
      </p>
    );

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-3">
        <label className="flex items-center gap-2 text-sm text-slate-300">
          <input
            type="checkbox"
            checked={selected.size === rows.length}
            onChange={(e) => setSelected(e.target.checked ? new Set(rows.map((r) => r.id)) : new Set())}
            className="h-4 w-4 accent-blue-500"
          />
          Chọn tất cả ({rows.length})
        </label>
        <button
          type="button"
          disabled={selected.size === 0 || busy}
          onClick={approveSelected}
          className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
        >
          <Check size={15} />
          Duyệt {selected.size > 0 ? `${selected.size} buổi` : ""}
        </button>
      </div>

      {rows.map((s) => {
        const meta = SESSION_TYPE_META[s.session_type];
        const Icon = meta.icon;
        const baseline = baselines.get(s.assistant_id);
        const anomaly =
          s.session_type === "lop" &&
          s.student_touches != null &&
          baseline != null &&
          baseline > 0 &&
          s.student_touches >= baseline * ANOMALY_RATIO;

        return (
          <div
            key={s.id}
            className={`rounded-2xl border p-4 ${anomaly ? "border-amber-400/40 bg-amber-500/5" : "border-white/10 bg-white/5"}`}
          >
            <div className="flex items-start gap-3">
              <input
                type="checkbox"
                checked={selected.has(s.id)}
                onChange={(e) => {
                  const next = new Set(selected);
                  if (e.target.checked) next.add(s.id);
                  else next.delete(s.id);
                  setSelected(next);
                }}
                className="mt-1 h-4 w-4 shrink-0 accent-blue-500"
              />
              <span className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white/10 text-slate-300">
                <Icon size={16} />
              </span>
              <div className="min-w-0 flex-1">
                <p className="font-semibold text-white">
                  {s.assistant_name} · {meta.label}
                  {s.class_label ? ` · ${s.class_label}` : ""}
                </p>
                <p className="text-xs text-slate-400">
                  {new Date(s.work_date).toLocaleDateString("vi-VN")}
                  {s.hours ? ` · ${formatHours(s.hours)} giờ` : ""}
                </p>
                <p className="mt-1 text-sm text-slate-300">{detailLine(s)}</p>
                {s.error_note && <p className="mt-1 text-xs text-slate-400">Lỗi lớp: {s.error_note}</p>}
                {s.policy && <div className="mt-2 space-y-1 text-xs text-blue-200"><p>Chữa bài: {s.policy.teaching_minutes || 0} phút · {s.policy.homework_checked ? "Đã kiểm tra bài tập" : "Chưa kiểm tra bài tập"}</p>{s.policy.teaching_note && <p>Nội dung chữa bài: {s.policy.teaching_note}</p>}{s.policy.attention_note && <p>Em cần chú ý: {s.policy.attention_note}</p>}{s.policy.followups?.map((f,i)=><p key={i}>{f.student} · {f.lesson || "Chưa ghi bài"} · {f.difficulty || "Chưa ghi nhận xét"}</p>)}</div>}
                {s.note && <p className="mt-1 text-xs text-slate-500">Ghi chú: {s.note}</p>}
                {anomaly && (
                  <p className="mt-2 inline-flex items-center gap-1.5 rounded-full bg-amber-500/15 px-2.5 py-1 text-xs font-semibold text-amber-300">
                    <AlertTriangle size={12} />
                    Cao hơn thường lệ — trung bình của bạn này là {baseline!.toFixed(1)} lượt/buổi
                  </p>
                )}
              </div>
              <button
                type="button"
                onClick={() => {
                  setRejectingId(rejectingId === s.id ? null : s.id);
                  setRejectReason("");
                }}
                className="shrink-0 rounded-xl border border-white/15 px-3 py-2 text-xs font-semibold text-slate-300"
              >
                <X size={14} />
              </button>
            </div>

            {rejectingId === s.id && (
              <div className="mt-3 flex flex-wrap gap-2 border-t border-white/10 pt-3">
                <input
                  value={rejectReason}
                  onChange={(e) => setRejectReason(e.target.value)}
                  placeholder="Lý do từ chối (trợ giảng sẽ thấy)…"
                  className="min-w-0 flex-1 rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-slate-500"
                />
                <button
                  type="button"
                  disabled={busy}
                  onClick={() => confirmReject(s.id)}
                  className="rounded-xl bg-red-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
                >
                  Từ chối
                </button>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
