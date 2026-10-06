# Prompt — trang chủ nói chuyện được với PHỤ HUYNH (6 việc)

Ngày: 02/10/2026. Dán phần dưới dấu `---` cho agent (DeepSeek / Claude Code) chạy trong repo.
Căn cứ: nhận xét 02/10 — trang chủ hiện tại chỉ nói với "em", phụ huynh tìm chỗ học cho con không thấy
thầy là ai, kết quả ra sao, học phí, cách liên hệ, cách theo dõi con.

**Thầy điền trước khi giao (agent không được bịa):**

| Khoá | Giá trị | Dùng ở |
|---|---|---|
| `PHONE` | `0909 xxx xxx` | dải phụ huynh, footer |
| `ZALO_URL` | `https://zalo.me/…` | dải phụ huynh, footer, trang phụ huynh |
| `TEACHER_PHOTO` | `public/images/thay-thach.webp` (ảnh thật, ≤ 150 KB, rộng ≤ 800px) | khối Người đứng lớp |
| `YEARS` | số năm dạy | khối Người đứng lớp |
| `SCHOOL` | trường đang công tác | khối Người đứng lớp |
| `AREA` | khu vực dạy (quận/tỉnh) | footer |
| `PARENT_SHOTS` | 2–3 ảnh chụp màn hình bảng kết quả thật (đã che tên học sinh), `.webp` ≤ 150 KB | trang phụ huynh |

Giá trị nào thầy chưa điền thì agent **bỏ trống phần tử đó** (không render), không ghi "0909 123 456".

---

Bạn là kỹ sư front-end trong repo Next.js `thachlab`. Đọc `AGENTS.md` trước (đặc biệt mục tối ưu tốc độ và
đồng bộ phiên) và tra `node_modules/next/dist/docs/` khi cần API. Mục tiêu: trang chủ và trang phụ huynh
trả lời được 6 câu phụ huynh Việt hỏi khi tìm chỗ học cho con. **Không đổi theme, không đổi bố cục tổng,
không thêm request Supabase lúc tải trang.**

## Hệ thị giác — giữ nguyên ThachLab
- Dùng token trong `app/globals.css` (`--color-primary`, `--color-accent`, `--color-panel`, `--color-ink`,
  `--color-muted`, `--color-line`), font `--font-display`/`--font-body`. Đẹp ở cả `data-theme="dark"` và `"light"`.
- Kiểu khối theo `components/home/OpenClasses.tsx` và `Features.tsx` đang có. Không eyebrow mono IN HOA mới,
  không gradient text, không glow.
- Giọng với phụ huynh: xưng **"thầy" – gọi "anh chị"**; giọng với học sinh giữ "em" như cũ. Không trộn trong
  cùng một khối.

## Việc 1 — Dải "Dành cho phụ huynh" (component mới `components/home/ForParents.tsx`)
Đặt trong `app/(public)/page.tsx` **ngay sau `OpenClasses`**, trước hero mô phỏng. Một khối ngang, 3 cột
(mobile 1 cột), mỗi cột một câu ngắn + 1 dòng giải thích:
1. **Con học gì** — "Lý thuyết, bài tập, đề kiểm tra theo đúng chương trình 2018, bám nhịp lớp trên trường."
2. **Thầy theo dõi ra sao** — "Mỗi bài làm được chấm ngay; câu sai gắn với chủ đề, thầy biết em yếu chỗ nào để phụ đạo."
3. **Anh chị xem kết quả ở đâu** — "Tài khoản phụ huynh xem điểm, bài đã làm, chủ đề còn sai." → link `/phu-huynh`.
Bên phải/dưới: dòng **"Học miễn phí trên web"** + nút `Nhắn Zalo cho thầy` (`ZALO_URL`, `target=_blank rel=noopener`)
+ nút `Gọi PHONE` (`tel:`). Thiếu `PHONE`/`ZALO_URL` thì ẩn nút tương ứng.

## Việc 2 — Khối "Người đứng lớp" (`components/home/AboutFounder.tsx`)
Sắp lại theo thứ tự phụ huynh cần, giữ nguyên style khối:
1. Ảnh thật `TEACHER_PHOTO` (`next/image`, `.webp`, `sizes` đúng, `loading="lazy"`), bên trái trên desktop,
   trên cùng ở mobile. Không có ảnh → giữ bố cục chữ hiện tại.
2. Tên + dòng "`YEARS` năm dạy Vật lý · `SCHOOL`" + "Dạy KHTN 9 và Vật lý 10–12 theo chương trình 2018, CNC – tiện – phay (CTTC)".
3. Câu nói "Hiểu bản chất, không học thuộc công thức."
4. Sở thích (gym, trượt băng, cơ khí) xuống **cuối**, 1 dòng, giữ vì là chất riêng.
5. Giữ 3 link mạng xã hội và dòng "3.300+ người theo dõi".
Tuyệt đối **không bịa** bằng cấp, giải thưởng, thành tích.

