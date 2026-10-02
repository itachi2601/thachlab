# Prompt DeepSeek — Đồng bộ khung trang chương ↔ trang bài học (10/2026)

> Chạy tại thư mục gốc repo ThachLab, trên một nhánh mới tách từ `main` (`git fetch origin && git checkout -b
> feat/dong-bo-trang-chuong origin/main`). Đọc `docs/STATE.md` và `AGENTS.md` trước. Không đụng Supabase,
> không đổi schema, không thêm request mạng mới. Làm **từng đợt một PR riêng**, đợt sau chỉ bắt đầu khi
> đợt trước đã merge vào `main`.

Nguồn phân tích: `docs/NGHIEN-CUU-DONG-BO-TRANG-CHUONG-TRANG-BAI.md` (bản nghiên cứu 2/10/2026). Prompt này
là bản thực thi đã thu hẹp lại sau khi đối chiếu code; chỗ nào khác bản nghiên cứu thì **theo prompt này**.

---

## Bối cảnh (đã kiểm trên code, khỏi dò lại)

Hai trang dùng chung `.lesson-shell` nhưng khác khung xương:

| | Trang chương `app/lop-hoc/page.tsx` (583 dòng) | Trang bài `app/lop-hoc/bai/page.tsx` (1 778 dòng) |
|---|---|---|
| Khung | `.lesson-main.lesson-main--single`, **760px ở mọi breakpoint** | `.lesson-layout`: 1 cột 860px (640–1023) → `272px + 1fr` 1320px (≥1024) → `272 + 1fr + 292` (≥1320) |
| Cây chương | accordion `.class-chapter` / `.class-lesson` (43 rule `.class-*` trong `app/globals.css`, **chỉ trang này dùng**) | `renderChapterTree()` dòng ~1301, markup `.lesson-tree` / `.lesson-tree-chapter`; CSS ở `globals.css` ~1125–1139 (cột trái) và ~1210–1219 (ngăn kéo `.lesson-drawer-body .lesson-tree*`) |
| Tên chương | `chapterDisplayTitle()` (dòng 65) bỏ tiền tố "Chương N:" rồi ghép lại "Chương N · Tên" | in `chapter.title` nguyên bản → cây hiện **"1  Chương 1: Vật lí nhiệt"** (lặp số); breadcrumb dòng ~1599 và link quay lại dòng ~984, ~1001 cũng in bản thô |
| Đơn vị đếm | thanh tiến độ chương "x/y nội dung hoàn thành" (đơn vị **mục**) | `<small>x/y</small>` trong cây (đơn vị **bài**, không ghi chữ) |
| Nhãn vào bài đang dở | thẻ `.class-continue` eyebrow "Tiếp tục học", nút "Tiếp tục" | nút `renderContinueLink()` dòng ~1358 "Học tiếp" |
| Mobile < 640 | danh sách trôi, không thanh đáy | `.lesson-bottombar--mobile` 3 nút + ngăn kéo `.lesson-drawer` (vuốt/Esc) |

Đã có sẵn, **tận dụng, không viết lại**:
- Trang chương đã đọc `?chapter=<id>` vào `requestedChapterId` (dòng ~116) và tự mở/cuộn tới chương đó. Đây
  là trạng thái URL cho "chương đang chọn" — dùng lại, không thêm param mới.
- `isPeriodicExam`, `isSemesterExam`, `LESSON_KIND_META` ở `features/lessons/types.ts`.
- `courseChapters` (trang bài, dòng ~805) đã gom `{ chapter, lessons[] }` theo lớp/môn, bài KT giữa/cuối kì
  xếp cuối mỗi chương.
- CSS media: `.lesson-nav` ẩn dưới 640 (`globals.css:1157`), sticky ngang ở 640–1023 (`:1078`), cột trái
  sticky ở ≥1024 (`:1095`); `.lesson-side` chỉ hiện ≥1320 (`:1147`).

