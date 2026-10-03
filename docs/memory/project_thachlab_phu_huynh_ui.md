# UI phụ huynh (45–60 tuổi) — bộ quy tắc P + trang /phu-huynh

**Cập nhật 3/10/2026 (đợt 2, sau phản biện — xem §9 của quy tắc):** thêm P22–P27 — "Sắp tới", điểm danh, học phí,
mục tiêu điểm 7/8/9 (localStorage), xếp loại Giỏi/Khá/TB thay "Đạt 6,5", biểu đồ cột có số thay chuỗi số, "so với
cả lớp" tuỳ chọn theo dải, gợi ý cách hỏi con, xưng "phụ huynh", thẻ "Tin Zalo cho phụ huynh" trong hồ sơ HS của
thầy. Migration `20261003130000` CHỜ CHẠY (mở khoá điểm danh + sửa lỗi cũ: phụ huynh không đọc được "Bài tập về
nhà"). Treo: phỏng vấn 5–8 phụ huynh thật (mọi giả thuyết văn hoá còn `[SUY LUẬN]`), Zalo OA/ZNS tự gửi,
OTP đăng nhập, ngày kiểm tra trong DB.

**Trạng thái 3/10/2026 (đợt 1):** đã code xong trang khách + bố cục trang đã đăng nhập; chưa có ảnh nghiệm thu
trang đã đăng nhập (cần tài khoản phụ huynh thật); 7 việc treo ở §6 của quy tắc.

## Hai file phải đọc
- `docs/QUY-TAC-THIET-KE-PHU-HUYNH.md` — **quy tắc P1..P21** cho mọi màn hình phụ huynh nhìn thấy, bảng
  khác biệt so với bộ quy tắc học sinh, cấu trúc trang, bảng đo trước/sau, checklist 10 điểm.
- `docs/NGHIEN-CUU-PHU-HUYNH-45-60.md` — nghiên cứu nền 26 nguồn (thị giác, nhận thức, tâm lý, Zalo);
  mọi khẳng định gắn nhãn `[ĐO]` / `[SUY LUẬN]` / `[CHƯA CÓ NGUỒN]`.

## 8 con số dễ nhớ
- Thân bài **18px**, nhãn phụ **15px**, không có chữ nào dưới 15px cho câu cần đọc (trước là 14px).
- Tương phản chữ phụ **7:1** (trước 4,76:1) — `#475569`/trắng; panel tối `#b8c4d6`.
- Đích chạm **≥48px** cho mọi thứ bấm được; số to 24px+, `tabular-nums`, một cột đọc.
- Nền **sáng** mặc định ở `/phu-huynh` + nút Dịu mắt · A− / A+ (nhãn 15px).
- **Không** biểu đồ ở trang phụ huynh; thay bằng "Ba bài gần nhất: 6,5 → 8 → 7,5".
- Không jargon ("mở khoá", "RP"); không phán xét ("đang thấp"); đối chiếu theo **ngưỡng đạt 6,5**.
- Ngày có thứ: "Thứ Tư, 30/09/2026"; mọi chênh lệch có cả màu **lẫn** chữ (↑ tăng 0,5 / ↓ giảm 1,0).
- Liên hệ thầy (gọi/Zalo) ở **đầu và cuối** trang; không form.

## Cách cài trong code
`app/globals.css` khối `.parent-page` (sàn cỡ chữ + tương phản + đích chạm, dùng `rem` để A+/A− phóng
được) · `components/parent/*` (trang khách, liên hệ, FAQ) · `components/results/StudentResultsDashboard.tsx`
nhánh `viewer="parent"` (Tóm tắt + `afterSummary`) · `components/results/ParentHomeworkNotes.tsx`.

## Bẫy đã gặp
- Component phụ huynh **dùng chung với học sinh** → không sửa cỡ chữ trực tiếp trong component, mà nâng
  theo phạm vi trang bằng `.parent-page` (nếu không sẽ kéo giao diện 14–18 tuổi theo).
- Lớp override theme sáng trong `globals.css` dùng `!important` → muốn đổi màu riêng cho phụ huynh cũng
  phải `!important` + specificity cao hơn (`html[data-theme="light"] .parent-page :is(...)`).
- Ảnh `loading="lazy"` không tải khi chụp bằng `captureBeyondViewport` → phải cuộn hết trang rồi mới chụp.
- Mock dữ liệu Supabase để chụp trang đã đăng nhập: khớp URL theo `/rest/v1/<bảng>` (khớp chuỗi con sẽ
  dính bẫy — `tutoring_needs` select có nhúng `question_topics(...)`).
