# Đề xuất cải tiến bài lý thuyết sau đợt "học thử vai học sinh" (26/11/2026)

Nguồn: bàn giao từ phiên chat cloud (đóng vai HS THPT trung bình đọc `l10-luc-ma-sat`, `l11-luc-coulomb`, quét 83 bundle).
Phiên Mac 26/11 đã đo lại, sửa những chỗ chắc chắn, và gom những chỗ cần thầy quyết vào đây. **Chưa ghi DB.**

## Đã sửa trong repo (chờ duyệt để đăng bằng `cap-nhat-ly-thuyet.sh`)

| Bài | Sửa | Commit |
|---|---|---|
| `l10-luc-ma-sat` (lesson 63) | Mục 1 giới thiệu luôn $F_{msn\,max} = \mu_n N$ + "μ_n đo ở mục 4", khớp dòng chốt ô 1·4 (không đổi Tập) | 4b0990acd |
| `l10-luc-ma-sat` | Hình 3 trở lại SVG tự vẽ (P, P_x, P_y, N, F_ms, α = 30°); ảnh OpenStax (w, f, 25°) vào ô "📷 Bấm xem ảnh thật" | 4b0990acd |
| `l11-luc-coulomb` (lesson 35) | Hộp cân điện tử ghi "số liệu mô phỏng" (T8) | e8b50873f |
| `l11-luc-coulomb` | Mục 2: câu thay số ngay sau công thức (3 nC, −4 nC, 6 cm; nhiễu: sai chiều, quên bình phương, quên đổi cm) | e8b50873f, 0fc2bf996 |
| `l11-luc-coulomb` | Mục 4: ví dụ số tam giác đều (bấm xem) + câu tự kiểm hợp lực góc 120° | e8b50873f, 0fc2bf996 |

Đã soát: agent `kiem-code` tính lại mọi số, chạy KaTeX (0 lỗi), `validate_bundle` ok. **Chưa chụp 375px** trong app.

## P1 — Đề cuối bài "trùng" câu trong bài: là CHỦ Ý, không sửa

- Script mới: `npx tsx scripts/kiem-trung-cau-de-ly-thuyet.mts [--md out.md] [--prefix l10-]` (chỉ đọc file).
- `exam` trong `bundle.json` ("Kiểm tra nhanh — …", 5–7 câu): **284/461 câu (62%) trùng**, 17 bài trùng 100%.
  Đây đúng quy ước skill `soan-bai-ly-thuyet-tuong-tac` mục 7: *"dùng chính các câu tự kiểm tra trong bài làm đề Luyện tập nhỏ"*.
- Bộ 20 câu "Kiểm tra nhanh" riêng (`scripts/data/theory-quiz/<id>.json`, skill `soan-quiz-ly-thuyet`) có ở 78/83 bài: **chỉ 90/1.535 câu (6%) trùng** → đề kiểm thật sự đã khác bài.
- Cần thầy quyết (chỉ khi muốn đổi quy ước):
  - **(a) Giữ nguyên** — đề 5–7 câu là ôn nhắc lại, bộ 20 câu mới là kiểm. *Đề xuất chọn.*
  - (b) Đổi số liệu/bối cảnh cho đề bundle (giữ dạng + bẫy). Tốn ~83 bài × 5 câu, lợi ích nhỏ vì đã có bộ 20 câu.

## P2 — Dòng "đọc khoảng N phút"

- Số phút do `lint_do_dai.py` tính theo **từ hiện ngay** ở 140 từ/phút — không tính ô bấm mở, phản hồi quiz, clip. Có ở ~19/83 bài (phần lớn 15–20 phút).
- HS làm hết câu, mở ô, xem clip mất nhiều hơn hẳn (phiên học thử ước 35–45 phút, chưa đo trên HS thật).
- Phương án:
  - **(a) Hai mốc** "Đọc ~N phút · học kỹ (làm câu, mở ô, xem clip) ~M phút"; M = tổng từ/140 + giây clip + 30 s/câu, tính trong `lint_do_dai.py`. *Đề xuất chọn*, kèm ghi vào mọi bài khi build lại.
  - (b) Thêm "điểm dừng" sau mục II ("Nghỉ được ở đây — phần sau là bẫy và bài toán mẫu"). Hợp quy tắc N5/G2 (nhiều cửa sổ ngắt) nhưng cần thầy chốt câu chữ.
