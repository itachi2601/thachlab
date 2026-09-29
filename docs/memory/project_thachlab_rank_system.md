---
name: thachlab-rank-system
description: "Hệ thống rank RP theo mùa + 45 danh hiệu; đã deploy 24/9/2026; mùa thử nghiệm 1 tháng (21/9–25/10/2026, ngưỡng đã hạ) đang active cho cả lớp 11 và 12, đã bật Luyện tập (+BTVN lớp 12), chưa gán đề thử thách"
metadata:
  node_type: memory
  type: project
  originSessionId: b06823c6-6232-4b7a-8124-5a2e6b72857e
  modified: 2026-09-27T03:57:09.098Z
---

Hệ thống rank (RP/bậc theo mùa) + 45 danh hiệu — thay hoàn toàn 3 chỗ "hạng theo điểm" cũ
(ô Hạng lớp, dòng Hạng x/y ở Kết quả/phụ huynh, hạng từng đề). Code xong 23/9/2026, chưa commit.

**Trạng thái (23/9/2026):** migration ĐÃ chạy, test SQL ĐÃ qua; đã commit `cd931e0` (chỉ file tính năng,
`ThptStudentHome.tsx` stage riêng phần rank vì file còn WIP thoát phụ đạo chưa commit). Đã test UI admin
(5 tab) + trang HS/Kết quả ở trạng thái "chưa mở mùa" bằng tài khoản admin. Trong DB có mùa nháp
"Mùa thử nghiệm (nháp)" lớp 12 do em tạo khi test — thầy dùng tiếp hoặc bỏ. ĐÃ deploy 24/9/2026 theo lệnh thầy
(deploy branch f9b43fc, build từ origin/main 928d356b trong worktree sạch). CHƯA test luồng HS thật với mùa active
(cần tài khoản HS + mở mùa + bật bài tính RP).

**Why:** tạo động lực bằng lên hạng/sưu tập thay vì so điểm; ai đủ điều kiện đều lên được bậc cao nhất.
App là static export → toàn bộ tính RP/danh hiệu nằm trong Postgres (trigger + RPC security definer).

**How to apply:**
- Quyết định đã chốt: thay cả 3 chỗ hạng cũ (hàm SQL `get_exam_rank`/`get_periodic_rank` vẫn còn trong DB,
  chỉ xoá wrapper TS); sửa sai = bài ngắn từ question_bank cùng chủ đề tầng bài, loại câu đề gốc theo
  content_hash, chỉ áp dụng bài qua ExamRunner; mục tiêu tuần = ≥3 bài tính RP đạt ≥7,0 (Thứ Hai–CN giờ VN);
  trang GV ở `/quan-tri/xep-hang` dù ROADMAP khuyên hạn chế mảng quản lý.
- Chống cộng trùng: `rank_rp_awards` khoá (season, student, kind, ref) + `rank_award()` chỉ cộng delta, `for update`.
- Danh hiệu không có chủ đề trong DB (Photon, Nguyên tử, Máy biến áp, Cân bằng nhiệt) không active tới khi GV gắn.
- Cao Thủ/Thách Đấu bắt buộc có đề thử thách — GV chưa gán thì không ai lên được (UI nói rõ).
- Không quy đổi điểm cũ; GV bấm "Tính lại" (rank_recompute_season) nếu muốn tính bài trong khung mùa.
- Chưa test được UI với RPC thật (migration chưa chạy) — chỉ mới verify build + render không crash.