Luật repo bắt buộc (từ `AGENTS.md`):
- Không thêm round-trip Supabase. Toàn bộ việc là bố cục + tái dùng markup.
- Component nặng mới trên trang học sinh phải `next/dynamic({ ssr: false })` + `LazyErrorBoundary`
  (`components/ui/LazyErrorBoundary.tsx`). `MistakeReviewPanel`, `ClassRankGroups` trang chương đã làm vậy —
  giữ nguyên.
- Ảnh mới thêm vào `docs/anh/` phải `.webp`.
- File dùng chung (`docs/STATE.md`, `AGENTS.md`, `package.json`): chỉ **thêm dòng**, không sắp xếp lại.
- **Không refactor trang bài** ngoài đúng các chỗ prompt này chỉ.

Kiểm trước khi push mỗi đợt:

```
npm run lint
npx tsc --noEmit
npm run build
```

Chụp màn hình 375 / 768 / 1280 / 1440 (dark + light) cả hai trang, lưu `docs/anh/trang-chuong-2026-10/*.webp`,
đối chiếu với bộ ảnh trang bài sẵn có ở `docs/anh/trang-bai-2026-10/`.

---

## ĐỢT 1 — Gộp tên chương, đơn vị đếm, nhãn (PR nhỏ, làm ngay)

Mục tiêu: hai trang nói cùng một thứ tiếng. Không đổi bố cục.

### 1.1 Dời `chapterDisplayTitle` sang nơi dùng chung

Xoá hàm ở `app/lop-hoc/page.tsx:63-67`, thêm vào `features/lessons/types.ts` (file này đã chứa các helper
thuần như `isPeriodicExam`, không phụ thuộc Supabase):

```ts
/**
 * Tiêu đề chương trong CSDL thường đã có "Chương N: …". Bỏ tiền tố đó để nơi hiển thị tự ghép
 * "Chương N · Tên" (hoặc chỉ "Tên" khi số chương đã hiện riêng), tránh lặp "1  Chương 1: …".
 */
export function chapterDisplayTitle(title: string): string {
  return title.replace(/^chương\s*\d+\s*[:.\-–]?\s*/i, "").trim() || title;
}

/** "Chương N · Tên" — nhãn đầy đủ dùng cho breadcrumb, link quay lại, tiêu đề thẻ chương. */
export function chapterLabel(index: number, title: string): string {
  return `Chương ${index + 1} · ${chapterDisplayTitle(title)}`;
}
```

Trang chương: import từ `@/features/lessons/types`, dòng 389 giữ nguyên hành vi (`Chương N · tên`).

### 1.2 Trang bài dùng helper ở đúng 3 chỗ

Trong `app/lop-hoc/bai/page.tsx`:

1. Cây chương (`renderChapterTree`, dòng ~1319): `<span>{chapter.title}</span>` →
   `<span>{chapterDisplayTitle(chapter.title)}</span>` (số chương đã có ở `<em>`).
2. Tính một nhãn chương đầy đủ, đặt cạnh `courseChapters`:
   ```ts
   const chapterFullLabel = useMemo(() => {
     const idx = courseChapters.findIndex((e) => e.chapter.id === chapterId);
     if (idx < 0) return chapterDisplayTitle(chapterTitle);
     return chapterLabel(idx, courseChapters[idx].chapter.title);
   }, [courseChapters, chapterId, chapterTitle]);
   ```
   Dùng `chapterFullLabel` thay `chapterTitle` ở: breadcrumb dòng ~1599, link quay lại dòng ~984 và ~1001,
   tiêu đề ngăn kéo dòng ~1745 và `aria-label` dòng ~1733. Fallback `"Chương"` giữ như cũ khi rỗng.
3. Đơn vị trong cây: `<small>{doneInChapter}/{lessons.length}</small>` →
   `<small>{doneInChapter}/{lessons.length} bài</small>`. Kiểm ở 272px và trong ngăn kéo 375px không
   xuống dòng (CSS đã `white-space: nowrap`).

