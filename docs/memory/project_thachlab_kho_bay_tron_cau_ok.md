---
name: thachlab-kho-bay-tron-cau-ok
description: Kho bẫy câu sai (ôn cách quãng) — lượt ôn trộn câu bẫy với câu đã làm đúng, tỉ lệ thích ứng; đã chạy + deploy 11/10/2026
metadata:
  type: project
---

Kho bẫy: bảng `student_mistakes` (221 câu / 26 HS lúc 11/10), thẻ `MistakeVaultCard` ở `/luyen-tap`, modal `MistakeReviewModal`.
Migration `20261011150000` (kho bẫy) và `20261011190000_mistake_review_mix_ok` (trộn câu ok) đã chạy 11/10.

**Quy tắc trộn (thầy duyệt 11/10):** tỉ lệ bẫy mặc định 0,6 (config mùa `mistake_review_trap_share`); lượt trước đúng <50% hoặc >15 bẫy tồn → 0,4; hai lượt liền >80% → 0,7. Câu đầu và cuối luôn là câu ok. Câu ok lấy từ câu từng làm đúng (ưu tiên ≥3 ngày), không cộng RP, không đổi lịch ôn; làm sai thì thành bẫy mới. Cơ sở: Wilson 2019 (vùng ~85% đúng), peak-end (Kahneman), Roediger & Karpicke.

**Why:** lượt toàn câu sai kéo tỉ lệ đúng ~60% → dễ nản. **How to apply:** đổi tỉ lệ bằng config mùa, không sửa code.

Còn treo: quy tắc "sai 2 câu liền thì chèn câu ok" chưa làm (nộp cả lượt một lần); chưa thử UI bằng HS thật; câu sai mới chỉ đến hạn sau 2 ngày nên thẻ ban đầu hiện "chưa đến hạn". Liên quan [[project_thachlab_daily_streak]].
