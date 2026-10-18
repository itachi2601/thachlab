import assert from "node:assert/strict";
import { buildPushPayload } from "../supabase/functions/send-daily-push/message";

const weak = buildPushPayload({ topic_name: "Lực ma sát nghỉ", level: "weak" });
assert.equal(weak.body, "Em còn 🔴 Lực ma sát nghỉ — 5 phút?");
assert.equal(buildPushPayload({ topic_name: "Công suất", level: "practicing" }).body, "Em còn 🟡 Công suất — 5 phút?");
assert.equal(buildPushPayload({ topic_name: null, level: null }).body, "Hôm nay luyện 5 phút nhé?");
assert.equal(buildPushPayload({ topic_name: "  ", level: "weak" }).body, "Hôm nay luyện 5 phút nhé?");
const long = buildPushPayload({ topic_name: "x".repeat(200), level: "weak" });
assert.ok(long.body.length < 90 && long.body.includes("…"));
assert.equal(weak.url, "/lop-hoc/");
// luân phiên: 3 seed liên tiếp cho 3 mẫu khác nhau, không lặp liền nhau
const bodies = [0, 1, 2].map((seed) => buildPushPayload({ topic_name: "Công suất", level: "weak", seed }).body);
assert.equal(new Set(bodies).size, 3);
// lâu chưa học: đổi giọng, không nhắc chủ đề yếu
assert.ok(buildPushPayload({ topic_name: "Công suất", level: "weak", inactive_days: 5 }).body.startsWith("Lâu rồi"));
assert.ok(buildPushPayload({ topic_name: "Công suất", level: "weak", inactive_days: 8 }).body.includes("chờ em"));
for (const seed of [0, 1, 2]) for (const idle of [0, 5, 8]) {
  const b = buildPushPayload({ topic_name: "Công suất", level: "weak", seed, inactive_days: idle }).body;
  assert.ok(!/mất chuỗi|phạt|hết hạn|bỏ rơi/i.test(b), b);
}
console.log("push message: OK");
