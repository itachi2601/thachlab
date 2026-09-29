---
name: project_thachlab_kiem_tra_hieu_bai
description: "Quiz lý thuyết trỏ đúng đoạn (kiểm tra hiểu bài) — cơ chế + UI đã deploy, đã tự kiểm trên web thật; đang chờ thầy cho ví dụ cụ thể cho khiếu nại 'map sai lý thuyết' 26/9/2026"
metadata:
  node_type: memory
  type: project
  originSessionId: a0371ff8-6129-47a6-847d-b1c438608c7c
  modified: 2026-09-26T11:16:46.762Z
---

Tính năng: sau khi đọc mục lý thuyết, học sinh làm quiz "Kiểm tra nhanh" (cơ chế
sẵn có, tái dùng `exams`/`ExamRunner`/`quiz_min_correct`) — câu nào sai thì nút
"Ôn ngay" ở màn xem lại trỏ THẲNG về đúng đoạn `<h3>` lý thuyết liên quan (cuộn +
tô vàng tạm ~2.6s), thay vì chỉ nhảy tới đầu cả mục lý thuyết như trước.

**Cơ chế (đã deploy 25/9/2026, commit 3e3e8771):**
- `features/exams/types.ts` — câu hỏi có thêm tag `theorySection?: number` (chỉ số
  0-based của khối heading trong mục lý thuyết CỦA CHÍNH bài đó).
- `features/lessons/theory-sections.ts` (`wrapTheorySections`) — chia body_html
  mục lý thuyết thành từng khối gắn id `theory-sec-<itemId>-<n>`. Nhận diện 2 kiểu
  đánh dấu mục lớn: `<h3>` (kiểu Roman số I/II/III, phổ biến ở KHTN 9) HOẶC
  `<p><strong>N. Tiêu đề</strong></p>` đứng riêng 1 dòng (kiểu lớp 12, ví dụ
  "1. Mô hình động học phân tử...") — ưu tiên `<h3>` nếu có, không thì thử kiểu
  bold-numbered. Nếu bài dùng kiểu khác hẳn (không khớp cả hai) thì coi như không
  chia được, quay về hành vi cũ (không lỗi, chỉ không có hiệu ứng tô đúng đoạn).
- `app/lop-hoc/bai/page.tsx` — mục lý thuyết tự mở nếu hash `#theory-sec-<itemId>-*`
  khớp mục đó; hiệu ứng cuộn+tô chạy LẠI mỗi khi `items` cập nhật (không chỉ 1 lần).
- `components/exams/ExamRunner.tsx` + `app/kiem-tra/lam/page.tsx` — thêm prop
  `theoryLessonId`; câu sai có `theorySection` thì "Ôn ngay" build link chính xác.

**Bẫy đã tự kiểm và sửa (đáng nhớ cho việc tương tự sau này):** trang bài học ưu
tiên hiển thị BẢN TĨNH build sẵn trước (`fetchLessonWithItemsStatic`), rồi âm thầm
đối chiếu Supabase (`revalidateLesson` trong `services/static-content.ts`) và
render lại nếu khác. Hiệu ứng "chỉ chạy 1 lần lúc có dữ liệu" (dùng ref cờ) sẽ bị
bản đối chiếu mới (dangerouslySetInnerHTML dựng lại DOM) xoá mất mà không chạy lại
— bất kỳ hiệu ứng nào nhắm vào node BÊN TRONG nội dung ContentHtml đều phải tính
tới việc `items` có thể đổi nhiều lần, không được coi lần đầu là lần cuối.

