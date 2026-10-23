// Ghi admin_note + đổi trạng thái cho báo lỗi #128, #130, #137 (23/10/2026). Chỉ UPDATE bug_reports theo id.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"));
const D = "da_xu_ly";
const rows: [number, string, string][] = [
  [128, D, "Thầy đã sửa lỗi đáp án đúng hiện một lúc rồi biến mất ở bước xem lại lý thuyết; bản sửa đã lên ngày 23/10. Em mở lại bài, bấm xem đáp án thử giúp thầy, nếu còn nhảy mất thì báo lại nhé."],
  [130, D, "Thầy đã sửa: thông báo lên hạng/danh hiệu chỉ hiện khi em vượt mốc cao nhất đã được chúc mừng, rank tụt rồi lên lại không hiện lại nữa. Bản sửa đã lên ngày 23/10. Nếu vẫn còn hiện lặp thì báo thầy kèm tên em và trình duyệt đang dùng."],
  [137, D, "Em đúng rồi: đề không nêu cùng nhiệt độ thì ý c phải xét lại. Thầy đã thêm 'ở cùng nhiệt độ' vào đề (đáp án giữ Đúng). Cảm ơn em đã báo."],
];
for (const [id, status, admin_note] of rows) {
  const { error } = await sb.from("bug_reports").update({ status, admin_note, updated_at: new Date().toISOString() }).eq("id", id);
  console.log(id, status, error ? "LỖI " + error.message : "ok");
}
const { data } = await sb.from("bug_reports").select("id,status").in("id", rows.map((r) => r[0]));
console.log(JSON.stringify(data));
