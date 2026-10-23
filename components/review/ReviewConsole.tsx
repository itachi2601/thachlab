"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { ArrowLeft, Check, Clock, Tv } from "lucide-react";
import Button from "@/components/ui/Button";
import ConfirmDialog from "@/components/ui/ConfirmDialog";
import { useToast } from "@/components/ui/Toast";
import { useAuth } from "@/components/auth/AuthProvider";
import { useCountdown, usePoll } from "@/components/quiz-live/shared";
import {
  extendReviewStage,
  fetchQuestionSnippets,
  getReviewBoard,
  reviewErrorText,
  setReviewStage,
  type BoardStudent,
  type ReviewBoard,
  type StageState,
} from "@/services/review-session";
import { reviewScreenPath } from "@/lib/review-link";
import { Bar, clock, StatePill } from "./shared";

/** Em đang làm mà đáp án không được lưu quá ngần này giây thì coi là "đứng yên" — người đến hỏi thăm. */
const STALL_SECS = 180;

const ORDER: Record<StageState, number> = { failed: 1, idle: 2, doing: 3, passed: 4 };

function priority(s: BoardStudent): number {
  if (s.state === "doing" && (s.idle_secs ?? 0) >= STALL_SECS) return 0;
  return ORDER[s.state];
}

/** Tên Việt xếp theo từ cuối (tên gọi), rồi cả chuỗi. */
function nameKey(full: string): string {
  const parts = full.trim().split(/\s+/);
  return `${parts[parts.length - 1] ?? ""} ${full}`;
}

const FILTERS: { key: StageState | "all" | "care"; label: string }[] = [
  { key: "care", label: "Cần để ý" },
  { key: "all", label: "Cả lớp" },
  { key: "idle", label: "Chưa mở" },
  { key: "doing", label: "Đang làm" },
  { key: "failed", label: "Chưa đạt" },
  { key: "passed", label: "Đạt" },
];

function seenKey(id: number) {
  return `thachlab.on-tap.${id}.da-hoi`;
}

