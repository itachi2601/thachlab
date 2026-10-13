# Bốc và xếp câu khi tự luyện (13/10/2026)

Mã nguồn duy nhất: `features/lessons/practice-arrange.ts` (`pickByMix`, `arrangeForMotivation`, `pickAndArrange`). Kiểm: `npx tsx scripts/test-practice-arrange.mts`.

**Vấn đề cũ**: bốc ngẫu nhiên thuần rồi trộn (PracticeSession, ôn tổng hợp, bài tương tự, bài cuối buổi) → em yếu có thể gặp 3 câu khó liền ở vị trí bất kỳ, và câu cuối thường là câu khó.

**Tỉ lệ** (dễ/TB/khó): em yếu hoặc phụ đạo đúng chỗ hổng 50/40/10; mặc định 30/50/20; em khá 20/50/30. Mục tiêu đúng ≈ 70–80% (Wilson 2019 "85% rule"; Vygotsky ZPD; Bjork: khó có lợi chỉ khi em còn thành công được).

**Thứ tự**: 2 câu dễ mở đầu (Bandura – thành công sớm tạo hiệu năng bản thân; goal-gradient Kivetz 2006); câu nhẹ tăng dần, câu khó rải về phía cuối (đỉnh ~70% bộ), không dồn ≥3 câu khó liền; câu cuối vừa sức (peak–end, Kahneman 1993 – ký ức về cả lượt do đỉnh và cuối quyết định, quyết định em có quay lại không).

**Áp dụng**: `TopicPracticeModal` (phụ đạo một phần, ôn tổng hợp, luyện cả bài), `PracticeSession` (có/không thang mức), `TutoringExitQuiz` (cuối buổi + tự kiểm), `SimilarBankPractice`. Không đổi: thi thăng hạng thích ứng (`rank_gate_*`) và kho bẫy trộn câu ok (`mistake_review`) — đã có thiết kế riêng.

**Chưa làm (bước sau, cần dữ liệu)**: hạ độ khó ngay trong lượt khi sai 2 câu liền; chọn `band` theo tỉ lệ đúng 10 phiên gần nhất của chủ đề thay vì mặc định. **Cách đo**: tỉ lệ bỏ giữa chừng và số phiên/tuần của nhóm 25% dưới, trước/sau.
