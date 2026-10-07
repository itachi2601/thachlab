---
name: xong-viec
description: Quy trình chốt việc sau khi code xong, chạy một mạch không hỏi từng bước: kiểm → soát diff → commit đúng file → (deploy) → rút kinh nghiệm → bàn giao. Dùng khi thầy nói "xong rồi", "chốt", "/xong-viec", "commit và deploy đi".
---

# Chốt việc — chạy liền, chỉ dừng khi gặp mục "DỪNG & HỎI"

Thầy đã chốt: không hỏi từng bước. Làm tuần tự, cuối cùng báo MỘT lần.

## 1. Kiểm (bỏ bước không áp dụng)
- `npx tsc --noEmit` (+ `npm run lint` nếu đụng component).
- UI học sinh/phụ huynh: xem thử 375px, nêu mã quy tắc (QUY-TAC-THIET-KE), không báo xong khi chưa xem.
- Có ảnh mới/đụng trang đã tối ưu: ảnh ≤150 KB, không thêm round-trip Supabase.

## 2. Soát
- Diff > ~50 dòng hoặc có nội dung đăng: gọi agent `kiem-code`. Diff nhỏ: tự đọc `git diff`.

## 3. Commit
- Chỉ file của việc này: `git add <file mới>` rồi `git commit -- <path>`; không `git add -A`. File của phiên khác lẫn trong diff → bỏ lại.
- Thông điệp theo phong cách repo (`feat(...)`, `content(...)`, `fix(...)`), kèm Co-Authored-By.
- Trên Mac: commit thẳng `main`. Trên cloud: push nhánh `claude/...` và in lệnh merge.

## 4. Đưa lên web (chỉ khi việc ảnh hưởng web)
- Có migration → KHÔNG tự chạy; cập nhật `FILES` trong `scripts/run-migrations.sh`, in `bash scripts/run-migrations.sh` + 3 dòng (làm gì / ngoài giờ làm bài? / rollback), ghi "ĐANG CHỜ" vào `docs/STATE.md`.
- Có sửa code/nội dung tĩnh: build sạch trong worktree nếu working tree còn WIP phiên khác, rồi `bash scripts/deploy.sh` (nếu bước push bị chặn → in đúng lệnh cho thầy chạy).
- Có script/skill cho thầy chạy: đảm bảo đã vào `main`, lệnh đầu là `cd /Users/MAC/Projects/thachlab && git pull origin main`.

## 5. Rút kinh nghiệm (chỉ khi có làm lý thuyết/đề/quiz/ngân hàng câu)
- 3–6 gạch đầu dòng trong câu trả lời cuối + ghi vào `## Nhật ký rút kinh nghiệm` của skill liên quan (`- YYYY-MM-DD · sự cố → quy tắc`). Không có gì mới thì ghi "không có bài học mới".

## 6. Bàn giao
- Cập nhật `docs/STATE.md` (chỉ thêm dòng) và memory liên quan, hoặc chạy `/ban-giao` nếu là đợt việc lớn.

## DỪNG & HỎI (chỉ các trường hợp này)
- Schema/RLS/xoá dữ liệu production, đổi DNS.
- Diff còn lẫn việc của phiên khác không tách được.
- Kiểm ở bước 1–2 thất bại và không tự sửa được.

## Câu trả lời cuối (gọn, một lần)
Đã làm gì · commit hash · đã deploy/chưa · việc thầy phải chạy (nếu có, mỗi lệnh một khối) · rút kinh nghiệm (nếu áp dụng).

## Nhật ký rút kinh nghiệm
- 2026-10-07 · Thầy sửa tab "Thí nghiệm" ở hero trang chủ nhiều lần, sau đó thấy trang thật "quay về như cũ": thay đổi nằm trong working tree, chưa commit nên deploy (build từ commit) không có → khi thầy báo "đã sửa mà web vẫn cũ", chạy `git status` + `git show HEAD:<file> | grep <từ khoá mới>` TRƯỚC; thấy chưa commit thì commit đúng file (`git commit -- <path>`, file mới `git add` trước) rồi deploy, đừng dò nguyên nhân khác.
- 2026-10-07 · Working tree còn WIP của phiên khác nên không build thẳng được → deploy từ worktree sạch: `git worktree add --detach /tmp/tl-deploy HEAD`, `cp .env.local`, **`cp -cR node_modules`** (clone APFS, nhanh); symlink `node_modules` làm Turbopack panic "Symlink [project]/node_modules is invalid", rồi chạy `bash scripts/deploy.sh` ở tab terminal (build ~5 phút, bước TypeScript/gom trang im lặng lâu là bình thường), xong `git worktree remove --force` và `git push origin main`.