**Bẫy thứ hai (commit 6fa5e7e9, 25/9/2026):** ngay sau `scrollIntoView`, có 1
re-render khác (nghi do chính lệnh cuộn làm effect scroll-spy — IntersectionObserver
dò "mục đang đọc" để tô sáng thanh điều hướng trái — đổi `activeSection`) xoá mất
class `theory-section--highlight` vừa thêm VÀ cắt ngang luôn animation cuộn, dù
`items` không đổi (đã xác nhận bằng MutationObserver, chưa lần ra nguyên nhân gốc
trong React/ContentHtml — nghi ngờ nhưng chưa chứng minh được dangerouslySetInnerHTML
có bỏ qua so sánh chuỗi giống hệt như tưởng hay không). Sửa tạm bằng cách tô lại +
cuộn lại đều đặn (setInterval ~150ms) trong giây đầu tiên thay vì làm 1 lần — không
tốn kém (classList.add lặp lại là no-op), nhưng là hướng "chữa triệu chứng" chứ chưa
sửa gốc; nếu sau này thấy hiệu ứng cuộn/tô còn chớp giật, quay lại đây trước.

**Thẻ nhắc câu sai (commit 6fa5e7e9 → sửa sticky ở 73fd9126 → nâng lên nhiều câu ở
d982ab6f, 25/9/2026):** bấm "Ôn ngay" mang theo đề bài + đáp án (đã chọn/đúng) qua
`sessionStorage` (`saveTheoryReviewContext`/`consumeTheoryReviewContext` trong
theory-sections.ts, giờ nhận **mảng** `TheoryReviewContext[]`, không phải 1 object)
— trang bài học hiện thành thẻ **liệt kê đủ mọi câu sai** có `theorySection` trong
cả lượt làm (không chỉ đúng câu vừa bấm — sai nhiều câu ở nhiều đoạn khác nhau vẫn
thấy đủ), mỗi câu có nút "↑ Xem đoạn này" tự nhảy qua lại; tô vàng ĐỦ mọi đoạn liên
quan cùng lúc, chỉ đoạn khớp hash đang bấm mới có animation cuộn. `position: fixed`
(không phải `sticky`) — `.lesson-shell` có `overflow: clip` (chặn tràn ngang di
động) khiến MỌI `position: sticky` bên trong vô hiệu, kể cả `.lesson-nav` sẵn có,
tách `overflow-x`/`overflow-y` riêng cũng không ăn thua (nghi quy tắc CSS tự
chuyển trục "visible" thành "auto"). Chỉ tóm tắt được câu trắc nghiệm 4 đáp án
(đúng-sai/trả lời ngắn/tự luận chỉ hiện đề bài, không có đáp án đúng/đã chọn).

**Làm rõ có thể bấm mở (commit de9e3cf7, 25/9/2026):** thầy test xong lần thu gọn
(09a2d383) tưởng nhầm là bug "chỉ ôn được 1 câu" — thực ra chỉ vì dòng chữ thu gọn
quá nhỏ, không để ý bấm mở được để xem hết danh sách. Đã đổi chữ rõ hơn ("bấm vào
đây để xem danh sách") + mũi tên nhấp nháy 3 lần lúc mới hiện (CSS animation
`lesson-review-hint`) để mời bấm. **Đã tự kiểm bằng cách bấm mở trực tiếp trên web
thật (thachlab.id.vn) — đúng, ra đủ danh sách.**

**Đã deploy thật:** 2 lượt build+push thủ công qua worktree riêng trong phiên này
(commit 09a2d383 rồi de9e3cf7), xác nhận bằng cách fetch trực tiếp CSS trên
thachlab.id.vn thấy đúng class mới. Sau đó phiên khác đã tự deploy tiếp lúc
2026-09-26 17:40 (nhánh `deploy` tại `f3164d1b`, dựng từ main đã có `de9e3cf7` —
kiểm bằng `git merge-base --is-ancestor` xác nhận `de9e3cf7` là tổ tiên của HEAD
hiện tại `dac7cd77`) → **không cần deploy lại, bản trên web đã có đủ các sửa của
tính năng này.**

