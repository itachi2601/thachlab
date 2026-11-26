---
name: project_thachlab_ra_soat_quiz_do_dai
description: Mục 17–20 (26/11/2026) — sửa lỗi nội dung, rút độ dài ≤2.500 từ, rải đáp án quiz; còn rà theo chương
metadata:
  type: project
---

Đợt 26/11/2026 (nhánh `claude/fix-lesson-content-errors-c5fbcb`, đã vào main):
- Đã đăng lý thuyết: 59, 79, 35, 38, 33, 13, 17, 126 (mục 17–19) và L12 Ch.3: 10, 11, 12, 125, 127 (mục 20).
- CHỜ thầy duyệt câu Đ/S + trả lời ngắn mới trong `build_bundle.py` (đề Luyện tập) của bài 13 (4 câu), 17 (2), 126 (2) — đăng đề cần đường đăng cả Luyện tập, không phải cap-nhat-ly-thuyet.sh.
- Còn lại mục 20: các chương khác, ưu tiên theo `docs/quet-quiz-do-dai-2026-11-26.tsv` (L12 nhiệt/hạt nhân, L11 sóng/dao động, L10 động lực học). Quét lại bằng script ở dưới trước khi làm (số đã đổi).
- Cách làm mỗi chương: 1 agent general-purpose/bài với brief dưới → phiên chính commit từng bài → kiem-code soát diff cả chương → `git merge origin/main` (phiên khác hay sửa dòng "Đọc ~N phút · học kỹ ~M phút": sau merge chạy `build_figs.py`, `build_bundle.py`, rồi `dat_phut_hai_moc.py <thư mục bài>`) → push main → sau 22h `cap-nhat-ly-thuyet.sh` (tee log ra file để grep).
- lesson_id tra ở `content/thi-nghiem/video-theo-bai.json` hoặc `lesson_id` trong `content/thi-nghiem/tn-*.json`.

## Brief agent (nguyên văn đợt 26/11)
# Brief chung — sửa bài lý thuyết thachlab (đợt 26/11/2026)

Repo (worktree): /Users/MAC/Projects/thachlab/.claude/worktrees/fix-lesson-content-errors-c5fbcb
Bài nằm ở `content/lesson-samples/<slug>/`. Mỗi agent CHỈ sửa thư mục bài được giao. Các agent khác đang sửa bài khác song song trong cùng thư mục — không đụng file ngoài bài mình, KHÔNG commit, KHÔNG git stash/reset/checkout.

## Quy trình
1. Chỉ sửa nguồn `theory.src.html` (và `build_bundle.py` nếu việc là đề Luyện tập). Không sửa tay `theory.html`.
2. Dựng lại: `cd content/lesson-samples/<slug> && python3 build_figs.py && python3 build_bundle.py`.
3. Sau build: `git diff --stat -- content/thi-nghiem` — nếu build ghi đè file `content/thi-nghiem/*.json` thì `git checkout -- content/thi-nghiem/<file>` (chỉ file đó). Kiểm `git diff -- content/lesson-samples/<slug>/theory.html` chỉ có thay đổi bạn chủ ý.
4. Đo độ dài: `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py content/lesson-samples/<slug>/theory.html` — ghi số TRƯỚC và SAU.
5. Lint khác: `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_theory.py <theory.html>` và `check_quizzes.py` (xem `--help` hoặc đầu file) — không để phát sinh lỗi mới.
6. Đọc `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md` (hạn mức) và `docs/QUY-TAC-THIET-KE.md` mục E1–E3 nếu đụng quiz. Giọng văn: không dùng vai "thầy"; mỗi ý một dòng; không chép SGK.

