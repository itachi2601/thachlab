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
- Danh vị Vô Song (Paragon) trên Chí Tôn: migration `20260926100000_rank_paragon.sql` ĐÃ chạy 26/9/2026 (rollback `perf/rollback/…rank_paragon.down.sql`); chế độ admin "Xem như học sinh" mở khoá hết (features/rank/preview.ts).
- Loại GV/admin khỏi rank RP: migration `20260926110000_rank_exclude_staff.sql` ĐÃ chạy 26/9/2026 — chặn tận gốc (3 hàm) việc tài khoản không phải role='student' bị cộng RP/lọt bảng xếp hạng khi tự test bài, đã dọn sạch dữ liệu rác (rollback `perf/rollback/20260926110000_rank_exclude_staff.down.sql`).
- Vá 2 lỗ hổng RLS tautology + `class_assessments using(true)`: migration `20260926140000_fix_rls_tautology.sql` ĐÃ chạy 26/9/2026 (rollback `perf/rollback/20260926140000_fix_rls_tautology.down.sql`).

## Migration — ĐÃ CHẠY XONG (26/09/2026, 17:28)
Cả 7 file trong `supabase/migrations/` đã chạy lên production qua `bash scripts/run-migrations.sh`
(log ở `scripts/logs/20260926-170957-*`): perf_indexes, perf_rpc_gv, perf_rls, difficulty_source,
mastery, lesson_item_draft_publish, exam_violation_alert. Cộng rank_paragon và rank_exclude_staff
chạy trước đó trong ngày. Rollback từng file ở `perf/rollback/`.

**Không còn migration nào chờ.** Khi có file mới, agent cập nhật mảng `FILES` trong
`scripts/run-migrations.sh` theo quy tắc ở `AGENTS.md`.

## Việc tay còn lại
- [ ] **Backfill mức độ câu hỏi** — còn ~3541/7223 câu `question_bank.difficulty` rỗng.
  Script **ghi thật ngay, không có dry-run**; tham số chỉ giới hạn số câu:
  `npx tsx scripts/backfill-question-bank-difficulty.mts 20` (thử nhỏ, xem lại
  `/quan-tri/ngan-hang-cau-hoi`, rồi chạy không giới hạn). Tốn API Anthropic (~90 lô × 40 câu).
- [ ] **Kiểm hồi quy bằng tài khoản thật** — cả 2 đợt tối ưu đều chưa làm được (agent không đăng
  nhập được). Đợt 2 có động vào `AuthProvider` nên cần kiểm kỹ: HS làm một đề, GV xem gradebook +
  phụ đạo, admin vào đăng đề, trang Rank, một trang CNC.
- [ ] **Đo lại Lighthouse trên máy thật** — Agent D đo trong sandbox dùng chung nên số không so
  được với mốc ban đầu. Chạy PageSpeed Insights trên site thật sau khi deploy.

## CHƯA làm (đợt kế tiếp — prompt `prompt-giai-doan-1-2.md`)
- `/luyen-tap` có bộ lọc Lớp → Chương → Bài → YCCĐ → Dễ/TB/Khó (route chưa tồn tại).
- Thẻ "3 kỹ năng yếu nhất" trên dashboard học sinh + trọng số mức độ trong mastery.
- Bổ sung câu hỏi chương Động học 10 cho đủ ≥30 câu/bài.
- `/lo-trinh` — Learning Journey (route chưa tồn tại).

## Việc ngoài roadmap đang treo
- Chuyển Supabase sang Singapore (lợi ~3–4× độ trễ).
- Tách KaTeX (290 KB) + framer-motion (139 KB) khỏi JS ban đầu của `/lop-hoc/bai` và `/kiem-tra/lam` (2 trang này vẫn ~1,4 MB).
- Cache header cho ảnh png/jpg/webp trong `.htaccess`.
- Cột `updated_at` cho `lessons`/`lesson_items` để lớp tĩnh biết lý thuyết đã sửa.
