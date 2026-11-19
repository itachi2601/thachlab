# Kế hoạch cải tiến clip thí nghiệm motion graphic (rà 19/11/2026)

Nguồn: phiên `claude/motion-graphic-video-review-17d781`. Ba học sinh ảo (L9, L10, L12) xem khung hình cỡ 375px, mỗi khung cách 2 giây,
của ba clip đang đăng: `tn-l10-nemngang-01-20261119`, `tn-l9-khucxa-02-20261119`, `tn-l12-thuchanhtu-04-20261119-2`;
khung tương tác đo ở `/dev/video-tuong-tac` cỡ 375×812.
Giới hạn: học sinh ảo, 3 trên hơn 200 clip, chưa mở trong trang bài thật bằng tài khoản học sinh. Điểm số là hướng; số đo px là đo thật.

## 1. Kết quả đo

| Tiêu chí | Ném ngang L10 | Khúc xạ L9 | Cân dòng điện L12 |
|---|---|---|---|
| Hiểu bài | 6 | 5 | 6 |
| Đọc kịp | 5 | 4 | 4 |
| Nhìn rõ trên điện thoại | 5 | 6 | 5 |
| Muốn xem hết | 5 | 5 | 6 |
| Từ/phút cả clip (`--do-chu`) | 182 | 172 | 199 |
| Cảnh dày nhất (từ/phút) | hook 236, end 234, bẫy 220 | end 214, bẫy 210 | chuỗi 234, hook 233, end 224 |

Số đo hiển thị (375×812):
- Video trong bài rộng 283px, cao 503px (62% chiều cao màn) → tỉ lệ thu 0,262. Chữ 32px trong mp4 còn ≈ 8,4px; 36px còn ≈ 9,4px. Toàn màn hình (375px) chữ 32px còn ≈ 11px.
- Lúc dừng ở câu Dự đoán: video dính chiếm y 8–511; chữ câu hỏi ở y 364, lựa chọn A ở 431, B ở 487 (nằm SAU video), C ở 543, D ở 599.
  Khoảng trống dưới video ≈ 245px (trừ thanh điều hướng dưới), không đủ cho câu hỏi + 4 lựa chọn × 48px.
- Video dừng ở 8,69 s trong khi cảnh Dự đoán của `thuchanhtu4` kết thúc ở 8,2 s → hình lúc dừng đã sang cảnh sau.
- Khi dừng, thanh điều khiển gốc của trình duyệt đè lên phụ đề và dòng chân trang của clip.

Lỗi nội dung học sinh ảo nêu:
- Câu chốt cuối clip không có đáp án; hình đứng yên khoảng 8 giây.
- Nhiều thứ mới hiện cùng một nhịp (bảng + "ĐÁP ÁN" + công thức + phụ đề đổi). Cảnh Bẫy `thuchanhtu4` dồn ≈ 20 từ vào 2 giây.
- Ký hiệu chưa giới thiệu: `l` (thuchanhtu4), `sin` và `n`/chiết suất (khucxa2); nhãn i, r chỉ hiện 4 giây đầu.
- Cảnh Bẫy `nemngang1`: "lệch 1–2 khung hình" không hiểu được; câu bị gạch ngang gây lẫn.
- Dòng "Chọn đáp án ở khung câu hỏi" trong clip vô nghĩa khi xem toàn màn hình hoặc xem mp4 rời.
- Nhãn trên hình 8–11px ở cỡ điện thoại, chữ xám nhạt; nhiều cảnh trống 1/3–2/3 khung, hình dụng cụ chỉ cao ≈ 100px.
- Chỉ có một điểm bấm trong cả clip; học sinh muốn tự kéo biến (độ cao máng, góc laser, dòng I, đảo chiều).

## 2. Các việc, xếp theo lợi ích trên công sức

Mỗi việc một phiên riêng, làm được độc lập trừ chỗ ghi "sau việc …". Việc 1 và 2 cùng đụng `components/lessons/VideoThiNghiemKhung.tsx` → làm lần lượt, không song song.

