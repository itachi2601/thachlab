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
   chuyển động thẳng, đẳng áp, đẳng tích…), `hyperbola` (đẳng nhiệt p–V), `exponential` (phóng xạ, tụ).
   Hình không thuộc 4 loại này (mạch điện, sơ đồ thí nghiệm, vectơ…) → `kind: "khong_ve_duoc"` và ghi mô tả.
4. Đường sinusoid: tính A, T, phi từ điểm cắt trục và cực trị trên ảnh, đối chiếu với đề bài.
   Công thức dùng: y = A·cos(2π·x/T + phi) + y0. Đường bắt đầu từ 0 đi LÊN là sin → phi = −1.5708.
   Kiểm lại: tại x = 0 giá trị y trên ảnh có khớp A·cos(phi) không? Nếu không, sửa phi.
5. Polyline: liệt kê từng điểm gãy theo thứ tự x tăng, đọc toạ độ từ vạch chia.
6. Điểm có đánh dấu (chấm, chữ M, N, A, B…) → `points`; đường gióng nét đứt → `guides`.
7. `do_tin_cay`: 1 nếu mọi số liệu đọc được rõ hoặc có trong đề bài; 0.5 nếu phải ước lượng; 0 nếu đoán.
8. `ghi_chu`: ghi những gì ảnh có mà schema không tả được (ví dụ "hai đường cùng màu", "có mũi tên").

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
