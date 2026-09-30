---
name: project_thachlab_examrunner_nav_bug
description: "Bug có sẵn ở ExamRunner: chuyển câu (Câu sau/bảng câu) tăng đúng bộ đếm nhưng nội dung câu hỏi không đổi theo — phát hiện 25/9/2026; trạng thái sửa chưa rõ tính tới 26/9/2026"
metadata:
  node_type: memory
  type: project
  originSessionId: a0371ff8-6129-47a6-847d-b1c438608c7c
  modified: 2026-09-26T11:17:09.725Z
---

Phát hiện khi tự kiểm tính năng [[project_thachlab_kiem_tra_hieu_bai]] (không liên
quan tới thay đổi đó — tái hiện được trên đề id=88, một đề cũ có sẵn từ trước).

Bấm "Câu sau →" hoặc bấm số câu ở bảng câu hỏi trong `components/exams/ExamRunner.tsx`
(trang `/kiem-tra/lam`): dòng đếm "Câu N/M" và số "đã làm" cập nhật đúng, nhưng khối
nội dung câu hỏi (đề bài + đáp án) vẫn giữ nguyên câu 1, không đổi theo `cur`.

Đã gắn task nền để điều tra + sửa, chưa chạy. Nghi ở chỗ AnimatePresence/key bọc
QuestionCard không khớp đúng lúc `cur` đổi. **Chưa xác nhận 100%** đây có phải lỗi
người dùng thật gặp hay chỉ là do môi trường tự động hoá trình duyệt (Claude Browser
tool dùng `.click()` DOM thật, không phải thao tác chuột người dùng) — việc đầu tiên
khi sửa là tự tay bấm thử trên trình duyệt thật để xác nhận.

**Why:** đáng lẽ không liên quan gì tới việc đang làm, nhưng là bug ảnh hưởng luồng
làm bài thi chính — ghi lại để không quên, không tự sửa ngay vì ngoài phạm vi việc
đang làm lúc phát hiện.
**How to apply:** khi thầy báo "bấm câu sau mà đề không đổi" hoặc tương tự, đây có
thể là đúng bug này — ưu tiên xác nhận trên trình duyệt thật trước khi sửa.

**Cập nhật 26/9/2026 (bàn giao):** không rõ task nền (thầy tự bấm chạy trong 1
phiên riêng) đã sửa xong chưa — phiên này không nhận được kết quả. Thấy
`components/exams/ExamReviewPager.tsx` đang bị sửa dở trong working tree, và
MEMORY.md có mục "Bảng câu hỏi chia mục TN/ĐS/TLN" (commit push 26/9/2026, chưa
test UI thật) cũng đụng đúng 2 file `ExamRunner.tsx`/`ExamReviewPager.tsx` —
CHƯA XÁC ĐỊNH được đây là cùng 1 việc (fix bug này) hay là việc khác (thêm tính
năng chia mục TN/ĐS/TLN) chỉ tình cờ chung file. Phiên sau cần: `git log -p` 2
file này từ sau 25/9/2026 để xem có commit nào thật sự sửa AnimatePresence/key
không, rồi tự tay bấm thử "Câu sau" trên trình duyệt thật để xác nhận còn bug
hay đã hết.
