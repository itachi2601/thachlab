# Kế hoạch: rút hộp có video · clip hiện tượng · ảnh động (thầy giao 26/10/2026)

Mục tiêu: bớt chữ ở hộp thí nghiệm, để học sinh nhớ hiện tượng qua hình (clip ngắn có phụ đề từ khoá,
SVG chuyển động) thay vì đọc câu dài. Quy tắc: `docs/QUY-TAC-THIET-KE.md` **V8–V11** (kèm V1–V7, B4, H1, N8).

## Hiện trạng (đếm 26/10/2026, 103 bài L9–L12 + CNC, không tính AVCN)

| | L9 | L10 | L11 | L12 | CNC | Tổng |
|---|---|---|---|---|---|---|
| Hộp thí nghiệm `.tl-box--exp` | 35 | 86 | 63 | 58 | 19 | 261 |
| trong đó khung 6 ô (giữ đủ chữ) | 0 | 0 | 0 | 19 | 0 | 19 |
| Hộp ví dụ đã có clip YouTube (→ chặng 1) | 11 | 10 | 21 | 10 | 0 | 52 |
| Hộp ví dụ chưa có clip (→ lọc ở chặng 3) | 24 | 76 | 42 | 29 | 19 | 190 |

74/103 bài đã > 2.300 từ hiện ngay (trần 2.500) — rút hộp ở chặng 1 còn hạ được tổng chữ.
Web đã sẵn: SMIL `<animate>` qua được sanitize (`lib/sanitize-html.ts`), `ContentHtml` gỡ hoạt hình khi
máy bật "giảm chuyển động"; clip YouTube hiện ảnh bìa, chỉ tải player khi bấm (V5).

## Ranh giới với các phiên khác (đọc trước mỗi chặng)

- **L12 làm sau cùng**: phiên `cap-nhat-thi-nghiem-l12` đang viết lại hộp thí nghiệm L12; phiên mẹo từ khoá 🧠
  (`docs/BANG-MEO-TU-KHOA.md`) đang sửa dòng 🔑/Trả bài/Mang về. Trước khi sửa bài nào: `git fetch origin && git merge
  origin/main`, rồi `git log origin/main -3 -- content/lesson-samples/<bài>/theory.src.html` — có commit trong 24 giờ
  qua của phiên khác thì bỏ qua bài đó, ghi vào sổ.
- Chỉ sửa trong hộp `.tl-box--exp`, hộp video ngay sau nó, và chỗ chèn ảnh động. Không đụng 🔑, mẹo 🧠, quiz, số liệu.
- Mỗi bài xong: commit theo đường dẫn (`theory.src.html`, `theory.html`, `bundle.json`, `tn-*.json`) ngay, rồi mới sang bài sau.

## Sổ theo dõi

`content/thi-nghiem/so-clip-anh-dong.md` (tạo ở chặng 0) — mỗi hộp một dòng:
`bài · id thí nghiệm · việc (rút / clip / ảnh động) · trạng thái (nháp / đã soát / đã đăng / bỏ qua: lý do) · ngày · từ hiện ngay trước→sau`.

## Phân công agent

