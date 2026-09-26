# STATE — Hiện trạng ThachLab (cập nhật 26/09/2026)

File này là bản mô tả hiện trạng dùng chung cho mọi phiên Claude. Cập nhật sau mỗi đợt lớn.

## Hạ tầng
- Next.js App Router + TypeScript + Tailwind v4, `output: "export"` (xuất tĩnh), deploy bằng `scripts/deploy.sh` → nhánh `deploy`.
- Supabase project `fxnqgmfqdbvnjawgnsfi`, **region Sydney (ap-southeast-2)** → mỗi round-trip từ VN ~100–150 ms.
- Công thức: **KaTeX 0.17** (không phải MathJax).
- Font tự host qua `next/font` (Be Vietnam Pro 400/600/700/800, Inter 400/500/600, JetBrains Mono 400).
- 56 route `page.tsx`, 69 trang tĩnh khi build.
- Học liệu tĩnh: `scripts/build-content.mjs` chạy ở `prebuild`, xuất `public/data/` (catalog + 116 file bài). Sửa lý thuyết phải **deploy lại** mới lên web.

## Đã hoàn thành
- **Đợt tối ưu tốc độ (perf, 24–25/09)**: Lighthouse trang chủ 68→91, trang bài 78→83; `out/` 41→34 MB; ảnh 4,6 MB→0,6 MB; bỏ Google Fonts; Supabase request trang bài 10→4. Chi tiết: `perf/RESULT.md`.
- **Đợt Giai đoạn 0–1 (feat, 25/09)**: cột `difficulty` + `difficulty_source`, UI chọn mức ở Đăng đề, backfill bằng AI; nạp bundle lý thuyết lớp 12; RPC `get_lesson_mastery` / `get_chapter_mastery` + nhãn Nắm vững / Cần luyện thêm / Chưa đạt. Chi tiết: `feat/RESULT.md`.
- Hệ thống Rank/RP 7 bậc (Tinh Quang → Chí Tôn), nhiệm vụ hằng ngày, chuỗi ngày.

## ĐANG CHỜ — 5 migration CHƯA chạy trên production
Chạy bằng SQL Editor hoặc `supabase db query --linked -f <file>`. **Không dùng `supabase db push`** (thư mục `supabase/migrations/` mới, CLI không biết 99 migration cũ).

| # | File | Nội dung |
|---|---|---|
| 1 | `20260925120000_perf_indexes.sql` | 7 index cho truy vấn nóng |
| 2 | `20260925130000_perf_rpc_gv.sql` | 5 hàm RPC tổng hợp cho trang GV |
| 3 | `20260925140000_perf_rls.sql` | 85 policy: `auth.uid()` → `(select auth.uid())`; rollback ở `perf/rollback/` |
| 4 | `20260925150000_difficulty_source.sql` | cột `question_bank.difficulty_source` + vá 3 hàm |
| 5 | `20260925160000_mastery.sql` | 2 hàm mastery |

Sau đó chạy backfill: `npx tsx scripts/backfill-question-bank-difficulty.mts 20` (thử nhỏ trước — script **ghi thật ngay, không có dry-run**), rồi chạy không giới hạn cho ~3541 câu còn thiếu mức độ.

## CHƯA làm (đợt kế tiếp — prompt `prompt-giai-doan-1-2.md`)
- `/luyen-tap` có bộ lọc Lớp → Chương → Bài → YCCĐ → Dễ/TB/Khó (route chưa tồn tại).
- Thẻ "3 kỹ năng yếu nhất" trên dashboard học sinh + trọng số mức độ trong mastery.
- Bổ sung câu hỏi chương Động học 10 cho đủ ≥30 câu/bài.
- `/lo-trinh` — Learning Journey (route chưa tồn tại).

## Lỗ hổng bảo mật cần vá sớm (perf/RESULT.md §9)
1. 2 policy tautology `e.course_id = e.course_id` trên `attendance_sessions` và `equipment_breakdown_reports` → SV đọc chéo được mọi khoá.
2. `class_assessments` policy `using (true)` — mọi tài khoản đăng nhập đọc được toàn bảng.

## Việc ngoài roadmap đang treo
- Chuyển Supabase sang Singapore (lợi ~3–4× độ trễ).
- Tách KaTeX (290 KB) + framer-motion (139 KB) khỏi JS ban đầu của `/lop-hoc/bai` và `/kiem-tra/lam` (2 trang này vẫn ~1,4 MB).
- Cache header cho ảnh png/jpg/webp trong `.htaccess`.
- Cột `updated_at` cho `lessons`/`lesson_items` để lớp tĩnh biết lý thuyết đã sửa.
