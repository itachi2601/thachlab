import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { PGlite } from "@electric-sql/pglite";
import {
  billingKeyOf,
  chargesForMonth,
  chargeState,
  formatVnd,
  monthStart,
  parentFeeBlocks,
  parentMonthLine,
  parseAmountVnd,
  type TuitionCourseRef,
  type TuitionMonth,
  type TuitionRegistration,
} from "../features/tuition/ledger";

const pairA = {
  id: 1,
  name: "Vật lí 12L1 — buổi A · Thứ 4",
  pairKey: "Vật lí 12L1",
  pairSlot: "A",
};
const pairB = {
  id: 2,
  name: "Vật lí 12L1 — buổi B · Thứ 7",
  pairKey: "Vật lí 12L1",
  pairSlot: "B",
};
const single = { id: 9, name: "Vật lí 10", pairKey: null, pairSlot: null };

assert.equal(billingKeyOf(pairA), "pair:Vật lí 12L1");
assert.equal(billingKeyOf(pairB), billingKeyOf(pairA));
assert.equal(billingKeyOf({ id: 3, name: "Vật lí 12L1 — buổi A · Thứ 4" }), "pair:Vật lí 12L1");
assert.equal(billingKeyOf(single), "course:9");

assert.equal(monthStart(new Date("2026-10-05T17:30:00Z")), "2026-10-01");
assert.equal(monthStart(new Date("2026-09-30T16:30:00Z")), "2026-09-01");
assert.equal(monthStart(new Date("2026-09-30T17:30:00Z")), "2026-10-01");

assert.equal(parseAmountVnd("800.000"), 800000);
assert.equal(parseAmountVnd("0"), null);
assert.equal(parseAmountVnd("20000001"), null);
assert.equal(formatVnd(800000), "800.000 đ");

assert.equal(chargeState(100, 100, false), "paid");
assert.equal(chargeState(100, 40, false), "open");
assert.equal(chargeState(100, 100, true), "waived");

const plans = [{ id: 4, billingKey: "pair:Vật lí 12L1", amountVnd: 800000, active: true }];
const regs = [
  { studentId: "s1", status: "active", billingKey: "pair:Vật lí 12L1" },
  { studentId: "s1", status: "active", billingKey: "pair:Vật lí 12L1" },
  { studentId: "s2", status: "catchup", billingKey: "pair:Vật lí 12L1" },
  { studentId: "s3", status: "pending", billingKey: "pair:Vật lí 12L1" },
  { studentId: null, status: "active", billingKey: "pair:Vật lí 12L1" },
];
const drafts = chargesForMonth(plans, regs, "2026-10-01");
assert.deepEqual(
  drafts.map((d) => d.studentId),
  ["s1", "s2"],
);
assert.equal(drafts[0].amountVnd, 800000);

const course = (c: typeof pairA): TuitionCourseRef => ({
  id: c.id,
  name: c.name,
  feeNote: "Đóng tại trung tâm",
  pairKey: c.pairKey,
  pairSlot: c.pairSlot,
});
const reg = (id: number, courseId: number, name: string): TuitionRegistration => ({
  id,
  courseId,
  courseName: name,
  studentId: "s1",
  paymentStatus: "unpaid",
  paymentNote: "",
});
const month: TuitionMonth = {
  studentId: "s1",
  billingKey: "pair:Vật lí 12L1",
  label: "Vật lí 12L1",
  period: "2026-10-01",
  amountVnd: 800000,
  paidVnd: 0,
  waived: false,
  dueDay: 5,
};

const hidden = parentFeeBlocks(
  [reg(1, 1, pairA.name), reg(2, 2, pairB.name)],
  [course(pairA), course(pairB)],
  [],
);
assert.equal(hidden.length, 2);
assert.equal(hidden[0].months.length, 0);

const shown = parentFeeBlocks(
  [reg(1, 1, pairA.name), reg(2, 2, pairB.name)],
  [course(pairA), course(pairB)],
  [month],
);
assert.equal(shown.length, 1);
assert.equal(shown[0].title, "Vật lí 12L1");
assert.match(parentMonthLine(month).text, /Tháng 10\/2026: chưa ghi nhận khoản đóng \(800\.000 đ, hạn 5\/10\/2026\)/);
assert.equal(parentMonthLine({ ...month, paidVnd: 800000 }).tone, "paid");
assert.equal(parentMonthLine({ ...month, paidVnd: 800000, waived: true }).tone, "waived");
assert.match(parentMonthLine({ ...month, paidVnd: 300000 }).text, /còn 500\.000 đ/);

const sql = readFileSync(new URL("../supabase/migrations/20261006120000_thpt_fee_ledger.sql", import.meta.url), "utf8");
const fn = sql.match(/-- BEGIN billing_key\n([\s\S]*?)\n-- END billing_key/)?.[1];
assert.ok(fn, "không thấy hàm thpt_fee_billing_key trong migration");
const db = new PGlite();
await db.exec(fn!);
const cases: { args: [number, string, string | null, string | null]; want: string }[] = [
  { args: [1, "Vật lí 12L1 — buổi A · Thứ 4", "Vật lí 12L1", "A"], want: "pair:Vật lí 12L1" },
  { args: [2, "Vật lí 12L1 — buổi B · Thứ 7", "Vật lí 12L1", "B"], want: "pair:Vật lí 12L1" },
  { args: [3, "Vật lí 12L1 — buổi A · Thứ 4", null, null], want: "pair:Vật lí 12L1" },
  { args: [9, "Vật lí 10", null, null], want: "course:9" },
];
for (const { args, want } of cases) {
  const row = await db.query<{ k: string }>(
    "select public.thpt_fee_billing_key($1, $2, $3, $4) as k",
    args,
  );
  assert.equal(row.rows[0].k, want);
}
await db.close();

console.log("tuition-ledger: OK");
