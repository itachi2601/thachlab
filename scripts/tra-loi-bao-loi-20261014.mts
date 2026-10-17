// Ghi admin_note + đổi trạng thái cho báo lỗi #59–#105 còn mới (14/10/2026). Chỉ UPDATE bug_reports theo id.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const env = (k: string) => fs.readFileSync(".env.local", "utf8").split("\n").find((l) => l.startsWith(k + "="))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"));
const D = "da_xu_ly", W = "dang_xu_ly";
const AC = "Đã sửa đáp án câu 16 (AC là điện xoay chiều). Cảm ơn em đã báo.";
const DONG = "Câu hỏi hay đó em. Em cho thầy biết cụ thể câu nào, bước nào em chưa làm được nhé, thầy sẽ chỉ riêng.";
const LOP = "Thầy đã nhận. Thầy sẽ chuyển em sang lớp Tiếng Anh chuyên ngành; em chờ thầy xác nhận và đăng nhập lại để thấy lớp mới nhé. (Em báo một lần là đủ.)";
const rows: [number, string, string][] = [
  [91, D, AC],
  [93, D, AC + " Chuyện Starbucks thầy xin ghi nhận 😄."],
  [90, D, "Đúng rồi em, AC là dòng điện xoay chiều. Thầy đã sửa đáp án câu 16. Cảm ơn em."],
  [89, W, "Câu 18 (dao động điều hoà) thầy đã kiểm: đề này chưa học tới phần đó và số liệu không khớp lựa chọn nào. Thầy đang xử lý lại câu này; cảm ơn em đã báo."],
  [92, W, "Đã sửa đáp án câu 28 (là 3 m) và câu 16. Câu 18 thầy đang xử lý lại. Về điểm thưởng cho các bạn, thầy sẽ xem và báo lại ở lớp."],
  [94, D, DONG + " Đóng báo này."],
  [87, W, "Đã sửa: nút đăng lịch phụ đạo hiện ở mọi tháng. Sẽ có sau lần cập nhật tới."],
  [96, W, "Đã sửa: hộp thông báo ở chuông bị tràn mép trái trên điện thoại. Sẽ có sau lần cập nhật tới."],
  [105, D, "Đã tìm ra: làm luyện tập chưa được xét mở danh hiệu ngay (phải chờ nộp đề). Thầy đã sửa và xét bù cho các em, em vào lại trang Xếp hạng xem nhé. Nếu vẫn chưa thấy thì báo lại."],
  [97, W, "Hệ thống đúng như vậy: thi thăng hạng trượt thì chờ 48 giờ. Chữ '00:40' dễ đọc thành 40 phút nên thầy đã sửa để ghi rõ ngày giờ và thời gian còn lại, sẽ có sau lần cập nhật tới. Lần sau em làm nghiêm túc nhé 😄."],
  [95, W, "Em cho thầy biết: lúc đó em làm ở trang nào, mấy giờ bấm nộp, và đáp án bị ẩn ở câu số mấy? Bài kiểm tra cuối buổi chỉ mở trong 20 phút sau khi trợ giảng mở, nếu quá giờ sẽ không nộp được. Chụp màn hình gửi lại giúp thầy."],
  [104, W, "Đã sửa: bảng điểm danh của thầy/trợ giảng không tải lại khi bấm Làm mới. Dữ liệu em điểm danh vẫn được lưu. Sẽ có sau lần cập nhật tới; trong lúc chờ nhờ thầy/cô bấm đổi buổi rồi quay lại."],
  [88, W, "Em cho thầy biết 'không hoạt động' là chỗ nào: cả trang không mở được hay bảng đang học trống? Em dùng tài khoản gì và chụp màn hình giúp thầy."],
  [98, W, "Bài này tải chậm khi mạng yếu. Thầy ghi nhận để tối ưu. Em đang dùng wifi hay 4G?"],
  [99, D, LOP], [100, D, LOP], [101, D, LOP], [102, D, LOP], [103, D, LOP],
  [59, W, "Ý hay: kéo nam châm ra vào cuộn dây để thấy kim điện kế lệch. Thầy ghi nhận cho bài này."],
  [86, W, "Thầy ghi nhận 3 ý: hiện đáp án sau khi làm, bấm viền ngoài không nên thoát bài, và phân bố điểm cần giải thích rõ hơn."],
];
for (const [id, status, note] of rows) {
  const { error } = await sb.from("bug_reports").update({ status, admin_note: note, updated_at: new Date().toISOString() }).eq("id", id);
  console.log(id, status, error ? "LỖI " + error.message : "ok");
}
