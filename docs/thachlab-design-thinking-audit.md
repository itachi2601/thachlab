# ThachLab – Kiểm tra mức độ áp dụng Design Thinking

Nguồn: báo cáo "Tư duy thiết kế trong giáo dục bậc cao" (16/10/2026).
Mục đích: rà codebase ThachLab (Next.js + Supabase) để xác định mỗi hạng mục dưới đây **đã có / có một phần / chưa có**, rồi lập kế hoạch bổ sung.

## Hướng dẫn cho agent kiểm tra

1. Chỉ ĐỌC, không sửa code, không chạy migration.
2. Với mỗi hạng mục, tìm bằng chứng theo cột "Dấu hiệu cần tìm" trong: `supabase/migrations`, `supabase/functions`, `app` (routes), `components`, `features`, `lib`, `services`, `hooks`, `types`.
3. Điền cột **Trạng thái** (`Đã có` / `Một phần` / `Chưa có`) và **Bằng chứng** (đường dẫn file + dòng, tên bảng/cột, tên route).
4. Với `Một phần` hoặc `Chưa có`: ghi phần còn thiếu và ước lượng công sức (S ≤ 1 ngày, M 2–5 ngày, L > 5 ngày).
5. Kiểm tra riêng: dữ liệu hành vi học sinh có RLS chặt chưa; có chỗ nào gửi dữ liệu định danh học sinh ra model ngoài (DeepSeek, Gemini) không.
6. Xuất kết quả thành bảng tổng hợp + danh sách đề xuất theo thứ tự ưu tiên.

## Bảng hạng mục

| ID | Ý từ hội thảo | Hạng mục cần có trong ThachLab | Dấu hiệu cần tìm trong code | Căn cứ nghiên cứu | Ưu tiên | Trạng thái | Bằng chứng / Phần còn thiếu |
|---|---|---|---|---|---|---|---|
| DT-01 | Thấu cảm – dùng bằng chứng người dùng thay vì giả định | Ghi sự kiện học tập (mở bài, thời gian ở mỗi mục, dừng ở đâu, câu sai nhiều) | Bảng kiểu `learning_events` / `activity_logs` / `page_views`; hàm ghi event khi mở lesson_item, nộp bài; truy vấn thống kê câu sai nhiều | Gruber et al. 2015; Norman | Cao | | |
| DT-02 | Thấu cảm – phản hồi trực tiếp | Kênh thu phản hồi người học (khảo sát ngắn, nút "bài này khó chỗ nào", báo lỗi) | Bucket `bug-report-screenshots`, bảng `feedback` / `bug_reports`, form góp ý trong lesson | Gruber et al. 2015 | Trung bình | | |
| DT-03 | Đánh giá quá trình | Kiểm tra ngắn 3–5 câu cuối mỗi mục lý thuyết | lesson_items loại quiz gắn với mục lý thuyết; component quiz nhúng trong trang bài | Roediger & Karpicke 2006 | Cao | | |
| DT-04 | Đánh giá quá trình – luyện truy xuất giãn cách | Lặp lại câu làm sai sau 1, 3, 7 ngày | Bảng lịch ôn (`review_queue`, `next_review_at`, `interval`); logic chọn câu ôn theo ngày | Roediger & Karpicke 2006 | Cao | | |
| DT-05 | Lộ trình linh hoạt, cá nhân hoá | Gợi ý bài tiếp theo theo dạng bài học sinh còn yếu | Dùng kết quả Edge Function `classify-questions` (nhãn dạng bài) + điểm từng dạng để đề xuất | Bloom 1984; ASU | Trung bình | | |
| DT-06 | Lộ trình linh hoạt – học làm chủ | Mở khoá bài mới khi đạt ngưỡng làm chủ (ví dụ 80%) | Cột ngưỡng / trạng thái `mastery`, `unlocked`; điều kiện hiển thị bài | Bloom 1984 | Trung bình | | |
| DT-07 | Cảnh báo sớm dựa trên dữ liệu | Bảng "học sinh cần quan tâm" cho giáo viên/trợ giảng: không đăng nhập 7 ngày, điểm giảm 2 bài liên tiếp, vắng điểm danh | Trang dashboard giáo viên; truy vấn `last_sign_in_at`, xu hướng điểm, dữ liệu điểm danh | Georgia State GPS | Cao | | |
| DT-08 | Học chủ động | AI tutor gợi ý từng bước (hỏi ngược, không đưa đáp án ngay) | Edge Function / API route AI tutor; prompt có chế độ gợi ý từng bước; giới hạn số lần xem lời giải | Freeman et al. 2014 | Trung bình | | |
| DT-09 | Học chủ động – mô phỏng | Mô phỏng PhET kèm câu hỏi dự đoán trước khi chạy | Nhúng PhET (iframe) trong bài; câu hỏi "dự đoán" đi kèm trước mô phỏng | Freeman et al. 2014 | Trung bình | | |
| DT-10 | Đồng sáng tạo, sức mạnh cộng đồng | Học sinh gửi câu hỏi/lời giải hay → giáo viên duyệt → vào ngân hàng | Bảng đề xuất câu hỏi có trạng thái duyệt (`pending/approved`); quyền RLS cho học sinh insert | OECD "new normal" | Thấp | | |
| DT-11 | Đồng sáng tạo – đội trợ giảng | Trợ giảng chấm và phản hồi bài trên cùng nền tảng | Role `assistant`/`ta`; trang chấm bài; cột nhận xét trên bài nộp | OECD "new normal" | Thấp | | |
| DT-12 | Thất bại sớm, rẻ | Cơ chế bật tính năng thử cho 1 lớp (feature flag) + chỉ số đo thành công | Bảng/cấu hình `feature_flags` theo lớp; log chỉ số trước–sau | Design Thinking; VUCA – "mơ hồ" | Cao | | |
| DT-13 | Kết nối doanh nghiệp (mảng CNC) | Thư viện bản vẽ thật làm bài tập lập quy trình gia công | Bucket `cnc-drawings`, `cnc-lessons`; trang liệt kê bản vẽ gắn với bài tập | Singapore Polytechnic | Trung bình | | |
| DT-14 | Kết nối doanh nghiệp (mảng CNC) | Sinh viên nộp chương trình G-code để nhận xét | Upload file `.nc`/`.txt`; hiển thị/kiểm tra cú pháp G-code; cột nhận xét | Singapore Polytechnic | Trung bình | | |
| DT-15 | Quan tâm sức khoẻ toàn diện | Giới hạn lượng bài mỗi ngày; hiển thị tiến bộ cá nhân thay vì xếp hạng công khai | Cấu hình giới hạn; component biểu đồ tiến bộ; kiểm tra có bảng xếp hạng công khai không | OECD "new normal" | Thấp | | |
| DT-16 | Bảo vệ dữ liệu (điều kiện cho DT-01, 04, 07) | RLS chặt cho dữ liệu hành vi; không gửi dữ liệu định danh ra model ngoài | Policy RLS trên các bảng ở DT-01/04/07; payload gửi tới DeepSeek/Gemini có chứa tên, email, mã HS không | Quy tắc nội bộ ThachLab | Cao | | |

