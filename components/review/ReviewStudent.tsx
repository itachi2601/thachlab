"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, Clock } from "lucide-react";
import { useCountdown, usePoll } from "@/components/quiz-live/shared";
import { getMyReviewState, type MyReviewState, type MyStage } from "@/services/review-session";
import { examTakePath } from "@/lib/exam-link";
import { Bar, clock, StatePill } from "./shared";
import ClassRoster from "./ClassRoster";

const BTN =
  "inline-flex min-h-12 w-full items-center justify-center rounded-full bg-primary px-6 py-3 text-base font-bold text-white hover:bg-primary-dark sm:w-auto";

/** Phần "việc của em ở chặng này" — một việc rõ ràng, một nút to. */
function MyAction({ stage, index, threshold }: { stage: MyStage; index: number; threshold: number }) {
  const m = stage.mine;
  const href = examTakePath(stage.exam_id, stage.item_id);
  const state = m?.state ?? "idle";

  if (state === "passed") {
    return (
      <div className="space-y-2">
        <p className="text-lg font-bold text-ok">✓ Em đạt {m?.best_pct}%</p>
        <p className="text-muted">Chờ giáo viên mở chặng tiếp theo. Em có thể xem lại câu sai trong mục Kết quả.</p>
        <Link href="/lop-hoc/ket-qua/" className="inline-flex min-h-11 items-center font-semibold text-primary underline">Xem kết quả của em</Link>
      </div>
    );
  }
  if (state === "failed") {
    return (
      <div className="space-y-3">
        <p className="text-lg font-bold text-warn">Em được {m?.best_pct}% — cần từ {threshold}% để qua chặng</p>
        <p className="text-muted">Làm lại để đạt, điểm tốt nhất của em sẽ được tính.</p>
        <Link href={href} className={BTN}>Làm lại chặng {index + 1}</Link>
      </div>
    );
  }
  if (state === "doing") {
    return (
      <div className="space-y-3">
        <p className="font-semibold text-ink">Em đã trả lời {m?.answered}/{m?.total} câu</p>
        <Bar value={m?.answered ?? 0} max={m?.total ?? 0} />
        <Link href={href} className={BTN}>Tiếp tục làm</Link>
      </div>
    );
  }
  return (
    <div className="space-y-3">
      <p className="text-ink">Em chưa mở đề của chặng này.</p>
      <Link href={href} className={BTN}>Vào làm chặng {index + 1}</Link>
    </div>
  );
}

function openText(iso: string): string {
  return new Date(iso).toLocaleString("vi-VN", { hour: "2-digit", minute: "2-digit", weekday: "long", day: "2-digit", month: "2-digit" });
}

function dueText(iso: string): string {
  return new Date(iso).toLocaleString("vi-VN", { hour: "2-digit", minute: "2-digit", weekday: "short", day: "2-digit", month: "2-digit" });
}

