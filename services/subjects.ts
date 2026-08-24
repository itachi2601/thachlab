export interface SubjectDefinition {
  code: string;
  label: string;
  joinPrefix: string;
  /** Whether teacher-dashboard curriculum data (lessons, competencies, assessment plan) exists for this subject yet. */
  hasCurriculum: boolean;
  /** Workshop code (`machines.workshop`) whose machines this subject's attendance/máy picker uses. */
  workshop: string;
}

export const SUBJECTS: SubjectDefinition[] = [
  { code: "cnc", label: "Gia công CNC", joinPrefix: "CNC", hasCurriculum: true, workshop: "C1.2" },
  { code: "tien-phay", label: "Tiện – Phay truyền thống", joinPrefix: "TP", hasCurriculum: false, workshop: "C1.1" },
];

export function getSubject(code: string): SubjectDefinition {
  return SUBJECTS.find((item) => item.code === code) ?? SUBJECTS[0];
}
