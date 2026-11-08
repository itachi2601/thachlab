"use client";

// Quiz "chuẩn bị tối trước" của CNC lớp đảo ngược (JiTT). 5 câu trên một trang, nộp một lần,
// xem đúng/sai + giải thích ngay, kèm ô "chỗ em chưa rõ" gửi giảng viên. Không tính điểm.
// Quy tắc: N1 (một gói ≤20', 5 câu), E1 (nhãn A. B. C. D.), C2/M5 (phản hồi ngay sau khi nộp).
import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { BookOpen, CheckCircle2, FileQuestion, Send } from "lucide-react";
import type { CncQuizQuestion } from "@/services/cnc-exam-bank";
import {
  CNC_PREP_PASS,
  CNC_PREP_SESSIONS,
  cncLessonHref,
  cncSessionSheetHref,
  fetchCncPrepBanks,
  fetchMyCncPrep,
  submitCncPrep,
  type CncPrepResponse,
} from "@/services/cnc-prep";

// lessonId: chỉ các buổi thuộc bài đó (đặt cuối tab Lý thuyết, như Kiểm tra nhanh các môn khác).
// variant "line": một dòng nhắc ở đầu trang khoá học, trỏ vào bài của buổi tới chưa làm.
export default function CncPrepQuiz({
  courseId,
  studentId,
  lessonId,
  variant = "full",
}: {
  courseId: number;
  studentId: string;
  lessonId?: string;
  variant?: "full" | "line";
}) {
  const [banks, setBanks] = useState<Record<number, CncQuizQuestion[]> | null>(null);
  const [mine, setMine] = useState<CncPrepResponse[]>([]);
  const [sessionNo, setSessionNo] = useState<number | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([fetchCncPrepBanks(), fetchMyCncPrep(courseId, studentId).catch(() => [])])
      .then(([b, rows]) => {
        if (cancelled) return;
        setBanks(b);
        setMine(rows);
        const available = CNC_PREP_SESSIONS.filter((s) => b[s.no] && (!lessonId || s.lessonId === lessonId));
        const done = new Set(rows.map((r) => r.session_no));
        setSessionNo((available.find((s) => !done.has(s.no)) ?? available[available.length - 1])?.no ?? null);
      })
      .catch(() => {
        if (!cancelled) setBanks({});
      });
    return () => {
      cancelled = true;
    };
  }, [courseId, studentId, lessonId]);

  const available = useMemo(
    () => CNC_PREP_SESSIONS.filter((s) => banks?.[s.no] && (!lessonId || s.lessonId === lessonId)),
    [banks, lessonId],
  );
  if (!banks || !available.length || sessionNo === null) return null;
  const session = available.find((s) => s.no === sessionNo) ?? available[0];
  const best = (no: number) =>
    mine.filter((r) => r.session_no === no).reduce<number | null>((m, r) => Math.max(m ?? 0, r.score), null);

  if (variant === "line") {
    const done = new Set(mine.map((r) => r.session_no));
    const next = available.find((s) => !done.has(s.no));
    if (!next) return null;
    return (
      <p className="cnc-prep-line mb-4 rounded-xl border border-line bg-panel px-4 py-3 text-sm text-ink">
        <FileQuestion size={16} className="mr-1 inline text-primary" aria-hidden />
        <strong>Chuẩn bị buổi {next.no}:</strong> đọc {next.read}, rồi làm 5 câu ở cuối phần Lý thuyết.{" "}
        {next.lessonId && (
          <a href={cncLessonHref(next.lessonId, next.anchor)} className="inline-flex min-h-[44px] items-center font-semibold text-primary underline">
            Mở đúng mục
          </a>
        )}{" "}
        ·{" "}
        <Link href={cncSessionSheetHref(next.no)} className="inline-flex min-h-[44px] items-center font-semibold text-primary underline">
          Phiếu buổi {next.no}
        </Link>
      </p>
    );
  }

  return (
    <section className="cnc-prep mb-6 rounded-2xl border border-line bg-panel p-5" aria-labelledby="cnc-prep-title">
      <h2 id="cnc-prep-title" className="font-display text-base font-semibold text-ink">
        Chuẩn bị trước buổi học
      </h2>
      <p className="mt-1 text-sm text-slate-500">
        Tối hôm trước, khoảng 15–20 phút: đọc đúng mục được giao rồi làm 5 câu. Không tính điểm; giảng viên xem câu cả
        lớp sai để chữa đầu giờ.
      </p>
      {available.length > 1 && (
        <div className="mt-3 flex flex-wrap gap-2" role="tablist" aria-label="Chọn buổi">
          {available.map((s) => {
            const b = best(s.no);
            const active = s.no === session.no;
            return (
              <button
                key={s.no}
                type="button"
                role="tab"
                aria-selected={active}
                onClick={() => setSessionNo(s.no)}
                className={`min-h-[44px] rounded-xl border px-3 text-sm font-semibold ${active ? "border-primary bg-primary/10 text-primary" : "border-line text-slate-600"}`}
              >
                Buổi {s.no}
                {b !== null && <span className="ml-1 font-normal">· {b}/5</span>}
              </button>
            );
          })}
        </div>
      )}
      <PrepForm
        key={session.no}
        courseId={courseId}
        session={session}
        questions={banks[session.no]}
        previous={mine.filter((r) => r.session_no === session.no)}
        onSubmitted={(row) => setMine((rows) => [...rows, row])}
      />
    </section>
  );
}

