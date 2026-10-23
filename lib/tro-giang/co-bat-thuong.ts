import type { SessionPolicy } from "./policy";

/** Phần của một buổi mà việc gắn cờ cần; TaPendingSession và TaSessionRow đều thoả. */
export interface FlagSession {
  id: string;
  assistant_id: string;
  work_date: string;
  session_type: string;
  start_time?: string | null;
  end_time?: string | null;
  hours?: number | null;
  student_touches?: number | null;
  created_at?: string;
  policy?: SessionPolicy;
}

export type FlagLevel = "red" | "amber";
export interface SessionFlag {
  code: string;
  level: FlagLevel;
  text: string;
}

/** Số buổi lặp tối thiểu (kể cả buổi đang xét) để coi là "lặp y hệt". */
const REPEAT_MIN = 4;
const LATE_LOG_DAYS = 5;
const TOUCH_TARGET = 12;

const toMin = (t: string | null | undefined) => {
  if (!t) return null;
  const [h, m] = t.split(":").map(Number);
  return Number.isFinite(h) && Number.isFinite(m) ? h * 60 + m : null;
};
const slotKey = (s: FlagSession) => (s.start_time && s.end_time ? `${s.start_time.slice(0, 5)}-${s.end_time.slice(0, 5)}` : null);
const dayDiff = (a: string, b: string) => Math.round((new Date(b).getTime() - new Date(a).getTime()) / 86400000);

const isAbsent = (s: FlagSession) => s.policy?.attendance === "excused_absence" || s.policy?.attendance === "unexcused_absence";
const allTicked = (s: FlagSession) =>
  !!s.policy && s.policy.arrived_early && s.policy.homework_checked && s.policy.walked_tables && s.policy.reported_students;

/**
 * `history`: các buổi gần đây của cùng trợ giảng (mọi trạng thái, kể cả buổi đang xét).
 * `passRatio`: kết quả RPC ta_tutoring_pass_ratio cho buổi phụ đạo (undefined = chưa tra được).
 */
export function flagSession(
  s: FlagSession,
  history: FlagSession[],
  passRatio?: number | null,
): SessionFlag[] {
  const flags: SessionFlag[] = [];
  const mine = history.filter((h) => h.assistant_id === s.assistant_id);
  const others = mine.filter((h) => h.id !== s.id);

  // Trùng giờ với buổi khác cùng ngày của chính bạn đó.
  const a0 = toMin(s.start_time);
  const a1 = toMin(s.end_time);
  if (a0 != null && a1 != null) {
    const clash = others.find((h) => {
      if (h.work_date !== s.work_date) return false;
      const b0 = toMin(h.start_time);
      const b1 = toMin(h.end_time);
      return b0 != null && b1 != null && a0 < b1 && b0 < a1;
    });
    if (clash) flags.push({ code: "overlap", level: "red", text: "Trùng giờ với một buổi khác của bạn này trong cùng ngày" });
  }

  // Giờ ghi lệch giờ vào/ra.
  if (a0 != null && a1 != null && s.hours != null && Math.abs((a1 - a0) / 60 - s.hours) > 0.26) {
    flags.push({ code: "hours_mismatch", level: "amber", text: "Số giờ khác khoảng giờ vào/ra đã ghi" });
  }

  // Ghi muộn.
  const lag = s.created_at ? dayDiff(s.work_date, s.created_at.slice(0, 10)) : 0;
  if (lag > LATE_LOG_DAYS) flags.push({ code: "late_log", level: "amber", text: `Ghi muộn ${lag} ngày sau buổi` });

  // Khung giờ lặp y hệt.
  const key = slotKey(s);
  if (key) {
    const same = mine.filter((h) => slotKey(h) === key && h.session_type === s.session_type).length;
    if (same >= REPEAT_MIN)
      flags.push({ code: "same_slot", level: "amber", text: `Khung giờ ${key} lặp y hệt ở ${same} buổi gần đây` });
  }

  if (s.session_type === "lop" && !isAbsent(s)) {
    const lessons = mine
      .filter((h) => h.session_type === "lop" && !isAbsent(h) && h.work_date <= s.work_date)
      .sort((x, y) => y.work_date.localeCompare(x.work_date))
      .slice(0, REPEAT_MIN + 1);
    if (lessons.length >= REPEAT_MIN) {
      if (lessons.every(allTicked))
        flags.push({ code: "all_ticks", level: "amber", text: `Tick đủ mọi mục ở ${lessons.length} buổi lên lớp liên tiếp` });
      if (lessons.every((h) => (h.student_touches ?? 0) >= TOUCH_TARGET))
        flags.push({ code: "touch_streak", level: "amber", text: `Đạt từ ${TOUCH_TARGET} lượt tiếp xúc ở ${lessons.length} buổi liên tiếp` });
    }
  }

  if (s.session_type === "phudao") {
    if (passRatio === 0)
      flags.push({ code: "no_exit_evidence", level: "red", text: "Không có em nào làm đạt bài cuối buổi trong ngày — chưa có bằng chứng buổi phụ đạo diễn ra" });
    else if (passRatio === null)
      flags.push({ code: "no_topics", level: "amber", text: "Chưa gắn chủ đề phụ đạo cho em nào, hệ thống không đối chiếu được" });
  }

  return flags.sort((x, y) => (x.level === y.level ? 0 : x.level === "red" ? -1 : 1));
}

