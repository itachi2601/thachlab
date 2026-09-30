---
name: project-thachlab-ta-policy
description: "Quy chế trợ giảng Phần A từ 01/10/2026 — chấm điểm tháng, hệ số lương, chốt tháng; code xong chưa commit, chưa chạy migration, chưa test"
metadata:
  node_type: memory
  type: project
  originSessionId: 6093eceb-f6fb-4d0d-b57e-05c21ebebc94
  modified: 2026-09-26T02:32:59.400Z
---

Mảng **quy chế trợ giảng Phần A**, áp dụng từ **01/10/2026**. Toàn bộ code đang nằm ở
working tree, **chưa commit** (tính đến 2026-09-14).

## Quy tắc nghiệp vụ đã chốt

Điểm tháng thang 100: tiếp xúc 30 · phụ đạo 25 · kiểm tra BTVN 20 · chuyên cần 15 ·
thầy quan sát 10. Đạt ≥ 70 thì hệ số lên lớp ×1,0; dưới 70 ×0,9. **Riêng tháng 10/2026
luôn ×1,0** (tháng chạy thử — chấm và công bố điểm nhưng chưa giảm lương).

- Tiếp xúc: mục tiêu 12 lượt/buổi, tính tỷ lệ **từng buổi** rồi lấy trung bình (cố ý —
  để một buổi 24 lượt không bù cho buổi 0 lượt; có test riêng).
- Phụ đạo 1–2 em ×1,2; 3–4 em ×1,4; tối đa 4 em/buổi. Không nhân chồng hệ số lên lớp.
- Chữa bài thay thầy: phút đứng bảng /60 × đơn giá × 1,6; phần giờ còn lại tính lên lớp.
- Chấm kiểm tra ngoài giờ 1.500 đ/bài.
- **Từ 01/10/2026 không còn ghi công hành chính** (`session_type='hanhchinh'` bị chặn ở
  cả DB lẫn form).
- Lịch sử trước 10/2026 **không đụng tới**: `ta_monthly_score`/`ta_converted_hours` cũ giữ
  nguyên. UI tự chuyển: tháng `>= "2026-10"` dùng nhánh mới, cũ hơn dùng `LegacyDashboard`.

Chốt tháng: chỉ admin, phải đủ điểm + đơn giá + không còn buổi chờ duyệt. Chốt xong lưu
`snapshot`. Admin sửa công của tháng đã chốt → tháng **tự mở lại**, bản chốt cũ vào
`ta_policy_audit`. Trợ giảng không sửa được tháng đã chốt.

## Code đã viết

- `docs/supabase-migration-ta-policy-oct2026.sql` (200 dòng) — `ta_sessions.policy jsonb`,
  bảng `ta_month_reviews` + `ta_policy_audit`, trigger `ta_policy_session_guard`, RPC
  `ta_monthly_policy` và `ta_save_month_review`. Idempotent, chạy lại được.
- `lib/tro-giang/policy.ts` — kiểu `SessionPolicy`/`MonthPolicy`, gọi 2 RPC trên.
  `policyError()` đổi lỗi `PGRST202/42P01/42703` thành câu "quy chế chưa được kích hoạt"
  → đây là dấu hiệu **migration chưa chạy**.
- `components/tro-giang/Policy*.tsx` (5 file mới) — form phiếu buổi, bảng chấm tháng của
  admin, trang tháng của trợ giảng.
- `app/tro-giang/quy-che/page.tsx` — trang quy chế cho trợ giảng đọc (đã gồm cả Phần B
  "chưa áp dụng": bậc Tập sự/Chính thức/Nòng cốt, để từ khóa sau).
- `app/tro-giang/mau/` + `LocalAssistantPreview.tsx` — **chỉ chạy `NODE_ENV=development`**,
  production `notFound()`. Dùng để xem trước form mà không cần tài khoản thật.
- Sửa: `GhiBuoiForm`, `AdminMonthlyTable`, `AdminSessionQueue`, `TroGiangDashboard`,
  `queries.ts` (thêm `policy` vào `TaSessionRow`/`NewSessionInput`; `fetchPendingSessions`
  đổi sang `select("*")`).

## Trạng thái: đã xong và đã deploy (2026-09-14)

1. Migration `docs/supabase-migration-ta-policy-oct2026.sql` — **đã chạy trên Supabase**.
2. `scripts/tests/ta-policy.mjs` — **12/12 PASS**. Cần `@electric-sql/pglite` (đã thêm vào
   devDependencies), chạy bằng:
   `PGLITE_MODULE="$PWD/node_modules/@electric-sql/pglite/dist/index.js" node scripts/tests/ta-policy.mjs`
3. Đã test tay, commit `f47ff63f`, push `main`, chạy `scripts/deploy.sh` lên nhánh `deploy`.

Nếu sau này giao diện báo "quy chế chưa được kích hoạt" thì là RPC/bảng biến mất chứ không
phải chưa chạy migration — migration đã chạy rồi.

Nhớ [[feedback-thachlab-deploy-scope]]: commit này **không** gồm sửa skill up đề,
`.claude/commands/`, `scratchpad/` hay [[project-thachlab-restore-posts]] — vẫn đang nằm ở
working tree.

**Cập nhật 2026-09-25 (phiên khác, không phải phiên viết mục này):** điểm "phụ đạo 25đ" đổi
công thức — từ 01/10/2026 cần thêm bằng chứng khách quan `tutoring_exit_attempts` đạt ≥80%
cùng ngày ghi buổi, không chỉ tick tay prepared/recalled/asked_each như trước (buổi trước
01/10/2026 không đổi). Đã commit + push (`b85d82a7`), `scripts/tests/ta-policy.mjs` đã thêm
ca kiểm thử cho công thức mới, 13/13 pass. Chi tiết ở [[project_thachlab_tutoring_exit_quiz]].
Chưa test UI thật qua tài khoản trợ giảng/học sinh.
