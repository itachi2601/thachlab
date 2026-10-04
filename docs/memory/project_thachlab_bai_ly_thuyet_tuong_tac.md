---
name: project-thachlab-bai-ly-thuyet-tuong-tac
description: Skill soan-bai-ly-thuyet-tuong-tac + bài mẫu Định luật III Newton (lớp 10) + kho thí nghiệm content/thi-nghiem — soạn 2026-10-01, PR #22 chờ merge, bài CHƯA lên web (thầy vẫn thấy bài cũ)
metadata:
  type: project
---

## Mục tiêu
Bài LÝ THUYẾT tương tác để thầy **chiếu giảng trực tiếp** và học sinh **tự học lại** (không phải video). Ba thói quen dạy của thầy là bắt buộc trong mọi bài (2026-10-01): (1) mỗi kiến thức kèm ví dụ/thí nghiệm (`.tl-box--exp`: Làm–Quan sát–Rút ra); (2) mục "Trả bài" lý thuyết/công thức trước khi giải bài tập; (3) bài toán mẫu đọc đề từng câu theo bảng *Câu trong đề / Dữ liệu / Kiến thức liên quan* (`.tl-table--data`) rồi mới lời giải. Mở bài bằng tình huống đời thường (bài mẫu: sân băng). Các thí nghiệm ghi vào kho dữ liệu làm đầu vào cho giai đoạn **Mô phỏng** (chưa bắt đầu).

## Đã xong (nhánh `claude/ecstatic-noether-4hpb1z`, working tree sạch, đã push, HEAD `e6ae1d7`)
- Skill `.claude/skills/soan-bai-ly-thuyet-tuong-tac/` (SKILL.md, references/, assets/ gồm CSS bản sao + bài mẫu, scripts/: `lint_theory.py`, `thi_nghiem.py`, `validate_bundle.mts`, `preview.mjs`, `svg_lib.py`) + file cài `dist-skills/soan-bai-ly-thuyet-tuong-tac.skill`.
- CSS `.tl-*` cuối `app/globals.css` (radio + `:checked`/`:has()`, `<details>`, hộp, bảng dữ liệu). **Không có CSS này trên bản deploy thì bài hiện trơ, không tương tác.**
- Bài mẫu `content/lesson-samples/l10-dinh-luat-3-newton/` (`theory.html` 6 mục, 4 hình SVG tự vẽ, 4 quiz, 8 details; `bundle.json` hợp lệ `validateBundle`; `build_figs.py` sinh hình).
- Kho `content/thi-nghiem/` 6 mục `tn-l10-newton3-01..06.json` + `README.md` quy ước + `index.json` (sinh tự động); bài liên kết bằng `data-exp="<id>"`. Số liệu mẫu **tính từ mô hình (g=9,8), chưa phải số đo thật**; tham số min/max/ma sát 0,03 là em tự đề xuất, **thầy chưa duyệt**.
- Bản xem thử độc lập (Artifact, riêng tư): https://claude.ai/artifact/YMp9CJQTFoDkZvcvGzHqmj (v2; công thức MathML, không phải KaTeX/app thật).
- PR https://github.com/itachi2601/thachlab/pull/22 → `main`, đã merge `origin/main` vào nhánh không xung đột, `tsc --noEmit` sạch. **Chưa merge** (thầy quyết).

