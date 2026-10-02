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
