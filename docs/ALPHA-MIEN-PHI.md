# Alpha test miễn phí → thu phí từ từ (chốt hướng 7/10/2026)

Khuyến nghị đã thống nhất; mục **[CẦN THẦY CHỐT]** là chỗ chỉ thầy quyết được, đừng tự điền.

## Nguyên tắc kỹ thuật
- `user_classes.status='active'` chỉ nghĩa "em đã chọn lớp", **KHÔNG** nghĩa "đã trả tiền". Khi thu phí, thêm lớp quyền riêng (gói + hạn dùng), đừng dùng `active` làm cờ trả phí.
- Ngày đăng ký: `profiles.created_at`. Nguồn đăng ký: `auth.users.raw_user_meta_data->>'signup_source'` (từ `?ref=` hoặc tên miền giới thiệu; tài khoản trước 7/10 không có).
- Nhóm alpha = `profiles.created_at` trước ngày bật thu phí → dùng để cấp ưu đãi "thành viên sáng lập".

## Phần miễn phí mãi / phần có thể thu phí (đề xuất, chờ thầy duyệt)
- Luôn miễn phí: bài lý thuyết, luyện tập cơ bản, rank/chuỗi ngày, báo lỗi/góp ý.
- Ứng viên thu phí: phụ đạo có người, chấm chữa chi tiết, đề thi thử, AI tutor (Q2/2027), sách in.
- **[CẦN THẦY CHỐT]** Nguồn thu chính: thuê bao web hay học phí lớp có thầy (sổ học phí `thpt_fee_ledger`).
- **[CẦN THẦY CHỐT]** Ngày/điều kiện kết thúc alpha (rồi ghi vào nhãn footer, ví dụ "đến hết học kỳ 1").
- **[CẦN THẦY CHỐT]** Ưu đãi thành viên sáng lập (giảm giá hay miễn phí trọn đời phần nào).

## Chỉ số để biết khi nào đủ sức thu phí
Số học sinh hoạt động mỗi tuần (có làm ≥1 bài/đề trong 7 ngày) và tỉ lệ quay lại sau 4 tuần. Đo từ bảng bài làm hiện có; chưa có truy vấn sẵn.

## Mẫu thông báo trước khi thu phí (gửi ít nhất 1 tháng trước)
> Gửi các em, ThachLab đã chạy bản alpha miễn phí từ 10/2026. Từ [ngày], phần [tên phần] sẽ có phí [mức phí]. Các em đăng ký trong giai đoạn alpha được [ưu đãi]. Bài lý thuyết và luyện tập cơ bản vẫn miễn phí. Cảm ơn các em đã góp ý để website tốt lên; mọi thắc mắc cứ nhắn thầy qua Zalo.
