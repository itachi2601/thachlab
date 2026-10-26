---
name: video-tom-tat-bai
description: Làm VIDEO TÓM TẮT dọc 9:16 (điện thoại, 2–4 phút) cho MỘT bài lý thuyết thachlab đã đăng — mỗi kiến thức gắn một hình ảnh chốt dễ nhớ (trí nhớ hình ảnh), có hoạt hình, phụ đề ngắn, giọng đọc (giọng máy Linh hoặc giọng thầy thu). Quy trình cố định: Claude viết kịch bản → agent đóng vai học sinh xem và góp ý (khớp bài không, dễ nhớ không, hình nào dễ lẫn) → Claude kiểm từng góp ý, sửa → mới dựng video (Python + PIL + ffmpeg) → đồng bộ ngược các hình chốt vào bài web. Dùng khi thầy nói "làm video tóm tắt bài X", "video dọc cho bài…", "tóm tắt bài bằng video", "/video-tom-tat-bai". KHÁC tai-nguyen-bai-hoc (tìm video thí nghiệm có sẵn để nhúng) — skill này tự dựng video tóm tắt cả bài. Chạy trên Mac (cần `say`, ffmpeg của imageio, phông SF).
---

# Video tóm tắt bài học (dọc 9:16)

Mẫu đã làm và đã sửa theo góp ý: `content/lesson-samples/l12-thuyet-dong-hoc-phan-tu/video/`
(`make_video.py` dựng video, `nhap_giong.py` nhập giọng thu, `kich-ban-thu-am.md`). Bài mới copy thư mục đó làm khung.

Đầu ra trong `content/lesson-samples/<bai>/video/`: `kich-ban.md`, `gop-y-hoc-sinh.md`, `make_video.py`, `nhap_giong.py`,
`kich-ban-thu-am.md`, `<ten>.mp4`. File mp4, `audio/`, `preview/` nằm trong `.gitignore` của thư mục, không commit.

## Nguyên tắc nội dung (đọc trước khi viết kịch bản)
- **Một kiến thức = một hình chốt** cụ thể, đời thường, vẽ được (hạt khói nhảy múa, bàn bi-a hoàn hảo, thùng 1 mol). Học sinh
  nhớ hình rồi kéo được kiến thức theo (mã hoá kép, Paivio; Mayer: lời nói + hình động).
- **Các hình chốt phải khác hẳn nhau.** Hai hình cùng kiểu (hai cảnh "đám đông") làm học sinh yếu lẫn hai khái niệm.
  Bản đầu của mẫu dùng "quả bóng giữa đám đông" (Brown) cạnh "chen chợ Tết" (khuếch tán) và phải sửa.
- **Cảnh cuối nhắc lại 5 hình chốt** theo thứ tự, mỗi hình một dòng (chuỗi định vị). Câu chốt: "Nhớ năm hình, nhớ cả bài."
- **Phủ đủ "bẫy" của bài**: mỗi bẫy trong mục "Ba cái bẫy" trên web phải có ít nhất một keyword `Bẫy: …` trong video,
  hoặc một cảnh riêng nếu là bẫy lớn.
- **Bài thử có đếm ngược** (3–4 giây im) rồi mới hiện đáp án. Đáp án **đủ mọi bước bài web nhấn** (mẫu: thiếu bước nhân Nₐ
  ra số phân tử, đúng lỗi bài web hay bắt).
- **Gộp ý thì nói rõ là gộp.** Bài viết "ba nội dung" mà có thêm ý thứ tư thì video phải nói ý đó nằm trong chữ nào,
  để học sinh không hỏi "thuyết có 3 hay 4 ý".
- **Chữ màn hình ≤ 2 dòng** (cỡ 46, rộng 900 px) và **ngắn hơn câu đọc**: phụ đề là ý chính, không chép nguyên lời
  (Mayer: chữ trùng lời đọc gây dư thừa). `python3 make_video.py --kiem` phải báo 0 câu quá 2 dòng.