### Việc 1 — Khung Dự đoán không bị video che trên điện thoại
- **Model:** Sonnet (sửa một component, có số đo rõ).
- **File:** `components/lessons/VideoThiNghiemKhung.tsx` (lớp dính và chiều cao ở dòng ~447–452; `scrollIntoView` dòng ~196; chỗ dừng dòng ~119).
- **Làm:** khi đang dừng ở câu hỏi trên màn < lg: thu video còn ≈ 35–40svh hoặc bỏ dính; cuộn sao cho câu hỏi nằm ngay dưới video
  (tính cả chiều cao video dính và thanh điều hướng dưới); dừng sớm hơn ≈ 0,5 s để hình còn là hình của câu hỏi; ẩn thanh điều khiển gốc lúc dừng
  hoặc dời để không đè phụ đề.
- **Đạt khi:** ở 375×812 và 375×667, lúc dừng: chữ câu hỏi + cả 4 lựa chọn + "Chưa muốn đoán" có `getBoundingClientRect().top` ≥ đáy video
  và đáy ≤ đỉnh thanh điều hướng dưới, không cần cuộn; mọi nút ≥ 44px; màn ≥ 1280 không đổi. Thử ít nhất 3 clip ở `/dev/video-tuong-tac`.
- **Mã quy tắc:** K7 (skill `dung-video-thi-nghiem`), checklist mục 8 của `docs/QUY-TAC-THIET-KE.md` (chụp 375px trước).

### Việc 2 — Đưa câu chốt ra khung, có đáp án (sau việc 1)
- **Model:** Opus cho thiết kế + component; Sonnet cho việc điền dữ liệu từng clip.
- **File:** `components/lessons/VideoThiNghiemKhung.tsx`, kiểu `VideoKhungData`, `scripts/video-thi-nghiem/xuat-khung.py` (`--kiem`),
  `content/thi-nghiem/video-khung/*.json`.
- **Làm:** thêm trường tuỳ chọn cho câu chốt (câu hỏi, lựa chọn hoặc đáp số, giải thích, mốc giây); video dừng lần hai ở đầu cảnh Chốt,
  học sinh trả lời rồi mới hiện đáp án. Clip chưa có trường này chạy như cũ. Điền trước cho 3 clip đã rà, sau đó theo lô.
- **Đạt khi:** `--kiem` nhận trường mới; 3 clip mẫu có đáp án câu chốt khớp `content/thi-nghiem/<id>.json`; phản hồi không điểm, không xếp hạng (K6).
- **Cần thầy quyết trước:** câu chốt dạng chọn A–D hay ô đáp số; có ghi kết quả vào DB để đo hay chưa.
- Tư vấn theo nghiên cứu trước khi làm (AGENTS: tính năng HS thấy): nêu mã quy tắc, 3–6 dòng, thầy quyết.

### Việc 3 — Cổng soát mới trong bộ dựng (chặn lỗi từ gốc)
- **Model:** Sonnet.
- **File:** `scripts/video-thi-nghiem/render.py` (`--do-chu`, `--sheet`), `.claude/skills/dung-video-thi-nghiem/SKILL.md`.
- **Làm:**
  - `--do-chu` báo lỗi khi một cảnh > 180 từ/phút (đang cho tới 260); thêm kiểm "một nhịp một thứ mới": trong cùng 2 giây không quá
    một khối chữ mới ngoài phụ đề.
  - Thêm `--sheet-375`: ảnh ghép thu về rộng 283px (cỡ hiển thị thật trong bài) để agent soát đọc được hay không; cổng B dùng ảnh này.
  - Checklist skill: chữ nhỏ nhất ≥ 48px trong mp4; ký hiệu mới phải có nhãn ngay lúc xuất hiện; không dùng dòng "Chọn đáp án ở khung câu hỏi"
    (đổi thành "Dừng lại, tự đoán"); cảnh Bẫy có hình tự giải thích, không dựa vào chữ gạch ngang; không để hình đứng yên > 4 giây.
