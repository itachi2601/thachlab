// Test thư viện biến thể đổi số: npx tsx scripts/test-bien-the.mts
import assert from "node:assert/strict";
import { checkTemplate, evaluate, formatNum, generate, gradeNumeric, mulberry32, parseExpr, roundSpec, tryOnce } from "../lib/bien-the";
import type { WorkedVariant } from "../features/lessons/types";

const close = (a: number, b: number) => assert.ok(Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(b)), `${a} ≠ ${b}`);

// — Biểu thức: thứ tự phép tính, ^ kết hợp phải, trừ một ngôi
close(evaluate("1 + 2 * 3", {}), 7);
close(evaluate("2 ^ 3 ^ 2", {}), 512);
close(evaluate("-2 ^ 2", {}), -4);
close(evaluate("2 ^ -1", {}), 0.5);
close(evaluate("(1 + 2) * 3", {}), 9);
close(evaluate("6.022e23 / 6.022E23", {}), 1);
close(evaluate("N0 * 2 ^ (-t / T)", { N0: 8, t: 276, T: 138 }), 2);
close(evaluate("T * log2(h0 / h)", { T: 5730, h0: 0.226, h: 0.113 }), 5730);
close(evaluate("sin(30) + cos(60)", {}), 1);
close(evaluate("round(3.14159, 2)", {}), 3.14);
close(evaluate("max(1, 5, 3) - min(4, 2)", {}), 3);
close(evaluate("sqrt(2 * 9.8 * 5)", {}), Math.sqrt(98));
close(evaluate("pi", {}), Math.PI);
// so sánh & logic trả 1/0
assert.equal(evaluate("3 > 2 && 2 >= 2", {}), 1);
assert.equal(evaluate("3 < 2 || 1 == 2", {}), 0);
assert.equal(evaluate("!(1 != 1)", {}), 1);
assert.equal(evaluate("0.1 + 0.2 == 0.3", {}), 1);
// không phải eval: chuỗi lạ bị chặn
assert.throws(() => parseExpr("alert(1)"), /hàm lạ/);
assert.throws(() => parseExpr("constructor.constructor('x')()"), /ký tự lạ|hàm lạ|thừa/);
assert.throws(() => parseExpr("1 +"), /cụt/);
assert.throws(() => parseExpr("(1 + 2"), /thiếu/);
assert.throws(() => evaluate("x + 1", {}), /biến chưa có/);
assert.throws(() => parseExpr("log2(1, 2)"), /đối số/);
// không đi qua prototype
assert.throws(() => evaluate("constructor", {}), /biến chưa có/);
assert.throws(() => parseExpr("toString(1)"), /hàm lạ/);

// — Làm tròn & in số kiểu đề Việt Nam
assert.equal(formatNum(6.4e18, { cs: 3 }), "6{,}4.10^{18}");
assert.equal(formatNum(4.0e17, { cs: 3 }), "4.10^{17}");
assert.equal(formatNum(9.996e17, { cs: 3 }), "10^{18}");
assert.equal(formatNum(4.17e-9, { cs: 3 }), "4{,}17.10^{-9}");
assert.equal(formatNum(9455.3, { cs: 3 }), "9460");
assert.equal(formatNum(2.2097, { tp: 1 }, false), "2,2");
assert.equal(formatNum(1130.4, { tp: 0 }, false), "1130");
assert.equal(formatNum(-0.04, { tp: 1 }, false), "0");
assert.equal(formatNum(93.75, { cs: 3 }), "93{,}8");
assert.equal(roundSpec(0.0123456, { cs: 2 }), 0.012);
assert.equal(roundSpec(123456, { cs: 2 }), 120000);

// — Seed: cùng seed cùng dãy
const r1 = mulberry32(42), r2 = mulberry32(42);
for (let i = 0; i < 5; i++) assert.equal(r1(), r2());

