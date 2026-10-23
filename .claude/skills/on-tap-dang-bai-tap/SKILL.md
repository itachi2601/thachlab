---
name: on-tap-dang-bai-tap
description: Chuẩn bị phần "ôn các dạng bài tập" của Ôn tập theo chặng cho MỘT chương — gán từng câu bài tập trong ngân hàng vào đúng dạng trong mục Bài tập mẫu của bài (bảng question_dang, Claude đọc từng câu qua subagent Sonnet), kiểm mẫu, nạp DB, rồi thầy/trợ giảng tạo buổi ôn theo bài để thấy cả lớp vướng dạng nào. Dùng khi thầy nói "gán dạng cho chương X", "làm ôn dạng bài tập cho lớp 11/10", "mở rộng ôn dạng sang chương khác", "dạng nào còn thiếu câu", "/on-tap-dang-bai-tap". KHÁC soan-bai-tap-mau (soạn dạng mới) — skill này dùng các dạng ĐÃ có.
---

# Ôn dạng bài tập — gán dạng cho câu ngân hàng

**Bối cảnh (23/10/2026, thí điểm Chương 3 lớp 12 — chương id 4):** "dạng" = các nhãn `Dạng N · Mức · tên` trong `lesson_items.questions` (kind `bai_tap_mau`) của bài. Câu ngân hàng chỉ gắn yêu cầu cần đạt (YCCĐ) và **nhiều dạng dùng chung một YCCĐ**, nên không tách được dạng nếu không gán riêng. Gán xong lưu ở `question_dang(question_id, lesson_id, dang_label, unsure)`; app dựng đề bằng `review_build_dang_exam`, bảng điều phối hiện `by_dang`. Chi tiết thiết kế + trạng thái: `docs/memory/project_thachlab_on_tap_theo_chang.md`. Migration `20261023120000_on_tap_dang_bai_tap` đã chạy — **không cần migration mới khi mở rộng sang chương khác, chỉ cần nạp thêm dữ liệu**.

## Quy trình (chạy trên Mac, Terminal panel)

Thư mục làm việc = scratchpad của phiên (không để trong repo). `W` bên dưới là thư mục đó.

