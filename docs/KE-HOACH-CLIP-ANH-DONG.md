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

Hai agent mới đã tạo 26/10/2026: `.claude/agents/ve-hinh-dong.md`, `.claude/agents/dung-clip.md` (tóm tắt):

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

## Cập nhật 26/10/2026 — bỏ bước tải YouTube cho clip tự dựng
`scripts/tai-clip-len-storage.mts <clip.mp4> --tn <id> [--nhan …] [--nhin-vao …] [--apply]`: kiểm 8–30 s, ≤ 3 MB, tạo
ảnh bìa webp từ giây 1, tải lên bucket `lesson-clips` (migration `20261026200000_bucket_lesson_clips.sql`), ghi
`video.mp4`/`poster` vào `tn-*.json`. Rồi `chen-video-thi-nghiem.mts` chèn `<video preload="none">`. Ở chặng 3b, bước
"thầy tải lên YouTube" thay bằng lệnh trên (Claude chạy trong tab terminal). Clip mẫu: `l12-thuyet-dong-hoc-phan-tu/video/clip_bong_bay.py`.


## Kế hoạch clip còn thiếu — đếm lại 14/11/2026

**Đếm thật** (script đọc 330 file `content/thi-nghiem/tn-*.json`, trường `video`; hộp = bài nguồn có `data-exp="<id>"`):
`thi_nghiem` không có video nào **78** (L12 25 · L11 12 · L10 27 · L9 14); `vi_du` không video 65 (không làm clip — T11);
`thi_nghiem` chỉ có YouTube 52 (ngoài kế hoạch này). Con số "211 / 65 bài" trong STATE.md là số cũ.
Trong 78: 3 nhóm A đã duyệt `x` chưa nhập (L12 chuyenthe-02, tutruong-01, tutruong-03 — phiên `chen-clip-l12-nhom-a` đang làm, đừng đụng);
3 đã loại có lý do (l10-klr-apsuat-04, l11-cuong-do-dong-dien-01, l9-kinhlup-02); 4 bài chưa có hộp exp; còn lại **68 nhóm B** (ứng viên YouTube chưa duyệt).
Nhóm C cũ (`danh-sach-tu-dung.md`) đã dựng xong. Theo tiền lệ lô L10 9/11: **B chưa duyệt = tự dựng**; thầy duyệt dòng B nào thì dòng đó rút khỏi lô.

**Chi phí**: ~2,4–2,6 USD/clip (số đo cũ). 70 clip (68 B + 2 hộp mới L12) ≈ 170–180 USD; riêng L12 (lô 1–3, 22 clip) ≈ 55 USD.
Mỗi clip: khung T1–T12 (`docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md`), kịch bản ≤200 từ/phút, không nút A–D trong hình (K10), cổng A + A2 + B 2 vòng.
"thiếu T11" = kho chưa có `gia_thuyet`/`du_doan_neu_dung`/`khong_chung_minh` → bổ sung kho trước khi viết kịch bản.

### Lô đề xuất (lớp · bài · tn-id · nhóm · ghi chú) — "bài N" = `lesson_id` trong kho, không phải số bài SGK

Lô 1 — L12 Ch.1–2 nhiệt + khí (đề Bộ 2025/2026 hỏi thí nghiệm nhiệt nhiều nhất):
- 12 · bài 4 nội năng · tn-l12-noinang-02 · B→tự dựng · đo c nước bằng oát kế; T7 chiều sai số
- 12 · bài 7 Boyle–Charles · tn-l12-boylecharles-02 · B→tự dựng · cột khí V theo T (Charles), bảng V/T
- 12 · bài 7 Boyle–Charles · tn-l12-boylecharles-03 · B→tự dựng · ống chữ J; thiếu T11
- 12 · bài 3 thang nhiệt độ · tn-l12-thangnhietdo-03 · B→tự dựng · kéo dài p(t) tìm 0 K; thiếu T11
- 12 · bài 3 thang nhiệt độ · tn-l12-thangnhietdo-02 · B→tự dựng · kiểm hai mốc 0 °C và 100 °C
- 12 · bài 4 nội năng · tn-l12-noinang-01 · B→tự dựng · bơm xe nóng lên (A > 0, Q ≈ 0)
- 12 · bài 6 thuyết động học · tn-l12-tdhphantu-01 · B→tự dựng · hạt khói Brown
- 12 · bài 2 chuyển thể · tn-l12-chuyenthe-03 · B→tự dựng · bay hơi trước quạt; thiếu T11

