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
assert.ok(!/mất chuỗi|phạt|hết hạn/i.test(weak.body));
console.log("push message: OK");
