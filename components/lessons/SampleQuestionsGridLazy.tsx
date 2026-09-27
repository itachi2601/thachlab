"use client";

import dynamic from "next/dynamic";
import type { ComponentProps } from "react";
import { LazyErrorBoundary } from "@/components/ui/LazyErrorBoundary";

/**
 * Bản tải-chậm của SampleQuestionsGrid (mục "Bài tập mẫu") — kéo theo
 * QuestionCard.tsx, chunk riêng lớn nhất còn lại của `/lop-hoc/bai` (đợt tối
 * ưu tốc độ lần 4, perf4/RESULT.md §7 việc #1). Từ 27/9/2026 trang bài học đã
 * đổi thành danh sách 6 mục thu gọn — mục "Bài tập mẫu" chỉ MOUNT khi học sinh
 * bấm mở (xem app/lop-hoc/bai/page.tsx `{isOpen && (...)}` và
 * InlineLessonAccordion.tsx `{open && (...)}`, không phải ẩn bằng CSS) nên
 * tách JS ra khỏi bundle ban đầu của trang không đổi trải nghiệm chính, chỉ
 * chớp loading rất ngắn lần đầu mở mục.
 *
 * `loading`/fallback dùng ĐÚNG nguyên văn 2 dòng chữ mà SampleQuestionsGrid tự
 * có sẵn cho trạng thái tải dữ liệu/lỗi của chính nó (`Đang tải bài tập
 * mẫu…` / `Không tải được bài tập mẫu. Thử tải lại trang.`) — chunk chưa về
 * trông giống hệt lúc chunk đã về nhưng dữ liệu Supabase chưa tải xong, không
 * có skeleton lạ gây nhảy layout.
 */
const SampleQuestionsGridLazyInner = dynamic(() => import("@/components/lessons/SampleQuestionsGrid"), {
  ssr: false,
  loading: () => <p className="text-sm text-slate-400">Đang tải bài tập mẫu…</p>,
});

// LazyErrorBoundary: "Bài tập mẫu" là 1 mục trong danh sách 6 mục của bài học, không phải luồng
// nộp bài/chấm điểm — nếu chunk lỗi (mạng chập chờn, vừa deploy bản mới), chỉ đúng mục này báo lỗi
// bằng đúng dòng chữ SampleQuestionsGrid vẫn dùng cho lỗi tải dữ liệu, không kéo sập cả trang bài
// học đang xem dở (không có app/error.tsx bọc route này).
function SampleQuestionsGridLazy(props: ComponentProps<typeof SampleQuestionsGridLazyInner>) {
  return (
    <LazyErrorBoundary
      fallback={<p className="text-sm text-slate-400">Không tải được bài tập mẫu. Thử tải lại trang.</p>}
    >
      <SampleQuestionsGridLazyInner {...props} />
    </LazyErrorBoundary>
  );
}

export default SampleQuestionsGridLazy;
