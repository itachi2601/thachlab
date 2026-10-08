---
name: project-thachlab-anthropic-credit
description: Credit khuyến mãi $100 Anthropic API hết hạn 22/10/2026 — chỉ dùng được qua API/Batch/Agent SDK, KHÔNG dùng cho Claude Code; script batch-ra-soat-bai.mts để đốt credit vào việc có ích
metadata:
  type: project
---

Thầy được cấp **$100 credit khuyến mãi Anthropic** (ghi nhận 8/10/2026), **hết hạn 22/10/2026**, không chuyển kỳ sau.
"Applies to": Agent SDK, API, Batch API, Playground, Managed Agents. **Không** áp dụng cho Claude Code
(Claude Code báo "balance too low" vì số dư mua = $0). Claude Code chạy bằng gói claude.ai (`/login`), không nạp tiền.

**Cách tận dụng (đã xây 8/10/2026):** `scripts/batch-ra-soat-bai.mts` — Batch API (giá ½), Claude đọc mục lý thuyết
của từng bài như "lượt Claude" (bước 1b skill `cap-nhat-bai-hoc-theo-gemini`), trả JSON góp ý + bẫy quiz chưa nhấn.
Chế độ 2 (`--che-do bai-tap-mau`): nháp đúng 4 dạng bài tập mẫu bắc cầu 4 cấp bám lý thuyết + YCCĐ (prompt của skill
`soan-bai-tap-mau`), tự chạy `kiem-ban-nhap-gemini.py`, báo cáo `BAO-CAO-BAI-TAP-MAU.md`; vẫn phải viết lại trước khi đăng.
Chế độ: `--du-toan` (đếm token, không tốn tiền) → `--gui` → `--nhan --cho` → `BAO-CAO.md` xếp bài cần sửa.
Kết quả: `scripts/logs/batch-ra-soat/ket-qua/<lesson_id>.json`; bài có thư mục trong `content/gemini/hang-doi.md`
thì ghi thêm `gemini/nhan/hoc-sinh-trung-binh-claude.json` để `/gemini-nhan` xử lý tiếp. Ước ~$0.05–0.10/bài Opus 5.5
→ cả ~116 bài ≈ $6–12; còn dư thì chạy thêm vai `yeu`/`kha` hoặc đổi `--effort xhigh`.

Việc khác credit áp dụng được: phân loại/mức độ câu hỏi ngân hàng bằng Haiku 5.5 (script backfill hiện dùng DeepSeek),
`eval-ai-tutor.mts --providers anthropic`. Agent SDK chưa thử (chưa rõ CLI dùng API key có tính là Agent SDK không).

**Why:** credit sắp hết hạn, chi phí Claude Code (subscription) không giảm nếu không dùng API.
**How to apply:** trước 22/10 nhắc thầy chạy batch; sau ngày đó script vẫn dùng được nhưng tính tiền thật. Xem [[project-thachlab-cap-nhat-bai-theo-gemini]].
