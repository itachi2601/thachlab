# Prompt + kế hoạch: triển khai đợt 1 "mẹo vài chữ" cho 17 bài L10–12

Gửi cho một phiên Claude Code **trên Mac** (cần đăng DB). Dán nguyên khối từ dòng `---BẮT ĐẦU PROMPT---`.
Chi tiết từng chỗ sửa nằm ở `docs/DE-XUAT-TU-KHOA-NEN-2026-10-26.md` (mục 3 ★, mục 4 lỗi) — phiên nhận không cần rà lại.

## Phân công agent (theo mục "Phân công mô hình" trong AGENTS.md)

| Việc | Ai | Lý do |
|---|---|---|
| Điều phối, soạn chữ mẹo + sửa `theory.src.html`, Trả bài, Mang về | **phiên chính, model Opus** | nội dung HS nhìn thấy, phải cân vật lí từng chữ; không giao Cursor/Gemini |
| Soát từng bài trước đăng (mẹo ↔ 🔑 ↔ Trả bài khớp 1–1, không lộ đáp án trước quiz, 375px) | subagent **`kiem-code`** (Sonnet) | quy định: nội dung lý thuyết sắp đăng phải qua kiem-code |
| Build + đăng `cap-nhat-ly-thuyet.sh`, kiểm lại trên web | phiên chính, **tab terminal** | lệnh ghi DB, cần `.env.local`, thầy theo dõi được |
| Không cần `kien-truc-du-lieu`, `nhap-du-lieu-hoc-sinh` | | không đụng schema, không có dữ liệu HS |

Chạy 2 lô (lô 1: L12 8 bài, lô 2: L10 + L11 9 bài); chốt lô 1 trên web rồi mới mở lô 2 — lỗi lặp của lô 1 ghi vào prompt lô 2.

---BẮT ĐẦU PROMPT---

Việc: thêm "mẹo vài chữ" (🧠) lên trên dòng từ khoá 🔑 ở các mục đã được thầy duyệt, sửa 6 lỗi 🔑, đăng lại 17 bài lý thuyết L10–12.
Đọc trước, chỉ các file này: `docs/DE-XUAT-TU-KHOA-NEN-2026-10-26.md` (danh sách ★ mục 3 và lỗi mục 4 — đó là spec, không rà lại),
`docs/QUY-TAC-THIET-KE.md` mục G1 và nhóm C, `docs/MAU-NEN-SANG.md` (token màu), `docs/memory/project_thachlab_cap_nhat_ly_thuyet.md`.
Nguồn bài: `content/lesson-samples/<slug>/theory.src.html` → build theo cách của thư mục đó (`build_bundle.py` hoặc script sẵn có) → `theory.html`.

## Quyết định đã chốt (không hỏi lại)
- Chữ mẹo: **đậm, viết hoa chữ đầu mỗi chữ, ngăn bằng " – "** (ví dụ `Nhỏ – Loạn – Đập`); không viết HOA toàn bộ (C-nhóm: chữ hoa toàn dòng đọc chậm trên điện thoại). Thầy đổi ý thì chỉ sửa CSS `text-transform`.
- Dòng 🔑 cũ **giữ nguyên** ngay dưới mẹo. Mẹo là tầng nhớ, 🔑 là tầng nghĩa.
- Mỗi bài sửa: thêm dòng "N hình = cả bài" cuối khung Mang về (N = số mục kiến thức, ≤ 5; mỗi mục một hình ảnh cụ thể đã có trong bài: thí nghiệm, vật đời thường, hình SVG).
- Chữ mẹo lấy **đúng** bảng đề xuất; chỉ đổi khi sai vật lí hoặc hai mẹo trong cùng khối lớp trùng chữ cho ý khác — khi đổi, ghi lý do vào `docs/BANG-MEO-TU-KHOA.md`.

## Mẫu HTML (thêm vào mọi chỗ ★)
```html
<p class="tl-meo">🧠 <b>Nhỏ – Loạn – Đập</b></p>
<p class="tl-key">🔑 Kích thước bé xíu · Hỗn loạn không ngừng · Va chạm gây áp suất</p>
```
CSS một lần vào nơi đang chứa `.tl-key` (kiểm `grep -rn "tl-key" app/ styles/ content/`): `.tl-meo` cỡ chữ bằng `.tl-key` + 2px, màu token nhấn nền sáng,
`letter-spacing: .02em`, không nền. Không thêm font. Kiểm 375px: mẹo 4–5 chữ phải nằm trên MỘT dòng; nếu xuống dòng thì bỏ dấu " – " thành " · ".

