---
name: project_thachlab_ra_soat_giao_dien
description: "Rà soát mỹ thuật giao diện 2026-10-13 (ảnh chụp thật 375/1280) → 10 điểm cần sửa + 2 lỗi hiển thị; phân công Cursor C1–C4 / Gemini G1–G2 / Claude K1–K6 trong docs/PHAN-CONG-UI-2026-10-13.md"
metadata:
  node_type: memory
  type: project
  modified: 2026-10-13T17:00:00.000Z
---

**Mục tiêu:** sửa giao diện theo bản nhận xét 2026-10-13 (phiên cloud `claude/charming-hopper-4vgvxp`, commit `295f186c`).
Bản phân công + prompt sẵn để dán: `docs/PHAN-CONG-UI-2026-10-13.md`. Thầy sẽ tự dán cho Cursor/Gemini; phiên Mac nhận lại.

## Kết luận rà soát (2026-10-13)
Nền tảng vững (một màu nhấn, tương phản đo bằng script, chữ 16–18px). Yếu ở bản sắc và nhất quán:
1. Bìa AI neon ở `components/home/LearningPath.tsx` (`public/images/learning-path/*.jpg|webp`) phá hệ màu nặng nhất.
2. Trang bài học 375px: 3 tầng cố định đáy (MobileTabBar + toolbar LessonPresenter + BugReportWidget) ≈130px.
3. Trang chủ 12 khối, 10.000px desktop / 15.000px mobile.
4. Dải "Vật lý quanh ta" (`PhysicsPostRibbon`) nằm TRÊN H1 hero.
5. Huy hiệu Hạng 1/2/3 (`HonorBoard`) thô. 6. Ảnh chat đen ở `Testimonials`. 7. Bo góc không thống nhất (pill/8px/999px).
8. Nhãn chữ trong SVG bài học ~11px, màu pastel. 9. Hộp Mục tiêu/Dự đoán/nút TIẾP cùng tông xanh lơ.
10. `/phu-huynh`: poster điểm TNTHPT công khai tên + điểm HS, mâu thuẫn dòng "không công khai" ngay dưới.

## Lỗi hiển thị thật (chưa sửa)
- `app/lop-hoc/page.tsx:777` đổ `p.body` HTML thô vào `<small>` → trang Lớp 10 hiện `<p><strong>`.
- Cùng khối đó ở 375px vỡ mỗi chữ một dòng (CSS `components/lessons/class-overview.css`, thiếu `min-width:0`).

## Còn chờ
- Thầy dán prompt Cursor C1–C4 (nhánh `cursor/ui-c1..c4`) và Gemini G1–G2 (lưu `assets/bia-gemini/`, `assets/huy-hieu-gemini/`).
- Phiên Mac làm K1–K6 (mục C của file phân công); K6 = soát nhánh Cursor bằng `kiem-code` + gắn SVG Gemini. Chưa sửa dòng code nào.
- Mọi UI HS: nêu mã quy tắc `docs/QUY-TAC-THIET-KE.md`; chụp 375 trước.

## Cách chụp đúng (bài học)
`scripts/do-bo-cuc.mjs` chụp toàn trang ra khoảng trắng lớn vì `whileInView` chưa kích hoạt → phải cuộn hết trang
(bước 0,6 viewport, 250 ms/bước) rồi về đầu trước khi `captureScreenshot`. Trên cloud: Chrome ở `/opt/pw-browsers/chromium`
+ `--no-sandbox`. Nên thêm bước cuộn vào script (chưa làm, cần thầy duyệt vì script dùng chung).