## Còn chờ
1. **Thầy merge PR #22** — nếu không, phiên cloud mới (tải từ `main`) không thấy skill/CSS/kho thí nghiệm; CSS cũng không lên deploy nếu deploy từ `main`.
2. **Bài chưa lên web.** Thầy báo bài lớp 10 chương 3 "Định luật 3 Newton" vẫn là bài cũ. Đích đăng dự kiến `lesson_id=61` (URL `.../lop-hoc/bai/?id=61&subject=vat-ly&chapter=12&class=lop-10`). ⚠ `chapter=12` là **id chương trong CSDL, không phải số chương theo chương trình** (em từng hiểu nhầm); id 61 nhiều khả năng đúng là Định luật 3 Newton (id 58 = Bài 13 Tổng hợp và phân tích lực) nhưng **chưa xác nhận tên bài** — script upload in `Bài học #61 "<tên>"`, kiểm tên trước. Chưa rõ thầy đã chạy `upload-lesson.mts` chưa. Chẩn đoán đã đưa thầy: (a) dòng `Lý thuyết: ghi đè` khi upload; (b) `node scripts/build-content.mjs && grep -c "tl-quiz" public/data/lessons/61.json` (0 = DB chưa có bài mới; >0 = lỗi ở deploy); (c) deploy từ đúng nhánh (nhánh có CSS, hoặc `main` sau merge #22). **Chưa nhận kết quả** từ thầy.
3. Lệnh đăng (thay thế mục lý thuyết + xoá đề Luyện tập cũ của bài; thầy đã đồng ý ghi đè): `cp public/data/lessons/61.json ~/Desktop/bai61-backup.json` trước, rồi `npx tsx scripts/upload-lesson.mts content/lesson-samples/l10-dinh-luat-3-newton/bundle.json --lesson 61 --target luyen_tap`, rồi `bash scripts/deploy.sh`. Không xoá mục Bài tập mẫu khác của bài (script không đụng).
4. **Mới trên main (hook phiên 2026-10-01):** `docs/CLOUD-GHI-DB.md` — hook báo "mạng thông, service key có → ĐĂNG/SỬA BÀI ĐƯỢC từ cloud (upload-lesson.mts, update-*.mts)". Phiên sau nên đọc file đó; nếu đúng thì có thể tự chạy upload bài 61 từ cloud (sau khi xác nhận tên bài + sao lưu, và thầy đồng ý ghi đè) thay vì bắt thầy chạy Mac. Lưu ý trước đó trong phiên này Supabase bị chặn nên em đã nói sai là "không đăng được từ cloud".
5. Mục "Cần kiểm tra khi thầy xem được bài mẫu" cuối SKILL.md còn trống (radio có sống trong app Next.js thật không, `<details>` trên điện thoại, độ dài bài, kiểu hình que có chấp nhận không, giọng văn) — điền sau khi thầy xem bản đăng thật.
6. Trên Mac: `bash scripts/sync-skill.sh soan-bai-ly-thuyet-tuong-tac` (sang Library plugin + `~/.codex`).
7. Thí nghiệm 05, 06 chưa có hình trong bài; chưa có mô phỏng nào.

## Quyết định đã chốt (code không tự suy ra)
- HTML lưu DB cấm `<script>`, `<style>`, `on*=` (`checkTags` trong `services/lesson-import.ts`) → tương tác chỉ bằng `<details>` + radio/CSS; cấu trúc `.tl-quiz` (input/label/`.tl-fb` là anh em trực tiếp, id duy nhất toàn trang, tiền tố `tl<bài>-q<câu><đáp án>`) rất nhạy.
- Không dùng ảnh sách Halliday (bản quyền, trang công khai) → vẽ lại SVG tự vẽ; không ảnh raster (quy tắc tốc độ trong AGENTS.md).
- Bundle bắt buộc có `exam` ≥1 câu → dùng chính các câu tự kiểm tra làm đề Luyện tập 3 câu.
- Cloud xem thử bài: Artifact CSP chặn stylesheet ngoài → KaTeX phải render MathML trước, không tải CSS KaTeX.

## Đợt 2026-10-04 — nốt 13 bài Vật lí 12 bằng subagent song song (phiên DSH trên Mac)
- **Đã đăng DB (chỉ mục Lý thuyết, `cap-nhat-ly-thuyet.sh --yes`, log `scripts/logs/dang-13-bai-l12-*.log`)**:
  id 6, 7, 8, 9 (Khí lí tưởng) · 10, 11, 125, 127 (Từ trường) · 15, 16, 17, 18, 19 (Hạt nhân). Mỗi bài có
  `content/lesson-samples/l12-<slug>/` (theory.html + theory.src.html + build_figs.py + build_bundle.py +
  bundle.json) và 2–4 file `content/thi-nghiem/tn-l12-*.json`. Trừ đúng các bài Kiểm tra và hai bài Thực hành
  đo (id 5, id 12 — id 5 do phiên khác làm rồi).
- **Cách làm (đã ghi vào SKILL.md, mục "Làm nhiều bài một đợt")**: 1 bài chạy thử một mình → 3 lô song song
  (3+5+5 bài) → 1 vòng kiểm lại 5 bài. Mỗi bài: subagent soạn → subagent **kiểm chéo độc lập** (giải lại từng
  quiz, tính lại số liệu, soi toạ độ SVG) → subagent sửa. ~50 lượt subagent, ~2 giờ. Mọi bài đều có ≥1 lỗi
  `chan` do kiểm chéo bắt; 5 bài phải sửa 2 vòng (6, 7, 10, 16, 19).
- **Bài học**: (1) đưa NGUYÊN danh sách lỗi cho agent sửa — cắt JSON ở 4 000 ký tự làm nó bỏ sót nửa danh
  sách; (2) yêu cầu sửa cả `nen_sua`, không chỉ `chan`; (3) `xem-thu/` 43 MB cho 13 bài → **không commit**,
  sinh lại bằng `build_preview.py` + `chup_anh.py`; (4) `chup_anh.py` nay tự cắt mục >5 000 px thành
  `sec-2a/sec-2b…` (WebP trần 16 383 px, trước đó script chết giữa vòng).
- **Xung đột phiên**: bài 15 (id 126) đã bị phiên khác soạn + đăng trước (`l12-ung-dung-cam-ung/`) → không ghi
  đè; bản của phiên này `l12-ung-dung-cam-ung-dien-tu/` để nguyên chưa đăng. Trước khi đăng luôn `select` lại
  `lesson_items` để biết bài nào vừa bị phiên khác đăng.
- **Còn lại**: deploy (site tĩnh build đọc DB); cân nhắc bộ "Kiểm tra nhanh" 20 câu cho từng bài
  (`scripts/data/theory-quiz/<id>.json`, hiện mới có 32 và 58).