### 1.3 Đơn vị và nhãn ở trang chương

- Thanh tiến độ chương dòng ~399: `"{chapterCompleted}/{chapterTotal} nội dung hoàn thành"` →
  `"{chapterCompleted}/{chapterTotal} mục"`.
- Nút trong thẻ `.class-continue` dòng ~351: `"Tiếp tục"` → `"Tiếp tục học"`.

### 1.4 Nhãn ở trang bài

`renderContinueLink()` dòng ~1363: `"Học tiếp"` → `"Tiếp tục học"`. Kiểm nút không tràn ở cột 272px
(`.lesson-continue-btn` có `width: max-content; max-width: 100%`).

### Nghiệm thu đợt 1

- Cây chương trang bài hiện "1  Vật lí nhiệt  3/8 bài", breadcrumb "Lớp học › Chương 1 · Vật lí nhiệt › Tên bài".
- `grep -rn '"Học tiếp"\|nội dung hoàn thành' app components` không còn kết quả.
- `grep -rn 'function chapterDisplayTitle' app` không còn kết quả (chỉ còn ở `features/lessons/types.ts`).
- lint + tsc + build sạch. Ảnh 375 và 1440 của cả hai trang.

---

## ĐỢT 2 — Tách `ChapterTree`, trang chương dùng `.lesson-layout` (máy tính)

Mục tiêu: ở ≥1024, bấm một bài từ trang chương thì cây chương **đứng nguyên toạ độ**, chỉ cột giữa đổi.
Dưới 1024 trang chương **giữ nguyên accordion hiện tại** (học sinh dùng điện thoại là chính; ở đó cây chương
chính là nội dung để chọn, không giấu vào ngăn kéo).

### 2.1 Component dùng chung `components/lessons/ChapterTree.tsx`

Chuyển nguyên markup của `renderChapterTree()` (trang bài, dòng ~1301–1352) sang component. Trang bài sau đó
chỉ còn gọi `<ChapterTree …/>` ở hai chỗ (cột trái dòng ~1584 và ngăn kéo dòng ~1757). **Markup và class
CSS giữ y nguyên** để không phải sửa `globals.css` cho trang bài.

