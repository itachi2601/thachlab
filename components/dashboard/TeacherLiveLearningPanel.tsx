"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Activity, AlertTriangle, ChevronDown, Copy, RefreshCw, UserRound } from "lucide-react";
import { useToast } from "@/components/ui/Toast";
import { fetchClassLearningPresence, type ClassLearningPresence } from "@/services/learning-presence";

const ACTIVE_WINDOW_MS = 2 * 60_000;
const STUCK_MINUTES = 30;

type Row = ClassLearningPresence & { active: boolean; needsAttention: boolean; minutes: number };
type Group = { key: string; chapterTitle: string; lessonTitle: string; rows: Row[]; activeCount: number };

/**
 * Hoạt động học trực tiếp của MỘT lớp. Quy mô thật: vài chục em/lớp, thường chỉ 0–10 em online cùng lúc,
 * nên: gộp theo bài (thấy ngay "cả nhóm đang kẹt ở đâu"), em đang học lên trước, em vừa rời gấp vào một mục
 * thu gọn, lớp vắng thì chỉ một dòng. Nhóm "cần hỗ trợ" nổi lên đầu.
 */
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
  const [showRecent, setShowRecent] = useState(false);

  const load = useCallback(() => {
    return fetchClassLearningPresence(classId)
      .then((items) => { setRows(items); setError(""); setNow(Date.now()); })
      .catch((cause) => setError(cause instanceof Error ? cause.message : "Không tải được hoạt động học tập."))
      .finally(() => setLoading(false));
  }, [classId]);

  useEffect(() => {
    void load();
    // Tab ẩn thì không hỏi — giáo viên để tab nền cả buổi không nên tốn truy vấn.
    const timer = window.setInterval(() => { if (document.visibilityState === "visible") void load(); }, 30_000);
    const onVisible = () => { if (document.visibilityState === "visible") void load(); };
    document.addEventListener("visibilitychange", onVisible);
    return () => { window.clearInterval(timer); document.removeEventListener("visibilitychange", onVisible); };
  }, [load]);

  const { activeGroups, recentRows, activeCount, attentionRows } = useMemo(() => {
    const all: Row[] = rows.map((row) => {
      const active = now - Date.parse(row.lastSeenAt) <= ACTIVE_WINDOW_MS;
      const minutes = Math.max(1, Math.round((now - Date.parse(row.lessonOpenedAt)) / 60_000));
      return { ...row, active, minutes, needsAttention: active && minutes >= STUCK_MINUTES };
    });
    const map = new Map<string, Group>();
    for (const row of all.filter((r) => r.active)) {
      const key = String(row.lessonId ?? "none");
      const g = map.get(key) ?? { key, chapterTitle: row.chapterTitle, lessonTitle: row.lessonTitle, rows: [], activeCount: 0 };
      g.rows.push(row);
      g.activeCount += 1;
      map.set(key, g);
    }
    const groups = [...map.values()].sort((a, b) => b.activeCount - a.activeCount || a.lessonTitle.localeCompare(b.lessonTitle, "vi"));
    for (const g of groups) g.rows.sort((a, b) => Number(b.needsAttention) - Number(a.needsAttention) || b.minutes - a.minutes);
    return {
      activeGroups: groups,
      recentRows: all.filter((r) => !r.active),
      activeCount: all.filter((r) => r.active).length,
      attentionRows: all.filter((r) => r.needsAttention),
    };
  }, [rows, now]);

  async function copyReminder(row: Row) {
    const message = row.needsAttention
      ? `Thầy/cô thấy em đang học bài “${row.lessonTitle}” khá lâu. Em đang vướng phần nào để thầy/cô hỗ trợ không?`
      : `Em đang học đến bài “${row.lessonTitle}”. Cố gắng hoàn thành phần đang học, nếu có chỗ chưa hiểu hãy báo thầy/cô nhé.`;
    await navigator.clipboard.writeText(message);
    toast("success", `Đã sao chép lời nhắc cho ${row.fullName}.`);
  }

  const summary = activeCount > 0
    ? `${activeCount}/${studentCount} em đang học${attentionRows.length ? ` · ${attentionRows.length} em có thể đang mắc` : ""}`
    : recentRows.length > 0
      ? `Chưa em nào đang học · ${recentRows.length} em vừa rời trong 15 phút`
      : "Chưa em nào học trong 15 phút gần đây";

  return (
    <section className="rounded-2xl border border-line bg-panel p-4 sm:p-5">
      <div className="flex items-center justify-between gap-3">
        <div className="flex min-w-0 items-center gap-2">
          <span className="relative flex h-2.5 w-2.5 shrink-0">
            {activeCount > 0 && <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-ok opacity-60" />}
            <span className={`relative inline-flex h-2.5 w-2.5 rounded-full ${activeCount > 0 ? "bg-ok" : "bg-surface-2"}`} />
          </span>
          <Activity size={18} className="shrink-0 text-muted" />
          <h3 className="font-display text-base font-bold text-ink sm:text-lg">Đang học bây giờ</h3>
        </div>
        <button
          type="button"
          onClick={() => { setLoading(true); void load(); }}
          disabled={loading}
          className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg text-muted hover:bg-surface-2 hover:text-ink disabled:opacity-40"
          aria-label="Làm mới hoạt động học tập"
        >
          <RefreshCw size={16} className={loading ? "animate-spin" : ""} />
        </button>
      </div>
      <p className={`mt-1 text-sm ${attentionRows.length ? "text-warn" : "text-muted"}`}>
        {error ? "Chưa đọc được dữ liệu trực tiếp. Hãy kiểm tra migration learning presence." : loading && !rows.length ? "Đang tải…" : summary}
      </p>

      {!error && activeGroups.length > 0 && (
        <div className="mt-3 space-y-3">
          {activeGroups.map((g) => (
            <div key={g.key} className="rounded-xl border border-line">
              <div className="flex items-baseline justify-between gap-3 border-b border-line bg-surface-2 px-3 py-2">
                <p className="min-w-0 truncate text-sm font-semibold text-ink">{g.lessonTitle}</p>
                <span className="shrink-0 text-xs text-muted">{g.activeCount} em</span>
              </div>
              {g.chapterTitle && <p className="truncate px-3 pt-1.5 text-xs text-muted">{g.chapterTitle}</p>}
              <ul className="divide-y divide-line">
                {g.rows.map((row) => (
                  <li key={row.studentId} className="flex flex-col gap-1.5 px-3 py-2 sm:flex-row sm:items-center sm:gap-3">
                    <div className="min-w-0 flex-1">
                      <p className="flex flex-wrap items-center gap-x-2 text-sm text-ink">
                        <strong>{row.fullName}</strong>
                        <span className={`text-xs ${row.needsAttention ? "font-semibold text-warn" : "text-muted"}`}>
                          {row.needsAttention && <AlertTriangle size={11} className="mr-1 inline" />}
                          {row.minutes} phút{row.needsAttention ? " — hỏi em đang vướng ở đâu" : ""}
                        </span>
                      </p>
                    </div>
                    <RowActions row={row} onOpenStudent={onOpenStudent} onCopy={copyReminder} />
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

      {!error && recentRows.length > 0 && (
        <div className="mt-3">
          <button
            type="button"
            onClick={() => setShowRecent((v) => !v)}
            aria-expanded={showRecent}
            className="flex min-h-11 w-full items-center justify-between gap-2 rounded-lg px-1 text-sm text-muted hover:text-ink"
          >
            <span>Vừa rời trong 15 phút ({recentRows.length})</span>
            <ChevronDown size={16} className={showRecent ? "rotate-180" : ""} />
          </button>
          {showRecent && (
            <ul className="divide-y divide-line rounded-xl border border-line">
              {recentRows.map((row) => (
                <li key={row.studentId} className="flex flex-col gap-1.5 px-3 py-2 sm:flex-row sm:items-center sm:gap-3">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm text-ink"><strong>{row.fullName}</strong></p>
                    <p className="truncate text-xs text-muted">{row.lessonTitle} · {Math.max(1, Math.round((now - Date.parse(row.lastSeenAt)) / 60_000))} phút trước</p>
                  </div>
                  <RowActions row={row} onOpenStudent={onOpenStudent} onCopy={copyReminder} />
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </section>
  );
}

function RowActions({ row, onOpenStudent, onCopy }: { row: Row; onOpenStudent: (id: string) => void; onCopy: (row: Row) => void }) {
  return (
    <div className="flex gap-1.5 sm:shrink-0">
      <button type="button" onClick={() => onOpenStudent(row.studentId)} className="inline-flex min-h-11 flex-1 items-center justify-center gap-1 rounded-lg border border-line px-3 sm:flex-none text-xs font-semibold text-ink hover:bg-surface-2">
        <UserRound size={13} /> Hồ sơ
      </button>
      <button type="button" onClick={() => void onCopy(row)} className="inline-flex min-h-11 flex-1 items-center justify-center gap-1 rounded-lg border border-line px-3 sm:flex-none text-xs font-semibold text-ink hover:bg-surface-2">
        <Copy size={13} /> Lời nhắc
      </button>
    </div>
  );
}
