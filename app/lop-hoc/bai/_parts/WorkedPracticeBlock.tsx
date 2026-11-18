"use client";

import type { MutableRefObject } from "react";
import { Check } from "lucide-react";
import SampleQuestionsGrid from "@/components/lessons/SampleQuestionsGridLazy";
import WorkedQuestionsGrid from "@/components/lessons/WorkedQuestionsGridLazy";
import PracticeSession from "@/components/lessons/PracticeSessionLazy";
import type { LessonItem } from "@/features/lessons/types";
import { ACCENT } from "./lesson-nav";
import { workedSubtitle } from "./LessonBits";
import { TheorySummary } from "./TheoryBlock";

/** Mục Bài tập mẫu (lưới dạng bài có lời giải) hoặc Luyện tập (PracticeSession bốc câu từ ngân hàng). */
export function WorkedPracticeBlock({
  item,
  plain,
  showSummaries,
  theoryItems,
  workedState,
  onRetryWorked,
  onPresent,
  lessonId,
  poolExamIds,
  recordProgress,
  practiceActiveRef,
  done,
  onDone,
}: {
  item: LessonItem;
  /** Mục duy nhất của phần → ẩn tiêu đề riêng. */
  plain: boolean;
  /** Mục Luyện tập đầu tiên: hiện tóm tắt các mục lý thuyết (theoryItems) phía trên. */
  showSummaries: boolean;
  theoryItems: LessonItem[];
  workedState: "loading" | "failed";
  onRetryWorked: () => void;
  /** Chỉ giáo viên: trình chiếu bài tập mẫu từ dạng thứ `start`. */
  onPresent?: (start: number) => void;
  lessonId: number;
  poolExamIds: number[];
  recordProgress: boolean;
  /** PracticeSession báo đang làm dở — đổi tab sẽ unmount và mất bài, nên trang hỏi trước. */
  practiceActiveRef: MutableRefObject<boolean>;
  done: boolean;
  onDone: () => void;
}) {
  // Phụ đề lưu trong DB dễ lệch số: Luyện tập ghi số câu của MỘT đề gắn kèm trong khi PracticeSession bốc từ cả
  // ngân hàng (đã tự báo "Ngân hàng có N câu") → bỏ; Bài tập mẫu đếm cả mục tự luận cũ là "dạng" → đếm lại (N3).
  const blockSub = item.kind === "luyen_tap" ? "" : workedSubtitle(item);
  return (
    <div id={`lesson-item-${item.id}`} className="lesson-block" data-item={item.id}>
      {showSummaries && (
        <div className="mb-4">
          {theoryItems.map((t) => (
            <TheorySummary key={t.id} html={t.summary_html} title={t.title} />
          ))}
        </div>
      )}
      {(!plain || blockSub) && (
        <div className="lesson-block-head">
          {!plain && <p className="lesson-block-title">{item.title}</p>}
          {blockSub && <p className="lesson-block-sub">{blockSub}</p>}
        </div>
      )}
      {item.kind === "bai_tap_mau" ? (
        <>
          {item.exam_ids.length > 0 && <SampleQuestionsGrid examIds={item.exam_ids} color={ACCENT} />}
          {item.questions.length === 0 && (item.questions_count ?? 0) > 0 ? (
            // DB có dạng bài nhưng lời giải chưa về (file tĩnh không chứa): báo rõ, không để lưới trống (N3, L4).
            <p className="lesson-block-sub" role="status" aria-live="polite">
              {workedState === "failed" ? (
                <>
                  Chưa tải được {item.questions_count} dạng bài.{" "}
                  <button type="button" className="lesson-btn-ghost" onClick={onRetryWorked}>
                    Tải lại
                  </button>
                </>
              ) : (
                `Đang tải ${item.questions_count} dạng bài…`
              )}
            </p>
          ) : (
            <WorkedQuestionsGrid
              questions={item.questions}
              color={ACCENT}
              lessonId={item.lesson_id}
              onPresent={onPresent}
            />
          )}
        </>
      ) : (
        <PracticeSession
          examIds={item.exam_ids}
          poolExamIds={poolExamIds}
          lessonId={lessonId}
          itemId={item.id}
          passScore={item.practice_pass_score}
          color={ACCENT}
          recordProgress={recordProgress}
          onActiveChange={(active) => {
            practiceActiveRef.current = active;
          }}
        />
      )}
      {recordProgress && (
        <div className="lesson-block-foot">
          <button type="button" className={`lesson-done ${done ? "is-done" : ""}`} onClick={onDone} disabled={done}>
            <Check size={14} /> {done ? "Đã làm" : "Đánh dấu đã làm"}
          </button>
        </div>
      )}
    </div>
  );
}
