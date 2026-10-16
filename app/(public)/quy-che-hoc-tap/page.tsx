import type { Metadata } from "next";
import { Suspense } from "react";
import QuyChe from "./QuyChe";

export const metadata: Metadata = {
  title: "Quy chế học tập & cách dùng website",
  description:
    "Học sinh học thế nào trên ThachLab: việc cần làm trước và sau buổi học, cách làm bài kiểm tra, ôn câu sai, phụ đạo, xếp hạng và những điều cần giữ.",
  alternates: { canonical: "/quy-che-hoc-tap" },
};

// Nội dung ở ./content.tsx; bản đọc và bản chiếu lớp (?chieu=1) ở ./QuyChe.tsx. Static export nên đọc query ở client (Suspense bắt buộc).
export default function QuyCheHocTapPage() {
  return (
    <Suspense fallback={null}>
      <QuyChe />
    </Suspense>
  );
}
