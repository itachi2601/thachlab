# Bàn giao lập trình — Tách JS theo vai ở `/tai-khoan`, `/phu-huynh` và tách Luyện tập khỏi JS đầu `/lop-hoc/bai` (6/10/2026)

Người viết: phiên Fable 5.1 (phân tích). Người làm: phiên Sonnet. Thầy Thạch đã duyệt hướng đi ở
hội thoại 6/10/2026; bản này là spec kỹ thuật, không cần hỏi lại phần "làm gì", chỉ hỏi khi gặp mâu
thuẫn với code thật.

Đọc trước khi code (đúng các file này, không đọc hết `docs/`):
- `AGENTS.md` mục "Đăng nội dung — luôn tối ưu tốc độ tải" (quy tắc `next/dynamic({ssr:false})` + `LazyErrorBoundary`)
  và mục "Đồng bộ giữa các phiên" (working tree đầy WIP của phiên khác).
- `components/ui/LazyErrorBoundary.tsx` — đọc hết phần chú thích, nhất là mục **GIỚI HẠN**.
- Hai mẫu lazy đã dùng thật, chép đúng cấu trúc: `components/lessons/SampleQuestionsGridLazy.tsx`
  và `TopicPracticeModalLazy` trong `components/mastery/LessonMasteryCard.tsx`.
- `docs/QUY-TAC-THIET-KE.md` (UI học sinh: fallback/skeleton không được nhảy bố cục) và
  `docs/QUY-TAC-THIET-KE-PHU-HUYNH.md` (UI phụ huynh: chữ to, nền sáng, không chỉ spinner).
- `perf/chunks-report.mjs` — công cụ đo duy nhất dùng trong đợt này.

---

## 0. Số đo gốc (bản build 5/10/2026 trong `out/`, đo bằng `node perf/chunks-report.mjs .`)

| Trang | JS tải ban đầu (KB thô) | Số chunk | Ghi chú |
|---|---|---|---|
| `/tai-khoan` | 1456 | 20 | chunk riêng 166 KB + 117 KB; **framer-motion 139 KB** bị kéo vào qua `ThptStudentHome → TutoringExitQuiz` |
| `/phu-huynh` | 1167 | 18 | chunk riêng 133 KB (StudentResultsDashboard + ContentHtml + ParentScoreBars + ParentGoal) |
| `/lop-hoc/bai` | 1098 | 17 | PracticeSession (556 dòng) + LessonMasteryCard import tĩnh |
| `/kiem-tra/lam` | 1042 | 16 | phần riêng chỉ ~160 KB (ExamRunner + QuestionCard), framer đã tách |

JS nền dùng chung mọi trang: 880 KB thô / 253 KB gzip (react-dom 222, supabase-js 211, next runtime 144,
polyfills 110…). **Không đụng phần nền** — đã kết luận không đáng làm.

Chỉ tiêu sau đợt này (đo cùng công cụ, cùng cách build):

| Trang | Chỉ tiêu |
|---|---|
| `/tai-khoan` | ≤ 1000 KB theo chunks-report; HS THPT thực tế tải thêm 1 chunk ThptStudentHome |
| `/phu-huynh` | ≤ 1000 KB |
| `/lop-hoc/bai` | < 1000 KB |
| `/kiem-tra/lam` | không tăng (chỉ đo, không sửa) |

---

## 1. Ràng buộc chung cho cả ba việc

1. **Mẫu tách**: tạo file `XxxLazy.tsx` cạnh component gốc, nội dung đúng cấu trúc
   `SampleQuestionsGridLazy.tsx`: `dynamic(() => import(...), { ssr: false, loading })` bọc trong
   `LazyErrorBoundary` có `fallback` là chữ cụ thể (không phải spinner trơn). Trang gọi **chỉ đổi dòng
   import**, giữ nguyên props và vị trí render.
2. **Fallback giữ chỗ**: `loading` và `fallback` phải có chiều cao xấp xỉ khối thật (min-height) để
   không nhảy bố cục khi chunk về. Ghi mã quy tắc đã áp (HS: `docs/QUY-TAC-THIET-KE.md`; PH:
   `docs/QUY-TAC-THIET-KE-PHU-HUYNH.md`) vào mô tả commit.
3. **Không đổi hành vi, không thêm request Supabase**, không đổi RPC, không sửa copy/UI "tiện tay".
4. **KaTeX: giữ nguyên cơ chế hiện có** trong `components/exams/ContentHtml.tsx` (tải khi nội dung có
   công thức, hiện văn bản thô trong lúc chờ). Không đưa về đồng bộ, không tách thêm — thầy sẽ chốt
   riêng vì `AGENTS.md` đang nói khác code.
5. **Giới hạn LazyErrorBoundary**: chỉ dùng `dynamic` cho component mount **sau** khi đã hydrate
   (sau `RequireAuth`, sau một fetch, sau một cú bấm). Không lazy thứ render ngay cho khách ẩn danh ở
   lần tải đầu (xem chú thích GIỚI HẠN trong file boundary).
