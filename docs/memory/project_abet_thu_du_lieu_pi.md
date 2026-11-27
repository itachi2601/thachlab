---
name: project_abet_thu_du_lieu_pi
description: Module ABET trên thachlab (link nộp điểm câu PI cho chủ PI + /quan-tri/abet); chặng 1 đã chạy DB 27/11/2026, chưa deploy
metadata:
  type: project
---

Thầy Thạch điều phối ABET ngành CĐ CNKT Cơ khí (Cao Thắng). Hồ sơ gốc: `~/Documents/CTTC/3 - ABET và Kiểm định/Hồ sơ gốc ABET MET/0-ABET MET/` (01 Assessment Plan … 04 Evaluation; `02. SO Attainment Data/<năm>/<SO>/<PI>/du-lieu|de-dap-an|bai-mau`). File Excel theo dõi cũ: `02…/_Mau/ABET-MET-theo-doi (…).xlsx`. Chu kì: 2025-2026 đo SO1, SO2, SO4; 2026-2027 đo SO3, SO5.

Chặng 1 (27/11/2026): migration `20261127200000_abet_thu_du_lieu_pi` ĐÃ CHẠY. Có bảng `abet_sources/scores/files/history`, RPC `abet_nop_*` theo token, bucket riêng tư `abet-minh-chung`. Seed 23 dòng kế hoạch PI, tất cả đang "Chưa gửi", cột chủ PI còn trống. Trang `/abet/nop/?ma=<token>` (giáo viên không cần tài khoản) và `/quan-tri/abet` (chỉ admin) — **chưa deploy**. Đã thử nộp điểm + tải tệp bằng khách trên dòng thử `TEST-xoa` rồi xoá dòng; còn 1 ảnh thử 40px mồ côi trong bucket (thư mục `thuabet27112026xoasau/`), xoá qua Storage UI.

**Why:** thu điểm từng câu PI từ nhiều giáo viên bằng Zalo + Excel rất chậm, và % đạt phải tính tay.

**How to apply:** việc tiếp theo là deploy, điền chủ PI, rồi bấm "Tin nhắn" ở từng dòng để gửi Zalo. Góp ý đã nêu với thầy: rút còn 1 nguồn/PI; 1.3a, 1.4b, 1.2c, 5.2b đang lấy điểm cả bài chứ không phải tiêu chí PI; nên dời hạn HK1 30/11 sang 15/12. Chặng 2: xuất zip đúng cây thư mục + báo cáo SO. Chặng 3: gắn PI vào rubric/câu hỏi thachlab (`rubric_exam_attempts.item_levels`) để tự lấy điểm.
