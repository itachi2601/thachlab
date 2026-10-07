# Vẽ hình SVG cho bài lý thuyết

Dùng `scripts/svg_lib.py`: `defs(prefix)` (mũi tên 4 màu), `arrow`, `text`, `person` (người que + giày trượt), `wrap`. Mẫu dùng: `content/lesson-samples/l10-dinh-luat-3-newton/build_figs.py`.

## Quy ước
- **Mỗi hình = một ý.** Hình 1 minh hoạ tình huống mở bài; hình 2 minh hoạ chỗ hiểu lầm; hình 3 minh hoạ số liệu.
- **Màu có nghĩa, giữ nhất quán cả bài:** đỏ `#f87171` = lực/đại lượng "tác động"; xanh dương `#38bdf8` = phản ứng/đối tượng thứ hai; cam `#fb923c` = nhóm cùng vật; xanh lá `#34d399` = kết quả chuyển động/gia tốc. Chữ và nét thân vật dùng `currentColor`.
- **Độ dài mũi tên tỉ lệ độ lớn** (lực bằng nhau → dài bằng nhau; gia tốc 3 : 2 → 120 : 80 px).
- `viewBox` ≈ 420–440 rộng; `figure.fig` tự giới hạn 420 px. Chữ ≥ 11 px sau thu nhỏ; kiểm ở 375 px.
- Marker mũi tên **mỗi hình một tiền tố** (`f1-r`, `f2-b`…) — id trùng giữa các hình làm mũi tên mất.
- Chỉ số dưới: `<tspan dy="4" font-size="9">A</tspan><tspan dy="-4">…</tspan>`. Không dùng KaTeX trong SVG.
- Nhãn bằng chữ Việt ngắn ("F₁: em đẩy thành") dễ hiểu hơn ký hiệu trơ; ký hiệu đi kèm.
- Không nhồi: mỗi hình ≤ ~8 phần tử có nhãn.

## Lỗi hay gặp (đã gặp ở bài mẫu)
- `text-anchor="middle"` ở sát mép → bị cắt ("Thành sân"). Dùng `start` + toạ độ x ≥ 12.
- Hai nhãn cùng hàng đè nhau → so vị trí x/y, đẩy nhãn phụ xuống hàng khác.
- Tay hai người que phải gặp nhau cùng một điểm (cùng toạ độ), nếu không thành đường chéo lạ.
- Mũi tên đặt lên vật nào thì **đầu mũi tên/gốc nằm trên vật đó**; nếu phải vẽ lệch cho khỏi chồng, chú thích "đặt lên …".

## Quy trình
Viết script → `python3 build_figs.py` (thay khối `data-tl="1"`, chèn trước các mốc anchor) → `preview.mjs` chụp từng `figure.fig` → xem ảnh → sửa → chạy lại.

## Đường sức và chú thích hình (thầy chốt 7/10/2026)

- **Đường sức (từ) vẽ NÉT ĐỨT**, đầu mũi tên là **hai vạch chéo, mỗi vạch lệch 30° so với đường chính (chữ V mở), đầu nhọn** — không dùng tam giác đặc, không dùng `marker` (marker co theo bề dày nét làm đầu tù). Dùng `svg_lib.field_line(x1,y1,x2,y2,màu)` cho đường thẳng, `field_path(d, tip, hướng, màu)` cho đường cong, `chevron(x,y,dx,dy)` khi chỉ cần đầu mũi tên. Vectơ lực/vận tốc/dòng điện vẫn dùng mũi tên đặc `arrow()`.
- **Chú thích tách từng dòng**: mỗi ý một dòng `<text>` riêng (trong hình) hoặc một `<li>`/dòng riêng (dưới hình, ghi chú); không nối nhiều ý bằng "·", ";" hay dấu phẩy trong một dòng. Chú thích dài quá bề ngang thì xuống dòng, đừng thu nhỏ chữ.
