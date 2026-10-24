"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { ArrowLeft, Check, ChevronDown, Clock, Tv } from "lucide-react";
import Button from "@/components/ui/Button";
import ConfirmDialog from "@/components/ui/ConfirmDialog";
import { useToast } from "@/components/ui/Toast";
import { useAuth } from "@/components/auth/AuthProvider";
import { useCountdown, usePoll } from "@/components/quiz-live/shared";
import {
  extendReviewStage,
  fetchQuestionSnippets,
  getReviewBoard,
  getWrongStudents,
  reviewErrorText,
  setReviewStage,
  type BoardStudent,
  type ReviewBoard,
  type StageState,
  type WrongStudentRow,
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

const shortDang = (d: string) => d.replace(/^Dạng\s*\d+\s*·\s*/, "");

/** Danh sách tên em (nhạy địa vị bạn bè — chỉ hiện ở bảng của nhân sự, không bao giờ lên màn hình chiếu). */
function NameChips({ items }: { items: { id: string; name: string; note?: string }[] }) {
  const sorted = [...items].sort((a, b) => nameKey(a.name).localeCompare(nameKey(b.name), "vi"));
  return (
    <ul className="mt-2 flex flex-wrap gap-2">
      {sorted.map((it) => (
        <li key={it.id} className="rounded-full bg-surface-2 px-3 py-1.5 text-sm text-ink">
          <span className="font-semibold">{it.name}</span>
          {it.note && <span className="text-muted"> · {it.note}</span>}
        </li>
      ))}
    </ul>
  );
}

function Toggle({ open, onClick, children }: { open: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-expanded={open}
      className="inline-flex min-h-11 items-center gap-1 rounded-full px-3 text-sm font-semibold text-primary hover:bg-surface-2"
    >
      {children}
      <ChevronDown size={16} aria-hidden className={open ? "rotate-180" : ""} />
    </button>
  );
}

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
  /** null = theo chặng đang mở; số = đang xem lại chặng đó. */
  const [view, setView] = useState<number | null>(null);
  const [wrongRows, setWrongRows] = useState<{ stage: number; rows: WrongStudentRow[] } | null>(null);
  const [openKeys, setOpenKeys] = useState<Set<string>>(new Set());
  const [showAllQ, setShowAllQ] = useState(false);
  const [snippets, setSnippets] = useState<{ exam: number; list: string[] } | null>(null);
  const [seen, setSeen] = useState<Set<string>>(() => {
    try {
      return new Set(JSON.parse(window.localStorage.getItem(seenKey(sessionId)) ?? "[]") as string[]);
    } catch {
      return new Set();
    }
  });

  const { refresh, error } = usePoll(
    () => getReviewBoard(sessionId, view),
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
  /** Chặng mà các số liệu bên dưới đang nói về (theo chính bảng máy chủ trả về, không theo ô bấm). */
  const viewed = sess ? (sess.viewed_stage ?? idx) : -1;
  const reviewing = viewed >= 0 && viewed !== idx;
  const examId = viewed >= 0 ? sess?.stages[viewed]?.exam_id : undefined;

  const { refresh: refreshWrong } = usePoll(
    () => getWrongStudents(sessionId, view).then((rows) => ({ stage: view ?? idx, rows })),
    () => (running && !reviewing ? 8000 : 20000),
    (d) => setWrongRows(d),
    !fatal && !!board && viewed >= 0,
  );
  const kickRef = useRef({ refresh, refreshWrong });
  const firstView = useRef(true);
  useEffect(() => {
    kickRef.current = { refresh, refreshWrong };
  });
  useEffect(() => {
    // đổi chặng đang xem: lấy ngay số liệu mới, đóng các danh sách đang mở của chặng cũ
    if (firstView.current) {
      firstView.current = false;
      return;
    }
    setTimeout(() => {
      setOpenKeys(new Set());
      setShowAllQ(false);
    }, 0);
    kickRef.current.refresh();
    kickRef.current.refreshWrong();
  }, [view]);

  // Chỉ dùng danh sách tên khi nó đúng là của chặng đang hiển thị (tránh nháy dữ liệu chặng khác).
  const wrong = wrongRows && wrongRows.stage === viewed ? wrongRows.rows : null;
  const byQuestion = useMemo(() => {
    const m = new Map<number, WrongStudentRow[]>();
    for (const w of wrong ?? []) m.set(w.idx, [...(m.get(w.idx) ?? []), w]);
    return m;
  }, [wrong]);
  const byStudent = useMemo(() => {
    const m = new Map<string, WrongStudentRow[]>();
    for (const w of wrong ?? []) m.set(w.student_id, [...(m.get(w.student_id) ?? []), w]);
    return m;
  }, [wrong]);
  const byDangStudents = useMemo(() => {
    const m = new Map<string, Map<string, { name: string; qs: number[] }>>();
    for (const w of wrong ?? []) {
      if (!w.dang) continue;
      const d = m.get(w.dang) ?? new Map<string, { name: string; qs: number[] }>();
      const cur = d.get(w.student_id) ?? { name: w.name, qs: [] };
      cur.qs.push(w.idx + 1);
      d.set(w.student_id, cur);
      m.set(w.dang, d);
    }
    return m;
  }, [wrong]);
  const toggleKey = (k: string) =>
    setOpenKeys((cur) => {
      const next = new Set(cur);
      if (next.has(k)) next.delete(k);
      else next.add(k);
      return next;
    });
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
      <ol className="flex flex-wrap gap-2" aria-label="Các chặng — bấm để xem số liệu chặng đó">
        {sess.stages.map((s, i) => {
          const state = sess.status === "finished" || i < idx ? "done" : i === idx ? "now" : "next";
          const opened = i <= idx; // chặng chưa mở thì chưa có số liệu
          const watching = i === viewed;
          return (
            <li key={i}>
              <button
                type="button"
                disabled={!opened}
                aria-current={watching ? "true" : undefined}
                onClick={() => setView(i === idx && sess.status !== "finished" ? null : i)}
                className={`min-h-11 rounded-full border px-3 py-1.5 text-left text-sm font-semibold disabled:cursor-default ${
                  watching
                    ? "border-primary bg-primary-soft text-primary ring-2 ring-primary"
                    : state === "done"
                      ? "border-line bg-surface-2 text-muted hover:text-ink"
                      : state === "now"
                        ? "border-primary text-primary"
                        : "border-line text-ink"
                }`}
              >
                {state === "done" ? "✓ " : ""}Chặng {i + 1}
                <span className="ml-1 font-normal">· {s.title}</span>
              </button>
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

      {viewed >= 0 && (
        <>
          {reviewing && (
            <div className="flex flex-wrap items-center gap-3 rounded-2xl border border-primary bg-primary-soft px-4 py-3">
              <p className="flex-1 basis-60 text-ink">
                Đang xem lại <strong>Chặng {viewed + 1}</strong> — số liệu tính đến bây giờ, các em vẫn có thể nộp thêm.
              </p>
              {sess.status !== "finished" && (
                <Button variant="outline" onClick={() => setView(null)}>Về chặng {idx + 1} đang mở</Button>
              )}
            </div>
          )}

          {/* Tổng quan */}
          <section aria-label="Tổng quan chặng" className="space-y-3">
            <div className="flex items-baseline justify-between gap-3">
              <h2 className="text-lg font-bold text-ink">Chặng {viewed + 1} · đã nộp {submitted}/{counts.total}</h2>
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
            {!reviewing && counts.stalled > 0 && (
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
                  const stalled = !reviewing && s.state === "doing" && (s.idle_secs ?? 0) >= STALL_SECS;
                  const done = seen.has(s.id);
                  const mine = byStudent.get(s.id) ?? [];
                  const mineOpen = openKeys.has(`s${s.id}`);
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
                      {mine.length > 0 && (
                        <Toggle open={mineOpen} onClick={() => toggleKey(`s${s.id}`)}>
                          Đang sai {mine.length} câu
                        </Toggle>
                      )}
                      {!reviewing && s.state !== "passed" && (
                        <button
                          type="button"
                          onClick={() => toggleSeen(s.id)}
                          aria-pressed={done}
                          className={`inline-flex min-h-11 items-center gap-1 rounded-full px-3 text-sm font-semibold ${done ? "bg-surface-2 text-ok" : "text-muted hover:bg-surface-2"}`}
                        >
                          <Check size={14} /> {done ? "Đã hỏi" : "Hỏi thăm"}
                        </button>
                      )}
                      {mineOpen && (
                        <ul className="basis-full space-y-1 pb-1 text-sm text-ink">
                          {mine.map((w) => (
                            <li key={w.idx}>
                              <strong>Câu {w.idx + 1}</strong>
                              {w.dang && <span className="text-muted"> · {shortDang(w.dang)}</span>}
                              {w.max != null && w.earned != null && w.earned > 0 && (
                                <span className="text-muted"> · được {w.earned}/{w.max} điểm</span>
                              )}
                              {snippets && snippets.exam === examId && snippets.list[w.idx] && (
                                <span className="block truncate text-muted">{snippets.list[w.idx]}</span>
                              )}
                            </li>
                          ))}
                        </ul>
                      )}
                    </li>
                  );
                })}
              </ul>
            )}
            <p className="mt-2 text-xs text-muted">
              “Đang sai” = lượt làm mới nhất của em vẫn sai câu đó; em làm lại đúng thì hết hiện.
              {!reviewing && " Dấu “Hỏi thăm” chỉ lưu trên máy này, để trợ giảng không đến trùng một em."}
            </p>
          </section>

          {/* Sai theo dạng (chặng ôn dạng bài tập) */}
          {board.by_dang && board.by_dang.length > 0 && (
            <section aria-label="Sai theo dạng" className="space-y-3">
              <h2 className="text-lg font-bold text-ink">Cả lớp vướng ở dạng nào</h2>
              <ul className="space-y-2">
                {board.by_dang.map((d) => {
                  const who = byDangStudents.get(d.label);
                  const key = `d${d.label}`;
                  return (
                  <li key={d.label} className="rounded-2xl border border-line bg-panel px-4 py-3">
                    <p className="text-ink">
                      <strong>{shortDang(d.label)}</strong>
                    </p>
                    <p className="text-sm text-muted">
                      sai {d.pct}% ({d.wrong}/{d.total} lượt) · {d.students_wrong}/{d.students} em sai ít nhất một câu của dạng này
                      {d.pct >= 50 && <span className="ml-2 font-semibold text-warn">nên sửa chung</span>}
                    </p>
                    <div className="mt-2"><Bar value={d.pct} max={100} /></div>
                    {who && who.size > 0 && (
                      <>
                        <Toggle open={openKeys.has(key)} onClick={() => toggleKey(key)}>
                          Xem {who.size} em đang sai dạng này
                        </Toggle>
                        {openKeys.has(key) && (
                          <NameChips items={[...who.entries()].map(([id, v]) => ({ id, name: v.name, note: `câu ${v.qs.join(", ")}` }))} />
                        )}
                      </>
                    )}
                  </li>
                  );
                })}
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
                {board.wrongest.slice(0, showAllQ ? board.wrongest.length : 5).map((q) => {
                  const text = snippets && snippets.exam === examId ? snippets.list[q.idx] : "";
                  const who = byQuestion.get(q.idx);
                  const key = `q${q.idx}`;
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
                      {who && who.length > 0 ? (
                        <>
                          <Toggle open={openKeys.has(key)} onClick={() => toggleKey(key)}>
                            Xem {who.length} em đang sai câu này
                          </Toggle>
                          {openKeys.has(key) && (
                            <NameChips items={who.map((w) => ({ id: w.student_id, name: w.name, note: w.tries > 1 ? `lần ${w.tries}` : undefined }))} />
                          )}
                        </>
                      ) : (
                        wrong && <p className="mt-1 text-sm text-muted">Các em từng sai câu này đã làm lại đúng.</p>
                      )}
                    </li>
                  );
                })}
              </ul>
            )}
            {board.wrongest.length > 5 && (
              <button
                type="button"
                onClick={() => setShowAllQ((v) => !v)}
                aria-pressed={showAllQ}
                className="inline-flex min-h-11 items-center rounded-full border border-line px-4 text-sm font-semibold text-ink hover:bg-surface-2"
              >
                {showAllQ ? "Chỉ 5 câu sai nhiều nhất" : `Mọi câu có em sai (${board.wrongest.length})`}
              </button>
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
