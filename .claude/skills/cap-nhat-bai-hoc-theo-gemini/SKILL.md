---
name: cap-nhat-bai-hoc-theo-gemini
description: Quy trình trọn gói làm việc với Gemini (thầy dán tay vào gemini.google.com, không API) để CẬP NHẬT một bài thachlab — (1) Gemini đóng vai học sinh đọc bài lý thuyết và góp ý, Claude kiểm từng góp ý rồi sửa tối thiểu theory.src.html; (2) Gemini nháp 4 dạng bài tập mẫu theo hệ bắc cầu 4 cấp, Claude kiểm số liệu, viết lại theo phong cách thầy, dựng mô phỏng, kiểm chéo, rồi đăng. Hai chế độ — "/gemini-gui <bài|chương>" xuất file để thầy dán vào Gemini; "/gemini-nhan <bài>" xử lý JSON Gemini trả về. Dùng khi thầy nói "gửi bài này cho Gemini", "xuất file cho Gemini", "Gemini đã trả kết quả", "sửa lý thuyết/bài tập mẫu theo Gemini", "xử lý góp ý học sinh ảo". Soạn/sửa/build chạy được trên cloud; ĐĂNG lên DB phải chạy trên Mac và thầy duyệt trước.
---

# Cập nhật bài học theo Gemini (thầy chốt 8/10/2026)

Thầy có Gemini Pro trên web, **không dùng API**. Điểm nối duy nhất là các thư mục trong repo. Claude không gọi Gemini; thầy sao chép–dán.

## Thư mục (mỗi bài một bộ)

`content/lesson-samples/<bài>/gemini/`
| Ngăn | Ai ghi | Nội dung |
|---|---|---|
| `gui/` | Claude (script `--xuat`) | `<vai>-1-quiz-mu.txt`, `<vai>-2-doc-day-du.txt`, `<vai>-3-bai-tap-mau.txt` để thầy dán |
| `nhan/` | Thầy (hoặc Claude lưu khi thầy dán JSON vào chat) | `hoc-sinh-<yeu|trung-binh|kha>.json`, `bai-tap-mau.json`, tuỳ chọn `dap-an-that.json` |
| `da-xu-ly/` | Claude | `so-quyet-dinh.json` (từng góp ý: chap_nhan/tu_choi/hoi_thay + ghi chú), bản bài tập mẫu đã kiểm, báo cáo ngắn |

Điều phối nhiều bài: `content/gemini/hang-doi.md` (trạng thái `chua-gui → da-gui → da-nhan → da-sua → cho-duyet → da-dang`). Cập nhật bảng này ở cuối mỗi chế độ.
Prompt gốc nằm một nơi: `references/PROMPT-GEMINI-HOC-SINH.md` (skill này) và `soan-bai-tap-mau/references/PROMPT-GEMINI-BAI-TAP-MAU.md`. Không chép sang chỗ khác.

## Chế độ 1 — `/gemini-gui <bài | chương>`

1. Xác định thư mục bài, tên bài, lớp. Nhiều bài (cả chương): lặp từng bài.
2. Xuất file: `npx tsx scripts/gemini-phan-hoi.mts --bai <thư-mục> --ten "<tên bài>" [--vai trung-binh] --xuat` (đợt lớn chỉ vai `trung-binh`).
3. Hướng dẫn thầy (ngắn): mỗi vai một cuộc chat mới trên gemini.google.com, dán lần lượt file 1 → 2 → 3 (file 3 chỉ cần ở **một** vai, nên vai `trung-binh`); lưu JSON tin nhắn 2 thành `nhan/hoc-sinh-<vai>.json`, tin nhắn 3 thành `nhan/bai-tap-mau.json`; hoặc dán JSON vào chat để Claude lưu. Đợt lớn: gợi ý lưu prompt vai vào một Gem.
4. Ghi `da-gui` vào `hang-doi.md`.

## Chế độ 2 — `/gemini-nhan <bài>`

