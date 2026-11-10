# Prompt: soạn câu hỏi ngân hàng lớp 12 PHỎNG THEO bài tập Halliday–Resnick–Walker 12e (HRW)

Viết 27/10/2026, giai đoạn tiếp sau việc hình (hình đã xong: `docs/prompt-hinh-openstax.md`). Giao cho một phiên Opus, context
mới, chạy trên Mac (cần `.env.local` để ghi DB; `pdftotext`/`pdftoppm` đã có). Phiên chính không đọc PDF, không đọc ảnh.

## Bản quyền — bắt buộc (`docs/AGENTS-CHUYEN-DE.md` mục "Bản quyền", `/dieu-khoan`)

- HRW là sách Wiley, không giấy phép mở. **Không chép nguyên văn** đề, số liệu, hình; không dịch sát từng câu. Chỉ lấy **ý tưởng
  tình huống và cấu trúc hỏi** (bài nhiều bước, dữ liệu dạng bảng/đồ thị, bối cảnh thật), rồi viết lại bằng lời mình: đổi số liệu,
  đổi bối cảnh sang Việt Nam (mét/kg/°C, xe máy, quạt, bếp từ, lưới điện 220 V – 50 Hz…), đặt câu hỏi theo cách đề TN THPT 2025 hỏi.
- Văn bản trang sách chỉ nằm trong thư mục tạm (`/tmp/hrw/`), xoá khi xong. Không đưa trích đoạn sách vào repo, JSON, lời giải.
- Mỗi câu ghi `"nguon": "phỏng theo HRW 12e ch.28, bài 15"` trong JSON làm việc (không hiện cho HS). Mục Checkpoint và Sample
  Problem chỉ dùng làm mẫu cách hỏi.
- Không dùng bài cần đạo hàm/tích phân, vi phân, hoặc kiến thức ngoài chương trình GDPT 2018 lớp 12 (xem
  `.claude/skills/soan-quiz-ly-thuyet/references/phong-cach-de-bo-gd.md`). Bài quá dài nhiều ý phụ: cắt còn một ý chính.

## Mục tiêu

Ngân hàng hiện thiếu câu **bài toán có bối cảnh thật, nhiều bước, dữ liệu dạng bảng hoặc đồ thị** — đúng hướng Phần II (đúng–sai theo
tình huống) và Phần III (trả lời ngắn) của đề TN THPT từ 2025. Bổ sung kiểu này theo từng chương, thí điểm trước rồi mới mở rộng.

## Giai đoạn 2 — thí điểm Chương 3 "Từ trường" (20 câu), dừng chờ thầy duyệt

Chương 3 lớp 12 = `chapter_id` 4 trong DB, bài 10, 11, 12, 13, 14, 125, 126, 127 (bài 9–16 SGK). HRW tương ứng: ch. 28 Magnetic
Fields, 29 Magnetic Fields Due to Currents, 30 Induction and Inductance, 31 (phần AC: máy phát, biến áp). PDF Volume 2 ở
`/Users/MAC/Documents/THPT/số hoá THPT/Fundamentals of Physics 12th/`.

1. Tra chủ đề hợp lệ: `scripts/data/nap-ngan-hang-vl12/chu-de-lop12.json` (chỉ dùng đúng `name` trong file này, lọc theo chương Từ trường).
   Đếm câu hiện có theo chủ đề và `qtype` trong `question_bank` (grade 12) để biết chủ đề nào thiếu Đ–S/trả lời ngắn — dùng REST với key
   trong `.env.local`, không `select *`; cột xem `docs/DATABASE.md`.
2. Giao **subagent Sonnet, mỗi agent một chương HRW**, đọc `pdftotext -f A -l B` phần Problems cuối chương (mục lục ở đầu PDF cho số
   trang), trả về **văn bản**: danh sách 8–10 "ý tưởng tình huống" (một câu mô tả hiện tượng + đại lượng cho/hỏi, KHÔNG chép đề), gắn chủ
   đề thachlab. Agent không trả nguyên văn đề sách.
3. Phiên chính chọn 20 ý tưởng phủ đều 8 bài, cơ cấu: 6 trắc nghiệm A. B. C. D. (tính toán, có bẫy), 8 đúng–sai a) b) c) d) theo tình
   huống (mỗi ý một mệnh đề kiểm được), 6 trả lời ngắn (đáp số theo định dạng đề Bộ: số thập phân dấu phẩy, tối đa 4 ký tự).
   Mức: 6 dễ / 10 trung bình / 4 khó.