```tsx
"use client";
import Link from "next/link";
import { Check, ChevronDown } from "lucide-react";
import type { Chapter, Lesson } from "@/features/lessons/types";
import { chapterDisplayTitle, isSemesterExam } from "@/features/lessons/types";

export interface ChapterTreeEntry { chapter: Chapter; lessons: Lesson[] }

interface Props {
  entries: ChapterTreeEntry[];
  /** "learn": trang bài (bài đang xem = is-current). "pick": trang chương (chương đang chọn = is-current). */
  mode: "learn" | "pick";
  currentLessonId?: number;
  currentChapterId?: number;
  openChapterIds: Set<number>;
  onToggleChapter: (chapterId: number) => void;
  /** pick: bấm tên chương thì chọn chương (cột giữa đổi), mũi tên vẫn chỉ gấp/mở. */
  onPickChapter?: (chapterId: number) => void;
  lessonHref: (lesson: Lesson) => string;
  isLessonDone: (lesson: Lesson) => boolean;
  onLessonClick?: (lesson: Lesson) => void;
  /** Kết quả ô "Tìm bài trong khoá"; null = không lọc. */
  filterLessonIds?: Set<number> | null;
}

export default function ChapterTree(p: Props) {
  return (
    <div className="lesson-tree">
      {p.entries.map(({ chapter, lessons }, chapterIndex) => {
        const shown = p.filterLessonIds ? lessons.filter((l) => p.filterLessonIds!.has(l.id)) : lessons;
        if (shown.length === 0) return null;
        const open = p.openChapterIds.has(chapter.id);
        const done = lessons.filter(p.isLessonDone).length;
        const picked = p.mode === "pick" && chapter.id === p.currentChapterId;
        return (
          <div key={chapter.id}>
            <button
              type="button"
              className={`lesson-tree-chapter ${picked ? "is-current" : ""}`}
              onClick={() => (p.mode === "pick" && p.onPickChapter ? p.onPickChapter(chapter.id) : p.onToggleChapter(chapter.id))}
              aria-expanded={open}
              aria-current={picked ? "true" : undefined}
            >
              <em>{chapterIndex + 1}</em>
              <span>{chapterDisplayTitle(chapter.title)}</span>
              <small>{done}/{lessons.length} bài</small>
              <ChevronDown
                size={15}
                className={open ? "is-open" : ""}
                aria-hidden
                onClick={(e) => { if (p.mode === "pick") { e.stopPropagation(); p.onToggleChapter(chapter.id); } }}
              />
            </button>
            {open && (
              <ol>
                {shown.map((lesson) => {
                  const current = p.mode === "learn" && lesson.id === p.currentLessonId;
                  const isDone = p.isLessonDone(lesson);
                  const exam = isSemesterExam(lesson.lesson_kind);
                  const icon = isDone ? <Check size={11} /> : exam ? "KT" : current ? "●" : "○";
                  const cls = `${isDone ? "is-done" : ""} ${exam ? "is-exam" : ""}`.trim();
                  return (
                    <li key={lesson.id}>
                      {current ? (
                        <span className={`lesson-tree-current is-current ${cls}`} aria-current="page">
                          <i aria-hidden>{icon}</i><span>{lesson.title}</span>
                        </span>
                      ) : (
                        <Link href={p.lessonHref(lesson)} className={cls} onClick={() => p.onLessonClick?.(lesson)}>
                          <i aria-hidden>{icon}</i><span>{lesson.title}</span>
                        </Link>
                      )}
                    </li>
                  );
                })}
              </ol>
            )}
          </div>
        );
      })}
      {p.filterLessonIds?.size === 0 && <p className="lesson-panel-empty">Không thấy bài nào khớp.</p>}
    </div>
  );
}
```

Ghi chú:
- Trong trang bài, `isChapterOpen(chapter.id, lessons)` đang tự mở chương chứa bài hiện tại — giữ logic đó
  **ở trang bài**, tính ra `openChapterIds` rồi truyền xuống; component không tự quyết.
- `lesson-tree-chapter` chưa có style `is-current` cho `mode="pick"` → thêm 1 dòng vào `globals.css` ngay
  sau `.lesson-tree-chapter:hover` (khối ≥1024) và bản ngăn kéo:
  `.lesson-tree-chapter.is-current { background: var(--lesson-accent-soft); color: var(--lesson-accent-text); }`
- Nhãn KT trong cây (bản nghiên cứu §2 chỉ ra trang bài "nằm lẫn không nhãn"): thêm
  `.lesson-tree .is-exam i { font-size: 9px; font-weight: 700; letter-spacing: .02em; }` cho cả hai khối CSS.
- Kiểm bằng mắt trang bài **trước và sau** tách: 1280 cột trái, 375 ngăn kéo — phải giống hệt ngoài nhãn
  "bài" và chữ KT.

### 2.2 Trang chương dùng `.lesson-layout` ở ≥1024

Trong `app/lop-hoc/page.tsx` (nhánh `if (effectiveSlug)`):

1. Thêm state `selectedChapterId` (number | null). Khởi tạo: `requestedChapterId` nếu thuộc `classChapters`,
   không thì chương đầu tiên có bài. Khi đổi chương: `setSelectedChapterId` + `ensureChapterMastery(id)` +
   `router.replace(url, { scroll: false })` với `url` giữ `subject` hiện có và đặt `chapter=<id>` (đọc
   `window.location.search`, không dựng tay từ đầu).