## Việc loại "rút độ dài" (mục 18)
Mục tiêu: tổng từ hiện ngay ≤ 2.500 (lý tưởng ≤ 2.300), không còn lỗi cứng ✗. Thứ tự:
a) Bỏ hộp video YouTube (`<div class="tl-box tl-box--video">` có iframe youtube, kèm comment `<!--video:...-->` đứng trước) nếu cùng hiện tượng đã có clip/hình/thí nghiệm khác trong bài (trùng). Video duy nhất cho một thí nghiệm thì giữ.
b) Đưa mục phụ vào `<details class="tl-details tl-more"><summary>…</summary>…</details>`: đoạn mở rộng, ví dụ đời sống thứ hai, giải thích lặp lại, chú thích ngoài lề. KHÔNG giấu định nghĩa, công thức lõi, quiz, ô 🎯 Cần nắm, hộp thí nghiệm chính.
c) Cắt câu thừa/lặp (nói lại cùng ý) — cắt chứ không viết lại nội dung vật lí.
Không tạo cảnh báo mới (đoạn liền > 300, mục > 350 nếu có thể thì giảm luôn).

## Việc loại "quiz" (mục 19)
- Phương án nhiễu phải dài ngang đáp án đúng (đáp án đúng không được dài/chi tiết nhất rõ rệt).
- Xáo vị trí đáp án đúng giữa các câu trong bài cho rải A/B/C/D (không câu nào liền 3 câu cùng chữ; không chữ nào chiếm > 40%). Khi đảo, đổi cả `id`, `for`, lớp `tl-ok/tl-no`, chữ cái A–D đầu nhãn, và mọi chỗ phản hồi nhắc tên phương án ("B và C đều…").
- Dòng `<p>⚠ …</p>` đứng TRƯỚC `.tl-quiz` mà gợi ý đáp án → chuyển nội dung vào `<div class="tl-fb tl-fb--no">` (phản hồi khi sai), bỏ dòng ⚠ ở trên.
- Tính lại mọi đáp số sau khi sửa.
- Câu MỚI Đúng/Sai và trả lời ngắn: thêm vào đề Luyện tập trong `build_bundle.py` (mảng EXAM questions), theo đúng dạng ở `content/lesson-samples/l12-tu-truong-ngoai-sgk/build_bundle.py` (type "true_false" và "short_answer"). Đ/S có 4 ý a)–d) (không gõ nhãn vào nội dung — E2), trộn đúng/sai; trả lời ngắn có đáp số một giá trị, ghi rõ đơn vị/làm tròn. Câu mới chỉ dùng kiến thức trong bài, số liệu tự tính hai lần.

## Báo cáo trả về (ngắn, ≤ 25 dòng)
- Từ hiện ngay trước → sau; lỗi ✗/⚠ còn lại.
- Danh sách thay đổi (mỗi dòng một thay đổi: cái gì, ở mục nào).
- Câu mới (nếu có): chép nguyên văn đề + đáp án để thầy duyệt.
- Điều nghi ngờ chưa sửa.

## Mục 20 — rà một bài (đợt theo chương)
Làm đủ 3 việc cho bài được giao, KHÔNG thêm câu mới:
1. **Tính lại mọi quiz** (`.tl-quiz` trong theory.src.html): đáp án đánh `tl-ok` có thật đúng không, số liệu đề đủ để ra đáp án, phương án sai có đúng là sai, phản hồi đúng/sai khớp. Câu sai/mơ hồ → sửa (ghi rõ trong báo cáo, đây là lỗi nặng nhất).
2. **Loại quiz** theo mục 19 ở trên (rải đáp án, nhiễu dài ngang, ⚠ lộ đáp án → phản hồi sai, > 8 quiz thì bỏ câu trùng ý).
3. **Độ dài** theo mục 18 nếu > 2.500 từ hiện ngay.
Khi bỏ hộp video YouTube: gỡ luôn khai báo của video đó — `content/thi-nghiem/video-theo-bai.json` (mục của bài) hoặc field `video` trong `content/thi-nghiem/tn-*.json` (đổi khoá thành `video_bo_khoi_bai` + field `ly_do_bo`), rồi `npx tsx scripts/chen-video-thi-nghiem.mts --bai <slug>` (không --apply) phải báo "0 khối video sẽ chèn". Chỉ đụng mục của bài mình trong video-theo-bai.json (agent khác có thể sửa mục khác cùng file — sửa bằng script Python đọc/ghi lại ngay, không giữ bản cũ trong bộ nhớ lâu).
Đổi "Đọc khoảng N phút" ở khung mục tiêu nếu lint đo phút lệch ≥ 1.
