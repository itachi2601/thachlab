---
name: project_thachlab_ra_soat_l10_l11_con_lai
description: Rà soát + vẽ lại hình 20 bài L10/L11 còn lại (31/10/2026) — đã commit repo, CHƯA đăng DB; danh sách bài, việc treo thầy chốt
metadata:
  type: project
---

Skill `ra-soat-bai-hoc`, 31/10/2026, 20 bài: L10 B1, B2, B3, B13–B22; L11 B1, B16–B21. Cộng với các đợt trước (L10 Ch.2, 4, 5–7; L11 Ch.1 B2–7, Ch.2, Ch.4) thì lý thuyết L10/L11 đã rà hết hình. Liên quan [[project_thachlab_ra_soat_ch2_l11]], [[project_thachlab_l10_ly_thuyet_ch4]].

**Trạng thái:** commit nhánh `claude/bai-hoc-lop-10-11-46760c` (đã push). ĐÃ GHI DB 31/10/2026 ~08:00 theo lệnh thầy 'đăng luôn' (20/20 bài, chỉ mục lý thuyết, sao lưu `scripts/logs/ly-thuyet-bai{id}-backup-*.json`). CHƯA deploy (bản tĩnh /data/lessons/46.json, 20.json còn cũ) — classifier chặn `bash scripts/deploy.sh` trong tab terminal, thầy tự chạy.
lesson_id: L10 B1–3 = 46,47,48; B13–22 = 58–67; L11 B1 = 20, B16–21 = 35–40.

**Thầy cần chốt:**
- L11 B1: quiz đảo thứ tự phương án (đáp án đúng A, D, B, C) — đăng bằng cap-nhat-ly-thuyet.sh.
- L10 B20: `theory.html` HEAD cũ lệch `theory.src.html` (video đặt sai chỗ); bản mới theo nguồn, video đứng sau hộp thí nghiệm.
- L10 B1: hai hộp video mực liền nhau (dòng 51–63), "chữ rộng 40 nm" ảnh STM chưa kiểm nguồn.
- L11 B21 caption Hình 3 "Hình vẽ 3 tụ." cụt; L11 B17 caption Hình 3 "không phải 1,69"; L11 B1 Hình 3 thiếu nhãn M, Q mà văn nhắc.
- L10 B18 fig-4: dời nhãn F_msn sang phải ~6 px (góp ý kiem-code, chưa làm).
- Dòng 🔑/Trả bài/Mang về nối ý bằng " · " ở hầu hết bài (lint) — chưa tách, văn có sẵn.
- Bản sửa chỉ số cuối của L10 B15, 17, 19, 20, 21, 13 chưa soát độc lập vòng 3.
