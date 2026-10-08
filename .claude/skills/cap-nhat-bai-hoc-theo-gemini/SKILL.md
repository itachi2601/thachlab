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
| `nhan/` | Thầy (hoặc Claude lưu khi thầy dán JSON vào chat) | `hoc-sinh-<yeu|trung-binh|kha>.json`, `bai-tap-mau.json`, tuỳ chọn `dap-an-that.json`; lượt Claude (tuỳ chọn): `hoc-sinh-<vai>-claude.json` |
| `da-xu-ly/` | Claude | `so-quyet-dinh.json` (từng góp ý: chap_nhan/tu_choi/hoi_thay + ghi chú), bản bài tập mẫu đã kiểm, báo cáo ngắn |

Điều phối nhiều bài: `content/gemini/hang-doi.md` (trạng thái `chua-gui → da-gui → da-nhan → da-sua → cho-duyet → da-dang`). Cập nhật bảng này ở cuối mỗi chế độ.
Prompt gốc nằm một nơi: `references/PROMPT-GEMINI-HOC-SINH.md` (skill này) và `soan-bai-tap-mau/references/PROMPT-GEMINI-BAI-TAP-MAU.md`. Không chép sang chỗ khác.

## Chế độ 1 — `/gemini-gui <bài | chương>`

1. Xác định thư mục bài, tên bài, lớp. Nhiều bài (cả chương): lặp từng bài.
2. Xuất file: `npx tsx scripts/gemini-phan-hoi.mts --bai <thư-mục> --ten "<tên bài>" --lesson-id <id> [--vai trung-binh] --xuat` (đợt lớn chỉ vai `trung-binh`). `--lesson-id` bắt buộc: nó nhúng danh mục YCCĐ vào tin nhắn 3 (thiếu thì Gemini lạc phạm vi). Script tự ghi `nhan/dap-an-that.json` (đáp án đúng lấy từ lớp `tl-ok`) để bước nhận đối chiếu quiz; tin nhắn 3 chỉ xuất cho vai `trung-binh`.
3. Hướng dẫn thầy (ngắn): mỗi vai một cuộc chat mới trên gemini.google.com, dán lần lượt file 1 → 2 → 3 (file 3 chỉ cần ở **một** vai, nên vai `trung-binh`); lưu JSON tin nhắn 2 thành `nhan/hoc-sinh-<vai>.json`, tin nhắn 3 thành `nhan/bai-tap-mau.json`; hoặc dán JSON vào chat để Claude lưu. Đợt lớn: gợi ý lưu prompt vai vào một Gem.
4. Ghi `da-gui` vào `hang-doi.md`.

## Chế độ 2 — `/gemini-nhan <bài>`

**A. Lý thuyết** (khi có `nhan/hoc-sinh-*.json`)
1. Gộp: `python3 .claude/skills/cap-nhat-bai-hoc-theo-gemini/scripts/gop-phan-hoi.py content/lesson-samples/<bài>`. Góp ý được ≥2 vai nêu và mức `chặn` xếp trước; in phân bố đáp án quiz (so với `nhan/dap-an-that.json` nếu có: `{"cau1":"C",…}`).
1b. **Lượt Claude (tuỳ chọn, ~vài cent/bài với Sonnet)**: chạy khi thầy bảo "thêm lượt Claude", hoặc khi Gemini ≤2 góp ý mà vai `trung-binh` sai ≥2 câu quiz. Giao **một subagent riêng** (Sonnet) theo `references/PROMPT-CLAUDE-HOC-SINH.md`: nó chỉ đọc `theory.src.html`, cấm đọc `gemini/nhan/` và `da-xu-ly/`; lưu `nhan/hoc-sinh-trung-binh-claude.json` (`"nguon":"claude"`, id `c1…`). Nó không đóng giả học sinh "không biết" (Claude biết vật lí và thấy đáp án trong nguồn) mà dò cơ học 4 thứ: thuật ngữ dùng trước định nghĩa · bước nhảy · ký hiệu/đơn vị/số liệu đổi giữa chừng · đáp án sai hấp dẫn nhất của từng câu quiz và bài đã nhấn chưa (`du_doan_loi_sai`). Chạy lại `gop-phan-hoi.py` ở bước 1: góp ý Gemini và Claude cùng `vi_tri`+`loai` xếp lên đầu (nhãn `trung-binh@claude`). Phiên chính vẫn là người kiểm — để cùng một Claude vừa nêu vừa kiểm thì nó tự chấm bài mình. Góp ý chỉ Claude nêu: kiểm bằng mắt như góp ý Gemini. **Nhiều bài một lượt / có credit API**: `npx tsx scripts/batch-ra-soat-bai.mts --du-toan|--gui|--nhan --cho` (Batch API, cùng prompt, tự ghi `nhan/hoc-sinh-trung-binh-claude.json` cho bài có trong `hang-doi.md`, báo cáo xếp hạng `scripts/logs/batch-ra-soat/BAO-CAO.md`).
2. **Kiểm từng góp ý, không sửa mù** (Gemini có thể sai vật lí hoặc bịa chỗ khó): chấp nhận (đối chiếu trích dẫn với `theory.src.html`; trích sai vị trí → nghi bịa) · từ chối (kiến thức ngoài chương trình, trái AI-TUTOR 9, làm bài quá dài; ghi lý do 1 dòng) · hỏi thầy (đổi cấu trúc, đổi tình huống mở bài, hai vai mâu thuẫn). Góp ý `nghi_sai_dap_an`: tự giải lại độc lập trước. Câu quiz vai `trung-binh` sai mà không góp ý nào ở đúng chỗ đó (script in dòng `!`) thì không bỏ qua: đọc lại mục liên quan, xem bài đã nhấn chỗ nhầm chưa, ghi kết luận vào `so-quyet-dinh.json` mục `quiz_sai_khong_gop_y`.
3. **Sửa tối thiểu** `theory.src.html`: không vai "thầy/cô"; chú thích nhiều ý mỗi ý một dòng; 🔑 3–6 chữ; `<`/`>` trong `$…$` viết `\lt`/`\gt`; hạn mức độ dài ở `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`; UI theo `docs/QUY-TAC-THIET-KE.md` (nêu mã quy tắc trong commit). Từ chưa giải thích → giải thích ≤1 câu ngay lần đầu, không thêm mục mới.
4. Build bài như skill `soan-bai-ly-thuyet-tuong-tac`, chụp 375px chỗ đã sửa. Ghi `da-xu-ly/so-quyet-dinh.json` (chạy lại `gop-phan-hoi.py … --danh-dau`, rồi điền quyết định).
5. Tối đa 3 vòng/bài. Dừng khi: không còn góp ý `chặn`; `tom_tat_bai_bang_loi_em` khớp mục tiêu đầu bài; `ly_do_chon` không viện kiến thức ngoài bài. Tỉ lệ quiz của Gemini chỉ để tham khảo (nó giỏi hơn HS thật) — câu nó sai là gợi ý bẫy cần nhấn, không phải thước đo bài. Vòng 2 trở đi chỉ vai `trung-binh`, chỉ gửi mục đã sửa.
6. Đăng (sau khi thầy duyệt): `bash scripts/cap-nhat-ly-thuyet.sh <theory.html|bundle.json> <lesson_id>` — chỉ ghi mục lý thuyết, tự sao lưu.

