---
name: project-thachlab-hinh-openstax
description: "Thầy chấp nhận CC BY-NC-SA 4.0 của OpenStax College Physics 2e (27/10/2026); 21 bài L12 đã thay 25 hình bằng ảnh OpenStax, đã đăng DB + deploy 27/10; quy tắc: chèn ảnh thẳng, không vẽ lại SVG theo sách"
metadata:
  node_type: memory
  type: project
  originSessionId: 32ff1e79-27fc-4112-9462-4348c643deb0
  modified: 2026-10-30T08:00:00.000Z
---

Ngày 27/10/2026 thầy Thạch **chấp nhận điều kiện CC BY‑NC‑SA 4.0** của OpenStax College Physics 2e (ghi nguồn mỗi trang trong figcaption, phi thương mại, phái sinh cùng giấy phép) để dùng hình cho bài lý thuyết lớp 12. Không hỏi lại. Đoạn giấy phép đã thêm ở `/dieu-khoan`.

- **Đã xong 27/10/2026**: 21 bài L12 đổi 25 hình sang ảnh OpenStax (`public/assets/openstax/<bài>/`, 33 file webp), giữ 58 SVG; đăng DB bằng `cap-nhat-ly-thuyet.sh`, deploy ảnh, 33/33 ảnh trả 200 image/webp; CHƯA xem trang thật ở 375 px (bài 13 Hình 3 chữ ~9 px, bài 2 Hình 3b/3c, ảnh Geiger bài 18 chưa đối chiếu nguồn Commons). Nhánh `claude/distracted-gauss-2d45d4` đã vào main. Bảng: `docs/ra-soat/hinh-openstax-l12.md`.
- Quy tắc thầy chốt sau đợt 1: **SVG agent vẽ lại theo sách sai nhiều → chèn ảnh OpenStax trực tiếp**, chữ Anh giải nghĩa trong figcaption; chỉ giữ SVG khi sách không có hình. Prompt: `docs/prompt-hinh-openstax.md`.
- Kế hoạch HRW 12e (Wiley, không giấy phép mở → chỉ tham khảo): `docs/prompt-ra-hinh-theo-hrw.md`, bảng `docs/ra-soat/hinh-hrw-l12.md`; 19 bài đã sửa SVG, đã đăng, nhánh `claude/kind-satoshi-913de4` trong main.
- Còn mở: phần câu hỏi kiểu HRW cho ngân hàng chỉ mới bàn, chưa quyết; `l12-may-phat-dien-bien-ap` vẫn 2698 chữ (quá hạn mức từ trước).

- **Đồng bộ repo↔DB 30/10**: 12 bài chỉ DB có thêm (Trả bài "nói bằng lời…", video Coulomb/áp suất/thực hành từ, data-khung) đã kéo về repo (theory.html, src, bundle). **8 bài lệch hai chiều đã chốt 30/10 theo bản mới nhất** (thầy duyệt): đăng repo cho ném, Newton 3, công cơ học; kéo DB về cho hướng tâm, điện trường đều; cảm ứng, hạt nhân, điện từ trường lấy bản nhánh ice-water (đã gộp vào main); gắn lại video bị mất ở Áp suất–động năng và Điện từ trường (video đặt SAU dòng nguồn).

**Why:** giấy phép NC là rủi ro thầy đã cân nhắc và quyết; agent sau chỉ cần làm đúng điều kiện ghi nguồn.
- **30/10/2026 rà 78 hình/51 bài**: bỏ 56 số mũ nguồn ảnh lạc chỗ (dòng 🔑, ngoài `<details>`), sửa 14.11a/b (Sự chuyển thể), 3 dòng nguồn Thang nhiệt độ, caption Hình 2 Biến dạng vật rắn; đăng 38 bài từ bản xuất DB (13 bài DB không có số mũ lạc). Nguồn ảnh: `</figure>` liền `<ol class="tl-fns">`, ≥1280 ra lề ngang đầu hình (commit 3573db29d), màn hẹp dưới hình; `_margin_fig.py` chỉ gắn số mũ khi đoạn sát hình. DB lệch repo ở 23 bài (video/khung, Trả bài; 6 bài DB còn nguồn trong figcaption: biến dạng, Newton 3, hướng tâm, moment, công cơ học, sóng ngang–dọc) — chưa đồng bộ. Đã deploy 30/10 (bản tĩnh bài 2, 3). Cùng ngày đưa nguồn 6 bài đó ra tl-fns trên DB (xong, khớp DB).

**How to apply:** mọi hình OpenStax phải có dòng nguồn + giấy phép trong figcaption, giữ `(credit: …)` của bên thứ ba; không nhúng URL CDN OpenStax thẳng; không giao agent vẽ lại SVG theo hình sách. Liên quan: [[project-thachlab-bai-ly-thuyet-tuong-tac]], [[project-thachlab-phap-ly-ban-quyen]].
