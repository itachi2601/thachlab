---
name: project-thachlab-vat-ly-quanh-ta-the
description: Thẻ "Vật lý quanh ta" có hook + câu đố tại chỗ + khung ảnh; chờ Gemini tìm ảnh thật theo docs/ANH-VAT-LY-QUANH-TA.md
metadata:
  type: project
---

Từ 14/10/2026 thẻ bài ở trang chủ (dải, câu đố gập sau nút) và `/blog` (lưới, mở sẵn) dùng `PhysicsCuriosityCard`: nhãn tò mò (`badge`), câu hook (`hook`), câu đố A/B/C (`quiz`) lấy từ front-matter 8 bài, khung ảnh 16:9 (ảnh thật `photo` hoặc khung "?").
Ảnh không có đủ ghi công (`photoCredit`) thì không hiện. Quy tắc + brief 8 bài + định dạng JSON Gemini trả: `docs/ANH-VAT-LY-QUANH-TA.md`; kiểm: `npx tsx scripts/kiem-anh-vat-ly-quanh-ta.mts`.

**Why:** nhận xét 14/10 — thẻ chỉ chữ, sự kịch tính "đoán thử" bị giấu trong bài. Thầy giao Gemini tìm ảnh; Claude đối chiếu giấy phép từng link rồi nạp.
**How to apply:** bài "Vật lý quanh ta" mới phải có `badge`/`hook`/`quiz` (script kiểm báo lỗi nếu thiếu). Chưa deploy, chưa thử máy thật, chưa đo lượt bấm.
