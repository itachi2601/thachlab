---
name: lich-tuan
description: Lên lịch tuần cho thầy Thạch — gộp lịch dạy Vật lí trên thachlab (thpt_course_schedules), thời khoá biểu Cao Thắng (portal giảng viên), lịch cố định (dạy HSG sáng T7 ở Trần Văn Ơn, họp cán bộ + cà phê T2, duyệt đồ án), các mục trong Lịch công tác tuần của trường có trưởng/phó khoa Cơ khí hoặc giao ban, rồi xếp ≥3 buổi trượt băng và 2–3 buổi gym vào chỗ trống, báo trùng giờ. Dùng khi thầy nói "lên lịch tuần", "tuần này thầy có gì", "lịch tuần sau", "xếp lịch tập", "/lich-tuan".
---

# Lên lịch tuần

Kết quả: bảng 7 ngày, mỗi mục ghi nguồn, đánh dấu ⚠ khi trùng giờ, ghi `scripts/data/lich-tuan/<thứ Hai>.md`.

## Nguồn
| Nguồn | Cách lấy |
|---|---|
| Thachlab | Script đọc `thpt_course_schedules` + `thpt_courses` (khoá chưa đóng, còn hiệu lực trong tuần). Weekday 1=Thứ 2…7=CN. |
| Cao Thắng TKB | **Portal cần đăng nhập** (`portal.caothang.edu.vn/giang_vien/tkb.php`, trả 302 khi chưa đăng nhập). Claude KHÔNG nhập mật khẩu. Xem bước 2. |
| Lịch công tác | Tự tải `caothang.edu.vn/m/bai_viet/Lich-Cong-Tac-Tuan-14` → trang tuần (văn bản theo THỨ/ngày, sáng/chiều, "TP:" thành phần). Lọc theo từ khoá trong `references/lich-co-dinh.json` (`loc_lich_cong_tac`). |
| Cố định | `references/lich-co-dinh.json` — sửa ở đó. |

## Quy trình
1. Xác định tuần (mặc định tuần hiện tại; "tuần sau" → `--tuan` một ngày trong tuần đó).
2. **TKB Cao Thắng**: nếu `scripts/data/lich-tuan/tkb-caothang.json` chưa có hoặc đã sang học kỳ/tuần khác, nhờ thầy đăng nhập portal trong tab trình duyệt (built-in hoặc Chrome), rồi Claude đọc trang TKB đã mở (`get_page_text`) và ghi file JSON `[{weekday,start,end,title,where}]` (tiết → giờ theo bảng tiết của trường; ghi rõ cách đổi tiết–giờ vào file nếu suy ra). Hoặc thầy dán/chụp TKB. TKB đổi theo tuần thì lưu lại theo tuần.
3. Chạy trong tab terminal (cần `.env.local`):
```
cd /Users/MAC/Projects/thachlab && npx tsx .claude/skills/lich-tuan/scripts/lich-tuan.mts
```
   Thêm `--tuan YYYY-MM-DD`, `--tkb <file>`, `--cong-tac <file.txt>` (dán tay nếu tải lỗi).
4. **Đọc lại bằng mắt**: mục "lịch công tác" lọc theo từ khoá nên có thể lọt/thừa — đối chiếu bản gốc, loại mục không liên quan, nêu mục không rõ giờ. Trùng giờ ⚠ → hỏi thầy ưu tiên, không tự bỏ mục nào.
5. **Đưa lên web**: chạy lại cùng lệnh thêm `--ghi itachi2601@gmail.com` (ghi bảng `staff_week_plans`, hiện ở mục "Lịch tuần" trang `/tai-khoan`, `components/account/StaffWeekPlan.tsx`). Chỉ ghi sau khi thầy xem bản nháp ổn. Chạy lại cùng tuần thì ghi đè.
6. Báo thầy bản cuối ngắn: mỗi ngày một khối, kèm số buổi trượt băng/gym đã xếp. Chỉ thêm vào Google Calendar khi thầy bảo.

