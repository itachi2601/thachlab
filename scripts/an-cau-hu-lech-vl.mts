// Ẩn các câu lệch (lô chưa có kq trong lech-vl, trừ lô 13 đang chạy batch) mà ghi chú của Sonnet báo ĐỀ hư/lỗi.
//   npx tsx scripts/an-cau-hu-lech-vl.mts   → in thống kê + ghi lech-vl/an-hu.sql, an-hu-giu.txt (câu giữ lại, để soát)
import fs from "node:fs";
const D = "scripts/data/giai-lai/lech-vl/";
const HU = /mất \^|mất ký|mất dấu|dính|lẫn|rác|trùng nhau|mơ hồ|không liên quan|không khớp|thiếu (dữ|ảnh|hình|bài|đề|ký|phương|ý)|không nêu|không nói|không ghi|không có (hình|ảnh|bài|dữ)|lỗi (chép|chuyển|ký|đề)|hình (không|thiếu)|ảnh (không|thiếu|đi kèm)|tham chiếu bài đọc|nên xoá|sai đề|đề (sai|lỗi|thiếu)|cần (bổ sung|sửa|xoá)|không rõ|hiểu là|đọc ước lượng|vỡ|hỏng|giống hệt|sửa ngầm|lỗi phân số|in nhầm|không có trong|mất giá trị|ghi nhầm|ghi sai|không tự kiểm|không mô tả|không nhất quán|bất thường|đơn vị ở ý/i;
const an: number[] = [], giu: string[] = [];
for (let i = 1; i <= 43; i++) {
  const s = String(i).padStart(2, "0");
  if (i === 13 || fs.existsSync(`${D}kq-${s}.json`)) continue;
  for (const x of JSON.parse(fs.readFileSync(`${D}lo-${s}.json`, "utf8"))) {
    const gc: string = x.sonnet?.ghi_chu ?? "";
    if (x.ly_do_lech === "Sonnet khớp đáp án nhưng có ghi chú" && HU.test(gc)) an.push(x.id);
    else giu.push(`${x.id} | ${x.ly_do_lech} | ${gc.slice(0, 140)}`);
  }
}
const note = "19/10/2026: câu lỗi/đề hư — ghi chú giải lại báo đề mất ký tự/dính/mơ hồ, không đáng sửa (lech-vl)";
fs.writeFileSync(D + "an-hu.sql", `begin;\n${an.map((id) => `update public.question_bank set archived = true, note = coalesce(note || ' | ', '') || $q$${note}$q$ where id = ${id} and archived = false;`).join("\n")}\ncommit;\n`);
fs.writeFileSync(D + "an-hu-ids.json", JSON.stringify(an));
fs.writeFileSync(D + "an-hu-giu.txt", giu.join("\n"));
console.log(`ẩn ${an.length} · giữ ${giu.length}`);