**B. Bài tập mẫu** (khi có `nhan/bai-tap-mau.json`) — làm theo skill `soan-bai-tap-mau` (đọc nó trước), điểm khác là phần nháp đã có:
0. Nháp có thể do Gemini (dán tay) hoặc do Claude qua Batch API (`scripts/batch-ra-soat-bai.mts --che-do bai-tap-mau`, tự chép vào `nhan/bai-tap-mau.json` nếu chưa có, đã chạy kiểm máy — xem `scripts/logs/batch-ra-soat/BAO-CAO-BAI-TAP-MAU.md`). Nguồn nào cũng đi đủ các bước dưới.
1. Kiểm máy: `python3 .claude/skills/soan-bai-tap-mau/scripts/kiem-ban-nhap-gemini.py content/lesson-samples/<bài>/gemini/nhan/bai-tap-mau.json --lesson-id <id>` (đúng 4 dạng, `cap_do` 1→4, tính lại `kiem_tinh`, trích đề, từ cấm, YCCĐ). Có ✗ thì sửa trước; mục `dieu_ban_khong_chac` tự giải lại đầu tiên. **0/4 YCCĐ khớp = lạc phạm vi**: không viết lại, chuyển file sang `da-xu-ly/bai-tap-mau.loai-vongN.json`, xuất lại tin nhắn 3 (có danh mục YCCĐ) cho thầy dán. Số học đúng hết không có nghĩa là bám bài — đọc 4 đề bằng mắt, so với các mục của bài.
2. **Không đăng nguyên văn**: viết lại lời giải theo "Phong cách" của `soan-bai-tap-mau` (khung kiến thức, bước đánh số, ⚠ điều kiện, nhận dạng), giữ cấu trúc bắc cầu (`cau_noi`), dựng mô phỏng + bảng phân tích, khớp `topic` với `question-topics.json`, lưu `scripts/data/bai-tap-mau/<id>.json`.
3. Kiểm chéo độc lập bằng `kiem-code` (tự giải không nhìn lời giải) → `review.checked: true` → validate → thầy duyệt → đăng `npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --dry-run` rồi bỏ `--dry-run` (`--giu-cu` nếu bài đã có dạng cũ). Chạy lệnh ghi DB trong tab terminal của thầy.
4. Lưu bản đã kiểm vào `da-xu-ly/`. Ghi trạng thái vào `hang-doi.md`.

## Ranh giới
- Chỉ gửi nội dung bài cho Gemini; **không** gửi tên, điểm, SĐT học sinh.
- Lời giải/đáp án do model ngoài sinh luôn được Claude tính lại trước khi đăng.
- Lượt Claude chạy bằng subagent tách biệt, không thấy kết quả Gemini; người kiểm vẫn là phiên chính. Không gửi gì ra ngoài Claude cho lượt này.
- Học sinh ảo giỏi hơn học sinh thật; vai `yeu` phải ép giả vờ không biết. Sau khi đăng, đối chiếu số liệu làm bài thật của lớp.
- Hai điểm thầy duyệt mỗi bài: các góp ý `hoi_thay`, và bản cuối trước khi đăng. Không tự đăng.

