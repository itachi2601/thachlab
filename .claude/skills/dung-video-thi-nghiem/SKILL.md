---
name: dung-video-thi-nghiem
description: Tự dựng video 9:16 KHÔNG giọng (phụ đề + nhạc tổng hợp) cho thí nghiệm trong content/thi-nghiem/ mà YouTube không có clip — viết kịch bản Python theo mẫu boyle/chuyenthe/camungdt, số liệu lấy từ so_lieu_mau, hộp Dự đoán đồng màu, render bằng scripts/video-thi-nghiem. Dùng khi thầy nói "làm video thí nghiệm X", "làm lô 1 video thí nghiệm", "thí nghiệm nào chưa có video", "/dung-video-thi-nghiem". KHÁC video ôn tập tóm tắt (có giọng đọc) và chen-video-thi-nghiem.mts (chèn clip YouTube có sẵn).
---

# Dựng video thí nghiệm tự làm (không giọng)

Thầy chốt 27/10/2026: thí nghiệm không có clip YouTube thì tự dựng; chỉ **phụ đề + nhạc**, giọng đọc dành riêng cho video ôn tập. Ba clip mẫu đã duyệt: `clips/boyle.py`, `clips/chuyenthe.py`, `clips/camungdt.py` (bản 3, 27/10: có cảnh đáp án, cảnh chốt `chot_hoi()` trong engine, tiếng báo `cues`). Cảnh chốt mới dùng `chot_hoi(d, t, sc, chot, hoi, goi_y)` thay vì tự vẽ.

## Quy trình một clip
1. Đọc `content/thi-nghiem/<id>.json` (`cac_buoc`, `so_lieu_mau`, `tham_so`, `hien_tuong_hay_sai`, `sai_so_thuong_gap`) và `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md`. **Mọi con số trong clip phải có trong `so_lieu_mau`/`tham_so`** — không nội suy, không bịa điểm.
2. Copy clip mẫu gần nhất thành `scripts/video-thi-nghiem/clips/<tên>.py` (Boyle = dụng cụ + bảng + đồ thị; chuyenthe = đồ thị theo thời gian; camungdt = nhiều bước so sánh). Chỉ viết file clip; **không sửa `engine.py`** khi làm hàng loạt (nhiều agent song song).
3. Cấu trúc bắt buộc, 35–50 s (hơn 50 s HS bỏ): **Dự đoán → Tiến hành (vẽ động theo số liệu mẫu) → Đáp án + Rút ra (cơ chế, ý "chưa nói được gì") → Bẫy hay gặp → Chốt 1 câu + câu hỏi tự nhớ lại**.
4. Hộp **Dự đoán**: các lựa chọn cùng màu, cùng cỡ, cùng kiểu; không gợi ý đáp án bằng màu/vị trí/kích thước; có thanh đếm để HS dừng nghĩ ≥ 4–5 s; phụ đề không nhắc đáp án. Nhãn A. B. C. D. (E1).
5. Phụ đề ngắn, 16–41 ký tự, mỗi câu 2,2–4,4 s (`cap_dur ≈ 0,052·số ký tự + 0,9`). Chữ nhỏ nhất ≥ 32 px trên khung 1080 (≈ 11 px ở 375 px), chữ chính ≥ 36 px.
6. **Xem thử và góp ý TRƯỚC khi render** (thầy chốt 27/10/2026). Render mất 2–4 phút; mỗi lần render rồi mới thấy lỗi là phải xem lại khung hình và render lại. Chặn lỗi bằng hai cổng rẻ, đặt **sau khi viết xong file clip, trước lệnh render**:
   - **Cổng A — kịch bản chữ, không ảnh (~1 s, vài trăm token):** `python3 scripts/video-thi-nghiem/render.py <tên> --kich-ban` in từng cảnh, mốc giây, phụ đề (số ký tự), tiếng báo, tổng giây. Người soạn tự soát bảng này theo checklist dưới. Sai cấu trúc/nội dung thì sửa ngay, chưa vẽ gì.
   - **Cổng B — MỘT ảnh ghép, đọc trong subagent (~1 s dựng):** `render.py <tên> --sheet` → `ra/<id>-sheet.png` (khung ở mỗi mốc phụ đề + 1,6 s và cuối cảnh, 6 cột). Giao **một** agent `kiem-code` đóng vai học sinh lớp N đang học bài đó: đưa đường dẫn ảnh + output cổng A + `so_lieu_mau`, yêu cầu trả ≤ 10 góp ý, mỗi dòng `mốc giây · lỗi · cách sửa`, xếp nặng → nhẹ. Phiên chính **không đọc ảnh ghép**; sửa xong chỉ cắt đúng vùng bị báo (crop) để tự kiểm, không dựng lại cả tấm. Tối đa 2 vòng cổng B.
   - Clip đầu tiên của một kiểu mới (mẫu mới, môn mới) → gửi ảnh ghép cho thầy (`SendUserFile`) trước khi render; clip trong lô theo mẫu đã duyệt thì không cần.
   - **Sau render chỉ đo, không xem lại hình:** độ dài, có audio, < 3 MB, và `ffmpeg -af silencedetect=n=-45dB:d=2` để kiểm tiếng báo rơi đúng mốc đã in ở cổng A.

   **Checklist cổng A + B** (lỗi đã gặp thật):
   - Dự đoán: lựa chọn cùng màu/cỡ; phụ đề không lộ; có ≥ 5 s im lặng để nghĩ.
   - Đồ thị/kết quả thật **khớp đúng một lựa chọn** nhìn bằng mắt (đoạn ngắn bị trục lớn "nuốt" thì phóng to), và có cảnh nói rõ "Đáp án X".
   - Mọi con số có trong `so_lieu_mau`/`tham_so`; nhãn trên màn hình khớp nhau (đồng hồ ↔ "số ghi ở phút").
   - Trục/thang không đổi giữa chừng; mỗi cơ chế (vd. tan và sôi) một hình riêng.
   - Kết bằng câu chốt + câu hỏi tự nhớ lại, không kết ở bẫy; tổng ≤ 50 s.
   - Chữ không chồng, không cắt mép phải (thanh/nhãn dài), chữ ≥ 32 px.
   Rồi `render.py <tên>` ra `ra/<id>.mp4` (**chạy trong tab terminal**, song song được). `--preview` (3 khung/cảnh, nhiều file) chỉ dùng khi cần soi riêng một cảnh.
