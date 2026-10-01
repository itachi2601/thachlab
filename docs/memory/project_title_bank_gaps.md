---
name: project-title-bank-gaps
description: 5 danh hiệu rank còn thiếu câu hỏi (66 câu) — dữ liệu để soạn ngay khi có token
metadata:
  node_type: memory
  type: project
  originSessionId: 756e3cd6-d577-481e-aa04-81ca78df1a60
  modified: 2026-09-30T10:25:47.778Z
---

Đo 30/9/2026: ngưỡng mỗi danh hiệu dễ 12 / TB 8 / khó 5. Còn thiếu: phap_su_thau_kinh (12/8/5), vu_cong_quy_dao (12/8/5), ke_pha_the_can_bang (2/4/4), chien_than_newton (0/0/3), tho_san_tan_so (0/0/3). Bảng đầy đủ: `docs/title-bank-gaps-2026-09-30.md`.

**Why:** thầy dặn ghi lại để dùng cho skill tạo câu hỏi ngay khi có token.
**How to apply:** khi thầy nói soạn câu cho danh hiệu / hết hạn token, mở file docs trên, soạn đúng số thiếu, rồi chạy lại `scripts/sql/title-bank-coverage.sql`. Liên quan [[feedback_batch_agent_upload_efficiency]].
