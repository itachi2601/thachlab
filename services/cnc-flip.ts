import type { CncQuizQuestion } from "@/services/cnc-exam-bank";
import { CNC_COMPETENCIES, cncCompetencyStates, type CompetencyId, type CompetencyPermission } from "@/services/cnc-competencies";
import type { CncLearningRecord } from "@/services/cnc-learning-records";
import { CNC_PREP_PASS, CNC_PREP_SESSIONS, summarizeCncPrep, type CncPrepQuestionStat, type CncPrepResponse } from "@/services/cnc-prep";
import { CNC_GATES, cncGateStates, passedAssessmentKeys, type CncGate, type CncGateApproval, type CncGateId, type CncGateStatus } from "@/services/cnc-progress";

// Bảng điều hành giảng viên theo nhịp lớp đảo ngược CNC (docs/CNC-FLIPPED-THIET-KE-LAI-2026-11-08.md mục 4.3–4.4):
// mỗi buổi đọc theo 3 chặng Tối trước → Trong buổi → Sau buổi. File này chỉ tính toán thuần (không gọi mạng)
// để dùng lại ở trang xem thử /dev/cnc-bang-buoi.

// Số bài như sinh viên thấy trên web (lesson-4-mill = Bài 5, lesson-5 = Bài 6, lesson-6 = Bài 7).
export const CNC_FLIP_LESSONS = [
  { id: "lesson-1", no: 1, name: "Tổng quan CNC" },
  { id: "lesson-2", no: 2, name: "Lập trình tiện" },
  { id: "lesson-3", no: 3, name: "Lập trình phay" },
  { id: "lesson-4-turn", no: 4, name: "Vận hành tiện" },
  { id: "lesson-4-mill", no: 5, name: "Vận hành phay" },
  { id: "lesson-5", no: 6, name: "Gia công tiện" },
  { id: "lesson-6", no: 7, name: "Gia công phay" },
] as const;

type SessionExtra = {
  /** Cổng lớp đang hướng tới ở buổi này. */
  gate: CncGateId;
  /** Buổi chốt cổng: cuối buổi lớp phải đạt. */
  gateCheck: boolean;
  machine: string;
  winnc: string;
  /** Quyền năng lực phải có mới được cắt thật ở buổi này. */
  cutNeeds: readonly CncGateApproval[];
};

const TURN_CUT = ["turn-operation", "turn-tool-setup"] as const;
const MILL_CUT = ["mill-operation", "mill-tool-setup"] as const;

const EXTRA: Record<number, SessionExtra> = {
  1: { gate: "G1", gateCheck: true, machine: "Nhận máy, Reference, JOG, MDI", winnc: "Chạy O0001", cutNeeds: [] },
  2: { gate: "G2", gateCheck: false, machine: "JOG/MDI theo phiếu, chạy khối không phôi", winnc: "Viết trục bậc G00/G01", cutNeeds: [] },
  3: { gate: "G2", gateCheck: true, machine: "Gá phôi, tiện mặt đầu bằng tay", winnc: "Bù mũi dao, chu trình", cutNeeds: [] },
  4: { gate: "G3", gateCheck: false, machine: "Máy phay: JOG, thay dao, MDI", winnc: "Rãnh, bậc", cutNeeds: [] },
  5: { gate: "G3", gateCheck: true, machine: "Phay mặt phẳng bằng tay", winnc: "Contour, 4 lỗ", cutNeeds: [] },
  6: { gate: "G4", gateCheck: true, machine: "Đặt W, đo dao, chạy chương trình buổi 3 trên phôi", winnc: "Nhập offset, mô phỏng", cutNeeds: [] },
  7: { gate: "G4", gateCheck: true, machine: "Dò cạnh, bù dài/bán kính, chạy chương trình buổi 5", winnc: "Nhập offset, mô phỏng", cutNeeds: [] },
  8: { gate: "G5", gateCheck: false, machine: "Cắt trục bậc vát/bo", winnc: "Kiểm chương trình trước khi cắt", cutNeeds: TURN_CUT },
  9: { gate: "G5", gateCheck: true, machine: "Trục côn, ren; đo, ghi sai lệch", winnc: "Kiểm chương trình trước khi cắt", cutNeeds: TURN_CUT },
  10: { gate: "G5", gateCheck: false, machine: "Phay bậc, cung", winnc: "Kiểm chương trình trước khi cắt", cutNeeds: MILL_CUT },
  11: { gate: "G5", gateCheck: true, machine: "Tấm đế 4 lỗ ren", winnc: "Kiểm chương trình trước khi cắt", cutNeeds: MILL_CUT },
  12: { gate: "G5", gateCheck: true, machine: "Dự án: từ bản vẽ đến chi tiết", winnc: "Chạy thử toàn bộ", cutNeeds: [...TURN_CUT, ...MILL_CUT] },
};