6. **Working tree đầy WIP của phiên khác** (Navbar, Footer, trang bài, trang chủ… đang sửa dở).
   Chỉ `git add` đúng file của mình; file mới phải `git add <path>` rồi `git commit -- <path>`.
   Trước khi commit, `git diff <file>` để chắc không lẫn việc phiên khác.
7. **Đo trong worktree riêng**, không `npm run build` trong cây làm việc: `git worktree add
   .claude/worktrees/perf-tach-js <commit>` rồi build và chạy `node perf/chunks-report.mjs
   .claude/worktrees/perf-tach-js`. Lý do: build lấy từ đĩa, không từ git, nên WIP phiên khác sẽ lẫn
   vào số đo.
8. **Không deploy** trong phiên này. Cuối phiên in lệnh `bash scripts/deploy.sh` cho thầy.
9. Mỗi việc **một commit riêng** (3 commit), message ghi KB trước/sau của trang đó.

---

## 2. Việc C — `/lop-hoc/bai`: tách Luyện tập (làm trước, nhỏ nhất, mẫu có sẵn)

File: `app/lop-hoc/bai/page.tsx`.

- C1. `PracticeSession` import tĩnh ở dòng 14, render ở dòng ~1578 (bên trong nhánh mục đã chấm
  điểm). Tạo `components/lessons/PracticeSessionLazy.tsx` theo đúng mẫu `SampleQuestionsGridLazy.tsx`.
  Chữ `loading`: `Đang tải phần luyện tập…`; `fallback`: `Không tải được phần luyện tập. Thử tải lại trang.`
- C2. **Xác minh trước khi tách**: mục Luyện tập chỉ mount khi học sinh mở mục (các guard `{open && ...}`
  ở `components/lessons/InlineLessonAccordion.tsx` và trong `page.tsx`). Nếu có trường hợp mục
  Luyện tập mở sẵn (tham số `?item=` trên URL, hoặc quay về từ trang làm đề với `reviewContexts`),
  lazy vẫn đúng nhưng fallback phải giữ chiều cao tương đương khối luyện tập.
- C3. Callback `onActiveChange` → `practiceActiveRef` (chặn rời trang khi đang luyện dở) phải còn
  chạy đúng sau khi tách. Kiểm bằng tay: mở luyện tập, trả lời 1 câu, bấm sang mục khác → vẫn có cảnh báo như trước.
- C4. `LessonMasteryCard` (dòng 16, render ~1830): 203 dòng, modal bên trong đã lazy. Chỉ tách nếu
  đo thấy phần nó kéo theo > 20 KB; không thì giữ tĩnh và ghi lại số đo.
- C5. Không đụng `ContentHtml`, `LessonPresenterLazy`, `SampleQuestionsGridLazy`, `WorkedQuestionsGrid`.
- C6. Kiểm: `/lop-hoc/bai?id=2` (có luyện tập), mở mục Luyện tập, làm 1–2 câu, nộp, mở lại; đường
  resume phiên luyện dở; luồng "Câu sai liên quan"; 375 px; console không lỗi.

Chỉ tiêu: `/lop-hoc/bai` < 1000 KB.

---

## 3. Việc A — `/tai-khoan`: tách bảng điều khiển theo vai (lợi lớn nhất)

File: `app/tai-khoan/page.tsx` (210 dòng; toàn bộ import nằm trên **một dòng** số 8 — tách dòng ra
cho dễ đọc là chấp nhận được, nhưng chỉ dòng import, không format lại phần khác).

Cây chọn vai hiện tại (dòng 140–207):
- `isStaff` (admin/instructor) → `StaffAccountCard` (nhỏ, giữ tĩnh).
- Có `enrollment` CNC: `StudentLearningDashboard` (dòng 174/198), `HomeroomStudentHome` (176/199),
  `StudentAttendancePanel` (177/200).
- Có `classRequest` THPT active: `ThptStudentHome` (182/203) — **đây là vai đông nhất**.
- Mọi vai: `WelcomePanel`, `DailyReminderCard` (đã lazy), `ProfileEditCard`.

Việc:
- A1. Tạo 4 file lazy: `ThptStudentHomeLazy.tsx`, `StudentLearningDashboardLazy.tsx`,
  `HomeroomStudentHomeLazy.tsx`, `StudentAttendancePanelLazy.tsx` (đặt cạnh component gốc). Trang
  chỉ đổi import. Các nhánh này đều render sau `RequireAuth` + sau fetch nên boundary bắt được lỗi.
- A2. **Framer-motion 139 KB**: `components/dashboard/ThptStudentHome.tsx` import tĩnh
  `TutoringExitQuiz` (dòng 73, dùng dòng ~659) — component này dùng framer-motion. Tách lazy tại chỗ
  dùng, chỉ mount khi điều kiện hiện quiz đúng. Sau đó chạy lại chunks-report: nếu chunk 139 KB vẫn
  còn trên `/tai-khoan`, dò tiếp qua `RankCard`/`TitleShowcase`/`ClassRankBoard` xem có kéo
  `TierLadder`, `GateQuizModal`, `FixQuizModal` (đều dùng framer) không, và lazy chúng tại nơi mở.
