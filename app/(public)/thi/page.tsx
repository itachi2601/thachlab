"use client";

import { Suspense, useCallback, useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";
import Button from "@/components/ui/Button";
import QuestionCard from "@/components/exams/QuestionCard";
import { emptyResponses, isAnswered, QUESTION_TYPE_LABELS } from "@/features/exams/types";
import type { ExamQuestionPublic, QuestionResponse } from "@/features/exams/types";
import { getSupabase } from "@/services/supabase";

/**
 * /thi/?ma=XXXX — làm đề bằng mã, KHÔNG cần tài khoản. Mỗi lượt em nhập họ tên + MSSV + lớp; server xáo câu và
 * phương án riêng cho lượt đó, chấm ở server, điểm vào bảng điểm của lớp (supabase/migrations/20261027120000_*).
 * Bài đang làm giữ trong sessionStorage để tải lại trang không mất (M2: không bắt làm lại từ đầu).
 */

interface Info {
  title: string;
  duration_minutes: number;
  question_count: number;
  gradebook: string;
}
interface Started {
  session_id: string;
  title: string;
  duration_minutes: number;
  questions: ExamQuestionPublic[];
  startedAt: number;
  responses: QuestionResponse[];
}
interface Result {
  score10: number;
  correct_count: number;
  question_count: number;
  full_name: string;
  student_code: string;
}

const storeKey = (code: string) => `guest-exam:${code}`;
function readStore(code: string): Started | null {
  try {
    const raw = window.sessionStorage.getItem(storeKey(code));
    return raw ? (JSON.parse(raw) as Started) : null;
  } catch {
    return null;
  }
}
function writeStore(code: string, s: Started | null) {
  try {
    if (s) window.sessionStorage.setItem(storeKey(code), JSON.stringify(s));
    else window.sessionStorage.removeItem(storeKey(code));
  } catch {
    /* sessionStorage bị chặn: vẫn làm bài được, chỉ không giữ khi tải lại */
  }
}
function errText(e: unknown): string {
  const m = e instanceof Error ? e.message : (e as { message?: string })?.message;
  return m || "Có lỗi, em thử lại nhé.";
}
function fmt(sec: number): string {
  const s = Math.max(0, sec);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

const INPUT = "mt-1 w-full min-h-11 rounded-xl border border-line-strong bg-surface px-3 text-base text-ink";

function GuestExam() {
  const params = useSearchParams();
  const [typed, setTyped] = useState("");
  const code = params.get("ma") ?? typed;
  const ma = code.trim().toUpperCase();

  const [info, setInfo] = useState<Info | null>(null);
  const [infoError, setInfoError] = useState("");
  const [form, setForm] = useState({ name: "", mssv: "", lop: "" });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [run, setRun] = useState<Started | null>(null);
  const [result, setResult] = useState<Result | null>(null);
  const [left, setLeft] = useState<number | null>(null);
  const submitting = useRef(false);

  useEffect(() => {
    if (!ma) return;
    let alive = true;
    void Promise.resolve().then(() => {
      if (alive) setRun(readStore(ma));
    });
    void getSupabase()
      .rpc("guest_exam_info", { p_code: ma })
      .then(({ data, error: e }) => {
        if (!alive) return;
        if (e || !data) setInfoError("Mã đề không đúng hoặc đã đóng. Em kiểm tra lại mã hoặc quét lại QR.");
        else setInfo(data as Info);
      });
    return () => {
      alive = false;
    };
  }, [ma]);

  async function start() {
    setError("");
    setBusy(true);
    try {
      const { data, error: e } = await getSupabase().rpc("guest_exam_start", {
        p_code: ma,
        p_full_name: form.name,
        p_student_code: form.mssv,
        p_class_name: form.lop,
      });
      if (e) throw e;
      const d = data as Omit<Started, "startedAt" | "responses">;
      const s: Started = { ...d, startedAt: Date.now(), responses: emptyResponses(d.questions) };
      writeStore(ma, s);
      setRun(s);
    } catch (e) {
      setError(errText(e));
    } finally {
      setBusy(false);
    }
  }

  const submit = useCallback(
    async (auto: boolean) => {
      if (!run || submitting.current) return;
      submitting.current = true;
      setBusy(true);
      setError("");
      try {
        const { data, error: e } = await getSupabase().rpc("guest_exam_submit", {
          p_session_id: run.session_id,
          p_responses: run.responses,
        });
        if (e) throw e;
        writeStore(ma, null);
        setResult(data as Result);
        setRun(null);
      } catch (e) {
        submitting.current = false;
        setError(`${auto ? "Hết giờ nhưng chưa nộp được. " : ""}${errText(e)} Bài của em vẫn còn đây, bấm Nộp bài lại.`);
      } finally {
        setBusy(false);
      }
    },
    [run, ma],
  );

  useEffect(() => {
    if (!run) return;
    const total = run.duration_minutes * 60;
    const tick = () => {
      const remain = total - Math.floor((Date.now() - run.startedAt) / 1000);
      setLeft(remain);
      if (remain <= 0) void submit(true);
    };
    tick();
    const t = window.setInterval(tick, 1000);
    return () => window.clearInterval(t);
  }, [run, submit]);

  function answer(i: number, r: QuestionResponse) {
    if (!run) return;
    const responses = run.responses.slice();
    responses[i] = r;
    const next = { ...run, responses };
    writeStore(ma, next);
    setRun(next);
  }

  if (!ma) {
    return (
      <main className="mx-auto max-w-md px-4 py-10">
        <h1 className="text-xl font-bold text-ink">Vào làm đề bằng mã</h1>
        <label className="mt-4 block text-sm text-muted">
          Mã đề (in trên bảng hoặc trong mã QR)
          <input className={INPUT} value={typed} onChange={(e) => setTyped(e.target.value)} autoCapitalize="characters" />
        </label>
      </main>
    );
  }

  if (result) {
    return (
      <main className="mx-auto max-w-md px-4 py-10">
        <h1 className="text-xl font-bold text-ink">Đã nộp bài</h1>
        <p className="mt-1 text-sm text-muted">
          {result.full_name} · {result.student_code}
        </p>
        <p className="mt-6 text-5xl font-bold text-ink">
          {result.score10.toLocaleString("vi-VN")}
          <span className="text-xl font-normal text-muted"> / 10</span>
        </p>
        <p className="mt-2 text-sm text-muted">
          Đúng {result.correct_count}/{result.question_count} câu. Điểm đã được lưu vào bảng điểm của lớp.
        </p>
        <Button className="mt-8" variant="outline" onClick={() => { setResult(null); setForm({ name: "", mssv: "", lop: "" }); }}>
          Nhập thông tin mới để làm lượt khác
        </Button>
      </main>
    );
  }

  if (run) {
    const answered = run.responses.filter((r, i) => isAnswered(run.questions[i], r)).length;
    return (
      <main className="mx-auto max-w-2xl px-4 pb-28 pt-4">
        <header className="sticky top-0 z-10 -mx-4 flex items-center justify-between gap-3 border-b border-line bg-surface/95 px-4 py-2 backdrop-blur">
          <p className="min-w-0 truncate text-sm font-semibold text-ink">{run.title}</p>
          <p className="shrink-0 text-sm tabular-nums text-muted" aria-label="Thời gian còn lại">
            ⏱ {left === null ? "—" : fmt(left)}
          </p>
        </header>
        <div className="mt-4 space-y-4">
          {run.questions.map((q, i) => {
            const head = i === 0 || run.questions[i - 1].type !== q.type ? QUESTION_TYPE_LABELS[q.type] : null;
            return (
              <div key={i}>
                {head && <h2 className="mb-2 mt-4 text-sm font-semibold uppercase tracking-wide text-muted">{head}</h2>}
                <QuestionCard index={i + 1} question={q} response={run.responses[i]} onChange={(r) => answer(i, r)} />
              </div>
            );
          })}
        </div>
        <div className="fixed inset-x-0 bottom-0 z-10 border-t border-line bg-surface px-4 py-3">
          <div className="mx-auto flex max-w-2xl items-center justify-between gap-3">
            <p className="text-sm text-muted">
              Đã trả lời {answered}/{run.questions.length}
            </p>
            <Button disabled={busy} onClick={() => {
              if (answered < run.questions.length && !window.confirm(`Còn ${run.questions.length - answered} câu chưa trả lời. Vẫn nộp bài?`)) return;
              void submit(false);
            }}>
              {busy ? "Đang nộp…" : "Nộp bài"}
            </Button>
          </div>
          {error && <p role="alert" className="mx-auto mt-2 max-w-2xl text-sm text-danger">{error}</p>}
        </div>
      </main>
    );
  }

  const ready = form.name.trim().length >= 2 && form.mssv.trim().length >= 3 && form.lop.trim().length >= 2;
  return (
    <main className="mx-auto max-w-md px-4 py-10">
      {infoError ? (
        <p role="alert" className="text-danger">{infoError}</p>
      ) : !info ? (
        <p className="text-muted">Đang mở đề…</p>
      ) : (
        <>
          <h1 className="text-xl font-bold text-ink">{info.title}</h1>
          <p className="mt-1 text-sm text-muted">
            {info.question_count} câu · {info.duration_minutes} phút · Mỗi em nhận một thứ tự câu và đáp án riêng.
          </p>
          <form
            className="mt-6 space-y-4"
            onSubmit={(e) => {
              e.preventDefault();
              if (ready && !busy) void start();
            }}
          >
            <label className="block text-sm text-muted">
              Họ và tên
              <input className={INPUT} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} autoComplete="name" maxLength={80} />
            </label>
            <label className="block text-sm text-muted">
              Mã số sinh viên
              <input className={INPUT} value={form.mssv} onChange={(e) => setForm({ ...form, mssv: e.target.value })} autoCapitalize="characters" maxLength={20} />
            </label>
            <label className="block text-sm text-muted">
              Lớp
              <input className={INPUT} value={form.lop} onChange={(e) => setForm({ ...form, lop: e.target.value })} autoCapitalize="characters" maxLength={30} placeholder="vd. CĐCK 24A" />
            </label>
            <p className="text-xs text-muted">Nhập đúng thông tin của em: điểm được ghi theo họ tên và MSSV này. Bấm Bắt đầu là đồng hồ chạy.</p>
            {error && <p role="alert" className="text-sm text-danger">{error}</p>}
            <Button type="submit" disabled={!ready || busy} className="w-full">
              {busy ? "Đang tạo đề…" : "Bắt đầu làm bài"}
            </Button>
          </form>
        </>
      )}
    </main>
  );
}

export default function Page() {
  return (
    <Suspense fallback={<p className="p-6 text-muted">Đang tải…</p>}>
      <GuestExam />
    </Suspense>
  );
}