**⚠️ Việc CHƯA xong khi bàn giao (26/9/2026) — khiếu nại "câu sai không map đúng
lý thuyết":** thầy báo "câu làm sai không map đúng với phần nội dung kiến thức lý
thuyết" nhưng KHÔNG cho ví dụ cụ thể (câu mấy, nhảy sai tới đoạn nào) trước khi
gõ `/ban-giao`. Đã tự kiểm 2 cách trong phiên này, **cả hai đều cho kết quả ĐÚNG**:
1. Đối chiếu tay cả 8 câu của exam 209 với đúng 3 mục lý thuyết thật (tải lại
   nguyên văn `body_html` của lesson_items.id=8 từ Supabase) — khớp đúng cả 8/8.
2. Truy vết tay công thức `theorySection` → href bằng đúng dữ liệu lượt làm thật
   của thầy (`exam_results.id=303`, responses `[1,1,0,1,0,1,1,1]`, 3 câu sai:
   Câu 4→mục 2, Câu 7→mục 3, Câu 8→mục 3) — khớp đúng, và đã tự kiểm lại bằng
   cách tái dựng chính xác dữ liệu đó trên web thật (thachlab.id.vn), mở thẻ ra
   thấy đúng 3 câu, đúng đoạn.

Chưa làm được: thử lại bằng thao tác CLICK THẬT (không phải sessionStorage giả
lập) qua `/kiem-tra/lam?id=209&item=8` vì dev server cục bộ (phiên khác đang sửa
song song) bị lỗi "Internal Server Error" rồi treo hẳn, không phản hồi — chưa rõ
đã hồi phục chưa.

**How to apply cho phiên sau:** nếu thầy báo lại vẫn thấy sai, VIỆC ĐẦU TIÊN là
xin ví dụ cụ thể (câu mấy, nó nhảy tới đoạn nói về gì) — đừng tự đoán/tự sửa mò,
vì đã tự kiểm kỹ 2 cách ở trên mà không tìm ra chỗ sai. Nếu thầy vẫn không cho
được ví dụ cụ thể, thử trực tiếp qua `/kiem-tra/lam?id=209&item=8` (dev server
cần đang chạy khoẻ) làm thật 1 lượt, cố tình chọn sai vài câu ở các mục khác
nhau, xong bấm "Ôn ngay" từng câu để so khớp bằng mắt.

**Nội dung — làm dần từng bài, ưu tiên lớp 12 trước (4 chương thật: Vật lí nhiệt,
Khí lí tưởng, Từ trường, Vật lí hạt nhân = 29 bài):**
- ✅ Bài 1. Sự chuyển thể (lesson_id=2, lesson_items.id=8) — exam id=209, 8 câu,
  quiz_min_correct=6, gắn `theorySection` 0/1/2 khớp 3 mục "1./2./3." — đã LIVE
  thật trên Supabase (không phải nháp), đã tự kiểm nút "Kiểm tra nhanh" hiện đúng
  + 3 khối theory-sec tách đúng trên trang thật + đã tự kiểm luôn thẻ nhiều câu
  trên web thật (xem trên).
- ⏳ 28 bài lớp 12 còn lại (Bài 2-6 chương Vật lí nhiệt, rồi 3 chương kia) — chưa làm.
- ⏳ Sau lớp 12: cân nhắc gắn vào skill `dang-bai-hoc-thachlab` để AI tự soạn quiz +
  gắn theorySection lúc đăng bài MỚI, thay vì làm hồi tố toàn bộ 118 bài THPT cũ.

**Why:** thầy chốt tái dùng hạ tầng `exams`/`ExamRunner` sẵn có (không xây quiz
riêng biệt) để không mất theo dõi tiến độ/lịch sử làm bài đang chạy ổn.
**How to apply:** khi soạn quiz cho 1 bài mới, đọc body_html mục lý thuyết trước để
biết bài đó dùng `<h3>` hay kiểu bold-numbered, soạn câu theo đúng thứ tự mục rồi
gắn `theorySection` khớp chỉ số 0-based của mục đó.