- Đo: so thời gian thật trên trang (nếu có log thời gian mở bài) với M.

## P3 — "✍️ Tập ô …", "Ruột tập" với HS tự học

- Có ở 81/83 bài. HS ngoài lớp thầy không có Tập → không hiểu dòng này.
- Phương án (đổi UI → theo `docs/QUY-TAC-THIET-KE.md`, thầy chọn):
  - **(a) Ẩn theo lớp**: chỉ HS thuộc lớp thầy dạy (có ruột tập) thấy dòng `✍️ Tập ô`; người khác thấy "✍️ Ghi vào vở · đối chiếu N dòng". Không đổi nội dung bài, chỉ đổi nhãn summary lúc render. *Đề xuất chọn* (giảm tải nhận thức: không bắt HS đoán thứ không có).
  - (b) Giữ nguyên + 1 dòng giải thích đầu bài và link tải ruột tập PDF.
- Cần quyết: lớp nào "có Tập"; có cho tải ruột tập công khai không.

## P4 — Bài toán mẫu chỉ có đáp số: là quy ước mới, không phải lệch

- 60/83 bài "Bấm xem đáp số" + link "Bài mẫu · Dạng N"; 16 bài còn lời giải trong lý thuyết. Đây là đợt rút bài toán mẫu 25/11 (memory `project_thachlab_on_5_phut`); Coulomb (35), khái niệm điện trường (36), nguồn điện (43) **cố ý để nguyên** vì chưa có dạng tương ứng.
- Đề xuất nhỏ (thầy quyết): trong hộp "Tự giải trước", thêm 1 ô "💡 Gợi ý bước đầu" (một câu, không số) trước ô đáp số — cho HS bí mà chưa muốn sang trang Dạng. Làm theo script cho cả 60 bài nếu duyệt mẫu 1 bài.

## P5 mở rộng — mục ≥3 công thức mà không có câu tự kiểm (22 mục)

Quét heuristic (`$$` + bảng công thức trong `<h4>`, không có `.tl-quiz`); một số mục có ví dụ trong ô bấm xem nên chưa chắc là thiếu. Ưu tiên soát:
`l10-chuyen-dong-thang-bien-doi-deu` mục 4 (7 CT), `l10-toc-do-van-toc` mục 1 (7), `l11-co-nang-dao-dong` mục 6 (8), `l11-khai-niem-dien-truong` mục 5 (6), `l11-bai-tap-song` mục 2 (5), `l11-van-toc-gia-toc` mục 4 (5).
Còn lại: `l10-chuyen-dong-nem` 1, 4 · `l10-dinh-luat-2-newton` 5 · `l10-giai-bai-toan-dong-luc-hoc` 1 · `l10-nang-luong-cong-co-hoc` 3 · `l10-thuc-hanh-do-toc-do` 4 · `l10-thuc-hanh-dong-luong` 3 · `l11-co-nang-dao-dong` 1, 2 · `l11-giao-thoa-song` 2, 4 · `l11-nang-luong-cong-suat-dien` 3 · `l11-nguon-dien` 5 · `l11-tu-dien` 5 · `l12-noi-nang-dl1` 4.

## Việc cần thầy quyết (tóm tắt)

1. Duyệt 2 bài đã sửa (63, 35) → đăng bằng `cap-nhat-ly-thuyet.sh` ngoài giờ HS.
2. P1: giữ quy ước (a)?
3. P2: hai mốc thời gian (a) và/hoặc điểm dừng (b)?
4. P3: ẩn "Tập ô" theo lớp (a) hay giải thích + link (b)?
5. P4: thêm ô gợi ý bước đầu?
6. P5: có làm tiếp 6 mục ưu tiên không?
