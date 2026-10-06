---
name: project_thachlab_ai_tutor
description: "AI Tutor Socratic (roadmap GĐ 4, Q2–Q3/2027) — 6/10/2026 đã chốt kiến trúc không phụ thuộc model (docs/AI-TUTOR.md) + script eval offline; chưa xây tutor, chưa chọn model"
metadata:
  node_type: memory
  type: project
  originSessionId: ec6225ef-64de-4d7a-8267-a3da9b524031
  modified: 2026-10-06T02:22:31.871Z
---

**Trạng thái 6/10/2026:** thầy nhận một bản phân tích giá API (DeepSeek/Claude/GPT) + một bản phản biện; tôi phản biện lại
rồi thầy chốt làm 2 việc: (2) `docs/AI-TUTOR.md` ghi quyết định không mục theo bảng giá, (3) `scripts/eval-ai-tutor.mts`
eval offline. Cả hai đã commit vào `main`. KHÔNG viết Edge Function `ai-tutor` bây giờ (roadmap 6–9 tháng nữa, code sẽ mục).

**Kết luận đã kiểm (trang chính thức, 6/10/2026):**
- Chi phí API cho 200 HS × 20 tin nhắn/tháng chỉ $2–$80/tháng → không phải nút thắt; chất lượng gợi ý mới là.
- DeepSeek peak = 01–04h & 06–10h UTC T2–T6 (8–11h, 13–17h VN); kênh phụ đạo buổi chiều rơi đúng peak. deepseek-flash mặc định bật thinking.
- Anthropic: cache theo workspace (không theo HS); ngưỡng cache Haiku 4.5 = 4.096 token, dòng 5.5 = 512; dòng 5.5 không tắt thinking được (Opus) / chỉ `between_tools` (Sonnet).
- Hệ số chi phí lớn nhất là số lượt/hội thoại (lịch sử cộng dồn), lớn hơn thinking. Doc chốt tối đa 8 lượt/hội thoại.

**Eval offline:** `npx tsx scripts/eval-ai-tutor.mts --n 30 --providers deepseek,openai,anthropic` → phiếu chấm mù
`scripts/logs/eval-ai-tutor-<stamp>-phieu-cham.md` (3 tiêu chí: không lộ · đúng VL · trúng chỗ sai) + khoá nhãn + JSON usage.
Thử 2 câu DeepSeek: 616 vào/142 ra, $0,34/1.000 gợi ý peak. `.env.local` mới có DEEPSEEK_API_KEY — muốn so 3 model thầy
phải thêm OPENAI_API_KEY / ANTHROPIC_API_KEY.

**Phát hiện dữ liệu:** `exam_question_results.is_correct` có dòng lệch với đề hiện tại (đề sửa đáp án sau khi HS làm); script
chấm lại bằng `gradeQuestion`. `tutoring_needs` cũng đọc cột này — chưa rà.

**Treo:** thầy chạy eval 30 câu + chấm; thêm key provider; rà `is_correct` lệch. Liên quan: [[project_thachlab_phu_dao]],
[[reference_anthropic_api_thinking_max_tokens]].
