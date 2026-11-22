# Brief: dựng bản chiếu trên lớp cho MỘT bài L11 (bước 1–5 + 8a của skill)

Worktree: <worktree của phiên> . Làm mọi việc trong worktree này, KHÔNG cd ra checkout chính, KHÔNG commit (phiên chính commit), KHÔNG push/deploy/ghi DB.
Thầy Thạch dạy Vật lí THPT, chiếu bài trên tivi 50" (lớp xa 6–8 m). Viết tiếng Việt có dấu, giọng ngắn gọn.

## Đọc trước (theo thứ tự, đừng đọc thừa)
1. `.claude/skills/ban-chieu-tren-lop/SKILL.md` — làm đúng bước 1–5 và phần chép-web của bước 8.
2. Bài mẫu `content/lesson-samples/l11-dien-the/`: `tren-lop.src.html` (khối `<head>`/CSS/JS cuối dùng lại NGUYÊN, gồm khối `:root` token nền sáng và `<link>` font `/fonts/be-vietnam-pro/be-vietnam-pro.css`), `build_tren_lop.py`, `build_qr.mts`, `tren-lop-ghi-chu.html`, và mục "Đã xử lý" cuối `thu-lop-ao/gop-y.md` (lỗi hay gặp).
3. Ruột tập `scripts/ruot-tap/l11-bai<N>.mjs` — trang 1–5 là học trên lớp, mã ô `t·k`. Chép câu A–D Y CHỮ Tập. Đầu file ghi nguồn nội dung.
4. `content/lesson-samples/<slug>/theory.html` — đọc theo đoạn (grep), không đọc hết. Hình SVG lấy từ đây qua `<!--FIGn-->` (n = thứ tự thẻ `<svg` trong theory.html, đếm từ 1).
5. Clip: `content/thi-nghiem/video-khung/<id>.json` của bài (id liên quan trong theory.html, `data-exp=`/`<!--video:`). Mốc dừng lấy từ khung JSON + engine (`~/.venvs/video-thi-nghiem/bin/python3`, engine ở `scripts/video-thi-nghiem/`, xem cách bài mẫu làm qua `git log -p --follow -- content/lesson-samples/l11-dien-the/tren-lop.src.html | grep -n data-bat | head`), cách đầu cảnh/chuyển động ≥ 0,3 s; kiểm khung hình thật bằng ffmpeg trích 1 khung tại mỗi mốc dừng (tải mp4 về scratchpad), XEM ảnh để chắc không dừng vào khung trắng/lộ đáp án. Bài không có clip phù hợp thì bỏ màn clip, đừng gượng.
   PhET: chỉ dùng sim có thật cho bài (theory.html thường đã nhúng); link dạng `https://phet.colorado.edu/sims/html/<sim>/latest/<sim>_all.html?locale=vi`.

## Làm ra (trong `content/lesson-samples/<slug>/`)
- `tren-lop.src.html`: 6 điểm dừng ≈ 30 phút + màn đề cuối tiết (QR) + màn "Về nhà". Khoảng 16–24 màn. Mỗi màn một ý; mỗi màn có `.tap` `tr.X · ô t·k` khớp Tập. Câu dự đoán mở bài → đáp án ở màn "Quay lại …" cuối tiết. Hình + đáp án cạnh nhau (`.hai`). Lớp `.fN` riêng cho từng hình với chiều cao + phóng chữ nhãn (`.fN svg text{font-size:…}`) để chữ hình ≥ 0,7 chữ thường. JS cuối file: chép nguyên của mẫu (regex `/^(a|r|m5c)/` tô phương án đúng — đặt id đáp án theo quy ước đó hoặc sửa regex cho khớp).
- `build_tren_lop.py`: như mẫu nhưng thay slug, bỏ `assert len(svgs)==3`, thay vòng FIG bằng: mọi `<!--FIGn-->` có trong src → svgs[n-1]. Chép bản web noindex sang `public/dev/tren-lop/<slug>.html` và `<slug>-ghi-chu.html`.
- `build_qr.mts`: như mẫu, đổi mã đề + mục; chạy `npx tsx content/lesson-samples/<slug>/build_qr.mts content/lesson-samples/<slug>/tren-lop-qr.svg` → phải in `khớp: true`.
- `tren-lop-ghi-chu.html`: cùng khung mẫu (chuẩn bị tivi F11/tải clip, biểu quyết, đi theo Tập, bảng điểm dừng phút · trang · ô · lời thầy, phiếu giấy dự phòng, thiếu/dư giờ, sau buổi dạy).

## Kiểm máy (bước 5) — bắt buộc trước khi báo
`python3 content/lesson-samples/<slug>/build_tren_lop.py` rồi
`node content/tren-lop-tien-do/kiem-tren-lop.mjs <slug>`
(1280×720 và 1920×1080, mở hết đáp án/bước clip; ✗ = màn tràn hoặc chữ hình < 0,7 chữ thường; katex-error; 375px). Sửa tới khi chỉ còn ✗ có lý do (ghi lý do trong báo cáo). Muốn xem bằng mắt: thêm `--chup` → ảnh từng màn ở `thu-lop-ao/chup/` (thư mục này KHÔNG commit). Không cần mở trình duyệt khác.

## Không được
Sửa `theory*.html`, `bundle.json`, đề kiểm tra, `features/lessons/tren-lop.ts` (phiên chính thêm dòng). Ruột tập `.mjs` chỉ sửa khi thật cần (Tập lệch màn) và PDF giữ nguyên số trang: `node scripts/ruot-tap/l11-bai<N>.mjs` trước/sau, so số trang.

## Báo cáo (≤ 12 dòng)
số màn · danh sách màn (id: ý) một dòng · điểm dừng/phút · clip dùng + mốc · PhET · kết quả kiểm máy (dòng ĐẠT/LỖI + ✗ còn lại có lý do) · chỗ Tập lệch/khó · file đã tạo/sửa.

## Lỗi lớp ảo hay bắt — tránh ngay từ đầu (từ bài 21, 22)
Tham khảo bài đã xong trọn: `content/lesson-samples/l11-cuong-do-dong-dien/` (build_tren_lop.py có dấu `<!--TAP:ten-->` lấy hình của Tập; mục "Đã xử lý" cuối thu-lop-ao/gop-y.md).
- Ô đề cuối tiết trong Tập là bảng "N câu chiếu trên lớp" lệch đề 20 câu → sửa như bài 20 ("Đề <mã> (20 câu, cuối tiết)": Điểm …/20 · Câu sai · Câu đoán mò), PDF giữ số trang.
- Chữ in sẵn trong Tập gợi ý đáp án câu biểu quyết; câu nói "A/B/C/D" mà chỉ có 3 phương án; ô trống có hai đáp án hợp lệ.
- Số liệu Tập lệch clip (ghi "cỡ"); ô không điểm dừng nào nhắc → ghi rõ ở màn "Về nhà"; một điểm dừng dồn > 20 ô trong 7 phút.
- Hình web vẽ cho nền tối (#38bdf8, #f87171…) → đổi sắc đậm cho nền trắng bằng CSS bản chiếu.
