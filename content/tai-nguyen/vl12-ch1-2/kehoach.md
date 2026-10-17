# Kế hoạch tài nguyên — Vật lí 12, Chương 1 (Vật lí nhiệt) và Chương 2 (Khí lí tưởng)

Nguồn: bài đã đăng (snapshot `public/data/lessons` 17/10/2026), id 2–9. Hiện cả 8 bài: 0 PhET, 0 video, 0 ảnh; hình trong bài đều là SVG tự vẽ (3–4 hình/bài).
PhET đã kiểm HTTP 200 cả bản `_vi` lẫn `_en` ngày 18/10/2026 (chưa mở thật; mở thật khi làm theo skill `phet`).
Video: chưa tìm. Bước tìm + kiểm sau khi thầy duyệt bảng này. Không có mốc thì ghi `prompts-video.md` cho Gemini.

## PhET (Claude làm)

| # | Bài | Vị trí | Học sinh vướng ở đâu | Sim | Câu dẫn dắt (dự kiến) |
|---|---|---|---|---|---|
| 1 | 2 · Sự chuyển thể | §II, sau thí nghiệm đun nước đá | Không thấy phân tử đổi cách sắp xếp khi nóng chảy/hoá hơi; vì sao nhiệt độ đứng yên | `states-of-matter` | Tăng nhiệt từ rắn đến khí: phân tử đổi thế nào ở từng giai đoạn? |
| 2 | 3 · Thang nhiệt độ | §II, thí nghiệm kéo dài p(t) về 0 K | Độ không tuyệt đối trừu tượng | `gas-properties` | Hạ nhiệt độ gần 0 K: áp suất và chuyển động phân tử ra sao? |
| 3 | 4 · Nội năng, ĐL1 NĐLH | §II, thí nghiệm bơm xe | Công làm khí nóng lên khó hình dung | `gas-properties` (kéo/ấn pittông) | Nén nhanh: nhiệt độ thay đổi thế nào? Vì sao? |
| 4 | 4 · Nội năng, ĐL1 NĐLH | §II, số liệu đo c của nước | Nhiệt lượng nhận vào chia ra thế nào | `energy-forms-and-changes` (tab Nhiệt hệ thống) | So sánh nước với sắt, gạch cùng khối lượng, cùng nhiệt lượng |
| 5 | 6 · Thuyết động học chất khí | §II, quan sát hạt khói | Không thấy va chạm phân tử gây ra chuyển động Brown | `gas-properties` | Quan sát một hạt nặng: vì sao nó chạy lung tung? |
| 6 | 6 · Thuyết động học chất khí | §II, khói trắng trong ống khuếch tán | Khuếch tán và tốc độ phụ thuộc khối lượng phân tử | `diffusion` | Hai khí khác khối lượng: khí nào lan nhanh hơn? |
| 7 | 7 · Boyle – Charles | §II, hai thí nghiệm đẳng nhiệt/đẳng áp | Tự đổi V hoặc T xem p | `gas-properties` | Giữ T không đổi, thu nhỏ V một nửa: p đổi bao nhiêu? |
| 8 | 8 · PT trạng thái | §II, bình kín ngâm nước 5 nhiệt độ | Đẳng tích, p/T không đổi | `gas-properties` (khoá thể tích) | Tăng T từng bước, ghi p: p/T có đổi không? |
| 9 | 9 · Áp suất, động năng phân tử | §II, hạt đập vào thành hộp | Vô số va chạm cộng thành áp suất | `gas-properties` | Tăng số hạt rồi tăng nhiệt độ: áp suất tăng vì lý do nào? |

Bài 5 (Thực hành đo c, λ, L): chưa có sim khớp, bỏ PhET.

## Video (Claude tìm + kiểm sau khi duyệt; chưa có link nào)

| # | Bài | Chỗ cần | Học sinh cần quan sát |
|---|---|---|---|
| V1 | 2 | Mở bài hoặc thí nghiệm rượu + nước | Thể tích hỗn hợp nhỏ hơn tổng hai thể tích |
| V2 | 2 | Thăng hoa (đá khô/iốt) | Chất rắn bay thẳng thành khí |
| V3 | 3 | Ba nhiệt kế đo một cốc nước | Nhiệt kế tiếp xúc khác hồng ngoại |
| V4 | 4 | Bơm xe nóng lên | Thân bơm nóng ở đâu |
| V5 | 5 | Đun đá đến hơi, đoạn nằm ngang | Nhiệt độ đứng yên khi đang đổi trạng thái |
| V6 | 6 | Chuyển động Brown | Hạt khói nhảy không có quy luật |
| V7 | 7 | Nén khí trong ống tiêm bịt đầu | p tăng khi V giảm |
| V8 | 9 | Quả bóng bàn bẹp ngâm nước nóng | Bóng phồng lại vì áp suất khí tăng |

## Hình (Gemini, chỉ ảnh đời sống không số liệu)

Cả 8 bài đã có SVG tự vẽ cho phần có số liệu. Đề xuất chỉ 3 ảnh mở bài đời sống, còn lại để nguyên:

| # | Bài | Ảnh | Tỉ lệ |
|---|---|---|---|
| H1 | 2 | Ly nước đá đọng giọt nước trên bàn (không chữ) | 16:9 |
| H2 | 3 | Nhiệt kế y tế và nhiệt kế hồng ngoại đặt cạnh nhau | 16:9 |
| H3 | 7 | Bơm xe đạp tay, thân bơm nóng | 16:9 |

Prompt Gemini viết khi thầy duyệt dòng H1–H3 (theo `prompts.md` của skill).

## Cần thầy quyết
1. Duyệt/sửa/bỏ từng dòng PhET (9 dòng), video (8 dòng), ảnh (3 dòng).
2. Có muốn đặt PhET trong `<details>` (mặc định theo skill `phet`) để bài không dài thêm trên 375px?
