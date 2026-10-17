// Ghi admin_note + trạng thái cho báo lỗi #115–#121 (17/10/2026). Chỉ UPDATE bug_reports theo id.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"));
const D = "da_xu_ly", W = "dang_xu_ly";
const rows: [number, string, string][] = [
  [115, W, "Đúng rồi em: bàn phím số trên điện thoại không có dấu trừ. Thầy đã sửa để câu có đáp án âm hiện bàn phím có dấu −, sẽ có sau lần cập nhật tới. Trong lúc chờ em chuyển sang bàn phím chữ cái, có dấu − ở đó."],
  [116, D, "Thầy kiểm tra lại thì trang chủ vẫn hiện bình thường. Ảnh em gửi là lúc web đang cập nhật nên mất giao diện. Em tải lại trang (kéo xuống để làm mới) là hết; nếu vẫn lạ thì báo lại thầy nhé."],
  [117, D, "Chào em 😄. Có gì cần báo em ghi rõ câu nào, trang nào cho thầy nhé."],
  [118, W, "Đề này không có câu kéo ảnh. Câu 6 có bảng số liệu nằm ngang, em vuốt sang phải để xem hết bảng. Em chụp màn hình chỗ em kéo không được gửi lại giúp thầy; thầy sẽ trình bày lại bảng cho dễ xem."],
  [119, D, "Đã sửa: câu này mất hình khi chuyển đề nên thầy viết lại thành câu không cần hình. Cảm ơn em đã báo."],
  [120, D, "Em nói đúng, hai phương án trùng nhau vì mất ký hiệu vectơ. Thầy đã thêm mũi tên vectơ cho phương án có vectơ (đáp án B). Cảm ơn em."],
  [121, D, "Đã sửa: câu này mất hình khi chuyển đề nên thầy viết lại thành câu không cần hình. Cảm ơn em đã báo."],
];
for (const [id, status, note] of rows) {
  const { error } = await sb.from("bug_reports").update({ status, admin_note: note, updated_at: new Date().toISOString() }).eq("id", id);
  console.log(id, status, error ? "LỖI " + error.message : "ok");
}