1. **Xuất dạng + câu ứng viên.** `bash .claude/skills/on-tap-dang-bai-tap/scripts/lay-dang.sh <chapter_id> $W`, rồi chạy 3 lệnh `supabase db query … > $W/*.json` nó in ra, **từ gốc repo, trong tab terminal** (Bash bị chặn `*.supabase.co`; CLI chỉ in câu cuối nên đã tách mỗi truy vấn một file). Chỉ đọc, không ghi DB.
2. **Xem trước các dạng.** Đọc `dangs.json`: bài nào dạng là **tình huống ứng dụng cụ thể** (đàn ghi ta, bếp từ, Foucault…) thì ngân hàng gần như không có câu khớp — đưa vào `--bo-bai` (hoặc `--chi-giu` ở bước 5) để khỏi gán rộng.
3. **Chia nhóm.** `python3 .claude/skills/on-tap-dang-bai-tap/scripts/chia-nhom.py $W [--bo-bai <lesson_id>…]` → `$W/in/<bài>_<chủ đề>.json`, mỗi file ≤80 câu (xáo ngẫu nhiên).
4. **Gán dạng bằng subagent.** Mỗi file `in/` một subagent `general-purpose` model `sonnet`, chạy song song (file nhỏ gộp chung một agent); prompt = `references/prompt-gan-dang.md` (điền đường dẫn). Subagent đọc từng câu và ghi `out/<tên>.json`; **cấm heuristic từ khoá**. Dữ liệu chỉ có câu hỏi, không có định danh học sinh nên được phép dùng subagent.
5. **Kiểm mẫu bằng mắt (bắt buộc, đừng bỏ).** In ~4–8 câu mỗi dạng cho các nhóm lớn (đặc biệt nhóm gán dồn một dạng — ví dụ 60/80 vào Dạng 1 là dấu hiệu gán quá rộng) và đối chiếu với `problem` của dạng. Sai thì sửa/loại: `--chi-giu BAI:ID` ở bước 6, hoặc cho subagent chạy lại với dặn rõ hơn.
6. **Sinh SQL.** `python3 .claude/skills/on-tap-dang-bai-tap/scripts/tao-sql.py $W scripts/sql/gan-dang-<chuong>.sql [--chi-giu BAI:ID…]` (kiểm đủ id; in số câu mỗi dạng, kể cả `unsure`). Câu `unsure` vẫn lưu nhưng **không dùng để dựng đề**.
7. **Chạy thử trong giao dịch hoàn tác** (đã chứng minh bắt được lỗi): ghép file SQL + `select set_config('request.jwt.claim.sub', <id admin>, true)` + gọi `review_dang_pool(bài)`, `review_build_dang_exam(<lớp>, <bài>, 3)`, `review_create`, `review_board`, kết thúc `rollback;`. Dùng bảng tạm để in kết quả vì CLI chỉ in câu cuối.
8. **Nạp thật.** Thêm file vào mảng `FILES` của `scripts/run-migrations.sh` (nối thêm, không sắp lại) → `bash scripts/run-migrations.sh --yes --only N` trong tab terminal → kiểm `select count(*), count(*) filter (where unsure) from question_dang`. Rollback: `delete from public.question_dang where source = 'claude-2026-10-23';` (đổi `source` nếu lượt khác).
9. **Báo thầy** số câu mỗi dạng, **dạng nào thiếu câu (<3 câu chắc chắn)** — chỗ đó cần soạn/tìm thêm câu hoặc gán rộng hơn (mỗi chủ đề mới xét ≤80 câu). Cập nhật `docs/STATE.md` (một dòng), file memory `project_thachlab_on_tap_theo_chang.md`; commit đúng đường dẫn; chạy `node scripts/gen-database-doc.mjs` nếu đổi schema.

Dùng trong app: `/tro-giang/on-tap/` → chọn lớp + chương → mục "Ôn các dạng bài tập — mỗi bài một chặng". Mỗi bài thành một chặng, mỗi dạng bốc k câu (mặc định 3); bảng điều phối hiện khối "Cả lớp vướng ở dạng nào".

## Giới hạn đã biết
- Bài mới chưa có Bài tập mẫu/dạng → không có gì để gán. Soạn dạng bằng skill `soan-bai-tap-mau` trước.
- Nhãn khớp theo **chuỗi label** của dạng; sửa/đổi tên dạng trong Bài tập mẫu sau này làm câu đã gán mất liên kết → gán lại bài đó.
- Chưa có "ôn lại" tự động và chưa chuyển dạng yếu sang phụ đạo (thầy tự chiếu câu sai).

## Nhật ký rút kinh nghiệm
- 2026-10-23 · Mẻ đầu dồn 60/80 câu Faraday chung vào "Dạng 1 · Đàn ghi ta điện" (bài ứng dụng) → dạng ứng dụng cụ thể chỉ nhận câu đúng bối cảnh; kiểm mẫu từng nhóm lớn trước khi nạp; bài như vậy dùng `--bo-bai`/`--chi-giu`.
- 2026-10-23 · Viết hàm insert vào `exams` bị lỗi vì `question_count` và `type_counts` là cột sinh → chạy thử trong giao dịch hoàn tác trước khi chạy thật; đừng insert hai cột này.
- 2026-10-23 · `supabase db query` chỉ in kết quả câu cuối và cần chạy từ gốc repo (không nhận project ở thư mục khác); mỗi truy vấn một file; terminal chặn dấu ngoặc đơn trong lệnh inline → để SQL vào file `-f`.
- 2026-10-23 · Giả định "dạng = YCCĐ" suýt thành cả migration sai → đọc vài dòng dữ liệu thật của đúng thứ thầy gọi tên trước khi thiết kế.