| Việc | Ai làm | Vì sao |
|---|---|---|
| Chặng 0: thí điểm, chốt mẫu, viết spec | phiên chính **Opus** | việc thiết kế, đặt chuẩn cho ~250 hộp sau |
| Chặng 1: rút chữ hộp có clip | phiên chính **Sonnet** | viết lại 2 dòng cần hiểu Vật lí nhưng lặp theo mẫu |
| Soát mỗi lô (Vật lí, V8–V11, ảnh 375px) | agent `kiem-code` (Sonnet) | đã có; đọc ảnh trong agent, phiên chính không mở ảnh |
| Vẽ SVG chuyển động theo spec | **agent mới `ve-hinh-dong`** (Sonnet) | code SVG + chụp + tự đọc ảnh, giữ ảnh ngoài phiên chính |
| Cắt clip, gắn phụ đề, nén, trích khung kiểm | **agent mới `dung-clip`** (Haiku) | chạy script cố định, việc lặp không cần suy luận |
| Viết script `gan-phu-de-clip.py`, `liet-ke-hop-co-video.mts` | **Cursor** (Auto) | code thường không đụng schema (phân công 6/10) → `kiem-code` soát trước khi dùng |
| Lọc 190 hộp, lập danh sách cảnh quay | phiên chính **Sonnet** | đọc kho `content/thi-nghiem/*.json`, không cần Opus |
| Quay clip 10–20 giây | **trợ giảng** (điện thoại) | hiện tượng thật thuyết phục hơn hoạt hình |
| Tải clip lên YouTube (không công khai) | **thầy** | tài khoản kênh của thầy |
| Đăng bài | `bash scripts/cap-nhat-ly-thuyet.sh` trên Mac, sau khi thầy duyệt lô | chỉ ghi mục lý thuyết |

Định nghĩa đề xuất cho hai agent mới (tạo `.claude/agents/<tên>.md` khi thầy đồng ý):

```
---
name: ve-hinh-dong
description: Vẽ MỘT hình SVG chuyển động (SMIL) cho bài lý thuyết thachlab theo spec ngắn — quá trình động như va đập phân tử, dao động, lan truyền sóng, từ thông biến thiên. Bấm mới chạy hoặc ≤ 2 lượt rồi dừng (V10), ≤ 15 KB, nét currentColor; tự chụp 375px và tự đọc ảnh, chỉ trả về đoạn SVG + báo cáo ngắn.
model: sonnet
tools: Read, Write, Edit, Bash, Glob
---
```

```
---
name: dung-clip
description: Xử lý clip hiện tượng 10–30 giây cho bài thachlab bằng scripts/gan-phu-de-clip.py — cắt đoạn, gắn ≤ 3 phụ đề từ khoá theo mốc giây, nén 720p, trích 3 khung hình để tự kiểm phụ đề đọc được và không lộ đáp án. Không sửa bài, không tải lên mạng; trả về đường dẫn file + kích thước + nhận xét khung hình.
model: haiku
tools: Bash, Read, Glob
---
```

## Tiến độ

| Chặng | Việc | Thời gian | Xong khi |
|---|---|---|---|
| 0 | Thí điểm bài Thuyết động học L12 + spec + sổ | 27–28/10 (1 phiên) | thầy duyệt mẫu 3 loại |
| 1 | Rút 52 hộp có clip: L9 → L10 → L11, L12 sau cùng | 28/10–1/11 (2–3 phiên, lô 10–15 hộp) | 52 dòng "đã đăng" hoặc "bỏ qua: lý do" |
| 2 | ~40 SVG chuyển động, theo chương sắp dạy | 3–15/11 (6–8 bài/phiên) | mỗi bài ưu tiên ≤ 2 hình |
| 3 | ~60 clip quay thật, ~10 cảnh/tuần | 3/11–mid 12 | clip nhúng, hộp đã rút theo V8 |

Đo hiệu quả (sau chặng 1): so tỉ lệ đúng câu tự kiểm tra + Trả bài của bài đã đổi, 2 tuần trước và sau; kèm từ hiện ngay.

---

## Prompt từng chặng (dán vào phiên mới, mỗi phiên một chặng/lô)

### Chặng 0 — thí điểm (Opus)