export const LEVEL_INFO: Record<FlagLevel, { label: string; meaning: string }> = {
  red: {
    label: "Cờ đỏ",
    meaning: "Dấu hiệu buổi này có thể không diễn ra hoặc ghi sai. Nên xác minh trước khi duyệt hoặc chốt tháng.",
  },
  amber: {
    label: "Cờ vàng",
    meaning: "Bất thường nhẹ hoặc quá đều đặn. Chưa kết luận gì, chỉ cần liếc qua; nhiều cờ vàng lặp lại ở cùng một người thì hỏi lại người đó.",
  },
};

/** Giải thích bằng lời thường: cờ nghĩa là gì và thầy nên làm gì. */
export const FLAG_INFO: Record<string, { title: string; why: string; todo: string }> = {
  overlap: {
    title: "Trùng giờ",
    why: "Hai buổi của cùng một người chồng lên nhau trong một ngày, nên không thể cùng diễn ra thật.",
    todo: "Mở cả hai buổi, hỏi lại giờ đúng rồi sửa; buổi nào không có thật thì chuyển sang Từ chối.",
  },
  no_exit_evidence: {
    title: "Phụ đạo chưa có bằng chứng",
    why: "Hôm đó không em nào làm đạt bài cuối buổi trong hệ thống, trong khi điểm phụ đạo dựa vào bài này.",
    todo: "Hỏi trợ giảng đã mở bài cuối buổi chưa hoặc hỏi lại em; nếu buổi có thật mà quên mở bài thì ghi chú rồi cho duyệt, không thì từ chối.",
  },
  no_topics: {
    title: "Chưa gắn chủ đề phụ đạo",
    why: "Buổi chưa ghi chủ đề cho em nào nên hệ thống không đối chiếu được với bài cuối buổi.",
    todo: "Nhắc trợ giảng gắn chủ đề cho lần sau; buổi này duyệt theo ghi chú trong phiếu.",
  },
  hours_mismatch: {
    title: "Giờ ghi lệch giờ vào/ra",
    why: "Số giờ tính tiền khác khoảng giờ bắt đầu đến kết thúc đã ghi.",
    todo: "So lại hai con số, sửa cho khớp. Tiền tính theo số giờ nên đây là chỗ dễ sai nhất.",
  },
  late_log: {
    title: "Ghi muộn",
    why: "Phiếu được ghi hơn 5 ngày sau buổi, dễ nhớ nhầm giờ hoặc số liệu.",
    todo: "Nếu chỉ một lần thì bỏ qua; nếu lặp lại thì nhắc ghi trong ngày.",
  },
  same_slot: {
    title: "Khung giờ lặp y hệt",
    why: "Nhiều buổi gần đây có đúng cùng giờ vào và ra, có thể là lịch cố định, cũng có thể là điền sẵn.",
    todo: "Đối chiếu với lịch lớp. Khớp lịch thì bỏ qua.",
  },
  all_ticks: {
    title: "Tick đủ mọi mục nhiều buổi liền",
    why: "Mọi ô trong phiếu đều được tick ở nhiều buổi liên tiếp, nên khó phân biệt làm thật với tick cho xong.",
    todo: "Hỏi miệng một việc cụ thể (hôm đó em nào làm sai bài gì), hoặc dự một buổi.",
  },
  touch_streak: {
    title: "Tiếp xúc luôn đạt mục tiêu",
    why: "Số lượt tiếp xúc đạt từ 12 ở nhiều buổi liên tiếp. Có thể giỏi thật, cũng có thể đếm rộng tay.",
    todo: "Hỏi tên vài em đã tiếp xúc hôm đó; trả lời được thì yên tâm.",
  },
};
