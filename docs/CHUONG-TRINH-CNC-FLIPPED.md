# Chương trình CNC theo lớp đảo ngược (flipped) — đề xuất 18/10/2026

Đối tượng: sinh viên CĐ đã học tiện, phay cơ bản (máy vạn năng). Bản mẫu buổi 1: `content/lesson-samples/cnc-flipped-buoi-1/` (đã ghi DB, `cnc_lessons.id = flip-1`).
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
| B3. Thực hành | 85 + 85 phút | Lượt 1 và Lượt 2 đổi trạm (máy thật ↔ WinNC); mỗi lượt: Nhiệm vụ 1 · Nhiệm vụ 2 · Thử thách; nghỉ 10 phút giữa hai lượt |
| B4. Kết buổi | 30 phút | phiếu nhóm và phiếu thoát lớp 20 phút, dọn máy 5S và bàn giao 10 phút |
| C. Sau buổi | ≤ 10 phút | Trả bài 3 câu bằng lời, tự đánh dấu năng lực |

Tổng B = 300 phút. Bài nặng lý thuyết (lập trình) kéo B2 lên 90 phút thì bớt Thử thách.
Quy tắc chung: quiz chỉ để chẩn đoán, **không tính điểm** (SDT: ít áp lực, dám sai); điểm lấy từ thao tác trên máy và checklist năng lực sẵn có (`cnc_competency_permissions`). Cách tính điểm theo công bố của giảng viên. Tiện và phay xen kẽ nhau để nhớ lâu hơn.
Lớp ~30 em, 6 máy, xưởng có **WinNC 3D View** (giả định mỗi em một máy tính, cần thầy xác nhận số máy tính): chia lớp hai nửa 15 em, **một nửa máy thật (2–3 em/máy), một nửa WinNC**, giữa phần thực hành đổi trạm. Mỗi em được ~35–40 phút bấm máy thật và ~85 phút trên WinNC; thử sai (va chạm) làm trên WinNC. Lập trình: viết xong chạy WinNC 3D trước, rồi mới ra máy thật.

## Phân bố 12 buổi (2 tuần) — bám đúng 7 bài hiện có (70 tiết)
Thứ tự theo chương trình của thầy: nhập môn → lập trình tiện → lập trình phay → vận hành tiện/phay → gia công tiện/phay → dự án. Nhập môn gom nội quy, máy, điểm chuẩn, hệ điều khiển WinNC FANUC, lệnh cơ bản và chương trình đầu tiên (bản cũ của tôi xếp "Bài 1 điểm chuẩn" thành một buổi riêng và đảo thứ tự, không đúng thực tế dạy).

| Buổi | Chủ đề (bài trên web) | Tối trước (A) | Giảng viên dạy (~1–2 giờ) | Thực hành (hai trạm) |
|---|---|---|---|---|
| 1 | Nhập môn: Mở đầu + Bài 1 + nhập môn lệnh (**bản mẫu, đã đăng**) | không có (buổi đầu) | nội quy, an toàn, máy, M-W-R, WinNC, lệnh, chương trình đầu tiên | máy thật: nhận máy, Reference, JOG, MDI · WinNC: nhập và chạy O0001 |
| 2 | Lập trình tiện (1): Bài 2 mục 1–3 | đọc mục 2–3, quiz | cấu trúc chương trình 21T, G18/G71/G95, G00/G01, G90/G91, X-Z và U-W | viết, chạy WinNC trục bậc đơn giản; máy thật chạy từng khối, không phôi |
| 3 | Lập trình tiện (2): Bài 2 mục 4–6 + bài toán mẫu | mục 4–6 | bù bán kính mũi dao, chu trình tiện và khoan, mã M | tiện tinh trục bậc trên WinNC, sửa lỗi cú pháp |
| 4 | Lập trình phay (1): Bài 3 mục 1–3 | mục 1–3 | điểm chuẩn phay, cấu trúc 21M, G17, dịch chuyển | rãnh, bậc trên WinNC |
| 5 | Lập trình phay (2): Bài 3 mục 4–7 + bài toán mẫu | mục 4–7 | bù bán kính và chiều dài, G81/G83/G73, tarô, doa, mã M | contour và 4 lỗ trên WinNC |
| 6 | Vận hành tiện: Bài 4 (EMCO TURN 55) | mục 1–4 | kiểm máy, Reference, JOG, MDI, gá, W, Geometry Offset | máy thật: gá, đặt W, đo dao · WinNC: nhập offset, chạy |
| 7 | Vận hành phay: Bài 5 (MILL 55) | mục 1–4 | tương tự phay, dò cạnh, chiều dài và bán kính dao | như buổi 6 trên phay |
| 8 | Gia công tiện (1): Bài 6 mục 1–3 | mục 1–3 | mặt đầu, trụ, bậc, vát, bo, thứ tự nguyên công | cắt chi tiết thật; WinNC kiểm trước |
| 9 | Gia công tiện (2): Bài 6 mục 4–5 + mẫu | mục 4–5 | côn, ren, năm bước giải bài tổng hợp | cắt trục có côn và bo cung, đo, ghi sai lệch |
| 10 | Gia công phay (1): Bài 7 mục 1–2 | mục 1–2 | phay phẳng, bậc, cong, cung | cắt chi tiết thật; WinNC kiểm trước |
| 11 | Gia công phay (2): Bài 7 mục 3–5 + mẫu | mục 3–5 | profile, khoan, tarô, sắp thứ tự nguyên công | cắt tấm đế bốn lỗ ren, đo, ghi sai lệch |
| 12 | *Mới (duy nhất cần soạn)* Dự án nhóm + kiểm tra thực hành | đề dự án | chữa lỗi thường gặp 30 phút | từ bản vẽ đến chi tiết, chấm theo checklist |

- Buổi 2–5: máy thật dùng để chạy **từng khối, không phôi**; vào cắt thật chỉ từ buổi 6 vì cần biết đặt W và offset.
- Cả 12 buổi dùng đúng 11 bài đã có (Bài 1–7 chia đôi ở bài dài), chỉ buổi 12 là bài mới. Bản cũ "4 bài mới" bỏ.
- Chưa rà từng mục con của Bài 4–7 xem đã đủ cho buổi 6–11; mỗi buổi soạn trang flipped riêng theo mẫu buổi 1.

## Việc cần thầy quyết
1. Bảng 12 buổi ở trên có khớp lịch thầy đang dạy không (thứ tự, chỗ chia đôi Bài 2, 3, 6, 7).
2. Cổng 4/5 trước khi vào xưởng từ buổi 2: bắt buộc hay chỉ khuyến khích.
3. Số máy tính WinNC (đang giả định mỗi em một máy).
4. Video: thầy tự quay hay chỉ dùng bài đọc có sẵn (mẫu mới dùng bài đọc).

## Chưa làm / chưa kiểm
- Buổi 1 đã ghi `cnc_lessons` (flip-1); buổi 2–12 chưa soạn trang flipped.
- Chương trình O0001 chưa chạy thử trên WinNC FANUC 21T thật của xưởng; cú pháp (nhất là `T0202 M6;`, `M5;`, F giữ hiệu lực ở khối sau) cần thầy chạy thử trước khi dùng.
- Chưa có chỗ để sinh viên gửi "câu chưa rõ" trên web (hiện nhờ nhóm lớp); chưa thử với sinh viên thật.
