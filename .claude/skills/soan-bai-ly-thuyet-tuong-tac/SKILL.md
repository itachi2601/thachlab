---
name: soan-bai-ly-thuyet-tuong-tac
description: Soạn một bài LÝ THUYẾT có tương tác cho thachlab theo phong cách thầy Thạch — luôn mở bằng ví dụ đời thường, có câu dự đoán, mục bấm-mở, trắc nghiệm tự chấm ngay trong bài, hình SVG tự vẽ (không ảnh nặng) — rồi đóng gói thành theory.html + bundle.json để đăng. Dùng khi thầy nói "soạn bài lý thuyết tương tác", "tạo bài lý thuyết có ví dụ thực tế", "làm bài học mới cho chương X", "vẽ hình cho bài lý thuyết". Khác dang-bai-hoc-thachlab (đăng .tex có sẵn) và soan-quiz-ly-thuyet (bộ 20 câu Kiểm tra nhanh cuối bài). Soạn + vẽ + kiểm chạy được trên cloud; ĐĂNG lên DB phải chạy trên Mac.
---

# Soạn bài lý thuyết tương tác

Bài mẫu chuẩn (đã làm, đọc để bắt chước nhịp): `content/lesson-samples/l10-dinh-luat-3-newton/` (`theory.html`, `bundle.json`, `build_figs.py`).
Trạng thái: **mẫu đầu tiên chưa được thầy xem trên web** — mọi quy ước dưới đây rút từ lần làm đó, sẽ chỉnh khi thầy phản hồi (xem mục cuối).

## Quy trình

1. **Chọn bài + nguồn.** Lớp → Chương → Bài (xem `public/data/catalog.json`). Nội dung lấy từ chương trình/SGK làm ý tưởng và số liệu; **không chép nguyên văn, không dùng ảnh của sách có bản quyền** (Halliday, SGK...) trên trang công khai — vẽ lại bằng SVG.
2. **Phiếu bài** (trong đầu/scratchpad): 1 ví dụ đời thường mở bài · khái niệm/định luật + phát biểu chuẩn · công thức + ký hiệu + đơn vị · 1–2 **hiểu lầm kinh điển** của học sinh · 1 ví dụ số · 3–4 ứng dụng đời sống. Hiểu lầm kinh điển là xương sống của bài — chọn đúng chỗ học sinh hay sai.
3. **Viết `theory.html`** theo dàn ý dưới + linh kiện trong `references/linh-kien-html.md`.
4. **Vẽ hình** 2–4 hình SVG theo `references/hinh-svg.md`, dùng `scripts/svg_lib.py` (sinh bằng script, chèn idempotent như `build_figs.py` của bài mẫu).
5. **Kiểm.** `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_theory.py <theory.html>` (lỗi cấu trúc) → `node .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/preview.mjs <theory.html> <thư-mục-ra>` (chụp 375px từng hình + tự bấm mọi đáp án kiểm phản hồi). **Phải xem ảnh bằng mắt** — nhãn chồng chữ/cắt biên không script nào bắt được.
6. **Đóng gói `bundle.json`** (schema `thachlab.lesson-bundle/v1`): `theory_html` + `worked_examples: []` + `exam` gồm các câu tự kiểm tra trong bài (validate bắt buộc ≥1 câu). Chạy `validateBundle` (mẫu: `scripts/_v.mts` trong lịch sử — import `validateBundle` từ `@/services/lesson-import`, đọc bundle, in kết quả; xoá file tạm sau khi chạy). Phải `ok: true`.
7. **Báo thầy** (ngắn): bài gì, hình nào ở đâu, đã kiểm gì. Nhắc lệnh trên Mac:
   ```
   npx tsx scripts/upload-lesson.mts <bundle.json> --lesson <id>   # hoặc dán theory.html vào /quan-tri/bai-hoc → Soạn mục
   bash scripts/deploy.sh      # CSS .tl-* nằm trong app/globals.css — không deploy thì bài hiện trơ, không tương tác
   ```
   Commit chỉ đúng thư mục bài + file đã đụng; không tự đăng DB.

## Dàn ý bài (nhịp 5 phần, mỗi phần là một `<h3>` đánh số I., II.…)

Dùng `<h3>` làm mốc — `wrapTheorySections` cắt đoạn theo `<h3>` để nút "Ôn ngay" của quiz cuộn đúng chỗ. Không dùng `<h2>` "LÝ THUYẾT" ngoài `<h3>`.

