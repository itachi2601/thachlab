---
name: project-thachlab-admin-redesign
description: "Khu /quan-tri đã đổi sang app shell riêng + bộ class admin-* dùng chung (21/9/2026, đã deploy)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f85454e-83be-4d3f-adbf-4b3c9e28cac0
  modified: 2026-09-21T15:57:44.983Z
---

Ngày 21/09/2026, khu quản trị `/quan-tri` được thiết kế lại và đã deploy (commit `9ffde8f9`).

**Cấu trúc mới**
- `app/quan-tri/layout.tsx` → `components/admin/AdminShell.tsx`: app shell riêng, KHÔNG dùng
  `Navbar`/`Footer` marketing. Sidebar cố định (ngăn kéo trên < 1024px) + thanh trên hiện
  khu vực và tên trang; `ThemeToggle` nằm ở thanh trên.
- `components/admin/nav.ts` giữ toàn bộ danh sách điều hướng (`AREA_ITEMS`, `SHARED_ITEMS`,
  `OVERVIEW_ITEM`, `areaOfPath`, `titleOfPath`). Thêm trang quản trị mới = thêm một mục ở đây,
  tiêu đề thanh trên và thẻ "Việc hay làm" tự có. `AdminSidebar.tsx` cũ đã xoá.
- `/quan-tri` không còn là màn hình chọn khu vực mà là trang Tổng quan: 6 ô số liệu đếm bằng
  `select("*", { count: "exact", head: true })` + lối tắt + 2 thẻ khu vực.
- Ba layout nhóm `(thpt)/(cttc)/(shared)` giờ chỉ còn `RequireAuth`.

**Bộ class dùng chung** nằm cuối `app/globals.css`: `admin-card`, `admin-btn(--primary/ghost/danger)`,
`admin-chip`, `admin-badge`, `admin-h2/h3`, `admin-lead`, `admin-eyebrow`, `admin-table-wrap`,
`admin-empty`, `admin-stat`, `admin-action`. Biến màu theo `data-area` trên `.admin-shell`:
xanh cho THPT, cam cho CTTC — có cả block nhuộm lại các class `text-blue-*/bg-blue-*` viết sẵn
trong trang CTTC, nên không cần sửa tay từng chỗ.

**Lưu ý khi viết trang quản trị mới**
- `input/select/textarea` trong `.admin-shell` đã được chuẩn hoá ở cấp phần tử (viền, bo, nền,
  padding) — không cần lặp lại chuỗi Tailwind; chỉ thêm `w-full` khi thực sự muốn full width.
- Đừng đặt lại tiêu đề trang bên trong component (thanh trên đã hiện rồi), chỉ cần `admin-lead`.
- Turbopack dev hay phục vụ file CSS cũ sau khi sửa `globals.css`; nếu style mới không lên,
  dừng server → `rm -rf .next/dev` → chạy lại.

**Trạng thái 2026-09-21 cuối phiên:** commit `9ffde8f9` đã có trên `main` VÀ `origin/main`
(phiên khác push kèm commit CNC `d9f09071` của họ). Bản deploy đang chạy là build sạch từ
`d9f09071` (deploy branch `e063aab`) nên production có cả hai. Working tree sạch, chỉ còn
2 file chưa theo dõi của việc khác: `scripts/restore-posts.mjs` + `scripts/data/restore-posts.json`
(xem [[project-thachlab-restore-posts]]).

**Đã kiểm chứng tận nơi** bằng tài khoản admin thật trên dev server: 12 trang quản trị
(Tổng quan, Bài học, Đăng đề, Nhập bài, Ngân hàng câu hỏi, Chủ đề, Lớp học, Học sinh, Bảng điểm,
Nội dung CNC + trang bài CNC, Tình trạng máy, Trợ giảng, Phân công giảng viên, Tin nhắn, Bài đăng),
ngăn kéo mobile, giao diện sáng. `next build` sạch; `eslint` 18 lỗi đúng bằng trước khi sửa.

**Còn treo / chưa làm:**
- Chưa test bằng tài khoản **giảng viên chỉ được phân công 1 khu vực** (`role=instructor` +
  `admin_area`) — nhánh `restrictedArea` trong AdminShell (ẩn Tổng quan, ẩn nhóm Dùng chung,
  ẩn nhóm khu vực kia) mới chỉ đọc code, chưa chạy thật.
- Các component ngoài `components/admin/` vẫn giữ style riêng: `components/tro-giang/*`
  (dùng chung với trang `/tro-giang` của trợ giảng nên cố ý không đụng), `components/exams/*`.
- Mục "Lớp học phần & sinh viên" trong sidebar CTTC vẫn trỏ ra `/dashboard` (trang ngoài khu
  quản trị, giao diện cũ) — đánh dấu `external: true`, chưa gom vào shell.
- Trang bài CNC `/quan-tri/lms-cnc/<id>` hiện tên "Nội dung học phần CNC" ở thanh trên (khớp
  prefix dài nhất trong `titleOfPath`), chưa hiện tên bài.
- Nút nổi "Xem như học sinh / trợ giảng" (render ở root layout) được đẩy sang phải 268px bằng
  CSS `body:has(.admin-shell)` để không đè sidebar; ở light theme chúng vẫn nền tối (lỗi có từ trước).

Liên quan: [[project-thachlab-lesson-ui-redesign]], [[project-thachlab-concurrent-sessions]]
