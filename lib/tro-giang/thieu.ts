import type { TaPendingSession } from "./queries";

/**
 * Liệt kê phần còn thiếu của một phiếu chờ duyệt (tính ở client, không đụng schema).
 * Phụ đạo: bài giao + nhận xét từng em. Lên lớp: lỗi lớp + kiểm tra bài tập.
 */
export function missingParts(s: TaPendingSession): string[] {
  const out: string[] = [];
  if (s.session_type === "phudao") {
    if (!s.homework_given?.trim()) out.push("bài giao");
    const followups = s.policy?.followups ?? [];
    const names = s.phudao_students ?? [];
    const noted = (n: string) => followups.some((f) => f.student === n && f.difficulty?.trim());
    const missing = names.length
      ? names.filter((n) => !noted(n)).length
      : followups.filter((f) => !f.difficulty?.trim()).length;
    if (missing > 0) out.push(`nhận xét ${missing} em`);
    else if (names.length === 0 && followups.length === 0) out.push("tên em và nhận xét");
  } else if (s.session_type === "lop") {
    if (!s.error_note?.trim()) out.push("lỗi lớp");
    if (s.policy && !s.policy.homework_checked) out.push("kiểm tra bài tập");
  }
  return out;
}
