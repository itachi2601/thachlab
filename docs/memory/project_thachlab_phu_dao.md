---
name: project_thachlab_phu_dao
description: Phụ đạo theo chủ đề trên thachlab — chủ đề hai tầng (bài → yêu cầu cần đạt) đã chạy migration và deploy 16/09/2026; còn lại là gắn nhãn đề cũ
metadata: 
  node_type: memory
  type: project
  originSessionId: a5c2c433-2393-47b5-bb5f-96d72c3fc6fc
  modified: 2026-09-21T15:44:30.983Z
---

2026-09-15: user muốn "HS biết hổng phần nào · gợi ý nội dung phụ đạo cho trợ giảng ·
mục nhập học sinh nối với danh sách lớp · thầy xem được". Nối tiếp
[[project_thachlab_exam_analytics]] (đợt đó đã làm cảnh báo điểm thấp, còn thiếu mắt xích
chủ đề ↔ buổi phụ đạo).

**Phát hiện quan trọng khi khảo sát:** `question_topics` trên Supabase thật **trống rỗng**
(0 dòng) → trang "chủ đề cần ôn" của HS xưa nay vẫn trắng. Đây mới là nút thắt, không phải
thiếu tính năng.

**User chốt:** ngưỡng xét **2 bài gần nhất**; **học sinh thấy** mục cần phụ đạo của mình
(khác student_alerts vốn ẩn tới khi trợ giảng xử lý); em được phụ đạo **buộc phải có tài
khoản** (bỏ gõ tay tên). Danh mục chủ đề lấy từ file Chương trình GDPT Vật lí 2018 user gửi.

**Đã làm (commit 7cc5f8f0):**
- `docs/supabase-migration-question-topics-seed.sql` — 73 chủ đề lớp 9/10/11/12, khớp theo
  TÊN chương + TÊN bài (đã verify 73/73 khớp DB thật), nên đổi tên bài thì phải chạy lại.
- `docs/supabase-migration-tutoring-needs.sql` — `tutoring_needs` (em × chủ đề × form,
  open→assigned→tutored→cleared), `tutoring_session_topics` (buổi nào dạy gì cho ai),
  `ta_sessions.class_id` + `phudao_student_ids`, `refresh_tutoring_needs()` chạy bằng
  **trigger statement-level trên `exam_question_results`** (KHÔNG móc vào exam_results được
  vì ExamRunner ghi eqr SAU), `refresh_class_tutoring_needs()` RPC để dựng lại.
- **Mở rộng `teaches_student()`** để tính cả trợ giảng được gán lớp qua `ta_assistant_classes`
  — trước đó trợ giảng KHÔNG đọc được student_alerts/eqr (class_instructors chỉ nhận
  role='instructor'). Chạy lại file exam-analytics sẽ ghi đè mất → phải chạy lại file này.
  Thêm policy cho trợ giảng đọc `user_classes` + `profiles` của lớp mình.
- UI: `PhudaoPlanner` trong phiếu ghi buổi (chọn em từ roster + tick chủ đề đã dạy),
  `/tro-giang/phu-dao`, tab "Phụ đạo" ở `/dashboard-thpt`, mục "Phần em cần phụ đạo" ở
  `/lop-hoc/ket-qua`. `createSession()` nay trả về id.
- `docs/PHU-DAO.md` — tài liệu vòng đời + các bước chạy.

**Còn phải làm (16/09/2026):** gắn nhãn chủ đề cho đề cũ ở `/quan-tri/chu-de` (chọn yêu cầu
cần đạt, không dừng ở tên bài), gán lớp cho trợ giảng ở trang Nhân sự, rồi bấm "Rà lại cả lớp"
ở tab Phụ đạo. 4 migration đã chạy, đã deploy.

**2026-09-16 — gắn nhãn TRƯỚC khi up đề (commit cf9ec1be), chưa deploy:**
- `build_bundle.py --grade <khối>` tự tải danh mục chủ đề (REST anon-key, đọc `.env.local`) rồi
  **chặn** nếu câu thiếu `topic`/`form` hoặc `topic` không có trong danh mục (gợi ý tên gần nhất
  bằng chuỗi con + difflib; tên lệch hoa/thường thì tự chuẩn hoá). `--new-topic "Tên"` khai báo
  chủ đề mới, `--topics file` cho offline, `--allow-untagged` là đường thoát.
- `/quan-tri/nhap-bai` mục 3 có khung "Nhãn chủ đề": n/n câu + chip từng chủ đề, **chặn nút Đăng**
  tới khi đủ nhãn; ô "Tạo … chủ đề mới cho <bài>" (tick sẵn) insert `question_topics` với đúng
  `chapter_id`/`lesson_id` đang chọn → nút "Ôn lại" nhảy đúng chỗ, khỏi gắn tay.
