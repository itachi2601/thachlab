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
