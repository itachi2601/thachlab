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
Tuỳ chọn: `lesson_id, nguon_trong_bai, sai_so_thuong_gap, an_toan, video`.

## Video thí nghiệm (tuỳ chọn, chèn tự động vào bài)
Mỗi thí nghiệm có thể gắn **một** clip YouTube thật. Video **không** viết vào `theory.html` bằng tay:
ghi vào đây rồi chạy script chèn — một nguồn dữ liệu, chèn lại được cho nhiều bài.

```json
"video": {
  "youtube_id": "UMkAXvWIRY4",          // 11 ký tự, bắt buộc
  "nhan": "khay sóng, hai nguồn điểm",  // nhãn hiện trên hộp (mặc định lấy `ten`)
  "nhin_vao": "Các đường cực đại và cực tiểu có dạng gì?",  // bắt buộc, ≤ 40 từ
  "giay_bat_dau": 12, "giay_ket_thuc": 48,                  // cắt đoạn cần xem, ≤ 120 giây
  "ten": "Ripple Tank: Interference of Two Point Sources",  // do `--kiem` điền
  "kenh": "MIT Physics Instructional Resources Lab",
  "da_kiem": "2026-10-06"
}
```

- Ưu tiên **tiếng Việt hoặc không lời**; cắt bằng `giay_bat_dau`/`giay_ket_thuc` để bỏ intro/nhiễu.
- `nhin_vao` là câu hướng chú ý (bắt buộc) — video thật thường nhiễu, không có câu này học sinh xem mà không rút ra gì.
- Clip dùng cho nhiều thí nghiệm/bài: khai một lần trong `video-dung-chung.json` (mục `videos`, mỗi mục có
  `youtube_id` + `ten` + `kenh` + `da_kiem`), rồi các file `tn-*.json` chỉ cần ghi `youtube_id` + `nhin_vao`.
- Chèn vào bài (mặc định xem thử, chỉ ghi khi có `--apply`; chạy lại không nhân đôi):
```
npx tsx scripts/chen-video-thi-nghiem.mts                       # xem thử mọi bài
npx tsx scripts/chen-video-thi-nghiem.mts --bai l11-giao-thoa-song --apply
```

### Video mở bài (và video gắn theo bài) — `video-theo-bai.json`
Clip **mở bài** (đặt vấn đề bằng hiện tượng thật) không thuộc hộp thí nghiệm nào, nên khai riêng:

```json
{
 "bai": [
  { "slug": "l11-giao-thoa-song", "lesson_id": 31,
    "videos": [
      { "vi_tri": "mo_bai", "youtube_id": "b87QZtYKmqo",
        "nhan": "hai loa phát cùng một âm",
        "nhin_vao": "Hai loa đều đang kêu, vậy chỗ nghe nhỏ có phải là chỗ hết sóng?",
        "giay_bat_dau": 20, "giay_ket_thuc": 70 }
    ] } ]
}
```

- `vi_tri`: `mo_bai` (mặc định) · `truoc:<data-exp>` · `sau:<data-exp>` để gắn clip vào một mốc bất kỳ.
- `mo_bai` được chèn **ngay trước hộp "Dự đoán trước khi học"** của mục I (không có hộp đó thì sau hình đầu,
  rồi mới tới sau đoạn văn đầu) — học sinh **thấy hiện tượng rồi mới dự đoán**, đúng thứ tự bài Giao thoa đã duyệt.
- Clip mở bài **chỉ quay hiện tượng, không giải thích cơ chế, không lộ đáp án**; `nhin_vao` hỏi đúng câu hỏi mở bài; nên ≤ 60 giây.
- Nhãn hộp mặc định "Xem thực tế"; đổi bằng `tieu_de_hop` nếu cần.
Script chèn khối `.tl-box--video` ngay sau hộp `.tl-box--exp`/`<figure>` mang `data-exp` đó, đồng bộ
`theory.src.html` + `theory.html` + `theory_html` trong `bundle.json`. Đăng lên DB:
`bash scripts/cap-nhat-ly-thuyet-hang-loat.sh <slug>:<lesson_id>` (một lượt deploy cho nhiều bài).

## Liên kết với bài lý thuyết
Trong `theory.html`, đặt `data-exp="<id>"` lên hộp thí nghiệm (`.tl-box--exp`) hoặc `<figure>` tương ứng. Kiểm bằng:
```
python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/thi_nghiem.py <theory.html>
```

## Danh sách hiện có
Xem `index.json` (211 mục, sinh tự động). Mỗi bài lý thuyết mới phải thêm mục vào đây, không để thí nghiệm chỉ nằm trong HTML.
