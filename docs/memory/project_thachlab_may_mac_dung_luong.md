---
name: project_thachlab_may_mac_dung_luong
description: Dọn dung lượng MacBook 2026-10-11 — xoá Documents/THPT (không sao lưu), Parallels, TeX Live→BasicTeX, tắt Time Machine; nguồn tài liệu cũ không còn
metadata:
  type: project
---

Phiên 2026-10-11 chỉ dọn máy Mac của thầy (không đụng code thachlab). Ổ Data 96% (21 GB trống) → 76% (107 GB trống, còn lên khoảng 140–150 GB sau khi xoá 2 snapshot).

**Đã xoá / đổi (đừng tìm lại):**
- `~/Documents/THPT` (36 GB) **xoá toàn bộ, không sao lưu** theo lựa chọn của thầy. Mất cả nguồn gốc ghi trong AGENTS.md ("Nơi lưu nội dung bồi dưỡng HSG KHTN 9", `HSG_KHTN9_Vat_li/`) và công cụ `_tools/trang-mau-sach/sach_mau.py`. Các memory khác còn trỏ `~/Documents/THPT/...` (de_lop10_24_25, de_thi_thu_truong_so, hk2_lop10_4chuong, chuong4_hat_nhan, bai8_mo_ta_song, khoa_hsg9_vat_ly) → đường dẫn đó **không còn tồn tại**; nội dung đã đăng nằm trong DB Supabase và `content/` của repo.
- Máy ảo Parallels Windows 11 (35 GB) + ISO + cấu hình Parallels trong `~/Library` — thầy không còn dùng.
- TeX Live (9,6 GB) → **BasicTeX** (597 MB) + gói vntex/babel-vietnamese/amsmath/mathtools/siunitx/cancel/collection-latexrecommended/fontsrecommended/langother. Đã biên dịch thử file tiếng Việt OK (pdflatex, xelatex). Repo thachlab không gọi TeX. Thiếu gói thì `sudo tlmgr install <gói>`.
- 10 worktree sạch trong `.claude/worktrees` (nhánh git còn nguyên), `.next`, `$RECYCLE.BIN` (7,3 GB), Trash, cache ShipIt của Cursor, cache Chrome + model AI OptGuide 4 GB (hồ sơ/mật khẩu Chrome giữ nguyên).
- Time Machine: `AutoBackup=0` (thầy tắt bằng giao diện). Máy hiện **không có sao lưu nào**.

**Why:** ổ đầy 96% sẽ làm build/macOS chậm; thầy chốt các mục trên từng bước.

**Còn treo:**
- Hai snapshot Time Machine cục bộ 2026-10-10 19:18:53 và 20:16:39 vẫn giữ khối của `THPT` — chạy `for s in 2026-10-10-191853 2026-10-10-201639; do tmutil deletelocalsnapshots $s; done` để trả 36 GB.
- Worktree để lại, chờ thầy quyết: `.claude/worktrees/deploy-ui` (12 file sửa dở chưa commit) và `.claude/worktrees/fix-trang-chuong-bai` (2 commit chưa vào main: 10d6d4eb8, 9e7e4ff54).
- Thư viện Ảnh 107 GB (79 GB là video; 6 video đầu ~28 GB): thầy cân nhắc bật "Optimize Mac Storage" ở Ảnh trên Mac + iPhone (chỉ làm khi iCloud đủ gói và đã đồng bộ hết).
- Khoản khác còn lớn: ảnh nền Aerials ~18 GB, ZaloData 9,5 GB, Claude vm_bundles 8,3 GB, GoodNotes 6,4 GB, Word container 5,1 GB, iThoughtsX 3,4 GB.
- AGENTS.md mục "Nơi lưu nội dung bồi dưỡng HSG KHTN 9" và "Trang mẫu chuẩn cho tài liệu/sách" đang trỏ thư mục đã xoá — cần thầy quyết nơi lưu mới (phiên này không sửa AGENTS.md).

**How to apply:** phiên sau thấy lệnh/skill đòi đọc `~/Documents/THPT/...` thì báo thầy là thư mục đã xoá, đừng cố tìm; muốn dàn trang PDF tài liệu thì dựng lại công cụ (BasicTeX hoặc Paged.js như `book/`).