4. Viết câu + lời giải theo `docs/QUY-TAC-LOI-GIAI.md` (mỗi bước một `<p class="text-base leading-relaxed my-2">`, công thức chữ trước
   số sau, "Sai vì…" cho ≥2 phương án bẫy, Đ–S mỗi ý một `<p>` "a) Đúng./Sai." + lý do, trả lời ngắn kết "Đáp số: …"). Công thức KaTeX
   `$…$`. Nhãn y như đề thật (`docs/QUY-TAC-THIET-KE.md` E1–E3). Không hình; câu cần hình thì bỏ (không vẽ).
5. Định dạng JSON như pipeline VnTeach: `scripts/data/nap-ngan-hang-vl12/hrw-c3/cau-final.json` (mỗi câu `key`, `form: "bai_tap"`,
   `type: multiple_choice | true_false | short_answer`, `question`, `options`+`answer` (chỉ số 0–3) / `statements[{text,answer}]` /
   `answer`, `explanation`, thêm `nguon`) và `gan-nhan.json` (`{key: {topic, difficulty: de|tb|kho}}`). Xem mẫu `…/c2/cau-final.json`.
6. **Kiểm chéo bắt buộc**: một subagent Sonnet đóng vai học sinh làm 20 câu CHƯA xem lời giải → đối chiếu đáp án; lệch thì sửa hoặc bỏ
   câu (không giải lại nhiều lần — `feedback_bo_cau_mo_ho`). Sau đó `kiem-code` soát: đáp án duy nhất, đơn vị, KaTeX hợp lệ, không
   ngoài chương trình, không câu nào giống đề sách.
7. Lập bản duyệt HTML cho thầy: `npx tsx scripts/lap-duyet-html.mts` (đọc đầu file để biết tham số) hoặc file HTML tương đương trong
   `docs/ra-soat/cau-hoi-hrw-c3.html`; commit `-- scripts/data/nap-ngan-hang-vl12/hrw-c3/ docs/ra-soat/ docs/prompt-cau-hoi-phong-theo-hrw.md`,
   push. Báo một lần: số câu theo loại/mức/bài, 3 câu thầy nên xem kỹ nhất. **Dừng chờ thầy duyệt. Chưa ghi DB.**

## Giai đoạn 3 — ghi DB + đo, rồi mở rộng (sau khi thầy duyệt)

- Ghi: `VL_GRADE=12 VL_TOPICS=scripts/data/nap-ngan-hang-vl12/chu-de-lop12.json VL10_DIR=scripts/data/nap-ngan-hang-vl12/hrw-c3 VL10_NOTE=hrw-c3-<ngày> npx tsx scripts/ghi-ngan-hang-vl10.mts`
  dry-run trước, xem `ghi-bao-cao.json`, rồi `--apply` trong tab terminal (script ghi ở trạng thái ẨN `archived=true`; thầy bật Hiện ở
  `/quan-tri/ngan-hang-cau-hoi`). 20 dòng thì không cần chờ sau 22h. Hoàn tác chỉ nêu `note`, không in lệnh xoá.
- Đo sau 2 tuần HS làm: tỉ lệ đúng và thời gian trung bình của câu `note = hrw-c3-…` so với câu cùng chủ đề; ghi vào memory
  `project_thachlab_cau_hoi_hrw.md`. HS bỏ dở nhiều hơn rõ rệt thì dừng, báo thầy.
- Mở rộng (chỉ khi thầy chốt): lặp giai đoạn 2 cho Chương 2 Khí lí tưởng (HRW ch. 18–19), Chương 1 Vật lí nhiệt (ch. 18),
  Chương 4 Hạt nhân (ch. 42–43), mỗi chương một thư mục `hrw-cN/`, một `note` riêng.

## Tiết kiệm token

- Phiên chính không đọc PDF, không đọc ảnh; `pdftotext` theo khoảng trang hẹp trong subagent. Gọi Agent **đồng bộ**, không kết thúc lượt
  khi còn agent chạy nền.
- Không báo tiến độ giữa chừng. Lỗi ghi `scripts/data/nap-ngan-hang-vl12/hrw-c3/ra-soat.md`. Commit theo đường dẫn, không `git add .`.
- Cuối phiên: Rút kinh nghiệm (3–6 dòng) ghi vào `docs/memory/project_thachlab_cau_hoi_hrw.md` (tạo mới, một dòng trỏ trong
  `docs/memory/MEMORY.md` mục "Việc mới 30/9"), dòng ĐANG CHỜ vào `docs/STATE.md` nếu còn chờ duyệt/ghi DB.
