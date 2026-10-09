export const ACADEMIC_SUBJECTS = [
  { code: "vat-ly", label: "Vật lý", icon: "⚡" },
  { code: "hoa-hoc", label: "Hóa học", icon: "🧪" },
  { code: "sinh-hoc", label: "Sinh học", icon: "🧬" },
  { code: "hsg-vat-ly", label: "Vật lí HSG & chuyên", icon: "🏆" },
] as const;

export type AcademicSubjectCode = (typeof ACADEMIC_SUBJECTS)[number]["code"];

// Khoá HSG & chuyên có lối vào riêng (thẻ ở /lop-hoc + menu trên cùng) nên không nằm trong hàng tab môn của KHTN 9.
export const HSG_SUBJECT_CODE = "hsg-vat-ly";
export const HSG_HREF = `/lop-hoc/khtn-9?subject=${HSG_SUBJECT_CODE}`;

export function subjectsForGrade(grade: string) {
  void grade; // điểm mở rộng để giới hạn môn theo khối khi có cấu hình riêng
  return ACADEMIC_SUBJECTS.filter((subject) => subject.code !== HSG_SUBJECT_CODE);
}

export function academicSubject(code: string | null | undefined) {
  return ACADEMIC_SUBJECTS.find((subject) => subject.code === code) ?? ACADEMIC_SUBJECTS[0];
}