7. Chạy lô: mỗi agent (Opus cho chất lượng hình) một clip, **mỗi agent một thư mục nháp con riêng** trong scratchpad; commit đúng file `clips/*.py` (mp4 nằm `ra/`, gitignore).

## Bẫy kỹ thuật đã gặp
- Pillow 11 bỏ qua alpha khi vẽ chữ trên ảnh RGB → chữ "hiện dần" thật ra hiện ngay. Engine đã sửa (27/10): dùng `text/ctext/rich` hoặc `dtext`, **không gọi `d.text(... fill=A(...))` trực tiếp** với alpha < 1; nếu cảnh vẽ trên ảnh phụ thì gán `IMG_REF[0] = img`.
- Engine làm mờ đầu mỗi cảnh → các bước cần liền mạch (cắm nhanh/chậm/rút) gộp vào MỘT cảnh.
- Ghép khung theo mốc phụ đề đã có sẵn: `--sheet` (bắt kim lệch/nhãn chồng); không viết lại script ghép.
- Vẽ chi tiết che nhau (nam châm vào cuộn dây): vẽ nửa sau dưới, nửa trước đè lên; vật mờ dần vẽ trên lớp riêng rồi mới làm mờ.
- **Âm thanh (thầy chốt 27/10/2026): không nhạc liền mạch** (Moreno & Mayer 2000: nhạc nền làm giảm nhớ). Clip khai `cues=` trả `[(giây, loại)]` → `engine.sfx()` chỉ phát tiếng ngắn ở mốc: `open` (hiện câu hỏi), `ding` (hết giờ dự đoán / lộ đáp án), `tap` (bắt đầu đoạn đặc biệt), `tick` (tua nhanh), `buzz` (bẫy); còn lại im, nhất là trong hộp Dự đoán. Mẫu: `_cues` trong `clips/chuyenthe.py`. Clip chưa có `cues` vẫn dùng `music()` cũ.

## Sau khi render
mp4 chưa chèn vào bài: chỗ đặt (YouTube không công khai + `scripts/chen-video-thi-nghiem.mts` hay file tĩnh trong web) thầy chưa chốt. Không tự đăng. Lô: 1 = L12 còn lại (~40), 2 = L12 + L11 điện (~60), 3 = L11 dao động + L9 (~45), 4 = L10 (~112).

## Nhật ký rút kinh nghiệm
- 2026-10-27 · Cổng B lần đầu (kiem-code vai HS) bắt được ở boyle/camungdt: thời gian nghĩ < 5 s, nhãn "Đáp án B" còn nằm sang bước sau, câu hỏi chốt cần dữ kiện clip chưa cho, chữ trong bài lệch số trong JSON (5% vs 8%), dòng "chưa nói được" không có nguồn → các mục này đã vào checklist; agent đọc ảnh nhỏ có khi báo nhầm chính tả, kiểm lại bằng mã trước khi sửa.
- 2026-10-27 · Bản 2 chuyenthe render xong mới phát hiện 5 lỗi nội dung qua góp ý học sinh → thêm cổng A (`--kich-ban`) + cổng B (`--sheet` đọc trong `kiem-code`) trước render; sau render chỉ đo bằng ffmpeg.
- 2026-10-27 · Học sinh ảo xem chuyenthe bản 2: đồ thị thật không khớp lựa chọn nào (đoạn −6→0 °C tàng hình trên trục 0–100), không lộ đáp án sau Dự đoán, nhãn "ghi lúc phút" lệch đồng hồ, trục t đổi thang giữa chừng → sau phần Tiến hành phải có cảnh "Đáp án X" + phóng to đoạn ngắn; trục cố định từ đầu; mỗi đoạn ngang một hình cơ chế riêng; kết bằng câu hỏi tự nhớ lại (không kết ở bẫy).
- 2026-10-27 · Bản đầu của 3 clip dài 43–65 s, hộp Dự đoán tô khác màu từng lựa chọn (lộ đáp án), nhiều nhãn chồng, có số nội suy không có trong dữ liệu → viết lại bằng Opus theo quy tắc trên, thầy duyệt.
- 2026-10-27 · Agent song song dùng chung scratchpad làm ảnh ghép đè nhau → mỗi agent thư mục con riêng.
