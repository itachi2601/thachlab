---
name: project_thachlab_on_5_phut
description: Ôn 5 phút sau bài + rút Bài toán mẫu trong lý thuyết sang Dạng N — thử L11 bài 22–24 (25/11/2026), chỉ ở /dev/on-tap, chưa đăng DB, chưa cho HS thấy
metadata:
  type: project
---

**Mục tiêu (thầy 25/11/2026):** (1) mỗi bài có bản ôn thu gọn có tương tác để HS tự nhớ lại sau khi học; (2) xử lý mục "V. Bài toán mẫu" trong lý thuyết nay trùng Bài tập mẫu (100/120 bài có, ~15% số chữ).

**Đã làm (nhánh `claude/student-review-plan-7e827d`):**
- Ôn 5 phút: `scripts/on-tap/rut-the-on.py <slug>` rút thẻ từ ô Chốt mục 🎯 (thẻ lật) + câu đầu hộp bẫy (thẻ chọn, bỏ dòng ⚠ gợi ý, đổi id `on-`) → `content/on-tap/<slug>.json`. Component `components/lessons/OnNamPhut.tsx`: một thẻ/màn, lật → Nhớ rõ/Lơ mơ/Quên, "Ôn ngay" cuộn tới tiểu mục h4 (`neo` + `tieu_muc`), thẻ yếu lưu localStorage. Xem thử: `/dev/on-tap?bai=22|23|24`. Chỉ chạy được với bài có ô Chốt mục (hiện L11 22–26 và vài bài).
- Bài toán mẫu: phân 3 loại — trùng dạng → giữ đề + bảng phân tích, thay lời giải + "Điền bước" bằng hộp "Tự giải trước, rồi so đáp số" + link `#muc=bai-tap-mau&dang=N`; không trùng dạng → chuyển thành dạng mới rồi mới rút; bài thực hành → bỏ. Đã sửa bài 22 (→ D5) và 23 (→ D4, D5), mỗi bài bớt ~90–100 chữ (giữ 2 câu Thử sức vì hỏi hiểu, không hỏi quy trình). Bài 24 (lesson 43) KHÔNG có dạng "I = E/(R+r), U, đoản mạch" cơ bản → để nguyên, cần soạn thêm dạng.
- Code link dạng: `lesson-nav.ts` (`requestOpenDang`/`takePendingDang`), `page.tsx` applyHash, `WorkedQuestionsGrid.tsx` (id `dang-row-N`, mở + cuộn).

**Chưa làm / chờ thầy:** duyệt giao diện + cách rút; đặt Ôn 5 phút vào trang bài (tab hay thẻ "Ôn lại" ở Hôm nay sau 1 và 7 ngày — cần lưu DB, chưa có migration); deploy code TRƯỚC rồi mới `cap-nhat-ly-thuyet.sh` bài 22, 23 (sau 22h).
**How to apply:** thêm bài nào thì chạy script rồi đọc lại JSON, ≤8 thẻ; bài chưa có Chốt mục thì phải làm Chốt mục trước.