/** Buổi tự học ở nhà: các chặng xếp thành danh sách, mỗi chặng một nút; không đồng hồ, có hạn nộp, chặng sau chờ chặng trước nếu giáo viên bật. */
function HomeView({ data, finished }: { data: MyReviewState; finished: boolean }) {
  const n = data.stages.length;
  const passedCount = data.stages.filter((s) => s.mine?.state === "passed").length;
  const overdue = !finished && data.due_at ? Date.parse(data.due_at) < Date.parse(data.now) : false;
  // Chặng đầu tiên chưa đạt và không khoá = việc tiếp theo của em.
  const nextIdx = data.stages.findIndex((s) => s.mine?.state !== "passed" && !s.locked);
  return (
    <div className="space-y-5">
      <div>
        <Link href="/lop-hoc/" className="inline-flex min-h-11 items-center gap-1.5 text-sm font-semibold text-primary">
          <ArrowLeft size={16} /> Lớp học
        </Link>
        <h1 className="font-display text-xl font-bold text-ink sm:text-2xl">{data.title}</h1>
        {data.due_at && (
          <p className={`mt-1 ${overdue ? "font-semibold text-warn" : "text-muted"}`}>
            {finished ? "Đã kết thúc" : overdue ? `Quá hạn từ ${dueText(data.due_at)} — em vẫn làm được, giáo viên sẽ thấy khi em nộp` : `Hạn nộp: ${dueText(data.due_at)}`}
          </p>
        )}
      </div>

      <section className="space-y-2" aria-label="Tiến độ của em">
        <p className="font-semibold text-ink">Em đã qua {passedCount}/{n} chặng</p>
        <Bar value={passedCount} max={n} tone="ok" />
        <p className="text-sm text-muted">
          Đạt từ {data.threshold}% là qua chặng. Chưa đạt thì làm lại, điểm tốt nhất được tính.
          {data.sequential ? " Chặng sau mở khi chặng trước đạt." : ""}
        </p>
      </section>

      <ol className="space-y-3" aria-label="Các chặng">
        {data.stages.map((s, i) => {
          const state = s.mine?.state ?? "idle";
          const href = examTakePath(s.exam_id, s.item_id);
          const isNext = !finished && i === nextIdx;
          return (
            <li
              key={i}
              aria-current={isNext ? "step" : undefined}
              className={`space-y-3 rounded-2xl border bg-panel p-4 ${isNext ? "border-primary" : "border-line"}`}
            >
              <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
                <span className="min-w-0 flex-1 basis-48 text-ink">
                  <span className="block text-sm font-semibold text-muted">Chặng {i + 1}/{n}</span>
                  <span className="block text-lg font-bold">{s.title}</span>
                </span>
                {s.locked ? (
                  <span className="inline-flex items-center gap-1 rounded-full bg-surface-2 px-2.5 py-1 text-xs font-bold text-muted">
                    <span aria-hidden>🔒</span>{s.open_at && Date.parse(s.open_at) > Date.parse(data.now) ? "Chưa tới ngày" : `Chờ chặng ${i}`}
                  </span>
                ) : (
                  <StatePill state={state} />
                )}
                {s.mine?.best_pct != null && <span className="text-sm tabular-nums text-muted">{s.mine.best_pct}%</span>}
              </div>
              {state === "doing" && (
                <div className="space-y-2">
                  <p className="text-sm text-ink">Em đã trả lời {s.mine?.answered}/{s.mine?.total} câu</p>
                  <Bar value={s.mine?.answered ?? 0} max={s.mine?.total ?? 0} />
                </div>
              )}
              {s.locked ? (
                <p className="text-sm text-muted">
                  {s.open_at && Date.parse(s.open_at) > Date.parse(data.now)
                    ? `Mở lúc ${openText(s.open_at)}.`
                    : `Làm chặng ${i} đạt ${data.threshold}% (hoặc nộp 2 lượt) để mở chặng này.`}
                </p>
              ) : finished ? null : state === "passed" ? (
                <Link href={href} className="inline-flex min-h-11 items-center font-semibold text-primary underline">Làm lại để ôn thêm</Link>
              ) : (
                <Link href={href} className={isNext ? BTN : "inline-flex min-h-11 items-center font-semibold text-primary underline"}>
                  {state === "doing" ? "Tiếp tục làm" : state === "failed" ? "Làm lại" : `Vào làm chặng ${i + 1}`}
                </Link>
              )}
              {s.class_submitted != null && s.class_total ? (
                <p className="text-xs text-muted">{s.class_submitted}/{s.class_total} bạn đã nộp chặng này</p>
              ) : null}
            </li>
          );
        })}
      </ol>

      {data.stages.some((s) => s.open_at) && <ClassRoster sessionId={data.id} stages={data.stages} now={data.now} />}
    </div>
  );
}

/** Nhân sự xem thử trang học sinh của một buổi ôn bằng `?id=` (học sinh không dùng; máy chủ chỉ cho nhân sự hoặc em trong lớp đó). */
function previewSessionId(): number | null {
  const n = Number(new URLSearchParams(window.location.search).get("id"));
  return Number.isInteger(n) && n > 0 ? n : null;
}

