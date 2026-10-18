# Kế hoạch soạn nội dung ôn thi Giải Vật lí trên máy tính cầm tay (Casio)

Soạn ngày 18/10/2026. Người soạn dần: **Opus** (phiên Mac, soạn trực tiếp, không Batch API). Người duyệt: thầy Thạch.
Khung ôn tập 12 tuần (giả định thi giữa tháng 1/2027) nằm ở cuộc trò chuyện 18/10; bản rút gọn ở mục 1.

## 0. Việc chặn mọi thứ: thể lệ chưa xác nhận
Chưa đọc được Công văn 5704/SGDĐT-GDPT (TP.HCM, 12/12/2025) và công văn năm 2026–2027. Các điểm dưới đây **chưa có nguồn**, WP-00 phải chốt trước khi soạn bài tập:
- hình thức (tự luận ghi tóm tắt cách giải + kết quả?), thời gian, số bài, thang điểm;
- quy tắc làm tròn / số chữ số có nghĩa; danh sách máy được dùng (fx-580VN X đã được Bộ cho phép);
- nội dung/chương trình thi (lớp 12 chương trình mới 2018? có kèm lớp 10–11?);
- ngày thi năm học 2026–2027.
Thầy dán văn bản vào phiên (sandbox không vào được thuvienphapluat.com). Chưa có thể lệ thì chỉ soạn WP-01, WP-02 (không phụ thuộc thể lệ).

## 1. Khung 4 giai đoạn
| GĐ | Tuần | Nội dung |
|---|---|---|
| 1 | 1–2 | Kỹ năng máy fx-580VN X |
| 2 | 3–8 | Sáu chuyên đề: dao động · sóng · điện xoay chiều · điện từ + sóng ánh sáng · lượng tử + hạt nhân · nhiệt + khí lí tưởng + từ trường |
| 3 | 9–10 | Bài tổng hợp, thực nghiệm, sai số, hồi quy |
| 4 | 11–12 | Đề thi thử + sổ lỗi máy |

## 2. Quy ước chung cho mọi gói (đọc trước khi soạn)
**Vị trí:** `content/casio-vat-ly/<mã-gói>/` (ví dụ `gd2-cd1-dao-dong/`), mỗi gói có `README.md` ngắn (file nào là gì, chỗ chưa chắc) và `nguon.json` (xem dưới).
**Định dạng một bài tập** (Markdown + KaTeX, công thức có `<`/`>` viết `\lt`/`\gt`):
1. Đề (số liệu cụ thể, đơn vị, yêu cầu làm tròn đúng quy tắc thể lệ)
2. Đáp số (ghi dạng thể lệ yêu cầu)
3. **Quy trình bấm máy**: từng bước, ghi phím/chế độ (MODE, SOLVE, CALC, TABLE…), biến nhớ dùng (A, B, C, M); mỗi ý một dòng
4. Lời giải: công thức chữ trước, số sau, đơn vị, rồi kết quả
5. Bẫy: lỗi làm tròn giữa chừng, đổi đơn vị, rad/độ, chế độ máy sai…
6. Mức: ⭐ cơ bản · ⭐⭐ đúng cấp thi · ⭐⭐⭐ phân loại
**Mỗi chuyên đề:** 3 trang "kỹ thuật" (công thức + cách bấm cho từng dạng) + 12 bài (4⭐ · 6⭐⭐ · 2⭐⭐⭐) + 1 mini-test 30 phút (4 bài).
**Hình:** SVG tự vẽ (helper `.claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py`); đường sức từ nét đứt, chú thích mỗi ý một dòng.
**Số liệu:** tính bằng Python (`decimal`/`numpy`), lưu script cùng thư mục; đáp số trong tài liệu phải sinh từ script, không tính tay.
**Bản quyền (xem AGENTS.md):** tự soạn đề, đổi số liệu/ngữ cảnh; không chép đề Casio các tỉnh, không chép sách. Nếu phỏng theo một đề thật thì ghi nguồn trong `nguon.json`; không rõ nguồn thì không dùng.
**Cách bấm máy:** chưa có máy thật để thử thì ghi rõ "chưa thử trên máy" trong README. Không bịa tên phím; thầy (hoặc `kiem-code`) bấm thử một mẫu mỗi chuyên đề.

