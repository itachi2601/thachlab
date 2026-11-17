---
name: project-thachlab-meo-nhin-giai-bai
description: 💡 Mẹo nhìn trong bài tập mẫu — 9 mẹo/11 dạng đã đăng; L12 b4 (lesson 5) hẹn đăng 22h05 2026-11-17; chặng 5 đo từ 2026-11-19
metadata:
  type: project
---

Mô hình đời thường giải nhanh một dạng (`meo` trong `scripts/data/bai-tap-mau/<id>.json`, khối gập sau lời giải). Kế hoạch: `docs/KE-HOACH-MEO-GIAI-BAI-TAP.md`; bảng tra bắt buộc: `docs/BANG-MEO-GIAI.md`. Khác [[project-thachlab-meo-tu-khoa]] (🧠 trong bài lý thuyết).

**Đã đăng:** đợt 1 ngày 2026-11-06 (153 d1–d2, 162 d3–d4, 90 d2, 157 d1, 23 d4, 18 d2, 83 d2); Thang máy dừng tầng lesson 2 d3–d4 ngày 2026-11-07.

**2026-11-17 — L12 Bài 4 (lesson 5):** DB vốn có 4 dạng chuẩn (repo không có `5.json`, ghi chú cũ "chưa có BTM" là sai) → chèn Dạng 3 (trộn kim loại vào nước + vỏ 40 J/K, c ≈ 391, 💡 Đòn bẩy nhiệt) và Dạng 4 (đá 0 °C vào nước 30 °C, không tan hết, còn ≈ 36,8 g, 💡 Quỹ nhiệt) bằng `scripts/data/bai-tap-mau/them-dang-nhiet-5.py` (nguồn `old/5.json` dump từ DB). kiem-code đạt; chữ hình ≥15,4px ở 375px. Commit 58ef800ac + b430b3a43 trên nhánh `claude/exercise-tips-3572cb` (chưa vào main lúc chốt). Thầy duyệt 17/11.

**Còn chờ:**
- Scheduled task `dang-btm-l12-bai4-meo-nhiet-17-11` (Auto) 22h05 2026-11-17: publish lesson 5 không `--giu-cu`, kiểm DB 6 dạng/2 mẹo, đổi trạng thái 2 hàng trong `BANG-MEO-GIAI.md` + mục KE-HOACH, commit. Phiên sau: xem lượt chạy ở Scheduled; nếu chưa chạy/lỗi thì chạy tay `npx tsx scripts/publish-bai-tap-mau.mts --lesson 5 --dry-run` rồi `--yes`.
- Chặng 5 đo hiệu quả: từ 2026-11-19 (đủ 2 tuần kể từ 2026-11-05) chạy `scripts/sql/do-meo-nhin.sql`; đợt 2 (15 ứng viên, KE-HOACH mục 4) chỉ mở sau khi có số.
- `meo.dieu_kien` Đòn bẩy nhiệt 50 chữ (validator cảnh báo > 40), dùng chung 153 + 5 — sửa ở `meo_nhiet.py` thì chạy lại cả hai bài.

**Why:** thầy muốn mẹo đặt đúng chỗ có dạng hợp ⚠ (đủ mọi giả thiết), mỗi bài ≤ 2 dạng có mẹo (G1).
**How to apply:** trước khi gắn mẹo vào bài "chưa có BTM", dump DB (`scripts/dump-bai-tap-mau-cu.mts <id>`); hình `thanh_nang_luong`: nhãn `mui` ≤ 5 ký tự kẻo bị thu dưới 13px.
