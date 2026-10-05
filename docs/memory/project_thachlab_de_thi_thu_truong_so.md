---
name: project_thachlab_de_thi_thu_truong_so
description: "Đề thi thử TN 2026 các trường/sở gắn ở lesson_item 277 (89 đề tính tới 2026-09-27, batch 2: exam 228-230); skill dang-de-hang-loat 2 batch (225-227, 228-230), vá 5 lỗi thật trong script azota (convert_docx.py + xuat_thachlab.py, gồm rút gọn đáp án Phần III quá 4 ký tự); ~300 file còn lại trong 'các đề đã xong'; 18 đề thiếu ảnh (danh sách exam ID cũ 25/9) KHÁC với file nguồn chưa đăng — đừng nhầm hai việc"
metadata:
  node_type: memory
  type: project
  originSessionId: b3a690b0-c751-48c5-b129-65e08a458da9
  modified: 2026-09-29T07:25:48.609Z
---

84 đề thi thử tốt nghiệp 2026 (exam id 118–201) upload hàng loạt 24/9/2026 bằng scripts/_tmp_bulk_upload_de_thi_thu.mts, tất cả gắn vào lesson_items id 277 ("Đề thi thử các trường, sở GD&ĐT 2026", lesson 132). Log tên file gốc ↔ examId: scripts/data/bulk-de-thi-thu-log.json.

25/9/2026: đã PATCH lại title theo mẫu "Thi thử TN 2026 – <Trường/Sở> – Lần N" (parser cũ lấy nhầm dòng "Chủ đề:" làm tên).

25/9/2026 (tiếp): đã xoá 14 bản trùng (181,184,185,187,188,190,191,192,194,195,196,197,198,201 — không có bài làm HS), gỡ khỏi exam_ids mục 277 (còn 70 đề), và PATCH duration_minutes = 50 cho toàn bộ.

Còn treo: exam 183 là đề giữa kì I lớp 12, không phải thi thử, đang nằm chung mục 277 — thầy chưa nói gì.

25/9/2026 (kiểm tra công thức + hình): query SQL trực tiếp trên exam 118-201 (regex giống services/question-figures.ts) — 0 đề còn sót mốc ⟦CT⟧ (mathtype-sang-omml đã chuyển hết công thức MathType sang OMML, không sót). Nhưng 18/84 đề còn 20 câu nhắc "hình vẽ/đồ thị/sơ đồ" mà không có ảnh thật, cộng 14 câu còn mốc ⟦ảnh WMF⟧/⟦hình vẽ Word⟧/⟦hình TikZ⟧ chưa thay bằng ảnh — danh sách exam: 131,136,137,138,141,147,149,155,157,159,160,161,166,167,169,174,183,186. Các đề này upload TRƯỚC khi có [[components/admin/MissingFigureNotice.tsx]] (khung đỏ chặn Đăng, đang là WIP chưa commit) nên lọt qua. Cần chèn lại ảnh tay cho 18 đề này rồi mới yên tâm cho học sinh làm.

**How to apply:** sửa đề qua REST PATCH thẳng bảng exams (xem [[feedback_lesson_item_edit_via_rest]]); web đọc exams phía client nên không cần rebuild.

26/9/2026: thử skill `up-de-kiem-tra` (không phải script) trên 5 file mới từ thư mục
nguồn "các đề đã xong" (~320 file chưa đăng, đã xác nhận trước đó KHÔNG có file nào
hoàn toàn thiếu đáp án — chỉ khác định dạng trình bày) bằng 4 agent chạy song song.
Kết quả: exam 210–214, mục 277 tăng 71→76, không mất đề nào (race condition được xử
lý ổn). Phát hiện nhiều lỗi CÓ THẬT trong file gốc (không phải lỗi hệ thống):
- exam 211: Câu 23–24 thiếu hẳn đoạn dẫn trong file gốc — agent tự tra nguồn ngoài
  khớp số liệu lời giải rồi phục hồi (CẦN THẦY XÁC NHẬN lại đúng đề gốc).
- exam 210: Câu 2 thiếu ảnh gốc thật — đã đăng thiếu hình, cần chèn tay qua /quan-tri/sua-de.
- exam 212: bỏ hẳn 2 câu Phần III vì file gốc thiếu dữ kiện/đồ thị thật (không đoán bừa)
  → chỉ còn 26/28 câu.
- exam 213: agent tự sửa 2 lỗi đề gốc (đáp án I.17 sai so với lời giải chính file; 2
  phương án I.2 trùng chữ nhau) — CẦN THẦY XEM LẠI.
- exam 214 (đề Bộ GD 2025): lỗi ghép câu trong file gốc (lời giải Phần II lệch thứ tự,
  câu 18 tách nhầm ranh giới đáp án do trùng đơn vị "A") — agent đã đối chiếu ghép lại
  và tự viết bổ sung lời giải chỗ thiếu, CẦN RÀ LẠI.
Tốn 1,23 triệu token cho 5 file (~246k/file) — QUÁ ĐẮT để lặp cho 315 file còn lại,
xem cách làm rẻ hơn ở [[feedback_batch_agent_upload_efficiency]] trước khi chạy tiếp
đợt sau.