## Mẫu kết quả mong muốn

```
Tổng: Đã có x/16 · Một phần y/16 · Chưa có z/16

Đề xuất theo thứ tự:
1. DT-xx – <việc cần làm> – <công sức S/M/L> – <file/bảng sẽ đụng tới>
2. ...
```

## Lộ trình thử nghiệm gợi ý (sau khi kiểm tra)

1. Tuần 1–2: bật ghi sự kiện học tập (DT-01) và phỏng vấn 5 học sinh lớp 12.
2. Tuần 3: chọn MỘT vấn đề gốc.
3. Tuần 4–5: làm bản mẫu (DT-03 + DT-04) cho một chương, thử trên một lớp (DT-12).
4. Tuần 6: so điểm kiểm tra chương giữa lớp thử và lớp cũ; giữ, sửa hoặc bỏ.

---

## KẾT QUẢ RÀ SOÁT (16/10/2026, chỉ đọc code + docs/DATABASE.md)

Tổng: Đã có 3/16 · Một phần 8/16 · Chưa có 5/16

| ID | Trạng thái | Bằng chứng | Phần còn thiếu · công sức |
|---|---|---|---|
| DT-01 | Một phần | `student_learning_presence` (1 dòng/HS: bài đang mở, `last_seen_at`); `theory_sessions`, `theory_reviews` (mở/nộp mục lý thuyết); `exam_question_results`, `practice_question_results`, `question_result_rollups` (câu sai theo chủ đề/dạng) | Không có bảng sự kiện nối tiếp (append-only): không biết thời gian ở từng mục, dừng ở đâu. Thêm `learning_events` + hàm ghi gộp theo lô, có retention. **M** |
| DT-02 | Đã có | `bug_reports` (+ `exam_id`, `question_index`, ảnh chụp), `app/bao-loi-cua-toi`, `xu-ly-bao-loi`; `teacher_lesson_notes` (ghi chú GV lúc dạy) | Thiếu khảo sát ngắn "bài này khó chỗ nào" gắn từng mục. **S** |
| DT-03 | Đã có | `theory_quiz_keys` (93 mục) + `theory_sessions`/`TheoryRpBar`: quiz tự chấm trong mục lý thuyết | Kiểm 3–5 câu cuối mỗi mục chưa phủ hết bài (skill `soan-quiz-ly-thuyet` bộ 20 câu). Phủ dần. **M** |
| DT-04 | Đã có | `student_mistakes` (`stage`, `next_review_at`, `cleared`), `student_mistake_review_attempts`, migration `20261011150000_student_mistakes_spaced_review.sql` | Lịch thật (đọc lại hàm ôn, 16/10): sai → 2 ngày → ôn đúng → 4 ngày → ôn đúng lần 2 → cleared + 7 ngày; ôn sai reset về 2 ngày. Gần tinh thần 1/3/7, **không đổi lịch khi chưa có số liệu**; đo sau 1 chương (tỉ lệ câu ôn làm đúng, số câu cleared). **S** |
| DT-05 | Một phần | `question_topics` + nhãn dạng từ `classify-questions`; `question_result_rollups`; phụ đạo `tutoring_needs`; radar `chapter_mastery_radar`, `course_mastery_radar` | Có chẩn đoán yếu và phụ đạo, chưa có gợi ý "bài tiếp theo" ngay trên trang HS. **M** |
| DT-06 | Một phần | Thăng hạng thích ứng `rank_gate_*`, `mastery.sql`; `course_offerings.open_lesson_ids` | Mở khoá bài do GV chọn tay, chưa tự mở khi đạt ngưỡng làm chủ. **M** |
| DT-07 | Một phần | `student_alerts` (kind: `low_score_streak`, `missed_assessment`, `exam_violation`), `evaluate_student_alerts`; vắng điểm danh có ở `thpt_attendance_*`, `ta_flags` | Thiếu tín hiệu "không đăng nhập 7 ngày" (chỉ thấy `last_sign_in_at` ở trang tài khoản) và vắng điểm danh chưa vào cảnh báo. **S–M** |
| DT-08 | Chưa có | Không có Edge Function tutor; `docs/AI-TUTOR.md` ghi rõ GĐ 4 (Q2–Q3/2027) | Theo roadmap, không xây trước. Chỉ `hsg-ai-grade` (chấm HSG, không phải tutor). **L (hoãn)** |
| DT-09 | Một phần | PhET nhúng ở bài mẫu (`content/lesson-samples/**`, skill `phet`); câu "dự đoán" có trong bài L9/L11 | Chưa thành chuẩn cho mọi bài có sim. **S/bài** |
| DT-10 | Chưa có | Không có bảng đề xuất câu hỏi từ HS | Bảng `question_suggestions` (pending/approved) + RLS insert HS + trang duyệt. **M** |
| DT-11 | Một phần | `ta_assistants`, `ta_sessions`, `ta_student_handoffs`, `app/tro-giang/*`, `exam_ta_previews`; chấm nhanh HSG (`20261010300000_hsg_cham_nhanh.sql`) | Trợ giảng quản lý buổi/phụ đạo tốt; chấm và nhận xét bài nộp bằng role riêng còn hạn chế. **M** |
| DT-12 | Chưa có | Không có `feature_flags`; chỉ có `published` và `exam_classes`/`chapter_classes` gán theo lớp | Bảng cờ theo lớp + hook đọc + log chỉ số trước/sau (nối DT-01). **M** |
| DT-13 | Một phần | `cnc_lessons`, `cnc_lesson_files`, `cnc_lesson_videos`, `app/lop-hoc/cnc` | Chưa có thư viện bản vẽ thật gắn bài lập quy trình gia công. **M** |
| DT-14 | Một phần | `cnc_drawing_submissions` (file, `teacher_feedback`, `reviewed_by`) | Nhận file nộp + nhận xét; chưa kiểm cú pháp G-code. **M** |
| DT-15 | Một phần | Có trang xếp hạng lớp `app/lop-hoc/xep-hang` (`RankPage`, RP/danh hiệu, mùa); `TheoryRpBar` có trần RP | Có bảng xếp hạng (xem rủi ro nhạy địa vị 14–18 tuổi ở `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md`); chưa có giới hạn bài/ngày; thiếu chế độ chỉ-xem-tiến-bộ-cá-nhân. **S–M** |
| DT-16 | Một phần | Có RLS: `student_learning_presence` (GV được giao đọc, HS tự quản), `student_alerts`, `student_mistakes`, `entry_diagnostics`, `theory_sessions`, `bug_reports` | Xem mục dưới. **S** |

