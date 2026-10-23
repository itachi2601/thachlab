# Linh kiện HTML của bài tương tác (CSS: `.tl-*` cuối `app/globals.css`)

Chỉ dùng trong `.exam-content` (bài học). Đặt tiền tố id/name theo bài: `tl<số bài>-q<câu><đáp án>`.

## Hộp (`.tl-box`)
```html
<div class="tl-box tl-box--think">   <!-- xanh: dự đoán / tự kiểm tra -->
<p class="tl-label">🤔 Dự đoán trước khi học</p>
<p>…</p>
</div>
<div class="tl-box tl-box--rule">    <!-- vàng: định nghĩa / mang về -->
<p class="tl-label">📘 Định luật …</p>
<p>…</p>
</div>
```

## Trắc nghiệm tự chấm (không JS)
```html
<div class="tl-quiz">
<input type="radio" name="tl3-q1" id="tl3-q1a"><label for="tl3-q1a" class="tl-opt tl-no">A. …</label>
<input type="radio" name="tl3-q1" id="tl3-q1b"><label for="tl3-q1b" class="tl-opt tl-ok">B. … (đúng)</label>
<div class="tl-fb tl-fb--ok"><p><strong>Đúng.</strong> lý do…</p></div>
<div class="tl-fb tl-fb--no"><p><strong>Chưa đúng.</strong> gợi ý cách nghĩ lại…</p></div>
</div>
```
Đúng đúng **một** `tl-ok` mỗi `.tl-quiz`. Phản hồi sai là gợi ý chung, không lộ đáp án.

## Bấm để mở
```html
<details class="tl-details">
<summary>🧮 Bấm xem: …</summary>
<p>…</p>
</details>
```
Dùng cho: lời giải, "thế thì sao?", thử thách. Không giấu kiến thức bắt buộc trong `<details>`.

## Bảng so sánh
`<table class="tl-table">` (tự được bọc cuộn ngang). 2–3 cột, ≤5 hàng.

## Hình
`<figure class="fig" data-tl="1"><svg …/><figcaption>Hình n. …</figcaption></figure>` — `data-tl="1"` để script chèn lại idempotent. Xem `hinh-svg.md`.

## Công thức
`$…$` inline, `$$…$$` riêng dòng, trong `<p>`. Đơn vị: `\ \text{m/s}^2`. Không `\[ \]` (validate chặn).

## Thí nghiệm / ví dụ thực tế (`.tl-box--exp`)
```html
<div class="tl-box tl-box--exp">
<p class="tl-label">🔬 Thí nghiệm: tên ngắn</p>
<ol class="tl-steps">
<li><strong>Làm:</strong> dụng cụ + thao tác, đủ để thầy làm thật trên lớp.</li>
<li><strong>Quan sát:</strong> hiện tượng/số đo thấy được.</li>
<li><strong>Rút ra:</strong> gắn lại đúng ý kiến thức đang học.</li>
</ol>
</div>
```
Dụng cụ phải có sẵn ở phòng thí nghiệm/nhà (lực kế, xe đẩy, ghế xoay...). Mỗi kiến thức chính có một ví dụ hoặc thí nghiệm.

## Trả bài (nhớ lại trước khi giải)
Hộp `tl-box tl-box--think`, nhãn "🎤 Trả bài", bên trong 4–6 `<details class="tl-details">`, `<summary>` là câu hỏi, nội dung là đáp án chuẩn.

## Ba linh kiện tự học (thêm 2/10/2026)

**Tự giải thích trước khi xem** — trong mục Trả bài, `<summary>` kết bằng dòng nhỏ:
```html
<details class="tl-details"><summary>Phát biểu định luật… <small>(nói bằng lời của em trước, rồi mới bấm xem)</small></summary>
<p>Đáp án từ khoá…</p></details>
```

**Bài giải để trống bước** — đặt sau lời giải bài toán mẫu, trước "Thử sức". Dùng `.tl-steps`, bước trống ghi `…?` và đáp án trong `<details>`:
```html
<div class="tl-box tl-box--think"><p><strong>✍️ Điền bước còn thiếu</strong> — cùng đề, chỉ đổi $v = 2$ m/s.</p>
<ol class="tl-steps">
<li>$\lambda = v/f = 2/0{,}5 = 4$ m</li>
<li><strong>Bước 2 (em điền):</strong> $\Delta\varphi = \;?$ — gợi ý: bao nhiêu bước sóng?</li>
<li>Kết luận: …?</li>
</ol>
<details class="tl-details"><summary>Xem bước 2–3</summary><p>$\Delta\varphi = 2\pi d/\lambda = \dots$</p></details></div>
```