2. Dựng `treeEntries: ChapterTreeEntry[]` từ `classChapters` + `lessons`, cùng quy tắc với `courseChapters`
   trang bài: bài thường trước, KT giữa/cuối kì xếp cuối chương, bỏ chương không có bài. `useMemo`.
3. Thay khung:
   ```tsx
   <div className="lesson-shell">
     <div className="lesson-layout lesson-layout--pick">
       <aside className="lesson-nav" aria-label="Chương trình lớp">
         {/* Thẻ "Tiếp tục học" (class-continue hiện tại) chuyển lên đây khi ≥1024 */}
         <ChapterTree mode="pick" entries={treeEntries} currentChapterId={selectedChapterId}
           openChapterIds={openIdsForTree} onToggleChapter={toggleChapter} onPickChapter={pickChapter}
           lessonHref={lessonHref} isLessonDone={(l) => lessonIsComplete(l)} onLessonClick={rememberLesson} />
       </aside>
       <div className="lesson-main">
         <Link href="/lop-hoc" className="lesson-back">…</Link>
         <header className="lesson-head">…giữ nguyên…</header>
         {/* ≥1024: chỉ chương đang chọn */}
         <div className="class-pick-desktop">{renderChapterSection(selectedChapter, idx)}</div>
         {/* <1024: accordion cả khoá như hiện nay, không đổi */}
         <div className="class-pick-mobile">{classChapters.map(renderChapterSection)}</div>
         <MistakeReviewPanel /> … ClassRankGroups … Đề thi … Thông báo (giữ nguyên thứ tự hiện tại)
       </div>
     </div>
   </div>
   ```
   `renderChapterSection(ch, chapterIndex)` = đúng khối `<section className="class-chapter">…</section>` +
   `semesterExams` hiện có trong `classChapters.map`, tách thành hàm để gọi ở hai nơi. Ở bản desktop, chương
   đang chọn luôn **mở** (bỏ qua `collapsedChapters`), tiêu đề `class-chapter-head` không cần nút gấp.
   `lessonIsComplete(l)` = `!!session && percent === 100` theo đúng công thức đang dùng ở dòng ~411.
4. `openIdsForTree` trên desktop = chương đang chọn + những chương người dùng tự mở trong cây (state riêng
   `treeOpenIds`, mặc định chỉ chứa chương đang chọn). Không dùng chung `collapsedChapters` của accordion
   mobile để hai chế độ không giật nhau.

CSS thêm vào `globals.css`, đặt **cuối file**, không chen vào các khối media đang có:

```css
/* Trang chương (mode pick): dưới 1024 giữ accordion ở giữa, ẩn cột trái; ≥1024 cột trái + 1 chương ở giữa. */
.class-pick-desktop { display: none; }
@media (min-width: 1024px) {
  .lesson-layout--pick .class-pick-desktop { display: block; }
  .lesson-layout--pick .class-pick-mobile { display: none; }
}
@media (max-width: 1023px) {
  .lesson-layout--pick .lesson-nav { display: none; }
  .lesson-layout--pick { max-width: 760px; }
}
/* Chưa có rail bên phải (đợt 4) → giữ 2 cột kể cả ≥1320, không để trống cột 3. */
@media (min-width: 1320px) {
  .lesson-layout--pick { grid-template-columns: 272px minmax(0, 1fr); }
}
```

Kiểm: ở 1024–1319 và ≥1320, `.lesson-main` trang chương rộng bằng `.lesson-main` trang bài (CSS `:1096`
đã `max-width: none`); ở 640–1023 trang chương **không** hiện dải sticky `.lesson-nav` (CSS trên đã ẩn).

### 2.3 Chưa làm ở đợt này

- **Không xoá** rule `.class-*`: accordion mobile và dòng bài trong cột giữa vẫn dùng. Xoá ở đợt 4.
- Không thêm `.lesson-side`, không thêm thanh đáy.

### Nghiệm thu đợt 2

