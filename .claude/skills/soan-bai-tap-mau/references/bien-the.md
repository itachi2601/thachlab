# Soạn `bien_the` — biến thể đổi số cho dạng tính toán (chặng 3A, 5/11/2026)

Dạng tính toán ít câu đúng dạng trong ngân hàng → gắn thêm khuôn đề đổi số. Trình duyệt tự sinh câu mới mỗi lần
(khối "Luyện đổi số" hiện sau lời giải, trước "Làm bài tương tự"); không gọi API, vô hạn câu. Thư viện `lib/bien-the.ts`,
type `WorkedVariant` (features/lessons/types.ts), component `components/lessons/VariantPractice.tsx`. Mẫu: bài 18
(`scripts/data/bai-tap-mau/18.json`, Dạng 2, 4, 5).

## Khi nào soạn
- Chỉ dạng có đáp số là MỘT con số tính bằng công thức. Dạng định tính, đọc đồ thị, chọn hình → không.
- Một câu chỉ hỏi kết quả chính của dạng (thường bước cuối), không chép cả a) b) c).

## Các trường
| Trường | Ý nghĩa |
|---|---|
| `kieu` | `"abcd"` (Phần I, A. B. C. D.) hoặc `"so"` (Phần III, ô đáp số ≤ 4 ký tự) |
| `de` | Đề HTML. Chỗ trống `{{ten}}` / `{{ten|3}}` (3 chữ số có nghĩa) / `{{ten|.2}}` (2 số thập phân). Chỗ trống SỐ phải nằm trong `$…$` |
| `bien` | `{ "m": { "min": 1, "max": 8, "buoc": 0.5 } }` — bốc ngẫu nhiên theo bước, gồm hai đầu |
| `bo` | (tuỳ chọn) bộ dữ kiện đi cùng nhau, mỗi lần bốc một bộ: `[{ "ten": "poloni $^{210}_{84}\\text{Po}$", "T": 138, "dv": "ngày" }]`. Trường chữ chỉ thay chỗ trống (được nằm ngoài `$`), trường số vào biểu thức |
| `tinh` | đại lượng trung gian, tính lần lượt: `{ "N0": "a * 10^k", "t": "n * T" }` |
| `dap_so` | biểu thức đáp số; nơi khác gọi tên `dap_so` |
| `don_vi` | in sau phương án (`abcd`) |
| `lam_tron` | `{ "cs": 3 }` (mặc định) hoặc `{ "tp": 0 }`. Kiểu `so` nên dùng `tp` và ghi trong đề "(Làm tròn đến …)" |
| `sai_so` | kiểu `so`: sai số tương đối chấp nhận thêm (0.01 = 1 %) khi đề có nhiều cách làm tròn trung gian |
| `nhieu` | kiểu `abcd`: ≥ 3 (nên 4–5 để dự phòng) `{ "bieu_thuc", "loi", "buoc" }` — `loi` hiện "Vì sao X sai" (≤ 25 chữ, nêu đúng lỗi tư duy), `buoc` là chỉ số 0-based trong `buoc[]` để gỡ rối tô sẵn bước đó |
| `rang_buoc` | biểu thức phải đúng: `"dap_so >= 100"`, `"H >= 0.01"`, `"n != floor(n)"` |
| `khac_nhau` | phương án lệch nhau tối thiểu (mặc định 0.05) |
| `loi_giai` | lời giải ngắn có chỗ trống, hiện sau khi chấm |

Biểu thức: `+ - * / ^`, ngoặc, so sánh `< <= > >= == !=`, `&& || !`, hàm `sqrt ln log10 log2 exp abs floor ceil round(x, k) min max`,
`sin cos tan` (theo ĐỘ), `asin acos atan` (ra độ), hằng `pi`. Viết `6.022e23` (dấu chấm thập phân trong biểu thức).

## Cách làm đúng
1. Số in trong đề phải là số máy dùng để tính: số đo có làm tròn thì làm tròn trong `tinh` (`"H": "round(r * 0.226 * m, 3)"`)
   rồi in `{{H|.3}}` — không in số đã làm tròn mà tính bằng số chưa làm tròn.
2. Hằng số (N_A, ln2, 1 Ci, 1 năm = 365 ngày) ghi rõ trong đề và dùng ĐÚNG giá trị đó trong biểu thức.
3. Khoảng biến sát thực tế (thực nghiệm, sách) và đủ rộng để câu khác nhau; tránh khoảng làm đáp số tròn trĩnh lộ quy luật.
4. Phân số LaTeX quanh chỗ trống: viết có dấu cách `\dfrac{ {{t}} }{ {{T}} }` cho dễ đọc.
5. Nhiễu `abcd` lấy từ `loi_hay_gap` của các bước — mỗi nhiễu là MỘT lỗi thật, không bịa số lệch ngẫu nhiên.
6. Kiểu `so`: đáp án đã làm tròn phải ≤ 4 ký tự (kể cả dấu phẩy, dấu trừ) — chọn đơn vị/khoảng biến cho vừa.

## Kiểm trước khi đăng
```
npx tsx scripts/kiem-bien-the.mts <lesson_id> --mau 3
```
Sinh 200 bộ số/khuôn: báo vi phạm ràng buộc, NaN/vô cực, phương án trùng/gần nhau, đáp số > 4 ký tự, KaTeX lỗi, chỗ trống chưa thay,
phân bố đáp án đúng A–D. "đạt ngay" < 50 % → nới khoảng biến/ràng buộc. Rồi `kiem-code` tự tính lại 2–3 câu mẫu mỗi khuôn.
Xem UI: `npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --xem-thu` → `/dev/btm?mock=1` (mở "Giải từng bước" → "Xem cả lời giải").
Đăng: như mọi dạng, `publish-bai-tap-mau.mts --lesson <id>` (đã chuyển trường `bien_the` vào `lesson_items.questions`), rồi deploy.