## Việc 3 — Khối "Kết quả có số" — chỉ số thật
Mở rộng `scripts/build-content.mjs` → `public/data/home-stats.json` (đọc qua `components/home/home-stats.server.ts`,
số được tính **lúc build**, không gọi Supabase khi tải trang). Thêm vào `totals`:
- `students`: số học sinh có tài khoản (bảng profile, role học sinh — tra `docs/DATABASE.md` để lấy đúng tên bảng/cột).
- `attempts`: số lượt làm đề đã chấm.
- `questions`: số câu trong ngân hàng câu hỏi.
Hiện trong dải tổng của `OpenClasses` (đang có 4 lớp · 22 chương · 116 bài · 257 mục) thêm
"`students` học sinh · `attempts` lượt làm đề đã chấm". Số < 50 thì **không hiện** số đó (tránh phản tác dụng).
Không hiện "điểm trung bình tăng" vì chưa có dữ liệu đối chứng.

## Việc 4 — Hero (`components/home/PhysicsSimulationHero.tsx`)
Dòng phụ hiện là "Hoàn toàn miễn phí. Thử kéo thanh Biên độ…". Tách thành 2 ý rõ: dòng 1 **"Học miễn phí trên web,
theo đúng nhịp lớp trên trường."**; dòng 2 mới là hướng dẫn kéo mô phỏng. Không đổi gì khác ở hero.

## Việc 5 — Trang phụ huynh (`app/phu-huynh/page.tsx`, `components/auth/RequireAuth.tsx` prop `guestNotice`)
Với khách chưa đăng nhập, `guestNotice` hiện:
1. Tiêu đề "Anh chị sẽ thấy gì" + 3 gạch đầu dòng: điểm theo thời gian · bài đã làm và câu sai theo chủ đề ·
   phần con đang được phụ đạo.
2. Lưới 2–3 ảnh `PARENT_SHOTS` (`next/image`, lazy). Không có ảnh → bỏ lưới.
3. Hai nút: `Đăng nhập` (như cũ) và **`Chưa có link mời? Nhắn Zalo cho thầy`** (`ZALO_URL`).
4. Giữ câu hướng dẫn link mời `/loi-moi?ma=PH…`.
Đưa link "Phụ huynh" **trở lại Navbar** cho khách và học sinh (hiện chỉ ở Footer và menu tài khoản
`Navbar.tsx:132`): một mục "Phụ huynh" sau "Tin tức" trong `links`, và một chip trong menu mobile.

## Việc 6 — Footer (`components/layout/Footer.tsx`)
Thêm cột "Liên hệ": `PHONE` (`tel:`), Zalo (`ZALO_URL`), `AREA`, email nếu có sẵn trong repo. Bỏ dòng tiếng Anh
"Living between equation and motion", thay bằng "Thầy Thạch · Vật lý THPT – KHTN 9 · `AREA`". Giữ các cột còn lại.

## Cấu hình liên hệ dùng chung
Tạo `lib/contact.ts` xuất `CONTACT = { phone, zalo, area, teacherPhoto, years, school }` đọc từ hằng (không phải
env, vì dùng ở client). Mọi chỗ ở trên import từ đây — không rải số điện thoại trong 4 file.

## Ràng buộc
- 0 request mới lúc tải `/` và `/phu-huynh`. Số liệu chỉ qua `home-stats.json` lúc build.
- Ảnh mới `.webp` ≤ 150 KB, chạy `node scripts/optimize-images.mjs` nếu đặt trong `public/`.
- Không đụng: trang bài học, `MobileTabBar`, `HonorBoard`, schema, migration, `docs/STATE.md` (chỉ **thêm** 1 dòng
  mục đang chờ), `docs/memory/MEMORY.md` (chỉ thêm dòng).
- Không thêm thư viện. Không format lại file ngoài phạm vi.
- Nhánh mới từ `main`: `feat/trang-chu-phu-huynh`; mỗi việc 1 commit `feat(home): …`; PR vào `main`,
  không push thẳng `main`.

## Kiểm trước khi báo xong — đính bằng chứng vào PR
- `npm run lint`, `npm run build` sạch; `node scripts/build-content.mjs` sinh `home-stats.json` có 3 trường mới.
- Ảnh chụp `/` và `/phu-huynh` ở **375px và 1280px, dark + light**, khách chưa đăng nhập.
- DevTools Network: số request `*.supabase.co` khi tải `/` **bằng** trước khi sửa (ghi 2 số).
- Lighthouse Mobile trang chủ trước/sau (ghi 2 số; đợt 9/2026 đang 91 desktop).
- Mục **"Cần thầy quyết"** trong PR: giá trị nào trong bảng khoá còn trống, số nào bị ẩn vì < 50, chỗ nào phải
  tự chọn câu chữ.

Nếu một yêu cầu mâu thuẫn với code thực tế, ưu tiên giữ chức năng đang chạy, làm phần còn lại và ghi rõ trong PR.
Không báo "xong" khi còn bước kiểm chưa làm.
