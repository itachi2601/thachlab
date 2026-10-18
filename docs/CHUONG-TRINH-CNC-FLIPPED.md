# Chương trình CNC theo lớp đảo ngược (flipped) — đề xuất 18/10/2026

Đối tượng: sinh viên CĐ đã học tiện, phay cơ bản (máy vạn năng). Bản mẫu: `content/lesson-samples/cnc-flipped-bai-1/` (chưa ghi DB).
Giả định cần thầy xác nhận: **một buổi ≈ 3 tiết (135 phút)**; sinh viên có điện thoại để làm quiz ở nhà.

## Vì sao đảo ngược cho môn này
- Môn thực hành: giờ ở xưởng quý hơn giờ ngồi nghe. Lý thuyết đã có sẵn thành 8 bài tự học (`cnc_lessons`), nên dồn nó về nhà, giờ lớp dành cho máy.
- Bằng chứng (nhớ từ tài liệu, chưa tra lại): tổng hợp của Strelan và cộng sự (2020) cho hiệu ứng nhỏ–vừa (~0,35); hiệu quả hơn khi có quiz trước giờ học và hoạt động chủ động tại lớp. Retrieval practice (Roediger & Karpicke) và tải nhận thức (Sweller, Mayer — đã có ở `docs/QUY-TAC-THIET-KE.md`) là cơ sở chọn quiz thấp rủi ro + bài tự học ngắn.
- Rủi ro đã biết: sinh viên không chuẩn bị ở nhà thì buổi lớp sụp. Cách chặn: **cổng an toàn** (quiz ≥4/5 mới đứng máy, làm lại không trừ điểm) và 10 phút đầu giờ chữa đúng câu nhiều bạn sai.

## Nhịp một buổi (mọi bài giống nhau)
| Giai đoạn | Thời lượng | Nội dung |
|---|---|---|
| A. Ở nhà | ≤ 25 phút | đọc/xem **2 mục** của bài, quiz 5 câu, gửi 1 câu "chỗ em chưa rõ" trước ≥12 giờ |
| B. Tại lớp | 135 phút | 10' chữa chỗ sai · nhóm 3 người, chia vai · 2 nhiệm vụ trên máy · thử thách · phiếu thoát lớp |
| C. Sau giờ | ≤ 15 phút | Trả bài 3 câu bằng lời, tự đánh dấu năng lực |

Quy tắc chung: quiz đặt cuối phần A chỉ để chẩn đoán, **không tính điểm** (SDT: ít áp lực, dám sai); điểm lấy từ thao tác trên máy và checklist năng lực sẵn có (`cnc_competency_permissions`). Cách tính điểm theo công bố của giảng viên.

## Bản đồ 8 bài hiện có → nhiệm vụ trên máy
| Bài | Phần A (ở nhà) | Việc chính tại lớp |
|---|---|---|
| Mở đầu: an toàn, 5S | quy tắc trước khi bật máy | đi vòng xưởng tìm 6 điểm nguy hiểm, dừng khẩn thật |
| 1 Giới thiệu, trục, điểm chuẩn | II.5, II.6 | tìm M, R; đặt W (**bản mẫu**) |
| 2 Lập trình tiện | G00/G01, tọa độ tuyệt đối/tương đối | viết và mô phỏng chương trình trục bậc |
| 3 Lập trình phay | G00/G01/G02/G03, bù dao | viết và mô phỏng contour tấm phôi |
| 4 Vận hành tiện | quy trình nhận máy | gá phôi, gá dao, đo dao, chạy không tải |
| 5 Vận hành phay | quy trình nhận máy | tương tự trên phay, đặt W bằng đầu dò/dao chạm |
| 6 Gia công tiện | đọc bản vẽ trục bậc | cắt chi tiết thật, đo, ghi sai lệch |
| 7 Gia công phay | đọc bản vẽ tấm đế | cắt chi tiết thật, đo, ghi sai lệch |

Đề xuất bổ sung sau khi thầy duyệt khung: bài 8 "Sửa lỗi chương trình và cảnh báo máy", bài 9 "Chọn chế độ cắt (S, F) và tuổi bền dao", bài 10 "Dự án nhóm" (từ bản vẽ đến chi tiết).

## Việc cần thầy quyết
1. Khung 3 giai đoạn, thời lượng buổi 135 phút có đúng lịch của lớp không.
2. Cổng 4/5 trước khi vào xưởng: bắt buộc hay chỉ khuyến khích.
3. Video: thầy tự quay (6–8 phút/bài) hay chỉ dùng bài đọc có sẵn. Bản mẫu mới dùng bài đọc, chưa có video.
4. Có bật trên web `/lop-hoc/cnc/` không: bài mẫu sẽ thành một mục mới hoặc thay phần mở đầu của `lesson-1` (mục ghi DB do thầy duyệt).

## Chưa làm / chưa kiểm
- Chưa ghi DB, chưa hiện cho sinh viên; chỉ có bản xem thử `content/lesson-samples/cnc-flipped-bai-1/xem-thu/xem-thu.html`.
- Chưa có chỗ để sinh viên gửi "câu chưa rõ" trên web (hiện nhờ nhóm lớp); chưa thử với sinh viên thật.
