"use client";

import { useEffect, useState } from "react";
import WorkedQuestionsGrid from "@/components/lessons/WorkedQuestionsGrid";
import type { LessonWorkedQuestion } from "@/features/lessons/types";
import { getSupabase } from "@/services/supabase";

/**
 * Xem thử UI "Bài tập mẫu" từ file JSON cục bộ TRƯỚC khi đăng lên DB (skill soan-bai-tap-mau).
 *   npx tsx scripts/publish-bai-tap-mau.mts --lesson 57 --xem-thu   → ghi public/xem-thu/btm.json (gitignore)
 *   rồi mở http://localhost:3000/dev/btm
 * Không có dữ liệu thật của học sinh; trang chỉ có ý nghĩa ở máy dev.
 */
export default function BtmPreviewPage() {
  const [data, setData] = useState<{ lesson_id: number; lesson_title?: string; questions: LessonWorkedQuestion[] } | null>(null);
  const [err, setErr] = useState<string | null>(null);
  useEffect(() => {
    // ?mock=1: giả RPC bài tương tự (không cần đăng nhập) để xem luồng chấm + gỡ rối
    if (new URLSearchParams(location.search).has("mock")) {
      const sb = getSupabase() as unknown as { rpc: (fn: string, args?: unknown) => unknown };
      const orig = sb.rpc.bind(sb);
      sb.rpc = (fn, args) =>
        fn === "get_similar_bank_questions"
          ? Promise.resolve({
              data: [1, 2, 3].map((id) => ({
                id,
                same_form: true,
                question: { type: "multiple_choice", question: `Câu giả ${id}: $t=\\sqrt{2h/g}$ với $h=20$ m, $g=10$ m/s² bằng?`, options: ["1 s", "2 s", "3 s", "4 s"], answer: 1, explanation: "t = 2 s" },
              })),
              error: null,
            })
          : orig(fn, args);
    }
    fetch("/xem-thu/btm.json", { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then(setData)
      .catch((e: Error) => setErr(e.message));
  }, []);
  return (
    <main className="lesson-shell lesson-page mx-auto max-w-3xl px-4 py-6">
      <h1 className="mb-1 text-lg font-bold text-white">Xem thử bài tập mẫu {data ? `· bài ${data.lesson_id}` : ""}</h1>
      <p className="mb-4 text-sm text-slate-400">{data?.lesson_title ?? ""}</p>
      {err && <p className="text-sm text-rose-300">Chưa có public/xem-thu/btm.json ({err}) — chạy publish-bai-tap-mau.mts --xem-thu.</p>}
      {data && <WorkedQuestionsGrid questions={data.questions} />}
    </main>
  );
}
