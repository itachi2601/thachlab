---
name: project-thachlab-giai-lai-ngan-hang
description: "Sinh lại lời giải ngân hàng bằng Haiku 5.5 (Batch) + Sonnet 5.5 kiểm câu lệch; 17/10/2026 đã ghi 349 câu lệch, còn 7.800 câu khớp chờ ghi"
metadata:
  node_type: memory
  type: project
---

**Việc:** lời giải cũ trong `question_bank` trống/quá ngắn (<80 ký tự) hoặc khó hiểu → sinh lại. 10.295 câu trống/ngắn, 1.922 có ảnh/SVG bị bỏ → 8.373 câu hợp lệ.

**Pipeline (17/10/2026), tất cả ở `scripts/`:** `sinh-loi-giai-ngan-hang.mts` (mẫu 200, gọi thường — chậm, đừng dùng cho số lớn) → `batch-giai-lai.mts nop|thu` (Haiku 5.5 Batch, $1,69 cho 8.373 câu) → `nop2|thu2` (Sonnet 5.5 giải mù lại câu Haiku lệch DB, $1,69/394 câu) → `lap-duyet-giai-lai.mts` (trang HTML duyệt) → `ap-dung-giai-lai-lech.mts [--apply]` (ghi DB, sao lưu `scripts/logs/giai-lai-lech-backup-*.json`). Lib dùng chung: `scripts/lib/giai-lai-chung.mts` (prompt, so khớp, `tachMuiTen` tách dòng ⇒ không tốn token, `katexLoi`). Kết quả: `scripts/data/giai-lai/ket-qua.json` (Haiku), `ket-qua2.json` (Sonnet).

**Đã ghi DB 17/10:** 228 câu đổi đáp án theo AI (Sonnet = Haiku ≠ DB) + 122 câu giữ đáp án, dùng lời giải Sonnet (349 ghi, 1 bỏ vì KaTeX lỗi); 44 câu bất đồng/parse lỗi bị ẩn (archived, note "17/10/2026: giải lại bằng AI"); 203 đề trong `exams.questions` cập nhật bản sao. Thầy quyết theo nhóm, KHÔNG duyệt từng câu.

**Còn chờ:** ~7.800 câu Haiku khớp đáp án DB (`ket-qua.json`, khop=true, không katex_loi/mui_ten_con) chưa ghi — theo kế hoạch cần `kiem-code` soát mẫu 30 câu rồi ghi bằng script cùng kiểu (sao lưu, cập nhật cả `exams.questions`); 1.922 câu có ảnh/SVG chưa làm; ~1.300 câu Haiku ghi chú "đề mơ hồ" (1.070 trong số đó vẫn khớp).

**Why:** thầy muốn lời giải rõ, logic, mỗi phép suy ra một dòng đầu bằng ⇒ ([[feedback-xuong-dong-tung-truong-hop]]); chi phí tổng ~$3,5 trên $20 credit Console.

**How to apply / bài học:** (1) Haiku không tuân thủ 100% quy tắc ⇒ → luôn hậu xử lý `tachMuiTen`. (2) Sonnet viết vài dòng chữ trước JSON → parse tìm `{"answer"`, đừng lấy `{` đầu. (3) Ghi lời giải phải cập nhật CẢ `exams.questions` (trigger chỉ đồng bộ nhãn); bản sao tìm theo nội dung chữ chứ không chỉ `source_index` (đề bị đổi thứ tự, 6/349 câu không còn bản sao). (4) Trang duyệt HTML >512 KB không mở được trong khung Browser của app → mở bằng `open -a "Google Chrome"`. (5) Gọi thường Haiku ~200 câu/giờ, Batch 8.373 câu ~10 phút. (6) DeepSeek: key trong `.env.local` đang bị comment, chưa chạy so sánh.

**18/10 (đợt 2): kiem-code soát mẫu 30 câu khớp** — 24 tốt, 4 nhẹ, 2 nặng; cả 2 câu nặng nằm trong nhóm Haiku có ghi chú "đề mơ hồ" (một câu tiếng Anh không có bài đọc, một câu đề lỗi ký tự) → quyết định: chỉ ghi nhóm khớp mà Haiku KHÔNG ghi chú (6.730 câu), giữ 1.070 câu có ghi chú để thầy duyệt. Script `scripts/ap-dung-giai-lai-khop.mts [--apply] [--conc=N] [--max-de=N]` (chạy lại được; tự sửa `<`/`>` trong $…$ thành \lt \gt). **Chậm:** cập nhật `exams.questions` tốn ~vài giây MỖI câu thay đổi (trigger đồng bộ ngân hàng) — song song nhiều luồng còn chậm hơn (6 luồng ≈ 130 s/đề vs 1 luồng); dùng `--conc=1`, 6.800 bản sao ≈ vài giờ. Sau bước exams, script tự ghi nốt `question_bank` những câu chưa được trigger đồng bộ.

