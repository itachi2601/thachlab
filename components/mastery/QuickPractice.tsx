"use client";

import { useEffect, useState, type ComponentProps } from "react";
import dynamic from "next/dynamic";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";
import { fetchLessonsStatic } from "@/services/static-content";

// Modal luyện: cùng chunk lazy với thẻ mastery ở trang bài (perf4) — chỉ tải khi bấm, có boundary.
const PracticeModalLazy = dynamic(() => import("@/components/mastery/TopicPracticeModal"), {
  ssr: false,
  loading: () => null,
});

function PracticeModal(props: ComponentProps<typeof PracticeModalLazy>) {
  return (
    <LazyErrorBoundary
      fallback={
        <div role="alertdialog" className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="max-w-sm rounded-2xl border border-white/10 bg-panel p-5 text-center text-sm text-slate-300">
            <p>Không tải được phần luyện tập (có thể do mạng chập chờn). Thử tải lại trang.</p>
            <button
              type="button"
              onClick={props.onClose}
              className="mt-3 min-h-11 rounded-full border border-white/15 px-4 text-xs font-semibold text-white hover:border-white/30"
            >
              Đóng
            </button>
          </div>
        </div>
      }
    >
      <PracticeModalLazy {...props} />
    </LazyErrorBoundary>
  );
}

export interface QuickPracticeRequest {
  lessonId: number;
  topicName: string;
}

/**
 * "Luyện nhanh 10 câu" cho một kỹ năng yếu (M2, GĐ 2.6): lấy các đề của bài từ danh mục tĩnh (không thêm lượt gọi
 * Supabase), mở modal luyện từng câu một, ghi phiên luyện như mọi lượt luyện (D2, N1).
 * Bài không có đề → gọi onUnavailable để nơi gọi đưa em vào thẳng bài (đường lui).
 */
export default function QuickPractice({
  request,
  onClose,
  onFinished,
  onUnavailable,
}: {
  request: QuickPracticeRequest | null;
  onClose: () => void;
  onFinished?: () => void;
  onUnavailable: (request: QuickPracticeRequest) => void;
}) {
  const [run, setRun] = useState<{ lessonId: number; examIds: number[]; topicName: string } | null>(null);

  useEffect(() => {
    if (!request) return;
    let cancelled = false;
    fetchLessonsStatic()
      .then((lessons) => {
        if (cancelled) return;
        const lesson = lessons.find((l) => l.id === request.lessonId);
        const examIds = lesson ? Array.from(new Set(lesson.itemRefs.flatMap((r) => r.exam_ids))) : [];
        if (examIds.length === 0) {
          onUnavailable(request);
          return;
        }
        setRun({ lessonId: request.lessonId, examIds, topicName: request.topicName });
      })
      .catch(() => {
        if (!cancelled) onUnavailable(request);
      });
    return () => {
      cancelled = true;
    };
    // onUnavailable đổi mỗi lần render ở nơi gọi; chỉ phản ứng khi mở yêu cầu mới.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [request]);

  if (!request || !run || run.lessonId !== request.lessonId) return null;
  return (
    <PracticeModal
      lessonId={run.lessonId}
      examIds={run.examIds}
      topicName={run.topicName}
      count={10}
      onClose={() => {
        setRun(null);
        onClose();
      }}
      onFinished={onFinished}
    />
  );
}
