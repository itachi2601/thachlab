// Điền cột lessons.description ("yêu cầu cần đạt") cho 18 bài THPT (lớp 10/11/12) + 2 bài
// KHTN 9 còn trống, dựa theo hai văn bản: "Yêu cầu cần đạt chương trình GDPT 2018 - môn Vật lí"
// (PDF thầy gửi 22/9/2026) và "Chương trình GDPT 2018 - môn Khoa học tự nhiên" (PDF thầy gửi
// cùng ngày, mục Lớp 9 - Ánh sáng, tr.60-61). Văn phong giữ ngắn gọn, cụm danh từ, giống các
// bài đã có description sẵn.
//
// Không đụng tới: các bài đã có description, các mục "Kiểm tra chương"/"Kiểm tra giữa học kì"
// (không phải bài học có YCCĐ riêng).
//
//   SUPABASE_SERVICE_ROLE_KEY=xxx NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co \
//     node scripts/backfill-lessons-description-thpt.mjs
//
// Chạy lại an toàn: chỉ ghi đè đúng 18 id liệt kê bên dưới, không đụng bài khác.

import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY.");
  process.exit(1);
}
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

const DESCRIPTIONS = {
  // Lớp 10
  46: "Đối tượng nghiên cứu và mục tiêu môn Vật lí; Ảnh hưởng của vật lí với khoa học, công nghệ, kĩ thuật; Ví dụ vật lí ứng dụng trong nhiều lĩnh vực",
  49: "Tốc độ trung bình và tốc độ theo một phương; Định nghĩa độ dịch chuyển từ ví dụ thực tiễn; So sánh quãng đường đi được và độ dịch chuyển",
  51: "Thiết kế phương án đo tốc độ bằng dụng cụ thực hành; So sánh ưu, nhược điểm của các phương pháp đo tốc độ",
  53: "Sự biến đổi vận tốc và định nghĩa gia tốc; Đơn vị, ý nghĩa của gia tốc; Chuyển động nhanh dần, chậm dần",
  56: "Thiết kế phương án đo gia tốc rơi tự do bằng dụng cụ thực hành; Xử lí số liệu thí nghiệm",
  59: "Phát biểu định luật 1 Newton; Quán tính của vật; Ví dụ minh hoạ trong thực tế",
  61: "Phát biểu định luật 3 Newton; Cặp lực và phản lực; Vận dụng trong một số tình huống thực tế",
  64: "Lực cản của không khí và của nước; Lực nâng tác dụng lên vật trong nước hoặc không khí; Ảnh hưởng của hình dạng vật đến lực cản",
  65: "Vận dụng ba định luật Newton và các lực cơ học để giải bài toán động lực học tổng hợp",
  67: "Thiết kế phương án tổng hợp hai lực đồng quy; Tổng hợp hai lực song song bằng dụng cụ thực hành",
  75: "Đo tốc độ vật trước và sau va chạm; Xác định, đánh giá động lượng của vật trước và sau va chạm bằng dụng cụ thực hành",
  // Lớp 11
  20: "Thí nghiệm tạo dao động và ví dụ về dao động tự do; Đồ thị li độ – thời gian dạng sin; Phương trình a = –ω²x của dao động điều hoà",
  23: "Vận dụng các đại lượng và phương trình dao động điều hoà để giải bài tập tổng hợp",
  26: "Vận dụng động năng, thế năng và định luật bảo toàn cơ năng trong dao động điều hoà để giải bài tập",
  29: "Thiết kế phương án đo tần số sóng âm bằng dao động kí hoặc dụng cụ thực hành",
  38: "Thế năng của điện tích trong điện trường đặc trưng cho khả năng sinh công; Công của lực điện khi điện tích dịch chuyển",
  45: "Thiết kế phương án đo suất điện động và điện trở trong của pin hoặc acquy bằng dụng cụ thực hành",
  // Lớp 12
  12: "Thiết kế phương án đo cảm ứng từ bằng cân \"dòng điện\"",
  // Lớp 9 (KHTN)
  87: "Đo tiêu cự của thấu kính hội tụ bằng dụng cụ thực hành; Vẽ sơ đồ tỉ lệ để giải bài tập thấu kính hội tụ",
  88: "Cấu tạo và cách sử dụng kính lúp; Vận dụng vẽ ảnh qua thấu kính để giải bài tập thấu kính hội tụ",
};

async function main() {
  const ids = Object.keys(DESCRIPTIONS).map(Number);
  const { data: before, error: readErr } = await supabase
    .from("lessons")
    .select("id, title, description")
    .in("id", ids);
  if (readErr) {
    console.error("Lỗi đọc lessons:", readErr.message);
    process.exit(1);
  }
  const nonEmpty = (before ?? []).filter((l) => l.description?.trim());
  if (nonEmpty.length) {
    console.log("Các bài đã có description (sẽ bị ghi đè):", nonEmpty.map((l) => `${l.id} ${l.title}`));
  }

  let ok = 0;
  for (const id of ids) {
    const { error } = await supabase.from("lessons").update({ description: DESCRIPTIONS[id] }).eq("id", id);
    if (error) {
      console.error(`Lỗi cập nhật bài ${id}:`, error.message);
      continue;
    }
    ok += 1;
  }
  console.log(`Đã cập nhật ${ok}/${ids.length} bài.`);
}

main();
