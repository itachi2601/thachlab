# Brief kiểm chéo đợt 4 (kiem-code) — đọc sau `_brief-dot4.md`

`<cd>` thư mục CĐ, `<id>` lesson_id. Dựng bản đầy đủ vào scratch RIÊNG của bạn (không ghi `<id>.json` thật):
`BTM<id>_OUT=<scratch>/all.json python3 scripts/data/bai-tap-mau/build-hinh-<id>.py`, rồi
`npx tsx .claude/skills/soan-bai-tap-mau/scripts/validate.mts <scratch>/all.json` (lỗi `review.checked` là bình thường).
Luyện tập: `content/hsg9/<cd>/luyen-tap/bundle.json`. Lý thuyết: `content/hsg9/<cd>/theory.html`.

KHÔNG sửa file nào trong repo. Chỉ báo cáo. Ghi báo cáo đầy đủ vào `<scratch>/bao-cao.md`, trả lời cuối ≤ 15 dòng,
mỗi lỗi một dòng: `[NẶNG|VỪA|NHẸ] file · vị trí (dạng/bước/câu) · lỗi · sửa đề xuất`. Không có lỗi thì nói rõ.

## Kiểm 1 — Giải độc lập
Tự giải lại TỪ ĐỀ (problem_html, câu hỏi từng bước, đề tự luận, câu luyện tập, quiz + thử thách trong lý thuyết) trước khi xem
lời giải/đáp án, bằng Python. Rồi đối chiếu: đáp số, đáp án đúng duy nhất, phương án nhiễu không trùng đáp án, sai_so hợp lý
(HS làm tròn hợp lý không bị chấm sai), đề kín (đủ dữ kiện, giả thiết ghi rõ, không hai cách hiểu cho hai số khác), bài nhiều
trường hợp không thiếu nghiệm, trùng số giữa lý thuyết/bài tập mẫu/tự luận/luyện tập.

## Kiểm 2 — Soát trình bày
Lý thuyết: sai công thức/đơn vị/khái niệm, ảo giác (số liệu thật, sự kiện thật), phạm vi HSG 9. Hình: tỉ lệ, chữ ≥ 14, nhãn đè,
tia sáng/đường sức đúng quy ước brief, lộ đáp số (figcaption, khung cuối mô phỏng, hình vẽ sẵn kết quả). KaTeX: chạy KaTeX trên
mọi `$…$` của cả 3 nguồn, quét ký tự điều khiển (`\t`, `\f`, `\b` lẫn trong JSON). Nhãn đề thi thật (A. B. C. D. / a) b) c) d) / đáp số).
Render 375px bằng Chrome headless (trong scratch), xem bằng mắt các hình và mục có tương tác; báo tràn ngang, chữ nhỏ.
