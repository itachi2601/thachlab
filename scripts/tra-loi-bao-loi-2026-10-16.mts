import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "node:fs";
for (const l of readFileSync(".env.local", "utf8").split("\n")) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] ??= m[2].trim().replace(/^"|"$/g, ""); }
const sb = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!);
const R: [number, string, string][] = [
  [106, "da_xu_ly", "Cảm ơn em. Thầy đã gỡ hình biển điện cao áp bị gắn nhầm ở câu 3 (rơi tự do)."],
  [108, "da_xu_ly", "Cảm ơn em. Thầy đã thay hình câu 11: nền trắng, cắt bớt lề nên hình to và rõ hơn."],
  [109, "dang_xu_ly", "Cảm ơn em. Công thức hiện chữ thô thường do mạng yếu nên chưa tải xong. Thầy đã sửa để máy tự thử tải lại. Nếu em vẫn gặp ở đề này, em tải lại trang và báo thầy nhé."],
  [110, "dang_xu_ly", "Cảm ơn em. Nút mở bài thoát còn khoá vì cần đọc đủ thời gian. Thầy đã thêm lời giải thích và thanh tiến độ. Em đọc lại bài thêm một lát, nút sẽ tự mở."],
  [111, "dang_xu_ly", "Cảm ơn em. Đây cùng lỗi nút thoát phụ đạo như báo #110. Thầy đã thêm lời giải thích và thanh tiến độ; em đọc lại bài thêm một lát, nút sẽ tự mở."],
  [113, "dang_xu_ly", "Cảm ơn em. Thầy đã sửa hộp Thông báo bị lệch ra ngoài màn hình. Nếu ở mục xem lại từng câu còn lỗi khác, em cho thầy biết đó là câu nào và hiện gì nhé."],
  [114, "dang_xu_ly", "Cảm ơn con. Lỗi ô Số câu chỉ nhận 10–19 đã được sửa, con gõ được đến 50."],
  [107, "dang_xu_ly", "Em cho thầy biết rõ hơn: em làm bài nào, câu nào đã trả lời mà không được tính điểm, và em thấy điểm hiện thế nào? Em gửi thêm ảnh chụp nếu có."],
  [112, "dang_xu_ly", "Thầy thấy em có một lượt làm đề 16/10 bắt đầu nhưng chưa nộp nên chưa có kết quả. Em có bấm Nộp bài và thấy báo thành công không? Nếu có, em gửi ảnh màn hình lúc nộp cho thầy nhé."],
];
for (const [id, status, admin_note] of R) {
  const { error } = await sb.from("bug_reports").update({ status, admin_note }).eq("id", id);
  console.log(id, error ? "LỖI " + error.message : "ok " + status);
}
