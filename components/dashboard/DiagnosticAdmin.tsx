"use client";

import { useCallback, useEffect, useState } from "react";
import { RotateCcw } from "lucide-react";
import ConfirmDialog from "@/components/ui/ConfirmDialog";
import { useToast } from "@/components/ui/Toast";
import DiagnosticStartMap from "@/components/tro-giang/DiagnosticStartMap";
import {
  assignHandoff,
  clearHandoff,
  fetchDiagnostic,
  fetchHandoffOptions,
  LEVEL_LABEL,
  levelOf,
  resetDiagnostic,
  type DiagnosticStatus,
  type HandoffOptions,
} from "@/services/diagnostic";
import { fetchQuestionTopics } from "@/services/analytics";
import { fetchTeachingCourses, inviteEntryDiagnostic, type TeachingCourse } from "@/services/teaching-progress";

/**
 * Kiểm tra đầu vào của em vào trễ, nhìn từ phía thầy/trợ giảng:
 * trạng thái "đã chẩn đoán" + nút "Cho làm lại" (RPC diagnostic_reset; các mục phụ đạo đã mở được giữ nguyên).
 * `compact` = một dòng nhỏ trong danh sách lớp; mặc định = thẻ chi tiết từng bài ở hồ sơ học sinh.
 */
export default function DiagnosticAdmin({
  studentId,
  studentName,
  compact = false,
  classId,
}: {
  studentId: string;
  studentName: string;
  compact?: boolean;
  /** Có classId (hồ sơ học sinh của thầy) thì hiện nút mời em đã có trong lớp làm bài. */
  classId?: number;
}) {
  const toast = useToast();
  const [status, setStatus] = useState<DiagnosticStatus | null | "error">(null);
  const [topicName, setTopicName] = useState<Map<number, string>>(new Map());
  const [confirm, setConfirm] = useState(false);
  const [busy, setBusy] = useState(false);
  const [courses, setCourses] = useState<TeachingCourse[]>([]);
  const [inviteCourse, setInviteCourse] = useState<number | "">("");
  const [invited, setInvited] = useState(false);
  const [handoff, setHandoff] = useState<HandoffOptions | null>(null);
  const [pickTa, setPickTa] = useState("");

  useEffect(() => {
    if (compact || classId == null) return;
    let cancelled = false;
    fetchTeachingCourses(classId)
      .then((rows) => {
        if (cancelled) return;
        const active = rows.filter((c) => c.status === "active");
        setCourses(active);
        setInviteCourse(active[0]?.id ?? "");
      })
      .catch(() => undefined);
    return () => { cancelled = true; };
  }, [compact, classId]);

  const loadHandoff = useCallback(() => {
    fetchHandoffOptions(studentId)
      .then((h) => {
        setHandoff(h);
        setPickTa((cur) => cur || h.current?.id || h.assistants[0]?.id || "");
      })
      .catch(() => setHandoff(null));
  }, [studentId]);

  useEffect(() => {
    if (!compact) loadHandoff();
  }, [compact, loadHandoff]);

  async function giao() {
    if (!pickTa) return;
    setBusy(true);
    try {
      // Em chưa làm kiểm tra đầu vào và lớp có khoá đang mở thì mời làm luôn.
      const r = await assignHandoff(studentId, pickTa, !done && inviteCourse !== "" ? inviteCourse : null);
      toast(
        "success",
        `Đã giao ${studentName} cho ${r.assistant}${r.invited ? ", em sẽ thấy bài kiểm tra đầu vào" : ""}${
          r.assignedNeeds > 0 ? ` (${r.assignedNeeds} phần hổng đã chuyển sang trợ giảng)` : ""
        }.`,
      );
      if (r.invited) setInvited(true);
      loadHandoff();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa giao được.");
    } finally {
      setBusy(false);
    }
  }

  async function boGiao() {
    setBusy(true);
    try {
      await clearHandoff(studentId);
      loadHandoff();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa bỏ giao được.");
    } finally {
      setBusy(false);
    }
  }

  async function invite() {
    if (inviteCourse === "") return;
    setBusy(true);
    try {
      const n = await inviteEntryDiagnostic(inviteCourse, studentId);
      setInvited(true);
      toast("success", `Đã mời ${studentName}: em sẽ thấy bài kiểm tra đầu vào (${Math.min(n, 6)} bài gần nhất lớp đã học).`);
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa mời được.");
    } finally {
      setBusy(false);
    }
  }

  const load = useCallback(() => {
    fetchDiagnostic(studentId).then(setStatus).catch(() => setStatus("error"));
  }, [studentId]);

  useEffect(() => { load(); }, [load]);
  useEffect(() => {
    if (compact) return;
    fetchQuestionTopics().then((t) => setTopicName(new Map(t.map((x) => [x.id, x.name])))).catch(() => undefined);
  }, [compact]);

  async function doReset() {
    setBusy(true);
    try {
      await resetDiagnostic(studentId);
      toast("success", `${studentName} sẽ thấy lại bài kiểm tra đầu vào.`);
      setConfirm(false);
      load();
    } catch (e) {
      toast("error", e instanceof Error ? e.message : "Chưa cho làm lại được.");
    } finally {
      setBusy(false);
    }
  }

  const done = status !== null && status !== "error" && status.done;
  const dialog = (
    <ConfirmDialog
      open={confirm}
      title={`Cho ${studentName} làm lại kiểm tra đầu vào?`}
      description="Kết quả lần trước sẽ bị xoá. Các mục phụ đạo đã mở từ lần đó vẫn giữ nguyên."
      confirmLabel={busy ? "Đang xử lý…" : "Cho làm lại"}
      onConfirm={() => { if (!busy) void doReset(); }}
      onCancel={() => setConfirm(false)}
    />
  );

  if (compact) {
    if (status === null) return <span className="text-[12px] text-slate-500">Đang kiểm tra…</span>;
    if (status === "error") return null;
    return (
      <span className="inline-flex flex-wrap items-center gap-1.5">
        <span className={`rounded-full px-2 py-0.5 text-[12px] font-bold ${done ? "bg-emerald-500/15 text-emerald-300" : "bg-white/10 text-slate-300"}`}>
          {done ? `✓ Đã chẩn đoán · ${status.needCount ?? 0} bài cần ôn` : "Chưa chẩn đoán"}
        </span>
        {done && (
          <button type="button" onClick={() => setConfirm(true)} className="text-xs text-slate-400 underline hover:text-white">
            Cho làm lại
          </button>
        )}
        {dialog}
      </span>
    );
  }

  if (status === null) return null;
  if (status === "error") return null;
  return (
    <section className="rounded-2xl border border-white/10 bg-panel p-5">
      <div className="flex flex-wrap items-center gap-3">
        <h4 className="min-w-0 flex-1 font-display text-lg font-bold text-white">Kiểm tra đầu vào</h4>
        {done && (
          <button
            type="button"
            onClick={() => setConfirm(true)}
            className="inline-flex items-center gap-1.5 rounded-xl border border-white/15 px-3 py-2 text-xs font-bold text-slate-200 hover:bg-white/10"
          >
            <RotateCcw size={14} /> Cho làm lại
          </button>
        )}
      </div>
      {handoff && (
        <div className="mt-3 rounded-xl border border-white/10 bg-white/3 p-3">
          <p className="text-sm font-semibold text-white">Trợ giảng phụ trách</p>
          {handoff.current && (
            <p className="mt-1 text-sm text-emerald-300">
              Đang giao cho {handoff.current.name}.{" "}
              <button type="button" disabled={busy} onClick={() => void boGiao()} className="text-xs text-slate-400 underline hover:text-white">
                Bỏ giao
              </button>
            </p>
          )}
          {handoff.assistants.length === 0 ? (
            <p className="mt-1 text-xs text-slate-500">Chưa có trợ giảng nào được gán lớp của em. Gán lớp ở trang Nhân sự trước.</p>
          ) : (
            <div className="mt-2 flex flex-wrap items-center gap-2">
              <select
                aria-label="Chọn trợ giảng"
                value={pickTa}
                onChange={(e) => setPickTa(e.target.value)}
                className="min-h-11 min-w-40 rounded-xl border border-white/10 bg-panel-deep px-3 py-2 text-sm text-white"
              >
                {handoff.assistants.map((a) => (
                  <option key={a.id} value={a.id}>{a.name}</option>
                ))}
              </select>
              <button
                type="button"
                disabled={busy || !pickTa}
                onClick={() => void giao()}
                className="min-h-11 rounded-xl bg-blue-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
              >
                {busy ? "Đang giao…" : handoff.current ? "Đổi trợ giảng" : done ? "Giao trợ giảng" : "Giao + mời làm kiểm tra"}
              </button>
            </div>
          )}
          <p className="mt-2 text-xs text-slate-500">
            Trợ giảng nhận thông báo, các phần em hổng (hiện có và sắp có sau kiểm tra đầu vào) tự giao cho trợ giảng đó.
          </p>
        </div>
      )}
      {!done ? (
        <div className="mt-2 space-y-3">
          <p className="text-sm text-slate-400">
            {invited
              ? "Đã mời — em sẽ thấy thẻ kiểm tra đầu vào ở trang chủ."
              : "Em chưa làm. Chỉ em được đánh dấu vào trễ mới thấy thẻ mời làm bài này."}
          </p>
          {classId != null && !invited && (
            courses.length === 0 ? (
              <p className="text-xs text-slate-500">Lớp chưa có khoá đang mở để gắn lời mời.</p>
            ) : (
              <div className="flex flex-wrap items-center gap-2">
                <select
                  aria-label="Khoá để mời"
                  value={inviteCourse}
                  onChange={(e) => setInviteCourse(Number(e.target.value))}
                  className="min-w-48 rounded-xl border border-white/10 bg-panel-deep px-3 py-2 text-sm text-white"
                >
                  {courses.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
                </select>
                <button
                  type="button"
                  disabled={busy || inviteCourse === ""}
                  onClick={() => void invite()}
                  className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
                >
                  {busy ? "Đang mời…" : "Mời làm kiểm tra đầu vào"}
                </button>
              </div>
            )
          )}
          {classId != null && !invited && courses.length > 0 && (
            <p className="text-xs text-slate-500">
              Cần đã đặt mốc “Lớp đang dạy tới bài” cho khoá. Em được ghi vào khoá là “vào trễ”; học phí giữ nguyên trạng thái mặc định.
            </p>
          )}
        </div>
      ) : (
        <>
          <p className="mt-2 text-sm text-slate-300">
            Làm ngày {status.createdAt ? new Date(status.createdAt).toLocaleDateString("vi-VN") : "—"} · {status.needCount ?? 0} bài cần ôn
          </p>
          <ul className="mt-3 space-y-1.5">
            {(status.perTopic ?? []).map((t) => {
              const pct = t.total > 0 ? Math.round((t.correct / t.total) * 100) : 0;
              return (
                <li key={t.topicId} className="flex items-center gap-2 text-sm">
                  <span className="min-w-0 flex-1 truncate text-slate-200">{topicName.get(t.topicId) ?? `Bài #${t.topicId}`}</span>
                  <span className="shrink-0 tabular-nums text-slate-300">{t.correct}/{t.total}</span>
                  <span className="shrink-0 text-xs text-slate-400">{LEVEL_LABEL[levelOf(t)]}</span>
                  <span aria-hidden>{pct >= 67 ? "✅" : pct >= 34 ? "🟡" : "🔴"}</span>
                </li>
              );
            })}
          </ul>
          <DiagnosticStartMap rows={status.perTopic ?? []} topicName={topicName} defaultOpen />
        </>
      )}
      {dialog}
    </section>
  );
}
