---
name: dung-video-thi-nghiem
description: Tự dựng video 9:16 KHÔNG giọng (phụ đề + nhạc tổng hợp) cho thí nghiệm trong content/thi-nghiem/ mà YouTube không có clip — viết kịch bản Python theo mẫu boyle/chuyenthe/camungdt, số liệu lấy từ so_lieu_mau, hộp Dự đoán đồng màu, render bằng scripts/video-thi-nghiem. Dùng khi thầy nói "làm video thí nghiệm X", "làm lô 1 video thí nghiệm", "thí nghiệm nào chưa có video", "/dung-video-thi-nghiem". KHÁC video ôn tập tóm tắt (có giọng đọc) và chen-video-thi-nghiem.mts (chèn clip YouTube có sẵn).
---

# Dựng video thí nghiệm tự làm (không giọng)

Thầy chốt 27/10/2026: thí nghiệm không có clip YouTube thì tự dựng; chỉ **phụ đề + nhạc**, giọng đọc dành riêng cho video ôn tập. Ba clip mẫu đã duyệt: `clips/boyle.py`, `clips/chuyenthe.py`, `clips/camungdt.py` (Opus làm lại, thầy đồng ý 27/10).

## Quy trình một clip
1. Đọc `content/thi-nghiem/<id>.json` (`cac_buoc`, `so_lieu_mau`, `tham_so`, `hien_tuong_hay_sai`, `sai_so_thuong_gap`) và `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md`. **Mọi con số trong clip phải có trong `so_lieu_mau`/`tham_so`** — không nội suy, không bịa điểm.
2. Copy clip mẫu gần nhất thành `scripts/video-thi-nghiem/clips/<tên>.py` (Boyle = dụng cụ + bảng + đồ thị; chuyenthe = đồ thị theo thời gian; camungdt = nhiều bước so sánh). Chỉ viết file clip; **không sửa `engine.py`** khi làm hàng loạt (nhiều agent song song).
3. Cấu trúc bắt buộc, 35–50 s (hơn 50 s HS bỏ): **Dự đoán → Tiến hành (vẽ động theo số liệu mẫu) → Rút ra (cơ chế, ý "chưa nói được gì") → Bẫy hay gặp**.
4. Hộp **Dự đoán**: các lựa chọn cùng màu, cùng cỡ, cùng kiểu; không gợi ý đáp án bằng màu/vị trí/kích thước; có thanh đếm để HS dừng nghĩ ≥ 4–5 s; phụ đề không nhắc đáp án. Nhãn A. B. C. D. (E1).
5. Phụ đề ngắn, 16–41 ký tự, mỗi câu 2,2–4,4 s (`cap_dur ≈ 0,052·số ký tự + 0,9`). Chữ nhỏ nhất ≥ 32 px trên khung 1080 (≈ 11 px ở 375 px), chữ chính ≥ 36 px.
6. Kiểm: `python3 scripts/video-thi-nghiem/render.py <tên> --preview` (PNG ở `ra/<id>-preview/`, ghép nhiều khung thành một ảnh rồi mới đọc), sửa đến khi không chồng nhãn/cắt mép; rồi `render.py <tên>` ra `ra/<id>.mp4` (~2–4 phút, **chạy trong tab terminal**, song song được). Kiểm độ dài, có audio, < 3 MB.
7. Chạy lô: mỗi agent (Opus cho chất lượng hình) một clip, **mỗi agent một thư mục nháp con riêng** trong scratchpad; commit đúng file `clips/*.py` (mp4 nằm `ra/`, gitignore).

## Bẫy kỹ thuật đã gặp
- Pillow 11 bỏ qua alpha khi vẽ chữ trên ảnh RGB → chữ "hiện dần" thật ra hiện ngay. Engine đã sửa (27/10): dùng `text/ctext/rich` hoặc `dtext`, **không gọi `d.text(... fill=A(...))` trực tiếp** với alpha < 1; nếu cảnh vẽ trên ảnh phụ thì gán `IMG_REF[0] = img`.
- Engine làm mờ đầu mỗi cảnh → các bước cần liền mạch (cắm nhanh/chậm/rút) gộp vào MỘT cảnh.
- Engine chỉ xem thử 3 khung mỗi cảnh; viết script ghép khung theo mốc phụ đề để bắt lỗi kim lệch/nhãn chồng.
- Vẽ chi tiết che nhau (nam châm vào cuộn dây): vẽ nửa sau dưới, nửa trước đè lên; vật mờ dần vẽ trên lớp riêng rồi mới làm mờ.
- Nhạc tổng hợp numpy (`music()`), không dính bản quyền; không chép nhạc ngoài.

## Sau khi render
mp4 chưa chèn vào bài: chỗ đặt (YouTube không công khai + `scripts/chen-video-thi-nghiem.mts` hay file tĩnh trong web) thầy chưa chốt. Không tự đăng. Lô: 1 = L12 còn lại (~40), 2 = L12 + L11 điện (~60), 3 = L11 dao động + L9 (~45), 4 = L10 (~112).

## Nhật ký rút kinh nghiệm
- 2026-10-27 · Bản đầu của 3 clip dài 43–65 s, hộp Dự đoán tô khác màu từng lựa chọn (lộ đáp án), nhiều nhãn chồng, có số nội suy không có trong dữ liệu → viết lại bằng Opus theo quy tắc trên, thầy duyệt.
- 2026-10-27 · Agent song song dùng chung scratchpad làm ảnh ghép đè nhau → mỗi agent thư mục con riêng.
