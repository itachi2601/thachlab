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

## Cập nhật 14/10/2026 (phiên Mac tiếp quản) — K1–K3, K5, K6 xong; K4 mới quét
- Git: thực tế không có merge dở/stash "truoc-pull-13-10" (đã pop sẵn vào nhánh `cursor/ui-c3`, 115 file dở của phiên khác còn nguyên trong cây). `main` đã merge origin/main + nhánh Cursor (C1–C3 xếp chồng trong `cursor/ui-c3`), đã push (df4966405). Kiểm-code: C1–C3 đạt; sửa thêm `stripHtml` entity số.
- K6: 4 SVG bìa Gemini (`public/images/learning-path/*.svg`, 400×300) gắn vào `LearningPath`, xoá 4 jpg cũ. **G2 huy hiệu Hạng 1/2/3 chưa có** (`assets/huy-hieu-gemini/` không tồn tại) → HonorBoard chưa đổi. Chữ trong SVG bìa 12px/400 = ~8px khi hiển thị, chỉ là trang trí.
- K1: trang chủ 12 → 6 khối (Hero+ribbon, Lớp, Tìm, Lộ trình, Phụ huynh, Vinh danh); Features/ExamSamples/AboutFounder/Testimonials sang `/gioi-thieu`; mobile 15.000 → ~9.000px. C4 làm luôn (ribbon dưới hero). Navbar/Footer/ExamSamplePreview đổi link.
- K2: poster → bảng HTML theo mức điểm, tên viết tắt; K3: 3 câu trích (chép bằng agent đọc ảnh) + ảnh melbourne.jpg; K5: CSS `.tl-box` trung tính, `--think` primary nhạt, `.theory-next` primary đặc (globals.css cuối khối tl-*).
- **K4 chưa sửa, cần thầy quyết:** `scripts/quet-nhan-svg.mts` (chỉ đọc) → 100/106 bài có SVG; 2699/3669 nhãn <13px khi hiển thị ở 375 (nhỏ nhất 7px), 1446 màu nhạt. Nâng cỡ chữ hàng loạt sẽ làm chữ đè nhau → nên sửa ở `svg_lib.py` cho bài mới + sửa từng bài sau khi xem hình; kết quả ở `scripts/logs/quet-nhan-svg.json`.
- Việc dở của phiên khác còn trong cây: `HomeByTrack`/`CttcHome` (Navbar, page.tsx đã có hunk riêng, chưa commit) — commit page.tsx/Navbar của tôi bằng blob từ HEAD để không kéo theo.
- `scripts/do-bo-cuc.mjs --toan-trang` nay tự cuộn hết trang trước khi chụp.
