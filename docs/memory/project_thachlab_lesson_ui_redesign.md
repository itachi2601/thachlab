---
name: project_thachlab_lesson_ui_redesign
description: "UI học sinh tối giản theo tông trang chủ: 2 luồng riêng /lop-hoc (THPT, xanh) và /lop-hoc/cttc (CTTC, cam) + trang lớp + trang bài học — đợt 4 (22/9/2026, fb0ecbb8) hoàn thiện trải nghiệm học: dedup tiêu đề, hàng thu/mở bài tập mẫu, trạng thái đăng nhập/tải/lỗi, bảng+công thức+ảnh không tràn/nhảy layout"
metadata: 
  node_type: memory
  type: project
  originSessionId: ee582589-5020-43e8-a1a9-cc22f84b9c05
  modified: 2026-09-22T03:04:53.822Z
---

**Mục tiêu:** thầy thấy giao diện bài học "dễ phân tâm quá" → làm lại theo hướng
đọc-là-chính, một màu nhấn, ít khối/ít nút. Đã xong và deploy 2026-09-21 cho
3 trang, mỗi trang một commit trên `main` (bản deploy = build sạch từ commit):

| Trang | File | Commit |
|---|---|---|
| Bài học `/lop-hoc/bai?id=` | `app/lop-hoc/bai/page.tsx` | 1302ee86 |
| Lớp `/lop-hoc/<slug>` (mục lục chương→bài) | `app/lop-hoc/page.tsx` (nhánh `if (effectiveSlug)`) | 830fb9be |
| Chọn lớp `/lop-hoc` | `app/lop-hoc/page.tsx` (render cuối) | b5bf82df |

CSS chung nằm ở `app/globals.css`, khối "Bài học Trung học — bố cục đọc"
(`.lesson-shell .lesson-layout .lesson-nav .lesson-main .lesson-section .lesson-block
.lesson-exam .lesson-btn …`) và khối "Trang lớp" (`.class-chapter .class-lesson
.class-num .class-meta …`). Khối `.secondary-lesson-*` cũ đã xoá; các `.cnc-*` vẫn
còn vì CncCourseWorkspace (CTTC) dùng — **CTTC chưa làm lại**.

**Quyết định thiết kế đã chốt (đọc code không tự suy ra):**
- Một màu nhấn `#3B82F6` cho mọi mục; 6 màu trong `SECTION_META` (features/lessons/types.ts)
  vẫn còn nhưng trang bài học không dùng nữa (chỉ dùng label). Emoji bỏ.
- Trang bài học: 6 phần xếp dọc trong cột 760px, mục lục sticky trái (mobile: dải tab
  sticky), scroll-spy bằng IntersectionObserver. Lý thuyết hiện thẳng, mục thứ 2 trở đi
  thu gọn. Nếu tên mục trùng tên phần và là mục duy nhất → ẩn tiêu đề (`plain`/`hideTitle`).
  Phần rỗng ẩn khỏi cột chính, mờ trong mục lục.
- Giữ nguyên id `secondary-stage-<kind>` vì `/lop-hoc/ket-qua` link tới; giữ `chapter-<id>`
  và param `chapter=` để cuộn tới chương.
- Tiến độ lý thuyết: không còn tự đánh dấu khi bấm "Xem"; có nút nhỏ "Đánh dấu đã đọc".
- Trang lớp: chương mở sẵn, bấm để thu (state `collapsedChapters` thay `openChapterId`).
  Kiểm tra chương/giữa kì = dòng "KT" viền đứt. `ContinueLearningCard` không dùng nữa
  (file còn, chưa xoá). `MistakeReviewPanel` đổi sang tông trung tính.
- Chọn lớp: bỏ tab; `?tab=cttc` chỉ đổi thứ tự (CTTC lên trước) để link Navbar/AudienceChooser
  vẫn đúng. Ảnh `public/images/learning-path/*` không còn dùng ở trang này.

