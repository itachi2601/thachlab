export interface SubjectDefinition {
  code: string;
  label: string;
  joinPrefix: string;
  /** Whether teacher-dashboard curriculum data (lessons, competencies, assessment plan) exists for this subject yet. */
  hasCurriculum: boolean;
  /** Workshop code (`machines.workshop`) whose machines this subject's attendance/máy picker uses. */
  workshop: string;
  /** Môn thực tập/thực hành xưởng — chỉ các môn này mới xuất hiện trong dashboard của giảng viên được phân công. */
  isPracticum: boolean;
}

export const SUBJECTS: SubjectDefinition[] = [
  { code: "cnc", label: "Gia công CNC", joinPrefix: "CNC", hasCurriculum: true, workshop: "C1.2", isPracticum: true },
  { code: "tien-phay", label: "Tiện – Phay truyền thống", joinPrefix: "TP", hasCurriculum: false, workshop: "C1.1", isPracticum: true },
  { code: "avcn", label: "Anh văn chuyên ngành", joinPrefix: "AVCN", hasCurriculum: false, workshop: "", isPracticum: false },
  { code: "khac", label: "Môn khác (lý thuyết)", joinPrefix: "LOP", hasCurriculum: false, workshop: "", isPracticum: false },
  { code: "gddd-ptnn", label: "Giáo dục đạo đức & phát triển nghề nghiệp", joinPrefix: "GDDD", hasCurriculum: false, workshop: "", isPracticum: false },
];

/** Môn của giáo viên chủ nhiệm — có trang "Lớp chủ nhiệm" riêng (điểm danh + bảng điểm + hạnh kiểm). */
export const HOMEROOM_SUBJECT_CODE = "gddd-ptnn";

export function getSubject(code: string): SubjectDefinition {
  return SUBJECTS.find((item) => item.code === code) ?? SUBJECTS[0];
}

/** Trang học tập của từng môn CTTC (nút "Học tiếp" ở trang chủ, hub CTTC). Môn chưa có trang riêng → /tai-khoan. */
export function learningHrefOf(subjectCode: string): string {
  if (subjectCode === "cnc") return "/lop-hoc/cnc";
  if (subjectCode === "tien-phay") return "/lop-hoc/tien-phay";
  if (subjectCode === "avcn") return "/lop-hoc/avcn";
  return "/tai-khoan";
}