- Gọi học sinh là "em", **không dùng vai "thầy"**. Không đưa thông tin ngoài bài web; số liệu lấy đúng như bài
  (cả các số đã ghi là "số minh hoạ").
- Độ dài 2–4 phút, 9–12 cảnh, mỗi cảnh 3–7 câu. Dài hơn thì tách thành hai video.

## Quy trình

### 1. Đọc bài (rẻ, không đọc cả HTML)
```bash
sed -e 's/<[^>]*>/ /g' content/lesson-samples/<bai>/theory.src.html | tr -s ' \n' | grep -v '^\s*$' | head -c 12000
```
Rút ra: mục tiêu, các mục kiến thức kèm dòng 🔑, mục "Ba cái bẫy", "Trả bài", một bài tính có số đẹp, "Mang về sau bài học".

### 2. Viết kịch bản `video/kich-ban.md` (chưa viết code)
Mỗi cảnh một bảng: **Hình chốt** · **Hình động** (cái gì chuyển động, chuyển động thế nào) · các dòng
`chữ màn hình | câu đọc` · keyword hiện ở cuối cảnh. Câu đọc viết theo cách giọng máy đọc đúng
(Brao, a mô ni ắc, các bô níc, N A); chữ màn hình viết chuẩn (Brown, NH₃, CO₂, Nₐ). Cuối file lập bảng
**Kiến thức trên web → cảnh nào phủ** để học sinh ảo dò phần còn thiếu.

### 3. Học sinh ảo góp ý (subagent, bắt buộc trước khi dựng)
Gọi `Agent` (`general-purpose`, `model: sonnet`) với prompt trong [hoc-sinh-ao.md](hoc-sinh-ao.md), điền đường dẫn
`kich-ban.md` và `theory.src.html`. Agent đóng hai vai: học sinh khá kiểm khớp nội dung, học sinh yếu kiểm dễ nhớ/dễ lẫn.
Agent trả về bảng góp ý có mã cảnh và mức độ, Claude ghi vào `video/gop-y-hoc-sinh.md`.

### 4. Kiểm từng góp ý rồi sửa
Mỗi góp ý: đối chiếu với `theory.src.html` rồi ghi **Sửa / Không sửa + lý do** vào `gop-y-hoc-sinh.md`.
Học sinh ảo có thể sai, nhất là khi đòi thêm kiến thức ngoài bài. Đổi hình chốt hoặc thêm cảnh thì chạy lại bước 3 một vòng
(tối đa 2 vòng). Thầy góp ý trực tiếp thì làm như một vòng học sinh ảo, không cần chạy lại agent.

### 5. Dựng video
1. Copy `make_video.py` và `nhap_giong.py` của mẫu. Giữ nguyên phần tiện ích: âm thanh (`tts`, file `.txt` đi kèm mỗi câu),
   `chrome`, `keyword`, `rich` (chỉ số trên/dưới), `Gas`, `Walk`, `cube`, `--kiem`, `--preview`. Viết lại `SCENES`
   theo kịch bản và các hàm vẽ `s_<key>`, mỗi cảnh 1 hàm. Mốc hiện hình đặt theo `M[i]` (lúc bắt đầu câu i), không đặt theo giây.
2. Bố cục cố định 1080×1920: đầu trang (chip bài + tên cảnh) đến y≈200 · hình 260–1250 · keyword quanh y 1400 ·
   phụ đề 1560–1790 · chân trang 1860. Nền sáng `BG`. Phông `/System/Library/Fonts/SFNS.ttf` (có ₂₃⁴, ①, chữ Việt);
   Arial thiếu chỉ số dưới.
