import type { CncLearningRecord } from "@/services/cnc-learning-records";

export const CNC_ASSESSMENT_PLAN: Record<string, readonly string[]> = {
  "lesson-1": ["final"],
  "lesson-2": ["exercise-1", "exercise-2", "exercise-3-short", "exercise-3", "exercise-4", "exercise-5", "final"],
  "lesson-3": ["exercise-1", "exercise-2", "exercise-3-short", "exercise-3", "exercise-4", "exercise-5", "final"],
  "lesson-4-turn": ["machine-operation", "tool-setup", "checklist-practice", "final", "checklist"],
  "lesson-4-mill": ["machine-operation", "tool-setup", "checklist-practice", "final", "checklist"],
  "lesson-5": ["checklist-practice", "final", "checklist", "rubric-exam"],
  "lesson-6": ["checklist-practice", "final", "checklist", "rubric-exam"],
};

// Đề kiểm tra trắc nghiệm cuối bài (assessment "final", tab Kiểm tra) — ngân hàng exams.cnc_key (thêm 9/11/2026).
export const CNC_FINAL_TEST_BANK: Record<string, string> = {
  "lesson-1": "lesson-1",
  "lesson-2": "test-2",
  "lesson-3": "test-3",
  "lesson-4-turn": "test-4-turn",
  "lesson-4-mill": "test-4-mill",
  "lesson-5": "test-5",
  "lesson-6": "test-6",
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

// Năm cổng năng lực G1–G5 (docs/CNC-FLIPPED-THIET-KE-LAI-2026-11-08.md mục 4.2): chỉ ĐỌC lại khoá đánh giá
// sẵn có trong CNC_ASSESSMENT_PLAN + quyền năng lực giảng viên duyệt; không thêm khoá, không đổi điều kiện mở bài.
// Quiz chuẩn bị (flip-N/prep-N) không thuộc cổng nào.
export type CncGateId = "G1" | "G2" | "G3" | "G4" | "G5";
export type CncGateApproval = "turn-operation" | "turn-tool-setup" | "mill-operation" | "mill-tool-setup";
export type CncGate = { id: CncGateId; title: string; keys: readonly string[]; approvals: readonly CncGateApproval[] };

const planKeys = (lessonId: string, keep: (assessmentId: string) => boolean = () => true) =>
  (CNC_ASSESSMENT_PLAN[lessonId] ?? []).filter(keep).map((assessmentId) => `${lessonId}:${assessmentId}`);

export const CNC_GATES: readonly CncGate[] = [
  { id: "G1", title: "Nhập môn", keys: planKeys("lesson-1"), approvals: [] },
  { id: "G2", title: "Lập trình tiện", keys: planKeys("lesson-2", (id) => id.startsWith("exercise-") || id === "final"), approvals: [] },
  { id: "G3", title: "Lập trình phay", keys: planKeys("lesson-3", (id) => id.startsWith("exercise-") || id === "final"), approvals: [] },
  {
    id: "G4",
    title: "Vận hành + cài dao",
    keys: [...planKeys("lesson-4-turn", (id) => id !== "checklist-practice"), ...planKeys("lesson-4-mill", (id) => id !== "checklist-practice")],
    approvals: ["turn-operation", "turn-tool-setup", "mill-operation", "mill-tool-setup"],
  },
  { id: "G5", title: "Chi tiết đạt dung sai", keys: [...planKeys("lesson-5", (id) => id === "final" || id === "rubric-exam"), ...planKeys("lesson-6", (id) => id === "final" || id === "rubric-exam")], approvals: [] },
];

export type CncGateStatus = "dat" | "cho_duyet" | "dang_lam" | "chua_lam" | "khoa";
export type CncGateState = {
  gate: CncGate;
  status: CncGateStatus;
  done: number;
  total: number;
  /** Bài + tab còn thiếu để bấm vào; null khi đã đạt, chờ duyệt hoặc cả cổng đang khoá. */
  next: { lessonId: string; section: CncSectionKind } | null;
};

const splitKey = (key: string) => {
  const at = key.lastIndexOf(":");
  return { lessonId: key.slice(0, at), assessmentId: key.slice(at + 1) };
};

export function cncGateStates(passed: Set<string>, isApproved: (id: CncGateApproval) => boolean, isLessonLocked: (lessonId: string) => boolean): CncGateState[] {
  return CNC_GATES.map((gate) => {
    const missing = gate.keys.filter((key) => !passed.has(key));
    const done = gate.keys.length - missing.length;
    const base = { gate, done, total: gate.keys.length };
    if (missing.length === 0) {
      // Đủ bài mà chưa duyệt: không còn việc gì trên web để trỏ tới → không bấm được.
      return { ...base, status: gate.approvals.every(isApproved) ? "dat" : "cho_duyet", next: null };
    }
    const open = missing.map(splitKey).find((item) => !isLessonLocked(item.lessonId));
    if (!open) return { ...base, status: "khoa", next: null };
    return { ...base, status: done > 0 ? "dang_lam" : "chua_lam", next: { lessonId: open.lessonId, section: CNC_ASSESSMENT_SECTION[open.assessmentId] } };
  });
}
