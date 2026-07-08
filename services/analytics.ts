import { getSupabase } from "@/services/supabase";

export interface ScorePoint {
  date: string;
  score: number;
  examTitle: string;
}

export interface TopicStats {
  topic: string;
  total: number;
  wrong: number;
  correct: number;
  percentage: number; // % câu sai
}

/** Lấy điểm qua thời gian cho biểu đồ line chart */
export async function fetchScoreHistory(userId: string): Promise<ScorePoint[]> {
  const { data } = await getSupabase()
    .from("exam_results")
    .select("created_at, score, exams(title)")
    .eq("student_id", userId)
    .order("created_at", { ascending: true });

  return (data ?? []).map((row: any) => ({
    date: new Date(row.created_at).toLocaleDateString("vi-VN"),
    score: Number(row.score),
    examTitle: row.exams?.title ?? "(Đề đã xóa)",
  }));
}

/** Lấy thống kê câu sai theo topic */
export async function fetchWrongTopicStats(userId: string): Promise<TopicStats[]> {
  try {
    const { data, error } = await getSupabase()
      .from("exam_question_results")
      .select("topic, is_correct")
      .in(
        "exam_result_id",
        // Lấy tất cả exam result IDs của user
        await getSupabase()
          .from("exam_results")
          .select("id")
          .eq("student_id", userId)
          .then(({ data }) => (data ?? []).map((r: any) => r.id))
      );

    // Nếu bảng chưa tồn tại hoặc chưa có dữ liệu, return empty array
    if (error || !data || data.length === 0) {
      return [];
    }

    // Tính toán thống kê theo topic
    const topicMap = new Map<
      string,
      { total: number; correct: number; wrong: number }
    >();

    for (const row of data) {
      const stats = topicMap.get(row.topic) ?? { total: 0, correct: 0, wrong: 0 };
      stats.total += 1;
      if (row.is_correct) {
        stats.correct += 1;
      } else {
        stats.wrong += 1;
      }
      topicMap.set(row.topic, stats);
    }

    // Convert to array, sort by số câu sai giảm dần
    return Array.from(topicMap.entries())
      .map(([topic, stats]) => ({
        topic,
        total: stats.total,
        correct: stats.correct,
        wrong: stats.wrong,
        percentage: Math.round((stats.wrong / stats.total) * 100),
      }))
      .sort((a, b) => b.wrong - a.wrong);
  } catch (err) {
    console.warn("Cannot fetch wrong topic stats:", err);
    return [];
  }
}

/** Lấy chi tiết câu sai của một topic cụ thể */
export interface DetailedWrongQuestion {
  examTitle: string;
  examDate: string;
  questionIndex: number;
  isCorrect: boolean;
}

export async function fetchWrongQuestionsByTopic(
  userId: string,
  topic: string
): Promise<DetailedWrongQuestion[]> {
  const { data: resultIds } = await getSupabase()
    .from("exam_results")
    .select("id, created_at, exams(title)")
    .eq("student_id", userId)
    .order("created_at", { ascending: false });

  if (!resultIds || resultIds.length === 0) {
    return [];
  }

  const resultMap = new Map(
    resultIds.map((r: any) => [
      r.id,
      {
        date: new Date(r.created_at).toLocaleDateString("vi-VN"),
        title: r.exams?.title ?? "(Đề đã xóa)",
      },
    ])
  );

  const { data } = await getSupabase()
    .from("exam_question_results")
    .select("exam_result_id, question_index, is_correct")
    .eq("topic", topic)
    .in("exam_result_id", Array.from(resultMap.keys()))
    .order("exam_result_id", { ascending: false })
    .order("question_index");

  return (data ?? []).map((row: any) => {
    const result = resultMap.get(row.exam_result_id);
    return {
      examTitle: result?.title ?? "(Đề đã xóa)",
      examDate: result?.date ?? "—",
      questionIndex: row.question_index,
      isCorrect: row.is_correct,
    };
  });
}
