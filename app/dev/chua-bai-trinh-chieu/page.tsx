"use client";

import { useEffect, useState } from "react";
import ReviewSlides from "@/components/dashboard/ReviewSlides";
import type { ExamReviewData } from "@/services/analytics";
import type { AiExamAnalysis } from "@/services/ai-exam-analysis";

/**
 * XEM THỬ TRÌNH CHIẾU PHÂN TÍCH BÀI LÀM (18/11/2026) — http://localhost:3000/dev/chua-bai-trinh-chieu
 *   (không tham số) → có lời AI cho học sinh · ?ai=0 → chỉ số liệu máy tính (chưa chạy AI / bản AI cũ)
 * Dữ liệu giả, không gọi DB. Phím: ← → chuyển · Space hiện đáp án (slide bẫy) · Enter chữa câu này · T nền tối · F toàn màn · +/- cỡ chữ.
 */
const DATA: ExamReviewData = {
  examTitle: "Kiểm tra 15 phút · Bài 12 Định luật Boyle",
  durationMinutes: 15,
  totalStudents: 32,
  questions: [
    {
      type: "multiple_choice",
      topic: "Định luật Boyle",
      question: "<p>Nén đẳng nhiệt một lượng khí từ thể tích 6 lít xuống 4 lít thì áp suất tăng thêm 0,75 atm. Áp suất ban đầu của khí là</p>",
      options: ["0,75 atm.", "1,0 atm.", "1,5 atm.", "2,25 atm."],
      answer: 2,
      explanation: "",
    },
    {
      type: "true_false",
      topic: "Đồ thị đẳng nhiệt",
      question: "<p>Một lượng khí lí tưởng biến đổi đẳng nhiệt. Xét các phát biểu sau:</p>",
      statements: [
        { text: "Tích $pV$ không đổi.", answer: true },
        { text: "Đường đẳng nhiệt trong hệ $(p, V)$ là đường thẳng đi qua gốc toạ độ.", answer: false },
        { text: "Nhiệt độ càng cao, đường đẳng nhiệt càng xa gốc toạ độ.", answer: true },
        { text: "Khi thể tích giảm một nửa thì áp suất cũng giảm một nửa.", answer: false },
      ],
      explanation: "",
    },
    {
      type: "short_answer",
      topic: "Định luật Boyle",
      question: "<p>Một bọt khí ở đáy hồ sâu 10 m nổi lên mặt nước. Lấy $p_0 = 10^5$ Pa, $\\rho = 1000$ kg/m³, $g = 10$ m/s². Thể tích bọt khí tăng bao nhiêu lần?</p>",
      answer: "2",
      explanation: "",
    },
    {
      type: "multiple_choice",
      topic: "Thuyết động học phân tử",
      question: "<p>Áp suất chất khí lên thành bình là do</p>",
      options: ["các phân tử khí va chạm vào thành bình.", "trọng lượng của khí.", "lực hút giữa các phân tử.", "khí nở ra khi nóng."],
      answer: 0,
      explanation: "",
    },
  ],
  stats: [
    { attempted: 32, correctN: 9, optionCounts: [4, 14, 9, 5] },
    { attempted: 32, correctN: 11, statementCorrectN: [29, 12, 21, 26] },
    { attempted: 32, correctN: 13, wrongAnswers: { "1": 9, "11": 6, "0,5": 2 } },
    { attempted: 32, correctN: 28, optionCounts: [28, 2, 1, 1] },
  ],
};

const AI: AiExamAnalysis = {
  overview: "",
  classMessage:
    "Cả lớp nắm chắc vì sao khí gây áp suất. Chỗ cần cùng xem lại: đọc đúng đại lượng đề cho ($\\Delta p$ chứ không phải $p_2$) và dáng đồ thị đẳng nhiệt.",
  topics: [
    {
      topic: "Định luật Boyle",
      priority: "cao",
      reason: "",
      reviewTip: "",
      studentTip: "Viết $p_1V_1 = p_2V_2$ rồi gạch chân: đề cho $p_2$ hay cho độ tăng $\\Delta p$?",
      questionIndexes: [0, 2],
    },
    {
      topic: "Đồ thị đẳng nhiệt",
      priority: "vua",
      reason: "",
      reviewTip: "",
      studentTip: "Vẽ lại đường hypebol $p = \\dfrac{\\text{hằng số}}{V}$ và so với đường thẳng qua gốc.",
      questionIndexes: [1],
    },
  ],
  questions: [
    {
      index: 0,
      misconception: "",
      teachingTip: "",
      studentWhy: "Đề cho áp suất TĂNG THÊM 0,75 atm, nhiều bạn coi 0,75 atm là $p_2$ rồi giải ra B.",
      studentAvoid: "Gặp chữ “tăng thêm”, “giảm bớt” → viết ngay $p_2 = p_1 + \\Delta p$ trước khi thay số.",
    },
    {
      index: 1,
      misconception: "",
      teachingTip: "",
      studentWhy: "Nhớ “$p$ tỉ lệ nghịch với $V$” nhưng lại vẽ thành đường thẳng — đó là đồ thị $p$ theo $1/V$.",
      studentAvoid: "Hỏi lại: trục ngang là $V$ hay $1/V$?",
    },
    {
      index: 2,
      misconception: "",
      teachingTip: "",
      studentWhy: "Quên cộng áp suất khí quyển: ở đáy hồ $p = p_0 + \\rho g h$, không phải chỉ $\\rho g h$.",
      studentAvoid: "Bọt khí trong chất lỏng luôn chịu cả $p_0$ ở trên mặt.",
    },
  ],
  reviewOrder: [0, 1, 2],
};

export default function ChuaBaiTrinhChieuDev() {
  const [ai, setAi] = useState<AiExamAnalysis | null>(AI);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- trang dev, đọc query sau hydrate
    if (new URLSearchParams(location.search).get("ai") === "0") setAi(null);
  }, []);
  const [msg, setMsg] = useState("");
  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 200 }}>
      <ReviewSlides
        data={DATA}
        ai={ai}
        onJump={(i) => setMsg(`→ mở Câu ${i + 1} trên bảng chữa bài`)}
        onClose={() => setMsg("→ đóng trình chiếu")}
      />
      {msg && (
        <p style={{ position: "fixed", bottom: 4, left: 8, zIndex: 300, fontSize: 12, color: "#64748b" }}>{msg}</p>
      )}
    </div>
  );
}