3. `python3 make_video.py --kiem`, rồi `--preview` (2 khung/cảnh vào `preview/`). Ghép thành 2–3 tấm, mỗi khung 360×640.
   Xem tấm ghép, **không** mở từng ảnh. Sửa chỗ tràn chữ hoặc chồng hình, rồi mới chạy `python3 make_video.py`
   (khoảng 2 phút cho 3,5 phút video). Kiểm bằng `ffmpeg -i` (1080×1920, có luồng âm thanh) và trích 1–2 khung ngẫu nhiên.
4. Đổi một câu đọc thì file `.txt` không còn khớp, script tự đọc lại câu đó bằng giọng máy. Trong ngày dựng, khi đổi số câu
   của một cảnh, **xoá tay** các `.wav` từ câu bị chèn trở đi nếu thư mục còn file cũ không có `.txt`.

### 6. Giọng đọc
- Mặc định: giọng Linh (`say -v Linh -r 185`), không có cảm xúc.
- Giọng thầy: `python3 nhap_giong.py --kich-ban` sinh `kich-ban-thu-am.md` (số câu, gợi ý giọng mỗi cảnh). Thầy thu một file
  liền trên iPhone, nghỉ khoảng 2 giây giữa hai câu, rồi chạy `python3 nhap_giong.py <file>`. Script cắt theo khoảng lặng và kiểm số câu.
- Sửa vài câu: `python3 nhap_giong.py --kich-ban --moi 8,10,41` đánh dấu câu cần thu,
  rồi `python3 nhap_giong.py --cau 8,10,41 <file>` chỉ ghi đè đúng các câu đó.
- Dịch vụ giọng AI (ElevenLabs, FPT.AI…) tốn tiền: chỉ dùng khi thầy chọn và tự cấp khoá.

### 7. Đồng bộ ngược sang bài web
Hình chốt và cụm từ video đặt ra mà web chưa có (mẫu: "Nhỏ · Loạn · Đập", "bàn bi-a hoàn hảo", "ống khói trắng") thì thêm
vào mục "Mang về sau bài học", hoặc ghi cạnh dòng 🔑 của mục tương ứng (dòng 🔑 ≤ 14 chữ). Học sinh xem video xong mở web
phải tìm thấy đúng các chữ đó. Sau khi sửa: `python3 build_figs.py && python3 build_bundle.py`, lint, rồi
`bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/<bai>/bundle.json <lesson_id> --yes` trong **tab terminal**.
Đọc phần "Khác biệt" ở bước xem thử: chỉ được thấy đúng chỗ mình sửa. Khác chỗ khác nghĩa là DB có bản sửa trên web:
dừng lại, hỏi thầy. Worktree thiếu `.env.local` thì tạo symlink tới bản ở `~/Projects/thachlab/.env.local`.
`lesson_id` lấy ở bảng trong skill `cap-nhat-thi-nghiem-l12` hoặc dòng "Bài #…" của bước xem thử.

### 8. Giao và chốt
`SendUserFile` gửi mp4. Commit đúng đường dẫn: script, md, bài web (không commit mp4). Rút kinh nghiệm vào nhật ký dưới đây.

## Nhật ký rút kinh nghiệm
Dạng: `- YYYY-MM-DD · <sự cố> → <quy tắc>`.
- 2026-10-26 · Video mẫu bài Thuyết động học phân tử (L12 bài 6): Arial thiếu ₂₃₄ và ①–④ nên chữ hiện ô vuông →
  dùng SFNS.ttf. Bản đầu dựng thẳng, không qua học sinh ảo, nên dính 4 lỗi phải sửa sau: thiếu bước nhân Nₐ, hai hình
  đám đông dễ lẫn, gộp ý lực liên kết mà không nói, chỉ nhắc 1/3 bẫy, cộng một phụ đề 3 dòng → bước 3–4 là bắt buộc,
  checklist ở mục "Nguyên tắc nội dung".
- 2026-10-26 · Cache giọng theo tên file `sNN_MM.wav` nên đổi câu hoặc chèn câu vẫn phát giọng cũ → mỗi `.wav` có `.txt`
  ghi câu đã đọc, lệch thì đọc lại.
