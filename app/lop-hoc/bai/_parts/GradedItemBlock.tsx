"use client";

import type { GradedStatusResult } from "@/features/progress/types";
import type { LessonItem } from "@/features/lessons/types";
import type { LessonExamMeta } from "@/services/lessons";
import { ExamRow } from "./ExamRow";
import { formatDue } from "./LessonBits";

/** Mục có chấm điểm (BTVN / kiểm tra): tiêu đề, hạn nộp và một dòng cho mỗi đề đang hiện. */
export function GradedItemBlock({
  item,
  plain,
  examIds,
  graded,
  examMetas,
  scores,
  loggedIn,
  metaStatus,
  teacherView,
}: {
  item: LessonItem;
  /** Mục duy nhất của phần → ẩn tiêu đề riêng (trùng tiêu đề phần ngay trên). */
  plain: boolean;
  /** Mã đề đã bỏ đề ẩn (visibleExamIds). */
  examIds: number[];
  graded: GradedStatusResult | undefined;
  examMetas: Map<number, LessonExamMeta>;
  scores: Map<number, number>;
  loggedIn: boolean;
  metaStatus: "loading" | "error" | "ready";
  teacherView: boolean;
}) {
  return (
    <div id={`lesson-item-${item.id}`} className="lesson-block" data-item={item.id}>
      {(!plain || item.due_at) && (
        <div className="lesson-block-head">
          {!plain && <p className="lesson-block-title">{item.title}</p>}
          {item.due_at && <p className="lesson-block-sub">Hạn nộp: {formatDue(item.due_at)}</p>}
        </div>
      )}
      {examIds.length === 0 ? (
        <p className="lesson-muted">Chưa gắn đề</p>
      ) : (
        <div className="lesson-stack">
          {examIds.map((examId) => (
            <ExamRow
              key={examId}
              examId={examId}
              itemId={item.id}
              exam={examMetas.get(examId)}
              score={scores.get(examId)}
              loggedIn={loggedIn}
              metaStatus={metaStatus}
              statusLabel={graded?.label}
              passed={graded ? graded.status === "passed" : undefined}
              teacherView={teacherView}
              showQr={item.kind === "kiem_tra"}
            />
          ))}
        </div>
      )}
    </div>
  );
}