## 3. Danh sách gói công việc (thứ tự soạn)
| Mã | Gói | Sản phẩm | Phụ thuộc | Trạng thái |
|---|---|---|---|---|
| WP-00 | Chốt thể lệ + chương trình thi | `the-le.md` (tóm tắt có dẫn nguồn, mục chưa rõ liệt kê) | thầy dán công văn | chờ thầy |
| WP-01 | GĐ1: sổ tay fx-580VN X cho Vật lí | 8 trang: SOLVE · CALC · TABLE · số phức (RLC, tổng hợp dao động) · vectơ · thống kê/hồi quy · hằng số & đổi đơn vị · biến nhớ; 20 bài luyện thao tác | không | nháp xong 18/10, đã kiểm 2 lần; chờ thầy bấm thử máy |
| WP-02 | GĐ1: quy tắc ghi kết quả + làm tròn | 1 trang + 10 cặp "làm tròn sai / đúng" có số thật | WP-00 (quy tắc làm tròn) | chưa soạn |
| WP-03 | CĐ1 Dao động cơ | theo mục 2 | WP-00, WP-01 | nháp xong 18/10 (thể lệ tạm), đã kiểm 2 lần; chờ thầy duyệt + rà theo thể lệ |
| WP-04 | CĐ2 Sóng cơ, giao thoa, sóng dừng | theo mục 2 | WP-03 | nháp xong 18/10 (thể lệ tạm), đã kiểm 2 lần; chờ thầy duyệt + rà theo thể lệ |
| WP-05 | CĐ3 Điện xoay chiều (RLC, cực trị, công suất) | theo mục 2 | WP-01 (số phức) | nháp xong 18/10 (thể lệ tạm), đã kiểm 2 lần; chờ thầy duyệt + rà theo thể lệ |
| WP-06 | CĐ4 Dao động–sóng điện từ, sóng ánh sáng | theo mục 2 | — | nháp xong 18/10 (thể lệ tạm), đã kiểm 2 lần; chờ thầy duyệt + rà theo thể lệ |
| WP-07 | CĐ5 Lượng tử, hạt nhân (độ hụt khối, phóng xạ, ln) | theo mục 2 | — | chưa soạn |
| WP-08 | CĐ6 Nhiệt, khí lí tưởng, từ trường (chương trình mới) | theo mục 2 | WP-00 (có thi nội dung này không) | chưa soạn |
| WP-09 | GĐ3: 20 bài tổng hợp + 10 bài thực nghiệm (bảng số liệu, đồ thị, sai số, hồi quy) | theo mục 2 | WP-03…08 | chưa soạn |
| WP-10 | GĐ4: 6 đề thi thử đúng cấu trúc thể lệ + đáp án + barem | PDF dàn bằng `_tools/trang-mau-sach` | WP-00, WP-09 | chưa soạn |
| WP-11 | Sổ lỗi máy: mẫu bảng + 40 lỗi điển hình rút từ các gói | 2 trang | WP-03…10 | chưa soạn |

Gợi ý nhịp: mỗi phiên Opus làm **một gói** (WP-03…08 mỗi gói ≈ 1 phiên). Làm xong gói nào thì cập nhật cột Trạng thái ở bảng này và commit.

## 4. Kiểm chất lượng (bắt buộc trước khi đánh dấu xong)
1. Lần 1 bằng máy: script Python tính lại toàn bộ đáp số, so với đáp số trong tài liệu; render KaTeX không lỗi.
2. Lần 2 độc lập: giao `kiem-code` giải từ đề **không kèm đáp án**, rồi đối chiếu; bài lệch thì sửa hoặc bỏ.
3. Thầy bấm thử mẫu quy trình bấm máy (3 bài/chuyên đề) trên máy thật.
4. Hình SVG xem ở 375px; PDF xem bằng mắt trước khi báo xong.
Chưa qua 1 và 2 thì để trạng thái "nháp", không đăng.

## 5. Đưa lên thachlab (chỉ khi thầy bảo)
Bài tập tự chấm có đáp số → qua `docs/DANG-DE-TU-WORD.md` hoặc skill đăng đề, nhãn Chủ đề/Dạng đầy đủ, nhãn câu hỏi như đề thật (E1–E3). Máy tính trên web: bài làm là điền đáp số (Phần III). Kiểm 2 lần trước khi bật Hiện (AGENTS.md mục "Chất lượng đề").

## 6. Prompt mẫu giao Opus (một gói)
> Soạn gói **WP-0X** trong `docs/KE-HOACH-CASIO-VAT-LY.md`. Đọc mục 0, 2, 4 và `the-le.md` (nếu đã có) trước. Sản phẩm vào `content/casio-vat-ly/<mã-gói>/`. Đáp số sinh từ script Python cùng thư mục. Xong thì giao `kiem-code` giải độc lập, sửa chỗ lệch, cập nhật cột Trạng thái, commit đúng đường dẫn. Cuối phiên ghi mục "Rút kinh nghiệm" vào cuối file này.

## Nhật ký rút kinh nghiệm
- 2026-10-18 · WP-01: tên phím/menu soạn khi chưa có máy thật → để cờ "chưa thử trên máy" trong README, nhờ thầy bấm thử 4 bài đại diện; đáp số sinh từ `tinh.py` rồi giao `kiem-code` giải từ đề đã tách đáp án (grep dòng Đề) — rẻ và đủ.
- 2026-10-18 · WP-03: kiem-code bắt lỗi ở CÔNG THỨC trong lời giải (arctan sai, thiếu điều kiện A≥0, S tắt dần chỉ đúng khi dừng ở O) dù mọi đáp số đúng → khi soạn kỹ thuật/lời giải, luôn ghi điều kiện áp dụng của từng công thức; đáp số khớp chưa đủ để coi lời giải đúng.
- 2026-10-18 · WP-04: kiem-code bắt số học trong phần "Bẫy" (65,17 chứ không phải 66,5) và giả thiết ẩn (nguồn kết hợp hay không) → mọi con số phụ trong Bẫy/ghi chú cũng phải sinh từ tinh.py, và đề có thao tác cộng nguồn phải nêu loại nguồn.
- 2026-10-18 · Tách đề khỏi đáp án để kiểm độc lập: `sed` theo mẫu `**M1.` bắt cả khối đáp án (cũng bắt đầu bằng `**M1.`) → WP-03/04 mini-test từng bị kiểm không độc lập. Tách bằng `split('## Đáp án')[0]` rồi đọc lại file đề xem có lọt đáp án không; đã kiểm lại 12/12 khớp.
- 2026-10-18 · Tên phím/biến máy: đã dùng biến `W` (không có trên fx-580VN X: chỉ A–F, X, Y, M) trong WP-03..06, kiem-code mới bắt ở WP-06 → khi soạn lệnh bấm máy, tra danh sách biến/phím trong so-tay.md (đã ghi rõ), và nhờ kiem-code rà tên phím/biến ngay từ gói đầu.
- 2026-10-18 · Không đọc được thể lệ gốc (sandbox chặn thuvienphapluat.com) → xin thầy dán công văn ngay từ đầu, đừng soạn bài tập khi chưa chốt quy tắc làm tròn.
