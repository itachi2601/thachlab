# Trình chiếu bài tập mẫu — thiết kế và kế hoạch triển khai (17/11/2026)

Thầy chiếu một dạng bài tập mẫu lên máy chiếu và giải cùng lớp. Bố cục:
- **Trái (cố định):** Cho/Tìm, hình vẽ thêm dần theo bước, bảng trạng thái ①② (nếu có).
- **Phải:** đề bài → "Kiến thức cần gọi lại" → từng bước giải.
  - Mỗi bước: hỏi lớp, phương án A/B/C, rồi hiện lời giải từng dòng.
  - Bước xong thu lại thành một dòng tóm tắt.
- **Cuối:** Đáp số, 🔎 Nhận dạng, ⚠ Bẫy.

Giao diện dùng chung khung `.lesson-presenter` với trình chiếu lý thuyết: thanh trên, thanh nút dưới, nền sáng/tối nhớ chung khoá `thachlab-presenter-bg`.

Phím tắt:

| Phím | Tác dụng |
|---|---|
| → / Space | tiếp |
| ← | lùi |
| 1–9 | nhảy tới bước |
| `[` `]` | đổi dạng |
| F | toàn màn hình |
| B | đổi nền sáng/tối |
| D / H / E | bút vẽ / dạ quang / tẩy (nét lưu theo từng dạng) |
| Z / C | bỏ nét vừa vẽ / xoá hết nét của dạng |
| Ctrl + / − / 0 | phóng to / thu nhỏ / cỡ gốc (nhớ khoá `thachlab-btm-zoom`) |
| N | ghi chú nhanh cho bước đang chiếu (bảng `teacher_lesson_notes`, `page_key` = `btm-<stt>-b<bước>`) |
| ? | bảng phím tắt |
| Esc | đóng bảng → tắt bút → thoát |

Link sâu: thêm `#chieu-btm-3` vào link trang bài → giáo viên mở là vào thẳng dạng 3 của mục Bài tập mẫu đầu tiên.

## Code

| File | Vai trò |
|---|---|
| `features/lessons/btm-trinh-chieu/types.ts` | kiểu `ChieuBai` (bản chiếu) + `ChieuGhiDe` (trường tuỳ chọn `trinh_chieu` của dạng) |
| `features/lessons/btm-trinh-chieu/tu-dang.tsx` | **dựng bản chiếu tự động** từ dạng đã soạn (`problem_html`, `tom_de`, `buoc[]`, `chon_buoc_ke`, `.bt-step`, `.bt-ans`, `.bt-final`, `cong_cu`) |
| `features/lessons/btm-trinh-chieu/mau-ong-thuy-ngan.tsx` | mẫu soạn tay đầy đủ: bảng ①②, hình SVG từng lớp, bẫy |
| `components/lessons/btm-trinh-chieu/BtmPresenter.tsx` + `.module.css` | màn chiếu |
| `components/lessons/presenter-ink.tsx` | bút vẽ dùng chung (`usePresenterInk` + `PresenterInkTools`), tách từ `LessonPresenter` — LessonPresenter chưa chuyển sang (đổi khi có dịp sửa file đó) |
| `components/lessons/btm-trinh-chieu/BtmPresenterLazy.tsx` | `next/dynamic({ssr:false})` + `LazyErrorBoundary` — không nặng thêm trang HS |
| `components/lessons/WorkedQuestionsGrid.tsx` | nút "Trình chiếu dạng này" trong từng dạng (chỉ khi xem bằng quyền giáo viên) |
| `app/lop-hoc/bai/page.tsx` | mở màn chiếu, dùng `questions` đã tải — **0 request Supabase mới** |
| `app/dev/btm-trinh-chieu` | xem thử: không tham số → mẫu soạn tay; `?f=btm` → file `public/xem-thu/btm.json` do `publish-bai-tap-mau.mts --lesson N --xem-thu` sinh ra |

## Hiện trạng dữ liệu (quét 17/11/2026)

- `scripts/data/bai-tap-mau/`: 101 bài, **523 dạng**.
- Cả 523 dạng có `problem_html` và lời giải chia `.bt-step`.
- Ở cả 523 dạng, số `buoc` khớp số `.bt-step` → tự dựng được ngay, không cần soạn thêm.

Mức đầy đủ:
- Có hình `cong_cu`: 515 dạng.
- Có `tom_de`: 510 dạng. Dạng thiếu `tom_de` thì cột trái hiện đề thu nhỏ.

Dạng cũ trên DB không có `buoc` nhưng có `.bt-step` vẫn chiếu được (tên bước lấy từ HTML). Dạng không chia bước thì không hiện nút.

## Kế hoạch

**Chặng 0 — đã xong (nhánh này):**
- Tự dựng cho mọi dạng; nút giáo viên trên trang bài.
- `publish-bai-tap-mau.mts` chép thêm trường `trinh_chieu`.

Việc còn lại: deploy theo quy trình thường; thầy bấm thử bằng tài khoản giáo viên trên một bài thật (154 hoặc bài sắp dạy).

**Chặng 1 — dùng thật 1–2 tuần (thầy):**
- Chiếu trên lớp, ghi chỗ vướng (dòng quá dài, bước cần tách, câu hỏi lớp chưa hợp).
- Đo bằng phản hồi của thầy và số dạng được chiếu. Chưa log sự kiện, tránh thêm round-trip.

**Chặng 2 — làm giàu theo lịch dạy, không làm hàng loạt:**
1. Thêm một bước vào skill `soan-bai-tap-mau` / `cap-nhat-dang-bai-tap`: với dạng khí, nhiệt, mạch điện…, soạn `trinh_chieu`:
   - `bang`: bảng trạng thái ①② và ô `can_tim`;
   - `buoc[i].hoi` viết lại cho hợp hỏi cả lớp;
   - `buoc[i].dong` có `bang:{"p.1":"71"}` để điền bảng theo dòng;
   - `bay`.
   Mẫu chuẩn: `mau-ong-thuy-ngan.tsx`.
2. Làm theo chương sắp dạy, mỗi đợt 1 chương:
   - đầu tiên L12 Ch.2 (khí lí tưởng — hợp bảng ①② nhất);
   - rồi L10 Ch.2–3, L11 Ch.4 dòng điện.
   Các dạng còn lại vẫn dùng bản tự dựng.
3. Mỗi dạng sửa: chạy `--xem-thu`, xem `/dev/btm-trinh-chieu?f=btm` ở 1280×720 sáng/tối, rồi đăng.

**Chặng 3 — công cụ trên lớp: ĐÃ LÀM 23/11/2026 (làm trước chặng 1 để bản deploy đầu đã đủ đồ nghề như chiếu lý thuyết):**
- Bút vẽ / bút dạ / tẩy, tách từ `LessonPresenter` thành component dùng chung.
- Phóng to ±.
- Ghi chú lớp (phím N), đọc qua skill `xem-ghi-chu-lop`.
- Link sâu `#chieu-btm-<i>` để mở thẳng một dạng.

**Không làm:**
- Mở cho học sinh: bản cho HS đã là "giải cùng hình" từng bước.
- Ghi DB lúc chiếu.
- Soạn `trinh_chieu` hàng loạt bằng AI ngoài: câu hỏi lớp cần giọng thầy.
