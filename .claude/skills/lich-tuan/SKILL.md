---
name: lich-tuan
description: Lịch công tác tuần của thầy Thạch — gộp lịch dạy thachlab (mốc bài), buổi HSG KHTN 9, TKB Cao Thắng, lịch cố định, lịch công tác trường; xếp trượt băng + gym vào chỗ trống, báo trùng giờ, đưa lên /tai-khoan. Cũng dùng khi thầy báo tiến độ dạy. Dùng khi thầy nói "lên lịch tuần", "tuần này thầy có gì", "xếp lịch tập", "cập nhật lịch dạy", "/lich-tuan".
---

# Lên lịch tuần

Kết quả: bảng 7 ngày, mỗi mục ghi nguồn, đánh dấu ⚠ khi trùng giờ, ghi `scripts/data/lich-tuan/<thứ Hai>.md` và (bước 5) bảng `staff_week_plans` → mục "Lịch tuần" trang `/tai-khoan` (`components/account/StaffWeekPlan.tsx`: mobile xem từng ngày, desktop lưới 7 cột, dòng "Tiếp theo", tổng kết buổi dạy/tập).

## Nguồn
| Nguồn | Cách lấy |
|---|---|
| Thachlab | Script đọc `thpt_course_schedules` + `thpt_courses` (khoá chưa đóng, còn hiệu lực trong tuần). Weekday 1=Thứ 2…7=CN. |
| Cao Thắng TKB | **Portal cần đăng nhập** (`portal.caothang.edu.vn/giang_vien/tkb.php`, trả 302 khi chưa đăng nhập). Claude KHÔNG nhập mật khẩu. Xem bước 2. |
| Lịch công tác | Tự tải `caothang.edu.vn/m/bai_viet/Lich-Cong-Tac-Tuan-14` → trang tuần (văn bản theo THỨ/ngày, sáng/chiều, "TP:" thành phần). Lọc theo từ khoá trong `references/lich-co-dinh.json` (`loc_lich_cong_tac`). |
| Cố định | `references/lich-co-dinh.json` — sửa ở đó. Buổi "Dạy HSG KHTN 9" gắn mốc từ `scripts/data/btvn-hsg9/tuan.json` (khớp `ngay` dd/mm với thứ Bảy của tuần; cùng nguồn với lộ trình HS `/lop-hoc/lo-trinh-hsg`) — đổi lộ trình thì sửa tuan.json, không sửa ở đây. |
| Mốc bài Vật lí | `thpt_courses.current_topic_id` (chủ đề tầng bài) → script tự ghi "Đã tới: … · Tiếp: …" + nhịp buổi `buoi_day.nhip`; khoá ôn thi không có mốc → `buoi_day.ghi_chu_khoa[id]`. |