- A3. `ProfileEditCard`: đo; < 15 KB thì giữ tĩnh.
- A4. Fallback cho ThptStudentHome: khung tối cùng nền trang, min-height xấp xỉ màn hình đầu của
  bảng (ước 60vh), chữ `Đang tải bảng học tập…`. Vai THPT vào trang này mỗi ngày nên chunk sẽ được
  cache; chấp nhận một chớp ngắn lần đầu.
- A5. Kiểm: đăng nhập 3 vai trên local (HS THPT, GV/admin, HS CNC nếu có tài khoản test — không có
  thì ghi rõ "chưa kiểm vai CNC"); 375 px; console không lỗi.
- A6. **Thực nghiệm boundary một lần** cho chunk mới lớn nhất (ThptStudentHome): build trong
  worktree, xoá đúng file chunk đó trong `out/_next/static/chunks/`, mở tab mới → trang không trắng,
  fallback hiện. Ghi kết quả vào commit.

Chỉ tiêu: `/tai-khoan` ≤ 1000 KB theo chunks-report; framer-motion không còn trong danh sách chunk
của trang.

---

## 4. Việc B — `/phu-huynh`: tách bảng kết quả của con

File: `app/phu-huynh/page.tsx` (269 dòng). Ba nhánh render:
- Khách chưa đăng nhập (dòng ~246–258): `RequireAuth` với `guestNotice={<ParentGuestLanding />}` —
  **giữ tĩnh** (render ngay cho khách ẩn danh, đúng trường hợp giới hạn của boundary).
- Đã đăng nhập nhưng chưa liên kết con (dòng 142): `NoChildYet` — giữ tĩnh.
- Đã liên kết con (dòng 152–240): `StudentResultsDashboard` (dòng 197; 889 dòng, kéo `ContentHtml`,
  `RankCard`, `ParentScoreBars`, `ParentGoal`) + 6 thẻ nhỏ (`ParentUpcoming`, `ParentAttendanceCard`,
  `ParentHomeworkNotes`, `CatchupCard`, `ParentStanding`, `ParentTuitionCard`) + `TeacherContact`, `ParentFaq`.

Việc:
- B1. `StudentResultsDashboard` → `StudentResultsDashboardLazy.tsx`. Đây là khối chính cần tách.
- B2. Sáu thẻ nhỏ: đo trước. Nếu tổng > 40 KB thì gom **một** chunk (một file lazy xuất một component
  bọc cả cụm), không tách vụn thành 6 chunk (mỗi chunk thêm một request trên mạng 4G). Dưới 40 KB thì giữ tĩnh.
- B3. Fallback theo quy tắc phụ huynh: chữ ≥ 18 px, nền sáng, câu đầy đủ `Đang tải kết quả học tập
  của con…`, min-height giữ chỗ cho khối kết quả. Nêu mã quy tắc P… đã áp trong commit.
- B4. Kiểm: tài khoản phụ huynh có ≥ 1 con (có thì kiểm cả chọn con khi > 1), tài khoản chưa liên
  kết, và trạng thái khách; 375 px; console không lỗi.

Chỉ tiêu: `/phu-huynh` ≤ 1000 KB.

---

## 5. Việc D — `/kiem-tra/lam`: chỉ đo

Không sửa. Ghi số trước/sau vào bảng. Nếu sau việc C chunk `QuestionCard` dùng chung với trang bài
đổi kích thước thì ghi nhận, không tối ưu thêm.

---

## 6. Những việc KHÔNG làm trong phiên này

- Không đổi cơ chế KaTeX (chờ thầy chốt lại `AGENTS.md`).
- Không sửa đồng hồ đếm ngược `ExamRunner`/`PracticeSession` (việc riêng, bàn giao khác).
- Không nén ảnh (việc riêng, chạy `scripts/optimize-images.mjs`).
- Không đụng `Navbar`, `Footer`, `MobileTabBar`, trang chủ — đang có WIP của phiên khác.
- Không đụng phần JS nền dùng chung (supabase-js, react-dom).

---

## 7. Kiểm trước khi báo xong

1. `npx tsc --noEmit` sạch; `npm run lint` sạch cho file đã sửa.
2. `npm run check:a11y` nếu có thêm markup fallback.
3. Bảng chunks-report trước/sau cho 4 trang (cùng worktree, cùng cách build).
4. Thực nghiệm boundary (A6) đã làm, có ghi kết quả.
5. Ảnh chụp 375 px của 3 trang đã sửa (đặt trong `perf/` hoặc scratchpad, nêu đường dẫn).
6. Ba commit riêng, mỗi commit: KB trước/sau + mã quy tắc thiết kế + file mới đã `git add`.
7. `docs/STATE.md`: **chỉ thêm** một mục ngắn ở phần hiện trạng (số đo + 3 commit); không sửa mục khác.

Báo cáo cuối gồm: bảng số đo; danh sách file mới; file dùng chung đã đụng; vai nào chưa kiểm được
(nếu có); lệnh cho thầy:

```
bash scripts/deploy.sh
```

và nhắc: sau deploy đo lại Lighthouse đúng ba trang `/lop-hoc/bai`, `/kiem-tra/lam`, `/tai-khoan`.
