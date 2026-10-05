# Bàn giao — Mobile PWA (GĐ 2.6), đã đối chiếu với code ngày 5/10/2026

Bản đề xuất gốc (dán từ phiên khác) có vài chỗ KHÔNG khớp repo. Bảng dưới là phần đã sửa; làm theo cột "Thực tế".

## Điều chỉnh so với đề xuất gốc
| Đề xuất gốc | Thực tế trong repo | Xử lý |
|---|---|---|
| Hợp đồng `/luyen-tap?...&so=10&uu_tien=sai`, RPC `get_practice_questions`, `get_weak_skills` | **Không tồn tại.** `/luyen-tap` chỉ là trang chọn bài (state React, không đọc query). RPC thật: `get_my_weakest_topics(p_limit)` (`services/mastery.ts`) | Bỏ hợp đồng URL. "Luyện nhanh" = nút mở `TopicPracticeModal` từ `WeakestSkillsCard` |
| Màn luyện 1 câu/màn là việc mới | **Đã có** chế độ "Từng câu" (`PracticeStepView`, `features/lessons/practice-step.ts`: Kiểm tra → đúng/sai + lời giải, làm lại câu sai, giãn cách ôn, mặc định `step`) | Không làm lại. Chỉ rà trên 375px theo `docs/QUY-TAC-THIET-KE.md` (N1, D2, D3, B2) |
| Streak đóng băng 1 ngày/tuần là việc mới | **Đã có** (`20260930130000_rank_streak_freeze.sql`, `DailyStreakCard`) | Bỏ khỏi M4 |
| Thanh đáy mới 4 tab "Học · Luyện · Lộ trình · Tôi" | **Đã có** `MobileTabBar`: Trang chủ · Lớp học · Luyện tập · Tài khoản; cố ý ẩn ở `/kiem-tra/lam`, `/lop-hoc/bai`, `/phu-huynh`, `/quan-tri`, `/tro-giang/ghi` | Giữ nguyên. Không đổi tên tab, không thêm thanh thứ hai |
| Dark mode, `theme_color #0B3D91` | Đã có `ThemeToggle` + `data-theme`; QUY-TAC M1: bài học/đề mặc định sáng, tối là tuỳ chọn. Nền site `--color-bg #05070b` | `theme_color`/`background_color` lấy theo token, không dùng #0B3D91 |
| Dùng `@serwist/next` | Next 16 + `output: "export"` + Turbopack: plugin này không chắc chạy | SW viết tay `public/sw.js`; đọc `node_modules/next/dist/docs/` về manifest trước khi code (AGENTS.md) |
| Cache-first nội dung | `services/static-content.ts` đọc `/data/*.json` trước rồi đối chiếu Supabase ngầm | SW chỉ precache shell + network-first cho `/data/*`, tránh phục vụ bài cũ |
| Thân chữ ≥16px, chạm ≥44px, haptic | Đã là quy tắc C/D trong QUY-TAC-THIET-KE | Không làm lại; haptic bỏ (iOS không hỗ trợ `vibrate`) |
| Bài lý thuyết "thẻ vuốt như story" | Mâu thuẫn bài tương tác đã chốt 2/10 (`soan-bai-ly-thuyet-tuong-tac`) | Hoãn, không nằm trong 2.6 |
| Lộ trình = tab mới | ROADMAP GĐ 2: bộ huy hiệu theo lớp *là* trang lộ trình | Không thêm tab; làm trong GĐ 2 |
| Cần chạy "2 migration chờ" | Xem mục ĐANG CHỜ trong `docs/STATE.md` | M1–M3 không cần migration; chỉ M4 cần 1 file |

## Ràng buộc bắt buộc
- Hiệu năng (AGENTS.md "Đăng nội dung — luôn tối ưu tốc độ tải"): không thêm round-trip Supabase cho `/`, `/lop-hoc/bai`, `/kiem-tra/lam`; khối JS mới tách `next/dynamic({ssr:false})` + `LazyErrorBoundary`; ảnh mới `.webp` (icon manifest PNG theo chuẩn thì ngoại lệ, < 20 KB).
- Luyện tập giữ nguyên: mức `de`/`trung-binh`/`kho`, `practice-ladder`, `savePracticeSession` (kết quả lần đầu), mastery, RP.
- UI HS: nêu mã quy tắc trong commit, chụp 375px trước khi báo xong. Phụ huynh không thấy banner cài/push của HS.
- Không migration tự chạy; M4 theo quy trình `run-migrations.sh`. Edge Function deploy + `supabase secrets set` (khoá VAPID) là việc của thầy trên Mac, phải bấm thử thật sau deploy.

## Thứ tự làm
1. **M1 vỏ PWA** (manifest, icon, `sw.js`, banner cài). Kiểm: Lighthouse PWA + cài thử Android và iOS thật.
2. **M2 Luyện nhanh 10 câu** từ `WeakestSkillsCard` (≈ nửa ngày, tái dùng modal sẵn có).
3. **M3 offline** hàng đợi kết quả (sau M2).
4. **M4 push 1 lần/ngày** (cần migration + Edge Function; làm cuối, ngoài giờ HS làm bài).
Mỗi việc một nhánh `claude/pwa-m<N>`, không giẫm file chung (xem AGENTS.md "Đồng bộ giữa các phiên"). M1 và M2 độc lập, chạy song song được.
