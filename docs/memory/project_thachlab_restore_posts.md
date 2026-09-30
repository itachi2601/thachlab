---
name: project-thachlab-restore-posts
description: Một số bài đăng (posts) bị xóa mất khỏi Supabase; script khôi phục đã viết nhưng file dữ liệu vẫn là mẫu rỗng
metadata: 
  node_type: memory
  type: project
  originSessionId: a5c2c433-2393-47b5-bb5f-96d72c3fc6fc
  modified: 2026-09-21T15:47:41.521Z
---

Một số bài đăng trong bảng `posts` (+ `post_classes`) bị xóa mất khỏi Supabase. Đã viết
`scripts/restore-posts.mjs` để nạp lại (chưa commit, tính đến 2026-09-14).

App export tĩnh (`next.config output: "export"`) nên không có API route service-role ở
production — script **chỉ chạy cục bộ**, cần `SUPABASE_SERVICE_ROLE_KEY` lấy ở Supabase
Dashboard → Settings → API. Key đó là secret: không commit, không để vào `.env.local`,
không dán vào chat. Script an toàn chạy lại: bỏ qua bài đã có (so khớp title).

**Còn treo:** `scripts/data/restore-posts.json` vẫn là file mẫu, mới có đúng một dòng
`"VÍ DỤ — xóa dòng này, điền các bài đăng thật vào"`. Thầy phải tự điền nội dung các bài
đã mất vào đó rồi mới chạy được.

**2026-09-21: thầy không nhớ nội dung các bài đã mất, quyết định BỎ QUA việc khôi phục.**
Đã kiểm tra không còn nguồn nào khác để lấy lại nội dung — không có trong repo, Wayback
Machine chưa từng crawl `thachlab.id.vn`. Script + file mẫu vẫn để nguyên trong working
tree (chưa commit, vô hại) phòng khi thầy tìm lại được nội dung sau này (Zalo/Facebook/
ảnh chụp màn hình). Đừng chủ động nhắc lại việc này trừ khi thầy hỏi lại.
