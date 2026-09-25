"use client";

import { useCallback, useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";
import Badge from "@/components/ui/Badge";
import TopicPracticeModal from "@/components/mastery/TopicPracticeModal";
import {
  MASTERY_ICON,
  MASTERY_LABEL,
  MASTERY_TONE,
  MIN_ANSWERS_FOR_LABEL,
  fetchLessonMastery,
  needsPractice,
  type LessonMastery,
  type TopicMastery,
} from "@/services/mastery";

/**
 * Thẻ nhãn mastery từng YCCĐ của bài — hiện cuối trang bài học (app/lop-hoc/bai/page.tsx), gần
 * mục luyện tập/kiểm tra để học sinh thấy ngay sau khi nộp bài. Gọi ĐÚNG 1 RPC
 * (get_lesson_mastery) khi mở bài; có nút "Làm mới" để tự cập nhật sau khi vừa làm thêm câu,
 * tránh phải thêm hook vào PracticeSession/ExamRunner (trang này đã tối ưu, không refetch tự
 * động sau khi nộp bài — xem perf/RESULT.md; nút refresh giữ đúng quy ước đó).
 */
export default function LessonMasteryCard({
  lessonId,
  examIds,
  loggedIn,
}: {
  lessonId: number;
  examIds: number[];
  loggedIn: boolean;
}) {
  // "pending" gộp cả lúc mới mount lẫn lúc đang tải lại — tránh setState đồng bộ ngay đầu effect
  // (không dùng riêng cờ "loading" đặt trước khi gọi fetch, theo đúng cách
  // components/rank/FixQuizModal.tsx đang làm: effect chỉ gọi thẳng promise, setState nằm trong
  // .then()/.catch()).
  const [state, setState] = useState<"pending" | "ready" | "error">("pending");
  const [mastery, setMastery] = useState<LessonMastery | null>(null);
  const [practiceTopic, setPracticeTopic] = useState<TopicMastery | null>(null);

  const load = useCallback(() => {
    fetchLessonMastery(lessonId)
      .then((m) => {
        setMastery(m);
        setState("ready");
      })
      .catch(() => setState("error"));
  }, [lessonId]);

  useEffect(() => {
    if (!loggedIn) return;
    load();
  }, [loggedIn, load]);

  function refresh() {
    setState("pending");
    load();
  }

  if (!loggedIn) return null;
  if (state === "pending") return <p className="lesson-muted">Đang tính mức độ thành thạo…</p>;
  if (state === "error" || !mastery) return null; // RPC chưa chạy/lỗi — im lặng, không chặn trang.

  return (
    <section className="lesson-section" aria-label="Mức độ thành thạo theo yêu cầu cần đạt">
      <h2>
        <span>
          <RefreshCw size={14} />
        </span>
        Mức độ thành thạo
        <button
          type="button"
          onClick={refresh}
          title="Làm mới"
          aria-label="Làm mới mức độ thành thạo"
          style={{ marginLeft: 8, fontSize: 12, color: "var(--color-muted)", background: "none", border: "none", cursor: "pointer" }}
        >
          Làm mới
        </button>
      </h2>
      <div className="lesson-stack" style={{ gap: 10 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span aria-hidden>{MASTERY_ICON[mastery.lessonLevel]}</span>
          <Badge tone={MASTERY_TONE[mastery.lessonLevel]}>Cả bài: {MASTERY_LABEL[mastery.lessonLevel]}</Badge>
        </div>

        {mastery.topics.length === 0 ? (
          <p className="lesson-muted">Bài này chưa chia yêu cầu cần đạt riêng.</p>
        ) : (
          <ul style={{ display: "grid", gap: 8, listStyle: "none", padding: 0, margin: 0 }}>
            {mastery.topics.map((t) => (
              <li
                key={t.topicId}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  gap: 10,
                  flexWrap: "wrap",
                  padding: "8px 10px",
                  borderRadius: 10,
                  border: "1px solid var(--color-line)",
                }}
              >
                <span style={{ display: "flex", alignItems: "center", gap: 8, minWidth: 0 }}>
                  <span aria-hidden>{MASTERY_ICON[t.level]}</span>
                  <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{t.topicName}</span>
                </span>
                <span style={{ display: "flex", alignItems: "center", gap: 8, flexShrink: 0 }}>
                  <Badge tone={MASTERY_TONE[t.level]}>
                    {t.level === "insufficient"
                      ? `Làm thêm ${Math.max(1, MIN_ANSWERS_FOR_LABEL - t.answeredCount)} câu`
                      : `${MASTERY_LABEL[t.level]} · ${t.pct}% (${t.answeredCount} câu)`}
                  </Badge>
                  {needsPractice(t.level) && (
                    <button
                      type="button"
                      onClick={() => setPracticeTopic(t)}
                      className="lesson-done"
                      style={{ padding: "4px 10px", fontSize: 12 }}
                    >
                      Luyện 10 câu phần này
                    </button>
                  )}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {practiceTopic && (
        <TopicPracticeModal
          lessonId={lessonId}
          examIds={examIds}
          topicName={practiceTopic.topicName}
          onClose={() => setPracticeTopic(null)}
          onFinished={refresh}
        />
      )}
    </section>
  );
}
