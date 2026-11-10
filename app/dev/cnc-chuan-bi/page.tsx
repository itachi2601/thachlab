"use client";

/**
 * XEM THỬ quiz "Chuẩn bị tối trước" CNC (lớp đảo ngược) — chỉ có nghĩa ở máy dev:
 * http://localhost:3000/dev/cnc-chuan-bi . Câu buổi 2 chép từ scripts/sql/cnc-prep-buoi-2.sql,
 * nộp bằng hàm giả (không ghi DB); bảng giảng viên dùng 6 lượt nộp mẫu.
 */
import { useState } from "react";
import { PrepForm } from "@/components/lessons/CncPrepQuiz";
import { CncPrepSessionResults } from "@/components/dashboard/CncPrepResultsPanel";
import { CNC_PREP_SESSIONS, type CncPrepResponse } from "@/services/cnc-prep";
import type { CncQuizQuestion } from "@/services/cnc-exam-bank";

const QUESTIONS: CncQuizQuestion[] = [
  {
    id: "prep-2-0",
    question: "Chương trình NC tiện ghi tọa độ so với điểm nào?",
    options: ["M, gốc máy", "R, điểm tham chiếu", "W, gốc phôi", "T/N, điểm chuẩn dao"],
    correctIndex: 2,
    explanation:
      "M, R, T/N cố định theo máy. W do người lập trình chọn theo bản vẽ và cách gá; mọi tọa độ trong chương trình tính từ W.",
  },
  {
    id: "prep-2-1",
    question:
      "W đặt ở tâm mặt đầu bên phải của phôi (như các ví dụ trong bài). Một điểm trên trục, nằm về phía mâm cặp và cách mặt đầu 30 mm, có tọa độ Z bằng bao nhiêu?",
    options: ["Z30", "Z-30", "Z0", "Z-60"],
    correctIndex: 1,
    explanation: "Mặt đầu là Z0; phần phôi phía mâm cặp có Z âm, nên cách mặt đầu 30 mm là Z-30.",
  },
  {
    id: "prep-2-2",
    question: "Tên chương trình nào viết đúng quy tắc FANUC 21T dùng ở xưởng?",
    options: ["O1601", "N1601", "P1601", "1601"],
    correctIndex: 0,
    explanation:
      "Tên chương trình là chữ O kèm bốn chữ số, ví dụ O1601. N là số thứ tự khối, không phải tên chương trình.",
  },
  {
    id: "prep-2-3",
    question: "Trong khối N40 G01 X20 Z-15 F0.2; phần F0.2 cho máy biết điều gì?",
    options: ["Tốc độ trục chính", "Lượng chạy dao", "Số dao cần gọi", "Số thứ tự khối"],
    correctIndex: 1,
    explanation:
      "F là lượng chạy dao; S là tốc độ trục chính, T chọn dao, N là số thứ tự khối. Mỗi khối kết thúc bằng dấu ;",
  },
  {
    id: "prep-2-4",
    question: "G90 và G91 khác nhau thế nào?",
    options: [
      "G90 tọa độ tuyệt đối (so với W), G91 tọa độ tương đối (so với điểm trước)",
      "G90 tọa độ tương đối, G91 tọa độ tuyệt đối",
      "G90 chạy nhanh, G91 chạy cắt",
      "G90 đơn vị mm, G91 đơn vị inch",
    ],
    correctIndex: 0,
    explanation: "G90: tọa độ tính từ gốc phôi W. G91: tọa độ tính từ vị trí dao ngay trước đó.",
  },
];

const STUDENTS = [
  { id: "a", name: "Nguyễn Văn An" },
  { id: "b", name: "Trần Thị Bình" },
  { id: "c", name: "Lê Minh Cường" },
  { id: "d", name: "Phạm Thu Dung" },
  { id: "e", name: "Võ Hoàng Em" },
  { id: "f", name: "Đỗ Gia Phúc" },
];
const row = (id: number, sv: string, answers: (number | null)[], chua_ro: string | null = null): CncPrepResponse => {
  const score = answers.filter((a, i) => a === QUESTIONS[i].correctIndex).length;
  return {
    id,
    course_id: 0,
    student_id: sv,
    session_no: 2,
    answers,
    score,
    total: 5,
    chua_ro,
    created_at: `2026-11-08T13:${10 + id}:00Z`,
  };
};
const ROWS: CncPrepResponse[] = [
  row(1, "a", [2, 0, 0, 1, 0], "Em chưa hiểu vì sao W lại đặt ở mặt đầu bên phải mà không ở mâm cặp."),
  row(2, "b", [2, 1, 0, 1, 0]),
  row(3, "c", [0, 0, 1, 0, 0], "G91 thì điểm trước là điểm nào khi mới bắt đầu chương trình?"),
  row(4, "d", [2, 0, 0, 1, 1]),
  row(5, "c", [2, 1, 0, 1, 0]),
];

export default function Page() {
  const [mine, setMine] = useState<CncPrepResponse[]>([]);
  return (
    <main className="cnc-shell lesson-shell lesson-shell--cttc mx-auto max-w-3xl space-y-8 p-4">
      <section className="mb-6 rounded-2xl border border-line bg-panel p-5">
        <h2 className="font-display text-base font-semibold text-ink">Chuẩn bị trước buổi học</h2>
        <p className="mt-1 text-sm text-slate-500">(Xem thử phía sinh viên — nộp không ghi DB.)</p>
        <PrepForm
          courseId={0}
          session={CNC_PREP_SESSIONS[0]}
          questions={QUESTIONS}
          previous={mine}
          onSubmitted={(r) => setMine((m) => [...m, r])}
          submit={async () => {
            await new Promise((ok) => setTimeout(ok, 300));
          }}
        />
      </section>
      <section className="rounded-2xl border border-line bg-panel p-5">
        <h3 className="font-display text-lg font-bold text-ink">
          Chuẩn bị tối trước · Buổi 2 (phía giảng viên, dữ liệu mẫu)
        </h3>
        <CncPrepSessionResults questions={QUESTIONS} rows={ROWS} students={STUDENTS} />
      </section>
    </main>
  );
}
