# Chương trình CNC theo lớp đảo ngược (flipped) — đề xuất 18/10/2026

Đối tượng: sinh viên CĐ đã học tiện, phay cơ bản (máy vạn năng). Bản mẫu: `content/lesson-samples/cnc-flipped-bai-1/` (chưa ghi DB).
Lịch (thầy nói 18/10/2026): **buổi 5 tiếng (300 phút), giảng viên dạy lý thuyết 1–2 giờ đầu buổi, 6 buổi/tuần, học liên tục 2 tuần = 12 buổi** (60 giờ). Bản trước ghi nhầm 180 phút, đã sửa.

## Vì sao đảo ngược cho môn này
- Môn thực hành: giờ ở xưởng quý hơn giờ ngồi nghe. Lý thuyết đã có sẵn thành 8 bài tự học (`cnc_lessons`), nên dồn nó về nhà, giờ lớp dành cho máy.
- Bằng chứng (nhớ từ tài liệu, chưa tra lại): tổng hợp của Strelan và cộng sự (2020) cho hiệu ứng nhỏ–vừa (~0,35); hiệu quả hơn khi có quiz trước giờ học và hoạt động chủ động tại lớp. Retrieval practice (Roediger & Karpicke) và tải nhận thức (Sweller, Mayer — đã có ở `docs/QUY-TAC-THIET-KE.md`) là cơ sở chọn quiz thấp rủi ro + bài tự học ngắn.
- Rủi ro đã biết: sinh viên không chuẩn bị ở nhà thì buổi lớp sụp. Cách chặn: **cổng an toàn** (quiz ≥4/5 mới đứng máy, làm lại không trừ điểm) và 10 phút đầu giờ chữa đúng câu nhiều bạn sai.

## Nhịp một buổi 300 phút (mọi bài giống nhau)
Học liền mỗi ngày nên "ở nhà" là **tối hôm trước, ≤ 20 phút**, không giao bài dài. Phần lý thuyết **giảng viên dạy ngay trên máy, khoảng 60 phút (tối đa 90)**, chia khối ≤20 phút có hỏi đáp theo cặp 2 phút (tải nhận thức, retrieval practice); dạy liền 2 giờ thì giữa chừng phải có nghỉ. Ngồi máy cả buổi dễ mệt: nghỉ 15 phút sau phần dạy và 10 phút giữa phần thực hành.

| Giai đoạn | Thời lượng | Nội dung |
|---|---|---|
| A. Tối hôm trước | ≤ 20 phút | đọc/xem **2 mục** của bài, quiz 5 câu, gửi 1 câu "chỗ em chưa rõ" trước 21 giờ |
| B1. Mở buổi | 15 phút | quiz nhanh, chữa chỗ sai (em chưa đạt 4/5 làm lại ở đây) |
| B2. Giảng viên dạy | 60 phút (đến 90 nếu bài nặng) | 3 khối ≤20 phút trên máy thật, mỗi khối 2 phút hỏi đáp cặp |
| nghỉ | 15 phút | rời máy |
| B3. Thực hành | 55 + 70 + 55 phút | Nhiệm vụ 1 · Nhiệm vụ 2 (đổi vai) · Thử thách, nghỉ 10 phút giữa chừng |
| B4. Kết buổi | 20 phút | phiếu thoát lớp 10 phút, dọn máy 5S và bàn giao 10 phút |
| C. Sau buổi | ≤ 10 phút | Trả bài 3 câu bằng lời, tự đánh dấu năng lực |