## Gemini desktop (Mac) ghi thẳng vào repo (thầy xác nhận 8/10/2026)
Gemini desktop có quyền vào `/Users/MAC/Projects/thachlab`. File 2 và 3 do `--xuat` sinh đã chứa lệnh "tự ghi JSON vào `<đường dẫn tuyệt đối>/gemini/nhan/…`" — thầy chỉ dán 1→2→3, KHÔNG dán JSON lại cho Claude. Sau khi thầy báo "xong", Claude đọc `nhan/`, kiểm JSON hợp lệ rồi chạy chế độ 2. Sửa script `--xuat` thì giữ phần `luu()`.

## Nhật ký rút kinh nghiệm (cập nhật cuối MỖI phiên dùng skill này — xem `AGENTS.md`)

- 2026-10-08 · Gộp 2 skill (phản hồi học sinh ảo + nháp bài tập mẫu) thành một; thầy dùng Gemini Pro web, không API (Gemini CLI đăng nhập Google bị bỏ vì hạn mức riêng, không phải gói Pro) → mặc định dán tay, hỏi trước thầy dùng Gemini qua đường nào. Chưa chạy vòng thật: sau bài đầu ghi lỗi hay gặp của Gemini và mức công Claude phải viết lại.
- 2026-10-08 · Thầy hỏi vì sao không bắt Gemini tự tạo JSON trong nhan/ → Gemini desktop ghi được file; đưa đường dẫn lưu vào chính prompt xuất, đừng bắt thầy dán lại.
- 2026-10-08 · Vòng thật đầu tiên (Bài 9 L12 *Khái niệm từ trường*): (a) Gemini nháp 4 dạng đều về góc từ khuynh — thứ bài không dạy — mà `kiem-ban-nhap` chỉ cảnh báo YCCĐ, máy báo "0 lỗi" → đã đổi 0/4 khớp thành lỗi và nhúng danh mục YCCĐ vào prompt (`--lesson-id`); bài ít số liệu thì Gemini bịa công thức để "có số mà tính". (b) Phiên xử lý không đối chiếu được quiz vì không có `dap-an-that.json` dù đáp án nằm sẵn ở lớp `tl-ok` → `--xuat` tự sinh. Nó cũng đếm nhầm "bundle 5 câu" (đó là đề Luyện tập trong bundle, không phải quiz trong bài). (c) Góp ý "1/8 không phải công thức chung" là đúng nhưng phiên sửa thành "chỉ đúng riêng thí nghiệm này" — sai vật lí (1/d³ là quy luật nam châm ở xa). Chấp nhận góp ý ≠ chấp nhận câu chữ Gemini đề xuất; viết lại cho đúng. (d) Gemini sai câu 1 ("hai dây cùng chiều đẩy nhau"): coi là bẫy thật cần nhấn, không phải thước đo 90%.
- 2026-10-08 · Thêm lượt Claude (bước 1b) sau khi xem vòng thật L12: cả 3 góp ý Gemini đều thuộc loại cấu trúc (mơ_hồ/nhảy_bước/lặp_ý) mà Claude dò được bằng văn bản, và 2 câu quiz sai (cau1, cau6) không có góp ý nào đi kèm. `gop-phan-hoi.py` nay tách nguồn (`nguon` → nhãn `vai@claude`), in `du_doan_loi_sai`, cảnh báo quiz sai không có góp ý, và không còn lỗi `KeyError` khi `so-quyet-dinh.json` viết tay thiếu khoá `files`. Chưa chạy lượt Claude thật: sau 3 bài đầu ghi tỉ lệ chấp nhận của Gemini so với Claude và số góp ý trùng nhau, rồi quyết định có giữ mặc định không. Giới hạn đã biết: gộp theo chuỗi `vi_tri`+`loai` nên trùng nhau chỉ khi Claude chép đúng tên mục (prompt đã dặn).
- 2026-10-08 · Thầy có $100 credit API (hết hạn 22/10) không dùng được cho Claude Code → viết `scripts/batch-ra-soat-bai.mts` chạy lượt Claude (1b) hàng loạt qua Batch API (giá ½, structured output để JSON không vỡ, system prompt lấy thẳng từ `PROMPT-CLAUDE-HOC-SINH.md` — sửa prompt một nơi). Chưa chạy thật: sau batch đầu ghi tỉ lệ góp ý chấp nhận được và có cần hạ xuống Sonnet không.
- 2026-10-08 · Thêm chế độ `--che-do bai-tap-mau` vào script batch (cùng prompt `PROMPT-GEMINI-BAI-TAP-MAU.md`, structured output, tự chạy `kiem-ban-nhap-gemini.py`, báo cáo xếp bản sạch lên đầu). Chưa chạy thật: sau batch đầu so tỉ lệ lạc phạm vi của Claude với Gemini (Bài 9 Gemini 0/4 khớp YCCĐ).
