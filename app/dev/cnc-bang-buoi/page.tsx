"use client";

/**
 * XEM THỬ bảng điều hành giảng viên CNC theo nhịp lớp đảo ngược (tab "Buổi học" của /dashboard) —
 * chỉ có nghĩa ở máy dev: http://localhost:3000/dev/cnc-bang-buoi . Dữ liệu mẫu 30 sinh viên, không đọc/ghi DB.
 */
import { useMemo, useState } from "react";
import { FlipBoardView } from "@/components/dashboard/TeacherFlipBoard";
import type { CncQuizQuestion } from "@/services/cnc-exam-bank";
import type { CompetencyPermission } from "@/services/cnc-competencies";
import { buildFlipBoard, type FlipStudent } from "@/services/cnc-flip";
import type { CncLearningRecord } from "@/services/cnc-learning-records";
import type { CncPrepResponse } from "@/services/cnc-prep";
import { CNC_ASSESSMENT_PLAN } from "@/services/cnc-progress";

const HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Võ", "Đỗ", "Huỳnh", "Bùi", "Đặng", "Phan"];
const TEN = ["An", "Bình", "Cường", "Dung", "Em", "Phúc", "Giang", "Hải", "Khoa", "Lâm", "Minh", "Nam", "Oanh", "Phát", "Quân"];
const QUESTIONS: CncQuizQuestion[] = [
  { id: "q0", question: "Đặt gốc phôi W trên máy tiện bằng cách nào?", options: ["Chạm dao vào mặt đầu rồi nhập Z0", "Về điểm tham chiếu R", "Bấm RESET", "Gọi dao T0101"], correctIndex: 0, explanation: "" },
  { id: "q1", question: "Bảng offset dao lưu giá trị nào?", options: ["Tốc độ trục chính", "Sai lệch X, Z của mũi dao", "Lượng chạy dao", "Số khối lệnh"], correctIndex: 1, explanation: "" },
  { id: "q2", question: "Trước khi chạy tự động chương trình mới phải làm gì?", options: ["Tăng F lên 120%", "Mở cửa che", "Chạy từng khối (SBL) và giảm tốc độ chạy nhanh", "Tắt dung dịch trơn nguội"], correctIndex: 2, explanation: "" },
  { id: "q3", question: "Đo dao xong, đường kính thực lớn hơn 0,1 mm so với bản vẽ. Sửa ở đâu?", options: ["Sửa chương trình", "Sửa ô mòn dao (wear) trục X", "Đổi dao khác", "Đặt lại W"], correctIndex: 1, explanation: "" },
  { id: "q4", question: "Nút nào dừng mọi chuyển động ngay lập tức?", options: ["FEED HOLD", "RESET", "Dừng khẩn cấp", "SBL"], correctIndex: 2, explanation: "" },
];

const CURRENT = 6; // lớp mẫu đang ở buổi 6
const OPEN = ["lesson-1", "lesson-2", "lesson-3", "lesson-4-turn"];

function mock() {
  const students: FlipStudent[] = [];
  const permissions: CompetencyPermission[] = [];
  const prepRows: CncPrepResponse[] = [];
  let rowId = 0;
  for (let i = 0; i < 30; i++) {
    const id = `sv-${i}`;
    // Mức chăm: 0 = bỏ nhiều, 1 = lơ mơ, 2–3 = đều.
    const level = i % 10 === 7 ? 0 : i % 4 === 1 ? 1 : 2;
    const records: CncLearningRecord[] = [];
    const pass = (lessonId: string, keep: (assessmentId: string, index: number) => boolean) =>
      CNC_ASSESSMENT_PLAN[lessonId].forEach((assessmentId, index) => {
        if (keep(assessmentId, index))
          records.push({ course_id: 0, student_id: id, lesson_id: lessonId, assessment_id: assessmentId, completed: true, latest_score: 18, best_score: 18, total_questions: 20, attempt_count: 1, last_activity_at: "2026-11-09T12:00:00Z" });
      });
    pass("lesson-1", () => level > 0 || i % 2 === 0);
    pass("lesson-2", (_, index) => level === 2 || (level === 1 && index < 4));
    pass("lesson-3", (_, index) => (level === 2 && i % 5 !== 0) || (level === 1 && index < 2));
    pass("lesson-4-turn", (assessmentId) => level === 2 && i % 3 !== 0 && assessmentId !== "checklist");
    if (level === 2 && i % 6 === 2)
      (["turn-operation", "turn-tool-setup"] as const).forEach((competency_id) =>
        permissions.push({ course_id: 0, student_id: id, competency_id, status: "approved", note: "", approved_at: null, updated_at: "", approved_by: null }),
      );
    for (let no = 2; no <= CURRENT; no++) {
      if (level === 0 && no !== 2) continue;
      if (level === 1 && (no + i) % 3 === 0) continue;
      if (no === CURRENT && i % 5 === 4) continue;
      const answers = QUESTIONS.map((q, qi) => (level === 2 && (i + qi + no) % 7 !== 0 ? q.correctIndex : (q.correctIndex + 1 + ((i + qi) % 2)) % 4));
      const score = answers.filter((a, qi) => a === QUESTIONS[qi].correctIndex).length;
      prepRows.push({
        id: rowId++, course_id: 0, student_id: id, session_no: no, answers, score, total: 5,
        chua_ro: no === CURRENT && i % 9 === 3 ? "Em chưa rõ khi nào sửa ô mòn dao, khi nào sửa hình học dao." : null,
        created_at: `2026-11-09T13:${String(10 + i).padStart(2, "0")}:00Z`,
      });
    }
    students.push({ id, name: `${HO[i % HO.length]} ${TEN[i % TEN.length]}`, records });
  }
  const banks: Record<number, CncQuizQuestion[]> = {};
  for (let no = 2; no <= 8; no++) banks[no] = QUESTIONS;
  return { students, permissions, prepRows, banks };
}

export default function Page() {
  const data = useMemo(() => mock(), []);
  const [sessionNo, setSessionNo] = useState(CURRENT);
  const [openLessons, setOpenLessons] = useState(OPEN);
  const [log, setLog] = useState("");
  const board = useMemo(() => buildFlipBoard({ ...data, openLessons, sessionNo }), [data, openLessons, sessionNo]);
  return (
    <main className="teacher-dashboard mx-auto min-h-screen w-full max-w-6xl space-y-4 px-4 py-6 lg:px-8">
      <p className="text-xs text-muted">Xem thử tab “Buổi học” của giảng viên CNC · dữ liệu mẫu{log && ` · ${log}`}</p>
      <FlipBoardView
        board={board}
        students={data.students}
        taughtCount={CURRENT - 1}
        today={{ present: 26, late: 2, absent: 2, open: true }}
        openLessons={openLessons}
        releaseBusy={false}
        releaseError=""
        loading={false}
        onPickSession={setSessionNo}
        onToggleLesson={(id) => setOpenLessons((cur) => (cur.includes(id) ? cur.filter((x) => x !== id) : [...cur, id]))}
        onReload={() => setLog("đã bấm Tải lại")}
        onOpenTab={(tab) => setLog(`mở tab ${tab}`)}
        onOpenStudent={(id) => setLog(`mở hồ sơ ${id}`)}
        onOpenLiveExam={() => setLog("mở phòng thi")}
      />
    </main>
  );
}
