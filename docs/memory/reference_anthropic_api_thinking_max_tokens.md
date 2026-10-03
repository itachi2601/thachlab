---
name: reference_anthropic_api_thinking_max_tokens
description: "Script gọi Claude API (Sonnet 5.5 / Opus 5.5): token SUY NGHĨ tính vào max_tokens — để 4096 là câu khó bị cắt trước JSON (stop_reason=max_tokens, text rỗng); để ≥16000 + output_config.effort low cho việc ngắn"
metadata:
  type: reference
---

3/10/2026, `scripts/backfill-distractor-notes.mts`: lượt vét thất bại gần 100% dù JSON repair đã có. Log cho thấy
`stop_reason=max_tokens`, văn bản dài 0 ký tự → suy nghĩ thích ứng (luôn bật trên claude-sonnet-5-5, không tắt được
bằng `type:"disabled"`) tiêu hết 4096 token với câu khó. Sửa: `max_tokens: 16000`, `output_config: { effort: "low" }`
→ 16/16 câu khó qua. Luôn log `stop_reason` + `stop_details` và lưu phản hồi hỏng ra file khi parse lỗi (thấy nguyên
nhân ngay, không đoán). Chi tiết tham số theo skill `claude-api` (model mới: không `budget_tokens`, không prefill).
Áp dụng cho mọi script backfill tương tự ([[project_thachlab_rank_gate_adaptive]], backfill mức độ câu hỏi).
