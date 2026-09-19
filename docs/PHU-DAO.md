# Phụ đạo theo chủ đề

Trả lời đúng ba câu: **em nào đang hổng phần nào**, **ai đang kèm**, **đã dạy lại rồi thì
em có làm đúng lên không**.

## Chủ đề hai tầng

Danh mục `question_topics` là cây hai tầng: **bài học** (`parent_id` null) → các **yêu cầu
cần đạt** trong bài (CT GDPT 2018).

- **Câu hỏi gắn nhãn ở tầng yêu cầu cần đạt** — đủ mịn để biết em hổng đúng chỗ nào.
- **Mục phụ đạo mở ở tầng bài** — `refresh_tutoring_needs` gom theo
  `coalesce(parent_id, topic_id)`. Lý do: một đề 40 câu trải 6–8 bài, tính ngưỡng ở tầng
  yêu cầu cần đạt thì mỗi mục chỉ 1–2 câu, không bao giờ đủ 3 câu để dám kết luận. Một buổi
  phụ đạo cũng dạy cả bài chứ không dạy một yêu cầu cần đạt 5 phút.
- **Chi tiết "hổng phần nào"** đọc thẳng từ `exam_question_results` qua hàm
  `student_outcome_gaps(uuid[], int)` — hiện dưới mỗi mục, cho cả thầy, trợ giảng và học sinh.

Câu gắn thẳng vào tên bài vẫn chạy như cũ, chỉ là không có dòng chi tiết. Trang nhập bài và
`build_bundle.py` nhắc (không chặn) khi bài đó đã tách yêu cầu cần đạt.

## Vòng đời một mục cần phụ đạo

Một mục = *một em × một chủ đề bài học × (lý thuyết | bài tập)*.

| Trạng thái | Khi nào | Ai đổi |
|---|---|---|
| `open` | Trong **2 bài gần nhất**, em sai **≥ 50%** số câu của chủ đề đó (tối thiểu 3 câu) | hệ thống |
| `assigned` | Trợ giảng bấm "Tôi nhận" | trợ giảng |
| `tutored` | Trợ giảng ghi buổi phụ đạo và tick đúng chủ đề đó | trợ giảng |
| `cleared` | Bài sau em làm đúng **≥ 75%** chủ đề đó | hệ thống |
| `dismissed` | Thầy thấy không cần | thầy |

Đã `cleared`/`dismissed` mà hổng lại thì mục tự mở lại như vấn đề mới.

Tất cả chạy trong Supabase (trigger trên `exam_question_results`), không cần cron, không
cần server.

## Chạy lần đầu

1. **SQL Editor** → chạy `docs/supabase-migration-question-topics-seed.sql`
   (73 chủ đề Vật lí 9/10/11/12 theo Chương trình 2018, gắn sẵn vào Chương → Bài đang có).
2. **SQL Editor** → chạy `docs/supabase-migration-tutoring-needs.sql`.
2b. **SQL Editor** → `docs/supabase-migration-topic-outcomes.sql` rồi
   `docs/supabase-migration-outcomes-seed.sql` (cây hai tầng + 159 yêu cầu cần đạt).
3. **Gắn nhãn chủ đề cho các đề đã có**: `/quan-tri/chu-de` → chọn đề → gắn chủ đề + loại
   (lý thuyết / bài tập) cho từng câu. Đề chưa gắn nhãn thì không sinh được mục phụ đạo nào.
4. **Gán lớp cho trợ giảng**: `/quan-tri/phan-cong-giang-vien` → mục trợ giảng. Chưa gán thì
   trợ giảng không đọc được danh sách lớp, phiếu phụ đạo sẽ trống.
5. Vào `/dashboard-thpt` → tab **Phụ đạo** → bấm **Rà lại cả lớp** để dựng mục từ bài cũ.

Đề mới nhập bằng skill `up-de-kiem-tra` phải ghi `topic` **đúng tên trong danh mục**
(`question_topics.name`), và nên trỏ vào **yêu cầu cần đạt** chứ không dừng ở tên bài.

## Ai thấy gì

- **Học sinh** — `/lop-hoc/ket-qua`: mục "Phần em cần phụ đạo", kèm trạng thái và nút
  "Ôn lại bài". Em thấy ngay, không chờ trợ giảng xử lý (khác `student_alerts`).
- **Trợ giảng** — `/tro-giang/phu-dao`: cả lớp, xếp em hổng nhiều nhất lên đầu, bấm "Tôi nhận".
  `/tro-giang/ghi` (phiếu phụ đạo): chọn em **từ danh sách lớp**, mỗi em hiện sẵn các phần
  đang hổng, tick phần vừa dạy.
- **Giáo viên** — `/dashboard-thpt` tab **Phụ đạo**: bốn số tổng, "Nên phụ đạo chung phần nào",
  và từng em với lịch sử đã dạy (ngày, tên trợ giảng).

## Bảng

| Bảng | Vai trò |
|---|---|
| `question_topics` | Danh mục chủ đề hai tầng (`parent_id`), trỏ về `lessons.id` cho nút "Ôn lại" |
| `exam_question_results` | Đúng/sai từng câu kèm chủ đề — nguồn của mọi thống kê |
| `tutoring_needs` | Mục cần phụ đạo + trạng thái |
| `tutoring_session_topics` | Buổi nào đã dạy chủ đề nào cho em nào |
| `ta_sessions.phudao_student_ids` | Nối phiếu phụ đạo với tài khoản học sinh thật |

Từ 01/10/2026 em được phụ đạo **bắt buộc có tài khoản** — chọn trong danh sách lớp, không
gõ tên tay nữa (DB chặn ở `ta_session_student_link_guard`). Buổi trước mốc đó giữ nguyên.

## Ngưỡng

Đổi trong `public.refresh_tutoring_needs`: `v_window` (2 bài), `v_min_q` (3 câu),
`v_need_pct` (50%), `v_clear_pct` (25%).