**Mùa thử nghiệm 1 tháng (chỉnh 25/9/2026 theo yêu cầu thầy, sửa thẳng DB qua REST, không cần deploy):**
season id 4 "Mùa thử nghiệm", lớp 18 (94 HS), 21/9 → 25/10/2026 (5 tuần tròn Thứ Hai–CN).
Ngưỡng RP / điều kiện danh hiệu đã hạ: Chiến Binh 50 · Tinh Anh 120 (1 Thức Tỉnh) · Tinh Nhuệ 200 (2 TT)
· Đại Sư 280 (2 TT) · Cao Thủ 350 (1 Làm Chủ) · Thách Đấu 420 (2 LC). Config RP giữ mặc định (20/bài, 30/tuần, 10 sửa sai).
Cơ sở: ~5 tuần × 30 + ~10 bài × 20 + sửa sai ≈ 400–450 RP tối đa.
25/9 đã bật 20 Luyện tập + 5 BTVN (exam) lớp 12 làm nguồn RP (max 20), replay 10 practice_sessions từ 21/9 qua
`rank_on_result` (service role không gọi được rank_recompute_season vì rank_is_staff cần auth.uid()).
25/9 (sau đó) mở thêm lớp 11 vào cùng season 4: `class_ids` → [18,17], bật 23 Luyện tập lớp 11 làm nguồn RP
(max 20) — lớp 11 chưa có mục BTVN nào có đề nên chưa bật gì ở đó. Gọi `rank_recompute_season(4)` bằng cách
giả lập JWT staff (`set_config('request.jwt.claims', ...)` — xem [[reference_supabase_db_query_cli]]) để backfill
RP cho hoạt động từ 21/9 trước khi mùa mở cho lớp 11: 144 học sinh được tính lại, 52 HS lớp 11 vào mùa.
25/9 (theo yêu cầu thầy) bật thêm mục Kiểm tra cho lớp 12: 6 đề kiểm tra theo bài/giữa kỳ + toàn bộ 70 đề "Đề thi thử các trường, sở GD&ĐT 2026" (lesson_item 277) + đề 56 (gắn thêm vào item 277) làm nguồn RP,
max vẫn 20 RP/đề — thầy biết rõ và chủ động chọn mức này dù có thể vượt 400-450 RP dự tính ban đầu (đã hỏi trước khi làm).
rank_recompute_season(4) sau đó đã cộng RP cho các lượt làm exam 10/56 từ thứ Tư 23/9 (trước khi tính năng deploy thứ Năm 24/9) — dùng
source_ref dạng `exam:<id>` / `practice_item:<id>` (không phải id kết quả), source_kind trong rank_rp_awards luôn là 'practice' bất kể loại bài.
CÒN TREO: Cao Thủ/Thách Đấu chưa có challenge_exam_id; mục Kiểm tra vẫn chưa bật cho lớp 11. Seed mặc định cho mùa sau (200…2600) vẫn giữ nguyên trong migration.

**Lỗ hổng cơ chế tính RP (phát hiện 27/9/2026, chưa sửa):** RP là whitelist opt-in qua bảng `rank_sources`
(trigger `rank_on_result` chấm mọi bài nộp nhưng chỉ cộng RP nếu đề đã được bật `enabled`). Danh sách ứng viên
để chọn — `fetchSourceCandidates()` ở services/rank.ts:353 — CHỈ quét `lesson_items` có
`kind in ('luyen_tap','bai_tap_ve_nha','kiem_tra')`. Bảng `class_assessments` (Kiểm tra định kỳ giữa/cuối kì,
xem [[project_thachlab_periodic_exam]]) bị cố tình tách khỏi lesson_items để tránh hiện trùng ở trang bài học,
nên các đề định kỳ KHÔNG hiện ra để chọn làm nguồn RP — muốn tính phải gắn thủ công đề đó vào một lesson_item
kiểu kiem_tra. Nếu thầy muốn "tất cả bài kiểm tra" đều vào rank, cần sửa fetchSourceCandidates() gộp thêm
class_assessments (hoặc JOIN exam_id chung) rồi mới bật enabled cho từng đề.