Tổng B = 300 phút. Bài nặng lý thuyết (lập trình) kéo B2 lên 90 phút thì bớt Thử thách.
Quy tắc chung: quiz chỉ để chẩn đoán, **không tính điểm** (SDT: ít áp lực, dám sai); điểm lấy từ thao tác trên máy và checklist năng lực sẵn có (`cnc_competency_permissions`). Cách tính điểm theo công bố của giảng viên. Tiện và phay xen kẽ nhau để nhớ lâu hơn.
Lớp ~30 em, 6 máy: **nhóm 5 người một máy, 5 vai xoay mỗi lượt** (vận hành, an toàn, đọc số, ghi, kiểm). Thực hành 3 giờ chia 5 lượt ~12 phút cho mỗi em tự bấm máy ở nhiệm vụ chính; em khác giữ vai, vẫn có việc. Nếu xưởng có phần mềm mô phỏng CNC thì thêm trạm mô phỏng cho nửa lớp để tăng giờ chạm tay (chờ thầy cho biết).

## Phân bố 12 buổi (2 tuần)
Tám bài hiện có chỉ phủ 8 buổi; 4 buổi còn lại cần bài mới (đánh dấu *mới*, chưa soạn).

| Buổi | Chủ đề | Phần A tối trước | Việc chính tại lớp |
|---|---|---|---|
| 1 | An toàn, 5S (bài Mở đầu) | quy tắc trước khi bật máy | đi vòng xưởng tìm điểm nguy hiểm, dừng khẩn thật |
| 2 | Bài 1: trục, điểm chuẩn (**bản mẫu**) | II.5, II.6 | tìm M, R; đặt W trên tiện và phay |
| 3 | Bài 4: vận hành tiện | quy trình nhận máy | gá phôi, gá dao, đo dao, chạy không tải |
| 4 | Bài 5: vận hành phay | quy trình nhận máy | đặt W bằng dao chạm, đo dao, chạy không tải |
| 5 | Bài 2: lập trình tiện (1) | G00/G01, tuyệt đối/tương đối | viết, mô phỏng, chạy trục bậc đơn giản |
| 6 | Bài 3: lập trình phay (1) | G00/G01, mặt phẳng, bù chiều dài | viết, mô phỏng, chạy rãnh và bậc |
| 7 | *Mới* Lập trình tiện (2) | G02/G03, côn, chu trình thô | trục có côn và bo cung |
| 8 | *Mới* Lập trình phay (2) | G02/G03, bù bán kính, chu trình khoan | contour và 4 lỗ |
| 9 | Bài 6: gia công tiện | bản vẽ trục bậc | cắt chi tiết thật, đo, ghi sai lệch |
| 10 | Bài 7: gia công phay | bản vẽ tấm đế | cắt chi tiết thật, đo, ghi sai lệch |
| 11 | *Mới* Sửa lỗi, chế độ cắt (S, F), tuổi bền dao | ca lỗi mẫu | sửa chương trình lỗi, so chi tiết trước/sau |
| 12 | *Mới* Dự án nhóm + kiểm tra thực hành | đề bài dự án | từ bản vẽ đến chi tiết, chấm theo checklist |

Thứ tự bài 4, 5 trước bài 2, 3: sinh viên đã chạm máy trước khi viết lệnh, nên lập trình có chỗ gắn. Nếu thầy muốn lập trình trước thì đảo buổi 3–4 với 5–6, bài mẫu không đổi.

## Việc cần thầy quyết
1. Thứ tự 12 buổi ở trên, nhất là bài vận hành (3–4) đặt trước lập trình (5–6).
2. Cổng 4/5 trước khi vào xưởng: bắt buộc hay chỉ khuyến khích.
3. Video: thầy tự quay (6–8 phút/bài) hay chỉ dùng bài đọc có sẵn. Bản mẫu mới dùng bài đọc, chưa có video.
4. Có bật trên web `/lop-hoc/cnc/` không: bài mẫu sẽ thành một mục mới hoặc thay phần mở đầu của `lesson-1` (mục ghi DB do thầy duyệt).

## Chưa làm / chưa kiểm
- Chưa ghi DB, chưa hiện cho sinh viên; chỉ có bản xem thử `content/lesson-samples/cnc-flipped-bai-1/xem-thu/xem-thu.html`.
- Chưa có chỗ để sinh viên gửi "câu chưa rõ" trên web (hiện nhờ nhóm lớp); chưa thử với sinh viên thật.
