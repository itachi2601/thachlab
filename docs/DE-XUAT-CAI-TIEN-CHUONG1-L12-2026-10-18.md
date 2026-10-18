# Đề xuất cải tiến chương 1 lớp 12 (bài 1–4) — prompt + agent thực hiện

Ngày 18/10/2026. Xuất phát từ một bản rà cấu trúc do agent đóng vai học sinh (không phải học sinh thật) đọc 4 bài:
`l12-su-chuyen-the`, `l12-thang-nhiet-do`, `l12-noi-nang-dl1`, `l12-thuc-hanh-nhiet` (nguồn `content/lesson-samples/<slug>/theory.src.html`).
Phản biện đã chốt: điểm yếu thật là **mật độ chữ + số khối `<details>` + thiếu báo trước độ dài**, không phải việc có câu tự kiểm chen giữa.
Căn cứ: `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md` (hạn mức mục 3, ba lớp đọc mục 4, L2) và `docs/QUY-TAC-THIET-KE.md` (G3, B8, C, V, L2).

Quy ước chung cho mọi việc dưới đây:
- Chỉ sửa `theory.src.html` → build → xem thử 375px → giao `kiem-code` → thầy duyệt → `bash scripts/cap-nhat-ly-thuyet.sh <theory.html> <lesson_id>`. Không đụng Luyện tập/Bài tập mẫu.
- `lesson_id` tra bằng truy vấn chỉ đọc theo slug, không đoán.
- Commit theo đường dẫn cụ thể; ghi mã quy tắc vào mô tả commit.

| # | Việc | Agent / model | Vì sao |
|---|---|---|---|
| 1 | Đo độ dài 4 bài bằng `lint_do_dai.py` | Phiên chính, `Bash` (không cần agent) | Script có sẵn, chỉ đọc, kết quả quyết định việc 3 |
| 2 | Thêm dòng ước lượng đầu bài (phút · mục · câu tự kiểm) | Phiên chính (sonnet) | Sửa máy móc theo số đo của việc 1 |
| 3 | Rà và mở lại các `<details>` giấu kiến thức cốt lõi | Phiên chính (opus) + `kiem-code` soát | Cần phán đoán sư phạm "cốt lõi hay mở rộng" |
| 4 | Dự phòng chữ dưới mỗi video YouTube | Phiên chính (sonnet) + `kiem-code` | Phải xem video thật để tả đúng hiện tượng |
| 5 | Mục Trả bài của bài 3–4 gọi lại bài 1–2 | Phiên chính (sonnet) + `kiem-code` | Nội dung ngắn, cần đối chiếu 4 bài |
| 6 | Đo độ sâu cuộn theo mục + tỉ lệ bấm quiz | `kien-truc-du-lieu` (opus) thiết kế bảng/RLS; phiên chính làm phần client | Đụng schema + dữ liệu học sinh |

Việc 1–5 là nội dung, làm một đợt trên Mac. Việc 6 là code, thầy quyết riêng (xem "đo thêm được rẻ" trong PHUONG-PHAP-NOI-DUNG-LY-THUYET.md).

---

## Việc 1 — Đo độ dài (phiên chính, Bash)

```
Chạy python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py cho 4 file
content/lesson-samples/{l12-su-chuyen-the,l12-thang-nhiet-do,l12-noi-nang-dl1,l12-thuc-hanh-nhiet}/theory.src.html.
Lập một bảng: bài | từ hiện ngay | tổng từ | ~phút | mục dài nhất | đoạn liền dài nhất | tới việc đầu | số <details> | số .tl-quiz | kết quả lint.
Đánh dấu ⚠/✗ theo hạn mức mục 3 của docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md (hiện ngay >2.000/>2.500; một mục >350/>480;
đoạn liền >300/>400; tới việc đầu >150/>250). Chỉ báo số, không sửa gì. Bài nào có ✗ mới chuyển sang việc 3 với yêu cầu cắt.
```

## Việc 2 — Dòng ước lượng đầu bài (phiên chính, sonnet)

```
Với 4 bài chương 1 lớp 12, lấy số đo từ bảng việc 1. Ngay dưới khối mục tiêu đầu bài, trước câu dự đoán, thêm một dòng
dạng "⏱ Khoảng N phút · M mục · K câu tự kiểm — học 2 mục rồi quay lại cũng được." (N = từ hiện ngay / 140, làm tròn;
M = số <h3> không tính mục tiêu; K = số .tl-quiz). Dùng đúng markup/class mà các bài đã có dòng này đang dùng — grep
"⏱" hoặc "phút ·" trong content/lesson-samples/*/theory.src.html để lấy mẫu, không tự chế class mới.
Dòng này không được đẩy "tới việc đầu" vượt 150 từ (L2). Build lại theory.html + bundle.json bằng build_bundle.py của bài,
chụp xem-thu 375px. Ghi mã L2 vào commit.
```

