---
name: project-thachlab-l12-tu-truong-dien-tu
description: "Thay lý thuyết 12 chủ đề Lớp 12 (Từ trường + Điện từ) bằng file GV mới, gộp vào 6 lesson_items; đã sửa lỗi bài tập lẫn lý thuyết + ảnh trang trí vô nghĩa + quiz trùng Luyện tập (6 bài) + gỡ 24 câu ẩn do lỗi data cũ (2026-09-26); đã rà thêm Lớp 10+11, chỉ 1 bài dính ảnh trang trí, đã sửa (2026-09-27)"
metadata:
  node_type: memory
  type: project
  originSessionId: 6093eceb-f6fb-4d0d-b57e-05c21ebebc94
  modified: 2026-09-28T03:07:02.511Z
---

Mục tiêu: thay lý thuyết Lớp 12 chương Từ trường + Điện từ bằng nội dung từ file "Chủ đề N ... - GV.docx" mới (giống pattern đã làm với [[project_thachlab_chuong4_hat_nhan_ly_thuyet]] cho hạt nhân). Đây là 1 trong 3 việc chạy song song bằng 3 agent (xem [[project_thachlab_mastery_yccd]], [[project_thachlab_question_bank]] cho 2 việc còn lại cùng đợt).

**Đã xong (26/9/2026):**
- 12 thư mục nguồn (`output/bai10-luc-tu`, `bai12-cam-ung-dien-tu`, `bai12-suat-dien-dong`, `bai12-tu-thong`, `bai13-dien-ap-xoay-chieu`, `bai13-nguyen-tac-dxc`, `bai14-may-bien-ap`, `bai14-may-phat-dien`, `bai14-ung-dung-an-toan`, `bai15-dan-ghi-ta-dien`, `bai15-dong-dien-foucault`, `bai16-dien-tu-truong`) đã render xong công thức (`html_report.json.ready=true`) và gộp vào **6 `lesson_items`** (id 52/66/141/143/145/183, ứng với `lesson_id` 11/13/14/125/126/127 — GV chia file chi tiết hơn cấu trúc 16-bài của LMS nên nhiều file GV gộp vào 1 bài LMS).
- Script `scripts/update-ly-thuyet-l12-tu-truong-dien-tu.mts` (mới, tái dùng pattern của `scripts/update-ly-thuyet-l12-cd4-hat-nhan.mts`) tải ảnh lên bucket Storage `lesson-media`, ghi đè `body_html` của 6 dòng trên. Đã chạy `node scripts/build-content.mjs` để nội dung tĩnh khớp DB.
- Đã merge vào `main` (nhánh `feat/bundles`) và push lên origin.
- `output/12-tu-thong-latex` (612 công thức) và 3 bundle cũ ở `output/lop10-chuong1-latex/bundles/` (bài đích đã có nội dung, khả năng bản trùng/cũ) — **không đụng**, để nguyên theo quyết định của thầy.

**Sự cố đã xảy ra và đã tự sửa trong phiên (ghi lại để tránh lặp lại):** lần chạy đầu bị lỗi mạng thoáng qua khi tải ảnh, agent tự kill rồi chạy lại → 2 tiến trình ghi đè chồng chéo làm hỏng dữ liệu (5/6 dòng thiếu URL ảnh thật, 1 dòng bị lẫn ảnh của bài khác). Phát hiện bằng cách tự đối chiếu SQL sau khi "tưởng xong", không tin log thành công. Sửa bằng cách chạy lại **1 tiến trình duy nhất, không can thiệp giữa chừng**. Bài học: khi chạy script ghi ảnh+DB cho nhiều bài, nếu nghi lỗi mạng thoáng qua thì để script tự retry/dừng theo thiết kế, đừng tự kill và chạy lại chồng lên tiến trình cũ.

**Rủi ro/việc cần thầy xem lại:**
- Nội dung lý thuyết mới **dài hơn bản cũ 8–14 lần** (file GV lồng cả bài tập mẫu vào phần lý thuyết) — nên xem qua UI thật xem có hợp lý không.
- Tiêu đề của 3 bài bị gộp (do 1 câu SQL lấy tiêu đề cũ bị treo giữa phiên) được agent tự đặt lại, KHÔNG copy nguyên từ DB cũ — cần thầy xem lại tên bài có đúng ý không.
- Chưa tự kiểm tra layout mobile bằng trình duyệt thật (chỉ kiểm tra qua code/SQL).
- **Có 1 phiên khác chạy song song làm đúng việc này** (commit `640774b0`, cùng ngày, theo cách khác: ảnh ở `public/lessons/.../media/*.png` + PATCH REST) — thầy đã chọn giữ bản của agent này (ảnh qua Storage bucket), bản kia coi như không dùng. Nếu sau này thấy lệch nội dung so với file GV gốc, đây là lý do.