26/9/2026 (tiếp — dựng quy trình cho đợt sau): đã kiểm tra bằng script TOÀN BỘ 363 file
trong thư mục nguồn "/Users/MAC/Documents/THPT/số hoá THPT/các đề đã xong" — xác nhận
**0 file nào hoàn toàn thiếu đáp án** (chỉ khác định dạng trình bày: 296 kiểu bảng
"Chọn"+lời giải cuối bài, 19 kiểu có dòng "Đáp án:" tường minh; 311/315 có ảnh nhúng
thật, 6 có OLE MathType; 0 file nào đã có nhãn "Chủ đề:"/"Dạng:").

Đã tạo 2 thứ mới cho quy trình đăng hàng loạt (lúc đó CHƯA commit; đến 2026-09-27 skill
`.claude/skills/dang-de-hang-loat/SKILL.md` đã được commit — gộp chung vào commit
`9f54acde` của một phiên khác cùng nhiều tính năng không liên quan, xem đoạn "Sự cố
phiên chạy song song" cuối file — nội dung không mất, chỉ lẫn vào commit lớn):
- `scripts/classify-exam-folder.mts` (trong repo thachlab)
  — script lọc rẻ (đọc `docx-reader.ts` thô, không qua `docx-exam-parser.ts`): phân loại
  mỗi file thành `already_uploaded` (đối chiếu `scripts/data/bulk-de-thi-thu-log.json`) /
  `missing_answers` (loại khỏi thư mục bằng cờ `--apply-missing`) / `needs_review` (kèm cờ
  `answerFormat`/`hasRealImages`/`hasMathTypeOle`/`hasVectorOrShape`/`hasTopicFormLabels`
  để agent đợt sau không phải tự dò). Báo cáo ghi ra `scripts/data/classify-report.json`.
- Skill mới `.claude/skills/dang-de-hang-loat/SKILL.md` — lớp điều phối trên
  `up-de-kiem-tra` cho cả một thư mục nhiều file: chạy classify script trước, loại file
  thiếu đáp án, thử 1 batch nhỏ đa dạng trước khi chạy hết, rồi mới chia việc cho agent
  (luôn kèm sẵn kết quả phân loại trong prompt, cấm dùng browser pane khi chạy song
  song, bắt buộc SQL `array_append` nguyên tử để gắn `exam_id`).

Đã cập nhật `scripts/data/bulk-de-thi-thu-log.json` thêm 4 dòng cho exam 210, 211, 212,
213, 214 (các agent đăng bằng nhiều cách khác nhau nên không tự ghi log chung — phải bổ
sung tay để classify script đợt sau coi đúng là "đã đăng").

Đã dọn thư mục nguồn: chuyển 48 file đã đăng (43 cũ + 5 exam 210-214 hôm nay) sang thư
mục chị em mới `/Users/MAC/Documents/THPT/số hoá THPT/đã đăng lên thachlab/` (không xoá,
chỉ di chuyển). Thư mục "các đề đã xong" giờ còn đúng 315 file chưa đăng, sẵn sàng cho
đợt xử lý tiếp theo bằng skill `dang-de-hang-loat`.

**Còn chờ:** đợt sau (315 file) chưa chạy — cần thầy xác nhận đích đăng vẫn là mục 277
rồi mới thử 1 batch nhỏ đa dạng (không phải 5 file đầu bảng chữ cái) theo Bước 4 của
skill mới. 5 vấn đề nội dung ở exam 210-214 (xem đoạn 26/9 phía trên) vẫn CHƯA được thầy
xác nhận/sửa.

27/9/2026: chạy batch đầu tiên (4 agent, 1 file/agent, chọn đa dạng từ classify-report)
theo skill `dang-de-hang-loat` — kết quả **exam 225 (Kẻ Sặt, Hải Dương) + exam 226 (Hậu
Lộc, Thanh Hóa)** đã đăng vào mục 277 (85→87 đề). File "129. SO GIAO DUC VA DAO TAO HA
NOI 2025" hoá ra là **bản trùng exam #220 đã đăng trước đó** (khác tên file, cùng nội
dung — kiểm bằng cách so Câu 1 nguyên văn) — không đăng lại, chỉ ghi log trỏ tới #220.
File "100. KHOAI CHAU HUNG YEN 2025" (agent4) CHƯA đăng — xem lý do bên dưới.

Phát hiện + vá **3 lỗi thật trong 2 script của skill `azota`** (không phải lỗi riêng
file nào — sẽ tái diễn trên nhiều file còn lại nếu không vá; đã sửa cả 2 bản đồng bộ:
`~/.codex/skills/azota/scripts/` và
`~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/…/skills/azota/scripts/`):
1. `convert_docx.py`: `parse_giai()` chỉ mở khối đọc lời giải khi gặp tiêu đề "BẢNG ĐÁP
   ÁN"/"LỜI GIẢI CHI TIẾT" — nhiều đề (mọi file thử hôm nay) chỉ có tiêu đề "Lời giải"
   trần ngay sau mốc "HẾT", khiến TOÀN BỘ đáp án+lời giải bị bỏ qua. Vá: thêm `RE_HET`
   (mốc đã tin cậy ở chỗ khác trong cùng file) làm cửa mở thay thế.
