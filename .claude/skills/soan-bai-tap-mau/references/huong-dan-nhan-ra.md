# Hướng dẫn soạn bài tập mẫu cho MỘT bài (dành cho subagent — nhân ra cả chương)

Mẫu hoàn chỉnh đã đăng: **bài 57** — `scripts/data/bai-tap-mau/build-hinh-57.py` (đọc toàn bộ file này trước, nó là chuẩn), `57.json` (kết quả).
Thư viện: `.claude/skills/soan-bai-tap-mau/scripts/dung.py` (sol/tbl/ball/smil/write/tu_luan_tu), `hinh.py` (fig/arrow/dim/arc/axes/poly/ground…, màu theo `svg_lib.py`). Đọc `SKILL.md` cùng thư mục (quy tắc phong cách) và `docs/AI-TUTOR.md` mục 9.1/9.3/9.5.

## Việc phải làm cho bài `<ID>`
1. Đọc lý thuyết của bài: `public/data/lessons/<ID>.json` (mục `ly_thuyet`: ký hiệu, giá trị g, công thức, thứ tự kiến thức) — dạng bài soạn phải **khớp đúng ký hiệu/quy ước của lý thuyết** bài đó. Đọc **toàn bộ** ví dụ cũ ở `scripts/data/bai-tap-mau/old/<ID>.json` (có đề + lời giải + ảnh `<img>`).
2. Chốt **4–6 dạng**, xếp **DỄ → KHÓ** (dạng sau dùng lại cách của dạng trước), mỗi dạng = một kiểu bài học sinh gặp lặp lại. Nhãn `Dạng k · Dễ|Trung bình|Khó · <tên>`.
3. Ví dụ cũ nào hợp một dạng → **biên tập lại thành dạng đó** (đổi số cho đẹp/thực tế, đề rõ nghĩa: điểm đo, mốc, chiều dương, cùng/khác độ cao…). Ví dụ cũ còn lại → gom vào `tu_luan` bằng `tu_luan_tu(old, order, muc)` xếp dễ→khó (giữ nguyên lời giải gốc, KHÔNG sửa).
4. Mỗi dạng cần: `label`, `topic` (**tên YCCĐ con nguyên văn** từ `scripts/data/question-topics.json`, đúng `lesson_id` của bài; ưu tiên con, cha chỉ khi bài không có con), `problem_html` (đề chữ, LaTeX `$…$`; `<`/`>` viết `\lt`/`\gt`), `BUILD[i](k)` (k=0: **mô phỏng hiện tượng nằm DƯỚI đề**, chạy một lần khi bấm; k=2: hình dữ kiện tĩnh cho phần phân tích), `ANALYSIS[i]` (bảng **Câu trong đề | Dữ liệu | Kiến thức liên quan**, mỗi hàng trích một cụm của đề, có hàng ⚠ điều kiện áp dụng; cột 3 chỉ công thức/ý, KHÔNG ghi số đáp án), `SOLS[i]` = `sol(recall, steps, finals, note)` (mỗi bước một khối, **mỗi công thức một dòng**, tách công thức chữ / thế số / kết quả; ô đáp số; "Nhận dạng").
5. Viết script `scripts/data/bai-tap-mau/build-hinh-<ID>.py` theo mẫu 57, kết thúc bằng `write(J, <ID>, "<tên bài>", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)`. Chạy → sinh `scripts/data/bai-tap-mau/<ID>.json`. Helper riêng của bài đặt trong chính file build (hoặc `scripts/data/bai-tap-mau/hinh_<ID>.py`), **không sửa** `dung.py`/`hinh.py`.

## Mô phỏng & hình (quan trọng)
- Hình **tính thật từ công thức** (mẫu cách đều thời gian, nội suy tuyến tính), không vẽ tay quỹ đạo/đồ thị. Chuyển động thẳng: vật chạy dọc trục có thước; đồ thị: điểm chạy trên đồ thị + vạch đứng; rơi tự do: vật rơi kèm các vị trí cách đều thời gian…
- **Chạy MỘT lần khi bấm**: dùng `ball()`/`smil()` (begin="indefinite", fill="freeze"); `fig()` tự thêm nút. Chạy đúng thời gian thật hoặc ghi "chạy chậm k lần" trong chú thích. Đối tượng phải **đúng vật lí** (ví dụ vật mang vận tốc của phương tiện: xe + hàng cùng chạy).
- **Không lộ đáp số** trong hình đề (chỉ dữ kiện đề cho, dấu "?" cho đại lượng cần tìm). Bài ngược chạy một lần "thử" hợp lí.
- Bố cục: mỗi hình ≤ ~8 nhãn, chữ ≥ 12, viewBox đủ chỗ cho thước đo (đừng đặt nhãn dưới mặt đất ngoài viewBox), nhãn không đè mũi tên/quỹ đạo, không chữ cắt mép. Marker mỗi hình một tiền tố (`defs(p)`).
- Đồ thị cần trục có đơn vị, vạch chia, nhãn đại lượng; dùng đúng màu quy ước bài lý thuyết.

## Kiểm (bắt buộc, tự làm trước khi báo xong)
- `npx tsx .claude/skills/soan-bai-tap-mau/scripts/validate.mts scripts/data/bai-tap-mau/<ID>.json` phải qua (review.checked sẽ false → lỗi duy nhất được phép; phiên chính sẽ đặt true sau kiểm chéo).
- **Tự giải lại mọi dạng bằng Python** (số học độc lập với lời giải) và ghi so sánh; số liệu thực tế (không v₀ = 70 km/h cho người nhảy xa…), đẹp (tròn, căn đẹp).
- Xem hình bằng mắt: `python3 .claude/skills/soan-bai-tap-mau/scripts/xem-thu.py scripts/data/bai-tap-mau/<ID>.json <thư mục scratchpad của bạn> [--dang 1,3]` rồi **Read các PNG** (đề + mô phỏng ở khung CUỐI + phân tích + lời giải). Sửa lỗi bố cục/chữ cắt/nhãn đè rồi chụp lại (mỗi hình ít nhất 1 lần sau sửa). KHÔNG dùng browser pane (nhiều agent cùng chạy sẽ đụng nhau).
- Tuân `docs/QUY-TAC-THIET-KE.md` (C1/C4/H5/B3/N7, B4).

## Ranh giới
- CHỈ tạo/sửa: `scripts/data/bai-tap-mau/<ID>.json`, `build-hinh-<ID>.py`, `hinh_<ID>.py` (tuỳ chọn) và file tạm trong scratchpad. KHÔNG sửa file chung (`dung.py`, `hinh.py`, `SKILL.md`, `globals.css`, `AGENTS.md`, `STATE.md`…), KHÔNG chạy `publish-*`, KHÔNG ghi DB, KHÔNG `git add/commit`, KHÔNG deploy, KHÔNG đụng bài khác. Không dùng vai "thầy/cô" trong nội dung.

## Báo cáo cuối (ngắn, ≤ 25 dòng)
Danh sách dạng (nhãn + mức + topic); ví dụ cũ nào đã biên tập thành dạng nào, nào vào tự luận (số lượng); kết quả tự giải lại (khớp/lệch); lỗi hình đã sửa; điều còn nghi ngờ cho phiên chính.