**How to apply:** nếu cần thay lý thuyết Lớp 12 chương khác bằng file GV mới, copy pattern script này (không phải viết lại từ đầu) — nhưng nhớ kiểm tra `html_report.json.ready` (KHÔNG dùng `report.json.equations_pending`, số này là snapshot tĩnh lúc extract, không tự cập nhật khi render xong).

**Cập nhật 26/9/2026 — đã sửa lỗi "bài tập lẫn lý thuyết" + "alt ảnh rác" đúng như rủi ro đã ghi ở trên:**
Thầy phát hiện đúng: rủi ro "lồng cả bài tập mẫu vào lý thuyết" ghi ở trên là có thật — cả 6 mục lý thuyết
đều có nguyên khối "CÂU HỎI TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN/ĐÚNG SAI/TRẢ LỜI NGẮN" kèm "Hướng dẫn giải" kẹt
trong `body_html`; riêng lesson_id=126 còn thiếu hẳn mục `bai_tap_mau`. Nguyên nhân gốc: `parts.json` ở
12 thư mục `output/bai1*-*/` liệt kê `thu_tu_dang: [ly_thuyet, bai_tap, bai_tap_ve_nha]` nhưng script tách
phần (skill `latex`, `prepare_html.cjs`) không tách được — chỉ tạo đúng 1 part `ly_thuyet` chứa tuốt.