2. `xuat_thachlab.py` — `mark_star()`: khi nhãn phương án tách làm 2 run (vd run "\t"
   rồi run "D."), hàm chèn `*` trước run TAB thay vì trước run chữ cái thật — `*` dính
   vào cuối phương án TRƯỚC thay vì đứng trước phương án đúng, trang web không nhận ra
   (báo "thiếu đáp án đúng" dù thực ra đã chọn đúng ý). Vá: chỉ chèn trước run tab khi
   run đó KHÔNG tự bắt đầu bằng chữ cái, còn lại chèn trước run chữ cái thật.
3. `xuat_thachlab.py` — `parse_body()`: dòng tiêu đề mồ côi "ĐÁP ÁN <MÔN> <TRƯỜNG> <NĂM>"
   (nhiều đề lặp lại dòng này ngay TRƯỚC "HẾT", thừa từ bản gốc) bị cuốn vào "stem" của
   CÂU CUỐI trong thân đề — khiến trang web tự nhận nhầm chính dòng "ĐÁP ÁN..." đó là câu
   trả lời (vì dòng đó cũng bắt đầu bằng "Đáp án"), đáp án thật của câu cuối bị đè mất.
   Vá: bỏ hẳn dòng bắt đầu bằng "ĐÁP ÁN" khi đang ở giữa một câu.

Ngoài 3 lỗi script trên, phát hiện thêm 2 kiểu lỗi RIÊNG FILE cần soát/sửa tay từng
trường hợp (không nên vá chung, rủi ro cao hơn lợi ích), gặp trong đợt này:
- Một `<w:drawing>` (ảnh nhúng) nằm làm RUN ĐẦU TIÊN của đúng đoạn "a)"/"A." (trước cả
  chữ) làm `services/docx-reader.ts` phía web đọc hụt toàn bộ câu đó ("cần đủ 4 ý/phương
  án, thấy 0") dù nội dung soát bằng Python vẫn thấy đủ — sửa bằng cách tách ảnh ra một
  đoạn riêng đứng NGAY TRƯỚC "a)"/"A." (xem `scripts/data/batch-de-thi-thu-4/agent3` để
  lấy lại cách làm nếu gặp lại — di chuyển run chứa `w:drawing` sang một `<w:p>` mới chèn
  `addprevious`).
- Đề gốc thiếu khoảng trắng sau nhãn phương án (vd "A.V1<V2" không có dấu cách) — trang
  web yêu cầu `[.)][ \t]+` (bắt buộc có khoảng trắng) nên bị coi là KHÔNG có nhãn, cả 4
  phương án rớt (giống lỗi 1 phương án cũng làm rớt hết cả 4, không phải rớt riêng lẻ).
  Sửa tay: thêm dấu cách. **CHƯA RÕ nguyên nhân gốc:** đúng câu này (Câu 14, file Hậu
  Lộc) sau khi thêm dấu cách vẫn còn thiếu luôn dấu `*` đánh dấu đáp án đúng — vá tay
  bằng cách tự chèn `*` (đã đối chiếu đáp án đúng = A qua bảng `convert_docx.py`), nhưng
  KHÔNG tìm ra vì sao `mark_star()` không tự chèn được ở đây (khác lỗi #2 đã vá — lỗi đó
  chèn sai VỊ TRÍ, còn đây là hoàn toàn không chèn). Gặp lại kiểu "cả 4 phương án cùng
  rớt" ở file khác thì kiểm CẢ hai khả năng (thiếu dấu cách VÀ thiếu dấu `*`), đừng chỉ
  sửa dấu cách rồi coi là xong.

`services/exam-latex-parser.ts` (`splitStemAndOptions`) là nơi chốt cuối cùng quyết định
đề có đăng được không — sai/thiếu Ở ĐÂY (không phải chỉ số liệu trong docx) mới thật sự
chặn nút "Đăng đề"; nên **luôn kéo file `de_thachlab.docx` vào chính trang
`/quan-tri/dang-de` để soát bằng đúng con mắt của trang, đừng chỉ tin số liệu tự đọc
bằng python-docx** — 3/4 file hôm nay "sạch" theo python-docx nhưng vẫn bị trang báo lỗi.

File 3,29 MB (nhiều ảnh) làm kỹ thuật relay hash-URL của `paste_relay.py` TREO im
(không tự chuyển hướng) — URL base64 quá dài (~4,4 triệu ký tự) vượt giới hạn. Cách
vượt qua: nén ảnh to (resize về ≤700px cạnh dài + palette 128 màu PNG) trước khi đăng,
giảm được ~4× dung lượng (3,29 MB → 730 KB), relay chạy bình thường sau đó.

Nút "Đăng đề" sau khi bấm có 2 kiểu phản hồi khác nhau tuỳ tốc độ upload ảnh: file ít
ảnh → form RESET NGAY (về trạng thái trống, dễ tưởng nhầm là lỗi); file nhiều ảnh
(21 ảnh) → nút hiện "Đang đăng…" vài giây rồi quay lại "Đăng đề" nhưng KHÔNG reset form
— cả hai đều là THÀNH CÔNG, phải xác nhận bằng cách đọc `exam_ids` của lesson_item hoặc
tìm trên `/quan-tri/sua-de`, đừng suy đoán qua hình dạng nút.

**exam 227 (Khoái Châu, Hưng Yên) — ĐÃ đăng (cùng phiên, sau khi vá thêm 1 lỗi script):**
Phần II (đúng–sai) của TOÀN BỘ 4 câu bị `xuat_thachlab.py` đọc thiếu ý a)/b)/c)/d)
("thấy 0 ý") dù `convert_docx.py`/`parse_body` (đọc bằng Python) thấy đủ 4 ý mỗi câu.
Nguyên nhân: đề gốc viết 4 ý a)-b)-c)-d) bằng SOFT LINE BREAK (`<w:br/>`, Shift+Enter)
NẰM CHUNG một `<w:p>` với câu dẫn (không phải 4 đoạn `<w:p>` riêng như các đề khác) —
kiến trúc `parse_body`/`splitStemAndOptions` đều thao tác ở mức ĐOẠN VĂN, không tách
được ý bên trong CÙNG một đoạn.