## Việc 3 — Rà khối `<details>` (phiên chính opus, kiem-code soát)

```
Bản rà ghi 4 bài chương 1 lớp 12 có khoảng 17 mục "Bấm xem" đóng mặc định. Với từng bài, liệt kê mọi <details>:
summary | nội dung thuộc loại nào (A: định nghĩa/công thức chính/"cái bẫy"/kết quả thí nghiệm — B: công thức suy ra,
ứng dụng, bài khó hơn, lịch sử) | đề xuất (mở hẳn thành đoạn thường / giữ gập / gộp với khối khác).
Nguyên tắc: loại A không được gập (G3, B8 — mắt chỉ quét 20–28% chữ, cái bẫy là phần giá trị nhất; gập là giấu, học sinh
trung bình học thiếu mà không biết). Loại B giữ gập. Mục tiêu mỗi bài còn 6–8 <details>.
Khi mở một khối A, viết lại thành bullet ≤8 từ hoặc 2–3 câu, không dán nguyên đoạn dài; nếu mục đó vượt 350 từ hiện ngay
thì tách <h4>. Chạy lại lint_do_dai.py sau khi sửa, không được làm bài vượt ✗.
In bảng đề xuất cho thầy duyệt TRƯỚC khi sửa file; sau duyệt mới sửa theory.src.html và build.
```

Prompt cho `kiem-code` sau khi sửa:
```
Soát diff theory.src.html của 4 bài chương 1 lớp 12. Kiểm: (1) không khối <details> nào chứa định nghĩa, công thức chính
hoặc "cái bẫy" còn đóng; (2) không mục <h3>/<h4> nào vượt 480 từ hiện ngay, không đoạn liền nào vượt 400 từ (chạy
lint_do_dai.py); (3) công thức KaTeX vẫn render, dấu < > trong $…$ viết \lt \gt; (4) không đổi gì ngoài mục Lý thuyết.
Trả về danh sách lỗi theo file:dòng, không sửa.
```

## Việc 4 — Dự phòng chữ dưới video (phiên chính sonnet, kiem-code soát)

```
Trong 4 bài chương 1 lớp 12, tìm mọi iframe YouTube. Với từng video: mở xem thật (hoặc đọc mô tả/transcript), rồi thêm ngay
dưới iframe một khối ngắn "Nếu không xem được video" 2–3 dòng: thí nghiệm làm gì, nhìn thấy gì, kết luận gì — đủ để câu
hỏi "Nhìn vào:" đi kèm vẫn trả lời được khi video không tải (nhóm V trong QUY-TAC-THIET-KE.md; mạng trường chậm,
điện thoại chặn YouTube). Mỗi ý một dòng, không ghép bằng dấu chấm phẩy. Nếu video đã hỏng/riêng tư/không còn tiếng Việt
thì báo thầy, không tự thay video khác. Ghi mã V vào commit.
```

## Việc 5 — Trả bài gọi lại bài trước (phiên chính sonnet, kiem-code soát)

```
Đọc mục "Trả bài" của bài l12-noi-nang-dl1 và l12-thuc-hanh-nhiet. Kiểm từng câu hỏi kiến thức của bài nào. Nếu không
có câu nào gọi lại bài 1–2 (sự chuyển thể, thang nhiệt độ), thêm đúng 1–2 câu ngắn dạng điền/chọn nối kiến thức cũ với
bài này (ví dụ: nhiệt độ đo bằng thang nào thì hiệu nhiệt độ trong Q = mcΔT không đổi; nhiệt nóng chảy riêng dùng khi
nào trong bài thực hành). Không làm mục Trả bài vượt trần 8 quiz của bài. Đáp án tự giải lại rồi mới ghi.
```

## Việc 6 — Đo độ sâu cuộn và tỉ lệ bấm quiz (kien-truc-du-lieu opus + phiên chính)

