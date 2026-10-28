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
   - Hình vật lí đúng: đường sức (ra N vào S, không cắt nhau), chiều vectơ/lực/dòng, tỉ lệ hình học.
   - Ký tự font không có glyph (∝, ℓ) hiện ô vuông → viết bằng chữ; kiểm bằng mã. Chữ phụ (trục, chú thích, bullet) đo cỡ thật ≥ 32 px, màu đậm.
   - Màn chốt: chữ trên màn không trả lời sẵn câu hỏi, câu hỏi không trùng ca hộp Dự đoán, gợi ý hiện trễ ~2,5 s (tự vẽ qua `body`). Thẻ "chưa nói được gì" là từ khoá, ≥ 4 s; cảnh bẫy có hình ngay khi phụ đề lên; số trên bảng hiện trước khi phụ đề đọc tới.
   Rồi `render.py <tên>` ra `ra/<id>.mp4` (**chạy trong tab terminal**, song song được). `--preview` (3 khung/cảnh, nhiều file) chỉ dùng khi cần soi riêng một cảnh.
7. Chạy lô: mỗi agent (Opus cho chất lượng hình) một clip, **mỗi agent một thư mục nháp con riêng** trong scratchpad; commit đúng file `clips/*.py` (mp4 nằm `ra/`, gitignore).
   Subagent không gọi được agent khác → phiên chính điều phối 2 giai đoạn: agent dựng dừng sau `--sheet` (không đọc ảnh) và trả kịch bản; phiên chính giao `kiem-code` (Sonnet) đọc sheet; gửi góp ý bằng `SendMessage` về agent dựng để sửa + render. Mức "CẦN SỬA NẶNG" → vòng 2 gửi lại cho chính agent `kiem-code` cũ (rẻ, đã có ngữ cảnh). Commit từng clip ngay khi render xong.

## Bẫy kỹ thuật đã gặp
- Pillow 11 bỏ qua alpha khi vẽ chữ trên ảnh RGB → chữ "hiện dần" thật ra hiện ngay. Engine đã sửa (27/10): dùng `text/ctext/rich` hoặc `dtext`, **không gọi `d.text(... fill=A(...))` trực tiếp** với alpha < 1; nếu cảnh vẽ trên ảnh phụ thì gán `IMG_REF[0] = img`.
- Engine làm mờ đầu mỗi cảnh → các bước cần liền mạch (cắm nhanh/chậm/rút) gộp vào MỘT cảnh.
- Ghép khung theo mốc phụ đề đã có sẵn: `--sheet` (bắt kim lệch/nhãn chồng); không viết lại script ghép.
- Vẽ chi tiết che nhau (nam châm vào cuộn dây): vẽ nửa sau dưới, nửa trước đè lên; vật mờ dần vẽ trên lớp riêng rồi mới làm mờ.
- **Âm thanh (thầy chốt 27/10/2026): không nhạc liền mạch** (Moreno & Mayer 2000: nhạc nền làm giảm nhớ). Clip khai `cues=` trả `[(giây, loại)]` → `engine.sfx()` chỉ phát tiếng ngắn ở mốc: `open` (hiện câu hỏi), `ding` (hết giờ dự đoán / lộ đáp án), `tap` (bắt đầu đoạn đặc biệt), `tick` (tua nhanh), `buzz` (bẫy); còn lại im, nhất là trong hộp Dự đoán. Mẫu: `_cues` trong `clips/chuyenthe.py`. Clip chưa có `cues` vẫn dùng `music()` cũ.

## Sau khi render
mp4 chưa chèn vào bài: chỗ đặt (YouTube không công khai + `scripts/chen-video-thi-nghiem.mts` hay file tĩnh trong web) thầy chưa chốt. Không tự đăng. Lô: 1 = L12 còn lại (~40), 2 = L12 + L11 điện (~60), 3 = L11 dao động + L9 (~45), 4 = L10 (~112).

