import { derivePair } from "@/services/thpt-courses-public";

/**
 * Sổ học phí theo tháng — phần thuần, không gọi Supabase.
 * Cổng bật/tắt nằm ở bảng `thpt_fee_settings` (mặc định cả hai cờ false).
 * Hàm `thpt_fee_billing_key` trong migration phải cho cùng kết quả với `billingKeyOf`.
 */

export const TUITION_AMOUNT_MAX = 20_000_000;

export function billingKeyOf(course: {
  id: number;
  name: string;
  pairKey?: string | null;
  pairSlot?: string | null;
  pair_key?: string | null;
  pair_slot?: string | null;
}): string {
  const pair = derivePair({
    name: course.name,
    pair_key: course.pair_key ?? course.pairKey,
    pair_slot: course.pair_slot ?? course.pairSlot,
  });
  return pair.pairKey ? `pair:${pair.pairKey}` : `course:${course.id}`;
}

/** YYYY-MM-DD theo giờ Việt Nam. */
export function todayVn(now: Date): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Ho_Chi_Minh",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(now);
}

/** Ngày 1 của tháng theo giờ Việt Nam. */
export function monthStart(now: Date): string {
  return `${todayVn(now).slice(0, 7)}-01`;
}

export function monthTitle(period: string): string {
  const [y, m] = period.split("-");
  return `Tháng ${Number(m)}/${y}`;
}

export function dueLabel(period: string, dueDay: number): string {
  const [y, m] = period.split("-");
  return `${dueDay}/${Number(m)}/${y}`;
}

export function formatVnd(amount: number): string {
  return `${Math.round(amount).toLocaleString("vi-VN")} đ`;
}

/** Nhận "800.000" hoặc "800000". Ngoài 1…20.000.000 thì null. */
export function parseAmountVnd(raw: string): number | null {
  const digits = raw.replace(/\D/g, "");
  if (!digits) return null;
  const n = Number(digits);
  if (!Number.isSafeInteger(n) || n < 1 || n > TUITION_AMOUNT_MAX) return null;
  return n;
}

export function chargeState(amountVnd: number, paidVnd: number, waived: boolean): "waived" | "paid" | "open" {
  if (waived) return "waived";
  if (paidVnd >= amountVnd) return "paid";
  return "open";
}

export interface ChargeDraft {
  planId: number;
  studentId: string;
  period: string;
  amountVnd: number;
}

/**
 * Cùng quy tắc với `thpt_fee_ensure_month`: một học sinh + một mức thu + một tháng = một khoản.
 * Buổi A và buổi B cùng pair chỉ sinh một khoản. Chờ duyệt / đã nghỉ không tính.
 */
export function chargesForMonth(
  plans: { id: number; billingKey: string; amountVnd: number; active: boolean }[],
  regs: { studentId: string | null; status: string; billingKey: string }[],
  period: string,
): ChargeDraft[] {
  const active = new Map(plans.filter((p) => p.active).map((p) => [p.billingKey, p]));
  const seen = new Set<string>();
  const out: ChargeDraft[] = [];
  for (const r of regs) {
    if (!r.studentId || (r.status !== "active" && r.status !== "catchup")) continue;
    const plan = active.get(r.billingKey);
    if (!plan) continue;
    const key = `${plan.id}:${r.studentId}:${period}`;
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({ planId: plan.id, studentId: r.studentId, period, amountVnd: plan.amountVnd });
  }
  return out;
}

export interface TuitionMonth {
  studentId: string;
  billingKey: string;
  label: string;
  period: string;
  amountVnd: number;
  paidVnd: number;
  waived: boolean;
  dueDay: number;
}

export interface TuitionRegistration {
  id: number;
  courseId: number;
  courseName: string;
  studentId: string | null;
  paymentStatus: "unpaid" | "paid_center" | "paid_transfer";
  paymentNote: string;
}

export interface TuitionCourseRef {
  id: number;
  name: string;
  feeNote: string;
  pairKey: string | null;
  pairSlot: string | null;
}

export interface ParentFeeBlock {
  key: string;
  title: string;
  feeNote: string;
  paymentStatus: TuitionRegistration["paymentStatus"];
  paymentNote: string;
  /** Rỗng → giữ câu "đã đóng / thầy chưa ghi nhận" như hiện tại. Có dòng → chỉ hiện sổ tháng. */
  months: TuitionMonth[];
}

/** Gộp hai buổi cùng lớp thành một khối khi đã có khoản tháng, để phụ huynh không thấy học phí hai lần. */
export function parentFeeBlocks(
  regs: TuitionRegistration[],
  courses: TuitionCourseRef[],
  months: TuitionMonth[],
): ParentFeeBlock[] {
  const courseById = new Map(courses.map((c) => [c.id, c]));
  const out: ParentFeeBlock[] = [];
  const seenLedger = new Set<string>();
  for (const r of regs) {
    const course = courseById.get(r.courseId);
    const billingKey = course ? billingKeyOf(course) : null;
    const mine =
      billingKey && r.studentId
        ? months.filter((m) => m.studentId === r.studentId && m.billingKey === billingKey)
        : [];
    if (mine.length > 0 && r.studentId && billingKey) {
      const key = `${r.studentId}:${billingKey}`;
      if (seenLedger.has(key)) continue;
      seenLedger.add(key);
      out.push({
        key,
        title: mine[0].label || r.courseName,
        feeNote: course?.feeNote ?? "",
        paymentStatus: r.paymentStatus,
        paymentNote: r.paymentNote,
        months: [...mine].sort((a, b) => b.period.localeCompare(a.period)),
      });
      continue;
    }
    out.push({
      key: `reg:${r.id}`,
      title: r.courseName,
      feeNote: course?.feeNote ?? "",
      paymentStatus: r.paymentStatus,
      paymentNote: r.paymentNote,
      months: [],
    });
  }
  return out;
}

/** Câu phụ huynh đọc được, không chỉ dựa vào màu (P12). Chưa đóng nói trung tính (P23). */
export function parentMonthLine(row: TuitionMonth): { tone: "paid" | "open" | "waived"; text: string } {
  const label = monthTitle(row.period);
  if (row.waived) return { tone: "waived", text: `${label}: được miễn.` };
  if (chargeState(row.amountVnd, row.paidVnd, false) === "paid") {
    return { tone: "paid", text: `${label}: đã đóng ${formatVnd(row.paidVnd)}.` };
  }
  const remain = row.amountVnd - row.paidVnd;
  if (row.paidVnd > 0) {
    return {
      tone: "open",
      text: `${label}: còn ${formatVnd(remain)}. Nếu đã chuyển khoản, nhắn thầy để thầy ghi nhận.`,
    };
  }
  return {
    tone: "open",
    text: `${label}: chưa ghi nhận khoản đóng (${formatVnd(row.amountVnd)}, hạn ${dueLabel(row.period, row.dueDay)}). Nếu đã đóng, nhắn thầy để thầy ghi nhận.`,
  };
}
