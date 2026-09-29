"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import ExamLibraryAdmin from "@/components/admin/ExamLibraryAdmin";

// Đọc ?exam=&q= — link từ mục "Báo lỗi & góp ý" (báo lỗi một câu cụ thể) nhảy
// thẳng vào đây, tự mở đúng đề và tô đậm đúng câu thay vì để admin tự tìm.
function PageBody() {
  const searchParams = useSearchParams();
  const examParam = Number(searchParams.get("exam"));
  const qParam = searchParams.get("q");
  return (
    <ExamLibraryAdmin
      initialExamId={Number.isFinite(examParam) && examParam > 0 ? examParam : null}
      initialQuestionIndex={qParam != null && qParam !== "" ? Number(qParam) : null}
    />
  );
}

export default function Page() {
  return (
    <Suspense fallback={null}>
      <PageBody />
    </Suspense>
  );
}
