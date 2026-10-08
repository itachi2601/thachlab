---
name: chinh-ly-thuyet-theo-phan-hoi
description: Đọc phản hồi của Gemini đóng vai học sinh (file JSON trong content/lesson-samples/<bài>/phan-hoi-hs/), gộp góp ý của nhiều vai, KIỂM từng góp ý rồi sửa tối thiểu bài lý thuyết tương tác (theory.src.html) cho dễ hiểu hơn; ghi lại góp ý nào chấp nhận/từ chối. Dùng khi thầy nói "/phan-hoi <bài>", "xử lý góp ý của Gemini", "Gemini đã đọc thử bài rồi, sửa đi", "sửa lý thuyết theo phản hồi học sinh ảo". Gemini chạy ngoài Claude (Cursor/Gemini app) theo references/PROMPT-GEMINI-HOC-SINH.md; skill này chỉ xử lý file kết quả. Sửa + build chạy được trên cloud; ĐĂNG lên DB phải chạy trên Mac.
---

# Sửa bài lý thuyết theo phản hồi của "học sinh ảo" (thầy chốt 8/10/2026)

Gemini đọc bài như học sinh lớp 10–12 rồi ghi góp ý ra file. Claude **không gọi API Gemini** (quy tắc phân công trong `AGENTS.md`); điểm nối duy nhất là thư mục trong repo:

`content/lesson-samples/<bài>/phan-hoi-hs/AAAA-MM-DD-<vai>.json` (vai: `yeu` | `trung-binh` | `kha`)

Prompt gửi Gemini và schema: `references/PROMPT-GEMINI-HOC-SINH.md`. Chỉ gửi nội dung bài, **không gửi dữ liệu định danh học sinh**.

## Chạy tự động (thầy cho phép 8/10/2026, ngoại lệ riêng cho việc này)

Thầy đã đồng ý cho script gọi Gemini thay vì dán tay: `scripts/gemini-phan-hoi.mts` (chạy trong tab terminal trên Mac; cần `GEMINI_API_KEY` + `GEMINI_MODEL` trong `.env.local`, không hard-code tên model).
```
npx tsx scripts/gemini-phan-hoi.mts --bai <thư-mục-bài> --ten "<tên bài>" --dry-run   # xem trước, không gọi API
npx tsx scripts/gemini-phan-hoi.mts --bai <thư-mục-bài> --ten "<tên bài>"             # 3 vai × 2 lượt, lưu vào phan-hoi-hs/
```
Mỗi vai gọi 2 lượt: quiz "mù" (bài đã bỏ lời giải/đáp án) rồi đọc đủ + góp ý. Chỉ gửi nội dung bài, không dữ liệu học sinh. Xong thì chạy bước 1 bên dưới. Chế độ bài tập mẫu: thêm `--che-do bai-tap-mau --lesson-id <id>`.

## Quy trình

1. **Gộp**: `python3 .claude/skills/chinh-ly-thuyet-theo-phan-hoi/scripts/gop-phan-hoi.py content/lesson-samples/<bài>`
   - In góp ý chưa xử lý, gom theo vị trí; góp ý được ≥2 vai nêu xếp trước; mức `chặn` xếp trước `khó` rồi `nhỏ`.
   - In phân bố đáp án quiz của các vai. Muốn so với đáp án thật: tạo `phan-hoi-hs/dap-an-that.json` dạng `{"cau1":"C",…}` (lấy từ `theory.src.html`); câu nào ≥1 vai trung-bình/khá chọn sai → xem lại phương án nhiễu và lời "Chưa đúng".
2. **Kiểm từng góp ý, không sửa mù.** Gemini có thể sai vật lí, bịa chỗ khó, hoặc khen xã giao. Với mỗi góp ý quyết định:
   - **Chấp nhận**: chỗ đó thật sự dễ gây hiểu sai/đứt mạch (đối chiếu trích dẫn với `theory.src.html`; trích sai vị trí → coi là nghi bịa).
   - **Từ chối**: góp ý đòi thêm kiến thức ngoài chương trình, trái AI-TUTOR 9, hoặc làm bài dài quá hạn mức. Ghi lý do 1 dòng.
   - **Hỏi thầy**: đổi cấu trúc bài, đổi tình huống mở bài, hoặc hai vai mâu thuẫn nhau.
3. **Sửa tối thiểu** trong `theory.src.html` (không soạn lại). Quy tắc giữ nguyên: không vai "thầy/cô"; chú thích nhiều ý mỗi ý một dòng; từ khoá 🔑 3–6 chữ; `<`/`>` trong `$…$` viết `\lt`/`\gt`; hạn mức độ dài/nhịp ở `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`; UI theo `docs/QUY-TAC-THIET-KE.md` (nêu mã quy tắc trong commit). Chỗ "từ chưa giải thích" → giải thích ngay lần đầu xuất hiện bằng ≤1 câu, đừng thêm mục mới.
4. **Build + xem**: chạy `build_*.py` của bài (như skill `soan-bai-ly-thuyet-tuong-tac`), chụp 375px chỗ đã sửa.
5. **Ghi sổ**: tạo/cập nhật `phan-hoi-hs/da-xu-ly.json` bằng `gop-phan-hoi.py … --danh-dau` rồi điền `quyet_dinh` (chap_nhan|tu_choi|hoi_thay) và `ghi_chu` cho từng id. Bảng tóm tắt gửi thầy: id · quyết định · đã sửa gì (1 dòng/góp ý).
6. **Vòng sau**: tối đa 3 vòng/bài. Dừng khi không còn góp ý `chặn` và vai `trung-binh` đúng ≥90% quiz. Sau khi thầy duyệt mới đăng bằng `bash scripts/cap-nhat-ly-thuyet.sh` (chỉ ghi mục lý thuyết, tự sao lưu).

## Giới hạn cần nhớ
- Học sinh ảo giỏi hơn học sinh thật; vai `yeu` phải ép "giả vờ không biết" (đã ghi trong prompt). Sau khi đăng, đối chiếu thêm số liệu làm bài thật của lớp.
- Không đưa tên/điểm học sinh thật vào file phản hồi hay prompt.
- Góp ý "nghi_sai_dap_an" → tự giải lại độc lập trước, nếu đúng là sai thì sửa cả `bundle.json`/quiz liên quan.

## Nhật ký rút kinh nghiệm (cập nhật cuối MỖI phiên dùng skill này — xem `AGENTS.md`)

- 2026-10-08 · Tạo skill (chưa chạy vòng thật) → sau vòng đầu ghi vào đây: góp ý nào của Gemini hay sai nhất, vai nào hữu ích nhất.
