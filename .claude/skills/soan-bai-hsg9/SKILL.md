---
name: soan-bai-hsg9
description: Soạn trọn MỘT chuyên đề của khoá "Vật lí HSG & chuyên" KHTN 9 (môn hsg-vat-ly, lớp 19) theo lịch `scripts/data/btvn-hsg9/lich-soan-bai.md` — chọn chuyên đề tới hạn, dàn ý nguon.md, lý thuyết nâng cao + bài tập mẫu (subagent song song) + ≥6 câu luyện tập tự chấm, kiểm chéo 2×kiem-code, ghi DB bằng cap-nhat-ly-thuyet.sh + publish-bai-tap-mau.mts + upload-lesson.mts, cập nhật lịch/memory; bật Hiện chỉ sau khi thầy duyệt và trước ngày gửi BTVN. Dùng khi thầy nói "soạn bài HSG 9", "soạn chuyên đề tiếp theo của khoá HSG", "làm CĐ12/CĐ16/CĐ07…", "bổ sung luyện tập cho khoá HSG", "/soan-bai-hsg9". KHÁC soan-bai-tap-tu-luan-hsg (bộ tự luận in PDF, không ghi DB) và bai-hoc-tron-goi (bài lớp 10–12). Soạn + kiểm chạy được trên cloud; ghi DB và deploy chạy trên Mac.
---

# Soạn chuyên đề khoá HSG Vật lí 9

Skill điều phối. Phần kỹ thuật của từng mục nằm ở skill chuyên trách — chỉ mở đúng phần cần:
lý thuyết → `soan-bai-ly-thuyet-tuong-tac`, bài tập mẫu → `soan-bai-tap-mau`, PhET → `phet`.

## 0. Đọc trước (chỉ mấy file này)
1. `scripts/data/btvn-hsg9/lich-soan-bai.md` — bảng hạn. Chọn dòng có **hạn bật Hiện sớm nhất còn việc**; thầy nêu tên CĐ thì làm CĐ đó.
2. `docs/HSG9-KHUNG.md` — lesson_id, chương, YCCĐ dùng cho "bài tương tự" (KHTN 9 chưa có YCCĐ → mượn lớp 10–12).
3. `docs/memory/project_thachlab_khoa_hsg9_vat_ly.md` — trạng thái từng CĐ, quy ước đã chốt.
4. `scripts/data/btvn-hsg9/tuan.json` — tuần nào dùng bài đó (`gui_ngay`, `tu_hoc`, `btvn`): nội dung phải khớp việc HS được giao tuần đó.

Quy ước đã chốt (giữ thống nhất giữa lý thuyết, bài tập mẫu, luyện tập): g = 10 m/s² ghi ở mục tiêu; sai số 1 chữ số có nghĩa;
góc dây đo so với phương thẳng đứng (bài dùng góc với phương ngang thì ghi rõ); chỉ Vật lí, không soạn Hoá–Sinh của phần chung.

## 1. Chuẩn bị mục trên DB
- Bài phải có sẵn mục `ly_thuyet` + `bai_tap_mau`. Đã tạo: 159/157/165 (đợt 2), 150/153/164 (đợt 3).
  Chưa có (151, 156, 158, 178, 152, 163) → viết migration theo mẫu `supabase/migrations/20261016130000_hsg9_dot3_muc_noi_dung.sql`
  (idempotent, kèm rollback), nối vào `FILES` của `scripts/run-migrations.sh`, chạy `--only N` trong tab terminal (mục "Có script thì chạy giúp" của AGENTS.md).
- Thư mục làm việc: `content/hsg9/cd<NN>-<slug>/` (lý thuyết), `scripts/data/bai-tap-mau/<lesson_id>.json` (bài tập mẫu).