**A. Lý thuyết** (khi có `nhan/hoc-sinh-*.json`)
1. Gộp: `python3 .claude/skills/cap-nhat-bai-hoc-theo-gemini/scripts/gop-phan-hoi.py content/lesson-samples/<bài>`. Góp ý được ≥2 vai nêu và mức `chặn` xếp trước; in phân bố đáp án quiz (so với `nhan/dap-an-that.json` nếu có: `{"cau1":"C",…}`).
2. **Kiểm từng góp ý, không sửa mù** (Gemini có thể sai vật lí hoặc bịa chỗ khó): chấp nhận (đối chiếu trích dẫn với `theory.src.html`; trích sai vị trí → nghi bịa) · từ chối (kiến thức ngoài chương trình, trái AI-TUTOR 9, làm bài quá dài; ghi lý do 1 dòng) · hỏi thầy (đổi cấu trúc, đổi tình huống mở bài, hai vai mâu thuẫn). Góp ý `nghi_sai_dap_an`: tự giải lại độc lập trước.
3. **Sửa tối thiểu** `theory.src.html`: không vai "thầy/cô"; chú thích nhiều ý mỗi ý một dòng; 🔑 3–6 chữ; `<`/`>` trong `$…$` viết `\lt`/`\gt`; hạn mức độ dài ở `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`; UI theo `docs/QUY-TAC-THIET-KE.md` (nêu mã quy tắc trong commit). Từ chưa giải thích → giải thích ≤1 câu ngay lần đầu, không thêm mục mới.
4. Build bài như skill `soan-bai-ly-thuyet-tuong-tac`, chụp 375px chỗ đã sửa. Ghi `da-xu-ly/so-quyet-dinh.json` (chạy lại `gop-phan-hoi.py … --danh-dau`, rồi điền quyết định).
5. Tối đa 3 vòng/bài. Dừng khi không còn góp ý `chặn` và vai trung-bình đúng ≥90% quiz.
6. Đăng (sau khi thầy duyệt): `bash scripts/cap-nhat-ly-thuyet.sh <theory.html|bundle.json> <lesson_id>` — chỉ ghi mục lý thuyết, tự sao lưu.

**B. Bài tập mẫu** (khi có `nhan/bai-tap-mau.json`) — làm theo skill `soan-bai-tap-mau` (đọc nó trước), điểm khác là phần nháp đã có:
1. Kiểm máy: `python3 .claude/skills/soan-bai-tap-mau/scripts/kiem-ban-nhap-gemini.py content/lesson-samples/<bài>/gemini/nhan/bai-tap-mau.json --lesson-id <id>` (đúng 4 dạng, `cap_do` 1→4, tính lại `kiem_tinh`, trích đề, từ cấm, YCCĐ). Có ✗ thì sửa trước; mục `dieu_ban_khong_chac` tự giải lại đầu tiên.
2. **Không đăng nguyên văn**: viết lại lời giải theo "Phong cách" của `soan-bai-tap-mau` (khung kiến thức, bước đánh số, ⚠ điều kiện, nhận dạng), giữ cấu trúc bắc cầu (`cau_noi`), dựng mô phỏng + bảng phân tích, khớp `topic` với `question-topics.json`, lưu `scripts/data/bai-tap-mau/<id>.json`.
3. Kiểm chéo độc lập bằng `kiem-code` (tự giải không nhìn lời giải) → `review.checked: true` → validate → thầy duyệt → đăng `npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --dry-run` rồi bỏ `--dry-run` (`--giu-cu` nếu bài đã có dạng cũ). Chạy lệnh ghi DB trong tab terminal của thầy.
4. Lưu bản đã kiểm vào `da-xu-ly/`. Ghi trạng thái vào `hang-doi.md`.

## Ranh giới
- Chỉ gửi nội dung bài cho Gemini; **không** gửi tên, điểm, SĐT học sinh.
- Lời giải/đáp án do model ngoài sinh luôn được Claude tính lại trước khi đăng.
- Học sinh ảo giỏi hơn học sinh thật; vai `yeu` phải ép giả vờ không biết. Sau khi đăng, đối chiếu số liệu làm bài thật của lớp.
- Hai điểm thầy duyệt mỗi bài: các góp ý `hoi_thay`, và bản cuối trước khi đăng. Không tự đăng.

## Nhật ký rút kinh nghiệm (cập nhật cuối MỖI phiên dùng skill này — xem `AGENTS.md`)

- 2026-10-08 · Gộp 2 skill (phản hồi học sinh ảo + nháp bài tập mẫu) thành một; thầy dùng Gemini Pro web, không API (Gemini CLI đăng nhập Google bị bỏ vì hạn mức riêng, không phải gói Pro) → mặc định dán tay, hỏi trước thầy dùng Gemini qua đường nào. Chưa chạy vòng thật: sau bài đầu ghi lỗi hay gặp của Gemini và mức công Claude phải viết lại.
