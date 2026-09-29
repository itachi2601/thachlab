---
name: project_thachlab_azota_skill
description: "Skill azota (plugin anthropic-skills, bản gốc trong Library/Application Support + bản codex ~/.codex/skills/azota) — bước 6 xuat_thachlab.py dựng Word cho /quan-tri/dang-de kèm nhãn"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7c9fccc2-7d0b-42e9-9bfa-9484e15d84c0
  modified: 2026-09-27T15:52:18.014Z
---

Skill `azota` sống ở hai chỗ giống hệt nhau, phải sửa cả hai (cp sau khi sửa):
- `/Users/MAC/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/f7f31a21-…/46c5a460-…/skills/azota/` (bản Claude Code nạp)
- `~/.codex/skills/azota/`

Sửa 2026-09-19: thêm **Bước 6 — Đưa đề lên thachlab** + `scripts/xuat_thachlab.py de_azota.docx nhan.json
de_thachlab.docx --grade 12`: đọc bản Azota (đáp án trong bảng sau HẾT, "Câu n: Chọn đáp án…" ở phần
lời giải) → dựng Word cho trang Đăng đề: `*` trước phương án/ý đúng (chèn được cả khi hai phương án
chung dòng, nhãn tách run), Phần III dòng "Đáp án:", "Lời giải:" ngay dưới câu, hai dòng
`Chủ đề:`/`Dạng:` từ nhan.json (`{"phần": {"câu": ["yêu cầu cần đạt", "lý thuyết|bài tập"]}}`),
đánh số liên tục. Tự in lại nhãn A./a) khi đề mất nhãn do đánh số tự động (lấy 4 đoạn cuối).
`--grade` soát tên với `question_topics` qua REST (đọc `~/Projects/thachlab/.env.local`, cờ `--env`).
Đã test trên `~/Downloads/Lop11_KTGiuaKy1_VatLyThuongKiet_2026-2027_Azota.docx`: 21/21 câu qua parser
thachlab, đủ đáp án; chưa kéo thử vào trang thật (cần đăng nhập).

**Why:** thầy muốn đề up lên có luôn phân loại theo yêu cầu cần đạt; bản Azota không dán thẳng được.
**How to apply:** người viết `nhan.json` là Claude (đọc đề dẫn, chọn yêu cầu cần đạt trong danh mục —
tải bằng curl REST như trong SKILL.md). Xem [[project_thachlab_dang_de_tags]], [[project_thachlab_up_de_skill]].

Sửa 2026-09-19 (2): thêm skill sinh đôi `ngan-hang-cau-hoi` (cũng 2 bản, cùng hai thư mục trên) — lo
file "ngân hàng câu hỏi ôn tập theo chủ đề" KHÔNG có PHẦN I/II/III và đáp án KHÔNG đánh dấu sẵn (khác
đề thi TN THPT của azota). Thêm dòng disambiguation vào description của cả hai skill để trigger đúng.
Xem [[project_thachlab_ngan_hang_cau_hoi_skill]].

**Sửa 2026-09-25 — vá lỗi gốc "Câu N in đôi":** hàm `cell_pars()` trong `convert_docx.py` (cả 3 bản:
Library, ~/.codex, và bản project riêng ở
`.../Lop12/NamHoc/2026-2027/06_Azota_so_hoa/_CongCu/convert_docx.py`) lặp `for c in row.cells` — khi
một ô có `gridSpan > 1` (thường là ô câu hỏi/stem bị Word gộp cột), python-docx trả về CÙNG một `_Cell`
nhiều lần, nên đoạn văn trong ô đó (cả câu hỏi) bị yield lặp lại → đúng triệu chứng "Câu N: ... lặp đôi
cách nhau vài đoạn văn" mà thầy hay gặp khi convert đề có bảng 2 cột (trái đề/phải hình) hoặc bảng
Phát biểu bị Word merge cột. Đã vá bằng cách lọc trùng theo `id(c._tc)` trước khi yield. Xác nhận qua
đợt convert batch 233-236 (đề "SO GIAO DUC BINH DUONG 2025 LAN 2"): trước vá báo nhầm Phần III có 11
câu (phantom câu 7-11 từ ô gridSpan lặp), sau vá đúng 6 câu.
**Why:** đây chính là lỗi thầy yêu cầu "dọn sạch" ở review batch_12; không phải lỗi ngẫu nhiên, mà là
bug hệ thống trong hàm dùng chung cho mọi bảng 2+ cột.
**How to apply:** nếu thấy tiêu đề "Câu N" lặp y hệt cách nhau vài đoạn trong file `_Azota.docx` mới
convert, kiểm tra trước tiên xem `cell_pars()` ở bản convert_docx.py đang dùng đã có đoạn lọc `seen`
này chưa — rất có thể một bản (project hoặc skill) bị sửa lại từ bản cũ chưa vá.