| Phần | Nội dung | Linh kiện |
|---|---|---|
| I. Mở bài | Tình huống đời thường gần học sinh (sân băng, xưởng CNC, xe đạp, bếp...), kể bằng giọng thầy, kết bằng câu hỏi "tại sao?" | hộp **dự đoán** (radio) |
| II. Kiến thức | Phát biểu + công thức + ký hiệu; 3–4 gạch đầu dòng ngắn | hộp **định nghĩa** + hình 1 + `<details>` "xem thêm" |
| III. Bẫy | Hiểu lầm kinh điển, vì sao sai; bảng so sánh đúng/sai | bảng + hình 2 + **tự kiểm tra** |
| IV. Tính toán | Ví dụ số nhỏ, số đẹp; lời giải ẩn trong `<details>` | hình 3 + 1–2 câu tự kiểm tra |
| V. Đời sống + tổng kết | 3–4 ứng dụng; 1 thử thách ẩn gợi ý; khung "Mang về sau bài học" 3 ý | `<details>` + hộp định nghĩa |

## Giọng văn thầy Thạch

- Xưng "thầy", gọi "em/các em". Câu ngắn. Mở bằng cảnh thật, **không** mở bằng định nghĩa.
- Có người thật nói câu thật ("Thầy ơi, em đẩy thành chứ có đẩy mình đâu…"). Mẹo nhớ có tên (4 chữ, 1 câu hỏi kiểm tra "đặt lên mấy vật?").
- Sai thì **giải thích vì sao sai** và gợi cách nghĩ lại, không chỉ báo "sai". Đúng thì củng cố lý do.
- Thầy dạy vật lí THPT + CNC/chế tạo máy + trượt băng: ưu tiên ví dụ từ ba mảng đó. Trả lời chung gọn, vào thẳng kết quả.

## Bài học rút ra từ bài mẫu (đừng lặp lại lỗi)

1. **HTML trong DB cấm `<script>`, `<style>`, `on*=`** (`checkTags` trong `services/lesson-import.ts` chặn). Tương tác chỉ bằng `<details>` và radio + CSS `:checked`. CSS nằm ở `app/globals.css` (khối `.tl-*`) — sửa linh kiện = sửa CSS + deploy.
2. **Cấu trúc `.tl-quiz` rất nhạy:** `<input>` ngay trước `<label>` của nó, tất cả + các `.tl-fb` là **anh em trực tiếp** trong cùng `.tl-quiz`. Mỗi câu một `name`; `id` duy nhất toàn trang → đặt tiền tố theo bài (`tl3-q1a`: bài 3, câu 1, đáp án a). Bọc thêm `<div>` giữa chừng là hỏng phản hồi.
3. **Mỗi đáp án sai phải sai chắc chắn.** Bài mẫu suýt có hai đáp án đúng (sách ép bàn/bàn đỡ sách cũng là cặp lực–phản lực). Với mỗi câu: tự trả lời lại từng phương án một, và nhờ subagent kiểm chéo nếu câu khó.
4. **Đáp án đúng cho nhãn `tl-ok`, sai cho `tl-no`** — hiện phản hồi theo `:has()`. Chỉ màu hiện khi đã chọn nên không lộ đáp án trước.
5. **`ContentHtml` xử lý chuỗi:** `<p>` mở đầu bằng "- "/"•" bị đổi thành gạch đầu dòng; chuỗi "...." (≥4 chấm) bị xoá; `<table>` tự bọc `.table-scroll`; `$…$`/`$$…$$` là công thức KaTeX (không dùng `$` cho tiền); số dấu `$` phải chẵn. KaTeX chạy sau khi tải xong → `<details>` đã mở có thể đóng lại đúng lúc render đầu (chấp nhận được).
6. **Hình SVG tự vẽ, không ảnh raster** (quy tắc tốc độ trong `AGENTS.md`): vài KB, không request thêm, nét theo `currentColor` nên tối/sáng đều đọc. Nếu thật sự cần ảnh: `.webp` ≤1200px, ≤150 KB, qua Storage — không base64 trong HTML.
7. **Bundle bắt buộc có `exam` ≥1 câu**; dùng chính các câu tự kiểm tra trong bài làm đề Luyện tập nhỏ (3–5 câu, kèm `explanation`).
8. **Kiểm bằng mắt ở 375px** (thầy học sinh dùng điện thoại): bài mẫu bị cắt nhãn "Thành sân" và chồng chữ "mặt băng"/"em trượt lùi" cho tới khi chụp ảnh mới thấy.
9. **Chưa test trong app thật** (Next.js tĩnh): preview chỉ dùng CSS + KaTeX rời. Khi có trình duyệt xem được `/lop-hoc/bai`, kiểm lại bài đăng thật trước khi nhân rộng.

## Cần kiểm tra khi thầy xem được bài mẫu (điền tiếp)

- [ ] Radio tự chấm hiện đúng trong app thật (không bị React/`ContentHtml` render lại làm mất chọn)?
- [ ] `<details>` mở/đóng ổn trên điện thoại?
- [ ] Độ dài bài (≈20 KB, 5 phần) có vừa ý; mật độ tương tác có quá nhiều/ít?
- [ ] Hình SVG: kiểu que có chấp nhận được hay cần vẽ đẹp hơn?
- [ ] Giọng văn: chỗ nào chưa giống thầy?