Chỉ làm khi thầy chốt. Prompt cho `kien-truc-du-lieu`:
```
Thiết kế cách ghi hai chỉ số cho trang /lop-hoc/bai: (a) mục <h3> sâu nhất học sinh cuộn tới trong một lượt đọc,
(b) số .tl-quiz đã bấm / tổng quiz của bài. Yêu cầu: không thêm round-trip khi tải trang (gửi 1 lần khi rời trang hoặc
gộp vào heartbeat "đang học" hiện có — xem docs/memory/project_thachlab_bao_live_dang_hoc.md); bảng mới có RLS, học sinh
chỉ ghi dòng của mình, giáo viên đọc theo lớp; giữ DB không phình theo project_thachlab_db_retention.md (rollup, xoá
thô >90 ngày). Đọc docs/DATABASE.md trước, không dò schema. Viết migration vào supabase/migrations/ kèm rollback,
nối vào FILES của scripts/run-migrations.sh, không chạy.
```
Sau đó phiên chính làm phần client và một truy vấn tổng hợp "mục nào bị bỏ nhiều nhất theo bài" để so trước/sau việc 3.

---

# Mở rộng: các chương và lớp còn lại (đo 18/10/2026)

Đã chạy việc 1 cho **toàn bộ 112 bài** (bảng đầy đủ: `docs/DO-DAI-BAI-2026-10-18.md`). Kết quả đảo ngược hai điểm của bản rà:

| Lớp | Bài | Có ✗ | Chỉ ⚠ | `<details>` > 8 | Video YouTube (bài có) | PhET (bài có) |
|---|---|---|---|---|---|---|
| l9 | 12 | 0 | 6 | 12 | 15 (7) | 12 |
| l10 | 34 | 0 | 31 | 34 | 11 (8) | 10 |
| l11 | 26 | 1 | 19 | 26 | 30 (12) | 18 |
| l12 | 22 | 2 | 17 | 19 | 22 (14) | 11 |
| cnc | 9 | 0 | 5 | 8 | 0 | 0 |
| avcn | 9 | 7 | 2 | 9 (100–213) | 0 | 0 |

**Ba kết luận**
1. **Chương 1 lớp 12 là ngoại lệ về độ dài, không phải mẫu chung.** Cả site chỉ có 3 bài Vật lí ✗, và 2 bài trong đó là chương 1 L12 (`l12-su-chuyen-the` 2.556 từ + mục 495 từ; `l12-thang-nhiet-do` 2.511). Bài thứ ba là `l11-thuc-hanh-do-sdd-pin` (đoạn liền 434 từ). Ngoài ra 94 bài Vật lí còn lại đều nằm ở dải 1.800–2.450 từ hiện ngay, tức ⚠ "tổng" gần như đồng loạt — đó là vùng xám đã chấp nhận khi đặt ngưỡng (bài tốt chỉ ⚠), không phải lỗi hàng loạt.
2. **"17 mục Bấm xem" là sai với chương 1 — và đúng với phần còn lại.** Bốn bài chương 1 L12 chỉ có 8–10 `<details>` (ít nhất site). Còn 108 bài khác có 11–20, AVCN 100–213 (thẻ từ vựng, cố ý). Vậy việc 3 (rà `<details>` giấu kiến thức cốt lõi) là **việc toàn site**, không riêng chương 1.
3. **Video YouTube không có dự phòng là rủi ro ở 41 bài / 78 iframe**, tập trung l11 sóng (`song-dung` 6, `giao-thoa-song` 5), l12 cảm ứng (`ung-dung-cam-ung-dien-tu` 5), l9 quang. Việc 4 vì thế cũng là việc toàn site.

**Việc đầu** (≤150 từ) đạt ở 109/112 bài; chỉ AVCN (cố ý, bảng điểm thi) và `cnc-flipped-buoi-1`, `l11-mo-ta-song` (174) vượt nhẹ. Không cần làm gì.

## Kế hoạch toàn site — thứ tự và agent