Đã viết [scripts/fix-l12-tu-truong-mixed-quiz-content.mts](../../../../Projects/thachlab/scripts/fix-l12-tu-truong-mixed-quiz-content.mts)
— KHÔNG đụng .tex nguồn/pipeline latex, chỉ sửa dữ liệu Supabase đã đăng: tách block cấp-1 của
`body_html`, nhận diện 3 tiêu đề trắc nghiệm (kể cả khi dính vào cuối 1 đoạn lý thuyết qua `<br/>`),
gom mỗi "Câu N" (đến "Hướng dẫn giải") thành 1 phần tử `{label, body_html}` đẩy vào `questions[]` của
mục `bai_tap_mau` cùng bài (tạo mới #283 cho lesson_id=126). KHÔNG dùng số thứ tự "Câu N" để quyết định
ranh giới nhóm (nguồn GV có vài chỗ đánh số nhảy/lặp/mở đầu bằng "Ví dụ" — lỗi đánh máy gốc) — chỉ thoát
nhóm khi gặp `<h2 class="text-xl font-bold mt-3 mb-1.5">` (mốc chuyển "Chủ đề" GV do script gộp bài tự
chèn) hoặc 1 trong 3 tiêu đề trắc nghiệm khác. Cũng dọn `alt="..."` rác (leftover LaTeX/table từ
`alt_goi_y` trong parts.json) → `alt=""` trên mọi `<img>`.

Kết quả: 521/520 câu bắt được đúng (đối chiếu bằng đếm block "Câu N" thật, không dùng đếm thô toàn văn
bản vì bị trùng do "Câu N" bị nhắc lại trong lời giải câu khác). Đã `--write` (tự backup vào
`scripts/logs/l12-tu-truong-quiz-fix-backup-*.json`, gitignored) + `node scripts/build-content.mjs` +
kiểm tra trực tiếp trên dev server (bài 13 và bài 15 lên đúng, ảnh hiển thị, Luyện tập tự cập nhật số
câu). Còn 1 lỗi HTML có sẵn từ TRƯỚC (không phải do script gây ra, đã đối chiếu với bản gốc): lesson
id=66 thiếu 1 thẻ `</p>` ở cuối 1 câu Đúng-Sai lớn — vô hại (trình duyệt tự đóng), chưa sửa.

Đã hỏi thầy (tree lúc đó dirty với WIP phiên khác) — thầy chọn "cứ deploy luôn". Đã build + deploy
thành công (`scripts/deploy.sh`).

**Cập nhật thêm cùng phiên — dọn ảnh trang trí vô nghĩa:** thầy phát hiện tiếp 1 lỗi khác: một số
`<img>` trong lý thuyết không phải hình vật lý mà là ảnh mockup "thanh tiêu đề cửa sổ trình duyệt"
(cam/xanh navy, file gốc `d01.png`/`d02.png`/`d03.png` trong `output/bai1*-*/media/`) — vốn là ảnh
trang trí kiểu tiêu đề trong file Word GV, bị pipeline trích ảnh gộp nhầm vào nội dung. Đã viết
[scripts/remove-junk-decorative-images-l12.mts](../../../../Projects/thachlab/scripts/remove-junk-decorative-images-l12.mts)
— nhận diện bằng cách so khớp MD5 ảnh đã tải lên Supabase Storage với 9 hash đã xem bằng mắt xác
nhận là ảnh trang trí (KHÔNG đoán theo tên file: `d01.png` ở `bai14-may-bien-ap` lại là ảnh thật —
máy biến áp, không phải trang trí). Xoá đúng 17 ảnh (2-4 ảnh/bài) khỏi 6 mục lý thuyết, `--write` +
backup + `build-content.mjs` + deploy lại — xong, đã lên production.

**Sự cố khi deploy (đã tự sửa, ghi lại để lần sau khỏi mất thời gian dò lại):** `git push` lên nhánh
`deploy` (~26MB) báo `HTTP 408 curl 22` + "unexpected disconnect while reading sideband packet" —
KHÔNG phải do file lớn/postBuffer (đã thử tăng `http.postBuffer` và tắt `http.lowSpeedLimit`, vẫn lỗi
y hệt) — sửa được bằng cách ép `git -c http.version=HTTP/1.1 push ...` (nghi ngờ proxy mạng xử lý sai
gói tin lớn qua HTTP/2). Nếu deploy sau này gặp lại đúng lỗi 408 này, thử HTTP/1.1 trước khi nghi ngờ
lỗi khác. Commit `out/` không mất khi push thất bại (chỉ `rm -rf .git` sau dòng push trong deploy.sh,
`set -e` dừng trước đó) — có thể `cd out && git push ...` lại trực tiếp mà không cần build lại từ đầu.

**Việc còn treo:** Bài 14 (lesson_id=125) Câu 10 thiếu 1 hình đồ thị thật (ảnh gốc JPEG-XR không giải mã
được lúc trích xuất, script này không tự vẽ lại được) — cần ảnh thật hoặc thầy tự vẽ tay. (Vẫn còn treo
sau đợt 2026-09-26 thứ hai bên dưới — đã kiểm tra lại, chưa có ai bổ sung ảnh.)

**Cập nhật 2026-09-26 (phiên khác, cùng ngày) — hệ quả của lần tách quiz khỏi lý thuyết ở trên: quiz vừa
tách lại TRÙNG với đề Luyện tập đã có sẵn, đồng thời lộ ra 1 lỗi dữ liệu cũ hơn nữa:**

Thầy phát hiện tiếp: mục "Các dạng bài tập" (`bai_tap_mau`) của các bài trong chương này — vốn được
`scripts/fix-l12-tu-truong-mixed-quiz-content.mts` (xem đợt trước ở trên) đổ quiz tách từ lý thuyết vào
— phần lớn TRÙNG với chính đề đã gắn ở mục Luyện tập (`exams.questions` qua `lesson_items.exam_ids`)
của cùng bài. Đã rà toàn bộ DB (không chỉ chương này) và sửa **6 bài**, toàn bộ qua PATCH REST thẳng vào
Supabase (không migration, không đổi code, không cần deploy — ghi là lên production ngay):

| Bài | lesson_items (Các dạng bài tập) | Luyện tập (exams) |
|---|---|---|
| Bài 10. Lực từ. Cảm ứng từ (lesson 11) | id=230: 77→8 (chỉ giữ 8 dạng mẫu thật) | #49 giữ nguyên (69 câu trùng đã xoá hẳn, không có gì để gộp) |
| Bài 12. Hiện tượng cảm ứng điện từ (lesson 13) | id=67: 13→4 | #50: 177→**210** (+33 câu) |
| Bài 13. Đại cương DĐXC (lesson 14) | id=231: 84→2 | #51: 77→**146** (+69 câu, bỏ 1 câu lỗi phương án trùng) |
| Bài 14. Máy phát điện XC. Máy biến áp (lesson 125) | id=232: 93→2 | #52: 85→**112** (+27 câu, bỏ 2 câu trùng lặp y hệt) |
| Bài 15. Ứng dụng cảm ứng điện từ (lesson 126) | id=283: 57→**0 (rỗng hẳn)** | #53: 57→**72** (+15 câu) |
| Bài 16. Điện từ trường. Sóng điện từ (lesson 127) | id=184: 74→14 | #75: 67→**75** (+8 câu) |

Cách làm: câu nào trùng y hệt câu đã có trong đề Luyện tập → xoá khỏi `bai_tap_mau` (không gộp lại, đã có
rồi). Câu nào KHÔNG trùng (nội dung đúng chủ đề nhưng chưa từng được đưa vào đề chấm điểm) → dùng agent
đọc "Hướng dẫn giải" có sẵn trong từng câu để chuyển sang JSON đúng schema `ExamQuestion`
(`features/exams/types.ts`) rồi gộp thêm vào cuối mảng `exams.questions`; tự tay đối chiếu lại tất cả câu
agent gắn cờ nghi vấn trước khi ghi (agent tự phát hiện và sửa đúng vài chỗ lời giải GỐC tính sai/nhầm
đơn vị — ví dụ Bài 12 "khung dây 500 vòng" lời giải gốc ghi nhầm 25×10⁻³ Wb thay vì 0,54 Wb; Bài 12 câu
lực kéo MN ghi nhầm "=1,2 N" thay vì đúng ra 0,00115 N; Bài 12 câu điện lượng ghi nhầm "25 μC" thay vì
25000 μC; Bài 14 câu "sóng biển" lời giải thế nhầm B; Bài 15 câu đàn guitar nghi đề gốc thiếu số 0 ở B).

**Phát hiện thêm ngoài dự tính — lỗi dữ liệu cũ hơn nữa, không liên quan lần tách quiz ở trên:** trong
lúc rà Bài 12, phát hiện 1 phần tử của mảng `questions` (lesson_items id=67) dài ~40KB — bị dán dính
24 câu khác vào chung 1 ô (`label`+`body_html` của 1 câu nhưng `body_html` chứa tiếp text của hàng chục
câu sau, không tách được thành phần tử mảng riêng — khả năng lỗi từ 1 script import/gộp bài rất cũ, trước
cả đợt 26/9 ở trên). 24 câu này (11 đúng-sai + 13 trả lời ngắn) CHƯA TỪNG hiển thị hay chấm điểm được cho
học sinh vì nằm ẩn trong text. Đã tách thủ công bằng regex theo mốc `<strong>Câu N:</strong>`, xác nhận
đúng ranh giới, rồi xử lý và gộp vào đề #50 cùng đợt trên (đã tính trong con số 177→210 ở bảng trên).

**Cần thầy quyết định:**
- **Bài 15 (lesson_id=126)**: mục "Các dạng bài tập" giờ **rỗng hoàn toàn (0 mục)** vì bài này chưa từng
  có dạng bài mẫu tự luận thật — chỉ có nguyên quiz trùng. Thầy cần chọn: ẩn hẳn mục này trên trang bài
  học, hoặc soạn thêm dạng bài mẫu mới.
- 1 câu ở đề #50 (Bài 12) thiếu hình đồ thị minh hoạ gốc (không giải mã được lúc trích xuất từ trước) —
  vẫn giữ câu vì lời giải đã đủ số liệu để chấm đúng, nhưng nên bổ sung ảnh khi có dịp.
- Bài 14 câu #10 vẫn thiếu ảnh đồ thị e1/e2 như đã ghi ở mục "Việc còn treo" phía trên (không phải lỗi
  mới, cùng 1 vấn đề).