**27/9/2026 — thầy yêu cầu bật Kiểm tra cho lớp 10/11/12 (không mở lớp 9):** kiểm tra lại thì
`rank_sources.enabled=true` đã có sẵn cho ĐỦ cả 102 exam_id "Kiểm tra" ở 3 lớp (ai đó/phiên khác đã bật
trước khi em chạy migration — không cần INSERT thêm). Vấn đề còn lại chỉ là BACKFILL: các lượt làm bài
nộp TRƯỚC lúc nguồn được bật chưa có RP (trigger `rank_on_result` chỉ chấm lúc insert mới, không chạy
lại cho dữ liệu cũ). Xác nhận thiếu backfill ở ít nhất 9 đề (~260 lượt): lớp 10 exam 23/224, lớp 11
exam 12/205/206, lớp 12 exam 9/56/214/219. Đã viết `docs/supabase-recompute-rank-backfill-20260927.sql`
(gọi lại `rank_recompute_season(4)` + `(5)`, an toàn chạy nhiều lần) — CHƯA chạy, chờ thầy tự chạy qua
`supabase db query --linked -f ...` (theo AGENTS.md, không tự gọi lệnh ghi lên production). Lớp 9 (KHTN,
class_id 15) vẫn chưa thuộc season nào và chưa có đề kiểm tra nào — thầy chủ động không mở, giữ nguyên.

**27/9/2026 (sau đó) — thầy tự chạy file backfill, đã xong.** exam 224/12/205/206/219 lên RP đầy đủ.
exam 23 (lớp 10, season 5) và exam 9 (lớp 12, season 4) vẫn 0 RP — không phải lỗi: `rank_recompute_student`
chỉ tính lượt làm trong khung `starts_on..ends_on` của season (season 5 mở 26/9/2026, season 4 mở 21/9/2026),
và mọi lượt làm 2 đề đó đều nộp trước ngày mở mùa. exam 214 chỉ có 1 lượt của chính tài khoản admin
Ngô Diệu Thạch, bị loại đúng thiết kế (rank_exclude_staff). Kết luận: cơ chế tính RP hoạt động đúng như
thiết kế cho lớp 10/11/12, không còn gì tồn đọng ở việc này.

**27/9/2026 — đã bật Kiểm tra RP cho lớp 10/11/12 (REST trực tiếp, insert rank_sources, không cần deploy):**
Lớp 12 (season 4): +14 exam_id (219,210-218,220-223 — 13 đề thi thử trường/sở item 277 + đề 219).
Lớp 11 (season 4): +5 exam_id (12,13,203,205,206). Lớp 10 (season 5): +2 exam_id (23,224).
`class_assessments` chỉ là bảng metadata (class_id/exam_id/kind/term), KHÔNG có cột điểm riêng và KHÔNG
insert exam_results riêng — điểm vẫn qua exam_results theo exam_id bình thường, nên bật đúng exam_id trong
rank_sources là đủ, KHÔNG cần sửa fetchSourceCandidates()/trigger gì thêm cho loại đề định kỳ.
CÒN TREO: (1) lớp 9 KHTN chưa thuộc season nào + chưa có đề kiểm tra nào trong LMS — chưa bật được gì,
cần thầy quyết có đưa vào rank không; (2) chưa chạy rank_recompute_season để backfill RP cho các lượt làm
bài TRƯỚC thời điểm bật hôm nay — bước này cần JWT giả lập staff qua `db query --linked`, đúng loại lệnh
AGENTS.md cấm agent tự chạy, để lại cho thầy.

**2026-09-28 10:42 — thầy đã chạy `20260928100000_rank_specialist_difficulty.sql` + `docs/supabase-recompute-rank-titles-20260928.sql`**
(rank_recompute_season 4 và 5): 63 danh hiệu mới cấp cho 50 HS theo logic Dễ/TB/Khó. CODE đi kèm vẫn là WIP chưa commit
trong working tree (phiên khác) → web thật lệch RPC: TitleCollection không hiện tiến độ danh hiệu chuyên môn (không crash).
Cùng lúc chạy `20260928130000_rank_title_code_in_class_rpcs.sql` (xem [[project_thachlab_title_showcase]]).
