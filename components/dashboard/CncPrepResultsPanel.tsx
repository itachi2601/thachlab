"use client";

// Bảng kết quả quiz chuẩn bị tối trước (CNC lớp đảo ngược) cho giảng viên: ai đã làm, câu lớp sai nhiều
// nhất (theo lượt đầu), phương án nhiễu hay chọn, các câu "chỗ em chưa rõ". Dùng để chọn 2 câu chữa đầu giờ.
import { useEffect, useMemo, useState } from "react";
import { ClipboardList, MessageCircleQuestion, RefreshCw } from "lucide-react";
import type { CncQuizQuestion } from "@/services/cnc-exam-bank";
import {
  CNC_PREP_PASS,
  CNC_PREP_SESSIONS,
  fetchCncPrepBanks,
  fetchCourseCncPrep,
  summarizeCncPrep,
  type CncPrepResponse,
} from "@/services/cnc-prep";

type Student = { id: string; name: string };

export default function CncPrepResultsPanel({ courseId, students }: { courseId: number; students: Student[] }) {
  const [banks, setBanks] = useState<Record<number, CncQuizQuestion[]> | null>(null);
  const [sessionNo, setSessionNo] = useState<number | null>(null);
  const [tick, setTick] = useState(0);
  const [result, setResult] = useState<{ key: string; rows: CncPrepResponse[]; error: string }>({
    key: "",
    rows: [],
    error: "",
  });
  const requestKey = `${sessionNo}-${tick}`;
  const loading = sessionNo !== null && result.key !== requestKey;
  const rows = result.rows;
  const error = loading ? "" : result.error;

  useEffect(() => {
    let cancelled = false;
    fetchCncPrepBanks()
      .then((b) => {
        if (cancelled) return;
        setBanks(b);
        const nos = Object.keys(b)
          .map(Number)
          .sort((x, y) => x - y);
        setSessionNo((cur) => cur ?? nos[0] ?? null);
      })
      .catch(() => {
        if (!cancelled) setBanks({});
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (sessionNo === null) return;
    let cancelled = false;
    const key = `${sessionNo}-${tick}`;
    fetchCourseCncPrep(courseId, sessionNo)
      .then((r) => {
        if (!cancelled) setResult({ key, rows: r, error: "" });
      })
      .catch(() => {
        if (!cancelled)
          setResult({ key, rows: [], error: "Chưa đọc được kết quả. Có thể migration cnc_prep_responses chưa chạy." });
      });
    return () => {
      cancelled = true;
    };
  }, [courseId, sessionNo, tick]);

  const questions = useMemo(() => (sessionNo !== null && banks?.[sessionNo]) || [], [banks, sessionNo]);

  if (!banks) return null;
  const sessions = CNC_PREP_SESSIONS.filter((s) => banks[s.no]);
  const session = sessions.find((s) => s.no === sessionNo);

  return (
    <section className="rounded-2xl border border-line bg-panel p-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <ClipboardList size={19} className="text-primary" aria-hidden />
          <h3 className="font-display text-lg font-bold text-ink">Chuẩn bị tối trước</h3>
        </div>
        {session && (
          <button
            type="button"
            onClick={() => setTick((t) => t + 1)}
            className="inline-flex min-h-[40px] items-center gap-1.5 rounded-xl border border-line px-3 text-xs font-semibold text-slate-600"
          >
            <RefreshCw size={14} aria-hidden /> Tải lại
          </button>
        )}
      </div>
      {!sessions.length ? (
        <p className="mt-3 text-sm text-slate-500">
          Chưa có buổi nào đăng câu hỏi. Đăng 5 câu vào ngân hàng “Chuẩn bị buổi N” ở trang Đăng đề CNC.
        </p>
      ) : (
        <>
          <div className="mt-3 flex flex-wrap gap-2">
            {sessions.map((s) => (
              <button
                key={s.no}
                type="button"
                onClick={() => setSessionNo(s.no)}
                className={`min-h-[40px] rounded-xl border px-3 text-xs font-bold ${s.no === sessionNo ? "border-primary bg-primary/10 text-primary" : "border-line text-slate-600"}`}
              >
                Buổi {s.no} · {s.title}
              </button>
            ))}
          </div>
          {error && <p className="mt-3 rounded-xl bg-red-500/10 p-3 text-sm text-red-700">{error}</p>}
          {session && !error && (
            <CncPrepSessionResults questions={questions} rows={rows} students={students} loading={loading} />
          )}
        </>
      )}
    </section>
  );
}

// Phần thân thuần (không gọi mạng) — dùng lại ở trang xem thử /dev/cnc-chuan-bi.
export function CncPrepSessionResults({
  questions,
  rows,
  students,
  loading = false,
}: {
  questions: CncQuizQuestion[];
  rows: CncPrepResponse[];
  students: Student[];
  loading?: boolean;
}) {
  const summary = useMemo(() => summarizeCncPrep(rows, questions), [rows, questions]);
  const nameOf = useMemo(() => new Map(students.map((s) => [s.id, s.name])), [students]);
  const done = summary.firsts.length;
  const ready = [...summary.best.values()].filter(
    (b) => b >= Math.min(CNC_PREP_PASS, questions.length || CNC_PREP_PASS),
  ).length;
  const missing = students.filter((s) => !summary.best.has(s.id));
  const ranked = [...summary.stats].sort(
    (a, b) => b.wrong / Math.max(1, b.answered) - a.wrong / Math.max(1, a.answered),
  );
  return (
    <div className={`mt-4 space-y-4 ${loading ? "opacity-60" : ""}`}>
      <div className="grid grid-cols-3 gap-2 text-center">
        <Stat value={`${done}/${students.length}`} label="đã làm" />
        <Stat value={`${Math.round(summary.avg * 100)}%`} label="đúng lượt đầu" />
        <Stat value={`${ready}`} label={`đạt ${Math.min(CNC_PREP_PASS, questions.length)}/${questions.length}`} />
      </div>

      <div>
        <h4 className="text-sm font-bold text-ink">Câu lớp sai nhiều nhất (lượt đầu)</h4>
        <ol className="mt-2 space-y-2">
          {ranked.map((st) => {
            const pct = st.answered ? Math.round((st.wrong / st.answered) * 100) : 0;
            const q = questions[st.index];
            const topWrong = st.picks
              .map((n, i) => ({ n, i }))
              .filter((x) => x.i !== st.correctIndex && x.n > 0)
              .sort((a, b) => b.n - a.n)[0];
            return (
              <li key={st.index} className="rounded-xl border border-line bg-surface-2 p-3">
                <div className="flex items-start justify-between gap-3">
                  <p className="text-sm text-ink">
                    <strong>Câu {st.index + 1}.</strong> {st.question}
                  </p>
                  <span
                    className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-bold ${pct >= 40 ? "bg-red-500/10 text-red-700" : "bg-emerald-500/10 text-emerald-700"}`}
                  >
                    sai {st.wrong}/{st.answered}
                  </span>
                </div>
                <p className="mt-1 text-xs text-slate-500">
                  Đáp án {String.fromCharCode(65 + st.correctIndex)} · chọn:{" "}
                  {st.picks.map((n, i) => `${String.fromCharCode(65 + i)} ${n}`).join(" · ")}
                  {topWrong && q && (
                    <>
                      {" "}
                      · nhầm nhiều nhất:{" "}
                      <strong>
                        {String.fromCharCode(65 + topWrong.i)}. {q.options[topWrong.i]}
                      </strong>
                    </>
                  )}
                </p>
              </li>
            );
          })}
        </ol>
      </div>

      <div>
        <h4 className="flex items-center gap-1.5 text-sm font-bold text-ink">
          <MessageCircleQuestion size={16} aria-hidden /> Chỗ em chưa rõ ({summary.notes.length})
        </h4>
        {summary.notes.length ? (
          <ul className="mt-2 space-y-2">
            {summary.notes.map((n, i) => (
              <li key={`${n.studentId}-${i}`} className="rounded-xl border border-line p-3 text-sm text-ink">
                <span className="text-xs font-semibold text-slate-500">
                  {nameOf.get(n.studentId) ?? "Sinh viên"} ·{" "}
                  {new Date(n.at).toLocaleString("vi-VN", {
                    hour: "2-digit",
                    minute: "2-digit",
                    day: "2-digit",
                    month: "2-digit",
                  })}
                </span>
                <p className="mt-1 whitespace-pre-line">{n.text}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-sm text-slate-500">Chưa có câu hỏi nào.</p>
        )}
      </div>

      {missing.length > 0 && (
        <div>
          <h4 className="text-sm font-bold text-ink">Chưa làm ({missing.length})</h4>
          <p className="mt-1 text-sm text-slate-600">{missing.map((s) => s.name).join(", ")}</p>
        </div>
      )}
    </div>
  );
}

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-xl border border-line bg-surface-2 p-3">
      <strong className="block text-xl text-ink">{value}</strong>
      <small className="text-xs text-slate-500">{label}</small>
    </div>
  );
}
