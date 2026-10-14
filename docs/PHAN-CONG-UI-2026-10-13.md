# Phân công sửa giao diện ThachLab — 13/10/2026

Nguồn: bản nhận xét giao diện 13/10/2026 (ảnh chụp 375px/1280px trang chủ, `/lop-hoc`, Lớp 10, bài học, `/phu-huynh`, đăng nhập).
Nguyên tắc chia việc theo `AGENTS.md` mục "Phân công mô hình":
- **Cursor (Auto)**: code thường, không đụng schema/RLS, có file + tiêu chí nghiệm thu rõ.
- **Gemini (gemini.google.com)**: phác thảo tài sản hình (SVG), không cần mã nguồn, không dữ liệu học sinh.
- **Claude**: việc cần phán đoán thiết kế theo `docs/QUY-TAC-THIET-KE.md`, việc có tên/điểm học sinh, và **soát mọi thứ Cursor/Gemini trả về** (`kiem-code`) trước khi merge.

Thứ tự khuyên làm: Cursor C1→C4 (độc lập, chạy song song với Gemini G1–G2) → Claude K1–K5 → Claude K6 gộp và soát.

| Mã | Việc | Ai làm | Nộp lại gì |
|---|---|---|---|
| C1 | Khối "Thông báo và học liệu" lộ HTML thô + vỡ một chữ một dòng ở 375px | Cursor | commit trên nhánh `cursor/ui-c1` |
| C2 | Thống nhất bán kính góc toàn site (3 mức) | Cursor | nhánh `cursor/ui-c2` |
| C3 | Trang bài học trên điện thoại: ẩn thanh tab chung + nút Báo lỗi khi đang trong bài | Cursor | nhánh `cursor/ui-c3` |
| C4 | Dời dải "Vật lý quanh ta" từ trên hero xuống dưới hero | Cursor | nhánh `cursor/ui-c4` |
| G1 | 4 hình bìa phẳng (KHTN 9, Vật lý 10/11/12) dạng SVG thay bìa AI neon | Gemini | 4 file `.svg` → thầy lưu `assets/bia-gemini/` |
| G2 | Huy hiệu Hạng 1/2/3 dạng SVG sắc nét | Gemini | 3 file `.svg` → `assets/huy-hieu-gemini/` |
| K1 | Rút trang chủ từ 12 khối xuống 5–6, có tư vấn theo quy tắc B2/N2 | Claude | |
| K2 | Poster điểm TNTHPT ở `/phu-huynh` → bảng HTML; gỡ mâu thuẫn "không công khai điểm" | Claude (có tên HS) | |
| K3 | "Lời nhắn từ học trò" → 2–3 trích dẫn + 1 ảnh gốc | Claude (lời HS) | |
| K4 | Nhãn chữ trong hình SVG bài học: ≥13px, màu ink/primary (quét DB, script) | Claude | |
| K5 | Hộp mục tiêu / dự đoán / nút TIẾP cùng tông xanh lơ → chọn lại tông | Claude | |
| K6 | Soát C1–C4, tối ưu + gắn G1–G2 vào `components/home/LearningPath.tsx`, `HonorBoard.tsx`; chụp 375/1440; commit | Claude | |

---

## A. Prompt cho Cursor (chế độ Auto) — mỗi việc một phiên chat mới

Dán nguyên khối, đổi tên nhánh nếu cần. Không gộp hai việc vào một nhánh để Claude soát từng cái.

### C1 — Khối "Thông báo và học liệu" ở trang lớp

