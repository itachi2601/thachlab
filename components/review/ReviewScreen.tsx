"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useCountdown, usePoll } from "@/components/quiz-live/shared";
import { getReviewBoard, reviewErrorText, type ReviewBoard } from "@/services/review-session";
import { examQrUrl } from "@/lib/exam-link";
import { reviewStudentUrl } from "@/lib/review-link";
import QrBox from "./QrBox";
import { Bar, clock } from "./shared";

/**
 * Màn hình chiếu lên tivi: chỉ thứ cả lớp cần nhìn trong 2 giây — chặng nào, còn bao lâu, quét mã/nhập số đề nào,
 * cả lớp đã nộp bao nhiêu. KHÔNG có tên em nào (tuổi 14–18 nhạy việc bị bạn thấy mình ở cuối bảng); chi tiết từng em
 * chỉ có ở màn hình điều phối của giáo viên/trợ giảng.
 */
export default function ReviewScreen({ sessionId }: { sessionId: number }) {
  const [board, setBoard] = useState<ReviewBoard | null>(null);
  const [stamp, setStamp] = useState(0);
  const [fatal, setFatal] = useState("");

  const { error } = usePoll(
    () => getReviewBoard(sessionId),
    () => 3000,
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
  const left = useCountdown(sess?.secs_left ?? 0, stamp, running);

  const stat = useMemo(() => {
    const st = board?.students ?? [];
    const submitted = st.filter((s) => s.state === "passed" || s.state === "failed").length;
    return { submitted, passed: st.filter((s) => s.state === "passed").length, total: st.length };
  }, [board]);

  if (fatal) {
    return (
      <main className="grid min-h-screen place-items-center bg-white p-8 text-center text-slate-900">
        <div>
          <p className="text-xl">{fatal}</p>
          <Link href="/tro-giang/on-tap/" className="mt-4 inline-block font-semibold text-blue-700 underline">Về danh sách buổi ôn</Link>
        </div>
      </main>
    );
  }
  if (!board || !sess) {
    return <main className="grid min-h-screen place-items-center bg-white text-xl text-slate-600">Đang tải…</main>;
  }

  const n = sess.stages.length;
  const stage = idx >= 0 ? sess.stages[idx] : null;

  return (
    <main className="min-h-screen bg-white px-6 py-8 text-slate-900 sm:px-12">
      <div className="mx-auto flex min-h-[calc(100vh-4rem)] max-w-6xl flex-col">
        <header className="flex flex-wrap items-baseline justify-between gap-3">
          <h1 className="text-2xl font-bold sm:text-3xl">{sess.title}</h1>
          <ol className="flex gap-2" aria-label="Các chặng">
            {sess.stages.map((_, i) => (
              <li
                key={i}
                className={`grid size-9 place-items-center rounded-full text-base font-bold ${
                  sess.status === "finished" || i < idx
                    ? "bg-slate-200 text-slate-600"
                    : i === idx
                      ? "bg-blue-700 text-white"
                      : "border-2 border-slate-300 text-slate-500"
                }`}
              >
                {sess.status === "finished" || i < idx ? "✓" : i + 1}
              </li>
            ))}
          </ol>
        </header>

        {sess.status === "finished" ? (
          <section className="grid flex-1 place-items-center text-center">
            <div>
              <p className="text-5xl font-bold">Hết buổi ôn</p>
              <p className="mt-4 text-2xl text-slate-600">Cảm ơn cả lớp. Chặng cuối: {stat.passed}/{stat.total} bạn đạt.</p>
            </div>
          </section>
        ) : !stage ? (
          <section className="grid flex-1 place-items-center">
            <div className="text-center">
              <p className="text-4xl font-bold sm:text-5xl">Quét mã để vào buổi ôn</p>
              <div className="mt-8 flex justify-center">
                <QrBox text={reviewStudentUrl()} label="Mã QR vào buổi ôn tập" className="size-72 sm:size-80" />
              </div>
              <p className="mt-6 text-2xl text-slate-600">Hoặc vào Lớp học → Buổi ôn. Chờ giáo viên mở chặng 1.</p>
            </div>
          </section>
        ) : (
          <section className="grid flex-1 items-center gap-8 py-6 lg:grid-cols-2">
            <div>
              <p className="text-2xl font-semibold text-slate-600">Chặng {idx + 1}/{n}</p>
              <p className="mt-1 text-4xl font-bold leading-tight sm:text-5xl">{stage.title}</p>
              <p
                className={`mt-8 font-mono text-8xl font-bold tabular-nums sm:text-9xl ${left > 0 ? "text-slate-900" : "text-amber-700"}`}
                role="timer"
                aria-label={left > 0 ? `Còn ${clock(left)}` : "Hết giờ"}
              >
                {left > 0 ? clock(left) : "Hết giờ"}
              </p>
              {left <= 0 && <p className="mt-2 text-2xl text-slate-600">Nộp bài đang làm rồi chờ chặng tiếp theo.</p>}
              <div className="mt-8 max-w-xl">
                <p className="mb-2 text-2xl font-semibold">{stat.submitted}/{stat.total} bạn đã nộp</p>
                <Bar value={stat.submitted} max={stat.total} tone="ok" />
              </div>
              <p className="mt-6 text-xl text-slate-600">
                Đạt từ <strong className="text-slate-900">{sess.threshold}%</strong> là qua chặng. Chưa đạt thì làm lại để đạt.
              </p>
            </div>
            <div className="text-center">
              <div className="flex justify-center">
                <QrBox text={examQrUrl(stage.exam_id, stage.item_id)} label={`Mã QR mở đề chặng ${idx + 1}`} className="size-72 sm:size-96" />
              </div>
              <p className="mt-4 text-2xl text-slate-600">Quét mã, hoặc nhập số đề ở mục Quét mã</p>
              <p className="font-mono text-6xl font-bold tabular-nums sm:text-7xl">{stage.exam_id}</p>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
