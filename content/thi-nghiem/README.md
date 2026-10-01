# Kho thí nghiệm / ví dụ thực tế (dữ liệu nguồn cho giai đoạn Mô phỏng)

Mỗi file `tn-<lớp>-<bài>-<số>.json` mô tả MỘT thí nghiệm hoặc ví dụ xuất hiện trong bài lý thuyết tương tác (`.tl-box--exp`, hình minh hoạ, hoặc bài toán mẫu). Viết cho **hai người đọc**: học sinh/thầy (qua bài) và **bộ dựng mô phỏng** ở giai đoạn sau (đọc máy được: tham số, khoảng giá trị, phương trình, số liệu mẫu).

`index.json` do `thi_nghiem.py` sinh tự động, không sửa tay.

## Quy ước
- `id`: `tn-l<lớp>-<bài-không-dấu>-<nn>`, trùng tên file.
- `loai`: `thi_nghiem` (làm được ở lớp/phòng thí nghiệm) hoặc `vi_du` (tình huống đời sống, chỉ phân tích/mô phỏng).
- `kien_thuc`: mã `chu_de.y_nho` (chữ thường, số, `_`), dùng chung giữa các bài để sau này nối với YCCĐ/mastery: `newton3.cung_luc`, `newton2.a_bang_f_chia_m`...
- `tham_so[].kieu`: `dieu_chinh` (thanh trượt mô phỏng, bắt buộc có `min`/`max`/`mac_dinh`), `do_duoc` (đại lượng đo, có `sai_so_do`), `tinh_ra` (đầu ra tính từ mô hình), `co_dinh` (hằng số, có `gia_tri`).
- `mo_hinh.phuong_trinh`: các hệ thức dạng chữ, `gia_thiet` ghi rõ điều đã bỏ qua. Số liệu mẫu tính từ chính các hệ thức này (g = 9,8 m/s²).
- `so_lieu_mau`: `cot` + `hang`, mỗi hàng đúng số cột; là số liệu minh hoạ tính từ mô hình, không phải đo thật (trừ khi `ghi_chu` nói khác).
- `goi_y_mo_phong.loai`: `2d_dong_hoc` | `so_do_luc` | `do_thi` | `bang_so_lieu` (ghép bằng `+`).
- `hien_tuong_hay_sai`: hiểu lầm cần để mô phỏng "đặt bẫy" cho học sinh dự đoán trước.

## Trường bắt buộc
`id, ten, loai, muc_do, mon, lop, bai, kien_thuc, muc_tieu, dung_cu, cac_buoc{lam,quan_sat,rut_ra}, tham_so, mo_hinh, so_lieu_mau, ket_qua_ky_vong, hien_tuong_hay_sai, goi_y_mo_phong`.
Tuỳ chọn: `lesson_id, nguon_trong_bai, sai_so_thuong_gap, an_toan`.

## Liên kết với bài lý thuyết
Trong `theory.html`, đặt `data-exp="<id>"` lên hộp thí nghiệm (`.tl-box--exp`) hoặc `<figure>` tương ứng. Kiểm bằng:
```
python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/thi_nghiem.py <theory.html>
```

## Danh sách hiện có
Xem `index.json` (6 mục từ bài Định luật III Newton, lớp 10). Mỗi bài lý thuyết mới phải thêm mục vào đây, không để thí nghiệm chỉ nằm trong HTML.
