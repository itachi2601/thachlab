---
name: xem-ghi-chu-lop
description: Xem lại các ghi chú thầy bấm lúc dạy (phím N / nút Ghi chú trong chế độ trình chiếu bài học, bảng teacher_lesson_notes) — gom theo bài và mục, đề xuất cải tiến cho lớp sau, thầy duyệt rồi Claude làm bằng đúng skill chuyên trách. Dùng khi thầy nói "xem ghi chú lớp", "ghi chú dạy tuần này", "cải tiến bài sau buổi dạy", "/xem-ghi-chu-lop".
---

# Xem ghi chú lúc dạy → đề xuất cải tiến cùng thầy

Ghi chú do thầy bấm **N** trong trình chiếu (`components/lessons/PresenterNoteBox.tsx`); mỗi ghi chú tự gắn bài + mục lý thuyết + trang chiếu đang xem, kèm nhãn: HS hiểu sai · Thiếu hình/mô phỏng · Ví dụ chưa hay · Dài/quá nhanh · Lỗi · Ý tưởng. Chỉ thầy (giáo viên/trợ giảng) thấy, học sinh không thấy.

## B1. Đọc (script, chỉ đọc) — tab terminal trên Mac
```
cd /Users/MAC/Projects/thachlab && npx tsx .claude/skills/xem-ghi-chu-lop/scripts/doc-ghi-chu.mts
```
Mặc định lấy ghi chú chưa xử lý; in theo bài → mục, ghi bản JSON vào `scripts/logs/`. Cloud không có service_role → in lệnh cho thầy, đừng giả vờ chạy.

## B2. Gom và đề xuất (phiên chính, ngắn)
Với mỗi bài: gộp ghi chú trùng ý; mở đúng đoạn bài liên quan (grep theo `page_heading`, không đọc cả bài); lập bảng
`# | bài › mục | thầy ghi | nguyên nhân giả định | đề xuất cụ thể | skill sẽ dùng | công sức`.
Chọn skill theo nhãn:
| Nhãn | Hướng thường gặp | Skill |
|---|---|---|
| HS hiểu sai | thêm câu dự đoán / "bẫy" vào bài, đổi cách mở, thêm câu kiểm tra nhanh | `soan-bai-ly-thuyet-tuong-tac`, `soan-quiz-ly-thuyet` |
| Thiếu hình/mô phỏng | tìm PhET hoặc vẽ SVG | `phet`, `tai-nguyen-bai-hoc` |
| Ví dụ chưa hay / bài tập mẫu | đổi tình huống, thêm dạng | `soan-bai-ly-thuyet-tuong-tac`, `soan-bai-tap-mau` |
| Dài / quá nhanh | cắt, tách trang chiếu, xem `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md` (hạn mức) | `soan-bai-ly-thuyet-tuong-tac` |
| Lỗi | sửa tối thiểu rồi `kiem-code` soát | `cap-nhat-ly-thuyet.sh` |
| Ý tưởng về tính năng web | tư vấn theo nghiên cứu (AGENTS.md "Mọi quyết định đổi/thêm tính năng") | phiên chính |
Ghi chú không đủ rõ → hỏi lại thầy, đừng đoán.

## B3. Thầy duyệt, Claude làm
Đưa bảng cho thầy; chỉ làm mục thầy gật. Sửa lý thuyết đã đăng: chỉ ghi mục Lý thuyết (`scripts/cap-nhat-ly-thuyet.sh`), theo AGENTS.md. Nhớ giao `kiem-code` soát nội dung trước khi đăng.

## B4. Đóng ghi chú
```
npx tsx .claude/skills/xem-ghi-chu-lop/scripts/doc-ghi-chu.mts --danh-dau da_xu_ly --ids 3,5 --ghi "thêm PhET, đăng 14/10"
```
`da_xem` cho ghi chú đã đọc nhưng chưa làm. Cuối buổi báo thầy: đã làm gì, còn treo gì.

## Nhật ký rút kinh nghiệm
- 2026-10-14 · skill mới, chưa chạy với ghi chú thật → sau lần xem đầu tiên ghi lại chỗ nào bảng B2 thiếu cột/nhãn.