```
Bạn đang sửa repo thachlab (Next.js 16, Tailwind v4, static export). Chỉ sửa đúng hai file nêu dưới, không đổi file khác, không đụng supabase/.

Lỗi 1 (desktop): trang /lop-hoc/lop-10, khối "Thông báo và học liệu" hiện mã HTML thô kiểu
`<p><strong>Điều gì mới:</strong> Ngày 6/10/2026…`. Nguyên nhân: app/lop-hoc/page.tsx khoảng dòng 777 đổ thẳng `p.body` (HTML) vào `<small className="line-clamp-1">`.
Sửa: viết hàm thuần `stripHtmlToText(html: string, max = 160): string` (xoá thẻ, gộp khoảng trắng, giải mã &amp; &nbsp; &lt; &gt; &quot;, cắt tới max ký tự + "…") đặt trong lib/ (tạo lib/strip-html.ts nếu chưa có hàm tương tự — grep "stripHtml" trước, có rồi thì dùng lại). Dùng hàm đó ở dòng 777. Không dùng dangerouslySetInnerHTML.

Lỗi 2 (375px): cùng khối đó, mỗi chữ của tiêu đề rơi xuống một dòng (chiều rộng cột về 0). Khối dùng class .class-lessons--flat / .class-lesson / .class-lesson-title trong components/lessons/class-overview.css. Tìm nguyên nhân (thường là grid/flex con không có min-width: 0, hoặc width cố định của cột bên), sửa tối thiểu bằng CSS trong file đó. Không thêm width cứng.

Nghiệm thu, làm rồi ghi kết quả vào mô tả commit:
- `npm run lint` sạch.
- Chạy `npm run dev` rồi `node scripts/do-bo-cuc.mjs http://localhost:3000/lop-hoc/lop-10/ --rong=375 --cao=812 --anh=/tmp/c1-375.png --toan-trang` (script dùng Chrome trên Mac): scrollWidth phải = 375, tiêu đề thông báo nằm trên 1–2 dòng, không còn ký tự "<p>" trong ảnh.
- Commit lên nhánh cursor/ui-c1 với message tiếng Việt, chỉ `git add` hai file đã sửa (+ lib/strip-html.ts nếu tạo). Không git add . / commit -a.
```

### C2 — Thống nhất bán kính góc

```
Repo thachlab (Next.js 16, Tailwind v4). Mục tiêu: toàn site chỉ còn 3 mức bo góc. Hiện navbar dùng pill, nút hero 8px, form đăng nhập rounded-full, nút đổi theme hình vuông bo, thẻ bài học 12–16px.

Bước 1: trong app/globals.css, khối `@theme` (đầu file), thêm 3 token:
  --radius-sm: 0.5rem;   /* chip, ô nhập nhỏ, nút trong bảng */
  --radius-md: 0.875rem; /* nút chính, thẻ, ô nhập chính */
  --radius-pill: 9999px; /* chỉ cho chip trạng thái và avatar */
(Tailwind v4 tự sinh utility rounded-sm / rounded-md / rounded-pill từ token này. Kiểm tra bằng grep xem tên có đụng utility sẵn có không; nếu đụng thì đặt --radius-ui-sm/-md/-pill.)

Bước 2: áp dụng ở đúng các file sau, KHÔNG quét toàn repo:
- components/layout/Navbar.tsx: nút Đăng nhập/Đăng ký và nút ThemeToggle cùng một mức (md). Dropdown giữ md.
- components/layout/ThemeToggle.tsx: cùng mức md, cùng chiều cao với nút Đăng nhập.
- components/home/PhysicsSimulationHero.tsx: hai nút "Vào lớp học", "Xem lộ trình" → md.
- components/auth/ (form đăng nhập, đăng ký, quên mật khẩu): ô nhập và nút → md (bỏ rounded-full).
- components/layout/MobileTabBar.tsx: giữ nguyên.
Không đổi thẻ bài học, hộp trong bài (đã là 12–16px ≈ md, chỉ thay class rounded-xl/2xl → rounded-md nếu cùng file đang sửa).

Nghiệm thu: `npm run lint`; chụp http://localhost:3000/ và /dang-nhap ở 1280 và 375 bằng `node scripts/do-bo-cuc.mjs <url> --rong=375 --cao=812 --anh=/tmp/c2.png`; nút trong navbar và hero phải cùng kiểu bo. Commit nhánh cursor/ui-c2, chỉ add các file đã sửa, ghi "mã quy tắc: B3 (nhất quán hình khối)" trong mô tả commit.
```

### C3 — Trang bài học trên điện thoại: bớt thanh cố định

```
Repo thachlab. Ở /lop-hoc/bai/?id=… trên màn 375px hiện có 3 lớp cố định dưới đáy: (1) thanh tab chung components/layout/MobileTabBar.tsx (render ở app/layout.tsx dòng ~139), (2) thanh công cụ của bài "Mục lục / Học xong / Bài sau" trong components/lessons/LessonPresenter.tsx, (3) nút nổi "Báo lỗi / Góp ý" components/BugReportWidget.tsx. Cộng lại ~130px, nội dung chỉ còn nửa màn.

