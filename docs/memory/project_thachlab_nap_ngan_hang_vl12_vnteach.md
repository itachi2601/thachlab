---
name: project_thachlab_nap_ngan_hang_vl12_vnteach
description: Nạp ngân hàng từ Tài liệu dạy thêm VL12 TVT2025 — ABCD Ch.1 189 + Ch.2 60 + Ch.3 131 + Ch.4 226 câu đang Hiện (2026-10-24); còn Đ–S/tính toán mọi chương; đáp án = tô vàng (Ch.3 gạch chân)
metadata:
  node_type: memory
  type: project
  originSessionId: b9777655-87ce-4297-bf75-bec7f143b060
  modified: 2026-10-24T08:35:05.979Z
---

Nguồn: `Documents/THPT/Lop12/00_Dung_chung/Thu_vien_tai_lieu/CT2025_tai-lieu-moi/lớp 12 (VnTeach)/BỘ TÀI LIỆU DẠY THÊM VẬT LÍ 12 BA BỘ SÁCH TVT2025 WORD/` — 4 file `[GV]CHƯƠNG 1..4 - LÝ 12 - VIP3/VIP2.docx` (25 MB).

**Khảo sát 24/10/2026 (chưa nạp gì):** là sách giáo viên cả chương (lý thuyết + trắc nghiệm ABCD, Đúng–Sai, tính toán/trả lời ngắn), KHÔNG phải ngân hàng đơn giản nên skill `ngan-hang-cau-hoi` bước 1–7 không khớp. Số "Câu n" đếm thô: Ch.1 643 (310 lời giải), Ch.2 378 (278), Ch.3 133 (0 lời giải, bố cục khác, 75 hình), Ch.4 331 (20).

**Đáp án MC = tô nền vàng (highlight YELLOW) trên phương án đúng** (không phải gạch chân như VL10); phương án khi là đoạn "A. … B. …" một dòng (đánh dấu theo run), khi là List Paragraph tự đánh số (không có nhãn A–D trong text). Cần `pip3 install python-docx` (chạy script bằng `python3` thường, không `-I`, nếu không thấy gói user).

Đường hợp lý: tái dùng pipeline VL10 ([[project_thachlab_nap_ngan_hang_vl10]]) đổi bước nhận đáp án sang highlight.

**Đã xong (2026-10-24, nhánh `claude/skill-nap-ngan-hang-cau-hoi-542083`, commit 787b05e4a…76d59d9f2):** Ch.1 ABCD (md dòng 646–3306): `scripts/data/nap-ngan-hang-vl12/parse12.py` → 281 câu → `dung-cau.py` (VL10) giữ 257 → `VL_GRADE=12 loc-trung-vl10.mts` bỏ 39 trùng → 218 giải bằng 9 subagent Sonnet độc lập (không Batch, key API hỏng): khớp 204/204 tô vàng; loại 14 null + 10 ghi chú + 3 agent báo; vớt 11 câu dính tiêu đề mục cuối phương án D (cắt sau `\n`) → 190 → ghi 189 (1 trùng). Nhãn 4 subagent Haiku (156 dễ/34 TB). **189 câu đang HIỆN**, `note='nap-vl12-c1-20261024'` (thầy từng hoàn tác rồi bảo bật lại; hoàn tác: `update question_bank set archived=true where note=…`; bật: `c1/hien.sql`). Dữ liệu: `c1/cau-final.json`, `ket-qua.json`, `gan-nhan.json`, `giai/`, `loai-sau-giai.json`; `gop-ket-qua.mts`; `chu-de-lop12.json` (lá Ch.1 = id 195–203).

**Ch.2 ABCD (24/10, md dòng 236–1049, `c2/`):** 93 câu → 79 → bỏ 12 trùng → 67 giải (3 subagent Sonnet) → 60 khớp tô vàng (loại 1 lệch mơ hồ c2-mc-056, 6 thiếu hình/2 đáp án); 60 câu HIỆN, note `nap-vl12-c2-20261024`, lá 204–212. Worktree chưa link supabase: `ghi-ngan-hang-vl10.mts --apply` lỗi LegacyProjectNotLinked → chạy `ghi.sql` bằng `supabase db query --linked -f` từ repo chính.

**Ch.3+Ch.4 ABCD (24/10, `c3/` `c4/`):** Ch.3 gạch chân (md đã đổi `1.`→`**Câu N:**` ở `c3q.md`, 5 cụm ABCD), loại 83 câu có hình; 146 giải → 131 Hiện (note `nap-vl12-c3-20261024`). Ch.4 md lấy từ docx sau khi gỡ 1 công thức OMML hỏng làm pandoc sập (bisect theo phần tử), đáp án tô vàng hoặc `Chọn X` trong Hướng dẫn; 269 giải → 226 Hiện (note `nap-vl12-c4-20261024`). Loại câu có ghi_chu sửa dữ kiện/lệch/thiếu hình-đồ thị; vớt câu chỉ dính tiêu đề mục ở D (cắt sau \n). Chưa làm Đ–S/tính toán Ch.3–4.

**Đ–S Ch.1–4 (24/10, `ds/`, parser `parse12ds.py`):** đáp án từ Hướng dẫn/tô vàng/gạch chân; Ch.3 dùng `c3/md/c3ds.md`; 169 → bỏ 55 trùng → 114 → 5 subagent Sonnet giải độc lập (khớp 84, loại 24 null + 6 lệch) → 84 câu Hiện, note `nap-vl12-ds-20261024`. Mức độ phải là `de`/`trung-binh`/`kho` (không `tb`). Còn: tính toán/trả lời ngắn mọi chương, Đ–S có hình/bảng.

**CÒN LÀM (cũ; Đ–S đã xong):** Ch.2 Đ–S (md 1050–1121, 5722+), tính toán (1122–5721); Ch.1 Đúng–Sai (md dòng ~3307–3852), tính toán (3853–7651, có lời giải), Đ–S phần III (7652+); Ch.2–4 (Ch.3 cần parser riêng). Sửa `ANTHROPIC_API_KEY` nếu muốn Batch; `batch-gan-nhan-vl10.mts`/`hien-vl10.mts` còn hardcode lớp 10 (hiện bỏ qua bằng subagent + `hien.sql`). Word nguồn chưa chuyển sang "đã đăng". Chưa xem mẫu 189 câu trên giao diện bằng mắt.

**Mẹo vận hành:** worktree không có `.env.local`/`node_modules`/supabase link → symlink 2 cái đầu từ repo chính; chạy `supabase db query --linked -f` từ thư mục repo chính với đường dẫn file trong worktree. `python3 -I` không thấy python-docx. Chuỗi `"…${GRADE}"` phải là backtick (đã sửa `ghi-ngan-hang-vl10.mts`).

**Rút kinh nghiệm (skill `ngan-hang-cau-hoi` nằm ngoài repo — nhắc thầy cập nhật nếu muốn):**
- Đếm cờ lỗi parser trước khi kết luận nguồn lỗi (regex bỏ sót `(BT)` làm 237 câu thành 148 "nhiều đáp án").
- Subagent giải độc lập: file vào không chứa đáp án, cho phép `answer=null`, 25 câu/lô, báo cáo 1 dòng → phiên chính không đọc lời giải.
- Dry-run phải đối chiếu số ngân hàng hiện có ≠ 0 (lỗi template làm so trùng với 0 câu).

Liên quan: [[project_thachlab_nap_ngan_hang_vl10]], [[feedback_bo_cau_mo_ho_thay_vi_giai_lai]].
