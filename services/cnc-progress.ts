import type { CncLearningRecord } from "@/services/cnc-learning-records";

export const CNC_ASSESSMENT_PLAN: Record<string, readonly string[]> = {
  "lesson-1": ["final"],
  "lesson-2": ["exercise-1", "exercise-2", "exercise-3-short", "exercise-3", "exercise-4", "exercise-5"],
  "lesson-3": ["exercise-1", "exercise-2", "exercise-3-short", "exercise-3", "exercise-4", "exercise-5"],
  "lesson-4-turn": ["machine-operation", "tool-setup", "checklist-practice", "checklist"],
  "lesson-4-mill": ["machine-operation", "tool-setup", "checklist-practice", "checklist"],
  "lesson-5": ["checklist-practice", "checklist", "rubric-exam"],
  "lesson-6": ["checklist-practice", "checklist", "rubric-exam"],
};

// Khuôn bài chung với các môn khác (docs/CNC-CAU-TRUC-BAI-THEO-MON-KHAC-2026-11-08.md, chặng A):
// bài nhóm theo chương, khoá đánh giá giữ nguyên, chỉ đổi tab hiển thị (Luyện tập / BTVN / Kiểm tra).
export const CNC_CHAPTERS = [
  { title: "I. Nhập môn CNC", lessonIds: ["lesson-1"] },
  { title: "II. Lập trình", lessonIds: ["lesson-2", "lesson-3"] },
  { title: "III. Vận hành máy", lessonIds: ["lesson-4-turn", "lesson-4-mill"] },
  { title: "IV. Gia công", lessonIds: ["lesson-5", "lesson-6"] },
] as const;

export const CNC_LESSON_COUNT = Object.keys(CNC_ASSESSMENT_PLAN).length;

export type CncSectionKind = "luyen_tap" | "bai_tap_ve_nha" | "kiem_tra";

export const CNC_ASSESSMENT_SECTION: Record<string, CncSectionKind> = {
  "exercise-1": "luyen_tap",
  "exercise-2": "luyen_tap",
  "exercise-3-short": "luyen_tap",
  "machine-operation": "luyen_tap",
  "tool-setup": "luyen_tap",
  "checklist-practice": "luyen_tap",
  "exercise-3": "bai_tap_ve_nha",
  "exercise-4": "bai_tap_ve_nha",
  "exercise-5": "bai_tap_ve_nha",
  final: "kiem_tra",
  checklist: "kiem_tra",
  "rubric-exam": "kiem_tra",
};

export function cncLessonSections(lessonId: string): CncSectionKind[] {
  const kinds = new Set((CNC_ASSESSMENT_PLAN[lessonId] ?? []).map((id) => CNC_ASSESSMENT_SECTION[id]));
  return (["luyen_tap", "bai_tap_ve_nha", "kiem_tra"] as const).filter((kind) => kinds.has(kind));
}

export function cncChapterOf(lessonId: string) {
  return CNC_CHAPTERS.find((chapter) => (chapter.lessonIds as readonly string[]).includes(lessonId)) ?? null;
}

export const CNC_TOTAL_ASSESSMENTS = Object.values(CNC_ASSESSMENT_PLAN).reduce((sum, items) => sum + items.length, 0);

export function passedAssessmentKeys(records: CncLearningRecord[]) {
  return new Set(records.filter((record) => record.completed && CNC_ASSESSMENT_PLAN[record.lesson_id]?.includes(record.assessment_id)).map((record) => `${record.lesson_id}:${record.assessment_id}`));
}

export function completedCncLessons(records: CncLearningRecord[]) {
  const passed = passedAssessmentKeys(records);
  return new Set(Object.entries(CNC_ASSESSMENT_PLAN).filter(([lessonId, assessments]) => assessments.every((assessmentId) => passed.has(`${lessonId}:${assessmentId}`))).map(([lessonId]) => lessonId));
}

export function cncAssessmentProgress(records: CncLearningRecord[]) {
  const passed = passedAssessmentKeys(records).size;
  return { passed, total: CNC_TOTAL_ASSESSMENTS, pct: Math.round((passed / CNC_TOTAL_ASSESSMENTS) * 100) };
}
