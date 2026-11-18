---
name: project_thachlab_tap_luyen
description: Chương trình gym A/B/C tăng ngực–vai (18/11/2026) + ứng dụng tập kiểu Hevy ở /suc-khoe/tap-luyen
metadata:
  type: project
---

**Mục tiêu thầy chốt 18/11/2026:** 1m60 · 53 kg · 82–72–85 → eo đã gọn (eo/cao 0,45), điểm yếu là ngực/eo 1,14 và ngực < mông. Tăng ngực + vai, KHÔNG giảm eo/mỡ thêm; ăn nhỉnh hơn duy trì; đo lại mỗi 4 tuần; mục tiêu ngực +3–4 cm, eo giữ 72.

**Chương trình** (`lib/tap-luyen/chuong-trinh.ts`, tóm tắt cho lịch tuần ở `.claude/skills/lich-tuan/references/lich-co-dinh.json` → `noi_dung_tap.gym` — sửa CẢ HAI): A Thân trên ngực–vai (25 hiệp, buổi trọng tâm), B Chân + ngực/vai phụ, C Toàn thân + sức bật. Tuần ≈ ngực 15 hiệp, vai 17 (vai giữa ~10), lưng 10. Tăng tạ double progression.

**Ứng dụng** `/suc-khoe/tap-luyen` (trong mục Sức khỏe `/suc-khoe` — đường vào: menu tài khoản, "Thêm" trên điện thoại, thẻ tài khoản giảng viên; địa chỉ cũ tự chuyển; link + "Mở ứng dụng tập →" ở mục gym trong Lịch tuần, `?buoi=A|B|C`): Tập (bắt đầu A/B/C/tự do, cột Lần trước, tick hiệp → đếm giờ nghỉ rung/bíp, gợi ý tăng tạ, thay/thêm/đổi thứ tự bài), Lịch sử, Tiến bộ (1RM Epley theo bài, hiệp/tuần theo nhóm cơ), Số đo (tỉ lệ BMI, eo/cao, eo/mông, ngực/eo, ngực−mông; mục tiêu 4 tuần; biểu đồ). Buổi đang tập giữ localStorage; lỗi mạng → hàng chờ tự gửi lại.

**Chưa có:** sửa chương trình ngay trong app (đang sửa trong code), siêu hiệp (superset), chia sẻ buổi. Đã deploy 18/11 ~23:00. Chưa ghi buổi tập thật trên điện thoại.

**Mục Sức khỏe `/suc-khoe` (19/11/2026):** trang đường vào (thẻ Hôm nay: buổi nên tập tiếp + tuần x/3 + ngực/eo + ngày đo lại; lưới mô-đun; lộ trình thành môn). Mô-đun + vai trò được mở khai báo ở `lib/suc-khoe/modules.ts` (`SUC_KHOE_ROLES` = admin, instructor; HS vào thấy "đang thử nghiệm"). Dinh dưỡng, Giấc ngủ & hồi phục, Bài học: "Sắp có". Khi thành môn HS: Số đo cơ thể KHÔNG mở cho HS (`forStudents:false`), tập theo bài thể lực, không xếp hạng cân/vóc dáng.
