---
name: project-thachlab-latex-skill
description: Skill latex (docx→LaTeX→thachlab) đã thay bằng bản codex có cache công thức + prepare_html.cjs
metadata:
  type: project
---

Ngày 18/09/2026 đã chép đè skill `latex` trong thư mục skills của Claude bằng bản ở `~/.codex/skills/latex` (bản cũ backup ở `skills/.latex-backup-20260918`). Bản mới:

- `equation_store.py` — kho công thức dùng chung `~/.codex/cache/latex-equations-v1/`, băm SHA-256 nội dung OLE, tái dùng phiên âm qua nhiều tài liệu (kho khởi đầu trống, lợi ích tăng dần).
- `prepare_html.cjs` — gọi thẳng `services/latex-converter.ts` + KaTeX của repo để sinh & kiểm HTML, thay cho việc model viết HTML tay khi phần có ảnh/bảng. Đường dẫn `--repo /Users/MAC/Projects/thachlab` đã ghim sẵn trong SKILL.md.
- SKILL.md gọn còn ~47% kích thước cũ.

Hai chỉnh tay sau khi chép đè (đã đồng bộ ngược sang `~/.codex/skills/latex`): ghim `--repo`, và sửa `HOMEWORK` regex trong `split_parts.py` để TỰ LUYỆN / TRẮC NGHIỆM / NĂNG LỰC / CẤP ĐỘ TƯ DUY / PHẦN I-II-III vào `luyen_tap_sach` như bản cũ — thầy chọn vậy, chỉ DẠNG n / VÍ DỤ n / BÀI TẬP MINH HỌA mới là `bai_tap_mau`.

Bổ sung tự viết cùng ngày (có trong cả hai bản):
- `imgtool.py` (Pillow) thay hẳn ImageMagick — máy này **không cài** `convert`, pipeline cũ sẽ chết ở bước render. Contact sheet giờ dựng bằng PIL, thêm phóng to dòng công thức ngắn (min 64px) nên đỡ phải mở lẻ `eNNN.png`.
- Phát hiện ảnh trắng tự động: `report.json.blank_images`, cờ `blank` trong `parts.json`, `prepare_html.cjs` chặn không ra HTML → khỏi duyệt mắt từng `d*.png`.
- `fill_eq.py` tự đổi ảnh trong `tabular` sang `width=2.5cm` (ngoài bảng vẫn `0.6\textwidth`).

Tự kiểm: `python3 <skill>/scripts/test_workflow.py /Users/MAC/Projects/thachlab` — 14/14 OK. Chạy không kèm đường dẫn repo sẽ fail 3 test vì thiếu typescript/katex, không phải lỗi thật.

Liên quan: [[project-thachlab-up-de-skill]], [[feedback-token-discipline]]

## Đường PDF (skill không có sẵn) — 18/09/2026

Skill chỉ nhận `.docx`. Với tài liệu chỉ có PDF (vd. bài 8 Mô tả sóng lớp 11): `pdftotext -layout` lấy chữ (công thức MathType ra dạng Symbol-font lộn xộn: `l`=λ, `p`=π, `w`=ω, `j`=φ, `D`=Δ — đọc được, nhưng phải zoom `pdftoppm -x -y -W -H` để đối chiếu), `pdfimages -all` lấy hình gốc, tự viết `final.tex`, rồi vào lại pipeline bằng `split_parts.py --src`. Không cần trích công thức bằng ảnh.

**Đáp án trắc nghiệm trong PDF thường đánh dấu bằng gạch chân dưới chữ cái phương án** — mất khi sang LaTeX. Dò tự động: `pdftotext -bbox-layout` lấy bbox từng token `A./B./C./D.`, render 150 DPI (scale 150/72), quét tỉ lệ pixel tối theo từng dòng trong bbox; gạch chân = dòng đậm ≥0.5 **sau khi ink của chữ đã hết và có ít nhất 1 dòng trắng**. Bắt buộc điều kiện "sau ink", nếu không nét trên của chữ D bị nhận nhầm. Cách này đọc đúng 54/55 câu; câu duy nhất trượt là câu bị cắt ngang ranh giới trang.

KaTeX repo (strict) **không nhận chữ tiếng Việt có dấu trong `\text{}`** — `v_{\text{rắn}}` báo lỗi. Bản MathType gốc cũng viết không dấu (`v_ran`, `v_{phan tu}`), cứ giữ vậy.

**Đăng gói qua trang admin — hai cái bẫy** (18/09/2026): (1) `pbcopy` trong phiên Claude Code chạy với `LANG` rỗng nên coi file UTF-8 là MacRoman, dán vào web ra mojibake ("Lớp"→"L·ªõp"). Luôn `LANG=en_US.UTF-8 pbcopy < file`, và kiểm bằng cách so `ta.value.length` với số **ký tự** của file (không phải số byte). (2) Browser pane **chặn fetch tới 127.0.0.1** (`ERR_BLOCKED_BY_CLIENT`) và **từ chối `navigator.clipboard.readText()`**, `⌘V` do tool bấm cũng không lấy được clipboard hệ thống → gói vài trăm KB phải nhờ người dùng tự dán. Sau khi họ dán rồi thì sửa/bổ sung trường bằng JS trên chính textarea được (parse → sửa → native setter + `input` event), không cần dán lại.
