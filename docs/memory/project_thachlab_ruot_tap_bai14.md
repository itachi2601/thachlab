---
name: project-thachlab-ruot-tap-bai14
description: Ruột tập in 12 trang cho Bài 14 VL12 (script dựng PDF trong repo) xếp theo nhịp buổi L12 + quy ước thiết kế thầy chốt 25/10; data-tap nối web với tập; chờ in thử, cập nhật DB, deploy
metadata:
  type: project
---

Dựng: `node scripts/ruot-tap/bai14.mjs` (+ module `bai14-btm.mjs` cho 2 trang Bài tập mẫu) → `scripts/ruot-tap/out/ruot-tap-vl12-bai14.pdf`; script in "trang N: dư X mm" để cân trang trước khi nhìn ảnh; QR kiểm bằng `npx tsx scripts/ruot-tap/giai-ma-qr.mts <png>`. Font Noto Sans trong `scripts/ruot-tap/fonts/` (phải có unicode-range, nếu không chữ đậm rơi về Helvetica). Mã ô "Tập: trang · ô" = `data-tap` trong `theory.src.html` (chỉ mục lý thuyết trang 1–5; Bài tập mẫu trên web KHÔNG gắn data-tap).

**Bố cục 12 trang (bản 2026-10-25, main 61d2a6d00):** 1–5 học bài mới trên lớp 60′ (trang 1 có dải nhịp buổi; trang 3 = Ôn 10′ đầu buổi sau, trả bài có ☐ nói được + bạn cùng bàn kiểm; trang 5 = ô Đề BTVN + mang về + thử thách + PhET) · 6–7 Bài tập mẫu 5 dạng bán cấu trúc · 8 Sửa bài trên lớp 30′ · 9 Sửa bài kiểm tra chương · 10 Làm lại câu sai sau 1 tuần · 11–12 ghi chú tự do.

**Quy ước thầy chốt 2026-10-25 (áp cho mọi ruột tập/sách in sau):**
- Nhịp buổi L12 (2 h): 10′ ôn → 20′ kiểm tra → 30′ sửa bài → 60′ bài mới; nội dung web dạy HẾT trên lớp, KHÔNG gắn nhãn Lớp/Nhà cho mục bài học. BTVN = một ĐỀ thầy giao cuối buổi (ô ghi tên đề, làm ở đâu, hạn, điểm, câu sai), không phải phần lý thuyết mang về.
- Bài tập mẫu: dạng dễ chỉ mấu chốt điền khuyết + ô đáp số (cao 9 mm cho phân số); dạng khó thêm MỘT ô "Phân tích và giải" 9 dòng — KHÔNG bảng phân tích đề riêng (phân tích ngay trong ô khi học).
- Nhãn yêu cầu ghi gọn ("Phân tích và giải", "Giải"), không ghi cách làm trong ngoặc. Số + đơn vị không tách dòng (đưa đơn vị vào KaTeX `\\ \\mathrm{g}` hoặc bọc `.nw`).
- Trang sửa bài theo góc HS trung bình theo kịp 30′: lưới đáp án em–đúng P.I 12 ô / P.II 3×a–d / P.III 3 ô (khoanh câu sai) → 4 ô "Câu …" rộng chỉ 4 tick lí do (đọc đề/công thức/tính/đơn vị) + ☐ làm lại (tr.10) → Ghi nhớ 2 dòng → dòng "Xem lại ở Tập". Không dùng bảng nhiều cột tick (HS không kịp điền khi thầy chữa).
- Lớp 10/11 buổi 195′ → bài mới còn 135′: ruột tập các bài đó có thể đưa nhiều dạng lên lớp hơn (xem `project_thachlab_lich_tuan.md`).

**Còn chờ:** thầy in thử giấy thật (chưa ai cầm bản in); `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/theory.html 15` (đưa data-tap vào DB) + deploy; migration `20261024190000_lesson_notes.sql` (ghi chú HS đồng bộ tài khoản). Nhánh `claude/fix-font-spacing-71c4ad` chỉ có commit font đã cherry-pick sang đây (e752ac9fb) — không cần merge lại.
