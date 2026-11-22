// Ghi admin_note + đổi trạng thái cho báo lỗi nhóm A (12/11/2026). Chỉ UPDATE bug_reports theo id.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"));
const D = "da_xu_ly", W = "dang_xu_ly";
const rows: [number, string, string][] = [
  [144, D, "Thầy đã kiểm câu 9: đề không cho số vì đây là câu khái niệm (khí giãn nở không trao đổi nhiệt thì Q = 0 J). Thầy đã sửa lại lời hỏi cho rõ là bình cách nhiệt và dùng ΔU = A + Q. Cảm ơn em đã báo."],
  [149, D, "Thầy đã kiểm câu 14 (rơi tự do): đáp án D đúng, nhưng phương án B \"nhanh dần\" gần nghĩa với D nên em thấy như trùng. Thầy đã sửa B thành \"nhanh dần nhưng gia tốc tăng dần\" để chỉ còn một đáp án đúng. Cảm ơn em."],
  [151, D, "Thông báo \"Chưa kiểm tra được câu này\" xuất hiện khi mạng chập chờn lúc bấm Kiểm tra; đáp án em chọn vẫn được giữ. Thầy đã kiểm đề, không có lỗi. Lần sau gặp lại em chờ mạng ổn rồi bấm Kiểm tra lại nhé."],
  [153, D, "Đã sửa: câu 12 hiện nhầm \"góc 1500\", đúng phải là góc 150°. Thầy đã sửa trong đề. Cảm ơn em đã báo."],
  [154, D, "Đã sửa: các ký hiệu ở câu 4 trước đây là ảnh bị thu quá nhỏ, thầy đã đổi sang chữ công thức rõ nét. Em tải lại trang là thấy. Cảm ơn em."],
  [160, W, "Đáp án đã lưu đúng, không lỗi chấm. Nhãn \"Đúng một phần\" là em đúng một số ý; nút màu xanh chỉ là ý em đã chọn, chưa phải đáp án đúng. Thầy đã thêm dòng chú thích ở màn kết quả, sẽ lên web trong lần cập nhật tới."],
  [164, W, "Thầy đã kiểm: câu 13 của đề này thiếu 4 hình khung dây. Thầy đang bổ sung hình. Cảm ơn em đã báo."],
  [148, D, "Theo định luật 1 Newton: vật chuyển động thẳng đều thì vận tốc không đổi, tức gia tốc a = 0. Theo định luật 2, F = m·a = 0, nên hợp lực tác dụng lên vật bằng 0 N. Lực kéo và lực cản lúc đó cân bằng nhau chứ không phải là không có lực."],
];
for (const [id, status, admin_note] of rows) {
  const { error } = await sb.from("bug_reports").update({ status, admin_note, updated_at: new Date().toISOString() }).eq("id", id);
  console.log(id, status, error ? "LỖI " + error.message : "ok");
}
const { data } = await sb.from("bug_reports").select("id,status").in("id", rows.map((r) => r[0]));
console.log(JSON.stringify(data));