Lô 2 — L12 Ch.3 từ trường (đề 2025 II.2 cân dòng điện) + Ch.4 đo phóng xạ:
- 12 · bài 11 lực từ · tn-l12-luctu-02 · B→tự dựng · dây giữa hai cực nam châm chữ U, bàn tay trái; thiếu T11
- 12 · bài 11 lực từ · tn-l12-luctu-03 · B→tự dựng · khung dây quay do ngẫu lực; thiếu T11
- 12 · bài 12 thực hành đo B · tn-l12-thuchanhtu-02 · B→tự dựng · đảo chiều I số cân đổi dấu; tránh trùng clip thuchanhtu3/4; thiếu T11
- 12 · bài 14 xoay chiều · tn-l12-xoaychieu-01 · B→tự dựng · biên độ e tỉ lệ tốc độ quay
- 12 · bài 14 xoay chiều · tn-l12-xoaychieu-02 · B→tự dựng · hai LED mắc ngược, đếm đổi chiều
- 12 · bài 125 máy phát–biến áp · tn-l12-mayphatdien-02 · B→tự dựng · ba cuộn lệch 120°; thiếu T11
- 12 · bài 18 phóng xạ · tn-l12-phongxa-01 · B→tự dựng · nhịp đếm ngẫu nhiên, trừ phông (T7); thiếu T11
- 12 · bài 19 an toàn phóng xạ · tn-l12-antoanpx-02 · B→tự dựng · giấy–nhôm–chì (YouTube là hoạt hình, V1); thiếu T11

Lô 3 — L12 còn lại + 2 hộp phải soạn trước:
- 12 · bài 127 điện từ trường · tn-l12-dttruong-01 · B→tự dựng · nam châm rơi qua ống dây → điện trường xoáy
- 12 · bài 10 khái niệm từ trường · tn-l12-tutruong-02 · B→tự dựng · kim la bàn dò hướng B; thiếu T11
- 12 · bài 19 an toàn phóng xạ · tn-l12-antoanpx-04 · B→tự dựng · đọc liều kế TLD suy liều năm; thiếu T11
- 12 · bài 17 phân hạch · tn-l12-phanbach-02 · B→tự dựng · bàn ghim + thanh điều khiển; thiếu T11
- 12 · bài 126 ứng dụng cảm ứng · tn-l12-udcamung-01 · CHƯA CÓ HỘP · soạn hộp exp trước (`cap-nhat-thi-nghiem-l12`), rồi clip nam châm–cuộn–loa
- 12 · bài 126 ứng dụng cảm ứng · tn-l12-udcamung-03 · CHƯA CÓ HỘP · soạn hộp trước; ống nhựa đối chứng ống đồng (khác camungdt-02 ở đối chứng)

Lô 4 — L11 Ch.3–4 điện (đo U–I, nguồn, tụ):
- 11 · bài 42 điện trở · tn-l11-dien-tro-ohm-01 · B→tự dựng · U–I điện trở 10 Ω thẳng qua gốc
- 11 · bài 42 điện trở · tn-l11-dien-tro-ohm-02 · B→tự dựng · U–I đèn sợi đốt cong
- 11 · bài 45 đo SĐĐ pin · tn-l11-do-sdd-pin-01 · B→tự dựng · biến trở, vôn kế, ampe kế (khác sddpin2)
- 11 · bài 43 nguồn điện · tn-l11-nguon-dien-03 · B→tự dựng · đoản mạch pin — YouTube nguy hiểm, clip dựng an toàn hơn
- 11 · bài 40 tụ điện · tn-l11-tudien-01 · B→tự dựng · tụ nạp rồi phóng qua LED
- 11 · bài 40 tụ điện · tn-l11-tudien-03 · B→tự dựng · tụ phẳng tự chế
- 11 · bài 35 Coulomb · tn-l11-coulomb-01 · B→tự dựng · thước cọ tóc hút giấy, lăn lon
- 11 · bài 37 điện trường đều · tn-l11-dien-truong-deu-03 · B→tự dựng · electron quỹ đạo parabol

Lô 5 — L11 sóng/âm + L9 quang:
- 11 · bài 29 đo tần số âm · tn-l11-dotansoam-02 · B→tự dựng · ghi âm điện thoại đếm chu kì
- 11 · bài 34 đo tốc độ âm · tn-l11-dotocdoam-03 · B→tự dựng · độ trễ hai micro
- 11 · bài 27 mô tả sóng · tn-l11-motasong-02 · CHƯA CÓ HỘP · soạn hộp trước
- 9 · bài 88 kính lúp · tn-l9-kinhlup-01 · B→tự dựng · tiêu cự kính lúp 5x
- 9 · bài 85 lăng kính · tn-l9-langkinh-03 · B→tự dựng · ba tia laser đỏ–lục–tím (YouTube chỉ một màu)
- 9 · bài 86 thấu kính · tn-l9-thaukinh-02 · B→tự dựng · hứng ảnh cửa sổ
- 9 · bài 86 thấu kính · tn-l9-thaukinh-03 · B→tự dựng · thước quang học d, d′
- 9 · bài 87 thực hành tiêu cự · tn-l9-tieucu-02 · B→tự dựng · 5 vị trí vật, f trung bình (gần thaukinh-03 — dùng chung khuôn)