// Xuất riêng để trang xem thử /dev/cnc-chuan-bi dùng với câu mẫu, `submit` giả (không ghi DB).
export function PrepForm({
  courseId,
  session,
  questions,
  previous,
  onSubmitted,
  submit: send = submitCncPrep,
}: {
  courseId: number;
  session: (typeof CNC_PREP_SESSIONS)[number];
  questions: CncQuizQuestion[];
  previous: CncPrepResponse[];
  onSubmitted: (row: CncPrepResponse) => void;
  submit?: typeof submitCncPrep;
}) {
  const [answers, setAnswers] = useState<(number | null)[]>(() => questions.map(() => null));
  const [chuaRo, setChuaRo] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const total = questions.length;
  const pass = Math.min(CNC_PREP_PASS, total);
  const score = answers.filter((a, i) => a === questions[i].correctIndex).length;
  const allAnswered = answers.every((a) => a !== null);
  const lastScore = previous.length ? previous[previous.length - 1].score : null;

  const submit = async () => {
    setBusy(true);
    setError("");
    try {
      await send({ courseId, sessionNo: session.no, answers, score, total, chuaRo });
      onSubmitted({
        id: Date.now(),
        course_id: courseId,
        student_id: "",
        session_no: session.no,
        answers,
        score,
        total,
        chua_ro: chuaRo.trim() || null,
        created_at: new Date().toISOString(),
      });
      setSubmitted(true);
    } catch {
      setError("Chưa gửi được. Kiểm tra mạng rồi bấm Nộp lại.");
    } finally {
      setBusy(false);
    }
  };
  const retry = () => {
    setAnswers(questions.map(() => null));
    setChuaRo("");
    setSubmitted(false);
  };

  return (
    <div className="mt-4">
      <div className="cnc-gate-banner">
        <FileQuestion size={26} aria-hidden />
        <div>
          <span>Buổi {session.no}</span>
          <h3>{session.title}</h3>
          <p>
            Đọc trước: <strong>{session.read}</strong>
            {session.lessonId && (
              <>
                {" "}
                ·{" "}
                {/* <a> (không phải Link): tải lại trang để CncCourseWorkspace đọc ?bai= và cuộn tới #muc-N */}
                <a href={cncLessonHref(session.lessonId, session.anchor)} className="inline-flex min-h-[44px] items-center gap-1 underline">
                  <BookOpen size={13} className="inline" aria-hidden /> mở đúng mục
                </a>
              </>
            )}
          </p>
        </div>
        <b className={submitted && score >= pass ? "passed" : ""}>
          {submitted ? `${score}/${total}` : `${pass}/${total}`}
          <small>{submitted ? "ĐÚNG" : "CẦN"}</small>
        </b>
      </div>
      {lastScore !== null && !submitted && (
        <p className="mt-2 text-sm text-slate-500">
          Em đã nộp {previous.length} lượt, lượt gần nhất đúng {lastScore}/{total}. Làm lại nếu muốn.
        </p>
      )}

      <div className="cnc-quiz">
        {questions.map((q, qi) => {
          const chosen = answers[qi];
          const wrong = submitted && chosen !== q.correctIndex;
          return (
            <fieldset key={q.id} className={wrong ? "wrong" : ""} disabled={submitted}>
              <legend className="float-left">
                <span>{qi + 1}</span>
                {q.question}
              </legend>
              {q.options.map((option, oi) => (
                <label key={oi} className="clear-left">
                  <input
                    type="radio"
                    name={`prep-${session.no}-${qi}`}
                    checked={chosen === oi}
                    onChange={() => setAnswers((cur) => cur.map((a, i) => (i === qi ? oi : a)))}
                  />
                  <i />
                  {String.fromCharCode(65 + oi)}. {option}
                </label>
              ))}
              {submitted && (
                <p>
                  {wrong ? `Đáp án đúng: ${String.fromCharCode(65 + q.correctIndex)}. ` : "Đúng. "}
                  {q.explanation}
                </p>
              )}
            </fieldset>
          );
        })}
      </div>

      {!submitted ? (
        <>
          <label className="mt-4 block text-sm font-semibold text-ink" htmlFor={`prep-note-${session.no}`}>
            Chỗ em chưa rõ (không bắt buộc)
          </label>
          <textarea
            id={`prep-note-${session.no}`}
            value={chuaRo}
            maxLength={500}
            rows={3}
            onChange={(e) => setChuaRo(e.target.value)}
            placeholder="Ví dụ: em chưa hiểu vì sao X ghi theo đường kính…"
            className="mt-1 w-full rounded-xl border border-line bg-surface-2 p-3 text-base text-ink"
          />
          <button type="button" className="cnc-submit" disabled={!allAnswered || busy} onClick={submit}>
            <Send size={17} aria-hidden />{" "}
            {busy
              ? "Đang gửi…"
              : allAnswered
                ? "Nộp và xem đáp án"
                : `Còn ${answers.filter((a) => a === null).length} câu chưa chọn`}
          </button>
          {error && (
            <div className="cnc-result" role="alert">
              {error}
            </div>
          )}
        </>
      ) : (
        <>
          <div className={`cnc-result ${score >= pass ? "passed" : ""}`} role="status">
            {score >= pass ? (
              <>
                <CheckCircle2 size={16} className="inline" aria-hidden /> Đúng {score}/{total}: em sẵn sàng vào máy buổi{" "}
                {session.no}.
              </>
            ) : (
              `Đúng ${score}/${total}. Đọc lại phần giải thích ở câu sai, rồi làm lại (cần ${pass}/${total} để vào máy; không trừ điểm).`
            )}
          </div>
          <button type="button" className="cnc-submit" onClick={retry}>
            <FileQuestion size={17} aria-hidden /> Làm lại
          </button>
        </>
      )}
    </div>
  );
}
