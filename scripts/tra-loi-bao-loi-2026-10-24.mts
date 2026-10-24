// Ghi admin_note + đổi trạng thái cho báo lỗi 24/10/2026. Chỉ UPDATE bug_reports theo id.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"));
const D = "da_xu_ly", W = "dang_xu_ly";
const rows: [number, string, string][] = [
  [141, D, "Em đúng rồi: đáp án D (nhiệt không thể tự truyền từ vật nhiệt độ thấp sang vật nhiệt độ cao hơn) mới đúng, hệ thống lưu nhầm là C. Thầy đã sửa đáp án và lời giải. Cảm ơn em đã báo."],
  [135, D, "Thầy đã kiểm: đáp án câu 20 là 660 °C (nhôm nóng chảy ở khoảng 660 °C, bài lý thuyết cũng ghi vậy), còn em điền 880 nên bị tính sai. Câu không lỗi hiển thị. Nếu em thấy cách hỏi chưa rõ thì báo lại thầy nhé."],
  [142, D, "Thầy đã kiểm câu 7 (thang Kelvin): đáp án a) Đúng, b) Sai, c) Đúng, d) Sai là chính xác. Ở màn xem lại, dấu ✓ nằm ở ô em đã chọn chứ không phải ô đáp án đúng; ô xanh mới là đáp án đúng. Thầy sẽ xem lại cách hiển thị cho dễ hiểu hơn."],
  [123, W, "Thầy chưa thấy chỗ thiếu dấu vectơ ở câu 12 (đề hỏi độ lớn nên không cần vectơ, lời giải đã có \\vec). Em nói rõ giúp thầy: dấu vectơ thiếu ở chữ nào (đề, phương án hay lời giải)? Chụp màn hình gửi thầy càng tốt."],
  [136, W, "Thầy đã đối chiếu 5 câu đúng/sai của đề này, ý a đều khớp lời giải. Em cho thầy biết là câu số mấy và em thấy đáp án hiện là Đúng hay Sai, lời giải ghi gì, để thầy tra đúng chỗ nhé."],
  [125, W, "Thầy thấy câu 8 và 9 của đề này thiếu mô tả thí nghiệm. Em cho thầy biết câu nào hình/chữ hiện sai (kèm ảnh chụp, thiết bị, trình duyệt) để thầy sửa đúng chỗ."],
  [124, W, "Thầy cần thêm thông tin: em dùng máy gì, trình duyệt nào, đề nào và câu mấy bị mất hình/công thức? Em chụp màn hình gửi thầy giúp nhé."],
  [126, W, "Thầy chưa tái hiện được. Em bấm vào mục nào ở trang tài khoản thì bị tắt, trên điện thoại hay máy tính? Em mô tả hoặc quay màn hình gửi thầy giúp."],
  [127, W, "Em không chọn được gì ở bài blog này (nút, đáp án hay chữ)? Em cho thầy biết thiết bị và trình duyệt để thầy kiểm tra."],
  [134, W, "Thầy cần thêm: trên Mac Pro 2019 em dùng trình duyệt gì, và khi gửi báo lỗi thì có hiện thông báo gì không? Với hình/ký hiệu căn, độ không hiện: đề nào, câu mấy? Em gửi ảnh chụp giúp thầy."],
  [138, W, "Thầy chưa hiểu ý em. Em nói rõ giúp: 'tư duy nhanh' ở bài này chỗ nào bị cho là sai lầm?"],
];
for (const [id, status, admin_note] of rows) {
  const { error } = await sb.from("bug_reports").update({ status, admin_note, updated_at: new Date().toISOString() }).eq("id", id);
  console.log(id, status, error ? "LỖI " + error.message : "ok");
}
const { data } = await sb.from("bug_reports").select("id,status").in("id", rows.map((r) => r[0]));
console.log(JSON.stringify(data));
