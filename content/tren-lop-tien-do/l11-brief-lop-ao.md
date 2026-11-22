# Brief lớp ảo (bước 6 skill ban-chieu-tren-lop) — dùng cho cả agent THẦY và agent HỌC SINH

Worktree: <worktree của phiên>. Thư mục làm việc: `content/lesson-samples/<slug>/thu-lop-ao/`. Không commit, không sửa file ngoài thu-lop-ao/.
Mẫu (đọc lướt 1–2 file để biết độ dài/giọng): `content/lesson-samples/l11-dien-the/thu-lop-ao/` (`dung-2.md`, `hs-2.md`, `phan-hoi-2.md`, `gop-y.md`).

## Vai THẦY
Lượt 1 (soạn): đọc `../tren-lop.src.html` (màn chiếu), `../tren-lop-ghi-chu.html`, ruột tập `scripts/ruot-tap/l11-bai<N>.mjs` (CHỈ trang 1–5). Viết:
- `sach-trong.md`: trang 1–5 của Tập chép dạng chữ, mọi chỗ điền thành `[__k__]` đánh số liên tục, BỎ đáp án.
- `dung-1.md … dung-K.md`: mỗi điểm dừng một file — thầy nói gì, màn nào chiếu (chữ trên màn, phần đáp án chỉ ghi sau dòng `--- sau khi lớp làm ---`), học sinh điền ô nào trong Tập.
- `nhat-ky-thay.md` mục "Soát trước giờ": chỗ màn / ghi chú / Tập lệch nhau (số câu, mã ô, đánh số, nhãn lộ đáp án, phương án dùng khái niệm chưa dạy, thứ tự lật trang).
Lượt 2 (sau khi học sinh làm): đọc `hs-*.md`, `sach-hs.md`; viết `phan-hoi-1..K.md` (học sinh hiểu sai/phải đoán ở đâu, do tài liệu nào), bổ sung `nhat-ky-thay.md`, rồi viết `gop-y.md`: bảng mục đánh số `file · vị trí · sửa gì · ưu tiên (cao/vừa/thấp) · bằng chứng (hs-N dòng…)`. Tập trung chỗ "phải đoán" và "tài liệu lệch nhau"; đừng tin tỉ lệ đúng. Không viết mục "Đã xử lý" (phiên khác viết).

## Vai HỌC SINH
Lớp 11 trung bình–khá, chỉ biết kiến thức tới HẾT bài trước (bài <N−1>), chưa học bài này. CHỈ đọc file trong thu-lop-ao/ (`sach-trong.md`, `dung-*.md`), không mở file nào khác trong repo.
Đi lần lượt dung-1 → dung-K: với mỗi điểm dừng, ĐỌC PHẦN TRƯỚC dòng `--- sau khi lớp làm ---` rồi viết câu trả lời/dự đoán vào `hs-N.md` TRƯỚC, sau đó mới đọc phần sau dòng đó và ghi "sau khi xem đáp án: đúng/sai, hiểu ra gì". Chỗ không chắc ghi "(đoán)" kèm lý do; chỗ khó hiểu chữ/ký hiệu thì ghi rõ chữ nào. Cuối cùng điền `sach-hs.md` = sach-trong.md với mọi `[__k__]` đã điền (ô về nhà chưa học thì ghi "(về nhà)").
Thật thà: học sinh thật không biết thì không biết.