- 1440: mở `/lop-hoc/12`, thấy cây chương trái + Chương 1 ở giữa; bấm Chương 3 trong cây → URL
  `?chapter=<id>`, cột giữa đổi, cây không nhảy; bấm một bài → sang `/lop-hoc/bai`, cây chương ở **cùng vị
  trí, cùng bề rộng**, chương đó vẫn mở, bài đó `is-current`. Bấm quay lại → về đúng chương.
- F5 với `?chapter=<id>` → mở đúng chương. Link cũ `/lop-hoc/12?chapter=<id>` từ nơi khác vẫn hoạt động.
- 375 và 768: trang chương **giống hệt trước đợt 2** (accordion, không cột trái, không dải sticky).
- Trang bài 1280 và 375 (ngăn kéo): giống trước, chỉ thêm "bài" và nhãn KT.
- Không có request Supabase mới: so Network tab trước/sau (số request `rest/v1` và `rpc/` bằng nhau).
- Ảnh 8 tấm: trang chương 375/768/1280/1440 dark, trang bài 1280 dark, cùng light 1440 hai trang.

---

## ĐỢT 3 — Thanh đáy điện thoại cho trang chương (không ngăn kéo)

Dưới 640, dùng lại `.lesson-bottombar.lesson-bottombar--mobile` và `.lesson-bottom-link` của trang bài
(CSS đã có, không viết mới), 3 nút:

| Vị trí | Nút | Hành vi |
|---|---|---|
| trái | `‹ Lớp học` | `Link href="/lop-hoc"` |
| giữa | `Tiếp tục học` | `continueLesson(lastLesson)`; không có `lastLesson` → bài đầu tiên chưa hoàn thành; không đăng nhập → bài đầu khoá |
| phải | `Mở tất cả` / `Thu gọn` | `toggleAllChapters()` (đã có) |

Không thêm ngăn kéo: cây chương đã nằm ngay cột giữa. Khi thanh đáy hiện, thẻ `.class-continue` ở đầu cột
giữa vẫn giữ (hai lối vào cùng một việc là chấp nhận được trên điện thoại; thẻ cho ngữ cảnh, nút cho tay
với tới). Kiểm `padding-bottom` của `.lesson-main` dưới 640 đủ để nội dung cuối không bị thanh đáy che
(trang bài đã xử lý ở `globals.css` khối `@media (max-width: 639px)` — xem nó đặt bao nhiêu và dùng cùng số).

Nghiệm thu: ảnh 375 đầu trang + cuối trang (dark), thao tác 3 nút; ≥640 không thấy thanh đáy.

---

## ĐỢT 4 — Cột giữa giàu thông tin + rail phải (CHƯA LÀM)

Phụ thuộc `docs/DE-XUAT-TRANG-CHUONG-2026-10.md` (mockup A/B/C) hiện **chưa có trên `main`**. Chỉ bắt đầu
khi file đó đã merge. Khi làm: thẻ chương (chip số liệu, dải sức khoẻ chương, dòng bài có lần cuối học),
`.lesson-side` ≥1320 với `.lesson-panel` (Tuần này · Cần ôn lại · Kiểm tra sắp tới · Thông báo), bỏ override
2 cột ≥1320 ở đợt 2, và xoá toàn bộ rule `.class-*`. Lưu ý "lần cuối học" theo bài hiện trang chương chưa
tải — phải lấy từ dữ liệu đã có (`progressMarks`) chứ không thêm query; nếu không đủ thì bỏ cột đó.

---

## Khi xong mỗi đợt

1. Commit đúng file của mình, push nhánh, mở PR vào `main`. Mô tả PR: đổi gì, ảnh trước/sau, số request
   Supabase trước/sau, file dùng chung đã đụng.
2. Thêm (không viết lại) một dòng vào `docs/STATE.md` mục hiện trạng: "Đồng bộ trang chương đợt N — PR #…".
3. Không merge tự động. Không chạy migration (đợt này không có).
