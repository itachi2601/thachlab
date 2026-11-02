# Danh mục file gốc trong thư mục `2026/` (trừ `dich/`)

Kiểm đếm bằng `find . -type f -not -path './dich/*'`: **27 file** (không phải 29 như ghi ban đầu): 2 zip + 2 file ở gốc + 18 file trong `WSC2026_TP01_actual_en/` + 5 file trong `WSC2026_TP01_skill_sets_pre_en/WSC2026_TP01_pre/`. Bậc dịch: 1 = song ngữ cho SV, 2 = cho giáo viên, 3 = tóm tắt, bỏ = không dịch.

## Thư mục gốc

| File | Trang / dung lượng | Nội dung | Bậc | Lý do |
|---|---|---|---|---|
| `Industrial_Mechanics_WorldSkills_2026.pdf` | 18 tr / 316 KB | Bản phân tích tiếng Việt có sẵn | bỏ | Dựa trên skill sets pre-release nên lỗi thời (`loi-ban-goc.md` #11): sai dung sai, coi A2 là sửa mạch vật lý, thiếu bộ dụng cụ Module A và trọng số điểm. **Khuyến nghị thay bằng bộ `dich/01-...`.** |
| `WSC2026_TD01_en.pdf` | 32 tr / 714 KB | Technical Description của Skill 01 | 2 | Luật chấm, thiết kế đề, PPE, luật riêng nghề → `dich/02-...` |
| `WSC2026_TP01_actual_en.zip` | 6.4 MB | Nén của thư mục `WSC2026_TP01_actual_en/` | bỏ | **Trùng**: 18 file bên trong giống hệt thư mục đã giải nén (cùng tên, cùng dung lượng) |
| `WSC2026_TP01_skill_sets_pre_en.zip` | 7.0 MB | Nén của thư mục `WSC2026_TP01_skill_sets_pre_en/` | bỏ | **Trùng**: 5 file PDF bên trong có cùng tên/dung lượng với bản giải nén |

## `WSC2026_TP01_actual_en/` (đề thật, 18 file)

| File | Trang / dung lượng | Nội dung | Bậc | Lý do |
|---|---|---|---|---|
| `WSC2026_TP01_MA1_actual_en.pdf` | 12 tr / 309 KB | Module A1: bảo trì dự đoán (cân chỉnh, rung, cân bằng) | 1 | Đề thật |
| `WSC2026_TP01_MA2_actual_en.pdf` | 2 tr / 219 KB | Module A2: sửa lỗi trên FluidSIM | 1 | Đề thật |
| `WSC2026_TP01_MB_1_2_actual_en.pdf` | 2 tr / 200 KB | Module B: hàn và lấy dấu | 1 | Đề thật |
| `WSC2026_TP01_MC_1_2_actual_en.pdf` | 2 tr / 226 KB | Module C: tiện–phay | 1 | Đề thật |
| `WSC2026_TP01_MD_actual_en.pdf` | 3 tr / 256 KB | Module D: lắp ráp và vận hành | 1 | Đề thật |
| `WSC2026_01_Industrial_Mechanics_marking_scheme.xlsx` | 203 KB | Thang điểm đầy đủ các Aspect | 1 | Chuyển thành `08-thang-diem-song-ngu.csv` |
| `WS2026_TP01_1st Assembly and Machining.pdf` | 13 tr / 1.4 MB | Bản vẽ lắp và gia công, phép chiếu góc phần tư I | 1 | Bản vẽ chính cho chú giải |
| `WS2026_TP01_3rd Assembly and Machining.pdf` | 13 tr / 1.4 MB | Cùng bộ, phép chiếu góc III | bỏ | **Trùng nội dung 1st angle**, chỉ khác phép chiếu |
| `WS2026_TP01_1st Angle Machining Aid + Machining Detail Parts.pdf` | 4 tr / 359 KB | Bản vẽ chi tiết gia công/dưỡng, góc I | 1 | Bản vẽ chính |
| `WS2026_TP01_3rd Angle Machining Aid + Machining Detail Parts.pdf` | 4 tr / 353 KB | Cùng bộ, góc III | bỏ | Trùng 1st angle |
| `WS2026_TP01_200 Fab and Welding Series 1st angle.pdf` | 4 tr / 365 KB | Bản vẽ chế tạo–hàn series 200, góc I | 1 | Dùng cho Module B |
| `WS2026_TP01_200 Fab and Welding Series 3rd angle.pdf` | 4 tr / 357 KB | Cùng bộ, góc III | bỏ | Trùng 1st angle |
| `WS2026_TP01_Pneumatics Build.pdf` | 6 tr / 401 KB | Sơ đồ khí nén, danh sách linh kiện và ống | 1 | Mã MM1…MM4 (Rev 11) |
| `WSC2026_statement_of_TP_validation_01_ALC_ITPV.pdf` | 1 tr / 139 KB | Xác nhận ITPV — Alex Le Comte | 3 | Gộp vào `statement-of-validation.md` |
| `..._01_CB_ITPV.pdf` | 1 tr / 167 KB | Xác nhận ITPV — Colin Buddin (scan) | 3 | Như trên |
| `..._01_ECS_ITPV.pdf` | 1 tr / 279 KB | Xác nhận ITPV — Emerson Costa Santos | 3 | Như trên |
| `..._01_FB_ITPV.pdf` | 1 tr / 40 KB | Xác nhận ITPV — Fabian Burguera (scan) | 3 | Như trên |
| `..._01_SS_ITPV.pdf` | 1 tr / 294 KB | Xác nhận ITPV — Shannon Savoy (ảnh chụp) | 3 | Như trên |

## `WSC2026_TP01_skill_sets_pre_en/WSC2026_TP01_pre/` (bản pre-release, 5 file)

| File | Trang / dung lượng | Nội dung | Bậc | Lý do |
|---|---|---|---|---|
| `WSC2026_TP01_skill_sets_pre_en.pdf` | 4 tr / 295 KB | Mô tả nội dung đề phát hành trước | 2 | Chỉ tham khảo; dung sai và vật liệu bị thang điểm thật thay thế (`loi-ban-goc.md` #1–3) |
| `WSC2026_TP01_milling_machine_info_pre_en.pdf` | 46 tr / 17.9 MB | Thông số máy phay M5 (dịch máy từ tiếng Trung, phần lớn ảnh) | 3 | → `may-phay-M5-thong-so.md` |
| `WSC2026_TP01_milling_machine_vise_info_pre_en.pdf` | 1 tr / 79 KB | Ảnh và thông số ê-tô 6" | 3 | Gộp vào file máy phay |
| `WSC2026_TP01_1st_angle_pre_en.pdf` | 15 tr / 784 KB | Bản vẽ pre-release, góc I | bỏ | Bị bản vẽ đề thật thay thế |
| `WSC2026_TP01_3rd_angle_pre_en.pdf` | 15 tr / 801 KB | Bản vẽ pre-release, góc III | bỏ | Trùng 1st angle và bị bản thật thay thế |

## Tóm tắt

- **Trùng:** 2 file .zip trùng thư mục đã giải nén; bộ bản vẽ 3rd angle (3 file thật + 1 pre) trùng nội dung 1st angle, chỉ khác phép chiếu. Dịch bản 1st angle (hệ ISO/châu Âu, khớp với cách dạy ở VN).
- **Bỏ qua:** zip (2), 3rd angle (4), 1st angle pre-release (1), bản phân tích VN cũ (1).
- **Khuyến nghị:** thay `Industrial_Mechanics_WorldSkills_2026.pdf` bằng bộ `dich/01-...`; không dùng bản cũ làm nguồn.

## Ghi chú bản gốc

1. Số trang lấy từ `pdfinfo`; dung lượng làm tròn từ `ls -l`.
2. Tên file thiếu một số hậu tố rút gọn ở bảng ITPV ("..." thay phần `WSC2026_statement_of_TP_validation_01`).
3. Mốc ngày trong zip: actual từ 6/8 đến 28/9/2026 (thang điểm sửa ngày 28/9 mới nhất); pre-release 24/6–29/7/2026. Thang điểm xlsx là bản sau cùng.
4. Chưa so nội dung bản vẽ 3rd/1st từng nét; kết luận "trùng" dựa trên tên, số trang, dung lượng gần nhau và quy ước của bộ đề.
