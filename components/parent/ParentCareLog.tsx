"use client";

import { useEffect, useState } from "react";
import { HeartHandshake } from "lucide-react";
import { getSupabase } from "@/services/supabase";
import { fetchNeedsForStudents, needLabel } from "@/services/tutoring";

/**
 * "Thầy theo dõi con" — nhật ký những việc thầy, trợ giảng và web đã làm RIÊNG cho con trong 60 ngày.
 * Mục đích (thầy chốt 15/10/2026): phụ huynh thấy con được theo dõi từng phần, không chỉ thấy điểm.
 * Trung thực về ai làm (P19): việc web tự chấm ghi "Web chấm…", việc người làm ghi "Thầy…"/"Trợ giảng…";
 * con số đầu khối chỉ đếm việc NGƯỜI làm — không thổi phồng bằng sự kiện máy tự sinh.
 * Mọi bảng dưới đây phụ huynh đã có quyền đọc (is_parent_of) — không cần migration. Kiểm tra đầu vào
 * (entry_diagnostics) chỉ đọc qua RPC nên đã có thẻ riêng (EntryDiagnosticCard), không lặp ở đây.
 */

export type CareKind = "web" | "teacher" | "child";
export interface CareEvent {
  at: string;
  kind: CareKind;
  text: string;
  sub?: string;
}

const DAYS = 60;
const SHOW = 6;

const ALERT_TEXT: Record<string, string> = {
  low_score_streak: "Thầy xem lại các bài điểm thấp liên tiếp của con và nhắc con.",
  missed_assessment: "Thầy nhắc con về bài kiểm tra con chưa làm.",
  exam_violation: "Thầy nhắc con giữ nghiêm túc khi làm bài kiểm tra.",
};

async function fetchCareEvents(studentId: string): Promise<CareEvent[]> {
  const supabase = getSupabase();
  const since = new Date(Date.now() - DAYS * 86400e3).toISOString();
  const [needs, hw, alerts, regs] = await Promise.all([
    fetchNeedsForStudents([studentId], []).catch(() => []),
    supabase
      .from("class_homework_checks")
      .select("percent, checked_at")
      .eq("student_id", studentId)
      .gte("checked_at", since),
    supabase
      .from("student_alerts")
      .select("kind, status, handled_note, updated_at")
      .eq("student_id", studentId)
      .neq("status", "open")
      .gte("updated_at", since),
    supabase
      .from("tutoring_registrations")
      .select("attended, attended_at")
      .eq("student_id", studentId)
      .eq("attended", true)
      .gte("attended_at", since),
  ]);

  const out: CareEvent[] = [];
  for (const n of needs) {
    if (n.status === "dismissed") continue;
    const label = needLabel(n);
    if (n.firstSeenAt >= since)
      out.push({
        at: n.firstSeenAt,
        kind: "web",
        text: `Web chấm bài và báo thầy: con còn sai phần ${label}.`,
        sub: `Sai ${n.wrong}/${n.total} câu — thầy đưa phần này vào danh sách phụ đạo.`,
      });
    if (n.tutoredAt && n.tutoredAt >= since)
      out.push({ at: n.tutoredAt, kind: "teacher", text: `Trợ giảng dạy lại riêng phần ${label} cho con.` });
    if (n.clearedAt && n.clearedAt >= since)
      out.push({ at: n.clearedAt, kind: "child", text: `Con làm đúng lại phần ${label} — xong phụ đạo phần này.` });
  }
  for (const h of hw.data ?? [])
    out.push({ at: h.checked_at, kind: "teacher", text: `Thầy kiểm tra bài tập về nhà: con làm được ${h.percent}%.` });
  for (const a of alerts.data ?? [])
    out.push({
      at: a.updated_at,
      kind: "teacher",
      text: ALERT_TEXT[a.kind] ?? "Thầy xem và xử lý một điểm cần chú ý của con.",
      sub: a.handled_note ? `Ghi chú của thầy: ${a.handled_note}` : undefined,
    });
  for (const r of regs.data ?? [])
    if (r.attended_at) out.push({ at: r.attended_at, kind: "child", text: "Con đi buổi phụ đạo với trợ giảng." });
  return out.sort((a, b) => (a.at < b.at ? 1 : -1));
}

