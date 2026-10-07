# Việc đang treo — phân loại (7/10/2026)

Nguồn: dòng "treo/chờ/chưa" trong `docs/memory/MEMORY.md` + đầu `docs/STATE.md`. Chưa đối chiếu từng mục với trạng thái
thật trên production, nên có mục có thể đã xong mà memory chưa cập nhật — gặp thì gạch bỏ.

Mục tiêu: 1–2 tuần không mở việc mới, chỉ đóng A, thử B, để C yên.

## A. Đóng được trong 1 buổi (chỉ cần chạy lệnh / bấm / xem bằng mắt)

**Lệnh chạy trên Mac**
- [ ] `bash scripts/run-migrations.sh --list` → đối chiếu tên file, chạy các migration còn chờ: `20261003130000` (UI phụ huynh), `20260928190000` (rank — kiểm lại xem đã chạy chưa, tránh lỗi "already exists").
- [ ] Push script `--nam l11` (commit `471489729`, chưa push).
- [ ] Deploy những gì đã vào main nhưng chưa lên web: Hero tab 4 "Hình chiếu"; 13 bài lý thuyết L12 (đã ghi DB nhưng chưa deploy).
- [ ] Pause project Supabase Sydney cũ (`fxnqgmfqdbvnjawgnsfi`).
- [ ] Tắt MCP thừa (giảm token).

**Mở web xem bằng mắt (mỗi mục ~5 phút)**
- [ ] WelcomePanel từng vai (HS / GV / PH).
- [ ] Navbar top bar khi đăng nhập ở 360/375px.
- [ ] ReadingZone khi đăng nhập; chữ `text-violet` ở theme sáng.
- [ ] 4 bài L10 mới (thay ví dụ xưởng bằng đời sống); ảnh bài 30 và 28 (L10 Ch5–7).
- [ ] Bug ExamRunner chuyển câu — memory ghi "trạng thái sửa chưa rõ": thử 1 lần là biết.
- [ ] Test bấm thật: `/quan-tri/sua-de` (sửa + lưu), Ngân hàng câu hỏi + cảnh báo trùng, Mastery YCCĐ ở `/lop-hoc`, Thoát phụ đạo (20 câu), Danh hiệu đeo + khung sưu tập.

**Quyết định (không tốn công, chỉ cần thầy chốt)**
- [ ] Bật "Hiện" đề lớp 11: item 57 (41 đề), 59 (28), 60 (15); item 58 đang ở Bản nháp.
- [ ] Đề thi thử trường/sở: chốt đích đăng + kiểm trùng (304 file đã lọc: 133 sạch, 164 chỉ [lưu ý], 5 bẩn) — hoặc ghi rõ "hoãn".
- [ ] Duyệt 80 hình AI trong đề (chống đề mất hình).

## B. Cần người thật / thiết bị thật (chọn tối đa 1–2 việc trong 2 tuần)

- [ ] PWA: thử trên điện thoại thật (cài, offline, Luyện nhanh 10 câu), gửi push thật; tick M4.
- [ ] Rank + danh hiệu: cho vài HS thật dùng trong mùa thử nghiệm (đến 25/10); theo dõi xem có nhảy bậc bất thường.
- [ ] UI phụ huynh: phỏng vấn 2–3 phụ huynh thật (45–60 tuổi), chụp ảnh nghiệm thu.

## C. Nên hoãn — đưa vào ROADMAP, không đụng tuần này

| Việc | Lý do hoãn |
|---|---|
| AI Tutor Socratic (chạy eval 30 câu, thêm API key) | Đã chốt không xây trước Q2/2027 |
| KHTN 9 Vật lí | Chưa làm gì, chưa có deadline |
| Zalo OA cho phụ huynh | Cần thủ tục ngoài, không gấp |
| Nhãn + lời giải + tự luận cho đề L10 (24–25) và L11 | Khối lượng lớn, đề đã đăng dùng được |
| 167 bộ đề L10 chưa được; 40 bộ đề L11 lệch (7 bộ 0 câu) | Vá tay từng bộ, giá trị thấp |
| Lý thuyết còn thiếu: lớp 11 (6 bài), lớp 12 (1 bài) | Đã có 90+ bài; làm khi rảnh |
| Hero chặng 2 (nhúng mô phỏng vào bài lý thuyết) | Cần dựng cơ chế mount mới trong `ContentHtml` |
| Sách in Chương 2 lớp 10 | Chưa in thử; hoàn thiện sau |
| Kiểm tra định kỳ (11 mục ẩn); Kiểm tra hiểu bài | Chờ gắn đề / chờ ví dụ |
| Phụ đạo: restamp đề cũ + sửa nhãn tay; bảng phân bố bậc; bỏ `topic_name`; tin tức | Cải tiến, không chặn gì |
| Dọn trùng ngân hàng câu hỏi (audit ledger, fix answers đang dở trong working tree) | Hoàn tất một lần rồi commit, đừng mở thêm đợt |

## Nguyên tắc 2 tuần tới
1. Không mở mảng mới. Có ý tưởng → ghi một dòng vào `docs/ROADMAP.md`.
2. Tối đa 2 mảng làm việc mỗi ngày.
3. Phiên agent dừng trước 23h; không chạy xuyên đêm.
4. Working tree phải sạch cuối tuần: commit hoặc bỏ hẳn từng file dở (hiện có 5 file sửa + 8 file chưa theo dõi thuộc sách in, audit ngân hàng câu hỏi, roadmap).

## Kết quả kiểm nhóm A (7/10/2026, buổi sáng)
- **Migration: không còn file nào thật sự chờ.** `bash scripts/run-migrations.sh --list` vẫn liệt kê 6 file, nhưng mảng `FILES` đã cũ — cả 6 (và `20261003130000`, `20260928190000`) đều có log chạy trong `scripts/logs/`, và `STATE.md` ghi "Đã chạy". Riêng `20261006180000_similar_bank_questions` (STATE vẫn ghi "Chờ chạy") có log 6/10 23:14 không lỗi → coi như đã chạy; `20261006120000_question_bank_dedup` lần 2 báo "already exists" = lần 1 đã chạy. **Không chạy lại gì.** Việc còn lại: dọn mảng `FILES` + sửa dòng "Chờ chạy" trong STATE.
- **Push:** 18 commit `main` đã push lên `origin/main` (0537f78b4 → 0c1a95a4c), gồm cả commit script `--nam l11`.
- **Deploy:** nhánh `deploy` được cập nhật 7/10 10:24 → Hero "Hình chiếu" và 13 bài L12 (commit ≤ 6/10) đã nằm trong bản đó; chưa kiểm trên web thật. Các commit sau 10:24 (sách in, skill) chưa cần deploy.
- **ExamRunner chuyển câu:** chưa xác nhận được — cần bấm tay trên trình duyệt thật có đăng nhập.