Yêu cầu:
1. Khi đường dẫn bắt đầu bằng /lop-hoc/bai và /kiem-tra/lam: MobileTabBar KHÔNG render (dùng usePathname trong chính MobileTabBar, trả về null; không sửa app/layout.tsx). Giữ nguyên ở mọi trang khác.
2. BugReportWidget ở hai đường dẫn trên: thu thành nút nhỏ 40px chỉ có icon, đặt phía trên thanh công cụ của bài (bottom = chiều cao thanh công cụ + 12px), không che nút "Bài sau". Ở trang khác giữ nguyên.
3. Thanh công cụ của bài trong LessonPresenter: không đổi bố cục, chỉ kiểm padding-bottom của vùng nội dung để dòng cuối không bị thanh che (env(safe-area-inset-bottom) đã có thì giữ).
Không đụng logic học, RP, tiến độ.

Nghiệm thu: `npm run lint`; chụp /lop-hoc/bai/?id=2 ở 375×812 bằng `node scripts/do-bo-cuc.mjs … --anh=/tmp/c3.png` (không --toan-trang): đáy màn chỉ còn một thanh + một nút icon, nút "Bài sau" bấm được (không bị che). Chụp thêm / để chắc MobileTabBar vẫn hiện. Commit nhánh cursor/ui-c3, chỉ add 2–3 file đã sửa, ghi "mã quy tắc: B2 (một điểm nổi bật mỗi màn), D2 (đích chạm)".
```

### C4 — Dời dải "Vật lý quanh ta" xuống dưới hero

```
Repo thachlab. Trang chủ app/(public)/page.tsx: dải 3 thẻ "Vật lý quanh ta" (components/home/PhysicsPostRibbon.tsx) đang nằm TRÊN câu hỏi mở đầu của hero (components/home/PhysicsSimulationHero.tsx nhận prop ribbonPosts), tranh chú ý với H1.

Yêu cầu: hero không render ribbon nữa (bỏ prop ribbonPosts khỏi PhysicsSimulationHero và mọi chỗ dùng nó bên trong; giữ nguyên mô phỏng, H1, hai nút). Render <PhysicsPostRibbon posts={ribbonPosts} /> ngay sau </PhysicsSimulationHero> trong page.tsx, trong một <div className="bg-bg px-6 lg:px-12"><div className="mx-auto max-w-6xl"> giống khối PwaInstallCard ngay dưới. Không đổi nội dung ribbon, không đổi logic xoay bài theo ngày.

Nghiệm thu: `npm run lint`; chụp / ở 375 và 1280 bằng scripts/do-bo-cuc.mjs: màn đầu chỉ còn navbar + H1 + mô phỏng; ribbon xuất hiện sau hero. Commit nhánh cursor/ui-c4, add đúng 2–3 file, ghi "mã quy tắc: B2, F-pattern".
```

---

## B. Prompt cho Gemini (dán vào gemini.google.com, không cần mã nguồn)

Gemini chỉ trả SVG; Claude sẽ tối ưu (svgo), kiểm tương phản và gắn vào code. Không gửi Gemini bất kỳ tên/điểm học sinh nào.

### G1 — Bốn hình bìa phẳng cho lớp

```
Bạn là hoạ sĩ minh hoạ phẳng (flat illustration) cho một website học Vật lý dành cho học sinh 14–19 tuổi, nền sáng, phong cách tĩnh lặng, ít màu. Hãy vẽ 4 hình bìa bằng mã SVG thuần (không raster, không font ngoài, không chữ trong hình), mỗi hình một file, viewBox="0 0 300 400" (tỉ lệ 3:4).

Bảng màu bắt buộc (chỉ dùng các mã này, tối đa 5 màu mỗi hình):
- nền: #f5f7fa
- nét chính: #0f172a
- nhấn: #1d4ed8
- nhấn nhạt: #eef2ff
- phụ: #475569
- một màu trạng thái tuỳ chọn: #047857 hoặc #b45309

Phong cách: hình khối đơn giản, nét 3px đều, góc bo nhẹ, không gradient, không bóng đổ, không neon, không hiệu ứng phát sáng, không nhiều chi tiết nhỏ. Mỗi hình chỉ 1 vật thể chính + tối đa 2 vật phụ, nhiều khoảng trống. Phải đọc được khi thu nhỏ còn 120px chiều rộng.

