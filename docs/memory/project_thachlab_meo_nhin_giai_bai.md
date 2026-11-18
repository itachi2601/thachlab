---
name: project-thachlab-meo-nhin-giai-bai
description: 💡 Mẹo nhìn trong bài tập mẫu — 9 mẹo/13 dạng đã đăng (L12 b4 đăng 2026-11-18); chặng 5 đo từ 2026-11-19
metadata:
  type: project
---

Mô hình đời thường giải nhanh một dạng (`meo` trong `scripts/data/bai-tap-mau/<id>.json`, khối gập sau lời giải). Kế hoạch: `docs/KE-HOACH-MEO-GIAI-BAI-TAP.md`; bảng tra bắt buộc: `docs/BANG-MEO-GIAI.md`. Khác [[project-thachlab-meo-tu-khoa]] (🧠 trong bài lý thuyết).

**Đã đăng:** đợt 1 ngày 2026-11-06 (153 d1–d2, 162 d3–d4, 90 d2, 157 d1, 23 d4, 18 d2, 83 d2); Thang máy dừng tầng lesson 2 d3–d4 ngày 2026-11-07.

**2026-11-17 — L12 Bài 4 (lesson 5):** DB vốn có 4 dạng chuẩn (repo không có `5.json`, ghi chú cũ "chưa có BTM" là sai) → chèn Dạng 3 (trộn kim loại vào nước + vỏ 40 J/K, c ≈ 391, 💡 Đòn bẩy nhiệt) và Dạng 4 (đá 0 °C vào nước 30 °C, không tan hết, còn ≈ 36,8 g, 💡 Quỹ nhiệt) bằng `scripts/data/bai-tap-mau/them-dang-nhiet-5.py` (nguồn `old/5.json` dump từ DB). kiem-code đạt; chữ hình ≥15,4px ở 375px. Commit 58ef800ac + b430b3a43. Thầy duyệt 17/11. **Đã đăng 2026-11-18 10h05** (lịch 22h05 17/11 chạy nhưng bị chặn ở bước duyệt tab terminal) — DB 6 dạng/2 mẹo, sao lưu `scripts/logs/bai-tap-mau-bai5-1794971105058.json`.

**Còn chờ:**
- Chặng 5 đo hiệu quả: từ 2026-11-19 (đủ 2 tuần kể từ 2026-11-05) chạy `scripts/sql/do-meo-nhin.sql`; đợt 2 (15 ứng viên, KE-HOACH mục 4) chỉ mở sau khi có số.
- Mở rộng thầy duyệt 2026-11-18 (KE-HOACH mục 7): ✓ Soát nhanh (1 câu tự trả lời ở bước cuối dạng) + ⚖ Lập tỉ số; chặng 6 ✅ 18/11 (bảng tra mục ✓/⚖ trong BANG-MEO-GIAI, trường `buoc[].soat` có validator + UI, chưa deploy), chặng 7 thí điểm L12 Ch.1 (8 dạng lesson 3/4/5) đã soạn + soát + deploy UI 18/11; hẹn đăng DB 22:05 18/11 trong tab terminal — sáng 19/11 kiểm `scripts/logs/dang-soat-nhanh-l12-ch1.log` có "XONG" và 3 file sao lưu `bai-tap-mau-bai{3,4,5}-*.json`. Chặng 8 ⚖ Lập tỉ số: vá 4 dạng 26·3, 152·4, 15·3, 40·2 (`them-ti-so-chang8.py`), kiem-code đạt, CHƯA đăng DB — chờ thầy duyệt rồi `publish-bai-tap-mau.mts --lesson <id> --yes` cho 15, 26, 40, 152 sau 22h. Chặng 9 đo từ 19/11. Main bị ruleset chặn tự gộp: thầy tự `push origin HEAD:main`.
- `meo.dieu_kien` Đòn bẩy nhiệt 50 chữ (validator cảnh báo > 40), dùng chung 153 + 5 — sửa ở `meo_nhiet.py` thì chạy lại cả hai bài.

**Why:** thầy muốn mẹo đặt đúng chỗ có dạng hợp ⚠ (đủ mọi giả thiết), mỗi bài ≤ 2 dạng có mẹo (G1).
**How to apply:** lịch tự động cần ghi DB qua tab terminal sẽ kẹt vì không ai duyệt — lịch đăng chỉ đáng tin nếu lệnh ghi chạy được qua Bash (Bash bị sandbox chặn supabase.co) → kiểm lượt chạy sáng hôm sau, đừng coi 'succeeded' là đã đăng;  trước khi gắn mẹo vào bài "chưa có BTM", dump DB (`scripts/dump-bai-tap-mau-cu.mts <id>`); hình `thanh_nang_luong`: nhãn `mui` ≤ 5 ký tự kẻo bị thu dưới 13px.
