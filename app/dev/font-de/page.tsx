"use client";

import { useState } from "react";
import ContentHtml from "@/components/exams/ContentHtml";
import QuestionCard from "@/components/exams/QuestionCard";
import type { ExamQuestion, QuestionResponse } from "@/features/exams/types";

/** XEM THỬ FONT ĐỀ (E4) — http://localhost:3000/dev/font-de. Trang chỉ có nghĩa ở máy dev.
 *  Cùng một QuestionCard mà ExamRunner, luyện tập, thăng hạng, phụ đạo đều dùng. */
const QS: ExamQuestion[] = [
  { type: "multiple_choice", question: "<p>Một vật dao động điều hòa với phương trình $x = 5\\cos(4\\pi t)$ (cm). Chu kì dao động của vật là</p>",
    options: ["<p>0,5 s.</p>", "<p>2 s.</p>", "<p>4 s.</p>", "<p>5 s.</p>"], answer: 0, explanation: "" },
  { type: "true_false", question: "<p>Khi nhiệt độ của một khối khí lí tưởng xác định tăng, các phát biểu sau đúng hay sai?</p>",
    statements: [{ text: "<p>Động năng trung bình của phân tử tăng.</p>", answer: true }, { text: "<p>Áp suất luôn giảm.</p>", answer: false },
      { text: "<p>Thể tích luôn tăng.</p>", answer: false }, { text: "<p>Nội năng của khí tăng.</p>", answer: true }], explanation: "" },
  { type: "short_answer", question: "<p>Một điện trở $R = 20\\,\\Omega$ có cường độ dòng điện 0,5 A. Hiệu điện thế (V) là bao nhiêu?</p>", answer: "10", explanation: "" },
];

export default function Page() {
  const [res, setRes] = useState<QuestionResponse[]>([null, [null, null, null, null], ""]);
  return (
    <main className="mx-auto max-w-2xl space-y-4 p-4">
      <p className="text-sm text-muted">Chữ câu hỏi phải là serif (Times New Roman); thanh này là Inter.</p>
      {QS.map((q, i) => (
        <QuestionCard key={i} index={i + 1} question={q} response={res[i]} onChange={(r) => setRes((a) => a.map((x, j) => (j === i ? r : x)))} />
      ))}
      <div className="rounded-2xl border border-line bg-panel p-5 text-[16px]">
        <p className="mb-2 text-sm text-muted">Bài lý thuyết: hộp Đề bài = serif, phần còn lại = Inter.</p>
        <ContentHtml html={'<div class="tl-box tl-box--rule"><p class="tl-label">📝 Đề bài</p><p>Một điện trở $R = 20\\,\\Omega$ có cường độ dòng điện 0,5 A. Tính hiệu điện thế giữa hai đầu điện trở.</p></div><p>Lời giải: áp dụng $U = IR$ nên $U = 10$ V.</p>'} />
      </div>
    </main>
  );
}