**Toàn bộ thao tác trên đều KHÔNG đụng `supabase/migrations/`, KHÔNG sửa code repo, KHÔNG cần deploy** —
chỉ là PATCH dữ liệu qua REST bằng `SUPABASE_SERVICE_ROLE_KEY` trong `.env.local` (xem
[[feedback_lesson_item_edit_via_rest]]), nên đã lên production ngay lúc ghi, độc lập với tree đang dirty
vì WIP của phiên khác (xem [[project_thachlab_concurrent_sessions]]) — không có gì để commit từ việc này.

**2026-09-27 — thầy hỏi ảnh trang trí có "rải rác ở bài khác" không, đã rà toàn bộ Lớp 10 + Lớp 11:**
Quét MD5 toàn bộ ảnh (Supabase Storage lẫn đường dẫn local `public/lessons/.../media/`) của 72 bài
(55 mục `ly_thuyet` + 45 `bai_tap_mau` + 55 `luyen_tap`) — chỉ tìm thấy **đúng 1 bài dính lỗi**:
lesson_items#90 (lesson_id=49, Lớp 10, "Độ dịch chuyển, quãng đường đi được") — 4 ảnh mockup
(`d01–d04.png` ở `public/lessons/do-dich-chuyen-quang-duong-di-duoc/media/`, d01/d02/d04 khớp đúng
hash rác đã biết, d03 là biến thể mới cùng loại — đã xem bằng mắt xác nhận). 83 ảnh nhỏ khác nghi
vấn (<6KB) đã tải về ghép thành 3 "contact sheet" xem hết bằng mắt — toàn bộ là nội dung thật (biểu
tượng an toàn phòng thí nghiệm, đồ thị, vector, công thức), không phải ảnh trang trí.

