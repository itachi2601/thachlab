"use client";

import Link from "next/link";
import {
  gradeQuestion,
  type ExamQuestion,
  type QuestionResponse,
} from "@/features/exams/types";

/** Ngưỡng trùng với mastery (docs/mastery-rules.md): ≥80% vững, 50–79% cần củng cố, <50% cần học lại. */
const SOLID = 0.8;
const MID = 0.5;

interface TopicStat {
  name: string;
  earned: number;
  max: number;
  wrong: number;
  total: number;
  /** số câu sai thuộc dạng lý thuyết / bài tập (theo nhãn `form`) */
  wrongTheory: number;
  wrongExercise: number;
}

function isBlank(q: ExamQuestion, r: QuestionResponse) {
  if (q.type === "multiple_choice") return r === null || r === undefined;
  if (q.type === "true_false") return Array.isArray(r) && r.every((x) => x === null);
  return typeof r !== "string" || r.trim() === "";
}

/**
 * Nhận xét thích ứng sau khi nộp đề: đọc kết quả LƯỢT NÀY theo nhãn Chủ đề/Dạng của từng câu,
 * chỉ ra chủ đề nào cần xem lại và xem lại theo cách nào (lý thuyết hay luyện dạng bài).
 * Thuần đọc props — không thêm query Supabase (QUY-TAC-THIET-KE: tải nhận thức thấp, 1 việc tiếp theo rõ).
 */
export default function ExamAdaptiveFeedback({
  questions,
  responses,
  lessonByTopic,
  detailAnchor,
}: {
  questions: ExamQuestion[];
  responses: QuestionResponse[];
  lessonByTopic: Map<string, number | null>;
  detailAnchor: string;
}) {
  const byTopic = new Map<string, TopicStat>();
  let earned = 0;
  let max = 0;
  let blank = 0;
  let graded = 0;

  questions.forEach((q, qi) => {
    if (q.type === "essay") return;
    const g = gradeQuestion(q, responses[qi]);
    graded += 1;
    earned += g.earned;
    max += g.max;
    const wrong = g.earned < g.max;
    if (wrong && isBlank(q, responses[qi])) blank += 1;
    const name = (q.topic ?? "").trim();
    if (!name) return;
    const s =
      byTopic.get(name) ??
      { name, earned: 0, max: 0, wrong: 0, total: 0, wrongTheory: 0, wrongExercise: 0 };
    s.earned += g.earned;
    s.max += g.max;
    s.total += 1;
    if (wrong) {
      s.wrong += 1;
      if (q.form === "ly_thuyet") s.wrongTheory += 1;
      else if (q.form === "bai_tap") s.wrongExercise += 1;
    }
    byTopic.set(name, s);
  });

  if (graded === 0 || max === 0) return null;
  const pct = earned / max;
  const topics = [...byTopic.values()];
  const weak = topics
    .filter((t) => t.max > 0 && t.earned / t.max < SOLID)
    .sort((a, b) => a.earned / a.max - b.earned / b.max)
    .slice(0, 4);
  const strong = topics.filter((t) => t.max > 0 && t.earned / t.max >= SOLID);

  // Lời mở đầu theo mức điểm + dạng sai (không dùng vai "thầy").
  let lead: string;
  if (pct >= 0.9 && weak.length === 0) {
    lead = "Làm chắc tay ở mọi chủ đề. Có thể sang bài tiếp theo hoặc thử đề khó hơn.";
  } else if (pct >= 0.7) {
    lead = weak.length
      ? "Nền tảng khá vững — chỉ cần vá đúng chỗ hổng nhỏ bên dưới là lên mức cao."
      : "Kết quả tốt. Xem lại các câu sai để chốt chắc.";
  } else if (pct >= 0.5) {
    lead = "Em nắm được một nửa. Ưu tiên ôn từng chủ đề bên dưới, từ trên xuống, rồi làm lại đề.";
  } else {
    lead = "Phần lớn kiến thức chưa chắc. Đừng làm lại đề ngay — đọc lại lý thuyết từng chủ đề bên dưới trước, rồi mới luyện.";
  }

  const adviceFor = (t: TopicStat) => {
    const r = t.earned / t.max;
    if (t.wrongTheory > t.wrongExercise) return "Sai ở câu lý thuyết — đọc lại phần khái niệm/định nghĩa.";
    if (t.wrongExercise > t.wrongTheory) return "Sai ở câu bài tập — xem lại bài mẫu rồi tự làm lại các bước.";
    return r < MID ? "Chưa vững — đọc lại lý thuyết rồi làm bài mẫu." : "Gần đúng rồi — xem lại các câu sai để tìm chỗ nhầm.";
  };

  return (
    <section
      aria-label="Nhận xét và gợi ý ôn tập"
      className="mt-4 rounded-2xl border border-white/10 bg-white/[0.03] p-4 sm:p-5"
    >
      <h2 className="font-display text-lg font-semibold text-white">Nhận xét cho em</h2>
      <p className="mt-1 text-sm leading-relaxed text-slate-300">{lead}</p>

      {blank > 0 && (
        <p className="mt-2 text-sm text-slate-400">
          Có {blank} câu để trống. Lần sau cứ chọn đáp án em nghĩ gần đúng nhất rồi đánh dấu quay lại — câu trống chắc chắn không có điểm.
        </p>
      )}

      {weak.length > 0 && (
        <>
          <h3 className="mt-4 text-sm font-semibold text-white">Nên xem lại</h3>
          <ul className="mt-2 space-y-2">
            {weak.map((t) => {
              const lessonId = lessonByTopic.get(t.name);
              const stage = t.wrongTheory > t.wrongExercise ? "ly_thuyet" : "bai_tap_mau";
              const r = t.earned / t.max;
              return (
                <li key={t.name} className="rounded-xl bg-amber-500/10 p-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="text-sm font-semibold text-amber-200">{t.name}</span>
                    <span className="text-xs text-slate-400">
                      sai {t.wrong}/{t.total} câu · {r < MID ? "cần học lại" : "cần củng cố"}
                    </span>
                  </div>
                  <p className="mt-1 text-sm text-slate-300">{adviceFor(t)}</p>
                  {lessonId && (
                    <Link
                      href={`/lop-hoc/bai/?id=${lessonId}#secondary-stage-${stage}`}
                      className="mt-2 inline-flex min-h-11 items-center text-sm font-semibold text-primary hover:underline"
                    >
                      Ôn chủ đề này →
                    </Link>
                  )}
                </li>
              );
            })}
          </ul>
        </>
      )}

      {strong.length > 0 && (
        <p className="mt-3 text-sm text-emerald-300">
          Đã vững: {strong.map((t) => t.name).join(", ")}.
        </p>
      )}

      <a
        href={`#${detailAnchor}`}
        className="mt-3 inline-flex min-h-11 items-center text-sm font-semibold text-primary hover:underline"
      >
        Xem lại từng câu sai ↓
      </a>
    </section>
  );
}