| Đợt | Phạm vi | Việc | Agent | Ước lượng |
|---|---|---|---|---|
| A | 3 bài ✗ (2 bài chương 1 L12 + `l11-thuc-hanh-do-sdd-pin`) | Cắt/tách mục theo việc 3; thêm dòng ước lượng (việc 2) | Phiên chính opus + `kiem-code` | 1 phiên |
| B | 4 bài chương 1 L12 | Việc 4 (video), việc 5 (Trả bài gọi lại bài trước) — làm cùng đợt A để thầy duyệt một lần | Phiên chính sonnet + `kiem-code` | gộp vào A |
| C | 94 bài Vật lí còn lại | Việc 2 (dòng ước lượng): **sửa bằng script**, một lượt, không agent | Phiên chính, `Bash` + `kiem-code` soát mẫu 5 bài | 1 phiên |
| D | 108 bài có `<details>` > 8 | Việc 3 kiểu quét: script liệt kê summary của mọi `<details>` + 20 từ đầu nội dung → phân loại A/B bằng từ khoá (định nghĩa, công thức, bẫy, kết quả) → bảng cho thầy duyệt bằng `lap-duyet-html` → sửa theo phản hồi | Phiên chính sonnet phân loại; `kiem-code` soát; thầy duyệt | 2–3 phiên, chia theo lớp |
| E | 41 bài có video | Việc 4: mỗi iframe một khối "Nếu không xem được video" | Phiên chính sonnet, theo lớp (l11 sóng trước) | 2 phiên |
| F | AVCN 7 bài ✗ | Không áp hạn mức Vật lí: bài là bộ thẻ từ vựng + `<details>` cố ý. Chỉ xét tách `avcn-chapter-6-welding` (mục 1.017 từ) và `chapter-2` (777) | Phiên chính sonnet, skill `soan-bai-avcn` | riêng |
| G | Toàn site | Việc 6 (đo cuộn + bấm quiz) — làm TRƯỚC đợt D nếu thầy muốn có số liệu trước/sau | `kien-truc-du-lieu` + phiên chính | thầy quyết |

Quy tắc chung cho đợt C–E (sửa hàng loạt nội dung đã đăng): dry-run in diff 3 bài mẫu → thầy xem → `--apply` trên `theory.src.html` → build → `kiem-code` soát ngẫu nhiên 10% → `cap-nhat-ly-thuyet.sh` từng bài (script đã tự sao lưu) → commit theo lớp. Không dùng `upload-lesson.mts`.

### Prompt đợt C — dòng ước lượng hàng loạt (phiên chính, Bash)
```
Viết scripts/chen-uoc-luong-bai.py: với mỗi content/lesson-samples/<slug>/theory.src.html (bỏ avcn-*, cnc-*), chạy
lint_do_dai.py --json lấy hien/so_h3/quiz, chèn (hoặc cập nhật nếu đã có) một dòng "⏱ Khoảng N phút · M mục · K câu tự kiểm"
ngay trước khối câu dự đoán đầu tiên, dùng markup/class đang có trong bài nào đã có dòng này (grep "⏱" trước; nếu chưa bài
nào có thì dùng <p class="tl-uoc-luong"> và thêm CSS một chỗ trong app, không inline). Có --dry-run (in diff 3 bài) và --apply.
Sau --apply chạy lại lint để chắc "tới việc đầu" không bài nào vượt 150. Mã L2.
```

### Prompt đợt D — quét `<details>` toàn site (phiên chính sonnet)
```
Viết scripts/quet-details-bai.py: với mỗi theory.src.html Vật lí (l9–l12), liệt kê từng <details>: slug | thứ tự | summary |
30 từ đầu nội dung | số từ | loại đề xuất. Loại A (không được gập) nếu nội dung chứa định nghĩa, công thức chính (có $…$ và
từ "công thức"/"định luật"), "bẫy"/"hay nhầm"/"sai lầm", hoặc "kết quả"/"rút ra" của thí nghiệm; loại B còn lại. Xuất
scripts/data/duyet/details-<lớp>/items.json (id = slug#thứ-tự, ghiChu = summary + 30 từ, deXuat = "mở"/"giữ gập") và dựng
duyet.html bằng scripts/lap-duyet-html.mts cho thầy duyệt từng lớp. Chỉ liệt kê, không sửa bài.
```
Sau khi thầy trả `phan-hoi.json`: phiên chính mở các khối được duyệt "mở" (viết lại thành bullet ≤8 từ hoặc 2–3 câu, tách
`<h4>` nếu mục vượt 350 từ), chạy lint, giao `kiem-code` theo prompt việc 3 ở trên, rồi đăng.

### Prompt đợt E — dự phòng video hàng loạt (phiên chính sonnet, theo lớp)
```
Liệt kê mọi iframe YouTube trong theory.src.html của lớp <l11>: slug | video id | tiêu đề | câu "Nhìn vào:" đi kèm (nếu có).
Với từng video, lấy tiêu đề + mô tả (oEmbed/trang xem) để tả đúng hiện tượng; chỉ xem video thật khi mô tả không đủ. Thêm
ngay dưới iframe khối <p class="tl-video-fallback"> "Nếu không xem được video" 2–3 dòng, mỗi ý một dòng, đủ để câu "Nhìn vào:"
trả lời được. Video hỏng/riêng tư → ghi vào ra-soat.md, không thay. Build, xem thử 375px 2 bài, giao kiem-code, đăng. Mã V.
```
