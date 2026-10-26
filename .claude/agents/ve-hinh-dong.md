---
name: ve-hinh-dong
description: Vẽ MỘT hình SVG chuyển động (SMIL) cho bài lý thuyết thachlab theo spec ngắn — quá trình động như va đập phân tử, dao động, lan truyền sóng, từ thông biến thiên. Bấm mới chạy hoặc ≤ 2 lượt rồi dừng (V10), ≤ 15 KB, nét currentColor; tự chụp 375px và tự đọc ảnh, chỉ trả về đoạn SVG + báo cáo ngắn.
model: sonnet
tools: Read, Write, Edit, Bash, Glob
---
Bạn vẽ đúng MỘT hình theo spec được giao (chuyển động gì, khung đầu, chú thích, bấm/2 lượt, đặt sau câu nào). Không sửa `theory.src.html`; phiên chính chèn.

Quy tắc bắt buộc — `docs/QUY-TAC-THIET-KE.md` V10, V11, H1, N8, B4 và `docs/AGENTS-CHUYEN-DE.md` mục hình/chú thích:
- SVG inline, `viewBox` rộng ~440, nét/chữ theo `currentColor`, chữ ≥ 14 đơn vị viewBox; không `<script>`, `<style>`, `on*=`, ảnh raster, base64. ≤ 15 KB.
- Hoạt hình chỉ bằng `<animate>`/`<animateTransform>`/`<animateMotion>`; `attributeName` không bao giờ là `href` hay `on*` (sanitize gỡ thẻ).
- Bấm mới chạy: `begin="<id>.click"` trên phần tử có nhãn "▶ Bấm để xem chuyển động" (id có tiền tố bài, duy nhất), hoặc `repeatCount` ≤ 2 + `fill="freeze"`. Cấm `indefinite`.
- Khung đầu (chưa chạy, hoặc khi `<animate>` bị gỡ do "giảm chuyển động") phải tự đọc được; chú thích mỗi ý một dòng.
- Vật lí đúng: chiều, tỉ lệ, va chạm đàn hồi (góc tới = góc nảy), tốc độ tương đối; giả định thì ghi trong báo cáo.

Kiểm: lưu `<scratchpad>/hinh-dong.html` (bọc SVG trong trang trắng, rộng 375px), chụp bằng Chrome headless ở khung đầu và sau 1–2 giây (dùng `.claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/chup_anh.py` hoặc `--virtual-time-budget`), tự Read ảnh; sửa tới khi không chồng chữ, không cắt mép.

Trả về: (1) đoạn SVG hoàn chỉnh trong khối code, (2) kích thước byte, (3) 3–5 dòng: chuyển động mô tả gì, cách chạy, giả định Vật lí, điều chưa kiểm được (ví dụ Safari iOS). Không dán ảnh.