**Hiệu chuẩn tự tin** — một `<p>` radio thường đặt **ngay trước** `.tl-quiz` (không đặt bên trong, vì `check_quizzes.py` và CSS `:has()` đòi mọi input trong `.tl-quiz` phải đi với `.tl-opt`). `name` riêng, không `tl-ok/tl-no`:
```html
<p class="tl-conf">Em chắc bao nhiêu?
<label><input type="radio" name="tl8-q3c" value="chac"> Chắc</label>
<label><input type="radio" name="tl8-q3c" value="khong"> Không chắc</label></p>
<div class="tl-quiz">… như thường …
<div class="tl-fb tl-fb--no"><p><strong>Chưa đúng.</strong> …lỗi cụ thể… Nếu em đã chọn <em>Chắc</em> mà vẫn sai, đây là chỗ cần xem lại nhất.</p></div>
</div>
```
Chỉ dùng cho 2–3 quiz quan trọng (bẫy, bài toán mẫu). Radio này không có CSS riêng trong `globals.css`, trình duyệt vẽ mặc định — chấp nhận được.

## Bảng "đề → dữ liệu → kiến thức"
```html
<div class="table-scroll"><table class="tl-table tl-table--data">
<thead><tr><th>Câu trong đề</th><th>Dữ liệu</th><th>Kiến thức liên quan</th></tr></thead>
<tbody><tr><td>"trích nguyên cụm từ trong đề"</td><td>$m = 40$ kg</td><td>định luật/công thức gọi ra</td></tr></tbody>
</table></div>
```
Mỗi hàng một câu/cụm của đề, theo đúng thứ tự đề. Cột Dữ liệu tự tô vàng. Dữ kiện "ngầm" (bỏ qua ma sát, bắt đầu từ nghỉ) cũng có một hàng riêng.

## Khối công thức / định luật (`.tl-fx`, chốt 21/10/2026)
Mọi công thức chủ chốt, định luật, định lý: đặt giữa, có khung, chú giải đại lượng ngay dưới (cột ký hiệu canh phải, nghĩa canh trái).
```html
<div class="tl-fx">
<p class="tl-fx-name">Dạng 3: lệch pha</p>
<p>$$\Delta\varphi=\dfrac{2\pi d}{\lambda}$$</p>
<p class="tl-fx-cond">Cùng pha</p>     <!-- điều kiện/trường hợp: chữ nhỏ trên công thức, không để chữ Việt trong \text{} -->
<p>$$d=k\lambda$$</p>
<ul class="tl-fx-def">
<li><span class="tl-sym">$d$</span><span>khoảng cách hai điểm (m)</span></li>
</ul>
<p class="tl-fx-note">Ghi chú ngắn (tuỳ chọn).</p>
</div>
```
Mỗi công thức một `$$…$$` riêng dòng; không nhét công thức có phân số vào giữa câu (dòng có `.katex` tự giãn `line-height:2`).

## Hệ khung có nghĩa — CHỈ BA loại khung (chốt 21/10/2026, bài mới thêm lớp; bài cũ giữ nguyên)
Học sinh phản hồi: quá nhiều loại khung thì không biết ô nào quan trọng, khung lồng khung ăn bề ngang 375px. Quy tắc:
| Ý nghĩa | Lớp | Icon + màu viền (token, M3) |
|---|---|---|
| Phải nhớ: công thức, định luật, "Mang về" | `.tl-fx` (khối công thức), `.tl-box.tl-box--rule.tl-keep` | 📌 màu mực `--color-ink` (trung tính, không dùng màu nhấn/trạng thái) |
| Bẫy mất điểm | `<div class="tl-trap">` bọc `<h4>Bẫy …` + nội dung | ⚠️ `--color-warn` (đỏ chỉ để "sai" trong phản hồi quiz bên trong) |
| Tự kiểm tra, Trả bài, biến thể | `.tl-box.tl-box--think.tl-check` | ✍️ `--color-primary` |
Mọi thứ còn lại KHÔNG có khung: `.tl-box … tl-note` (mục tiêu, dự đoán, 🔬 thí nghiệm, 🎬 video, 📄 đề bài; chỉ một vạch trái mỏng trung tính `--color-line-strong`; phân biệt loại bằng emoji ở nhãn, không bằng màu) và `<details class="tl-details tl-more">` (bấm xem). Giữ NGUYÊN các lớp cũ (`tl-box--exp`, `tl-box--video`, `tl-box--think`) vì script chèn video/thí nghiệm bám vào chúng; chỉ thêm lớp mới. Nhãn của hộp có khung bỏ emoji đầu (icon góc đã thay). Icon do CSS `::before`, không viết vào HTML. Thêm loại khung thứ tư = phá quy tắc, phải hỏi thầy.

### Chuyển bài CŨ sang hệ khung (23/10/2026)
`python3 scripts/ap-he-khung.py content/lesson-samples/<bài>/theory.src.html` tự thêm lớp `tl-keep`/`tl-check`/`tl-note`/`tl-more` và bọc `<h4>Bẫy …` vào `tl-trap` (chạy lại an toàn). Khối `.tl-fx` viết tay (bảng chú giải đại lượng). Sau đó `build_figs.py` → `build_bundle.py` → `build_preview.py` + `chup_anh.py` (xem thử nay nền sáng, `data-theme="light"`). Mẫu: `l11-mo-ta-song`. Ghi DB bằng `cap-nhat-ly-thuyet.sh` sau khi thầy duyệt.