## 2. Dàn ý `nguon.md` (phiên chính, trước khi giao agent)
- Có docx gốc trong `~/Documents/THPT/Lop09/00_Dung_chung/HSG_KHTN9_Vat_li/01_Chuyen_de/` → trích text (A yêu cầu · B lý thuyết · C dạng · D ví dụ · E tự luyện · G nâng cao · H lỗi). Sửa sai sót đã biết của docx (xem memory).
- CĐ mới không docx (10, 15, 16, 17) → tự viết dàn ý theo đề cương THI HSG 9 KHTN 26-27, lời mình (mục Bản quyền AGENTS.md).
- Dàn ý chốt: 5–7 mục lý thuyết, danh sách **4–7 dạng** (tên dạng + số liệu đã tính bằng Python), 6–8 bài tự luận (E+G), ≥6 câu luyện tập, cái bẫy (H).
  Số liệu tính một lần ở đây rồi đưa nguyên cho các agent → các mục không lệch số nhau.

## 3. Soạn song song (subagent, một lượt gửi)
| Agent | Việc | Đầu ra |
|---|---|---|
| A | Lý thuyết nâng cao theo `soan-bai-ly-thuyet-tuong-tac` (rút gọn theo `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`, quiz cuối bài, hình SVG `build_figs.py`) | `theory.src.html` → `theory.html` |
| B, C | Bài tập mẫu theo `soan-bai-tap-mau`, **mỗi agent một module** (`btm<id>_d123.py`, `btm<id>_d456.py`), main `build-hinh-<id>.py` gom | `<id>.json` phần dạng + mô phỏng |
| D | Tự luận E+G (module `btm<id>_tl.py`) + **≥6 câu luyện tập** tự chấm (Phần I A–D / Phần II a)–d) Đ/S / Phần III đáp số, E1–E3) | `luyen-tap/bundle.json` |

Brief mỗi agent gồm (và với mọi bài tự luận: soát điều kiện phụ — mục 8): đường dẫn `nguon.md`, số liệu đã chốt, quy ước ở mục 0, file được phép ghi (không ghi file của agent khác), lệnh chạy thử riêng.
Brief cũng ghi: chữ SVG ≥ 14 đơn vị (chỉ số dưới 12), số thập phân trong $…$ viết `a{,}b`, chữ có dấu trong $…$ bọc `\text{}`, thư mục scratch RIÊNG cho từng agent (`scratchpad/<id>-<module>/`), và cấp độ từng dạng lấy đúng theo nguon.md (đặt cấp không giảm ngay trong dàn ý, tránh agent tự nâng cấp lệch nhau).
Phiên chính không sửa file của agent khi agent còn có thể được gọi lại — sửa sau cùng.

Luyện tập: bundle `thachlab.lesson-bundle/v1` chỉ có `exam` (để `theory_html` rỗng và `worked_examples: []` → `upload-lesson.mts` giữ nguyên lý thuyết và bài tập mẫu).
Mỗi câu có Chủ đề/Dạng, đúng một đáp án đã đối chiếu lời giải, mọi phương án nhiễu do một cách sai cụ thể (`assert` khác đáp án đúng).

## 4. Kiểm chéo 2×`kiem-code` (song song, độc lập)
- Agent 1: tự giải lại toàn bộ bài tập mẫu + tự luận + luyện tập **từ đề không đáp án**, đối chiếu.
- Agent 2: soát lý thuyết (sai công thức/đơn vị/ảo giác), hình (tỉ lệ, đường sức nét đứt, mũi tên chevron 30°), lộ đáp số (figcaption, khung cuối mô phỏng, hình vẽ sẵn kết quả), KaTeX (quét ký tự điều khiển `\t` trong JSON), nhãn đề thi thật, 375px.
- Sửa theo kết quả; lỗi đúng/sai không chắc thì hỏi thầy, không đoán.

## 5. Xem thử
Dựng bản xem thử (`xem-thu/`), chụp 375px các hình + mục có tương tác; nhìn bằng mắt (trong subagent nếu nhiều ảnh). Chưa qua thì không ghi DB.

