---
name: project_thachlab_cau_tuong_tu_dung_dang
description: "Bài tương tự" ở Bài tập mẫu lấy đúng dạng qua question_dang + biến thể đổi số; đã đăng 2026-11-05, còn 218 dạng tính toán thiếu câu
metadata:
  type: project
---

**Mục tiêu:** nút "bài tương tự" dưới lời giải mỗi dạng Bài tập mẫu phải ra câu ĐÚNG dạng (trước 2026-11-05 lọc theo YCCĐ + `question_bank.form` — cột này chỉ là `bai_tap`/`ly_thuyet` nên ra câu khác dạng).

**Đã xong, đã ghi DB + deploy prod 2026-11-05:**
- Chặng 1: RPC `get_similar_dang_questions(p_lesson_id, p_dang_no, …)` (migration `20261105120000_similar_dang_questions.sql`) chỉ đọc `question_dang` `unsure=false`, khớp SỐ "Dạng N" (không khớp cả nhãn). UI `SimilarBankPractice.tsx`/`WorkedQuestionsGrid.tsx`: rỗng → câu cùng chủ đề có nhãn "chưa phân dạng"; không bù câu khác dạng.
- Chặng 2: 20 file mới `scripts/sql/gan-dang-*.sql` (file 82–101 trong `run-migrations.sh`; cộng 5 file 55–59 nạp 22–24/10 = 25 file `gan-dang-*` trên main) → `question_dang` 1.573 → 5.039 dòng. Bảng dạng thiếu câu: `docs/dang-thieu-cau.md`.
- Chặng 3A: `lib/bien-the.ts` + `components/lessons/VariantPractice.tsx` + `scripts/kiem-bien-the.mts`; trường `bien_the` trong `LessonWorkedQuestion`; hướng dẫn soạn `.claude/skills/soan-bai-tap-mau/references/bien-the.md`. Thí điểm bài 18 D2/D4/D5 — CHƯA ghi vào lesson_items DB nên HS chưa thấy.
- Chặng 3B: 95 câu mới cho 26 dạng lý thuyết (`question_bank.note = 'soan-dang-thieu-ly-thuyet-20261105'`, nguồn `scripts/data/soan-cau-dang-thieu/`); thầy bảo "đăng luôn" = duyệt.
- Chặng 4: `docs/do-cau-tuong-tu-2026-11-05.md` — 82/88 đúng dạng (93,2%); đã đặt unsure 6 câu lệch (sao lưu `question_dang_bak_20261105_do`, commit 5873a9f18). L11 lesson 38 Dạng 4 giờ 0 câu.

**Còn chờ:**
- Thầy xem thử 3 dạng biến thể bài 18 → rồi mới ghi DB và viết `bien_the` cho 218 dạng tính toán <3 câu (134 dạng 0 câu; nặng nhất HSG9 Điện, HSG9 Quang, KHTN9 Điện).
- Chưa bấm thử bằng tài khoản HS thật; chưa đo lại tỉ lệ sau khi gỡ 6 câu.

**Quyết định đã chốt:** không sinh câu bằng AI lúc HS học (tốn credit, không kiểm được một đáp án); dạng tính toán dùng đổi số chạy ở trình duyệt, dạng lý thuyết soạn sẵn trong phiên Mac. Ghi ~3.500 dòng tra theo khoá chính được chạy ban ngày (quy tắc 22h dành cho hàng chục nghìn dòng).

**Rút kinh nghiệm 2026-11-05:** chia nhiều phiên song song cùng đụng một file (`WorkedQuestionsGrid.tsx`, `run-migrations.sh`, `STATE.md`) → workflow tự gộp xung đột hoặc huỷ lượt chờ; phiên xong sau phải `git merge origin/main` trước khi push và xem `gh run list --workflow gop-claude-vao-main.yml`. Đã thêm thành quy tắc trong AGENTS.md (mục Đồng bộ giữa các phiên, 7/11/2026). Liên quan [[project_thachlab_on_tap_theo_chang]].
