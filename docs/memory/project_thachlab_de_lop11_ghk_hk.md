---
name: project_thachlab_de_lop11_ghk_hk
description: Đề Vật lí 11 (nguồn CT2025_VietnamTeach/đề thi ) đăng bằng dang-de-l10-24-25.py --nam l11 — 5/10/2026 lên 75 đề vào 3 mục ẩn; Cuối HK1 chưa làm
metadata:
  type: project
---

5/10/2026: script `scripts/dang-de-l10-24-25.py` thêm `--nam l11` (SRC11/ROOTS11, bỏ bản sao "Đề thi vật lý 11") và đọc đáp án bằng DeepSeek `deepseek-flash` (thinking tắt, json_object) khi không có ANTHROPIC_API_KEY. Chưa commit.
Đích: item 57 (lesson 117 Giữa HK1, 35 đề), 59 (119 Giữa HK2, 26 đề), 60 (120 Cuối HK2, 14 đề) — đều ĐANG ẨN, thầy "Hiện" sau khi xem. Log `scripts/data/de-l11-{log,run}.json`, file trung gian `scripts/logs/de-l11/`.
**Cuối HK1 (lesson 118/item 58, đang hiện, có exam 203) CHƯA đăng** — thầy chốt để nháp: khi làm phải đăng rồi đặt Bản nháp ở /quan-tri/sua-de (exam mới `published=true` mặc định). TARGET l11 hiện bỏ "2. HK1".
Còn lại: 87 bộ SKIP>20%, 35 LỆCH, 7 TRÙNG, 2 LỖI (số câu ≠ số mốc: VAT LY 11-CTST-GIUA HK1.docx, 03.11GK2.docx); chưa đối chiếu tay đáp án DeepSeek ngoài 1 đề (Nam Duyên Hà khớp 100%); chưa có lời giải/nhãn Chủ đề, tự luận bị cắt.

**6/10/2026 — xử lý bộ LỆCH (48):** `dang-de-l10-24-25.py --nam l11 --all --only-status LỆCH` + dung sai mới: đề DƯ câu ở ĐUÔI so với khoá (khoá đủ 1..M, câu M+1..N thiếu đáp án) không còn tính LỆCH → để `--drop-bad` bỏ. Lên thêm 8 đề (item 57 +5, item 58 +2 Bản nháp, item 60 +1); 40 bộ còn lại vẫn LỆCH/SKIP (khoá ít hơn đề nhiều, đề 0 câu convert không đọc được, MathType hỏng, tự luận lẫn P3) — cần vá tay từng bộ. Tổng lớp 11: item 57=41, 58=52 (47+2 nháp +203/693/701), 59=28, 60=15.
