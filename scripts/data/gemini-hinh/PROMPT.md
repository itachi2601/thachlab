# Nhiệm vụ cho Gemini: đọc hình đồ thị xấu → trả THÔNG SỐ để code vẽ lại bằng SVG

Thư mục này do thachlab xuất ra. Mỗi câu hỏi là một thư mục con `cau/<id>/` gồm:
- `anh-*.png` : ảnh gốc (chất lượng thấp) của câu hỏi, đọc kỹ từng chi tiết.
- `de-bai.md` : đề bài, các phương án, lời giải (nếu có). Số liệu trong đề bài là NGUỒN ĐÚNG khi ảnh mờ.

Với MỖI thư mục `cau/<id>/`, ghi một file `out/<id>.json` đúng cấu trúc trong `schema.json`.
Không ghi gì khác vào `cau/`. Không vẽ ảnh, không trả SVG, chỉ trả thông số.

## Quy tắc đọc hình
1. Trục: tên trục + đơn vị lấy từ ảnh; nếu ảnh không ghi thì suy từ đề bài (ví dụ "x (cm)", "t (s)").
2. Vạch chia: ghi ĐÚNG các giá trị có ghi trên trục của ảnh gốc (kể cả nhãn chữ như "T/2", "π").
3. Mỗi đường trên hình chọn ĐÚNG MỘT loại: `sinusoid` (dao động/sóng), `polyline` (gấp khúc,
   chuyển động thẳng, đẳng áp, đẳng tích…), `hyperbola` (đẳng nhiệt p–V), `parabola` (y = a·(x−h)²+k), `exponential` (phóng xạ, tụ).
   Hình không thuộc 4 loại này (mạch điện, sơ đồ thí nghiệm, vectơ…) → `kind: "khong_ve_duoc"` và ghi mô tả.
4. Đường sinusoid: tính A, T, phi từ điểm cắt trục và cực trị trên ảnh, đối chiếu với đề bài.
   Công thức dùng: y = A·cos(2π·x/T + phi) + y0. Đường bắt đầu từ 0 đi LÊN là sin → phi = −1.5708.
   Kiểm lại: tại x = 0 giá trị y trên ảnh có khớp A·cos(phi) không? Nếu không, sửa phi.
5. Polyline: liệt kê từng điểm gãy theo thứ tự x tăng, đọc toạ độ từ vạch chia.
6. Điểm có đánh dấu (chấm, chữ M, N, A, B…) → `points`; đường gióng nét đứt → `guides`.
7. `do_tin_cay`: 1 nếu mọi số liệu đọc được rõ hoặc có trong đề bài; 0.5 nếu phải ước lượng; 0 nếu đoán.
8. `ghi_chu`: ghi những gì ảnh có mà schema không tả được (ví dụ "hai đường cùng màu", "có mũi tên").

## Câu có NHIỀU hình (ảnh dẫn + 4 phương án A–D, hoặc Hình 1–4 của mệnh đề a–d)
Mỗi câu thư mục `cau/<id>/` có `anh-1`, `anh-2`… — ĐỌC HẾT các ảnh, đối chiếu `de-bai.md` xem ảnh nào là hình nào.
Có hơn một đồ thị cần vẽ → `kind: "multi"`, `figures: [ {nhan:"A", ...như plot}, {nhan:"B", ...}, … ]` đủ MỌI hình (thiếu một hình
thì cả câu bị loại). Nhãn `nhan` phải khớp chữ trong đề (A/B/C/D hoặc "Hình 1"…). Ảnh dẫn nếu có đồ thị riêng thì cũng là một phần tử.
Mỗi phần tử trong `figures` có đủ trục, khoảng, vạch chia, series như một câu `plot`.

## Nhãn tên đường (`label`)
Chỉ đặt `label` cho đường khi ảnh gốc CÓ ghi tên đường (p₁, p₂, T₁…). Không tự bịa nhãn. Code luôn vẽ nhãn ở đầu mút bên PHẢI của đường,
nên đừng lo vị trí; thứ tự `series` phải là thứ tự từ trên xuống dưới ở đầu mút phải để nhãn không đè nhau.

## Ảnh gốc hỏng/trống (vài trăm byte, chỉ có khung trục)
Nếu đề bài mô tả đủ đồ thị bằng lời hoặc công thức (ví dụ E ∝ 1/r², đun đá −20→20 °C có đoạn nóng chảy nằm ngang) thì VẼ THEO ĐỀ,
`do_tin_cay: 0.5` và ghi `ghi_chu: "vẽ theo đề, ảnh gốc hỏng"`. Chỉ `khong_ve_duoc` khi đề cũng không đủ thông tin.

## Ví dụ out/<id>.json
```json
{
  "id": 123456,
  "kind": "plot",
  "xLabel": "t (s)", "yLabel": "x (cm)",
  "xRange": [0, 2], "yRange": [-4, 4],
  "xTicks": [{"v": 0}, {"v": 0.5}, {"v": 1}, {"v": 1.5}, {"v": 2}],
  "yTicks": [{"v": -4}, {"v": 0}, {"v": 4}],
  "series": [{"type": "sinusoid", "A": 4, "T": 1, "phi": -1.5708, "label": "x"}],
  "points": [{"x": 0.25, "y": 4, "label": "M"}],
  "guides": [{"x": 0.25}],
  "do_tin_cay": 1,
  "ghi_chu": ""
}
```

## Ví dụ câu nhiều hình (kind = multi)
```json
{
  "id": 523830, "kind": "multi", "cols": 2,
  "figures": [
    {"nhan": "A", "xLabel": "t (°F)", "yLabel": "t (°C)", "xRange": [0, 100], "yRange": [-20, 40],
     "series": [{"type": "polyline", "points": [[32, 0], [100, 37.8]]}]},
    {"nhan": "B", "xLabel": "t (°F)", "yLabel": "t (°C)", "xRange": [0, 100], "yRange": [-20, 40],
     "series": [{"type": "polyline", "points": [[0, 0], [100, 37.8]]}]}
  ],
  "do_tin_cay": 1, "ghi_chu": ""
}
```
