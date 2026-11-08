# CNC — cấu trúc bài học theo khuôn các môn khác trên web (đề xuất 08/11/2026)

> Trạng thái: **đề xuất, chờ thầy duyệt**. Chưa sửa code/DB.
> Đi kèm: `docs/CNC-FLIPPED-THIET-KE-LAI-2026-11-08.md` (nhịp buổi lớp đảo ngược, quiz chuẩn bị đã chạy).

## 1. Các môn khác đang dựng bài thế nào

Mọi môn có nội dung ngoài CNC (Vật lí 9–12, AVCN, WorldSkills IM) dùng **một khuôn**:

- Dữ liệu: `classes → chapters → lessons → lesson_items` (mỗi mục một `kind`).
- Trang: `/lop-hoc/bai`, cây chương bên trái (`ChapterTree`), chế độ trình chiếu.
- Thứ tự tab cố định (`SECTION_ORDER`, `features/lessons/types.ts`):

| # | kind | Tab | Ghi chú |
|---|---|---|---|
| 1 | `ly_thuyet` | Lý thuyết | mục I/II/III, cuối bài có **Kiểm tra nhanh** (`quiz_min_correct`) + **Trả bài**; lưu chỗ đang đọc |
| 2 | `video` | Video | |
| 3 | `bai_tap_mau` | Bài mẫu | giải từng bước, tự trả lời từng bước |
| 4 | `luyen_tap` | Luyện tập | đề luyện, làm lại được, không tính điểm |
| 5 | `bai_tap_ve_nha` | BTVN | **tính điểm**, có hạn nộp |
| 6 | `kiem_tra` | Kiểm tra | **tính điểm** |

- Cuối trang: thẻ **Mastery/YCCĐ** (`LessonMasteryCard`) — em đã vững yêu cầu cần đạt nào.
- AVCN (môn CTTC, cùng đối tượng sinh viên CĐ) đã đi đúng khuôn này: Học (8 phần) → Bài mẫu (đề 5 Part) → Luyện tập.

## 2. CNC hiện khác ở đâu

| Mặt | Các môn khác | CNC hiện tại |
|---|---|---|
| Trang | `/lop-hoc/bai` | `/lop-hoc/cnc/?bai=…` (`CncCourseWorkspace`) |
| Tab | Lý thuyết · Video · Bài mẫu · Luyện tập · BTVN · Kiểm tra | Chuẩn đầu ra · Nội dung bài học · Video · Kiểm tra · Tài liệu |
| Mục tiêu bài | đầu phần Lý thuyết | tab riêng "Chuẩn đầu ra" |
| Tự kiểm sau đọc | Kiểm tra nhanh cuối Lý thuyết | không có; quiz chuẩn bị (mới) nằm ngoài bài, đầu trang khoá học |
| Ví dụ giải mẫu | tab Bài mẫu | lẫn trong slide / bài tập G-code ở tab Kiểm tra |
| Luyện vs chấm | tách: Luyện tập (không điểm) / BTVN + Kiểm tra (điểm) | dồn hết vào tab "Kiểm tra" (quiz nhận biết lệnh, dịch lệnh, bài tập 1–5, checklist tập, checklist thật, rubric) |
| Nhóm bài | Chương | danh sách phẳng 8 bài, số bài web (1–6, 4T/4P) khác số thư mục nội dung (bai-1..bai-7) |
| Tài liệu tải về | trong Lý thuyết | tab riêng |

Hệ quả cho sinh viên: một sinh viên học cả AVCN và CNC gặp hai cách tổ chức bài khác nhau; tab "Kiểm tra" của CNC trộn bài tập luyện với bài chấm nên khó biết cái nào tính điểm.

## 3. Tư vấn theo nghiên cứu (trước khi làm)

- **Hợp — B5** (vị trí nhất quán giữa các trang) và **B8** (thứ tự mục tiêu → nội dung → tự kiểm → bài tập): dùng chung khuôn tab với AVCN giảm việc phải học lại cách dùng trang; đưa Chuẩn đầu ra vào đầu Lý thuyết đúng B8.
- **Hợp — N6** (ví dụ giải sẵn trước bài tự làm): tách tab **Bài mẫu** cho chương trình G-code giải từng dòng trước khi sinh viên tự viết ở Luyện tập.
- **Lưu ý — N2** (≤4 lựa chọn nhìn thấy cùng lúc): 6 tab trên 375px phải dùng đúng thanh tab cuộn của `/lop-hoc/bai`; bài nào thiếu mục (vd. Bài 1 không có BTVN) thì ẩn tab, không hiện tab rỗng (**N3**).
- **Ngưỡng bỏ cuộc**: tách "Luyện tập (không điểm, làm lại được)" khỏi "Kiểm tra (tính điểm, mở khoá xưởng)" làm sinh viên dám luyện nhiều hơn; giữ nguyên điều kiện mở khoá hiện có, chỉ đổi chỗ hiển thị.
- **Đo**: tỉ lệ sinh viên làm quiz chuẩn bị trước buổi (đang có ở `cnc_prep_responses`), số lượt Luyện tập trước lượt Kiểm tra đầu tiên, so 2 tuần trước/sau.

## 4. Cấu trúc bài CNC mới (khuôn chung)

### 4.1 Nhóm bài thành chương (cây trái giống `ChapterTree`)

| Chương | Bài (số theo thư mục nội dung) | id hiện tại |
|---|---|---|
| I. Nhập môn CNC | Bài 1 Tổng quan máy CNC | `intro`, `lesson-1` |
| II. Lập trình | Bài 2 Lập trình tiện · Bài 3 Lập trình phay | `lesson-2`, `lesson-3` |
| III. Vận hành | Bài 4 Vận hành tiện · Bài 5 Vận hành phay | `lesson-4-turn`, `lesson-4-mill` |
| IV. Gia công | Bài 6 Gia công tiện · Bài 7 Gia công phay | `lesson-5`, `lesson-6` |

