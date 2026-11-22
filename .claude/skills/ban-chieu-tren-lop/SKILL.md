---
name: ban-chieu-tren-lop
description: Dựng "đường trên lớp" cho MỘT bài đã có lý thuyết + ruột tập: bản chiếu tivi 50" (tren-lop.html, mỗi màn một ý, chữ 5,2vh, clip có điểm dừng, PhET), ghi chú dạy, khớp Tập, cuối tiết đề kiểm tra lý thuyết (QR); rồi chạy lớp ảo (agent thầy dạy agent học sinh điền Tập) và sửa theo góp ý. Dùng khi thầy nói "làm bản chiếu bài X", "bài trên lớp", "/ban-chieu-tren-lop".
---

# Bản chiếu trên lớp + lớp ảo (mẫu: L11 Bài 20 Điện thế)

**Bài mẫu chuẩn** — đọc trước, sao cấu trúc, đừng tự nghĩ lại: `content/lesson-samples/l11-dien-the/`
`tren-lop.src.html` (CSS + JS dùng lại nguyên khối), `build_tren_lop.py`, `build_qr.mts`, `tren-lop-ghi-chu.html`,
`thu-lop-ao/` (lớp ảo + `gop-y.md` 25 mục — đọc mục "Đã xử lý" để biết lỗi hay gặp). Lịch sử: `git log --oneline -- content/lesson-samples/l11-dien-the/tren-lop*`.

**Không**: đăng DB, deploy, chạy `cap-nhat-ly-thuyet.sh`, sửa đề kiểm tra, sửa `theory*.html`/`bundle.json`. Ruột tập
`scripts/ruot-tap/<lop>-bai<N>.mjs` ĐƯỢC sửa (chưa in) nhưng PDF phải giữ nguyên số trang. Commit theo đường dẫn.

## Bước
1. **Nguồn**: bài lý thuyết `content/lesson-samples/<slug>/theory.html` (đọc đoạn, không đọc hết) + ruột tập `.mjs` (trang 1–5 = học trên lớp, mã ô `t·k`). Bản chiếu đi THEO Tập: mỗi điểm dừng ghi `tr.X · ô t·k` ở góc màn.
2. **Đề cuối tiết**: tìm đề "Kiểm tra lý thuyết" của bài trong DB (`exams`, theo lesson_id; tab terminal vì sandbox chặn supabase), lấy mã đề + mục → QR bằng `build_qr.mts` (kiểm giải mã lại `scripts/kiem-qr.mts`). Không có đề → màn cuối là Trả bài + Về nhà, ghi treo trong báo cáo.
3. **Bản chiếu** `tren-lop.src.html`, 6 điểm dừng ≈ 30 phút + 15 phút đề:
   - Một cột, mỗi màn một ý (N1); chữ `min(5.2vh,2.95vw)`; hình SVG lấy từ theory.html qua `<!--FIGn-->`, phóng nhãn (`.fN svg text{font-size}`) để chữ hình ≥ 0,7 chữ thường.
   - Câu A–D chép **y chữ Tập**; phương án không dùng khái niệm chưa dạy, không loại được ngay bằng so sánh số. Câu dự đoán mở bài: đáp án ở màn "Quay lại …" cuối tiết, không lộ ở nhãn màn khác.
   - Hình + đáp án mở ra phải nằm CẠNH nhau (`.hai`), đừng để đáp án ép hình nhỏ.
   - PhET (skill `phet`): nhúng nút mở tab, câu đoán trước, ô mở kết quả.
   - Clip tự dựng (`content/thi-nghiem/video-khung/<id>.json` có mốc giây): màn `.vg` video trái + `.buoc` phải, `data-bat/data-het/data-dung`. Mốc lấy từ engine (`~/.venvs/video-thi-nghiem/bin/python3`, `engine.build(CLIP)`), cách đầu cảnh/chuyển động ≥ 0,3 s, rồi **xem khung hình thật** (ffmpeg tile → agent đọc ảnh). Clip trùng ý PhET thì để "mặc định bỏ qua".
4. **Ghi chú dạy** `tren-lop-ghi-chu.html`: chuẩn bị (tivi F11, tải clip), biểu quyết, đi theo Tập, từng điểm dừng (phút · trang · ô · lời thầy), phiếu giấy dự phòng, thiếu/dư giờ, sau buổi dạy.
5. **Kiểm máy**: build; trình duyệt 1280×720 và 1920×1080, mở hết `.an[hidden]` → không `.man` nào `scrollHeight>clientHeight`; đo chiều cao hình + cỡ chữ nhỏ nhất trong hình khi đáp án mở; `.katex-error` = 0; 375px không cuộn ngang; clip dừng đúng mốc.
6. **Lớp ảo** (agent, lưu `thu-lop-ao/`): agent THẦY (sonnet) lập `sach-trong.md` (trang 1–5 bỏ đáp án) + `dung-N.md` từng điểm dừng + `phan-hoi-N.md` + `nhat-ky-thay.md`; agent HỌC SINH (sonnet, chỉ đọc file trong thu-lop-ao, kiến thức tới bài trước, chỗ đoán ghi "(đoán)") điền `sach-hs.md` + `hs-N.md`. Phiên chính chỉ nhắn "lượt N" (tin ≤ 40 từ). Cuối: thầy viết `gop-y.md` (file · vị trí · sửa gì · ưu tiên · bằng chứng). Tin mục "phải đoán" và "tài liệu lệch nhau", không tin tỉ lệ đúng.
7. **Sửa theo góp ý** (cao + vừa đã tự kiểm), chạy lại bước 5, PDF ruột tập `node scripts/ruot-tap/<file>.mjs` giữ số trang; ghi mục "Đã xử lý" cuối gop-y.md; commit.

## Báo cáo mỗi bài (một dòng)
`bài · commit · số màn · đề cuối tiết (mã/không có) · số góp ý làm/bỏ · việc treo`

## Nhật ký rút kinh nghiệm
- 2026-11-20 · Đáp án mở ra dưới hình ép hình còn 15% màn, chữ hình 13px — kiểm tràn không bắt được → đo chiều cao hình khi đáp án mở, dùng bố cục `.hai`.
- 2026-11-20 · Mốc dừng clip tính từ code lệch 0,1–0,2 s ở chỗ chuyển động/chuyển cảnh (dừng vào khung trắng, lộ đáp án) → cách ≥ 0,3 s và xem khung hình thật.
- 2026-11-20 · Học sinh ảo đúng 66/66 ô nên tỉ lệ đúng vô nghĩa; góp ý giá trị là chỗ phải đoán và chỗ màn/ghi chú/Tập lệch nhau (ô 4·3 "8 câu" vs đề 20 câu, phương án dùng từ chưa học).