```
Làm chặng 0 trong docs/KE-HOACH-CLIP-ANH-DONG.md trên bài L12 Thuyết động học phân tử
(content/lesson-samples/l12-thuyet-dong-hoc-phan-tu). Đọc trước: docs/QUY-TAC-THIET-KE.md V1–V11 và B4,
mục "Ranh giới" của file kế hoạch. Merge origin/main trước; bài này phiên mẹo 🧠 đã sửa, giữ nguyên phần đó.
1) Rút hộp hạt khói (tn-l12-tdhphantu-01, đã có clip) theo V8. Hộp ống khói trắng (có bảng số đo) giữ nguyên.
2) Một SVG chuyển động cho Đập (phân tử đập thành bình, bật ngược) theo V10, bấm mới chạy. Kiểm begin="click"
   chạy được trong app thật (npm run dev, /lop-hoc/bai) trên Chrome và Safari iOS giả lập; không chạy thì dùng
   repeatCount="2" fill="freeze" và ghi lại.
3) Kịch bản clip bóng bay 2 chậu nước (tn-l12-tdhphantu-04) theo V9: cảnh, độ dài, 3 phụ đề + mốc giây; chưa quay.
4) Viết 3 spec mẫu vào file kế hoạch (mục "Mẫu"): hộp rút, SVG chuyển động, kịch bản clip — để các chặng sau chép.
5) Tạo content/thi-nghiem/so-clip-anh-dong.md, ghi 3 dòng của bài này.
6) In prompt Cursor cho scripts/gan-phu-de-clip.py và scripts/liet-ke-hop-co-video.mts (mục "Prompt Cursor").
Build lại, lint_do_dai (không tăng từ hiện ngay), chụp 375px (kiem-code đọc ảnh). Không đăng DB; báo bản xem thử.
Commit theo đường dẫn, ghi mã V8/V10 trong mô tả. Cuối phiên: Rút kinh nghiệm vào skill soan-bai-ly-thuyet-tuong-tac.
```

### Chặng 1 — rút hộp có clip (Sonnet, mỗi lô 10–15 hộp)

```
Làm chặng 1, lô <L9 | L10 | L11 | L12> trong docs/KE-HOACH-CLIP-ANH-DONG.md. Đọc: QUY-TAC-THIET-KE V8, mục
"Mẫu → hộp rút" và "Ranh giới" của file kế hoạch. Merge origin/main trước.
Danh sách hộp: npx tsx scripts/liet-ke-hop-co-video.mts --lop <N> (bỏ hộp khung 6 ô, hộp có bảng số đo).
Mỗi hộp: viết lại còn "Nhìn vào:" (lấy từ nhin_vao của clip nếu đã tốt) + "Rút ra:", mỗi dòng ≤ 25 từ, giữ đúng
Vật lí của bản cũ; phần giải thích dài còn cần thì chuyển vào <details>. Không đụng 🔑, 🧠, quiz, số liệu.
Mỗi bài: build_figs.py + build_bundle.py của thư mục, lint_do_dai, commit theo đường dẫn ngay.
Hết lô: build_preview + chup_anh, giao kiem-code soát (Vật lí đúng, V8, ảnh 375px). Ghi sổ so-clip-anh-dong.md.
Không đăng; in danh sách bài + lesson_id để thầy duyệt rồi chạy cap-nhat-ly-thuyet.sh. Rút kinh nghiệm cuối phiên.
```

### Chặng 2 — SVG chuyển động (Sonnet + agent ve-hinh-dong)

```
Làm chặng 2 cho chương <…> lớp <…> trong docs/KE-HOACH-CLIP-ANH-DONG.md. Đọc V10, V11, H1, N8 và "Mẫu → SVG
chuyển động". Merge origin/main trước.
1) Với mỗi bài trong chương: chọn ≤ 2 chỗ là quá trình động mà hình tĩnh không cho thấy và bài chưa có
   PhET/clip cho đúng chỗ đó (V6). Không đủ lý do thì ghi "bỏ qua" vào sổ — không ép mỗi bài một hình.
2) Mỗi chỗ viết spec 5 dòng (chuyển động gì, khung đầu tự đọc được ra sao, chú thích từng dòng, bấm/2 lượt,
   đặt sau câu nào) rồi giao agent ve-hinh-dong; chạy song song tối đa 3 agent, mỗi agent một bài.
3) Chèn SVG vào theory.src.html đúng chỗ, build, lint_do_dai, commit từng bài.
4) kiem-code soát cả lô (Vật lí của chuyển động: chiều, tỉ lệ, va chạm đàn hồi…; ≤ 15 KB; không lặp vô hạn).
Không đăng; báo bản xem thử. Ghi sổ, rút kinh nghiệm.
```