### DT-16 chi tiết
- **RLS**: các bảng hành vi đã `enable RLS` + policy theo chủ sở hữu/GV được giao; chưa soát từng policy `select` với `anon`. Việc cần làm: chạy truy vấn `pg_policies` đối chiếu `docs/DATABASE.md` (đọc DB, ngoài phạm vi lần này).
- **Dữ liệu ra model ngoài (đã đọc code)**:
  - `classify-questions` → DeepSeek: chỉ gửi danh mục YCCĐ + **nội dung câu hỏi**, không có tên/email/mã HS. An toàn.
  - `hsg-ai-grade` → mặc định **đã là Claude Sonnet** (`provider` không truyền → "sonnet"; đọc lại code 16/10), DeepSeek chỉ chạy khi body gửi `provider: "deepseek"`. Payload: đề, đáp án chuẩn, **bài làm của HS (tối đa 6000 ký tự)**, không có tên/email/id, nhưng bài tự luận HS có thể tự ghi tên. Việc còn lại chỉ là quyết: **bỏ hẳn nhánh DeepSeek** (một dòng) hoặc lọc tên trước khi gửi. Không còn là việc ưu tiên 1.
  - `draw-figure` → Anthropic: chỉ vẽ hình, không ghi nhận dữ liệu HS.

