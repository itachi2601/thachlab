---
name: dang-tin-tuc-vat-ly
description: Tìm, kiểm chứng và đăng TIN TỨC Vật lí / học thuật (khám phá mới, giải Nobel, thí nghiệm lớn, tin thi cử – chương trình, học bổng, Olympic Vật lí) lên mục Tin tức (/tin-tuc) của thachlab, mỗi tin ngắn, viết lại bằng lời mình, có link nguồn và gắn với bài học lớp 10–12. Dùng khi thầy nói "cập nhật tin tức vật lý", "đăng tin vật lý tuần này", "tìm tin học thuật mới", "đăng tin này lên thachlab", "làm bản tin Vật lí". KHÁC blog (bài kiến thức dài, content/blog/*.md) và soan-bai-ly-thuyet-tuong-tac (bài học). Tìm + soạn + dry-run chạy được trên cloud; GHI DB phải chạy trên Mac.
---

# Đăng tin tức Vật lí & học thuật

Đầu ra: file `scripts/data/tin-tuc/<yyyy-mm-dd>-<slug>.json` (mẫu: `_mau.json.txt`). Đăng bằng `scripts/dang-tin-tuc.mts` → bảng `posts` (RPC `create_post_with_targets`, như trang `/quan-tri/bai-dang`) → hiện ở `/tin-tuc`. **Trang `/tin-tuc` đọc Supabase lúc chạy nên đăng xong là thấy, không cần `deploy.sh`.**

Tin ≠ Blog: tin ngắn (80–200 chữ, hiển thị thẳng trong thẻ). Muốn phân tích sâu → viết bài `content/blog/*.md`, không dùng skill này; bài giải thích hiện tượng đời sống cho HS → skill `vat-ly-quanh-ta`.

## Quy trình

1. **Chốt phạm vi.** Thầy không nói gì thì lấy: 7 ngày gần nhất, 3–5 tin. Nhóm tin: (a) khám phá/thí nghiệm Vật lí (b) Nobel, giải thưởng (c) công nghệ ứng dụng liên quan chương trình THPT (d) tin học thuật Việt Nam: thi tốt nghiệp, đề minh hoạ, tuyển sinh, IPhO/APhO, học bổng.
2. **Tìm.** `WebSearch` + `WebFetch` (nạp qua ToolSearch nếu chưa có). Ưu tiên nguồn gốc: tạp chí/ĐH/viện (Nature, Science, APS Physics, CERN, NASA, ESA, phys.org đối chiếu bài gốc), Bộ GD&ĐT / báo chính thống cho tin trong nước. Mỗi tin cần **link bài đăng cụ thể**, không link trang chủ.
3. **Kiểm chứng (bắt buộc, trước khi viết).**
   - Số liệu, tên giải, ngày: đối chiếu ≥ 2 nguồn, hoặc 1 nguồn gốc (bài báo khoa học/thông cáo của chính tổ chức).
   - Tin kiểu "phá vỡ định luật vật lí", "năng lượng vô hạn", "chưa phản biện (preprint)" → bỏ, hoặc nói rõ trong tin đây mới là kết quả sơ bộ.
   - Tin trong nước (lịch thi, quy chế): lấy từ văn bản/trang chính thức, ghi ngày ban hành.
   - Không chắc → loại, báo thầy "đã loại vì…". Không đoán.
4. **Chống trùng.** Xem tiêu đề các tin đã có trong `scripts/data/tin-tuc/` và `/tin-tuc`; script đăng cũng tự chặn trùng tiêu đề/link nguồn trong DB.
5. **Viết** (`body_html`), **bằng lời mình, không chép nguyên văn nguồn** (bản quyền; tối đa một trích dẫn dưới 15 từ, có ngoặc kép + ghi nguồn). Không dùng vai "thầy" (như bài lý thuyết). Khung 4 phần ngắn:
   - **Điều gì mới** — 1–2 câu, có số liệu/đại lượng cụ thể + đơn vị.
   - **Vì sao đáng chú ý** — 2–3 câu cho học sinh 14–18 tuổi, câu ngắn, thuật ngữ lạ phải giải nghĩa ngay.
   - **Gắn với bài học** — 1 câu: "Lớp 12 · Chương Vật lí hạt nhân" (tra `public/data/catalog.json` cho đúng tên chương; không có liên hệ thật thì bỏ dòng này, đừng gán gượng).
   - **Nguồn** — `<a href="…" target="_blank" rel="noopener noreferrer">Tên nguồn</a>`, kèm ngày đăng của nguồn. `body_html` PHẢI chứa đúng `source_url`.
   - Công thức dùng `$…$` (KaTeX), `<`/`>` viết `\lt`/`\gt`. Chỉ HTML thuần: `<p>`, `<strong>`, `<ul>`, `<a>`. Không `<script>`, không base64.
   - Ảnh: không tự chèn ảnh lấy từ nguồn (bản quyền + tốc độ tải, xem AGENTS.md mục "Đăng nội dung"). Có ảnh tự làm → `.webp` ≤150 KB, rộng ≤1200px.
6. **Gắn đích.** `subject_code` = `vat-ly` (mặc định; tin Hoá/Sinh thì `hoa-hoc`/`sinh-hoc`). `class_ids` = `[]` (toàn trường) cho tin chung; tin riêng một khối thì lấy id từ `catalog.json` (`classes[]`: lớp 10 = 16, lớp 11 = 17, lớp 12 = 18, KHTN 9 = 15). `content_type` = `thong_bao`.
7. **Dry-run.** `npx tsx scripts/dang-tin-tuc.mts` — kiểm độ dài (200–3500 ký tự), link https, có link nguồn trong thân, không script/base64, trùng DB. Sửa tới khi hết ✗.
8. **Đưa thầy duyệt**: bảng tiêu đề · nguồn · 1 dòng tóm tắt · tin đã loại + lý do. Thầy duyệt là đăng (không PR, không hỏi thêm).
9. **Đăng (Mac).** Phiên Mac chạy thẳng; phiên cloud chưa có khoá DB thì in lệnh:
   ```
   cd /Users/MAC/Projects/thachlab && git pull origin main
   npx tsx scripts/dang-tin-tuc.mts --yes
   ```
   Script ghi `posted_id` vào file JSON (đăng lại sẽ bỏ qua) và in tin đang HIỆN hay ẨN. Nếu ẨN → bật Hiện ở `/quan-tri/bai-dang`. Xoá/ẩn tin sai cũng ở trang đó.
10. **Commit** file JSON vừa đăng (`git add scripts/data/tin-tuc/<file>` rồi `git commit -- <path>`).

## Cập nhật định kỳ
Muốn bản tin hằng tuần: dùng skill `schedule` đặt lịch (vd thứ Hai 7h) chạy bước 1–8 rồi dừng ở bước duyệt; **không tự đăng không qua duyệt**.

## Câu tốt / câu xấu
- ✓ "Máy dò LIGO ghi thêm sự kiện hợp nhất hai lỗ đen; tín hiệu kéo dài chưa tới 1 giây." + giải nghĩa sóng hấp dẫn bằng 1 câu.
- ✗ "Các nhà khoa học vừa làm rung chuyển nền vật lí!" — giật tít, không có đại lượng, không kiểm chứng được.
- ✗ Dịch nguyên đoạn bài báo; link về trang chủ báo; tin từ blog không rõ nguồn gốc.

## Nhật ký rút kinh nghiệm
- 2026-10-06 · Tạo skill. `/tin-tuc` (bảng `posts`, ngắn, theo lớp/môn) khác `/blog` (Markdown tĩnh trong `content/blog`, cần deploy) → tin ngắn dùng skill này, bài sâu viết blog. Chưa chạy ghi thật lần nào: lần đầu đăng, xem lại tin HIỆN/ẨN và `body_html` hiển thị ra sao ở `/tin-tuc` (trang dùng `whitespace-pre-wrap`: script đã chặn xuống dòng trong `body_html`, viết liền một dòng).
