export interface SubjectDefinition {
  code: string;
  label: string;
  joinPrefix: string;
  /** Whether teacher-dashboard curriculum data (lessons, competencies, assessment plan) exists for this subject yet. */
  hasCurriculum: boolean;
}

export const SUBJECTS: SubjectDefinition[] = [
  { code: "cnc", label: "Gia công CNC", joinPrefix: "CNC", hasCurriculum: true },
  { code: "tien-phay", label: "Tiện – Phay truyền thống", joinPrefix: "TP", hasCurriculum: false },
];

export function getSubject(code: string): SubjectDefinition {
  return SUBJECTS.find((item) => item.code === code) ?? SUBJECTS[0];
}
