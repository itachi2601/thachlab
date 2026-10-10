// Ghi admin_note + đổi trạng thái cho các báo lỗi đã xử lý/cần hỏi lại (10/10/2026). Chỉ UPDATE bug_reports theo id.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"));
const D = "da_xu_ly", W = "dang_xu_ly";
const rows: [number, string, string][] = [
  [67, D, "Đã sửa: đáp án câu này là 39,9 µT (theo tan 53° ≈ 1,33 đề cho). Cảm ơn em."],
  [75, D, "Đề bị mất dấu độ nên đọc thành 200 độ. Đúng ra: nước 20 °C, miếng kim loại 200 °C. Đã sửa đề, cảm ơn em."],
  [80, D, "Đã sửa lỗi mất dấu độ (°) trong đề. Cảm ơn em."],
  [82, D, "Đã sửa lại số mũ (10⁵, 10⁶…) ở các câu bị lỗi. Cảm ơn em."],
  [76, D, "Câu đó thiếu đoạn dẫn nên không biết theo bài nào. Đã viết lại thành câu hỏi đứng một mình. Cảm ơn em."],
  [81, D, "Đã viết lại câu thiếu đoạn dẫn để làm được ngay. Cảm ơn em."],
  [77, D, "Em cho thầy biết cụ thể câu nào, sai chỗ nào nhé. Thầy đã rà cả đề và sửa các lỗi hiển thị tìm thấy. Đóng báo này."],
  [79, D, "Em cho thầy biết cụ thể câu nào, lỗi gì nhé. Thầy đã rà cả đề và sửa các lỗi hiển thị tìm thấy. Đóng báo này."],
  [78, W, "Thầy đã xem hết hình trong đề nhưng không thấy hình nhạy cảm. Em cho thầy biết là Câu số mấy, hình nào nhé?"],
  [65, W, "Đã sửa chỗ bị kẹt ở màn hình 'đang chuyển hướng', sẽ có sau lần cập nhật tới. Trong lúc chờ, em bấm vào chữ 'Tài khoản' ở thanh dưới, hoặc mở web bằng Safari/Chrome thay vì trong Zalo/Facebook nhé."],
  [66, W, "Đã sửa chỗ bị kẹt ở màn hình 'đang chuyển hướng', sẽ có sau lần cập nhật tới. Trong lúc chờ, em bấm vào chữ 'Tài khoản' ở thanh dưới, hoặc mở web bằng Safari/Chrome thay vì trong Zalo/Facebook nhé."],
  [63, W, "Em cho thầy biết: trang đăng nhập hiện gì (chữ báo lỗi nguyên văn), em dùng điện thoại gì và mở bằng Safari/Chrome hay trong Zalo? Nếu có thể chụp màn hình gửi lại giúp thầy."],
  [68, W, "Em cho thầy biết cụ thể chỗ nào bị lỗi: dải đen ở đáy màn hình, ô bị mất viền hay chỗ khác? Em dùng điện thoại gì và mở web bằng ứng dụng nào?"],
  [69, W, "Em cho thầy biết: lúc làm lại bài thoát phụ đạo, em bấm vào câu số mấy thì không gõ/chọn được? Em dùng điện thoại gì và mở bằng Safari/Chrome hay trong Zalo?"],
  [70, W, "Em muốn tính năng highlight thế nào? Ví dụ tô màu chỗ em làm sai trong lời giải, hay đánh dấu câu để xem lại sau? Em mô tả giúp thầy nhé."],
  [71, W, "Phần bài tập mẫu của bài này đôi khi tải chậm khi mạng yếu. Em thử tải lại trang (kéo xuống để làm mới) giúp thầy; em đang dùng wifi hay 4G? Nếu vẫn trống, báo lại kèm tên bài nhé."],
  [72, W, "Phần bài tập mẫu của bài này đôi khi tải chậm khi mạng yếu. Em thử tải lại trang giúp thầy; em đang dùng wifi hay 4G? Nếu vẫn trống, báo lại nhé."],
  [73, W, "Thầy ghi nhận ý kiến về chuỗi (streak) khó giữ. Em cho thầy biết cụ thể: em thường đứt chuỗi vì lý do gì (bận, quên, hay bài ngày đó khó)? Em muốn chuỗi tính thế nào cho hợp lý?"],
  [74, W, "Thầy chưa hiểu rõ ý. Em/phụ huynh cho thầy biết: tài khoản của con đang ở lớp nào, và cần chuyển sang lớp nào (ví dụ lớp HSG Vật lý 9)? Gửi tên đầy đủ của con để thầy kiểm tra."],
  [83, W, "Em muốn chuyển sang lớp chuyên/HSG nào (môn, khối)? Em cho thầy biết tên đầy đủ và lớp hiện tại để thầy xét nhé."],
  [84, W, "Đã tìm ra nguyên nhân (tài khoản trợ giảng chưa được phép đổi ảnh) và đã sửa, sẽ có sau lần cập nhật tới. Học sinh đổi ảnh bình thường."],
  [85, W, "Đã làm: trợ giảng sửa được buổi chưa duyệt trong 7 ngày kể từ ngày làm, quá hạn thì khoá. Sẽ có sau lần cập nhật tới."],
];
for (const [id, status, note] of rows) {
  const { error } = await sb.from("bug_reports").update({ status, admin_note: note, updated_at: new Date().toISOString() }).eq("id", id);
  console.log(id, status, error ? "LỖI " + error.message : "ok");
}