**Rủi ro trùng phiên:** 2026-09-25 phát hiện 2 phiên Claude khác đang chạy song song
("20 agent song song skill Azota và MT7 to OMML", "Phân chia công việc 30 agent MT7-OMML-Azota") cũng
ghi file vào chung thư mục `01_De_da_chuyen_2025/` — để lại 2 file trùng nội dung khác chỉ khoảng trắng
tên (`229.  ...` hai khoảng trắng, `234.. ...` hai dấu chấm, đúng kiểu đặt tên nguồn gốc). Thầy đã bảo
xoá, giữ bản của phiên review batch_12 (tên chuẩn một khoảng trắng/một dấu chấm) — đã xoá 2 file trùng
2026-09-25. Nhiều phiên cùng ghi vào một thư mục dùng chung vẫn là rủi ro cần để ý khi giao việc song
song kiểu này.

**2026-09-25 (phiên khác, cùng ngày) — bài học đắt giá:** một phiên Claude Code (không phải phiên viết
mục trên) nhận lệnh y hệt "30 agent MT7-OMML-Azota, 20 agent Azota+MT7-OMML" nhưng KHÔNG kiểm tra thư
mục dự án thật trước — tự chọn nhầm thư mục cá nhân `~/Documents/Chuyen_doi_Office_Math/Ngan_hang_de/`
(khác hẳn `THPT/Lop12/NamHoc/2026-2027/06_Azota_so_hoa/`) và cho 2 agent pilot (6+7 file) tự viết lại từ
đầu bộ giải mã MTEF — tốn **552.927 token** — trong khi công cụ đã có sẵn ở `_CongCu/mtef_to_omml/`
(do phiên kia dựng). Tệ hơn: 6/6 file pilot đó **trùng hoàn toàn** với file đã có sẵn trong
`01_De_da_chuyen_2025/` — gần như chắc chắn `đề các trường/` (197 file) chỉ là **bản sao nguồn thô**
của đúng số file đã nằm trong `01_De_da_chuyen_2025/` (chưa kiểm chứng hết 197 file, nhưng mẫu 6/6 khớp).
**Why:** hai phiên Claude Code khác nhau cùng nhận một câu lệnh mơ hồ ("30 agent, 20 agent") từ thầy,
mỗi phiên tự suy luận thư mục làm việc theo cách riêng — không có cơ chế nào buộc kiểm tra trạng thái
dự án thật trước khi hành động lớn.
**How to apply:** TRƯỚC khi làm bất cứ việc MT7/Azota hàng loạt nào, luôn kiểm tra
`THPT/Lop<N>/NamHoc/<năm>/06_Azota_so_hoa/_CongCu/` trước (đã có công cụ + có thể phiên khác đang/đã
làm dở) — đừng vội cho agent viết code mới. Xem [[project_thachlab_mtef_decoder_v2]].

**Cập nhật 2026-09-25:** `convert_docx.py` (bản ~/.codex và synced) có thêm `chuyen_anh_vector_sang_png(docx_path, warn)` — gọi sau `doc.save` trong `xuat_thachlab.py` để đổi EMF/WMF ảnh thật sang PNG bằng LibreOffice, bỏ qua ảnh xem trước MathType. Xem [[project_thachlab_missing_figures]].

**Cập nhật 2026-09-27:** `xuat_thachlab.py` (cả hai bản: `~/.codex` và Library) thêm
`norm_short_answer()` — đáp án Phần III (trả lời ngắn) lấy nguyên văn từ bảng đáp án gốc hay
dính đơn vị/ký hiệu ("≈9,4 cm", "x = 3,34", "100 J", "273°C") vượt quá giới hạn cứng 4 ký tự
của trang Đăng đề (`components/admin/ExamSection.tsx: a.length > 4` → không Đăng được). Hàm
mới tự bỏ tiền tố "x = "/"≈"/"~" và hậu tố chữ/đơn vị, giữ lại số; số vẫn dài (vd làm tròn 2
chữ số thập phân mà phần nguyên 2 chữ số, kiểu "11,95") thì tự rút còn 1 chữ số thập phân —
in cảnh báo ra `convert.log` mỗi lần đổi để người soát biết câu nào bị đổi giá trị thật (không
chỉ bỏ đơn vị), cân nhắc sửa luôn chữ "làm tròn đến phần trăm" trong câu hỏi cho khớp. Phát
hiện khi đăng 3 đề thi thử batch 27/9 (xem [[project_thachlab_de_thi_thu_truong_so]]), sửa tay
6+2 câu trước khi vá script.