/** Màn hình điều phối của thầy/trợ giảng: điều khiển chặng, đồng hồ, từng em ở đâu, câu sai nhiều nhất. */
export default function ReviewConsole({ sessionId }: { sessionId: number }) {
  const toast = useToast();
  const { profile } = useAuth();
  const [board, setBoard] = useState<ReviewBoard | null>(null);
  const [stamp, setStamp] = useState(0);
  const [busy, setBusy] = useState(false);
  const [fatal, setFatal] = useState("");
  const [filter, setFilter] = useState<(typeof FILTERS)[number]["key"]>("care");
  const [confirmNext, setConfirmNext] = useState<number | null>(null);
  const [snippets, setSnippets] = useState<{ exam: number; list: string[] } | null>(null);
  const [seen, setSeen] = useState<Set<string>>(() => {
    try {
      return new Set(JSON.parse(window.localStorage.getItem(seenKey(sessionId)) ?? "[]") as string[]);
    } catch {
      return new Set();
    }
  });

  const { refresh, error } = usePoll(
    () => getReviewBoard(sessionId),
    (last) => (last?.session.status === "running" ? 4000 : 10000),
    (d) => {
      setBoard(d);
      setStamp(Date.now());
    },
    !fatal,
  );
  useEffect(() => {
    if (error && /forbidden|not_found/.test(error)) setTimeout(() => setFatal(reviewErrorText(error)), 0);
  }, [error]);

  const sess = board?.session;
  const idx = sess?.current_stage ?? -1;
  const running = sess?.status === "running";
  const examId = idx >= 0 ? sess?.stages[idx]?.exam_id : undefined;
  const left = useCountdown(sess?.secs_left ?? 0, stamp, running);

  useEffect(() => {
    if (!examId || snippets?.exam === examId) return;
    let off = false;
    fetchQuestionSnippets(examId).then((list) => !off && setSnippets({ exam: examId, list })).catch(() => undefined);
    return () => {
      off = true;
    };
  }, [examId, snippets?.exam]);

  const counts = useMemo(() => {
    const c: Record<StageState, number> = { idle: 0, doing: 0, failed: 0, passed: 0 };
    let stalled = 0;
    for (const s of board?.students ?? []) {
      c[s.state] += 1;
      if (s.state === "doing" && (s.idle_secs ?? 0) >= STALL_SECS) stalled += 1;
    }
    return { ...c, stalled, total: board?.students.length ?? 0 };
  }, [board]);

  const rows = useMemo(() => {
    const all = [...(board?.students ?? [])];
    const filtered = all.filter((s) => {
      if (filter === "all") return true;
      if (filter === "care") return s.state !== "passed";
      return s.state === filter;
    });
    return filtered.sort((a, b) => priority(a) - priority(b) || nameKey(a.name).localeCompare(nameKey(b.name), "vi"));
  }, [board, filter]);

  const go = useCallback(
    async (stage: number) => {
      setBusy(true);
      try {
        await setReviewStage(sessionId, stage);
        refresh();
      } catch (e) {
        toast("error", reviewErrorText(e));
      } finally {
        setBusy(false);
        setConfirmNext(null);
      }
    },
    [sessionId, refresh, toast],
  );

  async function extend(sec: number) {
    setBusy(true);
    try {
      await extendReviewStage(sessionId, sec);
      refresh();
    } catch (e) {
      toast("error", reviewErrorText(e));
    } finally {
      setBusy(false);
    }
  }

  function toggleSeen(id: string) {
    setSeen((cur) => {
      const next = new Set(cur);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      try {
        window.localStorage.setItem(seenKey(sessionId), JSON.stringify([...next]));
      } catch {
        /* không lưu được thì thôi — chỉ là dấu nhớ trên máy này */
      }
      return next;
    });
  }

  if (fatal) {
    return (
      <div className="rounded-2xl border border-line bg-panel p-6 text-center">
        <p className="text-ink">{fatal}</p>
        <Link href="/tro-giang/on-tap/" className="mt-3 inline-block font-semibold text-primary underline">Về danh sách buổi ôn</Link>
      </div>
    );
  }
  if (!board || !sess) return <p className="text-muted">Đang tải bảng điều phối…</p>;

  const n = sess.stages.length;
  const last = idx === n - 1;
  const chuaBai = profile?.role === "tro_giang" ? "/tro-giang/chua-bai" : "/dashboard-thpt/chua-bai";
  const submitted = counts.passed + counts.failed;

  return (
    <div className="space-y-6">
      <div>
        <Link href="/tro-giang/on-tap/" className="inline-flex min-h-11 items-center gap-1.5 text-sm font-semibold text-primary">
          <ArrowLeft size={16} /> Các buổi ôn
        </Link>
        <h1 className="font-display text-2xl font-bold text-ink">{sess.title}</h1>
        <p className="text-sm text-muted">Ngưỡng đạt mỗi chặng: {sess.threshold}%</p>
      </div>

      {/* Dải chặng */}
      <ol className="flex flex-wrap gap-2" aria-label="Các chặng">
        {sess.stages.map((s, i) => {
          const state = sess.status === "finished" || i < idx ? "done" : i === idx ? "now" : "next";
          return (
            <li
              key={i}
              className={`rounded-full border px-3 py-1.5 text-sm font-semibold ${
                state === "now" ? "border-primary bg-primary-soft text-primary" : state === "done" ? "border-line bg-surface-2 text-muted" : "border-line text-ink"
              }`}
            >
              {state === "done" ? "✓ " : ""}Chặng {i + 1}
              <span className="ml-1 font-normal">· {s.title}</span>
            </li>
          );
        })}
      </ol>

      {/* Điều khiển */}
      <section className="rounded-2xl border border-line bg-panel p-4 sm:p-5" aria-label="Điều khiển">
        {sess.status === "finished" ? (
          <p className="font-semibold text-ink">Buổi ôn đã kết thúc.</p>
        ) : idx < 0 ? (
          <div className="flex flex-wrap items-center gap-3">
            <p className="flex-1 basis-60 text-ink">
              Chưa bắt đầu · {counts.total} em trong lớp. Học sinh vào <strong>Lớp học → Buổi ôn</strong> hoặc quét mã trên màn hình chiếu.
            </p>
            <Button onClick={() => void go(0)} disabled={busy}>Bắt đầu chặng 1</Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex flex-wrap items-center gap-x-6 gap-y-2">
              <p className="text-ink">
                <span className="text-sm text-muted">Chặng {idx + 1}/{n}</span>
                <span className="block font-semibold">{sess.stages[idx]?.title}</span>
              </p>
              <p className="flex items-center gap-2 font-mono text-4xl font-bold tabular-nums text-ink" role="timer">
                <Clock size={28} aria-hidden className="text-muted" />
                {left > 0 ? clock(left) : <span className="text-2xl text-warn">Hết giờ</span>}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button variant="outline" onClick={() => void extend(120)} disabled={busy}>+2 phút</Button>
              <Button
                onClick={() => (counts.doing > 0 ? setConfirmNext(idx + 1) : void go(idx + 1))}
                disabled={busy}
              >
                {last ? "Kết thúc buổi ôn" : `Mở chặng ${idx + 2}`}
              </Button>
              <a
                href={reviewScreenPath(sessionId)}
                target="_blank"
                rel="noreferrer"
                className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-line-strong px-5 py-2.5 text-sm font-semibold text-ink hover:bg-surface-2"
              >
                <Tv size={16} /> Màn hình chiếu
              </a>
            </div>
          </div>
        )}
      </section>

      {idx >= 0 && sess.status !== "finished" && (
        <>
          {/* Tổng quan */}
          <section aria-label="Tổng quan chặng" className="space-y-3">
            <div className="flex items-baseline justify-between gap-3">
              <h2 className="text-lg font-bold text-ink">Đã nộp {submitted}/{counts.total}</h2>
              <span className="text-sm text-muted">Làm mới tự động</span>
            </div>
            <Bar value={submitted} max={counts.total} tone="ok" />
            <div className="flex flex-wrap gap-2" role="group" aria-label="Lọc theo trạng thái">
              {FILTERS.map((f) => {
                const num = f.key === "all" ? counts.total : f.key === "care" ? counts.total - counts.passed : counts[f.key];
                const on = filter === f.key;
                return (
                  <button
                    key={f.key}
                    type="button"
                    onClick={() => setFilter(f.key)}
                    aria-pressed={on}
                    className={`min-h-11 rounded-full border px-3.5 text-sm font-semibold ${on ? "border-primary bg-primary-soft text-primary" : "border-line text-ink hover:bg-surface-2"}`}
                  >
                    {f.label} <span className="font-bold">{num}</span>
                  </button>
                );
              })}
            </div>
            {counts.stalled > 0 && (
              <p className="text-sm font-semibold text-warn">
                ● {counts.stalled} em đang làm nhưng đã {Math.round(STALL_SECS / 60)} phút chưa có đáp án mới — nên đến hỏi thăm.
              </p>
            )}
          </section>

          {/* Từng em */}
          <section aria-label="Từng học sinh">
            {rows.length === 0 ? (
              <p className="text-muted">Không có em nào ở nhóm này.</p>
            ) : (
              <ul className="divide-y divide-line rounded-2xl border border-line bg-panel">
                {rows.map((s) => {
                  const stalled = s.state === "doing" && (s.idle_secs ?? 0) >= STALL_SECS;
                  const done = seen.has(s.id);
                  return (
                    <li key={s.id} className="flex flex-wrap items-center gap-x-3 gap-y-1 px-4 py-2.5">
                      <span className="min-w-0 flex-1 basis-40 font-semibold text-ink">{s.name}</span>
                      <StatePill state={s.state} />
                      <span className="w-24 text-right text-sm tabular-nums text-muted">
                        {s.state === "idle" ? "—" : s.state === "doing" ? `${s.answered}/${s.total} câu` : `${s.best_pct ?? 0}%`}
                      </span>
                      {stalled && (
                        <span className="text-sm font-semibold text-warn">đứng yên {Math.round((s.idle_secs ?? 0) / 60)} phút</span>
                      )}
                      {s.tries > 1 && <span className="text-sm text-muted">lần {s.tries}</span>}
                      {s.state !== "passed" && (
                        <button
                          type="button"
                          onClick={() => toggleSeen(s.id)}
                          aria-pressed={done}
                          className={`inline-flex min-h-11 items-center gap-1 rounded-full px-3 text-sm font-semibold ${done ? "bg-surface-2 text-ok" : "text-muted hover:bg-surface-2"}`}
                        >
                          <Check size={14} /> {done ? "Đã hỏi" : "Hỏi thăm"}
                        </button>
                      )}
                    </li>
                  );
                })}
              </ul>
            )}
            <p className="mt-2 text-xs text-muted">Dấu “Hỏi thăm” chỉ lưu trên máy này, để trợ giảng không đến trùng một em.</p>
          </section>

          {/* Sai theo dạng (chặng ôn dạng bài tập) */}
          {board.by_dang && board.by_dang.length > 0 && (
            <section aria-label="Sai theo dạng" className="space-y-3">
              <h2 className="text-lg font-bold text-ink">Cả lớp vướng ở dạng nào</h2>
              <ul className="space-y-2">
                {board.by_dang.map((d) => (
                  <li key={d.label} className="rounded-2xl border border-line bg-panel px-4 py-3">
                    <p className="text-ink">
                      <strong>{d.label.replace(/^Dạng\s*\d+\s*·\s*/, "")}</strong>
                    </p>
                    <p className="text-sm text-muted">
                      sai {d.pct}% ({d.wrong}/{d.total} lượt) · {d.students_wrong}/{d.students} em sai ít nhất một câu của dạng này
                      {d.pct >= 50 && <span className="ml-2 font-semibold text-warn">nên sửa chung</span>}
                    </p>
                    <div className="mt-2"><Bar value={d.pct} max={100} /></div>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Câu sai nhiều nhất */}
          <section aria-label="Câu sai nhiều nhất" className="space-y-3">
            <h2 className="text-lg font-bold text-ink">Câu sai nhiều nhất</h2>
            {board.wrongest.length === 0 ? (
              <p className="text-sm text-muted">Chưa có câu nào bị sai — sẽ hiện khi có em nộp bài.</p>
            ) : (
              <ul className="space-y-2">
                {board.wrongest.slice(0, 5).map((q) => {
                  const text = snippets && snippets.exam === examId ? snippets.list[q.idx] : "";
                  return (
                    <li key={q.idx} className="rounded-2xl border border-line bg-panel px-4 py-3">
                      <div className="flex flex-wrap items-center gap-3">
                        <span className="min-w-0 flex-1 basis-48 text-ink">
                          <strong>Câu {q.idx + 1}</strong> · sai {q.pct}% ({q.wrong}/{q.total} lượt)
                          {q.dang && <span className="block text-sm text-muted">{q.dang.replace(/^Dạng\s*\d+\s*·\s*/, "")}</span>}
                          {text && <span className="block truncate text-sm text-muted">{text}</span>}
                        </span>
                        <a
                          href={`${chuaBai}?exam=${examId}&class=${sess.class_id}&q=${q.idx}`}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex min-h-11 items-center gap-1.5 rounded-full bg-primary px-4 text-sm font-semibold text-white hover:bg-primary-dark"
                        >
                          <Tv size={14} /> Chiếu
                        </a>
                      </div>
                      <div className="mt-2"><Bar value={q.pct} max={100} /></div>
                    </li>
                  );
                })}
              </ul>
            )}
          </section>
        </>
      )}

      <ConfirmDialog
        open={confirmNext !== null}
        title={last ? "Kết thúc buổi ôn?" : `Mở chặng ${idx + 2}?`}
        description={`Còn ${counts.doing} em đang làm dở. Các em vẫn nộp được bài đang làm, nhưng màn hình của lớp sẽ chuyển sang ${last ? "kết thúc" : "chặng mới"}.`}
        confirmLabel={last ? "Kết thúc" : "Mở chặng mới"}
        onConfirm={() => confirmNext !== null && void go(confirmNext)}
        onCancel={() => setConfirmNext(null)}
      />
    </div>
  );
}
