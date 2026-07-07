# ThachLab — Tổng kết & Lộ trình phát triển

> Nền tảng học Vật lý THPT của thầy Thạch — *"Vật lý không chỉ là công thức"*.
> Next.js 16 (xuất tĩnh `output: export`) deploy lên shared hosting LiteSpeed
> `thachlab.id.vn`; dữ liệu động qua Supabase (client-side + anon key + RLS).

---

## Phần 1 — Các task đã hoàn thành

### 1. Nền tảng & thiết kế
- Khởi tạo dự án với **Next.js 16 + React 19 + Tailwind v4 + TypeScript**.
- Kiến trúc thư mục: `app/` (route), `components/`, `features/`, `services/`, `lib/`.
- **Design system dark neon** hướng tới Gen-Z; thương hiệu cá nhân xuyên suốt site.
- Cấu hình xuất tĩnh cho hosting LiteSpeed (`trailingSlash: true` để tránh lỗi 403).

### 2. Trang chủ (landing page)
- **Hero mô phỏng vật lý tương tác**: `SpringSimulation`, `DisplacementChart`,
  `ControlPanel`, `FormulaPanel` (dao động điều hòa trực quan).
- Các section: `PhysicsEverywhere`, `LearningPath`, `Features`, `AboutFounder`,
  `Testimonials` (tin nhắn thật + thư viết tay của học sinh).
- Thư viện vật lý `lib/Physics/`: điện trường, dao động điều hòa, từ trường,
  con lắc, chuyển động ném, sóng.

### 3. LMS trên nền Supabase
- **Xác thực**: đăng ký / đăng nhập học sinh (`/dang-ky`, `/dang-nhap`),
  hướng dẫn xác nhận email sau đăng ký; `AuthProvider` + `RequireAuth`.
- **Tài khoản học sinh** (`/tai-khoan`).
- **Trang quản trị** (`/quan-tri`) với các tab: Bài học, Đề thi, Import Word,
  Lớp học, Kết quả, Bài viết, Tin nhắn.
- **Thi trực tuyến 3 dạng câu hỏi** theo cấu trúc đề 2025 (GDPT 2018):
  trắc nghiệm, đúng/sai (4 ý), trả lời ngắn — qua `ExamRunner` + `QuestionCard`.
- **Lớp học many-to-many**, bộ lọc theo lớp, **import đề từ file Word** (`mammoth`).
- **Chương trình học Chương → Bài học** (6 mục theo mỗi bài).
- **Tin tức / bài viết** (`/tin-tuc`) và **tin nhắn** (`/tin-nhan`).

### 4. SEO & Content marketing
- **Blog tĩnh chuẩn SEO** (`/blog`) dựng từ Markdown (`gray-matter` + `marked`).
- Bài viết đầu tiên: *Lộ trình học Vật lý THPT theo chương trình mới 2018*.
- Metadata đầy đủ: OpenGraph, Twitter card, JSON-LD (`EducationalOrganization`),
  `robots`, `canonical`.
- Xác minh **Google Search Console** (thẻ HTML).

---

## Phần 2 — Dự định phát triển tiếp theo

### Ưu tiên gần (quick wins)
- [ ] **Hoàn thiện tài liệu** đang rỗng: `BRAND.md`, `DATABASE.md`, `MANIFESTO.md`,
      `PROJECT.md`, `UI.md`.
- [ ] **Render công thức bằng KaTeX** (đã cài `katex`) thay cho ảnh `<img class="eq">`.
- [ ] **`sitemap.xml` + RSS** cho blog để tăng phủ SEO.
- [ ] Thêm bài blog theo từng chương → xây "cluster" nội dung.

### Trải nghiệm học tập
- [ ] **Dashboard kết quả cho học sinh**: lịch sử làm bài, điểm theo chủ đề,
      biểu đồ tiến bộ (mở rộng từ `ResultsAdmin`).
- [ ] **Đề ngẫu nhiên / trộn câu** và ngân hàng đề lớn hơn.
- [ ] **Mô phỏng tương tác cho các chương khác** — tận dụng engine sẵn có
      (điện trường, từ trường, sóng, con lắc, ném xiên) làm bài giảng trực quan.
- [ ] **Video bài giảng** nhúng vào bài học / bài viết.

### Tương tác & giữ chân
- [ ] **Gamification**: huy hiệu, streak, bảng xếp hạng lớp.
- [ ] **Nhắc lịch học / thông báo** đề mới, hạn nộp.
- [ ] Kênh **hỏi đáp / bình luận** dưới mỗi bài học.

### Kỹ thuật & vận hành
- [ ] **PWA** cho trải nghiệm mobile (cài về máy, offline nhẹ).
- [ ] Rà soát **RLS Supabase** & phân quyền admin/học sinh chặt chẽ.
- [ ] **Kiểm thử tự động** (unit + e2e) cho luồng thi và import đề.
- [ ] CI/CD build tĩnh → tự động deploy lên hosting.
