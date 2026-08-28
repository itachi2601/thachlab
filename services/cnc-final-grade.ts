import type { RubricExamAttempt } from "@/services/cnc-rubric-exam";
import type { AttendanceRecord } from "@/services/course-attendance";
import type { CourseGradeOverride } from "@/services/course-grade-overrides";

/** Công thức chính thức: Thi Tiện GV 45% + Thi Phay GV 45% + Chuyên cần 10% + cộng/trừ,
 * giới hạn 0–10. Dùng chung giữa bảng điểm trên dashboard và file xuất cuối kỳ — không
 * lặp lại công thức ở 2 nơi để tránh lệch điểm. */
export interface CncFinalGrade {
  turnSelf: number | null;
  turnTeacher: number | null;
  millSelf: number | null;
  millTeacher: number | null;
  attendanceScore: number;
  bonus: number;
  total: number;
}

function rubricScore(attempts: RubricExamAttempt[], studentId: string, machine: "tien" | "phay", role: "self" | "teacher") {
  return attempts.find((attempt) => attempt.student_id === studentId && attempt.machine === machine && attempt.role === role)?.total_score ?? null;
}

export function computeCncFinalGrade(
  studentId: string,
  attempts: RubricExamAttempt[],
  attendanceRecords: AttendanceRecord[],
  sessionCount: number,
  overrides: CourseGradeOverride[],
): CncFinalGrade {
  const override = (key: string, fallback: number | null) => overrides.find((item) => item.student_id === studentId && item.grade_key === key)?.score ?? fallback;
  const turnSelf = override("rubric:tien:self", rubricScore(attempts, studentId, "tien", "self"));
  const turnTeacher = override("rubric:tien:teacher", rubricScore(attempts, studentId, "tien", "teacher"));
  const millSelf = override("rubric:phay:self", rubricScore(attempts, studentId, "phay", "self"));
  const millTeacher = override("rubric:phay:teacher", rubricScore(attempts, studentId, "phay", "teacher"));
  const ownAttendance = attendanceRecords.filter((record) => record.student_id === studentId);
  const attended = ownAttendance.filter((record) => record.status === "present" || record.status === "late").length;
  const attendanceScore = override("attendance", sessionCount ? (10 * attended) / sessionCount : 0) ?? 0;
  const sourceBonus = ownAttendance.reduce((sum, record) => sum + record.bonus_points, 0);
  const bonus = override("bonus", sourceBonus) ?? 0;
  const total = Math.min(10, Math.max(0, (turnTeacher ?? 0) * 0.45 + (millTeacher ?? 0) * 0.45 + attendanceScore * 0.1 + bonus));
  return { turnSelf, turnTeacher, millSelf, millTeacher, attendanceScore, bonus, total };
}