## Cách đọc TKB portal (đã chạy thật 18/10/2026)
- Sau khi thầy đăng nhập: điều hướng `tkb.php`, bấm nút mũi tên phải để sang tuần cần (mặc định hiện tuần hiện tại), rồi `javascript_tool` lấy các hàng bảng. Ô "Buổi" (Sáng/Chiều/Tối) có rowspan nên hàng đầu mỗi buổi có thêm 1 ô — đếm cột từ phải, đừng dùng `get_page_text` (mất ô trống, lệch ngày).
- Trang này chỉ là lịch **lý thuyết**; chưa thấy lịch thực hành/đồ án — hỏi thầy nếu còn nguồn khác.
- Giờ tiết (thầy chốt 18/10/2026): mỗi tiết 45 phút, nghỉ 5 phút giữa các tiết, riêng giữa tiết 3 và 4 nghỉ 10 phút. Sáng bắt đầu 6h30: T1 6:30–7:15, T2 7:20–8:05, T3 8:10–8:55, T4 9:05–9:50, T5 9:55–10:40, T6 10:45–11:30. Chiều bắt đầu 12h30, cùng nhịp: T7 12:30–13:15, T8 13:20–14:05, T9 14:10–14:55, T10 15:05–15:50, T11 15:55–16:40, T12 16:45–17:30. Giờ các tiết tối (13–16) chưa có — hỏi thầy khi gặp.
- Gộp các tiết liền nhau cùng môn/lớp thành một mục; ghi giờ vào đầu tiết đầu và cuối tiết cuối.

## Quy ước (thầy chốt 18/10/2026)
- Sáng T7 8h–11h dạy HSG KHTN 9 ở THCS Trần Văn Ơn.
- T2: họp cán bộ 7h15–8h15, sau đó cà phê cùng cán bộ bộ môn; 10h có việc khác (nội dung chưa rõ, giả định 1 giờ — hỏi thầy tên việc).
- Duyệt đồ án 8h30–9h30 vào T4 và T6 (thầy xác nhận 18/10/2026; T2 không có duyệt đồ án).
- Lịch công tác tuần: thầy phải dự khi thành phần có **trưởng/phó khoa, Bộ Cơ khí, hoặc giao ban**.
- Trượt băng ≥3 buổi/tuần (giả định 2 giờ, chiều tối), gym 2–3 buổi (1,5 giờ, không hai ngày liền). Giờ ưu tiên sửa ở `the_thao`. Né T2 cho trượt băng. Tuần kín thì báo thiếu, không ép.
- Mỗi mục Dạy Vật lí ghi `lesson` = "Đã tới: <mốc thpt_courses.current_topic_id> · Tiếp: <chủ đề tầng bài kế tiếp cùng khối>" (khoá không theo mốc, vd ôn thi HK: `buoi_day.ghi_chu_khoa[id]` trong `lich-co-dinh.json`) và `note` = nhịp buổi `buoi_day.nhip` (tự ôn 10–15′ → kiểm tra bài cũ 20–25′ → sửa bài & ôn 30′ → bài mới + bài tập). Thầy báo "lớp X đã học tới bài Y" → gọi `teaching_set(course, topic, true, ngày)` qua `supabase db query --linked` với `set_config('request.jwt.claims', …sub = uid thầy…)`; mốc chỉ nhận chủ đề tầng bài (`parent_id null`, đúng khối).
- Giờ hợp lý cho thể thao: không xếp sát giờ ngủ; đừng gym nặng ngay trước buổi trượt băng (xếp xen kẽ).

## Chưa làm / giả định
- Địa điểm trượt băng/gym chưa có; thầy cho tên để ghi vào.
- Giờ kết thúc mục công tác ước 90 phút khi trang chỉ ghi giờ bắt đầu.

## Nhật ký rút kinh nghiệm
- 2026-10-18 · tạo skill · portal giảng viên trả 302 khi chưa đăng nhập → luôn xin thầy tự đăng nhập, không tự nhập mật khẩu; trang công tác chỉ là văn bản theo THỨ/ngày, không phải `<table>` chuẩn nên script tách theo dòng "THỨ …" và giờ "09h00".
- 2026-10-18 · thầy nêu lớp theo "thứ" nhưng lệch với `thpt_course_schedules` (nói "lớp 10 thứ 2" trong khi 10L3 là thứ 3) → đối chiếu theo TÊN lớp trong DB, ghi rõ cách hiểu khi báo lại; 12L1 B7/B8 ôn thi nên không có mốc bài → dùng `ghi_chu_khoa`.
