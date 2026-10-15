# Thành tựu qua các mùa & tương tác giữa avatar — spec (thầy duyệt hướng 15/10/2026)

Nghiên cứu nền: `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md` (Hanus & Fox 2015, Dahl–Steinberg, SDT).
Nguyên tắc: **khoe năng lực, không khoe thứ hạng**; tương tác **tích cực, có mẫu sẵn, hợp tác hơn đối đầu**.
Chỉ xây phần HS nhìn thấy **sau 25/10** (hết mùa thử nghiệm) và sau khi có số đo A1.

## 0. Hiện trạng (đã có trước spec này)
- Mọi bảng rank khoá theo `season_id` → mở mùa 2 **không mất** mùa 1.
- `rank_close_season` ghi `rank_season_results` (rp, bậc, số danh hiệu); `rank_seasons_of` đã đọc lịch sử mùa.
- Migration `20261015200000_rank_ho_so_thanh_tuu_mua.sql` (chờ chạy) bổ sung bản chụp: tên/thứ tự bậc, lớp lúc đóng,
  danh hiệu nhận **trong mùa**, số tuần đạt mục tiêu, RP theo tuần, YCCĐ đang Nắm vững; thêm `rank_snapshot_season`
  (idempotent; mùa đang mở chỉ chụp khi đóng hoặc p_force). Đã thử trên PGlite: chụp, chạy lại, đóng mùa, rollback.

## 1. Việc đóng mùa 1 (25/10)
1. Trước khi đóng: xem thử trong transaction: `begin; select rank_snapshot_season(4, true); select … from rank_season_results; rollback;` (giả lập JWT staff như `rank_recompute_season`) → đối chiếu vài em. Chụp thường bị chặn khi mùa đang mở (để `rank_seasons_of` không hiện số cũ).
2. Đóng mùa trên `/quan-tri/xep-hang` (gọi `rank_close_season`, tự chụp lại lần cuối).
3. Chạy A1 (`scripts/do-mua-1.mts`) → quyết mùa 2 theo mục 4.

## 2. Hồ sơ thành tựu (trang HS + khung avatar) — làm trước
| Thành phần | Nguồn | Ghi chú |
|---|---|---|
| **Thành tựu năng lực** (nổi nhất): số YCCĐ Nắm vững, danh hiệu chủ đề | `mastered_count`, `season_titles` | Không reset; so với chính em mùa trước |
| **Dấu mùa**: huy chương nhỏ "Mùa 1 · Tinh Nhuệ" | `tier_name`, `tier_sort` | Hiện ở hồ sơ + góc khung avatar (tối đa 1 dấu cao nhất); RP mùa sau về 0 |
| **Dòng hành trình**: "Mùa 1: 12 YCCĐ → Mùa 2: 27 YCCĐ" | các dòng `rank_season_results` | Chỉ em + phụ huynh + GV thấy |
| **Ghi nhận nhiều kiểu** cuối mùa: Bền bỉ (tuần đạt mục tiêu), Tiến bộ nhất (RP nửa sau − nửa đầu từ `weekly_rp`, hoặc YCCĐ tăng), Giúp bạn (mục 3) | các cột mới | Mỗi lớp nhiều người được nhắc; không xếp số thứ tự |
| **Giấy chứng nhận mùa** (PDF/QR xác thực, gửi phụ huynh) | snapshot | Viết dạng thông tin ("đã nắm vững 23 YCCĐ chương Dao động"), không "hạng 1" |

Quyền riêng tư: em chọn ẩn/hiện dấu mùa công khai (mặc định hiện cho bạn cùng lớp); đếm tỉ lệ tắt để đo.

## 3. Tương tác giữa avatar — làm sau, tuỳ số A1
- **Cổ vũ một chạm**: 3–4 câu mẫu (👏 Cố lên, 🔥 Giỏi quá, 💪 Chuẩn bị thăng hạng nhé). Người nhận thấy tổng, không có
  bảng "ai được cổ vũ nhiều nhất". Giới hạn số lượt/ngày, không có chữ tự do.
- **Mục tiêu chung của lớp**: "cả lớp nắm vững N YCCĐ tuần này" — thanh tiến độ + avatar những bạn đã góp.
- **Bạn đồng hành**: em đã Nắm vững một YCCĐ được gợi ý giúp bạn đang mắc ở đó; GV/trợ giảng ghép cặp (nối với
  `ta_student_handoffs`/phụ đạo). Ghi nhận "Giúp bạn" vào hồ sơ mùa.
- **Không làm**: chat/bình luận tự do, thách đấu 1–1 công khai, đếm lượt thích/người theo dõi, ép hiện bậc cạnh tên.

## 4. Cổng quyết định mùa 2 (từ A1)
- Nhóm 25% dưới còn ≥60% làm bài ở tuần 4–5 → làm mục 2 rồi mục 3.
- Thấp hơn → chỉ làm phần năng lực của mục 2 (YCCĐ, hành trình), giảm bảng tuần/vinh danh, hoãn mục 3.

## 5. Đo
- Tỉ lệ quay lại tuần đầu mùa 2, tách nhóm trên/dưới.
- Tỉ lệ tắt hiện công khai (cao = các em ngại so sánh).
- Lượt cổ vũ/ghép bạn đồng hành có tương quan với số bài làm của người nhận không.
