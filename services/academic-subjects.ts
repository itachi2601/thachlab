export const ACADEMIC_SUBJECTS = [
  { code: "vat-ly", label: "Vật lý", icon: "⚡" },
  { code: "hoa-hoc", label: "Hóa học", icon: "🧪" },
  { code: "sinh-hoc", label: "Sinh học", icon: "🧬" },
] as const;

export type AcademicSubjectCode = (typeof ACADEMIC_SUBJECTS)[number]["code"];

export function subjectsForGrade(grade: string) {
  void grade; // điểm mở rộng để giới hạn môn theo khối khi có cấu hình riêng
  return ACADEMIC_SUBJECTS;
}

export function academicSubject(code: string | null | undefined) {
  return ACADEMIC_SUBJECTS.find((subject) => subject.code === code) ?? ACADEMIC_SUBJECTS[0];
}