// — Khuôn mẫu nhỏ: số hạt còn lại
const v: WorkedVariant = {
  de: "<p>$N_0={{N0}}$, $T={{T}}$ ngày, sau $t={{t}}$ ngày còn bao nhiêu hạt?</p>",
  bien: { a: { min: 1, max: 9.9, buoc: 0.1 }, n: { min: 2, max: 5, buoc: 1 } },
  bo: [{ T: 138, ten: "poloni" }, { T: 8, ten: "iốt" }],
  tinh: { N0: "a * 10^18", t: "n * T" },
  dap_so: "N0 * 2^(-t / T)",
  don_vi: "hạt",
  kieu: "abcd",
  nhieu: [
    { bieu_thuc: "N0 / n", loi: "chia cho n", buoc: 1 },
    { bieu_thuc: "N0 - dap_so", loi: "số đã phân rã", buoc: 1 },
    { bieu_thuc: "N0 * 2^(-T / t)", loi: "chia ngược", buoc: 0 },
  ],
  rang_buoc: ["dap_so > 0"],
  loi_giai: "$N={{dap_so}}$ hạt",
};
assert.deepEqual(checkTemplate(v), []);
const q = generate(v, 7);
assert.ok(q && q.question.type === "multiple_choice");
if (q && q.question.type === "multiple_choice") {
  assert.equal(q.question.options.length, 4);
  assert.equal(new Set(q.question.options).size, 4);
  close(q.exact, q.scope.N0 * 2 ** -q.scope.n);
  assert.equal(q.stepByOption?.[q.question.answer], undefined);
  assert.equal(Object.keys(q.question.distractorNotes ?? {}).length, 3);
  assert.ok(!q.question.question.includes("{{"));
}
// cùng seed → cùng câu
assert.deepEqual(generate(v, 7), generate(v, 7));

// Kiểm tĩnh bắt lỗi soạn khuôn
const bad: WorkedVariant = { ...v, de: "N = {{N0}} và {{zz}}", dap_so: "N0 * q", nhieu: v.nhieu!.slice(0, 2) };
const errs = checkTemplate(bad);
assert.ok(errs.some((e) => e.includes("ngoài $")));
assert.ok(errs.some((e) => e.includes("{{zz}}")));
assert.ok(errs.some((e) => e.includes('"q"')));
assert.ok(errs.some((e) => e.includes("≥ 3")));

// Phương án trùng bị loại: n = 1,5 → N0/n và N0 − N lệch < 5 %
const near: WorkedVariant = { ...v, bien: { a: { min: 4, max: 4, buoc: 1 }, n: { min: 1.5, max: 1.5, buoc: 0.5 } } };
const rn = tryOnce(near, 1);
assert.ok(!rn.ok && rn.loi.includes("trùng"), JSON.stringify(rn));

// — Ô đáp số: ≤ 4 ký tự + sai số
const s: WorkedVariant = {
  de: "<p>$H_0={{H0}}$ Ci, sau $t={{t}}$ năm?</p>",
  bien: { H0: { min: 1000, max: 1000, buoc: 1 }, t: { min: 5.27, max: 5.27, buoc: 0.01 } },
  dap_so: "H0 * 2^(-t / 5.27)",
  lam_tron: { tp: 0 },
  kieu: "so",
  sai_so: 0.01,
};
const qs = generate(s, 1)!;
assert.equal(qs.question.type === "short_answer" && qs.question.answer, "500");
assert.deepEqual(gradeNumeric("500", qs, s), { dung: true, khopChuoi: true });
assert.equal(gradeNumeric("504", qs, s).dung, true); // trong 1 % + 0,5
assert.equal(gradeNumeric("506", qs, s).dung, false);
assert.equal(gradeNumeric("", qs, s).dung, false);
assert.equal(gradeNumeric("abc", qs, s).dung, false);
assert.equal(gradeNumeric("5e2", qs, s).dung, false);
// ràng buộc ném lỗi → bốc lại, không văng ngoại lệ
assert.equal(generate({ ...s, rang_buoc: ["zz > 0"] }, 1), null);
const long: WorkedVariant = { ...s, lam_tron: { tp: 2 } }; // "500" → "500" vẫn 3 ký tự; ép dài:
const r = tryOnce({ ...long, dap_so: "12345.678" }, 1);
assert.ok(!r.ok && r.loi.includes("4 ký tự"));

console.log("test-bien-the: tất cả đạt");