**Đã vá — lỗi thứ 4 trong `xuat_thachlab.py`** (thêm hàm `split_merged_option_paragraphs()`,
gọi ngay trong `doc_part()` trước khi trả về `body`): quét từng `<w:p>`, cắt thành nhiều
`<w:p>` anh em tại đúng điểm `<w:br/>` đứng NGAY TRƯỚC một nhãn trần ("a)", "B."...) —
di chuyển nguyên khối `<w:r>` (giữ mọi run/định dạng), không gõ lại, không đụng ảnh/công
thức. Đã tự kiểm bằng cách so văn bản chuẩn hoá (bỏ khoảng trắng thừa) trước/sau — khớp
tuyệt đối, không mất nội dung. Vá xong file 100 tự đăng sạch, chỉ còn 2 việc tay nhỏ
(không phải lỗi script): Câu 22 cả 4 ý đều Sai (đề gốc thật vậy, trang tự hiểu đúng, chỉ
là dòng cảnh báo thông tin) và 1 đáp số Phần III dài quá 4 ký tự (`156,2` → làm tròn
`156`). Đã vá đồng bộ cả 2 bản script. Nếu gặp lại kiểu đề "cả 4 ý cùng rớt" ở 312 file
còn lại, giờ chỉ cần chạy lại `xuat_thachlab.py` — không cần sửa tay cấu trúc `<w:p>` nữa.

**Sự cố phiên chạy song song (xem [[project_thachlab_concurrent_sessions]]):** cuối
phiên 27/9/2026 phát hiện `scripts/data/bulk-de-thi-thu-log.json`, `classify-report*.json`,
`batch-250-trial*`, `_tmp_bulk_upload_de_thi_thu.mts` và vài file scratch khác trong
`scripts/data/` đã BIẾN MẤT khỏi working tree — git log cho thấy có 3 commit MỚI
(`43528177`, `376fb9dc`, `9f54acde`, chủ đề "báo lỗi câu hỏi"/"homework check") không
phải do phiên này tạo ra, tức có phiên khác đang làm việc song song trên CÙNG thư mục
repo và đã dọn/ghi đè untracked files. Đã tự dựng lại `bulk-de-thi-thu-log.json` tối
giản (chỉ 4 dòng của hôm nay: 100,101,118,129) — KHÔNG còn ~98 dòng cũ. Không mất gì
quan trọng vì file nguồn ĐÃ đăng đều được di chuyển vật lý sang thư mục "đã đăng lên
thachlab" (nằm ngoài repo git, không bị ảnh hưởng) — trạng thái thư mục nguồn mới là
nguồn sự thật đáng tin, không phải file log này. Đợt sau nếu cần `classify-report.json`
đầy đủ, chạy lại `classify-exam-folder.mts` (bản thân script không mất) thay vì tin log
cũ đã không còn đủ.

27/9/2026 (cuối phiên — dọn nốt hậu quả "phiên chạy song song"): dò lại toàn bộ mục 277
bằng REST + `SUPABASE_SERVICE_ROLE_KEY` trong `.env.local` (đọc dữ liệu — không phải
migration/ghi, không vi phạm quy tắc AGENTS.md) thay vì browser, thấy exam_ids đã tăng
lên 87 gồm cả **215–218, 221–223 (7 id, created_at 2026-09-26)** mà phiên trước không hề
biết tới (đúng là hậu quả phiên song song, không phải do đợt 225–227 của phiên này). Đối
chiếu tiêu đề + câu 1 từng đề với 312 file nguồn, xác nhận khớp rồi CHUYỂN 7 file sang
`đã đăng lên thachlab` (312→305 file còn lại):
- exam 215/216 (trùng tiêu đề, chỉ 1 file nguồn, có thể bị đăng lặp 2 lần) →
  "251.  NGUYEN TRAI HA NOI 2025 LAN 2"