Lô 6 — L9 điện + cơ năng + âm:
- 9 · bài 90 đoạn mạch · tn-l9-doanmach-01 · B→tự dựng · I, U nối tiếp
- 9 · bài 90 đoạn mạch · tn-l9-doanmach-02 · B→tự dựng · dòng rẽ nhánh song song
- 9 · bài 89 Ohm · tn-l9-ohm-02 · B→tự dựng · I theo U dây constantan (gần l9ohm1 — khuôn)
- 9 · bài 89 Ohm · tn-l9-ohm-03 · B→tự dựng · R theo l, S, vật liệu
- 9 · bài 130 cơ năng · tn-l9-conang-02 · B→tự dựng · con lắc vướng đinh (dùng chung với L10 dong-nang-the-nang-02)
- 9 · bài 130 cơ năng · tn-l9-conang-03 · B→tự dựng · bóng nảy thấp dần
- 9 · bài 129 động năng–thế năng · tn-l9-dongthe-03 · B→tự dựng · quả nặng rơi xuống khay cát
- 9 · CĐ15 âm thanh (HSG) · tn-l9-hsgamthanh-02 · B→tự dựng · tiếng vang trước tường

Lô 7 — L10 Ch.3 Newton + ma sát:
- 10 · bài 59 Newton 1 · tn-l10-dl1-newton-01 · B→tự dựng · hai máng nghiêng Galilei
- 10 · bài 60 Newton 2 · tn-l10-dl2-newton-01 · B→tự dựng · a theo F (m không đổi)
- 10 · bài 60 Newton 2 · tn-l10-dl2-newton-02 · B→tự dựng · a theo m (F không đổi)
- 10 · bài 61 Newton 3 · tn-l10-newton3-01 · B→tự dựng · hai lực kế kéo nhau (khuôn `luc_ke()`)
- 10 · bài 62 trọng lực · tn-l10-trong-luc-luc-cang-01 · B→tự dựng · trọng tâm tấm bìa bằng dây dọi
- 10 · bài 63 ma sát · tn-l10-luc-ma-sat-01 · B→tự dựng · ma sát nghỉ cực đại, ma sát trượt
- 10 · bài 63 ma sát · tn-l10-luc-ma-sat-02 · B→tự dựng · không phụ thuộc diện tích, tốc độ
- 10 · bài 63 ma sát · tn-l10-luc-ma-sat-03 · B→tự dựng · hệ số ma sát bằng góc nghiêng

Lô 8 — L10 Ch.3 (tiếp) + Ch.7:
- 10 · bài 64 lực cản · tn-l10-luc-can-luc-nang-02 · B→tự dựng · chồng phễu giấy rơi đều
- 10 · bài 64 lực nâng · tn-l10-luc-can-luc-nang-03 · B→tự dựng · Archimedes lực kế + bình tràn
- 10 · bài 66 moment · tn-l10-moment-luc-01 · B→tự dựng · mở cửa: điểm đặt, hướng lực
- 10 · bài 66 moment · tn-l10-moment-luc-02 · B→tự dựng · thước trục giữa (gần moment3 — khuôn)
- 10 · bài 67 thực hành tổng hợp lực · tn-l10-thuchanhthl-01 · B→tự dựng · ba lực kế (khuôn tonghopluc2)
- 10 · bài 79 KLR–áp suất · tn-l10-klr-apsuat-03 · B→tự dựng · chai đục lỗ theo độ sâu
- 10 · bài 78 biến dạng · tn-l10-biendang-01 · B→tự dựng · lò xo bút bi đàn hồi/dẻo
- 10 · bài 78 biến dạng · tn-l10-biendang-02 · B→tự dựng · đo k

