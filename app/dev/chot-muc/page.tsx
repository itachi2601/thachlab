"use client";

import { useEffect, useState } from "react";
import { TheoryBlock } from "@/app/lop-hoc/bai/_parts/TheoryBlock";
import type { LessonItem } from "@/features/lessons/types";

/**
 * XEM THỬ "mỗi lần Tiếp một mục con + ô 📌 Chốt mục" (thử 25/11/2026) đi qua đúng TheoryBlock của trang học sinh,
 * vì bài thật cần đăng nhập. Mở http://localhost:3000/dev/chot-muc (bài Boyle–Charles L12, lấy từ bundle.json).
 * Không ghi RP/độ sâu đọc (recordProgress=false); chỉ có nghĩa ở máy dev.
 */
export default function ChotMucPreviewPage() {
  const [item, setItem] = useState<LessonItem | null>(null);
  useEffect(() => {
    import("@/content/lesson-samples/l12-boyle-charles/bundle.json").then((m) =>
      setItem({ id: 999007, title: "Lý thuyết", body_html: m.default.theory_html } as unknown as LessonItem),
    );
  }, []);
  return (
    <main className="lesson-shell lesson-page">
      {item ? (
        <TheoryBlock
          item={item}
          defaultOpen
          hideTitle
          done={false}
          loggedIn={false}
          onDone={() => {}}
          recordProgress={false}
        />
      ) : (
        <p>Đang tải…</p>
      )}
    </main>
  );
}
