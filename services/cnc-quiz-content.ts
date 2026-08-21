import { getSupabase } from "@/services/supabase";

export type CncQuizQuestionType = "multiple_choice" | "short_answer";

export type CncQuizQuestion = {
  id: string;
  quiz_key: string;
  question_type: CncQuizQuestionType;
  question: string;
  options: string[] | null;
  correct_index: number | null;
  keywords: string[] | null;
  min_keyword_matches: number | null;
  explanation: string;
  order_index: number;
};

const fields =
  "id, quiz_key, question_type, question, options, correct_index, keywords, min_keyword_matches, explanation, order_index";

const cache = new Map<string, CncQuizQuestion[]>();

export async function fetchQuizQuestions(quizKey: string, { fresh = false }: { fresh?: boolean } = {}) {
  if (!fresh && cache.has(quizKey)) return cache.get(quizKey)!;
  const { data, error } = await getSupabase()
    .from("cnc_quiz_questions")
    .select(fields)
    .eq("quiz_key", quizKey)
    .order("order_index", { ascending: true });
  if (error) throw error;
  const rows = (data ?? []) as CncQuizQuestion[];
  cache.set(quizKey, rows);
  return rows;
}

export function invalidateQuizCache(quizKey?: string) {
  if (quizKey) cache.delete(quizKey);
  else cache.clear();
}

export async function upsertQuizQuestion(input: Omit<CncQuizQuestion, "order_index"> & { order_index?: number }) {
  const supabase = getSupabase();
  const { data: userData } = await supabase.auth.getUser();
  const { data, error } = await supabase
    .from("cnc_quiz_questions")
    .upsert(
      {
        id: input.id,
        quiz_key: input.quiz_key,
        question_type: input.question_type,
        question: input.question,
        options: input.options,
        correct_index: input.correct_index,
        keywords: input.keywords,
        min_keyword_matches: input.min_keyword_matches,
        explanation: input.explanation,
        order_index: input.order_index ?? 0,
        updated_by: userData.user?.id ?? null,
        updated_at: new Date().toISOString(),
      },
      { onConflict: "id" },
    )
    .select(fields)
    .single();
  if (error) throw error;
  invalidateQuizCache(input.quiz_key);
  return data as CncQuizQuestion;
}

export async function deleteQuizQuestion(id: string, quizKey: string) {
  const { error } = await getSupabase().from("cnc_quiz_questions").delete().eq("id", id);
  if (error) throw error;
  invalidateQuizCache(quizKey);
}

export function normalizeAnswerText(value: string) {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/gi, "d")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

export function gradeShortAnswer(answer: string, keywords: string[], minMatches: number) {
  const normalizedAnswer = normalizeAnswerText(answer);
  const matched = keywords.filter((keyword) => normalizedAnswer.includes(normalizeAnswerText(keyword)));
  return { matchedCount: matched.length, matchedKeywords: matched, passed: matched.length >= minMatches };
}
