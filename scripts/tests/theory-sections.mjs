// Kiểm wrapTheorySections: npx tsx scripts/tests/theory-sections.mjs
import assert from "node:assert/strict";
import { stripAuthoredDuration, wrapTheorySections } from "../../features/lessons/theory-sections.ts";

// h3
const h3 = wrapTheorySections("<p>mở</p><h3>I. A</h3><p>a</p><h3>II. B</h3><p>b</p>", 7);
assert.deepEqual(h3.sections.map((s) => s.heading), ["I. A", "II. B"]);
assert.equal(h3.sections[1].id, "theory-sec-7-1");
assert.ok(h3.html.startsWith("<p>mở</p><div"));

// bold-numbered
const bold = wrapTheorySections("<p><strong>1. Mô hình</strong></p><p>x</p><p><strong>2. Cấu trúc</strong></p><p>y</p>", 8);
assert.deepEqual(bold.sections.map((s) => s.heading), ["1. Mô hình", "2. Cấu trúc"]);

// h2-only: bỏ "LÝ THUYẾT" chung, kể cả viết thường/có khoảng trắng/LÍ
const h2 = wrapTheorySections(
  "<h2>LÝ THUYẾT</h2><p>a</p><h2>I. Nam châm</h2><p>b</p><h2> lí  thuyết </h2><h2>II. Từ trường</h2><p>c</p>",
  10,
);
assert.deepEqual(h2.sections.map((s) => s.heading), ["I. Nam châm", "II. Từ trường"]);
assert.equal(h2.sections[0].id, "theory-sec-10-0");
assert.ok(h2.html.startsWith("<h2>LÝ THUYẾT</h2><p>a</p><div"));

// h3 thắng h2; không mốc → 0 đoạn
assert.equal(wrapTheorySections("<h2>I. X</h2><h3>a</h3>", 1).sections.length, 1);
assert.equal(wrapTheorySections("<h2>LÝ THUYẾT</h2><p>x</p>", 1).sections.length, 0);
assert.equal(wrapTheorySections("<p>x</p>", 1).html, "<p>x</p>");

const kept = stripAuthoredDuration("<p>Khoảng cách giữa hai mốc là 10 cm. Khoảng chênh 10 °C.</p>");
assert.equal(kept, "<p>Khoảng cách giữa hai mốc là 10 cm. Khoảng chênh 10 °C.</p>");
const stripped = stripAuthoredDuration(
  "<p>Cuối bài, em phải tự trả lời được <strong>6 câu ở mục Trả bài</strong>. Khoảng 17 phút · 6 mục · 6 câu tự kiểm tra.</p>",
);
assert.equal(
  stripped,
  "<p>Cuối bài, em phải tự trả lời được <strong>6 câu ở mục Trả bài</strong>.</p>",
);
const dashed = stripAuthoredDuration(
  "<p>Cuối bài, em tự trả lời được <strong>6 câu</strong> — khoảng 15 phút · 8 câu tự kiểm tra.</p>",
);
assert.equal(dashed, "<p>Cuối bài, em tự trả lời được <strong>6 câu</strong></p>");
console.log("theory-sections: OK");
