/**
 * Phân tích bài làm cả lớp TRƯỚC khi chữa — phần tính bằng máy (không tốn AI, hiện ngay):
 *  - gom câu theo chủ đề (q.topic), tỉ lệ đúng trung bình, số câu "khó" (<50%);
 *  - với mỗi câu: phương án sai được chọn nhiều nhất (trắc nghiệm), ý a–d sai nhiều nhất (đúng–sai),
 *    đáp số sai hay gặp (trả lời ngắn).
 * Đồng thời dựng gói dữ liệu GỌN gửi Edge Function `analyze-exam-results` (chỉ số liệu gộp cả lớp,
 * không có tên/mã học sinh).
 */
import type { ExamQuestion } from "@/features/exams/types";
import type { ExamReviewData, ReviewQuestionStat } from "@/services/analytics";
import { stripHtmlToText } from "@/lib/strip-html";

const LETTERS = ["A", "B", "C", "D"];
export const NO_TOPIC = "(chưa gắn chủ đề)";

export interface QuestionInsight {
  index: number;
  pct: number | null; // % cả lớp làm đúng; null = chưa có lượt
  topic: string;
  /** Mô tả ngắn lỗi hay gặp, vd "38% chọn B", "ý c) chỉ 20% đúng", "6 em ghi 2,5". */
  commonWrong: string;
}

export interface TopicInsight {
  topic: string;
  questionIndexes: number[];
  pct: number | null; // trung bình % đúng các câu có lượt làm
  hardCount: number; // số câu < 50%
  level: "cao" | "vua" | "thap"; // mức cần ôn
}

export interface ReviewInsights {
  attempts: number;
  avgPct: number | null;
  questions: QuestionInsight[];
  topics: TopicInsight[]; // cần ôn nhất lên trước
  /** Thứ tự chữa gợi ý: câu sai nhiều nhất trước, bỏ câu ≥ 80% đúng. */
  reviewOrder: number[];
}

export function pctOf(stat: ReviewQuestionStat | undefined): number | null {
  return stat && stat.attempted > 0 ? Math.round((stat.correctN / stat.attempted) * 100) : null;
}

function commonWrongOf(q: ExamQuestion, stat: ReviewQuestionStat): string {
  if (stat.attempted === 0) return "";
  if (q.type === "multiple_choice" && stat.optionCounts) {
    let best = -1;
    stat.optionCounts.forEach((n, i) => {
      if (i !== q.answer && n > 0 && (best < 0 || n > stat.optionCounts![best])) best = i;
    });
    if (best < 0) return "";
    return `${Math.round((stat.optionCounts[best] / stat.attempted) * 100)}% chọn ${LETTERS[best]}`;
  }
  if (q.type === "true_false" && stat.statementCorrectN) {
    let worst = 0;
    stat.statementCorrectN.forEach((n, i) => {
      if (n < stat.statementCorrectN![worst]) worst = i;
    });
    const p = Math.round((stat.statementCorrectN[worst] / stat.attempted) * 100);
    return p < 75 ? `ý ${String.fromCharCode(97 + worst)}) chỉ ${p}% đúng` : "";
  }
  if (q.type === "short_answer" && stat.wrongAnswers) {
    const top = Object.entries(stat.wrongAnswers).sort((a, b) => b[1] - a[1])[0];
    return top && top[1] >= 2 ? `${top[1]} em ghi ${top[0]}` : "";
  }
  return "";
}

export function computeReviewInsights(data: ExamReviewData): ReviewInsights {
  const questions: QuestionInsight[] = data.questions.map((q, i) => ({
    index: i,
    pct: pctOf(data.stats[i]),
    topic: (q.topic ?? "").trim() || NO_TOPIC,
    commonWrong: commonWrongOf(q, data.stats[i]),
  }));

  const byTopic = new Map<string, QuestionInsight[]>();
  for (const qi of questions) byTopic.set(qi.topic, [...(byTopic.get(qi.topic) ?? []), qi]);

  const topics: TopicInsight[] = [...byTopic.entries()].map(([topic, qs]) => {
    const withPct = qs.filter((x) => x.pct !== null);
    const pct = withPct.length ? Math.round(withPct.reduce((s, x) => s + (x.pct ?? 0), 0) / withPct.length) : null;
    const hardCount = withPct.filter((x) => (x.pct ?? 100) < 50).length;
    const level: TopicInsight["level"] = pct === null ? "thap" : pct < 50 || hardCount >= 2 ? "cao" : pct < 70 ? "vua" : "thap";
    return { topic, questionIndexes: qs.map((x) => x.index), pct, hardCount, level };
  });
  topics.sort((a, b) => (a.pct ?? 101) - (b.pct ?? 101));

  const scored = questions.filter((x) => x.pct !== null);
  const avgPct = scored.length ? Math.round(scored.reduce((s, x) => s + (x.pct ?? 0), 0) / scored.length) : null;
  const reviewOrder = scored
    .filter((x) => (x.pct ?? 100) < 80)
    .sort((a, b) => (a.pct ?? 0) - (b.pct ?? 0))
    .map((x) => x.index);

  return { attempts: data.totalStudents, avgPct, questions, topics, reviewOrder };
}

// ---------- Gói gửi AI ----------

export interface AiQuestionPayload {
  index: number;
  type: ExamQuestion["type"];
  topic: string;
  pct: number | null;
  text: string;
  options?: { label: string; text: string; pct: number }[]; // trắc nghiệm
  answer?: string; // chữ cái đúng / đáp số
  statements?: { label: string; text: string; answer: boolean; pctCorrect: number }[];
  wrongAnswers?: { value: string; n: number }[];
  explanation?: string;
}

export interface AiAnalysisPayload {
  examTitle: string;
  attempts: number;
  questions: AiQuestionPayload[];
}

/** Câu khó (<70%) gửi đủ chữ + lời giải; câu dễ chỉ gửi đề rút gọn để tiết kiệm token. */
export function buildAiPayload(data: ExamReviewData): AiAnalysisPayload {
  const questions = data.questions.map((q, i): AiQuestionPayload => {
    const stat = data.stats[i];
    const pct = pctOf(stat);
    const hard = pct !== null && pct < 70;
    const n = Math.max(1, stat.attempted);
    const base: AiQuestionPayload = {
      index: i,
      type: q.type,
      topic: (q.topic ?? "").trim(),
      pct,
      text: stripHtmlToText(q.question, hard ? 700 : 160),
    };
    if (q.type === "multiple_choice") {
      base.answer = LETTERS[q.answer] ?? "";
      if (hard)
        base.options = q.options.map((o, oi) => ({
          label: LETTERS[oi],
          text: stripHtmlToText(o, 120),
          pct: Math.round(((stat.optionCounts?.[oi] ?? 0) / n) * 100),
        }));
    } else if (q.type === "true_false") {
      base.statements = q.statements.map((s, si) => ({
        label: `${String.fromCharCode(97 + si)})`,
        text: stripHtmlToText(s.text, hard ? 200 : 80),
        answer: s.answer,
        pctCorrect: Math.round(((stat.statementCorrectN?.[si] ?? 0) / n) * 100),
      }));
    } else if (q.type === "short_answer") {
      base.answer = q.answer;
      base.wrongAnswers = Object.entries(stat.wrongAnswers ?? {})
        .sort((a, b) => b[1] - a[1])
        .slice(0, 4)
        .map(([value, cnt]) => ({ value, n: cnt }));
    }
    if (hard && "explanation" in q && q.explanation) base.explanation = stripHtmlToText(q.explanation, 500);
    return base;
  });
  return { examTitle: data.examTitle, attempts: data.totalStudents, questions };
}
