// Kiểm wrapTheorySections trên 3 kiểu mốc: <h3>, <p><strong>N. …</strong></p>, chỉ <h2>.
//   npx tsx scripts/tests/theory-sections.mts
import assert from "node:assert/strict";
import { wrapTheorySections } from "../../features/lessons/theory-sections.ts";

const h3 = "<p>Mở bài</p><h3>I. Khái niệm</h3><p>a</p><h3>II. Công thức</h3><p>b</p>";
const r3 = wrapTheorySections(h3, 5);
assert.deepEqual(r3.sections.map((s) => s.heading), ["I. Khái niệm", "II. Công thức"]);
assert.equal(r3.sections[1].id, "theory-sec-5-1");
assert.ok(r3.html.startsWith("<p>Mở bài</p><div"));

const bold = "<p><strong>1. Mô hình</strong></p><p>a</p><p><strong>2. Cấu trúc</strong></p><p>Chú ý <strong>a. x</strong></p>";
const rb = wrapTheorySections(bold, 7);
assert.deepEqual(rb.sections.map((s) => s.heading), ["1. Mô hình", "2. Cấu trúc"]);

const h2 = "<h2>LÝ THUYẾT</h2><h2>I. Nam châm</h2><p>a</p><h2> II. Từ trường </h2><p>b</p>";
const r2 = wrapTheorySections(h2, 9);
assert.deepEqual(r2.sections.map((s) => s.heading), ["I. Nam châm", "II. Từ trường"]);
assert.equal(r2.sections[0].id, "theory-sec-9-0");
assert.ok(r2.html.startsWith("<h2>LÝ THUYẾT</h2><div"));
assert.equal(wrapTheorySections("<h2>LÍ  thuyết</h2><p>x</p>", 1).sections.length, 0);

// Ưu tiên: có h3 thì bỏ qua h2/bold; có bold thì bỏ qua h2.
assert.equal(wrapTheorySections("<h2>A</h2><h3>B</h3>", 1).sections.length, 1);
assert.equal(wrapTheorySections("<h2>A</h2><p><strong>1. B</strong></p>", 1).sections[0].heading, "1. B");
// Không mốc: nguyên văn.
assert.deepEqual(wrapTheorySections("<p>x</p>", 1), { html: "<p>x</p>", sections: [] });

console.log("theory-sections: OK");