- **Đạt khi:** chạy `--do-chu` trên 3 clip đã rà báo đúng các cảnh dày ở bảng mục 1; `--sheet-375` ra file; skill có mục Nhật ký tương ứng.
- Không sửa `engine.py` trong lúc có phiên khác đang dựng lô.

### Việc 4 — Dựng lại clip theo cổng mới (sau việc 3)
- **Model:** Opus mỗi clip một agent (chất lượng hình), `kiem-code` (Sonnet) soát ảnh ghép 283px. Ước ≈ 2,5 USD/clip.
- **File:** `scripts/video-thi-nghiem/clips/*.py`, khung JSON, sổ `content/thi-nghiem/so-clip-anh-dong.md`.
- **Làm:** bắt đầu bằng 3 clip đã rà để chốt mẫu, gửi thầy duyệt, rồi mới theo lô, ưu tiên bài nhiều học sinh xem:
  - `nemngang1`: vẽ lại cảnh Bẫy (hai bi thả lệch nhau, có nhãn); tách công thức t và L thành hai nhịp; ghi rõ đường cong lần 1/lần 2.
  - `khucxa2`: giữ nhãn i, r suốt phần Tiến hành; một nhịp giới thiệu `sin i / sin r` trước cột số; nêu "≈ 1,5 = chiết suất n" ở Kết quả.
  - `thuchanhtu4`: chú thích `l` = chiều dài đoạn dây trong từ trường; cảnh Bẫy tách 3 bước ≥ 3 s; phóng to hộp Q, P, F′.
  - Cả ba: chữ ≥ 48px, bỏ chữ xám nhạt, phóng hình dụng cụ vào chỗ trống, cắt 8 giây tĩnh cuối (đã có việc 2) để giãn cảnh Bẫy; vẫn ≤ 50 s.
- **Đạt khi:** qua cổng A + B mới; mp4 < 3 MB; tải bản mới lên `lesson-clips` với hậu tố ngày; đổi URL trên DB bằng `scripts/doi-ban-clip-db.mts`
  sau 22h, có sao lưu; ghi sổ clip.

### Việc 5 — Mô phỏng tự kéo sau clip cho thí nghiệm một biến
- **Model:** Opus (thiết kế tương tác + vật lí), phiên chính làm UI học sinh.
- **File:** `components/physics/` (mẫu: `GasGraphsSimulation.tsx`, `ChargeInFieldSimulation.tsx`, `PredictGate.tsx`),
  `components/lessons/MoPhongPortals.tsx`, xem thử `/dev/mo-phong-tu-keo`.
- **Làm:** ba mô phỏng đầu: ném ngang (kéo độ cao máng và v0), khúc xạ bán trụ (kéo góc tới), cân dòng điện (thanh I + nút đảo chiều).
  Có dự đoán trước khi kéo; `next/dynamic({ssr:false})` + `LazyErrorBoundary`; không thêm round-trip Supabase.
- **Đạt khi:** chạy ở 375px, đích chạm ≥ 44px, số liệu khớp `so_lieu_mau` của kho thí nghiệm; gắn vào bài bằng hộp `.tl-mo-phong` rồi
  `cap-nhat-ly-thuyet.sh` sau khi thầy duyệt.
- Tư vấn theo nghiên cứu trước khi làm, thầy quyết.

## 3. Việc nên làm thêm để tin được kết quả
- Mở một bài thật bằng tài khoản học sinh trên điện thoại thật, xác nhận lỗi che ở việc 1 (mới đo ở trang `/dev`).
- Sau việc 1–2: nối `onEvent` của khung vào bảng ghi (cần migration, agent `kien-truc-du-lieu`) để đo tỉ lệ chọn, bỏ qua, xem lại
  trên học sinh thật — đây mới là thước đo hiệu quả, thay cho học sinh ảo.