/** Trang của học sinh trong buổi ôn: chặng hiện tại, đồng hồ, việc của em, tiến độ chung của lớp (ẩn danh). */
export default function ReviewStudent() {
  const [data, setData] = useState<MyReviewState | null | undefined>(undefined);
  const [stamp, setStamp] = useState(0);

  const { error } = usePoll(
    () => getMyReviewState(previewSessionId()),
    (last) => (last?.mode === "self" ? 30000 : 5000),
    (d) => {
      setData(d);
      setStamp(Date.now());
    },
  );
  const running = data?.status === "running";
  const left = useCountdown(data?.secs_left ?? 0, stamp, running);
  const offline = Boolean(error) && data === undefined;

  if (data === undefined) {
    return <p className="text-muted">{offline ? "Chưa kết nối được. Em thử tải lại trang." : "Đang tìm buổi ôn của lớp em…"}</p>;
  }
  if (data === null) {
    return (
      <div className="rounded-2xl border border-line bg-panel p-6 text-center">
        <p className="text-lg font-semibold text-ink">Lớp em chưa có buổi ôn nào đang diễn ra</p>
        <p className="mt-1 text-muted">Khi giáo viên mở buổi ôn, trang này sẽ tự hiện chặng cho em.</p>
        <Link href="/lop-hoc/" className="mt-4 inline-flex min-h-11 items-center font-semibold text-primary underline">Về Lớp học</Link>
      </div>
    );
  }

  if (data.mode === "self") return <HomeView data={data} finished={data.status === "finished"} />;

  const n = data.stages.length;
  const idx = data.current_stage;
  const stage = idx >= 0 ? data.stages[idx] : null;
  const finished = data.status === "finished";
  const earlier = data.stages.slice(0, Math.max(0, idx)).map((s, i) => ({ s, i }));

  return (
    <div className="space-y-5">
      <div>
        <Link href="/lop-hoc/" className="inline-flex min-h-11 items-center gap-1.5 text-sm font-semibold text-primary">
          <ArrowLeft size={16} /> Lớp học
        </Link>
        <h1 className="font-display text-xl font-bold text-ink sm:text-2xl">{data.title}</h1>
      </div>

      <ol className="flex gap-2" aria-label="Các chặng">
        {data.stages.map((s, i) => {
          const passed = s.mine?.state === "passed";
          const now = !finished && i === idx;
          return (
            <li
              key={i}
              aria-current={now ? "step" : undefined}
              className={`grid size-10 place-items-center rounded-full text-sm font-bold ${
                passed ? "bg-surface-2 text-ok" : now ? "bg-primary text-white" : "border border-line-strong text-muted"
              }`}
            >
              {passed ? "✓" : i + 1}
            </li>
          );
        })}
      </ol>

      {finished ? (
        <section className="rounded-2xl border border-line bg-panel p-5">
          <p className="text-lg font-bold text-ink">Buổi ôn đã kết thúc</p>
          <p className="mt-1 text-muted">Cảm ơn em. Dưới đây là kết quả từng chặng của em.</p>
        </section>
      ) : !stage ? (
        <section className="rounded-2xl border border-line bg-panel p-5">
          <p className="text-lg font-bold text-ink">Chờ giáo viên mở chặng 1</p>
          <p className="mt-1 text-muted">Em giữ trang này mở, chặng sẽ tự hiện ra.</p>
        </section>
      ) : (
        <section className="space-y-4 rounded-2xl border border-line bg-panel p-5" aria-label={`Chặng ${idx + 1}`}>
          <div>
            <p className="text-sm font-semibold text-muted">Chặng {idx + 1}/{n}</p>
            <p className="text-xl font-bold text-ink">{stage.title}</p>
          </div>
          <p className="flex items-center gap-2 font-mono text-4xl font-bold tabular-nums text-ink" role="timer">
            <Clock size={26} aria-hidden className="text-muted" />
            {left > 0 ? clock(left) : <span className="text-2xl text-warn">Hết giờ chặng</span>}
          </p>
          {left <= 0 && (
            <p className="text-muted">Em nộp bài đang làm dở rồi chờ giáo viên mở chặng tiếp theo.</p>
          )}
          <MyAction stage={stage} index={idx} threshold={data.threshold} />
        </section>
      )}

      {data.class && !finished && stage && (
        <section aria-label="Cả lớp" className="space-y-2">
          <p className="font-semibold text-ink">{data.class.submitted}/{data.class.total} bạn đã nộp chặng này</p>
          <Bar value={data.class.submitted} max={data.class.total} tone="ok" />
          <p className="text-sm text-muted">Đạt từ {data.threshold}% là qua chặng. Chưa đạt thì làm lại để đạt.</p>
        </section>
      )}

      {(finished ? data.stages.map((s, i) => ({ s, i })) : earlier).length > 0 && (
        <section aria-label="Các chặng trước" className="space-y-2">
          <h2 className="text-base font-bold text-ink">{finished ? "Kết quả của em" : "Các chặng trước"}</h2>
          <ul className="divide-y divide-line rounded-2xl border border-line bg-panel">
            {(finished ? data.stages.map((s, i) => ({ s, i })) : earlier).map(({ s, i }) => (
              <li key={i} className="flex flex-wrap items-center gap-x-3 gap-y-1 px-4 py-3">
                <span className="min-w-0 flex-1 basis-40 text-ink">
                  <span className="font-semibold">Chặng {i + 1}</span> · {s.title}
                </span>
                <StatePill state={s.mine?.state ?? "idle"} />
                {s.mine?.best_pct != null && <span className="text-sm tabular-nums text-muted">{s.mine.best_pct}%</span>}
                {s.mine?.state !== "passed" && !finished && (
                  <Link href={examTakePath(s.exam_id, s.item_id)} className="inline-flex min-h-11 items-center font-semibold text-primary underline">
                    {s.mine?.state === "failed" ? "Làm lại" : "Vào làm"}
                  </Link>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