export type CncFlipSession = SessionExtra & {
  no: number;
  title: string;
  lessonId: string | null;
  /** Gói đọc tối trước; null = buổi không có gói (buổi 1). */
  read: string | null;
  anchor: string | null;
  hasPrep: boolean;
};

export const CNC_FLIP_SESSIONS: readonly CncFlipSession[] = [
  { no: 1, title: "Nhập môn", lessonId: "lesson-1", read: null, anchor: null, hasPrep: false, ...EXTRA[1] },
  ...CNC_PREP_SESSIONS.map((s) => ({ no: s.no, title: s.title, lessonId: s.lessonId, read: s.read, anchor: s.anchor, hasPrep: true, ...EXTRA[s.no] })),
];

export const CNC_FLIP_SESSION_COUNT = CNC_FLIP_SESSIONS.length;

export const cncFlipLessonLabel = (lessonId: string | null) => {
  const lesson = CNC_FLIP_LESSONS.find((item) => item.id === lessonId);
  return lesson ? `Bài ${lesson.no} · ${lesson.name}` : "Dự án nhóm";
};

/** Buổi mặc định khi mở bảng: số ngày đã có ca điểm danh (hôm nay có ca thì là buổi hôm nay, chưa có thì buổi kế). */
export function inferCncFlipSession(sessionDates: string[], today: string) {
  const past = new Set(sessionDates.filter((date) => date <= today));
  const no = past.has(today) ? past.size : past.size + 1;
  return Math.min(CNC_FLIP_SESSION_COUNT, Math.max(1, no));
}

export type FlipStudent = { id: string; name: string; records: CncLearningRecord[] };
type Ref = { id: string; name: string };

export type FlipGateSummary = { gate: CncGate; byStatus: Record<CncGateStatus, Ref[]> };

export type FlipBoard = {
  session: CncFlipSession;
  prep: {
    /** Buổi có gói tối trước và đã đăng câu hỏi. */
    available: boolean;
    questions: CncQuizQuestion[];
    rows: CncPrepResponse[];
    pass: number;
    avg: number;
    /** Câu xếp theo tỉ lệ sai lượt đầu, cao nhất trước. */
    ranked: CncPrepQuestionStat[];
    notes: { studentId: string; name: string; text: string; at: string }[];
    ready: Ref[];
    weak: (Ref & { best: number })[];
    none: Ref[];
  };
  /** Số sinh viên đã làm quiz chuẩn bị theo từng buổi (buổi chưa đăng câu thì không có). */
  prepDone: Record<number, number>;
  gates: FlipGateSummary[];
  /** Đủ bài trên web, chờ giảng viên duyệt tại xưởng. */
  waiting: (Ref & { items: string[] })[];
  /** Chưa đủ quyền cắt thật cho buổi này. */
  cutBlocked: (Ref & { missing: string[] })[];
  /** Cần kèm sau buổi: chậm cổng đã chốt, bỏ chuẩn bị nhiều buổi. */
  behind: (Ref & { reasons: string[]; score: number })[];
};

const competencyTitle = (id: CompetencyId) => CNC_COMPETENCIES.find((item) => item.id === id)?.title ?? id;