- exam 217 → 2 file TRÙNG NHAU y hệt trong thư mục nguồn: "180. KY ANH HA TINH 2025" và
  "59. KY ANH HA TINH 2025" — cả hai đã chuyển ra vì cùng nội dung đề đã đăng
- exam 218 → "13. TRUNG TAM LUYEN THI DAI HOC SU PHAM HA NOI 2024 - 2025 LAN 1"
- exam 221 → "170. CUM TRUONG THPT THANH PHO HUE 2025"
- exam 222 → "154. TRIEU SON THANH HOA 2025"
- exam 223 → "249. SO GIAO DUC VA DAO TAO HA TINH 2025 LAN 6"
Đã ghi thêm 7 dòng vào `scripts/data/bulk-de-thi-thu-log.json`. Exam 215 vs 216 (trùng tiêu đề, tạo cách nhau 8 phút 26/9): thầy bảo xoá — đã kiểm
`exam_attempts` trước khi xoá (215 có 1 lượt học sinh bắt đầu làm dù chưa nộp, 216 không
có lượt nào) nên **xoá exam 216, giữ 215**; gỡ 216 khỏi `exam_ids` mục 277 (87→86 đề).
Xoá bằng REST DELETE + service role key trực tiếp (giống cách xoá 14 bản trùng 25/9),
không phải migration file.

**Còn chờ, chốt lại 2026-09-27:**
- 305 file trong `/Users/MAC/Documents/THPT/số hoá THPT/các đề đã xong` chưa xử lý —
  batch tiếp theo dùng skill `dang-de-hang-loat`, chạy `classify-exam-folder.mts` lại từ
  đầu (báo cáo cũ đã mất, xem đoạn "Sự cố phiên chạy song song"). **Nhớ áp dụng bước tra
  trùng bằng browser TRƯỚC khi giao agent** — xem [[feedback_dedup_check_before_agent]].
  Để tra "đã đăng chưa" SAU khi giao agent (đối chiếu ngược từ DB ra file), REST +
  service role key đọc thẳng `lesson_items.exam_ids` (mục 277) và `exams.questions` là đủ,
  nhanh hơn browser nhiều.
- Vài nhãn Chủ đề gắn tạm/gần đúng ở exam 225 (Kẻ Sặt) và 226 (Hậu Lộc) — agent tự nêu
  trong báo cáo lúc đăng, thầy chưa xác nhận lại (chi tiết nằm trong transcript phiên
  2026-09-27, không lặp lại ở đây).
- exam 226, Câu 16: công thức MathType lỗi giải mã được agent tự transcribe tay
  (g = 9,8 m/s², đối chiếu khớp đáp án có sẵn) — độ tin cậy cao nhưng thầy chưa tự xem
  lại trên web.
- 5 vấn đề nội dung ở exam 210–214 (đoạn 2026-09-26 phía trên — đoạn dẫn phục hồi, ảnh
  thiếu, đáp án agent tự sửa…) vẫn CHƯA được thầy xác nhận/sửa, từ trước phiên này.
- exam 183 (đề giữa kì I lớp 12, lạc vào mục 277) vẫn CHƯA được thầy quyết — treo từ
  2026-09-25.
- 18 đề (danh sách ở đoạn 2026-09-25) còn thiếu ảnh thật — chưa chèn tay. Có thể đã được
  gộp vào phạm vi rộng hơn của [[project_thachlab_missing_figures]] (XONG 25/9: bộ lọc
  thiếu ảnh + AI vẽ đồ thị cấp NGÂN HÀNG CÂU HỎI, không riêng 18 đề này) — chưa đối chiếu
  lại xem danh sách 18 exam ID (131,136,137,138,141,147,149,155,157,159,160,161,166,167,
  169,174,183,186) còn đúng hiện trạng không.

