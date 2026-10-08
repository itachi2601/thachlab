---
name: project-thachlab-cap-nhat-ly-thuyet
description: Quy tắc đẩy riêng phần lý thuyết bài học lên DB (script cap-nhat-ly-thuyet.sh), bài Giao thoa sóng L11 đã soạn chờ đăng
metadata:
  type: project
---

Thầy yêu cầu 2/10/2026: cập nhật bài lý thuyết tương tác phải **chỉ đẩy phần lý thuyết**, không đụng đề/bài tập mẫu/tiêu đề. Bộ script: `scripts/cap-nhat-ly-thuyet.sh` (bọc `update-ly-thuyet-from-bundle.mts`, nhận theory.html hoặc bundle.json, mặc định chỉ ghi `body_html`, tự sao lưu) + `khoi-phuc-ly-thuyet.mts`. Quy tắc đã ghi vào `AGENTS.md` và skill soan-bai-ly-thuyet-tuong-tac.

Bài Giao thoa sóng Vật lí 11 (lesson 31) soạn xong tại `content/lesson-samples/l11-giao-thoa-song/` (commit e4f76f15), **chưa đăng**: chờ thầy chạy `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l11-giao-thoa-song/theory.html 31`.

**Why:** tránh ghi đè Luyện tập/đề đã có học sinh làm.
**How to apply:** mọi lần đăng lại lý thuyết dùng script này; `\lt` thay `<` trong công thức.

## 4/10/2026 — quy tắc thành ràng buộc trong script (thầy: "chỉ đăng đúng vào phần lý thuyết của bài, không làm ảnh hưởng đến phần còn lại")

`update-ly-thuyet-from-bundle.mts` nay tự thực thi quy tắc, không dựa vào việc người chạy nhớ:
1. Lọc đúng MỘT mục `kind='ly_thuyet'` của bài; 0 hoặc >1 mục → dừng (không tự tạo mục).
2. `--dry-run` in rõ **phạm vi**: "CHỈ mục #108 (ly_thuyet). 2 mục khác của bài giữ nguyên — #109 bai_tap_mau, #110 luyen_tap."
3. UPDATE ràng buộc cả `id` lẫn `kind='ly_thuyet'`, `.select("id")` và đòi đúng 1 dòng bị ảnh hưởng.
4. Chụp toàn bộ `lesson_items` của bài TRƯỚC/SAU rồi đối chiếu: ngoài `body_html` (và `title`/`subtitle` khi
   `--with-title`) của mục Lý thuyết, mọi cột/mục khác phải y nguyên; lệch → in danh sách chỗ lệch + lệnh hoàn tác,
   `exit 1`. Logic đối chiếu đã kiểm bằng 8 ca (chỉ body_html đổi / mục Luyện tập đổi / mất exam_ids / đổi title
   ngoài phạm vi / có `--with-title` / thêm mục / mất mục / không đổi gì) — tất cả đúng.
5. Quy tắc ghi ở `AGENTS.md` mục "Cập nhật bài lý thuyết đã đăng" + bước 7 của skill soan-bai-ly-thuyet-tuong-tac,
   kèm câu "sửa script thì giữ nguyên phần kiểm này".

Bài 13 Tổng hợp và phân tích lực (lớp 10, lesson 58) đã đăng theo đúng quy tắc này 4/10/2026 (item 108, sao lưu
`scripts/logs/ly-thuyet-bai58-backup-1791083195069.json`), đã deploy; mục #109 và #110 giữ nguyên.

## 8/10/2026 tối — mẻ sửa lý thuyết 20 bài L12 bị `git stash` + `reset` nuốt mất (và bị nuốt LẦN HAI trong lúc sửa)

Batch `scripts/batch-ra-soat-bai.mts --che-do sua-ly-thuyet` ghi thẳng vào `content/lesson-samples/<bài>/theory.src.html`
trong working tree (13:04), **không commit**. 22:44 một bước dọn cây để pull (`git stash` + `git reset`) cất cả mẻ vào
`stash@{0}` và trả cây về bản trước khi sửa — trong khi `content/gemini/hang-doi.md` vẫn ghi `loi-lint`/`da-sua` như thật.
Hậu quả: DB của bài 4, 14, 15, 17, 18, 125, 126 là bản ĐÃ SỬA còn file repo là bản CŨ (đăng lại từ repo là lùi nội dung);
19 bài còn lại mất phần sửa.

- Cách moi lại: `git stash show --name-only stash@{0}` → `git show "stash@{0}:<đường-dẫn>" > <đường-dẫn>` (chỉ lấy file của
  mình, đừng `stash pop` cả mẻ). Rồi `cd content/lesson-samples/<bài> && python3 build_figs.py && python3 build_bundle.py`.
- Đã làm xong chương 1 L12 (Bài 1–4, lesson 2–5): cắt còn 2.434/2.445/2.484/2.436 từ hiện ngay, soát vật lí độc lập
  (sửa 3 chỗ bài 3, 1 chỗ bài 2, 1 chú thích hình bài 4), 4 lệnh lint/quiz/bundle sạch, đăng DB, `so-file-voi-db.mts` xác nhận file = DB.
- **15 bài L12 còn lại chưa khôi phục** — cùng mẻ, cùng cách làm.
- Trong lúc sửa, tiến trình khác lại `git stash` + `git reset` (23:18, 23:24) → mất việc lần hai. Cách chống: commit NGAY sau
  `--nhan`, và khi cây chính đang bận (merge) thì cứu việc bằng `git worktree add <tmp> -b claude/... origin/main` rồi commit/push
  ở worktree đó (không `git commit -- <path>` được khi đang merge: "cannot do a partial commit during a merge").
