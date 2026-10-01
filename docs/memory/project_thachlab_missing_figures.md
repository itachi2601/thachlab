---
name: project_thachlab_missing_figures
description: "Đề mất hình (đồ thị/hình vẽ) — đã xong 25/9/2026 cả chặn từ nguồn, bộ lọc, Tải ảnh, AI vẽ đồ thị (draw-figure + figure-spec.ts), Không cần hình, sửa hash/gộp trùng; còn treo — thầy duyệt 80 hình AI + xử lý 43 câu AI không vẽ được, (bảng backup đã xoá 28/9)"
metadata:
  node_type: memory
  type: project
  originSessionId: b0a9733a-e24e-4c14-82db-139261ec5d38
  modified: 2026-09-25T16:12:07.894Z
---

**Mục tiêu:** ngân hàng câu hỏi có ~90 câu ghi "đồ thị / hình vẽ" nhưng mất hình khi số hoá; chặn không phát sinh
thêm và khôi phục hình cho câu cũ với ít công tay nhất. Toàn bộ code đã commit lên `main` và deploy (bản mới
nhất của phiên này: e814cec2, 2026-09-25; các phiên khác đã commit/deploy tiếp sau đó).

## Đã xong (2026-09-25)

**Chặn từ nguồn (commit 18c39c2d):**
- `services/question-figures.ts`: helper "câu nhắc hình mà không có ảnh" (regex `FIGURE_WORDS_PG` dùng chung
  cho client và bộ lọc PostgREST `imatch`).
- `services/exam-latex-parser.ts`: `\includegraphics` → `<img src="media/…">` (bundle phải khai báo
  raster_images), tikzpicture → mốc ⟦hình TikZ⟧ + cảnh báo. `services/docx-reader.ts`: shape/chart/group
  của Word → mốc ⟦hình vẽ Word⟧ + cảnh báo Paste Special → Picture.
- Trang Đăng đề / Nhập bài / CNC đăng đề: khung đỏ `components/admin/MissingFigureNotice.tsx`, khoá nút Đăng
  tới khi tick xác nhận (ack gắn với bundle: đổi file là phải tick lại).
- Skill azota + ngan-hang-cau-hoi (bản ~/.codex; bản synced azota cũng có convert_docx.py nhưng cũ hơn, thiếu fix
  gridSpan): sau `doc.save` gọi `cd.chuyen_anh_vector_sang_png()` — EMF/WMF ảnh thật → PNG bằng LibreOffice
  headless, bỏ qua ảnh xem trước MathType trong w:object.

**Ngân hàng câu hỏi `/quan-tri/ngan-hang-cau-hoi` (commit 797f63af, 396ee2e8, c9f85387, 3ced896e, a841b974, 91be7601, e814cec2):**
- Mục "Nhắc hình, thiếu ảnh" trong cây bên trái (server lọc + client rà lại; bỏ câu `figure_not_needed`).
- Nút "Tải ảnh": `services/question-bank-figure.ts` nén → upload `lesson-media/bank/<id>` → RPC
  `bank_set_question_figure(p_bank_id, p_img_html)` (docs/supabase-migration-question-bank-figure.sql +
  -figure-ai.sql) chèn <img>/<svg> vào câu dẫn của dòng ngân hàng VÀ mọi `exams.questions` đang dùng câu đó
  (so content_hash cũ; hash đích lấy theo bản trong đề để trigger sync cập nhật tại chỗ, không sinh trùng).
- Nút "AI vẽ hình" + "AI vẽ cả danh sách": Edge Function `supabase/functions/draw-figure/index.ts`
  (claude-sonnet-5, tool use bắt buộc) trả THÔNG SỐ đồ thị, `services/figure-spec.ts` kiểm tra + vẽ SVG
  (sinusoid/polyline/hyperbola/exponential, điểm, đường gióng). QUYẾT ĐỊNH: không để AI tự viết <path> vì
  lần đầu vẽ ngược pha; SVG tự do chỉ cho hình không phải đồ thị hàm số và khung xem trước ghi rõ. Server tìm
  figure/svg ở mọi tầng kết quả tool (model hay bọc nhầm khoá). Kết quả lưu `question_bank.ai_figure` để duyệt
  trên máy khác: Dùng hình này (RPC xoá cột) / Vẽ lại / Bỏ. Hàm trả `usage`; đo thực ≈ 0,011 USD/đồ thị,
  0,019 USD/SVG tự do.
- Cột `figure_not_needed` + nút "Không cần hình"/"Cần hình".

**Bug hash/difficulty (commit 6379f327, docs/supabase-migration-question-bank-hash-fix.sql đã chạy prod):**
`question_content_hash()` loại thêm `difficulty` (trigger touch chèn khoá này vào question nên hash lệch → mỗi
lần đăng lại đề sinh dòng trùng). Gộp 10 780 → 7 215 dòng, không mất nhãn (đối chiếu backup).

**Dữ liệu đã xử lý 2026-09-25:**
- Chạy "AI vẽ cả danh sách" cả 3 khối: lớp 12 59 câu → 37 hình / 22 không đủ dữ kiện; lớp 11 45 → 36 / 9;
  lớp 10 19 → 7 / 12. Tổng 80 hình đang chờ thầy duyệt (18 là SVG tự do — có hình vẽ sai góc).
- 9 câu đề 109 (Thực hành động lượng lớp 10) đã gắn ảnh bố trí thí nghiệm lấy từ lý thuyết bài (lesson-media/75
  fig02 = va chạm mềm, fig03 = va chạm đàn hồi) qua RPC.
- 2 câu đề 107 mất cả 4 hình phương án: đã lưu trữ trong ngân hàng (id 274736, 274743) và XOÁ khỏi đề 107
  (73 → 71 câu; đề chưa có bài làm; source_index ngân hàng đã cập nhật). Backup 73 câu chỉ nằm trong scratchpad
  phiên cũ — mất khi phiên đóng, coi như không có.

## Còn treo

- Thầy duyệt 80 hình AI ở mục "Nhắc hình, thiếu ảnh" từng khối (chưa duyệt câu nào).
- 43 câu AI không vẽ được: ảnh thiết bị/thí nghiệm thực (nhiệt kế hồng ngoại, máy sưởi, ống chữ U, cầu chì…),
  sơ đồ ống dây/khung dây/vòng dây cần chiều dòng điện, quỹ đạo hạt beta, chu trình p–T thiếu toạ độ → cần
  "Tải ảnh" thật hoặc lưu trữ; câu lý thuyết hỏi dạng đồ thị chung (nhiều ở đề 43/44/45 lớp 11, 169, 157, 137)
  → thầy bấm "Không cần hình". Một câu đề 85 lỗi định dạng → "Vẽ lại".
- Bảng `public.question_bank_backup_20260925`: ĐÃ XOÁ 28/9/2026 10:55 (migration 20260928150000_drop_question_bank_backup.sql).
- Bản synced `azota/scripts/convert_docx.py` cũ hơn bản ~/.codex; synced ngan-hang-cau-hoi không có thư mục scripts.
- Lint có sẵn 2 lỗi `set-state-in-effect` ở QuestionBankAdmin (reloadTree/reloadItems), không phải của đợt này.
- Supabase CLI `supabase db query` thỉnh thoảng treo vài phút → chạy nền, thống kê bằng SQL file trong scratchpad.

Liên quan: [[project_thachlab_question_bank]], [[project_thachlab_dang_de_azota]], [[project_thachlab_azota_skill]],
[[project_thachlab_ngan_hang_cau_hoi_skill]], [[project_thachlab_concurrent_sessions]], [[reference_supabase_db_query_cli]].