## Quy trình
0. **Thầy báo tiến độ** ("lớp 10L3 đã học tới Tổng hợp lực", "12L1 thứ 4–5 tới dòng điện xoay chiều"): đối chiếu theo TÊN khoá trong DB (thứ thầy nói có thể lệch `thpt_course_schedules` — nêu rõ cách hiểu khi báo lại), rồi chạy trong tab terminal:
```
npx tsx .claude/skills/lich-tuan/scripts/ghi-moc-bai.mts --khoa            # xem khoá + mốc hiện tại
npx tsx .claude/skills/lich-tuan/scripts/ghi-moc-bai.mts --tim "sóng dừng"  # tìm id chủ đề tầng bài đúng khối
npx tsx .claude/skills/lich-tuan/scripts/ghi-moc-bai.mts 4:46:2026-10-16    # <course_id>:<topic_id>:<ngày dạy>, nhiều bộ cách nhau bằng dấu cách
```
   Script gọi `teaching_set` dưới danh nghĩa thầy (ghi `thpt_teaching_progress` + đồng bộ `current_topic_id`); chỉ nhận chủ đề `parent_id null` đúng khối. Ghi xong làm tiếp bước 1–5 để web cập nhật.
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
- **Lịch công tác tuần được ưu tiên** (thầy chốt 19/10/2026): việc khác trùng giờ với mục công tác thì KHÔNG tự bỏ, chỉ ghi cảnh báo "cần nhờ người dạy/dự thay" ở khung Cần chú ý (đầu mục Lịch tuần) để thầy nhờ người xem hộ. Hai mục công tác trùng nhau thì để thầy chọn mục dự. Script tự sinh các cảnh báo này (bước 5b).
- **Mục công tác có chữ "Thạch" (Thầy Thạch, Đ/c Thạch, Diệu Thạch…) là thầy — luôn giữ** dù không có trưởng/phó khoa hay giao ban. Cả trường chỉ có một người tên Thạch (thầy chốt 19/10/2026), nên khớp chữ "thạch" là đủ; từ khoá ở `ten_thay` trong `references/lich-co-dinh.json`. Mục khớp được ghi chú "CÓ TÊN THẦY".
- Sáng T7 8h–11h dạy HSG KHTN 9 ở THCS Trần Văn Ơn.
- T2: họp cán bộ 7h15–8h15, sau đó cà phê cùng cán bộ bộ môn; 10h có việc khác (nội dung chưa rõ, giả định 1 giờ — hỏi thầy tên việc).
- Duyệt đồ án 8h30–9h30 vào T4 và T6 (thầy xác nhận 18/10/2026; T2 không có duyệt đồ án).
- Lịch công tác tuần: thầy phải dự khi thành phần có **trưởng/phó khoa, Bộ Cơ khí, hoặc giao ban**.
- Trượt băng ≥3 buổi/tuần (giả định 2 giờ, chiều tối), gym 2–3 buổi (1,5 giờ, không hai ngày liền). Giờ ưu tiên sửa ở `the_thao`. Né T2 cho trượt băng. Tuần kín thì báo thiếu, không ép.
- Mỗi mục Dạy Vật lí ghi `lesson` = "Đã tới: <mốc thpt_courses.current_topic_id> · Tiếp: <chủ đề tầng bài kế tiếp cùng khối>" (khoá không theo mốc, vd ôn thi HK: `buoi_day.ghi_chu_khoa[id]` trong `lich-co-dinh.json`) và `note` = nhịp buổi `buoi_day.nhip` (tự ôn 10–15′ → kiểm tra bài cũ 20–25′ → sửa bài & ôn 30′ → bài mới + bài tập). Thầy báo "lớp X đã học tới bài Y" → gọi `teaching_set(course, topic, true, ngày)` qua `supabase db query --linked` với `set_config('request.jwt.claims', …sub = uid thầy…)`; mốc chỉ nhận chủ đề tầng bài (`parent_id null`, đúng khối).
- Giờ hợp lý cho thể thao: không xếp sát giờ ngủ; đừng gym nặng ngay trước buổi trượt băng (xếp xen kẽ).
- **Nội dung từng buổi tập** (thầy duyệt 19/10/2026) ở `noi_dung_tap` trong `lich-co-dinh.json`; script bước 5a gán: trượt băng ≥17:00 → Ôn nhẹ, cùng ngày gym → Edge & turn, còn lại Nhảy rồi Spin; gym cùng ngày trượt băng → Thân trên + core, còn lại Chân nặng rồi Toàn thân + sức bật. `lesson` = tên buổi, `note` = chi tiết + khung giờ. Đổi bài tập thì sửa JSON, không sửa script.

## Chưa làm / giả định
- Địa điểm trượt băng/gym chưa có; thầy cho tên để ghi vào.
- Giờ kết thúc mục công tác ước 90 phút khi trang chỉ ghi giờ bắt đầu.

## Nhật ký rút kinh nghiệm
- 2026-10-18 · tạo skill · portal giảng viên trả 302 khi chưa đăng nhập → luôn xin thầy tự đăng nhập, không tự nhập mật khẩu; trang công tác chỉ là văn bản theo THỨ/ngày, không phải `<table>` chuẩn nên script tách theo dòng "THỨ …" và giờ "09h00".
- 2026-10-18 · thầy nêu lớp theo "thứ" nhưng lệch với `thpt_course_schedules` (nói "lớp 10 thứ 2" trong khi 10L3 là thứ 3) → đối chiếu theo TÊN lớp trong DB, ghi rõ cách hiểu khi báo lại; 12L1 B7/B8 ôn thi nên không có mốc bài → dùng `ghi_chu_khoa`.
- 2026-10-19 · thầy dặn mục có tên "Thạch" là thầy và lịch công tác được ưu tiên → khớp chữ "thạch" là đủ (cả trường một người), trùng giờ thì cảnh báo "nhờ người xem hộ" chứ không tự bỏ việc nào; trước khi sửa `StaffWeekPlan.tsx` phải `git log` + đọc lại vì phiên khác đã viết lại file.
- 2026-10-19 · thầy muốn nội dung tập hiện trong lịch → đặt dữ liệu ở `lich-co-dinh.json` (`noi_dung_tap`), script chỉ gán theo quy tắc; trình tự trượt băng theo đúng triết lý thầy (edge → turn → waltz jump/spin), gym chân nặng không đặt ngay trước buổi nhảy.
