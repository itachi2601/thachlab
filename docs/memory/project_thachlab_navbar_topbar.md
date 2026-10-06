---
name: project_thachlab_navbar_topbar
description: Rà + sửa thanh top bar (components/layout/Navbar.tsx) 2026-10-04 theo QUY-TAC-THIET-KE; đã push + deploy, còn chờ kiểm khi đăng nhập thật
metadata:
  type: project
---

**Mục tiêu:** thanh top bar toàn site đạt quy tắc N2, N4, D1, D2, M2, B6 (`docs/QUY-TAC-THIET-KE.md`).

**Lỗi tìm thấy khi rà 2026-10-04 (dev server, chưa đăng nhập):** desktop 1024/1440 có 6/8 link gãy 2 dòng;
mobile khi đăng nhập ước ~440px > 375 (tràn); 8 link desktop (N2); menu mobile chip 28px, chip "Xem kết quả
của con" trùng href Phụ huynh, "Đăng ký" #60A5FA trên trắng ~2.5:1, nền 96% lộ chữ, không đóng bằng
bấm ngoài/Esc.

**Đã xong (Sonnet sửa, Opus kiểm lại):**
- `e1c8e7651` Navbar.tsx: desktop còn 5 mục — THPT – THCS (dropdown lớp) · CTTC · Đăng ký học · Phụ huynh ·
  "Thêm ▾" (Blog, Tin tức, Giới thiệu, Liên hệ); `whitespace-nowrap`. Mobile: nút tài khoản chỉ avatar
  44px dưới `sm`, ThemeToggle ẩn dưới `sm` và chuyển thành dòng "Giao diện sáng/tối" trong menu ☰. Menu
  mobile: chip `min-h-11`, bỏ chip trùng, nền đặc, đóng khi bấm ngoài/Escape/đổi pathname.
- `a849aa18c` globals.css: ghi đè nền trắng theme sáng chỉ cho `header .bg-[#0B1220]` — bản đầu áp toàn
  site làm mũi tên `components/physics/Tooltip.tsx` thành trắng trong khi bong bóng tối. Đừng nới lại.
- Đã push `main` và chạy `scripts/deploy.sh` trong `.claude/worktrees/deploy-tree` (build sạch, chỉ 2
  commit này) lúc ~21:30 2026-10-04; đã xác nhận LIVE trên thachlab.id.vn (last-modified 14:30 GMT = 21:30 giờ VN 2026-10-04).

**Còn chờ:**
- Kiểm khi ĐĂNG NHẬP thật ở 360/375px: bề rộng cụm phải (tên dài, chuông có số, avatar ảnh) — ~316px
  chỉ là ước tính cộng bề rộng; dropdown "Thêm" bằng bàn phím (Tab/Esc — Esc chỉ blur, chuột còn hover
  thì chưa đóng); menu mobile cao ~650px gần chạm MobileTabBar.
- Chưa giải quyết: ☰ mobile trùng một phần với MobileTabBar (Trang chủ/Lớp học/Luyện tập/Tài khoản).

Liên quan [[feedback_design_research_rules]], [[feedback_mobile_first_ui]], [[project_thachlab_concurrent_sessions]].