Lô 9 — L10 Ch.4–5 năng lượng, động lượng:
- 10 · bài 71 cơ năng · tn-l10-co-nang-bao-toan-02 · B→tự dựng · bóng bàn nảy thấp dần (dùng chung khuôn với nang-luong-cong-01, l9-conang-03)
- 10 · bài 68 năng lượng–công · tn-l10-nang-luong-cong-01 · B→tự dựng · bóng nảy: chuyển hoá, không mất
- 10 · bài 70 động năng–thế năng · tn-l10-dong-nang-the-nang-02 · B→tự dựng · con lắc vướng đinh
- 10 · bài 72 hiệu suất · tn-l10-hieu-suat-02 · B→tự dựng · ván nghiêng bốn góc
- 10 · bài 68 năng lượng–công · tn-l10-nang-luong-cong-02 · B→tự dựng · nhiều đường lên cùng độ cao (gần hieu-suat-02)
- 10 · bài 74 bảo toàn ĐL · tn-l10-baotoandl-01 · B→tự dựng · va chạm mềm đệm khí, cổng quang
- 10 · bài 74 bảo toàn ĐL · tn-l10-baotoandl-02 · B→tự dựng · va chạm gần đàn hồi
- 10 · bài 75 thực hành ĐL · tn-l10-thuchanhdl-01 · B→tự dựng · gần baotoandl-01 — một kịch bản hai số liệu
- 10 · bài 75 thực hành ĐL · tn-l10-thuchanhdl-02 · B→tự dựng · hai xe đẩy nhau lò xo
- 10 · bài 61 Newton 3 · tn-l10-newton3-05 · CHƯA CÓ HỘP · soạn hộp trước hoặc gộp vào thuchanhdl-02 (cùng hiện tượng)

Ngoài lô: `tn-l11-vantocdddh-02` (vi_du) đã có mp4 `-20261110-2` nhưng bài L11 Vận tốc–gia tốc chưa có hộp exp → soạn hộp rồi chèn.

