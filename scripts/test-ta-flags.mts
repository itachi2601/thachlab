import assert from "node:assert/strict";
import { flagSession, type FlagSession } from "../lib/tro-giang/co-bat-thuong";

const pol = (o: object = {}) =>
  ({ attendance: "on_time", arrived_early: true, homework_checked: true, walked_tables: true, reported_students: true, ...o }) as never;
let n = 0;
const mk = (o: Partial<FlagSession> = {}): FlagSession => ({
  id: `s${n++}`, assistant_id: "a", work_date: "2026-11-02", session_type: "lop", start_time: "18:00:00", end_time: "20:00:00",
  hours: 2, student_touches: 8, created_at: "2026-11-02T15:00:00Z", policy: pol({ homework_checked: false }), ...o,
});
const codes = (s: FlagSession, h: FlagSession[], r?: number | null) => flagSession(s, h, r).map((f) => f.code);

// buổi bình thường: không cờ
let s = mk();
assert.deepEqual(codes(s, [s]), []);

// trùng giờ
s = mk(); const o = mk({ session_type: "phudao", start_time: "19:00:00", end_time: "20:30:00" });
assert.ok(codes(s, [s, o]).includes("overlap"));
assert.ok(!codes(s, [s, mk({ work_date: "2026-11-03" })]).includes("overlap"));

// ghi muộn + giờ lệch
s = mk({ created_at: "2026-11-10T01:00:00Z", hours: 3 });
assert.deepEqual(codes(s, [s]).sort(), ["hours_mismatch", "late_log"]);

// chuỗi tick đủ + 12 lượt + lặp khung giờ
const hist = [1, 2, 3, 4].map((d) => mk({ work_date: `2026-10-0${d}`, student_touches: 12, policy: pol(), created_at: `2026-10-0${d}T15:00:00Z` }));
s = hist[3];
assert.deepEqual(codes(s, hist).sort(), ["all_ticks", "same_slot", "touch_streak"]);

// buổi vắng không bị tính chuỗi
const abs = hist.map((h) => ({ ...h, policy: pol({ attendance: "excused_absence" }) }));
assert.ok(!codes(abs[3], abs).includes("all_ticks"));

// phụ đạo
s = mk({ session_type: "phudao", policy: undefined });
assert.ok(flagSession(s, [s], 0).some((f) => f.code === "no_exit_evidence" && f.level === "red"));
assert.ok(codes(s, [s], null).includes("no_topics"));
assert.ok(!codes(s, [s], 0.5).length);
assert.ok(!codes(s, [s]).length);

console.log("ta-flags: OK");