**Trạng thái cuối phiên 2026-10-18 (chưa commit gì; script + dữ liệu `scripts/data/giai-lai*/` còn untracked):**
- `ap-dung-giai-lai-khop.mts --apply --conc=1` ĐANG chạy trong tab Terminal của thầy: lúc chốt phiên exams 200/716 đề (~30 s/đề → còn vài giờ). Xong bước exams nó tự ghi nốt `question_bank`. Sao lưu: `scripts/logs/giai-lai-khop-backup-*.json` (mỗi lần chạy một file; gốc câu bank + đề).
- **Phiên sau việc đầu tiên:** đọc output tab (hoặc chạy lại script — idempotent, câu/đề đã có lời giải ≥80 ký tự tự bị bỏ), đối chiếu DB: đếm câu trong `ket-qua.json` (khop, !ghi_chu, !katex_loi, !mui_ten_con) có `question_bank.explanation` = lời giải mới; báo số lỗi.
- Chưa làm: 1.070 câu khớp nhưng Haiku ghi chú mơ hồ (cần trang duyệt riêng, hai câu "nặng" của mẫu 30 nằm đúng nhóm này); 1.922 câu có ảnh/SVG; 8 câu Sonnet parse lỗi bị ẩn cùng 36 câu ba bên khác nhau; `ket-qua.json` (9 MB) chưa quyết có commit không (nên gitignore dữ liệu lớn, chỉ commit script).
- Thầy đã chốt: nhóm "DB nghi sai" (228) đổi đáp án theo AI mà không duyệt từng câu → vài câu có thể bị đổi sai; bản sao lưu `scripts/logs/giai-lai-lech-backup-1792236469277.json` để hoàn tác.
- Rút kinh nghiệm phiên: (1) đo tốc độ ghi trên mẫu nhỏ lệch (đề thử ít câu đổi) → ước tính 6 s/đề thật ra ~30 s/đề; đo trên đề điển hình. (2) Thầy quyết theo nhóm, ít duyệt từng câu; muốn lời giải có dòng ⇒ riêng. (3) DeepSeek chưa so sánh được vì `DEEPSEEK_API_KEY` trong `.env.local` bị comment.

**18/10 (đợt 3) — SỰ CỐ + soát câu mơ hồ:**
- `ap-dung-giai-lai-khop.mts` (cập nhật `exams.questions`) làm trigger exams→question_bank chép đáp án CŨ trong bản sao đề đè lên đáp án ngân hàng của MỌI câu nằm trong đề được ghi: 577 câu bị đổi đáp án (458 trắc nghiệm, 70 trả lời ngắn, 49 đúng/sai) trong 8.373 câu đã kiểm. Đã khôi phục bằng `scripts/khoi-phuc-dap-an-giai-lai.mts --apply` (sao lưu `scripts/logs/khoi-phuc-dap-an-backup-1792256579238.json`); còn 5 câu lệch nghi do khác định dạng. **CHƯA kiểm** các câu ngoài tập 8.373 nằm trong 716 đề đó (không có mốc trước) — nên đối chiếu với `question_bank_backup_20260930`.
- Hệ quả chưa xử lý: bản sao trong `exams.questions` của ≥577 câu mang đáp án KHÁC ngân hàng (ngân hàng đúng theo Haiku/Sonnet) → HS làm các đề đó có thể bị chấm theo đáp án cũ. Cần thầy quyết có đồng bộ đáp án bản sao đề theo ngân hàng không.
- **Chưa ghi nữa lời giải nào sau sự cố.** Không chạy lại script khop/exams cho tới khi tắt hoặc tránh trigger.
- 1.070 câu "khớp nhưng Haiku ghi chú mơ hồ": Sonnet (11 agent kiem-code, lô `scripts/data/giai-lai/mo-ho/lo-NN.json` → `kq-NN.json`, lô 08 làm lại `kq-08b.json`) chia: ghi thẳng 856, hỏi thầy 104, ẩn 76, đổi đáp án 3, lời giải cần sửa 31. Trang duyệt `scripts/data/giai-lai/mo-ho/duyet/duyet.html` (`lap-duyet-mo-ho.mts`, >512 KB → mở bằng Chrome); thầy lưu `phan-hoi.json` cùng thư mục. Chưa có script áp dụng phản hồi.
- Rút kinh nghiệm: (1) script ghi vào `exams` phải kiểm trigger trước — đo `question_bank.updated_at` của câu NGOÀI kế hoạch ngay sau lô thử đầu; (2) sau mọi lượt ghi hàng loạt, so lại đáp án với mốc trước, không chỉ đếm số ghi; (3) agent soát lô trả "ghi" hàng loạt với lý do mẫu giống nhau là dấu hiệu không tự giải — bắt làm lại và yêu cầu ly_do riêng từng câu; (4) agent song song dùng chung thư mục tạm sẽ ghi đè file nhau — chỉ định thư mục riêng.
- 18/10 sau sự cố: đồng bộ đáp án bản sao đề theo ngân hàng bằng `scripts/dong-bo-dap-an-exams.mts --apply` (579 câu ở 132 đề, sao lưu `scripts/logs/dong-bo-dap-an-exams-backup-1792278450199.json`); so lại `so-dap-an-exams-ngan-hang.mts` chỉ còn 5 câu lệch (đề 35#10, 73#2, 133#14, 140#8, 544#25 — xem `scripts/data/giai-lai/ngoai-tap-xem.json`): 35 và 133 đề sai (ngân hàng đúng), 140 và 544 ngân hàng sai (đề đúng), 73 mơ hồ (trung bình 1202 vs căn quân phương 1304). Chưa sửa.
