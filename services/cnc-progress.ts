import type { CncLearningRecord } from "@/services/cnc-learning-records";

export const CNC_ASSESSMENT_PLAN: Record<string, readonly string[]> = {
  "lesson-1": ["final"],
  "lesson-2": ["exercise-1", "exercise-2", "exercise-3", "exercise-4", "exercise-5"],
  "lesson-3": ["exercise-1", "exercise-2", "exercise-3", "exercise-4", "exercise-5"],
  "lesson-4-turn": ["machine-operation", "tool-setup", "checklist-practice", "checklist"],
  "lesson-4-mill": ["machine-operation", "tool-setup", "checklist-practice", "checklist"],
  "lesson-5": ["final"],
  "lesson-6": ["final"],
};

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