/** P11: ngày có thứ. */
function dayLabel(iso: string) {
  const d = new Date(iso);
  const wd = ["Chủ nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"][d.getDay()];
  return `${wd}, ${String(d.getDate()).padStart(2, "0")}/${String(d.getMonth() + 1).padStart(2, "0")}`;
}

const WHO: Record<CareKind, { label: string; cls: string }> = {
  teacher: { label: "Thầy", cls: "bg-primary/10 text-primary" },
  web: { label: "Web", cls: "bg-surface-2 text-muted" },
  child: { label: "Con", cls: "bg-ok/10 text-ok" },
};

export function CareLogView({ events }: { events: CareEvent[] }) {
  const [all, setAll] = useState(false);
  const [since] = useState(() => Date.now() - 30 * 86400e3);
  const human = events.filter((e) => e.kind === "teacher" && new Date(e.at).getTime() >= since).length;
  const shown = all ? events : events.slice(0, SHOW);

  return (
    <section className="mb-6 rounded-2xl border border-line bg-panel p-5">
      <div className="flex items-center gap-2">
        <HeartHandshake size={22} className="text-primary" aria-hidden />
        <h2 className="font-display text-lg font-bold text-ink">Thầy theo dõi con</h2>
      </div>
      <p className="parent-copy mt-2 text-ink">
        {human > 0 ? (
          <>
            30 ngày qua, thầy và trợ giảng đã làm <b className="parent-num">{human}</b> việc riêng cho con.
          </>
        ) : (
          <>
            Mỗi bài con làm đều được chấm và báo thầy. Khi con sai nhiều một phần, thầy xếp phụ đạo — việc đó sẽ hiện ở
            đây.
          </>
        )}
      </p>

      {events.length === 0 ? (
        <p className="parent-copy mt-3 text-muted">60 ngày qua chưa có phần nào con cần thầy kèm thêm.</p>
      ) : (
        <ol className="mt-4 space-y-0">
          {shown.map((e, i) => (
            <li
              key={`${e.at}-${i}`}
              className="grid grid-cols-[3.5rem_1fr] gap-3 border-t border-line py-3 first:border-t-0 first:pt-0"
            >
              <span className={`h-fit rounded-lg px-2 py-0.5 text-center text-[15px] font-semibold ${WHO[e.kind].cls}`}>
                {WHO[e.kind].label}
              </span>
              <div className="min-w-0">
                <p className="text-[15px] text-muted">{dayLabel(e.at)}</p>
                <p className="text-ink">{e.text}</p>
                {e.sub && <p className="text-muted">{e.sub}</p>}
              </div>
            </li>
          ))}
        </ol>
      )}
      {events.length > SHOW && (
        <button
          type="button"
          onClick={() => setAll((v) => !v)}
          className="mt-2 rounded-xl border border-line px-4 font-semibold text-ink hover:border-line-strong"
        >
          {all ? "Thu gọn" : `Xem thêm ${events.length - SHOW} việc`}
        </button>
      )}
    </section>
  );
}

export default function ParentCareLog({ studentId }: { studentId: string }) {
  const [events, setEvents] = useState<CareEvent[] | null>(null);
  useEffect(() => {
    let cancelled = false;
    fetchCareEvents(studentId)
      .then((ev) => !cancelled && setEvents(ev))
      .catch(() => !cancelled && setEvents([]));
    return () => {
      cancelled = true;
    };
  }, [studentId]);
  if (events === null) return <div className="mb-6 h-40 rounded-2xl border border-line bg-panel" aria-busy="true" />;
  return <CareLogView events={events} />;
}