## Nhật ký rút kinh nghiệm
- 2026-10-28 · Lô 2 (7 clip L12 nhóm C, brief chung + brief kiem-code để trong file nháp, agent tự đọc): 18,3 USD, TB 2,61 USD/clip (2,10–2,82), cả 7 qua cổng B 1 vòng, 47,6–50,0 s, 1,7–2,3 MB. Đưa checklist lỗi lô 1 vào brief KHÔNG làm cổng B hết việc: vẫn bắt câu chốt bị bảng/cột số trên màn trả lời sẵn (3/7), lựa chọn chỉ khác chữ hoa/thường (p/t vs p/T), số lẻ duy nhất giữa số tròn lộ đáp án, đỉnh đồ thị sai tỉ lệ (2,4× thay vì 2×), nửa khung trống → câu chốt phải dùng giá trị CHƯA từng hiện trên màn; lựa chọn số viết dạng "khoảng N".
- 2026-10-28 · Lô 1 (10 clip L12 nhóm C, Opus dựng + kiem-code Sonnet cổng B): tổng 24,0 USD, TB 2,40 USD/clip (1,95–3,30; 2 clip phải 2 vòng cổng B tốn ~3 USD), 6–12 phút máy/clip, 46,8–49,9 s, 1,8–2,8 MB. Cổng B bắt được lỗi thật ở cả 10 clip (glyph ∝/ℓ vỡ, chữ phụ < 32 px, câu chốt trả lời sẵn/trùng Dự đoán, logic tên TN ≠ nội dung, thiếu P/cặp lực) → đã thêm vào checklist; quy trình 2 giai đoạn ghi ở bước 7.
- 2026-10-28 · Đo chi phí thật 3 clip thử (phongxa2/udcamung2/thangnhietdo4, Opus 5.5, đủ cổng A+B, render 1 lần): 1,7–2,0 USD/clip theo giá API (≈150–170k cache write, 1,7–2,6 triệu cache read, ~31–34k output), +0,5 USD nếu cổng B giao 2 vòng kiem-code Sonnet; 6,5–9,5 phút/clip. Agent tự đọc ảnh ghép thay vì giao kiem-code thì rẻ hơn nhưng mất mắt thứ hai → lô lớn vẫn giao kiem-code.
- 2026-10-27 · camungdt vẽ đường sức nam châm bằng elip kín bao cả thanh (cắt trục ngay trước cực N, sau cực S) — thầy bắt sai → đường sức phải ra ở N, vòng ngoài, vào ở S: dùng `_trace()`/`field()` trong `clips/camungdt.py` (lần theo trường hai cực, ép dọc cho vừa khung). Cổng B phải hỏi riêng "hình vật lí có đúng không" (đường sức, chiều lực, chiều dòng), không chỉ soát chữ/số.
- 2026-10-27 · Cổng B lần đầu (kiem-code vai HS) bắt được ở boyle/camungdt: thời gian nghĩ < 5 s, nhãn "Đáp án B" còn nằm sang bước sau, câu hỏi chốt cần dữ kiện clip chưa cho, chữ trong bài lệch số trong JSON (5% vs 8%), dòng "chưa nói được" không có nguồn → các mục này đã vào checklist; agent đọc ảnh nhỏ có khi báo nhầm chính tả, kiểm lại bằng mã trước khi sửa.
- 2026-10-27 · Bản 2 chuyenthe render xong mới phát hiện 5 lỗi nội dung qua góp ý học sinh → thêm cổng A (`--kich-ban`) + cổng B (`--sheet` đọc trong `kiem-code`) trước render; sau render chỉ đo bằng ffmpeg.
- 2026-10-27 · Học sinh ảo xem chuyenthe bản 2: đồ thị thật không khớp lựa chọn nào (đoạn −6→0 °C tàng hình trên trục 0–100), không lộ đáp án sau Dự đoán, nhãn "ghi lúc phút" lệch đồng hồ, trục t đổi thang giữa chừng → sau phần Tiến hành phải có cảnh "Đáp án X" + phóng to đoạn ngắn; trục cố định từ đầu; mỗi đoạn ngang một hình cơ chế riêng; kết bằng câu hỏi tự nhớ lại (không kết ở bẫy).
- 2026-10-27 · Bản đầu của 3 clip dài 43–65 s, hộp Dự đoán tô khác màu từng lựa chọn (lộ đáp án), nhiều nhãn chồng, có số nội suy không có trong dữ liệu → viết lại bằng Opus theo quy tắc trên, thầy duyệt.
- 2026-10-27 · Agent song song dùng chung scratchpad làm ảnh ghép đè nhau → mỗi agent thư mục con riêng.
- 2026-10-28 · Đăng 23 clip lên web: `tai-clip-len-storage.mts` chặn clip > 30 s (ngưỡng V9 của clip hiện tượng) → video thí nghiệm dùng `--toi-da 55`. Mỗi clip tải ~1 phút. Chèn bằng `chen-video-thi-nghiem.mts` (khớp theo id hộp trong bài, KHÔNG theo `nguon_trong_bai`) — thí nghiệm không có hộp trong bản đăng (udcamung-02: chỉ thư mục trùng `.cu` có) thì không chèn được, phải xem lại bài. Thứ tự đúng: tải → chèn → commit → đăng `cap-nhat-ly-thuyet-hang-loat.sh … --chi-video`.
- 2026-10-28 · `--chi-video` chặn gần hết bài vì DB còn câu nhắc Trả bài mà commit 991c422cc đã gỡ trong file → đừng vá từng mẫu chữ; so bản DB (bỏ video) với MỌI phiên bản git của theory.html: khớp một phiên bản = không có bản sửa trên web → `--cho-phep-khac` an toàn; không khớp = có hotfix trên web (lần này: `<br>` tách phương án sai) → chép vào file trước rồi mới đăng.
