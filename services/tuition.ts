import { getSupabase } from "@/services/supabase";

/** Sổ học phí theo tháng. Hàm đọc của phụ huynh nuốt lỗi và trả []. Hàm ghi ném lỗi. */

export interface FeeVisibility {
  staffVisible: boolean;
  familyVisible: boolean;
}

export interface FeePlan {
  id: number;
  classId: number;
  billingKey: string;
  label: string;
  amountVnd: number;
  dueDay: number;
  active: boolean;
}

export interface FeeCharge {
  chargeId: number;
  planId: number;
  studentId: string;
  studentName: string;
  billingKey: string;
  label: string;
  period: string;
  amountVnd: number;
  paidVnd: number;
  waived: boolean;
  dueDay: number;
}

export interface FamilyTuitionLine {
  studentId: string;
  studentName: string;
  billingKey: string;
  label: string;
  period: string;
  amountVnd: number;
  paidVnd: number;
  waived: boolean;
  dueDay: number;
}

function fail(error: unknown, fallback: string): Error {
  const raw = error as { message?: unknown } | null;
  const message = typeof raw?.message === "string" && raw.message.trim() ? raw.message.trim() : fallback;
  return new Error(message);
}

export async function fetchFeeVisibility(): Promise<FeeVisibility> {
  const { data, error } = await getSupabase().rpc("thpt_fee_visibility");
  if (error) return { staffVisible: false, familyVisible: false };
  const row = ((data ?? []) as { staff_visible: boolean; family_visible: boolean }[])[0];
  if (!row) return { staffVisible: false, familyVisible: false };
  return { staffVisible: !!row.staff_visible, familyVisible: !!row.family_visible };
}

export async function setFeeVisibility(staffVisible: boolean, familyVisible: boolean): Promise<void> {
  const { error } = await getSupabase().rpc("thpt_fee_set_visibility", {
    p_staff: staffVisible,
    p_family: familyVisible,
  });
  if (error) throw fail(error, "Chưa đổi được cách hiện sổ.");
}

export async function fetchFeePlans(classId: number): Promise<FeePlan[]> {
  const { data, error } = await getSupabase().rpc("thpt_fee_plans", { p_class: classId });
  if (error) throw fail(error, "Chưa đọc được mức thu.");
  return ((data ?? []) as {
    id: number; class_id: number; billing_key: string; label: string;
    amount_vnd: number; due_day: number; active: boolean;
  }[]).map((r) => ({
    id: r.id,
    classId: r.class_id,
    billingKey: r.billing_key,
    label: r.label,
    amountVnd: r.amount_vnd,
    dueDay: r.due_day,
    active: r.active,
  }));
}

export async function upsertFeePlan(input: {
  classId: number;
  billingKey: string;
  label: string;
  amountVnd: number;
  dueDay: number;
}): Promise<void> {
  const { error } = await getSupabase().rpc("thpt_fee_upsert_plan", {
    p_class: input.classId,
    p_billing_key: input.billingKey,
    p_label: input.label,
    p_amount: input.amountVnd,
    p_due_day: input.dueDay,
  });
  if (error) throw fail(error, "Chưa lưu được mức thu.");
}

export async function archiveFeePlan(planId: number): Promise<void> {
  const { error } = await getSupabase().rpc("thpt_fee_archive_plan", { p_plan: planId });
  if (error) throw fail(error, "Chưa ngừng được mức thu.");
}

export async function ensureFeeMonth(classId: number, period: string): Promise<number> {
  const { data, error } = await getSupabase().rpc("thpt_fee_ensure_month", {
    p_class: classId,
    p_period: period,
  });
  if (error) throw fail(error, "Chưa tạo được khoản tháng.");
  return typeof data === "number" ? data : 0;
}

export async function fetchFeeLedger(classId: number, period: string): Promise<FeeCharge[]> {
  const { data, error } = await getSupabase().rpc("thpt_fee_ledger", {
    p_class: classId,
    p_period: period,
  });
  if (error) throw fail(error, "Chưa đọc được sổ tháng.");
  return ((data ?? []) as {
    charge_id: number; plan_id: number; student_id: string; student_name: string;
    billing_key: string; label: string; period: string; amount_vnd: number;
    paid_vnd: number; waived: boolean; due_day: number;
  }[]).map((r) => ({
    chargeId: r.charge_id,
    planId: r.plan_id,
    studentId: r.student_id,
    studentName: r.student_name,
    billingKey: r.billing_key,
    label: r.label,
    period: r.period,
    amountVnd: r.amount_vnd,
    paidVnd: r.paid_vnd,
    waived: r.waived,
    dueDay: r.due_day,
  }));
}

export async function recordFeePayment(input: {
  chargeId: number;
  amountVnd: number;
  method: "center" | "transfer";
  paidOn: string;
  note: string;
}): Promise<void> {
  const { error } = await getSupabase().rpc("thpt_fee_record_payment", {
    p_charge: input.chargeId,
    p_amount: input.amountVnd,
    p_method: input.method,
    p_paid_on: input.paidOn,
    p_note: input.note,
  });
  if (error) throw fail(error, "Chưa ghi được khoản đóng.");
}

export async function waiveFeeCharge(chargeId: number, waived: boolean): Promise<void> {
  const { error } = await getSupabase().rpc("thpt_fee_waive", { p_charge: chargeId, p_waived: waived });
  if (error) throw fail(error, "Chưa đổi được miễn phí.");
}

/** Rỗng khi sổ đang ẩn, migration chưa chạy, hoặc phụ huynh chưa có khoản. */
export async function fetchFamilyTuition(): Promise<FamilyTuitionLine[]> {
  try {
    const { data, error } = await getSupabase().rpc("thpt_fee_family_lines");
    if (error) return [];
    return ((data ?? []) as {
      student_id: string; student_name: string; billing_key: string; label: string;
      period: string; amount_vnd: number; paid_vnd: number; waived: boolean; due_day: number;
    }[]).map((r) => ({
      studentId: r.student_id,
      studentName: r.student_name,
      billingKey: r.billing_key,
      label: r.label,
      period: r.period,
      amountVnd: r.amount_vnd,
      paidVnd: r.paid_vnd,
      waived: r.waived,
      dueDay: r.due_day,
    }));
  } catch {
    return [];
  }
}