**Còn treo / gợi ý tiếp:**
- Các trang khác vẫn giao diện cũ, nếu thầy muốn "gọn tương tự": trang chủ học sinh THPT
  (`components/dashboard/ThptStudentHome.tsx` — đang là WIP của phiên khác, đừng đụng khi chưa
  hỏi), `/lop-hoc/ket-qua`, trang làm bài `/kiem-tra/lam`, CNC workspace.
- `PracticeSession`, `SampleQuestionsGrid`, `WorkedQuestionsGrid` chỉ mới nhận `color` một màu,
  bên trong vẫn nhiều nút/viền — chưa tối giản.
- Console có 1 lỗi 400 khi tải `/lop-hoc` và trang lớp, có từ trước redesign, chưa tìm ra
  nguồn (không hiện trong danh sách network). Nghi là truy vấn từ code WIP phiên khác.
- Chưa test với tài khoản học sinh thật (chỉ test bằng tài khoản thầy "Thạch" đang đăng nhập
  ở browser pane) và chưa test trang bài học có video/BTVN có hạn nộp.

Liên quan: [[feedback_thachlab_deploy_scope]] (cách deploy sạch bằng worktree khi tree có WIP),
[[project_thachlab_lesson_sections]], [[project_thachlab_periodic_exam]].

**Đợt 2 (21/9/2026, commit 376982d3, đã deploy):** thầy yêu cầu "THPT và CTTC để ở 2 luồng
riêng, tối giản nhưng thiết kế vẫn mang hướng của trang chủ, đồng bộ giao diện".
- `/lop-hoc` = hub THPT·THCS riêng (thẻ 10/11/12/9); `app/lop-hoc/cttc/page.tsx` = hub CTTC
  riêng (CNC, Tiện–Phay; 3 học phần "Sắp mở" mờ). Link cũ `?tab=cttc` → `router.replace`
  sang `/lop-hoc/cttc`; Navbar/AudienceChooser/breadcrumb CncCourseWorkspace trỏ thẳng hub mới.
  Navbar có `CTTC_PATHS` để mục "THPT – THCS" không sáng khi đang ở luồng CTTC.