## 6. Ghi DB (Mac, tab terminal)
- Lý thuyết + bài tập mẫu: thêm cặp `cd<NN>-<slug>:<id>` vào script đợt (`scripts/dang-hsg9-dot<N>.sh`, mẫu dot3; đợt mới thì sao từ dot3), chạy không `--yes` (dry-run) → xem phạm vi → `--yes`.
- Luyện tập: `npx tsx scripts/upload-lesson.mts content/hsg9/<cd>/luyen-tap/bundle.json --lesson <id> --target luyen_tap`.
- Kiểm lại sau ghi (truy vấn chỉ đọc `lesson_items` của bài: đủ 3 mục, số dạng, số câu). Bài tập mẫu là file tĩnh → cần deploy (`bash scripts/deploy.sh`, theo [[feedback_deploy_autonomy]]).
- Bài **vẫn ẩn**. Bật Hiện chỉ khi thầy duyệt, và phải trước `gui_ngay` của tuần dùng bài (thông báo chỉ gắn link bài đã Hiện).

## 7. Chốt
1. Cập nhật dòng của CĐ trong `lich-soan-bai.md` (đã ghi DB / chờ duyệt / còn thiếu gì) — chỉ sửa dòng đó.
2. Thêm một gạch ngày vào `docs/memory/project_thachlab_khoa_hsg9_vat_ly.md`; ĐANG CHỜ trong `docs/STATE.md` 1–2 dòng.
3. Commit theo đường dẫn (`git commit -- <path>…`), mô tả nêu mã quy tắc thiết kế nếu có.
4. Rút kinh nghiệm (bắt buộc theo AGENTS.md) → ghi vào mục dưới, hoặc vào skill chặng tương ứng nếu thuộc chặng đó.

## 8. Dòng "Bộ 12 câu tự luyện" trong lịch (bài tập tuần, không phải chuyên đề)
Mẫu đã chạy: bài 167 "Bài tập tuần này" (Cơ học VD–VDC, 11/10).
1. Soạn bộ đề in theo `soan-bai-tap-tu-luan-hsg` (12 bài, 3–4 ý khó dần, gợi ý 3 tầng, lời giải tập riêng, PDF bằng `_tools/trang-mau-sach`), lưu gốc ở `01_Chuyen_de/<tên bộ>/` thư mục Documents.
2. Kiểm: `kiem-code` giải độc lập từ đề không đáp án + soát **điều kiện phụ** (bình đủ cao, dây không giãn, công suất nào, lực cản áp cho đoạn nào); soát hình.
3. Số hoá: tạo bài ẩn ở đầu chương (mẫu `scripts/tao-bai-bt-tuan-hsg.mts`, đổi TITLE/CHAPTER), mỗi bài tự luận thành một dạng `buoc[]` (mẫu `scripts/data/bai-tap-mau/hsg-tuan/` + `167.json`), ghi bằng `publish-bai-tap-mau.mts`; PDF để ở `public/hsg9/` làm bản in.
4. Thêm id bài vào `lessons` của tuần tương ứng trong `tuan.json`; bật Hiện trước `gui_ngay`.