### Nhóm B L12 + L11 — thầy duyệt nhanh (đánh `x` ở `video-de-xuat-l<lớp>-tu-loc.md`, dòng duyệt rút khỏi lô; L10/L9 xem file cùng tên)
- L11 · tn-l11-coulomb-01 · https://www.youtube.com/watch?v=UOjHyIYnG4I · short tiếng Anh
- L11 · tn-l11-dien-tro-ohm-01 · https://www.youtube.com/watch?v=-If3dvVdlXQ · tiếng Việt
- L11 · tn-l11-dien-tro-ohm-02 · https://www.youtube.com/watch?v=z5pQ4hitt14 · tiếng Anh, lab dài
- L11 · tn-l11-dien-truong-deu-03 · https://www.youtube.com/watch?v=-Lw96s_e38k · tiếng Việt, chưa rõ quỹ đạo parabol; dự phòng rEAX3t9YkNs
- L11 · tn-l11-do-sdd-pin-01 · https://www.youtube.com/watch?v=AUgow8x6G_8 · tiếng Việt, EduTech
- L11 · tn-l11-dotansoam-02 · https://www.youtube.com/watch?v=AHD4loletOE · tiếng Việt
- L11 · tn-l11-dotocdoam-03 · https://www.youtube.com/watch?v=YuPp5wsvQjg · tiếng Anh, Physics with Simon
- L11 · tn-l11-motasong-02 · https://www.youtube.com/watch?v=rRaJiSmpcwE · tiếng Anh
- L11 · tn-l11-nguon-dien-03 · https://www.youtube.com/watch?v=O5WN0ClgNmM · tiếng Việt, nguy hiểm — thầy cân nhắc
- L11 · tn-l11-tudien-01 · https://www.youtube.com/watch?v=RL0oUJMuKcs · short tiếng Anh
- L11 · tn-l11-tudien-03 · https://www.youtube.com/watch?v=Nev4F_QR03A · Flipping Physics tiếng Anh
- L12 · tn-l12-antoanpx-02 · https://www.youtube.com/watch?v=boUg4VWjt8M · dạng bài giảng/hoạt hình (GCSE), không phải quay thí nghiệm — dễ vi ph
- L12 · tn-l12-antoanpx-04 · https://www.youtube.com/watch?v=QSnGrC1fBjE · tiếng Việt, clip thương mại
- L12 · tn-l12-boylecharles-02 · https://www.youtube.com/watch?v=wQFMBVYAX9E · CLEAPSS tiếng Anh; dự phòng 8KZF0AAVeYc
- L12 · tn-l12-boylecharles-03 · https://www.youtube.com/watch?v=nLBfnko3310 · tiếng Anh; dự phòng wfe85isT09Y
- L12 · tn-l12-chuyenthe-03 · https://www.youtube.com/watch?v=yxP4xHtjCbE · short tiếng Anh, mô tả làm mát bay hơi
- L12 · tn-l12-dttruong-01 · https://www.youtube.com/watch?v=gAUK54kURyY · VL12 cảm ứng điện từ (THANH TU BOSS); không phải nam châm RƠI qua ống 
- L12 · tn-l12-luctu-02 · https://www.youtube.com/watch?v=3fWLL5d5-T0 · chưa rõ dùng nam châm chữ U hay cân
- L12 · tn-l12-luctu-03 · https://www.youtube.com/watch?v=p_IVmAsDMLs · tiêu đề nói lực từ lên khung, chưa rõ là clip quay hay hình học
- L12 · tn-l12-mayphatdien-02 · https://www.youtube.com/watch?v=I6XDVeQ98AY · mô hình tự chế, tiếng Việt; chưa rõ có đo đồ thị
- L12 · tn-l12-noinang-01 · https://www.youtube.com/watch?v=7Y7td6ly5KM · short tiếng Việt, thiên về giải thích; dự phòng fire piston 4qe1Ueifek
- L12 · tn-l12-noinang-02 · https://www.youtube.com/watch?v=t8Og3N3nAqw · tiếng Việt; chưa rõ có oát kế
- L12 · tn-l12-phanbach-02 · https://www.youtube.com/watch?v=vFrJeJyTtJQ · tiếng Anh, có thể có lời
- L12 · tn-l12-phongxa-01 · https://www.youtube.com/watch?v=EMBairbyex0 · tiếng Việt, không chắc có đo nhiều lần
- L12 · tn-l12-tdhphantu-01 · https://www.youtube.com/watch?v=5Uv3-YLPBBE · tiêu đề nhắc 'phân tử không khí' — kiểm tra có đúng khói; dự phòng ETU
- L12 · tn-l12-thangnhietdo-02 · https://www.youtube.com/watch?v=NYw-51jBgh0 · tiếng Anh
- L12 · tn-l12-thangnhietdo-03 · https://www.youtube.com/watch?v=dOt4wYG4at4 · Columbia, dài, tiếng Anh; dự phòng SjwBHJhlOIo
- L12 · tn-l12-thuchanhtu-02 · https://www.youtube.com/watch?v=Nhm-WpSz2xg · chưa rõ clip có cảnh đảo chiều; trùng luctu-01 (khác bài)
- L12 · tn-l12-tutruong-02 · https://www.youtube.com/watch?v=VTYp52JaYVA · tiếng Anh (Physics with Simon), hơi dài; dự phòng NWUgK8W-4JM
- L12 · tn-l12-udcamung-01 · https://www.youtube.com/watch?v=gAUK54kURyY · không có cuộn nối loa; clip dùng điện kế, cùng bản chất
- L12 · tn-l12-udcamung-03 · https://www.youtube.com/watch?v=a-sgPLciGfQ · cần có đối chứng ống nhựa/không dẫn điện — chưa rõ clip có; trùng clip
- L12 · tn-l12-xoaychieu-01 · https://www.youtube.com/watch?v=chMKGDNPXm0 · tiếng Việt; không có số đo biên độ; dự phòng kRTU5tgJYpw
- L12 · tn-l12-xoaychieu-02 · https://www.youtube.com/watch?v=dfTUuueFG3Q · tên clip tạo dòng xoay chiều — chưa chắc có hai LED

### Việc tồn liên quan clip (14/11/2026)
- **thuchanhtu4 bản 2** (đã đăng DB bài 12, `-20261111-2`): mật độ chữ 285 từ/phút (> 200) — cắt chữ rồi dựng bản 3. JSON khung hiện ghi `tong_giay` 49,9 khớp engine (lệch 48,1 đã hết), vẫn chạy lại `xuat-khung.py` khi dựng bản 3. Soát `thuchanhtu3` cùng lỗi nhãn F/F′.
- **K10 clip cũ** (nút A/B/C vẽ trong hình): 19 clip L12 đã sửa 12/11. Grep còn thấy chuỗi "A." trong `btnangluong1`, `l9ohm1`, `thuchanhtu3`, `thuchanhtu4`, `boyle`, `camungdt`, `camungdt3`, `chuyenthe`, `mayphat1` — chưa chắc là nút, soát mắt khi soát 75 clip chưa từng soát (`ra-soat-clip-2026-11-11.md` mục 3).
- **Sách in thiếu 21 khối thí nghiệm L12** (thông tin từ phiên điều phối 14/11): bổ sung khối exp + QR clip khi dựng lại sách (`sach-in-tu-web`, memory `project_thachlab_sach_in_chuong2`).
- Treo cũ: tutruong4 kho "trụ đứng" ≠ clip nằm ngang; chốt udcamung2.