Đổi **nhãn hiển thị** sang Bài 1–7 (khớp thư mục nội dung và chữ "70 tiết · 7 bài"); **id trong DB giữ nguyên** nên điểm, checklist, bản vẽ đã nộp không ảnh hưởng.

### 4.2 Sáu tab trong mỗi bài

| Tab | Lấy từ CNC hiện tại | Tính điểm |
|---|---|---|
| **Lý thuyết** | Chuẩn đầu ra (đầu bài) → nội dung/slide theo mục 1, 2, 3… → **Kiểm tra nhanh trước buổi** (quiz chuẩn bị `prep-N` của các buổi thuộc bài này, chuyển từ đầu trang khoá học vào đây) → Trả bài → Tài liệu tải về (cuối) | không |
| **Video** | tab Video hiện có | không |
| **Bài mẫu** | chương trình G-code mẫu giải từng dòng (Bài 2, 3), quy trình mẫu gá/so dao có hình (Bài 4, 5), bản vẽ mẫu + quy trình công nghệ (Bài 6, 7) | không |
| **Luyện tập** | bài tập 1 Nhận biết lệnh, 2 Dịch block, 3-ngắn Dịch lệnh tự gõ; quiz vận hành/cài dao; **checklist tập** | không (làm lại thoải mái) |
| **BTVN** | bài tập 3 Điền khuyết chương trình, 4 Viết chương trình từ bản vẽ, 5 Mô phỏng và kiểm chứng | có |
| **Kiểm tra** | quiz cuối Bài 1, **checklist chấm thật** tại máy, **rubric thực hành** | có, mở khoá xưởng |

Ánh xạ `CNC_ASSESSMENT_PLAN` (không đổi khoá, chỉ đổi tab hiển thị):

| Khoá đánh giá | Tab mới |
|---|---|
| `exercise-1`, `exercise-2`, `exercise-3-short` | Luyện tập |
| `exercise-3`, `exercise-4`, `exercise-5` | BTVN |
| `machine-operation`, `tool-setup`, `checklist-practice` | Luyện tập |
| `checklist`, `rubric-exam`, `final` | Kiểm tra |

> Điều kiện mở khoá bài sau vẫn là "đạt mọi khoá trong `CNC_ASSESSMENT_PLAN`". Nếu thầy muốn bài tập Luyện tập không còn bắt buộc để mở khoá, đó là quyết định riêng (mục 6, câu 3).

## 5. Cách làm — 2 chặng

**Chặng A (đề xuất làm ngay, không đổi schema, không đụng dữ liệu SV):**

1. Thêm bảng ánh xạ `CNC_LESSON_LAYOUT` (chương, số bài hiển thị, khoá đánh giá → tab) ở `services/cnc-progress.ts`.
2. `CncCourseWorkspace` đổi bộ tab thành 6 tab theo `SECTION_ORDER`, dùng chung nhãn/biểu tượng/thanh tab với `/lop-hoc/bai`; ẩn tab rỗng (N3).
3. Danh sách bài → cây 4 chương; sửa chữ cứng "70 tiết · 7 bài học" (`CncCourseWorkspace.tsx:563`) và "/7 bài" (`TeacherOverview.tsx:41`) đọc từ bảng ánh xạ.
4. Chuyển `CncPrepQuiz` vào cuối tab Lý thuyết của bài tương ứng (lọc buổi theo `lessonId`); đầu trang khoá học chỉ còn một dòng "Buổi tới: đọc … · làm 5 câu" trỏ vào đúng bài.
5. Kiểm 375px trước (D1), so cạnh `/lop-hoc/bai` một bài AVCN ở 1280·768·375.

Ước lượng: 1 phiên. Rủi ro thấp: chỉ đổi giao diện, khoá đánh giá và bảng dữ liệu giữ nguyên.

**Chặng B (để kỳ sau, khi không có lớp đang học):** chuyển hẳn nội dung CNC sang `lessons/lesson_items` (lớp `cnc`) để dùng luôn trang `/lop-hoc/bai`, Mastery/YCCĐ, trình chiếu, ghi chú lớp. Chặn hiện tại:
- id bài CNC là chữ (`lesson-2`…) và 8+ bảng khoá theo id này (`cnc_learning_records`, `cnc_drawing_submissions`, `checklist_*`, `cnc_lesson_files`, `cnc_lesson_videos`, `course_offerings.open_lesson_ids`) → cần cột ánh xạ.
- Quyền vào bài CNC đi theo `course_enrollments` + mở bài theo khoá học (`open_lesson_ids`), `lessons` chỉ có `published`.
- Checklist máy, nộp bản vẽ, quyền năng lực (`cnc_competency_permissions`) không có `kind` tương ứng → giữ là bảng điều khiển cấp khoá học.
Chặng B cần migration + kiến trúc (agent `kien-truc-du-lieu`), chỉ lên kế hoạch sau khi chặng A chạy ổn một học kỳ.

## 6. Cần thầy quyết

1. Làm chặng A ngay? (đề xuất: có)
2. Đổi nhãn hiển thị sang **Bài 1–7** khớp thư mục nội dung? (đề xuất: có; id DB giữ nguyên)
3. Bài tập ở tab Luyện tập có còn **bắt buộc để mở khoá bài sau** không? (đề xuất: giữ bắt buộc như hiện tại, đổi sau khi có số liệu)
4. Quiz chuẩn bị chuyển vào cuối Lý thuyết của bài (như Kiểm tra nhanh các môn khác) hay giữ ở đầu trang khoá học? (đề xuất: chuyển, đầu trang chỉ giữ một dòng nhắc)
