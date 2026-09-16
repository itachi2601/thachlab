// Kiểm nhãn chủ đề của đề: node scripts/tests/exam-tags.mjs
import assert from "node:assert/strict";
import {
  auditQuestionTags,
  canonicalizeQuestionTopics,
  tagsComplete,
  topicKey,
} from "../../features/exams/types.ts";

const mc = (topic, form) => ({
  type: "multiple_choice",
  topic,
  form,
  question: "?",
  options: ["a", "b", "c", "d"],
  answer: 0,
  explanation: "",
});

const catalog = ["Nội năng. Định luật 1 của nhiệt động lực học", "Thang nhiệt độ. Nhiệt kế"];

// khoá so khớp: gom khoảng trắng + bỏ qua hoa/thường
assert.equal(topicKey("  Nội  NĂNG "), "nội năng");

// đủ nhãn, tên lệch hoa/thường vẫn tính là có trong danh mục
const ok = auditQuestionTags(
  [mc(" nội năng.  Định luật 1 của nhiệt động lực học ", "ly_thuyet"), mc("Thang nhiệt độ. Nhiệt kế", "bai_tap")],
  catalog,
);
assert.deepEqual(ok.missingTopic, []);
assert.deepEqual(ok.missingForm, []);
assert.equal(ok.tagged, 2);
assert.equal(ok.unknown.length, 0);
assert.deepEqual(
  ok.known.map((t) => t.name),
  ["Nội năng. Định luật 1 của nhiệt động lực học", "Thang nhiệt độ. Nhiệt kế"],
);
assert.equal(tagsComplete(ok), true);

// thiếu nhãn + chủ đề ngoài danh mục
const bad = auditQuestionTags(
  [mc("", "ly_thuyet"), mc("Chủ đề lạ", ""), mc("Chủ đề lạ", "bai_tap")],
  catalog,
);
assert.deepEqual(bad.missingTopic, [1]);
assert.deepEqual(bad.missingForm, [2]);
assert.equal(bad.tagged, 1);
assert.deepEqual(bad.unknown, [{ name: "Chủ đề lạ", count: 2 }]);
assert.equal(tagsComplete(bad), false);

// đề rỗng không được coi là "đủ nhãn"
assert.equal(tagsComplete(auditQuestionTags([], catalog)), false);

// không có danh mục -> mọi chủ đề là "chưa có trong danh mục", không crash
const noCat = auditQuestionTags([mc("Nội năng", "bai_tap")], []);
assert.deepEqual(noCat.unknown, [{ name: "Nội năng", count: 1 }]);

// chuẩn hoá chính tả theo danh mục, giữ nguyên tên lạ và câu không nhãn
const fixed = canonicalizeQuestionTopics(
  [mc("  nội năng.  định luật 1 của nhiệt động lực học", "ly_thuyet"), mc("Chủ đề lạ", "bai_tap"), mc("", "bai_tap")],
  catalog,
);
assert.equal(fixed[0].topic, "Nội năng. Định luật 1 của nhiệt động lực học");
assert.equal(fixed[1].topic, "Chủ đề lạ");
assert.equal(fixed[2].topic, "");

// hai tầng: gắn ở mức cả bài trong khi bài đã có yêu cầu cần đạt -> nhắc, không chặn
const twoLevel = [
  "Nội năng. Định luật 1 của nhiệt động lực học",
  "Vận dụng ΔU = A + Q",
  "Thang nhiệt độ. Nhiệt kế",
];
const coarseNames = ["Nội năng. Định luật 1 của nhiệt động lực học"];
const mixed = auditQuestionTags(
  [
    mc("Nội năng. Định luật 1 của nhiệt động lực học", "ly_thuyet"),
    mc("Vận dụng ΔU = A + Q", "bai_tap"),
    mc("Thang nhiệt độ. Nhiệt kế", "ly_thuyet"),
  ],
  twoLevel,
  coarseNames,
);
assert.deepEqual(mixed.coarse, [
  { name: "Nội năng. Định luật 1 của nhiệt động lực học", count: 1 },
]);
assert.equal(mixed.unknown.length, 0);
assert.equal(tagsComplete(mixed), true); // nhãn thô vẫn đăng được

// không truyền coarseNames -> không nhắc gì (tương thích ngược)
assert.deepEqual(auditQuestionTags([mc("Thang nhiệt độ. Nhiệt kế", "ly_thuyet")], twoLevel).coarse, []);

console.log("✓ exam-tags: 17 phép kiểm đều đạt");