Nội dung từng hình:
1. khtn-9.svg — Khoa học tự nhiên 9 (điện, từ, quang): một nam châm chữ U với vài đường sức từ nét đứt, một lăng kính nhỏ tách tia sáng (dùng màu nhấn cho tia).
2. vat-ly-10.svg — Vật lý 10 (cơ học): một quả bóng đang ném xiên với quỹ đạo parabol nét đứt, mặt đất là một đường ngang, một mũi tên vận tốc.
3. vat-ly-11.svg — Vật lý 11 (dao động, sóng, điện): một con lắc lò xo treo đứng bên cạnh một đường sin, bên dưới một mạch điện tối giản (nguồn + điện trở).
4. vat-ly-12.svg — Vật lý 12 (nhiệt, khí, hạt nhân): một bình khí có vài chấm phân tử, một nhiệt kế, một mô hình hạt nhân 3 vòng tròn đồng tâm tối giản.

Yêu cầu kỹ thuật: SVG hợp lệ, có xmlns, không script, không <image>, không <text>, mọi màu là mã hex ở trên, tổng kích thước mỗi file dưới 8 KB. Trả về 4 khối mã riêng biệt, mỗi khối ghi tên file ở dòng đầu.
```

### G2 — Huy hiệu Hạng 1/2/3

```
Vẽ 3 huy hiệu bằng mã SVG thuần cho bảng "Vinh danh tuần" của website học Vật lý (học sinh 14–19 tuổi), nền sáng. Mỗi huy hiệu là một file, viewBox="0 0 96 96", hiển thị ở 56px nên phải cực kỳ đơn giản và sắc nét: một hình tròn viền 4px, một dải ruy băng ngắn dưới đáy, và một ngôi sao 5 cánh ở tâm. Không vòng nguyệt quế, không gradient, không bóng, không chữ.

Màu (chỉ dùng các mã này):
- hang-1.svg: viền và sao #b45309, ruy băng #1d4ed8, nền trong #fff7ed
- hang-2.svg: viền và sao #475569, ruy băng #1d4ed8, nền trong #f1f5f9
- hang-3.svg: viền và sao #92400e, ruy băng #1d4ed8, nền trong #fef3c7

Để trống vùng tâm đủ rộng (đường kính ≥ 40 đơn vị) để website đặt chữ cái đầu tên học sinh đè lên ngôi sao bằng CSS; vì vậy ngôi sao vẽ bằng nét mảnh 2px, không tô đặc. SVG hợp lệ, có xmlns, dưới 2 KB mỗi file. Trả về 3 khối mã, ghi tên file ở dòng đầu.
```

---

## C. Việc Claude giữ lại (chạy trong Claude Code, có tư vấn trước khi sửa)

Dán từng dòng vào phiên Claude Code trên Mac (sau khi 4 nhánh Cursor đã merge vào `main` và 7 file SVG của Gemini đã lưu).

```
K1: Rút trang chủ còn 5–6 khối theo nhận xét 13/10 (docs/PHAN-CONG-UI-2026-10-13.md). Tư vấn trước theo B2/N2 rồi mới sửa app/(public)/page.tsx; chuyển AboutFounder + Testimonials sang trang riêng. Chụp 375/1440.
```
```
K2: /phu-huynh — thay poster điểm TNTHPT 2025 bằng bảng HTML (components/parent/… hoặc app/phu-huynh/page.tsx), tên học sinh viết tắt họ, và sửa câu "điểm của con không công khai" cho khớp. Theo P-rules.
```
```
K3: components/home/Testimonials.tsx — chọn 2–3 câu trích ngắn từ các lời nhắn, hiện dạng quote có chữ cái viết tắt, giữ 1 ảnh gốc làm bằng chứng. Không đổi nguồn album.
```
```
K4: Quét SVG trong body_html mục ly_thuyet của mọi bài (docs/DATABASE.md): <text> nhỏ hơn 13px hoặc màu pastel → nâng ≥13px, màu #0f172a/#1d4ed8. Viết script dry-run trước, đăng lại bằng scripts/cap-nhat-ly-thuyet.sh từng bài.
```
```
K5: Trang bài học — hộp Mục tiêu, hộp Dự đoán và nút TIẾP cùng tông xanh lơ; chọn lại: Mục tiêu nền surface-2, Dự đoán giữ primary-soft, TIẾP dùng primary. Sửa CSS trong globals.css khối bài học, chụp 375.
```
```
K6: Soát 4 nhánh cursor/ui-c1..c4 bằng agent kiem-code theo docs/QUY-TAC-THIET-KE.md; tối ưu 7 SVG trong assets/bia-gemini + assets/huy-hieu-gemini (svgo, kiểm tương phản), gắn vào components/home/LearningPath.tsx và HonorBoard.tsx, xoá 4 ảnh bìa cũ trong public/images/learning-path/. Chụp 375/1440 rồi /xong-viec.
```