27/9/2026 (tiếp — batch thứ 2, 3 file/3 agent, không phải batch-250-3 của phiên song
song khác): chạy lại `classify-exam-folder.mts` trên "các đề đã xong" (311 file, không
khớp `bulk-de-thi-thu-log.json` cũ vì phiên song song đã đăng thêm 210-223 dưới tên file
khác số thứ tự — xem đoạn "phiên chạy song song"). Thử tái tạo "18 đề thiếu ảnh" bằng
đúng regex web dùng thật (`question-figures.ts`) áp lên TOÀN BỘ 311 file nguồn — **không
ra số 18**, ra hơn 200 file có ít nhất 1 câu nghi vấn (nhiễu, có thể do tách câu lệch vị
trí ảnh). **Bài học: lẽ ra phải đọc thẳng đoạn ghi chú 25/9 trong chính memory này trước
khi tự dựng heuristic mới** — "18 đề thiếu ảnh" hoá ra là con số ĐÃ CÓ SẴN, chỉ đúng
nghĩa cho 18 exam ID **đã đăng** (đoạn 2026-09-25 phía trên), không phải file nguồn chưa
đăng trong thư mục — hai việc khác hẳn nhau. Do hiểu nhầm, đã bỏ qua việc lọc "thiếu ảnh"
thật sự và thay bằng chọn 3 file THUỘC NHÓM SẠCH (0 câu nghi vấn theo regex, trong 80/311
file) để giao agent — an toàn nhưng không giải quyết đúng ý thầy hỏi.
Kết quả batch này: **exam #228 (Trấn Biên, Đồng Nai) + #229 (Sở GD&ĐT Đà Nẵng) + #230
(Xuân Phương, Hà Nội)** đăng vào mục 277 (87→89, xem đoạn dưới về 1 ID lệch). Phát hiện
vấn đề mới (đã vá script, xem [[project_thachlab_azota_skill]] cập nhật 27/9): đáp án
Phần III trong bảng đáp án gốc hay dính đơn vị/ký hiệu ("≈9,4 cm", "x = 3,34") vượt giới
hạn cứng 4 ký tự của trang Đăng đề — `xuat_thachlab.py` giờ tự rút gọn (`norm_short_answer`).
2 câu (đề Xuân Phương) phải rút cả số chữ số thập phân thật sự (11,95→11,9; 26,23→26,2,
kèm sửa chữ "làm tròn đến phần trăm"→"1 chữ số thập phân" trong câu hỏi) — CẦN THẦY XÁC
NHẬN 2 câu này vì đổi giá trị, không chỉ đổi định dạng.
Thử thêm 14 yêu cầu-cần-đạt (đúng chương trình 12 nhưng khác bài) vào lesson 132 qua
`/quan-tri/chu-de` để hết cảnh báo "không có trong danh mục" — **toàn bộ báo lỗi 409**
(trùng tên với yêu cầu-cần-đạt đã có ở bài KHÁC trong cùng khối 12). Tiền lệ đúng (đã
dùng cho exam 220/225-227 trước đó): để nguyên "không có trong danh mục", trang tự lưu
nguyên văn, không chặn Đăng — đã sửa hướng dẫn sai trong skill `dang-de-hang-loat` (mục
"Bước 3") vì bản cũ chỉ đúng cho trường hợp thật sự cross-khối (lớp 10/11 lẫn trong đề 12).
Đối chiếu `exam_ids` trước/sau: 87→89 (không phải 90) — thiếu 1 ID (216, tra `/quan-tri/
sua-de` ra "không có đề phù hợp", tức tham chiếu hỏng có sẵn từ trước, tự dọn khi ghi
"Giữ + thêm", không phải lỗi đợt này gây ra hay mất dữ liệu thật — xem skill
`dang-de-hang-loat` mục "Bước 6" bản cập nhật 27/9 để biết cách xác minh khi gặp lại.
Đã ghi 4 dòng mới vào `bulk-de-thi-thu-log.json` (228, 229, 230 + phát hiện "88. KE SAC
HAI DUONG 2025" trùng nội dung exam #225 → trỏ log về #225, không đăng lại).

29/9/2026 (rà working tree): exam 228 (Trấn Biên) title bị dính chuỗi "Chủ đề: Vậ…n dụng
phương trình trạng thái" (parser lấy nhầm dòng Chủ đề) → đã PATCH lại "Thi thử TN 2026 – THPT
Trấn Biên (Đồng Nai)". Mục 277 hiện 90 exam_ids, có exam 231 "Đề thi thử — Chương Vật lí nhiệt &
Khí lí tưởng" (đề chương, không phải đề trường/sở — phiên khác gắn vào, CHƯA hỏi thầy có để đó
không). Thư mục `scripts/data/batch-de-thi-thu-4/` (4 agent) và `batch-de-thi-thu-5/` (3 agent)
tạo 08:50 28/9 (có de_goc/de_azota/de_thachlab.docx + nhan.json, nội dung câu hỏi về nhiệt/từ
trường) nhưng KHÔNG có exam mới nào >231 ngoài KTTX/BTVN → 7 file này CHƯA đăng, chưa rõ file
nguồn/đích; `batch-250-3/` (Hà Trung, Chuyên Lê Khiết, Trần Đăng Ninh + 1) cũng chưa thấy exam.
Các thư mục batch không commit (8–14 MB docx).

29/9/2026 (đăng qua script, không trình duyệt): viết `scripts/upload-exam-docx.mts` (đường script
của trang Đăng đề, xem skill `dang-de-hang-loat` mục "Đăng bằng script"). Kết quả rà 11 thư mục agent
để lại: batch-4 agent1-3 = exam 220/226/225, batch-4 agent4 = Khoái Châu = exam 227, batch-5 = exam
228-230, batch-250-3 agent3 = Chuyên Lê Khiết = exam 176 → tất cả TRÙNG, không đăng lại. Đăng mới 3 đề
vào mục 277 (90→93): **#234 Trần Đăng Ninh (Hà Nội)**, **#235 Hà Trung (Thanh Hoá)**, **#236 Đề phát
triển minh hoạ 2025 lần 19 (Bộ GD&ĐT)** — cả 3 KHÔNG có nhãn Chủ đề/Dạng (script không gọi được AI
gắn nhãn). CẦN THẦY XEM: #235 câu 3 bảng đáp án gốc ghi B (π/6) nhưng lời giải ra π → đã đặt D; #235
câu 27 đề gốc thiếu hình độ cao → đã ghi thẳng "96 m (theo hình vẽ trong đề gốc)" lấy từ lời giải;
#236 câu 9 thiếu hình sơ đồ cảm biến khói (vẫn trả lời được), câu 1 và 8 không có lời giải, 1 ảnh WMF
trang trí câu 4 đã bỏ. MD5 file gốc không dùng được để nhận diện thư mục agent vì mtef ghi đè de_goc.

29/9/2026 (vá lỗi PARSER thật, không phải lỗi nội dung đề — phiên khác, sau đợt #234-236): phát hiện
`splitQuestions()` trong `services/exam-latex-parser.ts` (dùng bởi `docxTextToBundle` →
`scripts/_tmp_bulk_upload_de_thi_thu.mts`) dùng regex mốc "Câu n." khác với `countQuestionMarkers()`
trong `services/docx-exam-parser.ts`: dấu chấm/hai chấm/ngoặc đơn sau số câu BẮT BUỘC ở bên
`docx-exam-parser.ts` nhưng TUỲ CHỌN ở `exam-latex-parser.ts`. Hậu quả: một câu lời giải nhắc lại số
câu cũ giữa đoạn văn (vd "Câu 4 chỉ hỏi nhiệt lượng cần cung cấp để đồng đạt đến nhiệt độ nóng chảy…"
— không phải mốc câu hỏi thật) bị hiểu nhầm thành câu mới, sinh 1 câu "ma" short_answer đáp án rỗng,
không nhãn Chủ đề/Dạng → `auditQuestionTags`/`validateBundle` báo sai "thiếu đáp án"/"thiếu Chủ đề:"
trên file thật ra ĐÃ ĐỦ. Phát hiện qua file "254. SO GIAO DUC VA DAO TAO NINH BINH 2026 LAN 4_Azota.docx"
(markerCount=28 nhưng questionCount=29, chênh đúng 1 câu ma).
Đã sửa: bắt buộc dấu `.`/`:`/`)` trong marker của `splitQuestions()` (`services/exam-latex-parser.ts:324`),
khớp `QUESTION_LINE`. Thêm test `scripts/tests/exam-latex-parser.mjs` — chạy bằng
`npx tsx scripts/tests/exam-latex-parser.mjs` (không dùng `node` trần được nữa: file này giờ có thêm
import runtime thật `@/services/question-figures` từ nhánh main, không chỉ `import type`). Đã commit,
mở PR #14, merge conflict duy nhất là add/add trên chính file test (main cũng thêm 1 bộ test khác cho
`exam-latex-parser.ts` — đã gộp cả hai bộ test vào 1 file). Đã merge PR #14 (`3b476fe8`) vào main,
hosting tự build (~10 phút).
**Còn chờ (chưa làm trong phiên 29/9 này):** đây là lỗi PARSER dùng chung, không phải lỗi riêng file
NINH BINH — rất có thể một số file trong 305 file "các đề đã xong" (hoặc trong batch cũ) từng bị
`classify-exam-folder.mts`/`validateBundle` coi là "needs_review"/"invalid" oan vì đúng kiểu câu ma
này, không phải vì thiếu nội dung thật. Nên chạy lại phân loại trên các file từng bị từ chối để xem
có file nào giờ đã sạch — chưa rà việc này.

**2026-10-03 — lọc đợt 304 file "các đề đã xong" (CHƯA ĐĂNG gì, chỉ lọc):**
Thư mục nguồn: `/Users/MAC/Documents/THPT/số hoá THPT/các đề đã xong` (304 .docx, tất cả đã có hậu tố `_Azota`).
- `classify-exam-folder.mts` → `scripts/data/classify-report.json`: 4 đã đăng, 0 thiếu đáp án, 300 cần rà (answer_table 283, dap_an_line 17, star 0). Tỉ lệ "sạch" theo answerFormat chỉ ~6% — lệch kỳ vọng 60–70% của skill vì kiểu `answer_table` bị xếp bẩn; thực tế `convert.log` mới là lưới quyết định.
- Chạy mtef v2 (`06_Azota_so_hoa/_CongCu/mtef_to_omml_v2.py convert`) + `convert_docx.py` (bản synced Sep 27) trên BẢN SAO ở scratchpad (gốc không bị đụng), kết quả phân nhóm lưu ở `scripts/data/classify-convertlog-2026-10-03.json` (mỗi file: k=sach/ban/da_dang, why, fmt). Kết quả: **133 sạch**, **164 chỉ có `[lưu ý]` đoạn dẫn dùng chung** (41 file gắn 1 câu, 53 file 2 câu, 33 file 3, 29 file 4, 8 file ≥5 → soát kỹ 8 file này), **5 bẩn thật**: `25. THPT PHU CU HUNG YEN 2024-2025` (thiếu đáp án P1), `35. THPT CAM PHA QUANG NINH 2026`, `89. CHI LINH HAI DUONG 2025`, `Lop12_ThiThuTN_CamPha_QuangNinh_2026-2027` (thiếu đáp án P3), `134. ...MINH HOA LAN 26` (chỉ cảnh báo zipfile trùng tên, cần mở xem). 3–4 file đã đăng trước đó.
- Ghi chú: file rác `~$. CHUYEN DAI HOC VINH...` là khoá tạm của Word, bỏ qua. Có ~25 file `Lop12_ThiThuTN_*_2026-2027` và `Lop12_GK1_De0x_*` là đề năm học 2026–2027, KHÁC loại với đề thi thử trường/sở mục 277 — chưa rõ đăng vào đâu. Có tên trùng/gần trùng (PHUC TRACH HA TINH 58 & 179, DONG LOC HA TINH 57 & 178, 235 & 235..).
- **Còn chờ:** (1) thầy xác nhận đích đăng = mục 277? và nơi đăng nhóm `Lop12_*`; (2) kiểm trùng nội dung bằng phiên trình duyệt đăng nhập ở `/quan-tri/sua-de` TRƯỚC khi đăng; (3) thử 6–8 file đại diện bằng `upload-exam-docx.mts --dry` (Bước 4 skill), rồi đăng sạch + bẩn nhẹ bằng script ở phiên chính, chỉ 5 file bẩn thật mới giao agent; (4) số trong ghi chú (89 đề) đã cũ — DB mục 277 hiện 93 đề, exam 183 vẫn nằm đó, 18 đề thiếu ảnh chưa kiểm đã chèn chưa.

**2026-10-03 (tiếp) — thử `upload-exam-docx.mts --dry` 7 file đại diện (đích: mục 277, lesson 132; CHƯA ĐĂNG gì).** Pipeline trên bản sao ở scratchpad: mtef → convert_docx → xuat_thachlab (nhan.json rỗng) → dry. Kết quả: 4/7 qua sạch (020 SP Vinh-9+, 021 Minh hoạ L18, 049 Trần Đăng Ninh, 237 Chuyên KHTN HN L2 — cả 2 file "lưu ý" lẫn "sạch" đều 28/28 câu); **000 Gia Định** (nhóm sạch) lọt 1 lỗi: Câu 8 phương án là ảnh, thứ tự C,D,*A,B bị xáo → "thấy 0 phương án" (cần sửa tay); **171 Phù Cừ** thiếu đáp án Câu 13 thật (lời giải không nêu đáp án); **194 Cẩm Phả** Câu 18 phương án dùng chữ Hy Lạp Α/Κ lookalike (+ lỗi tab) và Câu 28 thiếu đáp án + thiếu hình. Dòng "không đáp án: 4" trong dry-run là 4 câu Đúng–Sai (đáp án dạng mảng), không phải lỗi. Chưa có nhãn Chủ đề (0/28) — chấp nhận ở mục 277.

**2026-10-03 — ĐÃ ĐĂNG 3 đề sạch vào mục 277 (93→96):** exam **260** (SP Vinh Đề 9+ Lần 11), **261** (Minh hoạ 2025 Lần 18, Bộ GD&ĐT), **262** (Chuyên KHTN HN Lần 2). Tra trùng bằng REST service-role (so Câu 1 với mọi exam trong mục). File "141. TRAN DANG NINH HA NOI 2025" TRÙNG exam 234 → không đăng. Chưa có nhãn Chủ đề; chưa xem trên web. Còn: 000 (sửa tay Câu 8), 171, 194 và ~295 file khác.

**2026-10-05 — thầy chốt 3 điểm treo:**
1. Đích đăng nhóm `Lop12_*` (cùng các file khác) = mục 277 "Đề thi thử các trường, sở GD&ĐT 2026" (lesson 132). Chưa tách đích riêng cho đề năm học 2026–2027.
2. Kiểm trùng thay bằng script được, không cần trình duyệt: REST + service-role đọc `lesson_items.exam_ids` mục 277 và `exams.questions`, so Câu 1 (đã dùng 3/10 cho 260–262); `upload-exam-docx.mts` tự bỏ qua đề trùng ("DUP: trùng N/M câu"). Từ nay bỏ bước "phiên trình duyệt /quan-tri/sua-de" ở quy trình.
3. LOẠI khỏi đợt đăng: 000 Gia Định, 171 Phù Cừ, 194 Cẩm Phả (không sửa tay, không giao agent).

**2026-10-05 (đính chính + dọn nguồn):** 3/10 một phiên khác đã chạy đăng hàng loạt: mục 277 giờ **307 đề** (211 đề mới, exam 263–473, tạo 3/10; log file→exam ở `scripts/data/bulk-de-thi-thu-log.json` 297 dòng, kết quả chạy ở `bulk-de-thi-thu-run-2026-10-03.json`, câu bị lược ở `bulk-de-thi-thu-log-dropped.json`). Đề 000/171/194 (Gia Định 263, Phù Cừ 397, Cẩm Phả 411) CÒN nằm trong mục 277 dưới dạng bản đã lược câu — thầy muốn loại, chưa xoá (chờ thầy đồng ý). Đã chuyển 282 file đã đăng (đối chiếu log → exam id còn trong DB) sang `đã đăng lên thachlab` (giờ 341 file); thư mục "các đề đã xong" còn 22 file: 17 bị SKIP >20% câu mất, 5 LỖI bundle, + 1 khoá tạm `~$`. Bỏ ý "đăng ~295 file còn lại" ở trên — không còn.
