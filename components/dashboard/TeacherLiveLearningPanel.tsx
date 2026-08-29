"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Activity, AlertTriangle, Clock3, Copy, Eye, RefreshCw, UserRound } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { fetchClassLearningPresence, type ClassLearningPresence } from "@/services/learning-presence";

const ACTIVE_WINDOW_MS = 2 * 60_000;

export default function TeacherLiveLearningPanel({
  classId,
  studentCount,
  onOpenStudent,
}: {
  classId: number;
  studentCount: number;
  onOpenStudent: (studentId: string) => void;
}) {
  const toast = useToast();
  const [rows, setRows] = useState<ClassLearningPresence[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [now, setNow] = useState(0);

  const load = useCallback(() => {
    return fetchClassLearningPresence(classId)
      .then((items) => { setRows(items); setError(""); setNow(Date.now()); })
      .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được hoạt động học tập."))
      .finally(() => setLoading(false));
  }, [classId]);

  useEffect(() => {
    void load();
    const timer = window.setInterval(() => void load(), 30_000);
    return () => window.clearInterval(timer);
  }, [load]);

  const activityRows = useMemo(() => rows.map((row) => {
    const lastSeenAgo = Math.max(0, now - Date.parse(row.lastSeenAt));
    const studyingMinutes = Math.max(1, Math.round((now - Date.parse(row.lessonOpenedAt)) / 60_000));
    const active = lastSeenAgo <= ACTIVE_WINDOW_MS;
    const needsAttention = active && studyingMinutes >= 30;
    return { ...row, active, needsAttention, studyingMinutes };
  }), [rows, now]);
  const activeCount = activityRows.filter((row) => row.active).length;
  const attentionCount = activityRows.filter((row) => row.needsAttention).length;

  async function copyReminder(row: (typeof activityRows)[number]) {
    const message = row.needsAttention
      ? `Thầy/cô thấy em đang học bài “${row.lessonTitle}” khá lâu. Em đang vướng phần nào để thầy/cô hỗ trợ không?`
      : `Em đang học đến bài “${row.lessonTitle}”. Cố gắng hoàn thành phần đang học, nếu có chỗ chưa hiểu hãy báo thầy/cô nhé.`;
    await navigator.clipboard.writeText(message);
    toast("success", `Đã sao chép lời nhắc cho ${row.fullName}.`);
  }

  return (
    <section className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2"><Activity size={19} className="text-emerald-300" /><h3 className="font-display text-lg font-bold text-white">Hoạt động học tập trực tiếp</h3></div>
          <p className="mt-1 text-xs text-slate-500">Đang học: hoạt động trong 2 phút · Gần đây: hoạt động trong 15 phút</p>
        </div>
        <button type="button" onClick={() => { setLoading(true); void load(); }} disabled={loading} className="rounded-lg p-2 text-slate-400 hover:bg-white/5 hover:text-white disabled:opacity-40" aria-label="Làm mới hoạt động học tập"><RefreshCw size={16} className={loading ? "animate-spin" : ""} /></button>
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        <MiniMetric value={`${activeCount}/${studentCount}`} label="Đang học" tone="emerald" />
        <MiniMetric value={String(activityRows.length)} label="Hoạt động 15 phút" tone="blue" />
        <MiniMetric value={String(attentionCount)} label="Có thể cần hỗ trợ" tone="amber" />
      </div>

      {error ? (
        <p className="mt-4 rounded-xl border border-amber-400/15 bg-amber-500/5 p-3 text-xs text-amber-200">Chưa đọc được dữ liệu trực tiếp. Hãy kiểm tra migration learning presence.</p>
      ) : !activityRows.length ? (
        <p className="mt-4 rounded-xl border border-dashed border-white/10 p-7 text-center text-sm text-slate-500">Chưa có học sinh hoạt động trong 15 phút gần đây.</p>
      ) : (
        <div className="mt-4 space-y-2">
          {activityRows.map((row) => (
            <div key={row.studentId} className={`rounded-xl border p-3 ${row.needsAttention ? "border-amber-400/20 bg-amber-500/5" : "border-white/10 bg-white/[.02]"}`}>
              <div className="flex flex-wrap items-center gap-3">
                <span className={`h-2.5 w-2.5 rounded-full ${row.active ? "bg-emerald-400 shadow-[0_0_10px_#34d399]" : "bg-slate-600"}`} />
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <strong className="text-sm text-white">{row.fullName}</strong>
                    {row.needsAttention && <span className="inline-flex items-center gap-1 rounded-full bg-amber-500/10 px-2 py-0.5 text-[10px] font-bold text-amber-300"><AlertTriangle size={11} /> Có thể đang mắc</span>}
                  </div>
                  <p className="mt-1 truncate text-xs text-slate-400">{row.chapterTitle ? `${row.chapterTitle} · ` : ""}{row.lessonTitle}</p>
                  <p className="mt-1 flex items-center gap-1 text-[11px] text-slate-500"><Clock3 size={11} />{row.active ? `Đang học khoảng ${row.studyingMinutes} phút` : "Vừa dừng hoặc chuyển sang trang khác"}</p>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  <button type="button" onClick={() => onOpenStudent(row.studentId)} className="inline-flex items-center gap-1 rounded-lg border border-white/10 px-2.5 py-1.5 text-xs font-semibold text-slate-300 hover:border-blue-400/30 hover:text-blue-300"><UserRound size={13} /> Hồ sơ</button>
                  <button type="button" onClick={() => void copyReminder(row)} className="inline-flex items-center gap-1 rounded-lg border border-white/10 px-2.5 py-1.5 text-xs font-semibold text-slate-300 hover:border-emerald-400/30 hover:text-emerald-300"><Copy size={13} /> Lời nhắc</button>
                </div>
              </div>
              {row.needsAttention && <p className="mt-2 border-t border-amber-400/10 pt-2 text-xs text-amber-200/70"><Eye size={12} className="mr-1 inline" />Nên hỏi em đang vướng ở đâu trước khi nhắc hoàn thành bài.</p>}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function MiniMetric({ value, label, tone }: { value: string; label: string; tone: "emerald" | "blue" | "amber" }) {
  const toneClass = { emerald: "text-emerald-300", blue: "text-blue-300", amber: "text-amber-300" }[tone];
  return <div className="rounded-xl border border-white/10 bg-white/[.025] p-3"><strong className={`block text-2xl ${toneClass}`}>{value}</strong><small className="text-slate-500">{label}</small></div>;
}