Đã sửa bằng [scripts/remove-junk-decorative-image-lesson49.mts](../../../../Projects/thachlab/scripts/remove-junk-decorative-image-lesson49.mts)
(`--write` + backup) + `build-content.mjs` + `npm run build` + deploy (`git -c http.version=HTTP/1.1
push` ngay từ đầu, không bị lỗi 408 nữa) — đã lên production.

**Kết luận cũ (27/9) ĐÃ SAI — cập nhật 2026-09-28:** kết luận "chỉ 1 bài duy nhất" dựa trên so khớp
MD5 với danh sách hash rác ĐÃ BIẾT — có lỗ hổng coverage, không phải bằng chứng đã quét hết. Phát
hiện thêm **bài 13 Lớp 10 (Tổng hợp và phân tích lực, lesson_id=58, lesson_items#108)** dính đúng
loại lỗi này (2 ảnh header trang trí `d01.png`/`d02.png`, hình khối gradient xanh/bar — KHÁC hẳn
dạng "thanh tiêu đề trình duyệt cam/navy" đã biết) — hash không khớp danh sách cũ nên lần quét MD5
27/9 bỏ sót hoàn toàn. Đã xác nhận bằng mắt (xem ảnh trực tiếp, không đoán theo tên/kích thước) rồi
sửa qua PATCH REST thẳng `body_html` (xoá 2 thẻ `<img>`, giữ nguyên phần còn lại), rebuild+deploy,
verify trên web thật OK. Đã kiểm tra 6 bài lân cận cùng chương (14,16,17,18,19 Lớp 10 — bài 15 cũng
soát) không dính lỗi tương tự — các ảnh `dNN.png` nhỏ khác ở 6 bài đó là nhãn vector lực/công thức
thật, không phải trang trí.

**Kết luận đúng cho lần sau:** lỗi ảnh trang trí có thể xuất hiện ở BẤT KỲ bài nào từng qua pipeline
docx→JSON (mỗi file Word GV có thể có graphic header riêng, hash khác nhau mỗi lần) — so khớp MD5
với danh sách hash cũ chỉ bắt được ảnh ĐÃ THẤY TRƯỚC ĐÓ, không phải phương pháp đầy đủ. Cách chắc ăn
hơn: với mỗi bài nghi ngờ, xem trực tiếp toàn bộ ảnh nhỏ (<30KB) dùng trong `theory_html`/`body_html`
bằng contact sheet (ghép nhiều ảnh thành 1 lưới, xem 1 lần thay vì mở từng file) — phân biệt "icon
bullet nhỏ dùng LẶP LẠI nhiều lần giống hệt nhau" (thường vô hại, chỉ cần domain URL đúng + CSS
`.figure` không phóng to quá) với "hình khối/gradient LỚN chỉ xuất hiện 1 lần ở đầu đoạn lý thuyết"
(gần như chắc chắn là header trang trí, nên xoá hẳn thẻ `<img>`, không phải sửa kích thước).