- Ngôn ngữ trang chủ đưa vào `.lesson-shell`: nền `var(--color-bg)` (#05070b), quầng sáng
  `::before` (blur, `overflow: clip` — KHÔNG dùng hidden vì phá sticky mục lục), eyebrow mono
  viết hoa tracking như Features.tsx, thẻ kính rgba(255,255,255,.035) bo 16–18px, tiêu đề có
  `span.text-gradient` (CTTC: `.text-gradient--warm` cam). Màu nhấn chỉ qua biến
  `--lesson-accent / -hover / -text / -soft / -line / --lesson-glow`; `.lesson-shell--cttc`
  đổi cả bộ sang cam. Đã có override `html[data-theme="light"] .lesson-shell` cho cả khối.
- Đã soi: 2 hub (dark + light), trang lớp 12, trang bài học trên bản build tĩnh (serve `out/`
  cổng 3005) — vì dev server :3000 của phiên khác bị stale ("require is not defined" ở route
  `[classSlug]`, không phải lỗi code; build sạch qua hết). Vẫn chưa test tài khoản HS thật.
- **Đợt 3 (cùng ngày, commit sau 9ffde8f9, đã deploy):** CNC workspace + cổng ghi danh CNC/Tiện–Phay
  về cùng ngôn ngữ. Cách làm: GIỮ tên lớp `.cnc-*` trong TSX (1.382 dòng, chỉ đổi className),
  viết lại trọn khối CSS "Không gian học tập Gia công CNC" trong globals.css thành một bộ tối duy
  nhất, màu qua biến `--cnc-title/text/muted/faint/surface/line` + `--lesson-accent-*`; root
  workspace có `lesson-shell lesson-shell--cttc cnc-shell cnc-embedded` (giữ `.cnc-embedded` vì
  rubric ~dòng 1108 key theo nó). Bỏ hẳn nền sáng `.cnc-page` #f4f6f8. Đã soi bản build tĩnh
  (serve `out/` trên localhost:3000 khi dev server phiên kia tắt → dùng lại session admin của
  origin đó): danh sách bài, bài 2, bài 4 (mục Kiểm tra), light theme. Việc do subagent làm
  (~260k token) — đọc CSS 60KB trong subagent, phiên chính chỉ soi ảnh.
- **Vẫn chưa làm:** `/lop-hoc/ket-qua`, `/kiem-tra/lam`, trang chủ HS (`ThptStudentHome`,
  phiên khác commit 114537d4); footer vẫn tối trong light theme (có từ trước).
- Dev server :3000 của phiên khác hay stale (CSS không cập nhật, `require is not defined` ở
  route SSG) → kiểm chứng bằng build tĩnh trong worktree đáng tin hơn.

**Đợt 4 (22/9/2026, đã deploy) — hoàn thiện trải nghiệm học trên `/lop-hoc/bai`, theo
yêu cầu "giữ phong cách hiện tại, đừng thiết kế lại toàn bộ".** 6 commit trên `main`
(mỗi commit một bản deploy riêng qua worktree sạch, xem [[feedback_thachlab_deploy_scope]]):

| Việc | File chính | Commit |
|---|---|---|
| Dedup tiêu đề lý thuyết + mọi mục đơn lẻ khác, mục lục chỉ hiện phần có học liệu, tách 4 trạng thái đăng nhập/tải/lỗi/rỗng cho ExamRow/PracticeSession/SampleQuestionsGrid, đổi lưới nút "BÀI n" → hàng thu/mở | `app/lop-hoc/bai/page.tsx`, `components/lessons/{Sample,Worked}QuestionsGrid.tsx`, `PracticeSession.tsx`, `ContentHtml.tsx` | `ce8e983f` |
| Bảng dán từ Word tràn màn hình điện thoại → bọc `.table-scroll` | `ContentHtml.tsx` | `ae2aba88` |
| `.table-scroll` thiếu `max-width:100%` nên không co được | `globals.css` | `8bd7161f` |
| `.lesson-stack` là grid, item con mặc định `min-width:auto` → bảng đẩy tràn cả khối; thêm `.lesson-stack > * { min-width:0 }` | `globals.css` | `65fede62` |
| Công thức khối `$$...$$` có khung viền bo tròn riêng + `overflow-wrap/word-break` chống chữ bị `.lesson-shell{overflow:clip}` cắt mất | `globals.css` | `f8352eff` |
| Ảnh hình vẽ không có width/height → layout nhảy khi ảnh tải (rõ nhất lúc đang cuộn trên điện thoại) → script đọc kích thước thật từ header PNG/JPEG, gắn `width`/`height` vào `<img>` | `scripts/gen-image-dimensions.mjs` (mới) → `features/lessons/image-dimensions.json` (502 ảnh, tự sinh) → `ContentHtml.tsx` | `fb0ecbb8` |

**Cơ chế ảnh (đọc code không tự suy ra):** `scripts/gen-image-dimensions.mjs` quét
`public/lessons` + `public/exams`, đọc header PNG/JPEG (không cần thư viện ảnh), ghi
`features/lessons/image-dimensions.json` (map `/lessons/.../fig01.png` → `[w,h]`).
Chạy tự động qua `npm run prebuild` (hook chuẩn của npm, xem `package.json`) trước
**mỗi lần** `npm run build`/`deploy.sh` — ảnh đăng sau tự có, không cần chạy tay. File
JSON **có commit vào git** (không gitignore) vì `next dev` import tĩnh lúc chưa build
lần nào cũng cần nó tồn tại sẵn.

**Quyết định thiết kế thêm (đợt 4):**
- `plain`/`hideTitle` (ẩn tiêu đề mục khi trùng ý phần) giờ áp dụng cho **mọi mục đơn lẻ**
  trong phần (`section.items.length === 1`), không riêng lý thuyết và không cần khớp chữ
  chính xác như bản gốc.
- `SampleQuestionsGrid`/`WorkedQuestionsGrid`/`PracticeSession` vẫn giữ prop `color` (không
  đổi sang biến `--lesson-accent`) vì 3 component này còn dùng lại ở `InlineLessonAccordion`
  (trang lớp) và `LessonImporter`/`AzotaExamComposer` (khu quản trị) — nơi không có
  `.lesson-shell` bao ngoài. CSS mới (`.lesson-sample-*`, `.lesson-worked-*`, `.table-scroll`)
  cố ý tự chứa màu (rgba trung tính), không phụ thuộc biến `--lesson-*`.
- `ExamRow` không còn hiện "Đề #<id>" — chưa đăng nhập/đang tải/lỗi/không tìm thấy đều có
  chữ riêng, tên đề thật chỉ hiện khi đã tải xong.

**Đã kiểm tra:** build sạch + `tsc`/`eslint` từng bước; soi thật trên production
(thachlab.id.vn) bằng khung điện thoại giả lập lẫn ảnh chụp máy thật của thầy (bài
"Bài 12 – Cảm ứng điện từ" lớp 12, bài "Lực từ. Cảm ứng từ"); test riêng
`SampleQuestionsGrid` với đề thật (exam id 18) qua route tạm `app/tmp-verify-sample`
rồi xoá ngay (không đụng dữ liệu DB thật — thử PATCH thẳng DB bị permission chặn "Modify
Shared Resources", không cố lách).

**Còn treo:**
- Vẫn chưa test tài khoản học sinh thật (chỉ test tài khoản thầy "Thạch").
- Trang lớp `/lop-hoc/[slug]` cũng được thầy (hoặc phiên khác) làm thêm cùng lúc: mở sẵn
  1 chương, nút thu/mở tất cả, thanh tiến độ chương, nhãn trạng thái rõ nghĩa hơn, "Tiếp
  tục học" thêm `resume=1` tự cuộn tới mục chưa xong, bài học thêm thanh Bài trước/Bài tiếp
  theo — đi vào cùng các commit `ce8e983f`..`65fede62` ở trên (đã review + build sạch trước
  khi gộp, không phải việc tự làm trong phiên polish này nhưng cùng đợt deploy).
- `/lop-hoc/ket-qua`, `/kiem-tra/lam`, CNC workspace vẫn chưa "gọn tương tự" (như đợt 1 đã ghi).
- Ảnh chụp máy thật của thầy còn 1 điểm ngờ (dòng chữ ghost/đè ở mép trên khi vừa cuộn) —
  nghi là compositing lúc chụp màn hình lúc đang cuộn (không tái hiện được qua kiểm tra kỹ
  thuật: `document.documentElement.scrollWidth` luôn khớp viewport, không overflow thật) chứ
  không phải bug tràn chữ như 2 lần trước — sau khi vá layout-shift ảnh (đợt 4 dòng cuối) nếu
  thầy vẫn thấy lại đúng kiểu này thì báo tiếp, khả năng còn nguyên nhân khác.

Liên quan thêm: [[project_thachlab_concurrent_sessions]] (đợt này có tới 2-3 phiên khác
cùng sửa `app/lop-hoc/bai/page.tsx`/`app/globals.css` song song — phải soát git diff kỹ
trước mỗi commit).

## 2026-10-02 — khối "📌 Tóm tắt ý chính cần thuộc" dời sang tab Luyện tập
- **Đã làm + deploy:** `TheorySummary` (`app/lop-hoc/bai/page.tsx`) không còn render trong `TheoryBlock` (tab Lý thuyết). Nó hiện ở đầu mục `luyen_tap` đầu tiên của bài (`showSummaries` trong `renderSectionItems`), gộp `summary_html` của MỌI mục `ly_thuyet` trong bài, mỗi mục một khối, mục rỗng thì ẩn. PR #35 (commit 10f69b2e) đã merge `main`; bản build đẩy lên nhánh `deploy` lúc 15:37 ngày 2026-10-02 (hosting kéo trong ~10 phút).
- **Quyết định đã chốt:** đặt ĐẦU tab Luyện tập (ôn ngay trước khi làm bài). Chưa hỏi lại thầy muốn cuối tab hay ngay trên đề đầu tiên.
- **Dữ liệu không đổi:** cột `lesson_items.summary_html` vẫn gắn vào mục lý thuyết (migration 20260927120000, `scripts/backfill-lesson-summary.mts`); chỉ chỗ hiển thị đổi.
- **Chờ:** chưa mở web thật để xem bằng mắt (cần đăng nhập HS + bài đã backfill tóm tắt); chưa chụp 375px. Bài chỉ có mục `bai_tap_mau`/đề chấm mà không có mục `luyen_tap` thì sẽ KHÔNG thấy tóm tắt ở đâu cả — chưa xử lý trường hợp này.
- **Lưu ý deploy:** lúc deploy có phiên khác chạy `scripts/deploy.sh` cùng lúc trong `.claude/worktrees/deploy-tree` (cùng thư mục `out/`), cả hai kẹt ở `git fetch --depth=1 deploy` do mạng chậm. Tôi chỉ dừng tiến trình của mình rồi chạy lại một mình mới đẩy được. Trước khi deploy nên `ps aux | grep deploy.sh` xem có phiên nào đang chạy không.

## 2026-10-02 — nút "Trình chiếu bài giảng" ở tab Lý thuyết (dạy trên lớp, chiếu tivi/máy chiếu)
- **Đã làm:** `components/lessons/LessonPresenter.tsx` (+ bản tải chậm `LessonPresenterLazy.tsx`) — lớp phủ toàn màn hình lật từng trang, phím ←/→/Space/Home/End, mục lục nhảy nhanh (L), bảng phím tắt (?), bút vẽ + dạ quang + tẩy + bỏ nét (D/H/E/Z/C), Ctrl +/−/0 đổi cỡ chữ, nền sáng/tối, F toàn màn hình, Esc thoát dần. Nút mở đặt ở đầu tab Lý thuyết (`app/lop-hoc/bai/page.tsx`), chỉ tab đó; mở thẳng bằng `#chieu` trên URL.
- **Quyết định đã chốt với thầy (2 câu hỏi trước khi code):** (1) chỉ tab Lý thuyết, không làm cho tab bài tập/đề; (2) lật từng trang theo mốc I., II., III. + có bút vẽ và phóng to chữ; KHÔNG làm đồng hồ đếm ngược, không làm "che/bôi đen từng khối".
- **Chia trang chiếu KHÁC trang đọc — có lý do, đừng "thống nhất" lại:** `features/lessons/theory-sections.ts` giờ có `splitTheorySections(html, itemId, mode)`; `mode: "doc"` (mặc định, giữ nguyên hành vi cho "Ôn ngay") ưu tiên h3 → in đậm đánh số → h2; `mode: "chieu"` ưu tiên mốc LỚN h2 → h3 → in đậm. Nếu chia trang chiếu theo mốc nhỏ, mọi mục lớn đứng trước mốc nhỏ đầu tiên bị dồn vào "phần mở bài" (thấy thật ở bài 9 "Khái niệm từ trường": I + II + III nằm chung 1 trang, 5 trang sau chỉ là mục con "1. Định nghĩa" mất ngữ cảnh). Đo trên 81 mục lý thuyết: 39 mục có h2 khác "LÝ THUYẾT", 42 mục có h3, 22 mục có cả hai, 17 mục chỉ in đậm đánh số, 5 mục không có mốc nào → deck 1–8 trang/mục.
- **Không thêm request nào:** deck dựng từ `body_html` đã tải sẵn của tab Lý thuyết (không RPC mới, không route mới) — đúng quy tắc tối ưu tốc độ trong AGENTS.md. Component tách bằng `next/dynamic({ssr:false})` + `LazyErrorBoundary` nên không vào JS ban đầu của `/lop-hoc/bai`.
- **Bẫy đã gặp khi kiểm:** `setState` thẳng trong thân `useEffect` bị eslint `react-hooks/set-state-in-effect` chặn, và đọc `ref.current` lúc render bị `react-hooks/refs` chặn → cỡ chữ/nền đọc ngay trong hàm khởi tạo `useState` (component chỉ mount ở client), còn số nét vẽ giữ ở state riêng thay vì đọc `strokesRef` khi render.
- **Chờ:** chưa thử trên tivi/máy chiếu thật và chưa thử Safari/iPadOS (nút Toàn màn hình trên iOS không hỗ trợ cho phần tử — đã bọc `catch` nên chỉ là không phóng to; lớp phủ vẫn phủ kín màn hình).

## 2026-10-02/03 — gọn đầu trang bài học theo QUY-TAC-THIET-KE (4 mục ưu tiên 1 phụ lục A + bỏ căn đều)
- **Mục tiêu:** thầy thấy trang `/lop-hoc/bai` rối, yêu cầu mọi thiết kế phải theo nghiên cứu tâm lý/thị giác HS và ghi thành quy tắc. Quy tắc nằm ở `docs/QUY-TAC-THIET-KE.md` (mã N/C/M/B/H/D/L, checklist mục 8, **phụ lục A = bảng lỗi trang bài học theo ưu tiên**), nối vào `AGENTS.md`; memory `feedback_design_research_rules`. Commit `f08e46a0a`.
- **Đã sửa + deploy (2026-10-03 00:33, nhánh deploy `ac194d7`, live đã xác minh qua CSS chunk `0mkqcj93i94o2`):**
  - `8bad25b13` — `app/lop-hoc/bai/page.tsx` + khối CSS cuối `app/globals.css` ("Trang bài học — đợt gọn 2/10/2026"): bỏ mục cuối breadcrumb lặp h1, ẩn breadcrumb dưới 640px, bỏ chip "Bài học" + đếm "N mục · M phần" (chip chỉ còn khi `lessonKind !== "bai_hoc"`); nội dung học bắt đầu 58% → ~36% màn đầu ở 375×812. Thẻ "Trình chiếu bài giảng" bỏ, thay bằng nút nhỏ "Trình chiếu" trong `readTools`, chỉ `profile.role` ∈ admin/instructor/tro_giang (`canPresent`; `profile` đã tính chế độ "Xem như học sinh"). `#chieu` trên URL vẫn mở cho mọi người. Bảng chữ|hình (`.table-scroll table:has(img)`) xếp dọc dưới 760px, th/td không in đậm. `img.figure` trong `.lesson-prose` một khung chung: nền trắng, đệm 10px, bo 10px, max 440px. CSS `.lesson-present*` cũ đã xoá.
  - `1f0c9cd9a` — `.lesson-prose p { text-align: left }` thay justify (C6).
  - Deploy đi nhờ build của phiên khác (cùng `deploy-tree`, build từ commit sau của tôi nên đã gồm).
- **Còn treo:** (1) chưa thử nút Trình chiếu bằng tài khoản GV thật, chưa chụp bản live (browser pane từ chối mở thachlab.id.vn lần cuối); (2) phụ lục A mục ưu tiên 2–3 CHƯA làm: cột phải desktop 2 thẻ rỗng (Câu sai liên quan, Ghi chú), cột trái lặp mục lục chương + tiến độ cả lớp, thanh đáy mobile "Đánh dấu đã học xong bài này" 3 dòng, tab "Kiểm tra" trôi khỏi 375px, breadcrumb đè toolbar "Dịu mắt" ở 1440px, nền tối mặc định cho trang đọc (M1), 15 cỡ chữ trong vùng nội dung, công thức nghiêng không phải KaTeX, cột đọc 84 ký tự/dòng; (3) trang chủ HS, `/lop-hoc/ket-qua`, `/kiem-tra/lam` chưa rà theo quy tắc.
- **Lưu ý:** dev server :3000 chạy được route `/lop-hoc/bai/?id=4&subject=vat-ly&chapter=2&class=lop-12` (lỗi `generateStaticParams` chỉ do gõ sai slug lớp — slug đúng là `lop-12`, không phải `12`). Khi deploy luôn `pgrep -f "^bash scripts/deploy.sh"` trước; nhiều phiên deploy chồng nhau, `git fetch --depth=1` hay kẹt vài phút.