- Hàm dùng chung `auditQuestionTags` / `canonicalizeQuestionTopics` / `tagsComplete` ở
  `features/exams/types.ts`; test `node scripts/tests/exam-tags.mjs`.
- Đã thử trên dev (route tạm, đã xoá): 4/5 câu → chặn đăng; đủ nhãn → cho đăng; bỏ tick tạo chủ
  đề mới → chặn lại. Chưa bấm Đăng thật lần nào.

**Cập nhật 2026-09-21 tối:** thầy xác nhận đã test + deploy đợt gắn nhãn trước up đề (`cf9ec1be`).
Vẫn còn treo riêng (chưa làm, không liên quan migration/deploy): RPC `restamp_exam_question_results`
cho đề đã có học sinh làm, sửa nhãn tay ngay trang nhập, và các lỗi cũ ghi ở mục "Còn treo" dưới đây.

**2026-09-16 — chủ đề hai tầng (0518e2ff · 52b99c51 · e471fa35) — ĐÃ chạy migration, ĐÃ deploy:**
Verify trên Supabase thật: 159 YCCĐ có `parent_id`, RPC `student_outcome_gaps` trả 200.
Deploy build từ **worktree sạch tại HEAD** (`.claude/worktrees/deploy-tree`, symlink
`node_modules` tương đối — symlink ra ngoài cây repo làm Turbopack chết), nên WIP examMode
trong working tree không bị đẩy lên prod. Verify prod bằng cách grep chuỗi "cầu cần đạt"
trong các chunk JS của /quan-tri/chu-de.
User chỉ ra: yêu cầu cần đạt là nội dung nhỏ trong mỗi bài, mà danh mục cũ 1 bài = 1 chủ đề.
Chốt hướng **gắn nhãn mịn, kết luận thô** (user chọn phương án hai tầng + tôi soạn danh mục
theo CT 2018):
- `question_topics.parent_id` — cha = bài (73 mục cũ giữ nguyên), con = yêu cầu cần đạt.
  Trigger `question_topic_tree_guard` chặn tầng thứ ba và ép con nằm đúng chương/bài của cha;
  `question_topic_sync_children` kéo con theo khi cha đổi bài.
- `refresh_tutoring_needs` gom `coalesce(parent_id, topic_id)` → mục phụ đạo **vẫn ở tầng bài**
  (đề 40 câu trải 6–8 bài, tính ngưỡng 3 câu ở tầng YCCĐ là không bao giờ đạt).
- `student_outcome_gaps(uuid[], int)` security definer (trợ giảng đọc được eqr nhưng KHÔNG đọc
  được exam_results) → dòng "hổng cụ thể phần nào" ở tab Phụ đạo GV, /tro-giang/phu-dao,
  phiếu ghi buổi, /lop-hoc/ket-qua.
- `docs/supabase-migration-outcomes-seed.sql`: 159 YCCĐ cho đủ 73 bài.
- Nhãn vẫn khớp **theo tên** nên tên phải duy nhất trong khối — đã soát seed không trùng.
- `LessonImporter.tsx` lẫn WIP examMode của user → tách hunk bằng `git apply --cached` với
  patch lọc sẵn, commit riêng e471fa35 (coarseNames vào audit, cảnh báo "còn gắn ở mức cả
  bài", chủ đề mới sinh thành con của chủ đề bài). WIP examMode vẫn nằm trong working tree.
- Bug cũ chưa sửa: ExamRunner map tên→id không lọc khối, mà 'Điện trở. Định luật Ohm' có ở cả
  lớp 9 và 11 → câu của một trong hai lớp có thể ăn topic_id của lớp kia.

**Còn treo:** chưa có đường sửa nhãn cho đề ĐÃ có học sinh làm — `exam_question_results` chốt
`topic_id` lúc nộp, cần RPC kiểu `restamp_exam_question_results(p_exam)` đọc lại `exams.questions`
theo `question_index` rồi gọi `refresh_tutoring_needs` (biện pháp 4 trong đề xuất 16/09, chưa làm).
Biện pháp 3 (sửa nhãn tay ngay trong trang nhập, dùng lại `ExamTagger`) cũng chưa làm.
Chương "Chương 1: Năng lượng cơ học"
thiếu dòng `chapter_classes` (không hiện cho KHTN 9) — lỗi cũ, chưa sửa.
Sửa công buổi đã ghi chưa sửa được phần chủ đề đã dạy.

Liên quan: [[project_thachlab_exam_analytics]], [[project_thachlab_ta_policy]],
[[project_thachlab_up_de_skill]], [[feedback_thachlab_deploy_scope]]