## Việc trong từng bài (checklist, làm đủ mới tính xong bài)
1. Thêm `tl-meo` ở đúng mục theo bảng ★. Nếu mục có quiz hỏi cùng ý **đứng ngay sau** 🔑 → chuyển khối 🔑+mẹo xuống sau quiz (quy tắc lộ đáp án đã ghi trong skill).
2. Trả bài (mục IV): đáp án của câu tương ứng mở đầu bằng chữ mẹo, rồi mới tới từ khoá cũ. Thêm **một** câu Trả bài dạng "Chữ <X> trong mẹo … nghĩa là gì?" nếu mục chưa có câu nào hỏi đủ/thiếu ý.
3. Mang về: dòng của mục đó bắt đầu bằng chữ mẹo; thêm dòng cuối "N hình = cả bài: …".
4. Sửa lỗi mục 4 của spec nếu bài có (dao-dong-dieu-hoa soạn 🔑 cho cả 5 mục; khí lí tưởng đủ 4 ý; phóng xạ đủ 4 tia; hai bộ bước động lực học về một bộ; áp suất–động năng dùng lại Nhỏ–Loạn–Đập; bai-tap-dao-dong tách hai 🔑 dính).
5. Ghi mẹo vào `docs/BANG-MEO-TU-KHOA.md` (file mới, mỗi dòng: `lớp · bài · mục · mẹo · ý từng chữ · bài khác dùng lại`). Mẹo dùng chung (Vẽ–Kể–Viết–Chiếu; Ba cùng–Một ngược–Một khác; Nhỏ–Loạn–Đập; Quay–Đổi–Sinh; Tiếp–Ra–Vào–Mau / Tiếp–Kín–Không cắt–Mau) phải **y hệt từng chữ** ở mọi bài.
6. `python3 scripts/lint_theory.py <theory.html>` (hoặc lint sẵn có của thư mục) sạch; `lint_do_dai` không vượt hạn mức — mẹo thêm ≈ 5 từ/mục, nếu bài đã sát hạn mức thì cắt một câu dẫn gần đó, không cắt 🔑.
7. Chụp xem thử 375px (Chrome headless như skill `soan-bai-ly-thuyet-tuong-tac` làm) cho 2 bài đầu mỗi lô; các bài sau chỉ kiểm bằng lint + đọc.
8. Giao `kiem-code` soát bài theo 5 điểm: (a) mỗi chữ mẹo tra ngược ra đúng một ý trong 🔑; (b) mẹo không lộ đáp án quiz đứng sau; (c) chữ mẹo xuất hiện ở Trả bài và Mang về; (d) mẹo dùng chung y hệt bài khác trong cùng lô; (e) lỗi mục 4 đã sửa. Prompt cho kiem-code chỉ gửi đường dẫn file + 5 điểm, không dán nội dung.
9. Commit theo đường dẫn: `git commit -- content/lesson-samples/<slug>/ docs/BANG-MEO-TU-KHOA.md`, mô tả ghi mã G1, C-nhóm.
10. Đăng: tab terminal, `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/<slug>/theory.html <lesson_id>` (lesson_id tra `docs/memory/project_thachlab_cap_nhat_ly_thuyet.md` hoặc bảng `lessons` qua REST theo slug). Chỉ ghi `ly_thuyet`, KHÔNG `upload-lesson.mts`. Mở trang bài trên web (tài khoản đang đăng nhập) kiểm mẹo hiện đúng, rồi mới sang bài kế.

## Lô và thứ tự
- Lô 1 (L12, chương 1–2 trước vì đang dạy): thuyet-dong-hoc-phan-tu → ap-suat-dong-nang → su-chuyen-the → cam-ung-dien-tu → khai-niem-tu-truong → luc-tu-cam-ung-tu → dong-dien-xoay-chieu → may-phat-dien-bien-ap. Chốt lô 1 trên web, ghi "lỗi lặp lô 1" rồi mới mở lô 2.
- Lô 2 (L10 rồi L11): dinh-luat-3-newton → dinh-luat-2-newton + giai-bai-toan-dong-luc-hoc (một mẹo) → lam-quen-voi-vat-li → luc-ma-sat → do-dich-chuyen-quang-duong → chuyen-dong-nem → dao-dong-dieu-hoa (soạn 🔑 mới) → giao-thoa-song → tat-dan-cuong-buc → song-dung → khai-niem-dien-truong → cuong-do-dong-dien.
- Bỏ qua thư mục `l12-ung-dung-cam-ung.cu` (bản cũ). Mục ○ của spec KHÔNG làm đợt này.

## Ràng buộc
- Chỉ sửa file trong `content/lesson-samples/<slug>/`, `docs/BANG-MEO-TU-KHOA.md`, một chỗ CSS. Không đụng `bundle.json`, quiz 20 câu, bài tập mẫu, migration.
- Script/batch ghi file nguồn → `git add` ngay sau khi chạy, trước mọi pull/merge. Không `git commit -a`, không `git stash`.
- Đăng DB ban ngày được (mỗi lần một dòng `lessons`), không phải việc hàng loạt sau 22h.
- Không gọi API ngoài, không Batch API: soạn mẹo trực tiếp trong phiên.
- Mỗi lô xong: báo một lần — bài nào đã lên web, bài nào treo và vì sao, lệnh kiểm. Không báo tiến độ giữa chừng.

## Kết thúc
1. Ghi `docs/STATE.md` (chỉ thêm dòng): "Mẹo từ khoá đợt 1: 17 bài đã đăng <ngày>; đợt 2 (○) chờ số liệu Trả bài một chương".
2. Thêm quy tắc vào `.claude/skills/soan-bai-ly-thuyet-tuong-tac/SKILL.md` mục "Ít chữ — nhớ bằng từ khoá" (chỉ thêm, không viết lại):
   "Mục có 3–5 ý song song → thêm dòng 🧠 mẹo 3–5 chữ đơn, đậm, hoa chữ đầu, đặt trên 🔑; chữ mẹo lặp ở Trả bài và Mang về; tra `docs/BANG-MEO-TU-KHOA.md` trước khi đặt mẹo mới, cùng ý thì dùng cùng chữ; cuối Mang về có dòng 'N hình = cả bài'."
   Ghi mục `## Nhật ký rút kinh nghiệm` của skill: `- 2026-MM-DD · <lỗi lặp của đợt> → <quy tắc>`.
3. Rút kinh nghiệm (3–6 dòng) trong câu trả lời cuối + ghi vào skill/memory theo AGENTS.md; `/ban-giao`.

---KẾT THÚC PROMPT---

## Cách đo sau một chương (việc của phiên sau, không phải phiên này)
So điểm 6 câu Trả bài và câu quiz "đếm đủ N ý" của HS giữa bài đã có mẹo và bài chưa có; nếu không khác biệt thì dừng đợt 2.