### Đề xuất theo thứ tự ưu tiên (sửa 16/10/2026 sau khi đối chiếu code và roadmap)

Nguyên tắc xếp: việc **đo** đứng trước việc **sửa**; không chen vào mùa thử nghiệm rank (hết 25/10, `docs/ROADMAP.md` GĐ 1);
không mở roadmap thứ hai — danh sách này **gộp vào** `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md` mục 5 (14 việc đã xếp), các
mục DT-xx dưới đây được ghi thêm vào `docs/ROADMAP.md` mục "Design Thinking (16/10/2026)".

1. **DT-01** – `learning_events` mở/rời mục + nộp, ghi gộp theo lô, **kèm rollup theo ngày và retention ngắn ngay trong migration** (DB không phình, xem `docs/memory/project_thachlab_db_retention.md`); nối với A2/A3 của bản 11/10 (heartbeat đoạn đang đọc, phễu bài lý thuyết) thay vì làm song song – **M** – migration mới, `features/lessons`.
2. **DT-07** – thêm kind `inactive_7d`, `absent_streak` vào `student_alerts` (check constraint hiện chỉ 3 kind, `20260926130000_exam_violation_alert.sql`) và `evaluate_student_alerts` – **S–M** – GV/TA dùng được ngay.
3. **DT-03** – phủ quiz cuối mục lý thuyết cho **đúng chương sẽ thử** (chương đang dạy), không phủ đại trà – **M** – `theory_quiz_keys`, skill `soan-quiz-ly-thuyet`.
4. **DT-16** – chốt bỏ hay giữ nhánh DeepSeek trong `hsg-ai-grade`; soát `pg_policies` các bảng hành vi bằng truy vấn chỉ đọc – **S**.
5. **DT-12** – `feature_flags` theo lớp **sau khi** có DT-01; đo trước–sau trên cùng lớp hoặc đo chỉ số hành vi (tỉ lệ bỏ giữa bài, câu ôn làm được), **không** so điểm hai lớp khác GV/khác giờ – **M**.
6. **DT-05/06** – gợi ý bài tiếp theo + mở khoá theo ngưỡng, chỉ sau khi có dữ liệu DT-01 và số mùa 1 – **M**.
7. **DT-04** – giữ lịch 2/4/7; chỉ xem lại sau khi đo một chương – **S**.
8. **DT-15** – chế độ chỉ-xem-tiến-bộ-cá-nhân / giới hạn bài mỗi ngày: **quyết sau 25/10** cùng với C5 (mùa 2) của bản 11/10, không chen vào mùa 1 – **S–M**.
9. DT-10, DT-11, DT-13, DT-14 – ưu tiên thấp/trung bình; DT-08 hoãn theo roadmap (GĐ 4).

Lộ trình 6 tuần ở trên giữ nguyên trình tự; điểm không được bỏ là **tuần 3: chọn MỘT vấn đề gốc** — không làm cả 9 mục cùng lúc.

**Giới hạn lần rà**: chỉ grep + đọc docs/DATABASE.md và vài migration; chưa truy vấn DB thật, chưa đọc từng policy RLS, chưa mở UI. Mức "Đã có" của DT-02/03/04 dựa trên schema/migration, chưa thử bằng HS thật.
