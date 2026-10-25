---
name: project_thachlab_thi_nghiem_khung_de_thi
description: "Phần thí nghiệm bài lý thuyết L12 viết theo khung đề TN THPT (T1–T12); bài 14 đã đăng 25/10, 21 bài còn lại làm bằng skill cap-nhat-thi-nghiem-l12"
metadata:
  node_type: memory
  type: project
  originSessionId: c1bea9a0-fc9e-418d-a317-6d692fdb0264
  modified: 2026-10-25T09:54:42.741Z
---

Thầy chốt 25/10/2026: phần thí nghiệm trong bài lý thuyết phải viết theo cách đề TN THPT hỏi (5/8 câu Phần II hai đề
2025–2026 là câu thí nghiệm: giả thuyết → dụng cụ → bước → coi rằng/bỏ qua → kết quả → kết luận → cơ chế → giới hạn).

- Quy tắc T1–T12 + checklist: `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md`.
- Skill làm tiếp các bài: `.claude/skills/cap-nhat-thi-nghiem-l12/SKILL.md` (bảng 22 bài L12 + id, thứ tự ưu tiên 5 → 11 → 13 → 7 → 4).
- Đã đăng: L12 Bài 14 (id 15) 25/10, sao lưu `scripts/logs/ly-thuyet-bai15-backup-1792921923643.json`.

**Why:** học sinh thuộc kết luận nhưng mất ý c) cơ chế và d) giới hạn của câu Đúng/Sai; bài cũ lộ kết quả trước hộp Dự đoán.
**How to apply:** mỗi lượt 1–3 bài cùng chương; đo `lint_do_dai` trước vì khung 6 ô dài gấp đôi; đăng bằng `cap-nhat-ly-thuyet.sh`
từ checkout chính (worktree thiếu `.env.local`). Liên quan: [[project_thachlab_bai_ly_thuyet_tuong_tac]], [[project_thachlab_cap_nhat_ly_thuyet]].