## Nhật ký rút kinh nghiệm
- 2026-10-17 · CĐ07/14/17 dò lần 2 (3 kiem-code song song, mỗi bài một agent): nội dung sạch, lỗi còn lại là chữ SVG màu nền tối (#38bdf8/#fb923c/#34d399) khó đọc trên nền sáng, cả trong mô phỏng bài tập mẫu → bước gom `build-hinh-<id>.py` hậu xử lý màu trong `<text>/<tspan>` (mẫu 156/178), đưa vào brief soạn từ đầu. Hai số cùng tên khác công thức (nón tối 374 400 vs ℓmax 374 500) → chốt một giá trị làm tròn trong nguon.md trước khi giao agent. `deploy.sh` hỏng vì file `.mts` chưa commit của phiên khác → deploy từ worktree sạch tại HEAD (`cp -cR node_modules`, symlink `.env.local`; Turbopack không nhận node_modules symlink). Dry-run `dang-hsg9-dot*.sh` có câu hỏi y/N: chạy `yes n | …`, đừng `| tail` (che câu hỏi, treo).
- 2026-10-16 · CĐ16 + CĐ12 cùng lúc (8 agent soạn → 4 kiem-code → gửi sửa về đúng agent soạn bằng SendMessage → 1 agent dò lần 2): chạy trơn, kiểm chéo không ra lỗi đáp số, chỉ ra trùng số giữa thử thách lý thuyết và luyện tập, chữ SVG cỡ 9–12, KaTeX "4,8" thành "4, 8", ký hiệu $Q_2$ lệch giữa lý thuyết và bài tập mẫu → đưa các điểm này vào brief (mục 3); dàn ý nên ghi sẵn ký hiệu dùng chung. `upload-lesson.mts` hỏi dán service key → `dang-hsg9-dot3.sh` tự đọc từ `.env.local`; không bao giờ dán khoá tay.
- 2026-10-10 · Bộ tự luận Cơ học VD–VDC: đáp số đúng 12/12 nhưng 9 lỗi là điều kiện phụ thiếu trong đề → soát đề kín là bước riêng, không gộp vào "giải lại khớp". Agent xem ảnh nhỏ báo sai hình → in toạ độ SVG kiểm trước khi vẽ lại. Soát lại vài hình thì render từng SVG bằng Chrome headless xem ở phiên chính, không cho agent soát lại cả bộ trang.
- 2026-10-10 · CĐ01/02, đợt 1: kiểm chéo bắt lỗi dù agent soạn đã tự giải (thiếu nghiệm bài nhiều trường hợp, hình lộ đáp số, `chon_buoc_ke` sai thật ra đúng) → giữ 2×kiem-code, không bỏ khi vội.
- 2026-10-16 · CĐ15: chia bài tập mẫu cho 3 agent theo module + main gom, chạy thử riêng bằng biến môi trường để không ghi đè nhau; mục rỗng phải có trên DB trước khi ghi (migration tạo mục).
- 2026-10-16 · Lịch dạy 17 buổi: nội dung web phải Hiện trước ngày gửi BTVN; các bài đang Hiện còn thiếu luyện tập tự chấm → mỗi CĐ mới soạn luôn ≥6 câu luyện tập, không để đợt sau.
- 2026-10-17 · Bổ sung chỉ luyện tập cho bài đã Hiện (CĐ03/04): 2 agent soạn + 2 kiem-code, nhẹ hơn cả quy trình. `dang-hsg9-dot4.sh --yes <cặp>` vẫn ghi lại lý thuyết + bài tập mẫu (nội dung y hệt, có sao lưu) — chấp nhận được, không cần deploy nếu bài tập mẫu không đổi. Bắt agent in distractorNotes trước khi kiểm chéo làm lộ đáp án: dặn kiem-code tự giải từ phần đề rồi mới đối chiếu.
- 2026-10-27 · Đăng lại lý thuyết 18 CĐ (CĐ00–CĐ17) sau khi thêm khối cột lề: id lesson theo `docs/HSG9-KHUNG.md` (CĐ17=178), dùng `cap-nhat-ly-thuyet.sh content/hsg9/<cd>/theory.html <id> --yes` (chỉ ghi mục ly_thuyet, giữ nguyên Hiện/Ẩn). Worktree không có `.env.local` → symlink từ repo chính (gitignore) rồi chạy trong tab terminal. CĐ06/CĐ08/CĐ09/CĐ17 sát/quá trần 2500 từ: chỉ thêm câu chốt; muốn đủ khối phải tách bài. Chi tiết kỹ thuật: nhật ký skill `soan-bai-ly-thuyet-tuong-tac` cùng ngày.