export function buildFlipBoard(input: {
  students: FlipStudent[];
  permissions: CompetencyPermission[];
  openLessons: string[];
  banks: Record<number, CncQuizQuestion[]>;
  prepRows: CncPrepResponse[];
  sessionNo: number;
}): FlipBoard {
  const { students, permissions, openLessons, banks, prepRows, sessionNo } = input;
  const session = CNC_FLIP_SESSIONS.find((item) => item.no === sessionNo) ?? CNC_FLIP_SESSIONS[0];
  const ref = (student: FlipStudent): Ref => ({ id: student.id, name: student.name });
  const enrolled = new Set(students.map((student) => student.id));
  const rowsOf = (no: number) => prepRows.filter((row) => row.session_no === no && enrolled.has(row.student_id));

  // --- Tối trước ---
  const questions = banks[session.no] ?? [];
  const rows = rowsOf(session.no);
  const summary = summarizeCncPrep(rows, questions);
  const pass = Math.min(CNC_PREP_PASS, questions.length || CNC_PREP_PASS);
  const nameOf = new Map(students.map((student) => [student.id, student.name]));
  const ready: Ref[] = [];
  const weak: (Ref & { best: number })[] = [];
  const none: Ref[] = [];
  for (const student of students) {
    const best = summary.best.get(student.id);
    if (best === undefined) none.push(ref(student));
    else if (best >= pass) ready.push(ref(student));
    else weak.push({ ...ref(student), best });
  }
  const ranked = [...summary.stats]
    .filter((stat) => stat.answered > 0)
    .sort((a, b) => b.wrong / b.answered - a.wrong / a.answered);

  const prepDone: Record<number, number> = {};
  for (const item of CNC_FLIP_SESSIONS) {
    if (banks[item.no]?.length) prepDone[item.no] = new Set(rowsOf(item.no).map((row) => row.student_id)).size;
  }

  // --- Cổng năng lực + quyền đứng máy ---
  const gates: FlipGateSummary[] = CNC_GATES.map((gate) => ({
    gate,
    byStatus: { dat: [], cho_duyet: [], dang_lam: [], chua_lam: [], khoa: [] },
  }));
  const waiting: FlipBoard["waiting"] = [];
  const cutBlocked: FlipBoard["cutBlocked"] = [];
  const behind: FlipBoard["behind"] = [];
  const lastCheck = new Map<CncGateId, number>();
  for (const item of CNC_FLIP_SESSIONS) if (item.gateCheck) lastCheck.set(item.gate, item.no);
  const prepSessionsSoFar = CNC_FLIP_SESSIONS.filter((item) => item.no <= session.no && banks[item.no]?.length);
  const doneBySession = new Map(prepSessionsSoFar.map((item) => [item.no, new Set(rowsOf(item.no).map((row) => row.student_id))]));

  for (const student of students) {
    const own = permissions.filter((row) => row.student_id === student.id);
    const competency = cncCompetencyStates(student.records, own);
    const states = cncGateStates(
      passedAssessmentKeys(student.records),
      (id) => competency[id].approved,
      (lessonId) => !openLessons.includes(lessonId),
    );
    states.forEach((state, index) => gates[index].byStatus[state.status].push(ref(student)));

    const waitingItems = CNC_COMPETENCIES.filter((item) => item.approvalRequired && competency[item.id].eligible && !competency[item.id].approved).map((item) => item.title);
    if (waitingItems.length) waiting.push({ ...ref(student), items: waitingItems });

    const missing = session.cutNeeds.filter((id) => !competency[id].approved).map(competencyTitle);
    if (missing.length) cutBlocked.push({ ...ref(student), missing });

    const reasons: string[] = [];
    let score = 0;
    for (const state of states) {
      const due = lastCheck.get(state.gate.id) ?? CNC_FLIP_SESSION_COUNT;
      if (due >= session.no || state.status === "dat") continue;
      reasons.push(state.status === "cho_duyet" ? `${state.gate.id} chờ duyệt` : `${state.gate.id} mới ${state.done}/${state.total}`);
      score += state.status === "cho_duyet" ? 1 : 3;
    }
    const skipped = prepSessionsSoFar.filter((item) => !doneBySession.get(item.no)?.has(student.id)).length;
    if (skipped >= 2) {
      reasons.push(`Bỏ chuẩn bị ${skipped}/${prepSessionsSoFar.length} buổi`);
      score += skipped;
    }
    if (reasons.length) behind.push({ ...ref(student), reasons, score });
  }
  behind.sort((a, b) => b.score - a.score);

  return {
    session,
    prep: {
      available: session.hasPrep && questions.length > 0,
      questions,
      rows,
      pass,
      avg: summary.avg,
      ranked,
      notes: summary.notes.map((note) => ({ ...note, name: nameOf.get(note.studentId) ?? "Sinh viên" })),
      ready,
      weak,
      none,
    },
    prepDone,
    gates,
    waiting,
    cutBlocked,
    behind,
  };
}
