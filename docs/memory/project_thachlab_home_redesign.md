---
name: thachlab-home-redesign
description: "Trang chủ ThachLab thiết kế lại 22/9/2026 (bớt \"AI-look\", cyan chủ đạo, ít card/glow) — code xong + test, CHƯA commit/deploy"
metadata: 
  node_type: memory
  type: project
  originSessionId: a08b3153-be42-436b-9d59-3b1b6c6ba581
  modified: 2026-09-22T03:56:55.789Z
---

Trang chủ (7 section trong components/home + link Footer) đã viết lại ngày 22/9/2026: cyan làm màu nhấn, tiêu đề trắng, chỉ 1 gradient ở "dao động?", bỏ .glass/.glow-blob/.text-gradient khỏi trang chủ (class dùng chung vẫn giữ trong globals.css vì trang khác còn dùng). Mô phỏng con lắc giữ nguyên. Đã test desktop/mobile/light theme, tsc + eslint + next build pass. Commit 06866fcb trên main, deploy.sh chạy OK 22/9/2026 (deploy branch 92107a1).

**Why:** Thầy muốn trang chủ bớt cảm giác "web do AI tạo" nhưng giữ nền tối + bản sắc Vật lý.

**How to apply:** Tài nguyên còn thiếu: ảnh thật thầy Thạch (mục "Một chút về thầy Thạch" đang thuần chữ), ảnh + bài viết cho 3 câu hỏi phụ ở "Vật lý quanh ta" (đang hiện dạng danh sách không link). Không bịa tiểu sử/thành tích.

**Cập nhật 1/10/2026 — so với bản DeepSeek đề xuất (nền sáng, 2 cột + sidebar):** không đổi theme, chỉ ghép 4 ý:
PublicSubNav (vào nhanh lớp, chỉ trang chủ), OpenClasses thay AudienceChooser (4 thẻ lớp + số chương/bài/mục + dải
tổng, số đọc lúc build từ `public/data/home-stats.json` do `build-content.mjs` sinh — không gọi Supabase khi tải),
Testimonials mặc định 4 ảnh. Không lấy: sidebar 2 cột, hộp đăng ký cạnh hero, light theme toàn trang, bỏ HonorBoard.
Thứ tự section: SubNav → OpenClasses → Hero mô phỏng → Features → PhysicsEverywhere → LearningPath → HonorBoard →
AboutFounder → Testimonials. Số liệu trang chủ chỉ mới sau mỗi lần deploy (prebuild).