### Chặng 3a — lọc hộp, lập danh sách cảnh quay (Sonnet, một lần mỗi lớp)

```
Làm chặng 3a cho lớp <…> trong docs/KE-HOACH-CLIP-ANH-DONG.md. Đọc V9, V11 và kho content/thi-nghiem/tn-l<N>-*.json
(loai, dung_cu, cac_buoc). Chọn hộp chưa có clip mà: hiện tượng thật, mắt cần thấy mới tin, quay được bằng điện
thoại trong lớp với dụng cụ rẻ, an toàn. Mỗi bài tối đa 1 hộp. Với mỗi cảnh viết: dụng cụ, góc máy, 3 bước quay,
độ dài, 3 phụ đề + mốc giây, điều KHÔNG được lộ (đáp án Dự đoán). Xuất content/thi-nghiem/canh-quay-l<N>.md
chia tuần (~10 cảnh/tuần, theo lịch dạy sắp tới) + một tin nhắn gửi trợ giảng (không tên học sinh). Commit.
```

### Chặng 3b — dựng và nhúng clip (Sonnet + agent dung-clip)

```
Làm chặng 3b: trợ giảng đã gửi clip ở <thư mục>. Theo content/thi-nghiem/canh-quay-l<N>.md, giao agent dung-clip
xử lý từng file (cắt, 3 phụ đề, nén 720p, trích khung kiểm). Clip lộ đáp án hoặc mờ thì ghi "quay lại" vào sổ.
Clip đạt: báo thầy danh sách file để tải lên YouTube không công khai; thầy gửi lại youtube_id thì ghi vào video
của tn-*.json (nhin_vao ≤ 25 từ), chạy chen-video-thi-nghiem.mts (xem thử → --apply), rút hộp theo V8,
build, commit từng bài, kiem-code soát. Không đăng; báo thầy duyệt. Ghi sổ, rút kinh nghiệm.
```

### Prompt Cursor (Auto) — hai script công cụ

```
Viết scripts/gan-phu-de-clip.py cho repo thachlab. Vào: file video + JSON
{"bat_dau":s,"ket_thuc":s,"phu_de":[{"tu":s,"den":s,"chu":"≤8 chữ"}]}. Ra: mp4 H.264 720p 16:9, ≤ 30 giây, bỏ
tiếng hoặc giữ tiếng (--giu-tieng), phụ đề vẽ bằng ffmpeg drawtext (font hỗ trợ tiếng Việt, cao ≥ 6% khung,
nền đen mờ 50%, giữa đáy), trích 3 ảnh webp (đầu, giữa, cuối mỗi phụ đề) ra cùng thư mục, in kích thước file.
ffmpeg lấy từ imageio_ffmpeg nếu không có trong PATH. Không gọi mạng.
Viết scripts/liet-ke-hop-co-video.mts: quét content/lesson-samples/*/theory.src.html, in JSON danh sách hộp
.tl-box--exp có .tl-box--video ngay sau: bài, data-exp, số từ trong hộp, có "Giả thuyết" (khung 6 ô) không,
có <table> không. Tham số --lop N. Chỉ đọc file.
Nộp lại: hai file trên; Claude (kiem-code) soát trước khi dùng.
```

## Mẫu (chặng 0 điền)

- Hộp rút: _(chờ chặng 0)_
- SVG chuyển động: _(chờ chặng 0)_
- Kịch bản clip: _(chờ chặng 0)_
