# Bản đồ quy trình & đề xuất skill còn thiếu — 29/9/2026

Báo cáo phân tích, **không tạo skill, không viết code**. Mọi kết luận "chưa có" đều kèm bằng chứng đã
kiểm tra (file:dòng hoặc kết quả grep). Đọc theo thứ tự: §1 phạm vi khảo sát → §2 kiểm kê → §3 bản
đồ quy trình → §4 đề xuất → §5 việc phụ phát hiện thêm.

---

## 1. Phạm vi đã khảo sát (đọc thật)

| Nguồn | Đã đọc |
|---|---|
| Plugin Cowork/Desktop `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/…/skills/` | 26 skill: 10 nghiệp vụ (đọc trọn SKILL.md + `ls` scripts/references) + 16 generic (đọc frontmatter) |
| Repo `.claude/skills/` | `up-de-kiem-tra` (447 dòng), `dang-de-hang-loat` (300 dòng) |
| Repo `.claude/commands/` | `ban-giao.md`, `tinh-hinh.md` (slash command, không phải skill) |
| `~/.codex/skills/` | 4 bản sao: `azota`, `dang-bai-hoc-thachlab`, `latex`, `ngan-hang-cau-hoi` — đã `diff -rq` với bản plugin |
| `/mnt/skills/plugins/` | không tồn tại trên máy này |
| Repo ThachLab | `docs/STATE.md`, `ROADMAP.md`, `DATABASE.md` (99 bảng), `DATABASE-RPC.md` (216 hàm), 8 docs chuyên đề, 56 route `page.tsx`, 34 file `scripts/`, grep toàn repo theo 5 nhóm từ khoá |
| `anthropics/k12-teacher-skills` | clone thật, đọc 4 SKILL.md + `references/` + `evals/*/rubrics/*.csv` |
| Memory dự án | `project_thachlab_cnc_kiem_tra_redesign`, `cttc_roster_import`, `homeroom`, ARCHIVE |

Ghi chú: `docs/MANIFESTO.md` và `docs/PROJECT.md` là file **rỗng 0 byte**.

---

## 2. Kiểm kê skill hiện có

### 2.1 Skill nghiệp vụ (12) + command (2)

| Skill | Mảng | Input → Output | Chuẩn/YCCĐ tham chiếu | Kiểm định |
|---|---|---|---|---|
| `de-vat-ly-thpt` | Vật lí | chủ đề/lớp/tỉ lệ NB-TH-VD → `de.json` → Word Azota + đáp án + lời giải + **ma trận** | Cấu trúc TN 2025 18+4+6 (SKILL.md:25–29); GDPT 2018 (:19); ma trận chủ đề × mức độ (:36–39, `build_docx.py:206–219`). **Không** nêu TT32, **không** có bản đặc tả | checklist B7 (:100–107), `kiem_tra()` |
| `azota` | Vật lí + LMS | `.docx` có PHẦN I/II/III → `de_azota.docx`, `de_moi.docx` (lời giải), `de_thachlab.docx` (nhãn YCCĐ) | Cấu trúc TN 2025 (:205–210); YCCĐ từ `question_topics` (:152–176). Cố ý **bỏ** mức độ NB/TH/VD (:31–33) | checklist B4, script soát nhãn |
| `ngan-hang-cau-hoi` | Vật lí + LMS | `.docx` không PHẦN → `_ChuanHoa.docx` + `de_thachlab.docx` | YCCĐ danh mục khối (:111, :131–133) | checklist B5, câu mơ hồ đánh `?` |
| `mathtype-sang-omml` | công cụ | `.docx` MTEF → OMML tại chỗ | không | B5 xác minh 3 tầng bắt buộc |
| `latex` | Vật lí + **cơ khí** + LMS | `.docx` → `final.tex`, `parts.json`, HTML | không YCCĐ; có mục "8. Cơ khí/CNC" phiên âm Ø, Ra, G-code (`references/phien_am.md:87–95`) | `html_report.json`, `blank_images` |
| `dang-bai-hoc-thachlab` | Vật lí + LMS | `.tex`/HTML → bundle JSON → `lesson_items` + `exams` | YCCĐ `question_topics` (:60–65); `tex-structure.md:64` "LMS không có trường ma trận" | `validateBundle`, audit nhãn |
| `up-de-kiem-tra` (repo) | Vật lí + LMS | 1 file đề → `de.txt`/`bundle.json` → `/quan-tri/dang-de` hoặc `/nhap-bai` | YCCĐ 2 tầng (:67–68, :295–299); độ khó Dễ/TB/Khó do AI (:92–98) | `build_bundle.py`, soát SVG 2 bước |
| `dang-de-hang-loat` (repo) | Vật lí + LMS | thư mục `.docx` → `classify-report.json` → đăng tuần tự | cho phép tạo YCCĐ mới tại `/quan-tri/chu-de` (:130–152) | 4 lưới lọc, định lượng token |
| `bien-ban-shcn` | **CĐ Cao Thắng** (chủ nhiệm) | nội dung tuần trường + PDF GDĐĐ → biên bản Word/PDF + `homeroom_weekly_sessions` | biểu mẫu trường (:34) | không |
| `diem-danh-excel` | CĐ (chủ nhiệm) | chat Zalo lớp trưởng → Excel điểm danh | không | "không bịa số liệu" |
| `thachlab-perf-parallel-agents` | dev LMS | danh sách việc → nhiều worktree/nhánh | không | kiểm hồi quy |
| `skill-creator` | chung | ý định → skill + `evals/evals.json` + benchmark | không | **đầy đủ nhất**: grader, blind compare |
| `ban-giao`, `tinh-hinh` | quy trình | ghi/đọc memory đầu-cuối phiên | không | không |

Generic (16): `docx`, `pdf`, `pptx`, `xlsx`, `docs`, `deep-research`, `schedule`, `morning`,
`consolidate-memory`, `import-memory`, `explain-usage`, `setup-claude`, `setup-cowork`,
`built-in-browser`, `chrome-browser`, `computer-use`.

### 2.2 Kết luận kiểm kê (5 câu chốt)

| Câu hỏi | Kết quả | Bằng chứng |
|---|---|---|
| Có skill soạn **giáo án/KHBD theo CV 5512**? | **Không** | `grep -ri '5512\|giáo án\|kế hoạch bài dạy'` trên plugin + repo skills + commands → 0 |
| Có skill **phân tích kết quả** (Azota export, `exam_question_results`)? | **Không** | grep `attempts\|exam_attempts\|phân tích kết quả` → 0; các skill chỉ *gắn nhãn đầu vào* (`up-de-kiem-tra:291–302`) |
| Có skill phục vụ **CNC/cơ khí/ABET**? | Chỉ chủ nhiệm lớp CĐ CK 26C (`bien-ban-shcn`, `diem-danh-excel`) + 1 mục phiên âm cơ khí trong `latex`. **ABET/ETAC: 0 kết quả** ở mọi nơi (skill lẫn repo) | grep `ABET\|ETAC` → 0 |
| Có skill **mô phỏng/thí nghiệm ảo**? | Không. Chỉ có vẽ SVG tĩnh (`dang-bai-hoc-thachlab:187–196`, `up-de-kiem-tra/scripts/svglib.py`) | grep `mô phỏng\|PhET\|thí nghiệm ảo` → 0 |
| Có **ma trận / bản đặc tả**? | Ma trận: chỉ `de-vat-ly-thpt` (Word). **Bản đặc tả: không** | grep `đặc tả` → 0 |

### 2.3 LMS ThachLab đã có / chưa có (đọc code, không đọc docs cũ)

| # | Năng lực | Trạng thái | Bằng chứng |
|---|---|---|---|
| 1 | Nộp bài, chấm tự động | **ĐÃ CÓ** (tự luận chấm tay) | `features/exams/types.ts:143–165` `gradeQuestion()`; `ExamRunner.tsx:180–229` ghi `exam_results` + `exam_question_results`; RPC `grade_essay_answer` |
| 2 | Thống kê theo lớp/câu/YCCĐ | **ĐÃ CÓ** | `TeacherThptAnalysis.tsx`; RPC `get_class_exam_question_stats`, `get_class_topic_matrix`, `student_outcome_gaps`; `/dashboard-thpt/chua-bai` |
| 3 | Theo dõi tiến độ (mastery YCCĐ, phụ đạo, rank) | **ĐÃ CÓ** (chưa test HS thật) | `services/mastery.ts`, `tutoring_needs` + trigger, 12 bảng `rank_*` |
| 4 | Mô phỏng tương tác | **MỘT PHẦN, rất nhỏ** | 1 con lắc lò xo ở hero trang chủ (`components/physics/SpringSimulation.tsx`); `lib/Physics/*.ts` 6 mô hình **không được import**; 0 `<animate>`, 0 PhET trong bài; ROADMAP GĐ 3 = Q1/2027 |
| 5 | Xuất báo cáo GV | **MỘT PHẦN** | THPT chỉ CSV thô (`TeacherThptGradebook.tsx:36–39`); CTTC có xlsx (`services/roster-export.ts`); **không** PDF/Word, không báo cáo phân tích; ROADMAP GĐ 5 chưa làm |
| 6 | Nhập kết quả từ Azota | **CHƯA CÓ** | Toàn bộ code Azota là chiều đề → LMS (`AzotaExamComposer.tsx`, `docx-exam-parser.ts`) hoặc iframe (`docs/AZOTA-INTEGRATION.md`) |
| 7 | Giáo án / lịch dạy theo bài | **CHƯA CÓ** | grep 0; không bảng; chỉ `thpt_course_schedules` (lịch tuần khoá), `ta_sessions` (phiếu TA sau buổi) |
| 8 | Ngân hàng câu hỏi gắn YCCĐ + mức độ | **ĐÃ CÓ** | `question_bank` ~12.803 câu, `difficulty` gv/ai, `find_similar_bank_questions`; còn ~3.541 câu chưa có mức độ (STATE.md:49) |
| 9 | Ma trận ra đề / bản đặc tả | **CHƯA CÓ** | "ma trận" trong code là ma trận *phân tích* (`get_class_topic_matrix`); ROADMAP GĐ 5 "[ ] Tạo đề theo ma trận (YCCĐ × Dễ–TB–Khó)" |
| 10 | Nội dung CĐ / CNC | **ĐÃ CÓ, đóng băng** | 25 bảng CTTC, 8 `cnc_lessons`, 12 quiz bank `cnc_key`, 10 năng lực (`services/cnc-competencies.ts`), checklist, nộp bản vẽ, điểm danh theo máy; ROADMAP: "chỉ sửa lỗi" |
| 11 | Phản hồi cá nhân hoá sau bài | **MỘT PHẦN** | xem lại từng câu + `explanation`, "Ôn lại bài", "Luyện 10 câu", BTVN tự sinh 10 câu sai + 20 câu ngân hàng (`services/homework.ts`); chưa có "3 kỹ năng yếu nhất", gợi ý đoạn lý thuyết |
| 12 | Phụ huynh xem kết quả | **ĐÃ CÓ** | `docs/PHU-HUYNH.md`, `parent_links`, `/phu-huynh` |

---

## 3. Bản đồ quy trình

Ký hiệu: **[CÓ]** = đã có skill hoặc LMS phủ trọn · **[MỘT PHẦN]** · **[TRỐNG]**.

### 3.1 Mảng Vật lí THPT (GDPT 2018)

| Khâu | Trạng thái | Cái đã có | Cái còn thiếu (bằng chứng) |
|---|---|---|---|
| 1. Soạn chuẩn / YCCĐ | **[MỘT PHẦN]** | Danh mục `question_topics` 254 mục 2 tầng Bài → YCCĐ, trang `/quan-tri/chu-de`, script `backfill-lessons-description-thpt.mjs` | Không có file gốc TT32/2018 trong repo/skill để đối chiếu; `dang-de-hang-loat:130–152` cho phép thêm YCCĐ mới tay → danh mục có thể trôi khỏi TT32; không có nhãn năng lực thành phần / mức độ động từ (nêu được, vận dụng được) |
| 2a. Giáo án / KHBD (CV 5512) | **[TRỐNG]** | — | grep 0 trong mọi skill và repo (§2.2) |
| 2b. Bài giảng số lên LMS (lý thuyết, dạng bài) | **[CÓ]** | `latex` → `dang-bai-hoc-thachlab`; `/quan-tri/bai-hoc` | — |
| 2c. Slide / phiếu học tập cho tiết dạy | **[MỘT PHẦN]** | `pptx`, `docx` generic | Không skill nào sinh phiếu học tập / slide **từ** bài đã đăng trên LMS hoặc từ KHBD |
| 3a. Soạn đề mới / chuẩn hoá đề TN 2025 | **[CÓ]** | `de-vat-ly-thpt` (ma trận NB/TH/VD), `azota`, `ngan-hang-cau-hoi`, `mathtype-sang-omml` | — |
| 3b. Bản đặc tả + rút đề từ ngân hàng theo ma trận YCCĐ × mức độ | **[TRỐNG]** | `question_bank` đã đủ dữ liệu (12.8k câu, `difficulty`) | grep `đặc tả` → 0; ROADMAP GĐ 5 chưa làm; `de-vat-ly-thpt` sinh câu mới bằng AI chứ không rút từ ngân hàng |
| 3c. Kiểm định đề (mỗi phương án bảo vệ được, distractor có lý do) | **[MỘT PHẦN]** | checklist B7 `de-vat-ly-thpt`, giải ngược Phần III (`azota:97–134`) | Chưa có cổng verify kiểu Gate A/B (k12 CFU): viết lập luận từng lựa chọn, subagent giải mù |
| 4. Xuất bản (Azota / ThachLab / Word) | **[CÓ]** | `azota`, `up-de-kiem-tra`, `dang-de-hang-loat`, `dang-bai-hoc-thachlab`, `build_docx.py` | — |
| 5. Thu kết quả | **[MỘT PHẦN]** | ThachLab tự động (`exam_results`, `exam_question_results`) | Kết quả làm trên **Azota** không có đường nào về LMS hay về phân tích (§2.3 #6) |
| 6. Phân tích | **[MỘT PHẦN]** | Tab Phân tích, mastery, `tutoring_needs`, chữa bài | Không skill đọc DB/Azota export → báo cáo Word/Excel cho tổ CM, phụ huynh, sổ điểm; LMS chỉ xuất CSV thô (§2.3 #5) |
| 7. Điều chỉnh dạy | **[MỘT PHẦN]** | BTVN tự sinh từ câu sai (`services/homework.ts`), phụ đạo theo chủ đề, trình chiếu chữa bài | Không skill phân hoá 3 mức / kế hoạch dạy lại từ dữ liệu; BTVN tự sinh không phân hoá theo mức HS |

### 3.2 Mảng CNC / cơ khí (CĐKT Cao Thắng)

| Khâu | Trạng thái | Cái đã có | Cái còn thiếu (bằng chứng) |
|---|---|---|---|
| 1. Chuẩn đầu ra (ABET/ETAC, CLO ↔ PLO) | **[TRỐNG]** | 10 năng lực tiện/phay hardcode (`services/cnc-competencies.ts`) | `ABET`, `ETAC` = 0 kết quả trong skill + repo; 10 năng lực không ánh xạ tới outcome nào |
| 2. Đề cương học phần / giáo án LT-TH-tích hợp | **[MỘT PHẦN]** | 8 bài `cnc_lessons` đăng qua `/quan-tri/cnc-bai-hoc` (LaTeX editor dùng chung); `latex` có mục phiên âm cơ khí | Không skill soạn đề cương chi tiết / giáo án theo mẫu trường; không bảng giáo án |
| 3. Bài tập / đề / checklist | **[MỘT PHẦN]** | 12 quiz bank (`cnc_key`), checklist, rubric, nộp bản vẽ; `/quan-tri/cnc-dang-de` dán kiểu Azota | Không skill soạn đề CNC (`de-vat-ly-thpt` khoá cứng Vật lí); `up-de-kiem-tra` chỉ đích Lớp→Chương→Bài THPT, không nhận `cnc_key` |
| 4. Xuất bản | **[MỘT PHẦN]** | trang admin `cnc-bai-hoc`, `cnc-video`, `cnc-dang-de` | Không skill nào tự động hoá; làm tay trên web |
| 5. Thu kết quả / điểm danh | **[CÓ]** | `cnc_milling_quiz_attempts`, `checklist_attempts`, `cnc_learning_records`, điểm danh theo máy, roster import/export xlsx; `diem-danh-excel` | — |
| 6. Phân tích / đánh giá đạt chuẩn đầu ra | **[MỘT PHẦN]** | `ClassCompetencyMatrix`, bảng điểm xuất xlsx | Không báo cáo mức đạt theo outcome (ABET Criterion 3/4), không skill |
| 7. Điều chỉnh / cải tiến liên tục | **[TRỐNG]** | — | Không có vòng lặp assessment → action nào (ROADMAP: CNC chỉ sửa lỗi) |
| Chủ nhiệm lớp (SHCN, điểm danh) | **[CÓ]** | `bien-ban-shcn`, `diem-danh-excel`, module SHCN | — |

---

## 4. Đề xuất (chỉ cho khâu TRỐNG / MỘT PHẦN)

Nguyên tắc rút từ k12-teacher-skills (đã đọc): SKILL.md chỉ **route + quy trình**; sư phạm theo
môn nằm ở `references/<môn>.md`; một file nguồn JSON (`shared` + `documents[]`) render ra nhiều Word
để giáo án / phiếu HS / phiếu quan sát không lệch nhau; chuẩn trích nguyên văn **đúng 1 lần**; hỏi
tối đa 1–2 câu; rubric CSV nhị phân bucket P/R/O/M có cột `Conditional`. Áp dụng: **1 skill, 2
reference** (Vật lí THPT / CNC cao đẳng) thay vì tách 2 skill cho cùng khâu.

Thứ tự dưới đây = thứ tự ưu tiên theo tần suất dùng.

### Đ1. `khbd-5512` — Kế hoạch bài dạy theo CV 5512 (skill MỚI) — ưu tiên **RẤT CAO** (hằng tuần)

**Trigger (mô phỏng format hiện có):**
> Soạn Kế hoạch bài dạy (giáo án) theo Công văn 5512/BGDĐT-GDTrH cho một bài Vật lí THPT (GDPT 2018)
> hoặc một bài/mô-đun CNC cao đẳng: mục tiêu (kiến thức – năng lực – phẩm chất) bám YCCĐ, thiết bị,
> tiến trình 4 hoạt động (khởi động / hình thành kiến thức / luyện tập / vận dụng) mỗi hoạt động đủ
> mục tiêu – nội dung – sản phẩm – tổ chức thực hiện, phụ lục phiếu học tập; xuất Word theo mẫu tổ +
> phiếu học tập HS tách riêng. Dùng khi nói "soạn giáo án bài…", "KHBD bài…", "làm giáo án 5512",
> "giáo án tiết…", hoặc đưa tên bài/số tiết. KHÁC `dang-bai-hoc-thachlab` (đăng nội dung lên LMS,
> không phải giáo án) và `de-vat-ly-thpt` (đề, không phải giáo án).

- **Khâu lấp:** VL-2a [TRỐNG], VL-2c [MỘT PHẦN], CNC-2 [MỘT PHẦN]. Bằng chứng: §2.2 dòng 1.
- **Mới hay bổ sung:** **Mới** — không skill nào có cấu trúc 4 hoạt động; nhưng **tái dùng** tối đa:
  lấy `body_html`/`summary_html` của `lesson_items` và đề đã có trong `exam_ids` làm ngữ liệu để giáo
  án khớp với bài trên LMS; lấy YCCĐ từ `question_topics`; render Word bằng skill `docx`.
- **Cấu trúc gợi ý:** `references/vat-li-thpt.md` (mẫu KHBD tổ, cấu trúc theo loại bài: lý thuyết /
  bài tập / thực hành / ôn tập; bảng YCCĐ 10-11-12 trích từ TT32), `references/cnc-cao-dang.md`
  (mẫu giáo án LT/TH/tích hợp của trường, cột năng lực ↔ CLO), `scripts/render_khbd.py` (JSON →
  docx), `evals/rubrics/*.csv`.
- **Dữ liệu thầy cần cung cấp:** (1) PDF Chương trình môn Vật lí TT32/2018 (để trích YCCĐ 3 khối một
  lần thành `references/yccd-vat-li-{10,11,12}.md`, dùng chung cho Đ3); (2) 1–2 KHBD mẫu đã được tổ
  duyệt (.docx) làm mẫu định dạng; (3) phân phối chương trình + bộ sách đang dạy; (4) mẫu giáo án
  LT/TH/tích hợp của Cao Thắng + đề cương học phần CNC.

### Đ2. `phan-tich-ket-qua` — Báo cáo sau kiểm tra & nhận xét (skill MỚI) — ưu tiên **CAO** (sau mỗi bài KT)

**Trigger:**
> Đọc kết quả một (hoặc nhiều) bài kiểm tra — từ ThachLab (RPC `get_class_exam_question_stats`,
> `get_class_topic_matrix`, `student_outcome_gaps`, mastery) hoặc từ file kết quả xuất từ Azota
> (.xlsx/.csv) — rồi lập báo cáo cho giáo viên: phổ điểm, câu sai nhiều kèm phân tích distractor,
> YCCĐ yếu của lớp, danh sách HS cần phụ đạo, đề xuất nội dung tiết chữa bài; xuất Word/Excel theo
> mẫu tổ chuyên môn và nhận xét ngắn từng HS cho phụ huynh/sổ điểm. Với lớp CNC: cùng quy trình
> nhưng gộp theo năng lực/CLO. Dùng khi nói "phân tích kết quả bài…", "lớp này sai câu nào nhiều",
> "báo cáo sau kiểm tra", "nhận xét học sinh", hoặc đính kèm file điểm Azota.

- **Khâu lấp:** VL-5, VL-6 [MỘT PHẦN]; CNC-6 [MỘT PHẦN]. Bằng chứng: §2.2 dòng 2; §2.3 #5 (chỉ CSV
  thô), #6 (không importer Azota).
- **Mới hay bổ sung:** **Mới**. LMS đã có RPC phân tích — skill chỉ *đọc* qua RPC (không thêm
  round-trip mới cho trang HS, đúng quy tắc perf) và không ghi DB. Lưu ý kỹ thuật: REST anon không đọc
  được `exams`/kết quả (RLS) → cần chạy script cục bộ với service-role qua Terminal như
  `upload-lesson.mts` đang làm.
- **Cấu trúc:** `references/vat-li-thpt.md` (mẫu báo cáo tổ, ngưỡng đỏ/vàng đồng bộ với
  `docs/mastery-rules.md` 80/50%), `references/cnc-cao-dang.md` (gộp theo CLO — dùng chung với Đ5),
  `scripts/fetch_results.mts`, `scripts/parse_azota_export.py`, `scripts/render_report.py`.
- **Dữ liệu cần cung cấp:** (1) 1 file kết quả xuất từ Azota mẫu (để viết parser đúng cột thật);
  (2) mẫu báo cáo sau kiểm tra / biên bản rút kinh nghiệm của tổ (nếu có); (3) xác nhận cách cấp
  service-role key cho script (đang dùng cơ chế gõ qua Terminal).

### Đ3. Bổ sung `de-vat-ly-thpt` — bản đặc tả + rút đề từ ngân hàng + cổng kiểm định — ưu tiên **CAO** (mỗi kỳ KT định kỳ)

- **Khâu lấp:** VL-3b [TRỐNG], VL-3c [MỘT PHẦN], VL-1 [MỘT PHẦN]. Bằng chứng: grep `đặc tả` → 0;
  ROADMAP GĐ 5 chưa làm; `de-vat-ly-thpt` không có bước rút câu từ `question_bank`.
- **Mới hay bổ sung:** **Bổ sung** vào skill sẵn có, 3 bước:
  1. **Bước 3b — Bản đặc tả** sau ma trận: mỗi ô = YCCĐ (mã từ `question_topics` + trích nguyên văn
     TT32 đúng 1 lần) × mức độ × số câu × loại câu; dùng file `references/yccd-vat-li-*.md` sinh ở Đ1.
  2. **Bước 3c — Rút đề từ ngân hàng** (tuỳ chọn thay vì AI sinh câu mới): script query
     `question_bank` theo `topic_id` × `difficulty` × `qtype`, chống trùng bằng `content_hash`; cần
     chốt ánh xạ NB/TH/VD ↔ Dễ/TB/Khó (LMS chỉ có 3 mức Dễ/TB/Khó, `difficulty_source` gv/ai).
  3. **Bước 7b — Cổng kiểm định sau khi ghi file** (theo k12 CFU `verification.md`): mỗi phương án
     viết lập luận mạnh nhất → phải chỉ đúng 1; đúng–sai: mỗi ý tính lại số liệu; giao subagent giải
     mù bản HS.
- **Dữ liệu cần cung cấp:** mẫu bản đặc tả tổ/Sở đang dùng (.docx); quyết định ánh xạ 3 mức ↔ 3 mức
  độ; PDF TT32 (dùng chung Đ1).

### Đ4. Bổ sung `skill-creator` / mọi skill nghiệp vụ — rubric eval CSV — ưu tiên **TRUNG BÌNH-CAO** (một lần, lợi cho tất cả)

- **Khâu lấp:** xuyên suốt. Bằng chứng: chỉ `skill-creator` có harness; 12 skill nghiệp vụ không có
  `evals/`, chỉ checklist trong SKILL.md.
- **Mới hay bổ sung:** **Bổ sung**, không tạo skill. Dựng `evals/<skill>/rubrics/shared.csv` +
  `<môn>.csv` tiếng Việt theo đúng cột k12 (`ID, Bucket P/R/O/M, Criterion, What pass requires,
  Notes, Conditional, Source`), ví dụ Conditional `lop-12`, `co-hinh`, `phan-II`, `cnc-thuc-hanh`.
  Tiêu chí tiêu biểu cho bộ đề: "đúng 1 đáp án bảo vệ được", "bảng đáp án khớp lời giải", "nhãn
  YCCĐ có trong danh mục thật", "thân đề không lộ đáp án". Chạy bằng `skill-creator/scripts/run_eval.py`
  có sẵn. Cần tự viết bộ prompt mẫu (k12 cũng không cung cấp).
- **Dữ liệu cần cung cấp:** 3–5 file đề/bài thật làm test case cho mỗi skill.

### Đ5. `chuan-dau-ra-abet` — Ma trận CLO ↔ PLO ↔ ABET/ETAC + đề cương học phần (skill MỚI) — ưu tiên **TRUNG BÌNH** (đợt curriculum hiện tại, sau đó mỗi năm)

**Trigger:**
> Xây/rà soát chuẩn đầu ra học phần (CLO) cho các môn CNC, Công nghệ chế tạo máy: ánh xạ CLO ↔ PLO
> chương trình ↔ Student Outcomes ABET/ETAC (1)–(5), viết performance indicators + rubric đo, lập đề
> cương chi tiết theo mẫu phòng đào tạo, và bảng "assessment plan" (môn nào đo outcome nào, bằng công
> cụ nào, ngưỡng đạt). Dùng khi nói "chuẩn đầu ra môn…", "map CLO sang ABET", "đề cương học phần
> CNC", "syllabus theo ABET", "performance indicator". KHÁC `bien-ban-shcn`/`diem-danh-excel`
> (chủ nhiệm), KHÁC Đ1 (giáo án từng buổi).

- **Khâu lấp:** CNC-1 [TRỐNG], CNC-7 [TRỐNG]; nền cho CNC-6. Bằng chứng: `ABET|ETAC` = 0 ở mọi nơi;
  `services/cnc-competencies.ts` 10 năng lực không có cột outcome.
- **Mới hay bổ sung:** **Mới** (không skill nào gần). Có thể ghi bảng ánh xạ ra
  `references/cnc-outcome-map.md` để Đ1 và Đ2 dùng chung (giáo án CNC ghi CLO; báo cáo CNC gộp theo
  CLO). **Không đề xuất** sửa DB ThachLab ở giai đoạn này (ROADMAP: CNC chỉ sửa lỗi).
- **Dữ liệu cần cung cấp:** (1) bộ tiêu chí ETAC phiên bản đang áp dụng (2025–26 hoặc 2026–27) dạng
  PDF/text; (2) PLO chương trình CĐ CNCTM của trường; (3) đề cương học phần CNC/CNCTM hiện có (.docx);
  (4) mẫu đề cương + mẫu assessment report của phòng đào tạo / ban ABET trường.

### Đ6. `phan-hoa-day-lai` — gói phân hoá 3 mức & kế hoạch dạy lại (skill MỚI, hoặc bước 2 của Đ2) — ưu tiên **TRUNG BÌNH**

**Trigger:**
> Từ kết quả một bài (mục phụ đạo `tutoring_needs`, mastery, hoặc báo cáo của Đ2) sinh gói điều
> chỉnh dạy: kế hoạch tiết chữa bài/dạy lại nhắm YCCĐ yếu, 3 phiếu bài tập phân hoá (chưa đạt / cần
> luyện / nắm vững) cùng ngữ cảnh – khác mức hỗ trợ, rút câu từ `question_bank` theo `difficulty`,
> và phiếu quan sát cho tiết đó. Dùng khi nói "dạy lại phần…", "phân hoá cho lớp…", "làm phiếu cho
> nhóm yếu", "chuẩn bị tiết chữa bài".

- **Khâu lấp:** VL-7 [MỘT PHẦN]. Bằng chứng: `services/homework.ts` tự sinh BTVN 10+20 câu nhưng
  **một bộ cho cả lớp**, không phân hoá; không skill nào có khái niệm 3 mức.
- **Mới hay bổ sung:** ưu tiên làm **bước cuối của Đ2** ("kết quả → gói dạy lại") trước; tách skill
  riêng chỉ khi dùng độc lập nhiều. Mô phỏng 8 quy tắc R1–R8 của k12-lesson-differentiation (giữ
  nguyên phạm vi YCCĐ ở cả mức thấp, scaffold giảm dần, "sửa đổi vô hình" cùng ngữ cảnh).
- **Dữ liệu cần cung cấp:** cách thầy đang chia nhóm phụ đạo hiện nay; mẫu phiếu bài tập nếu có.

### Đ7. Bổ sung `up-de-kiem-tra` — đích CNC (`cnc_key`) — ưu tiên **THẤP-TRUNG BÌNH**

- **Khâu lấp:** CNC-3, CNC-4 [MỘT PHẦN]. Bằng chứng: `up-de-kiem-tra` chỉ nhận Lớp→Chương→Bài;
  `/quan-tri/cnc-dang-de` (`CncExamComposer.tsx`) dùng lại cùng `ExamSection` dán Azota → cùng định
  dạng `de.txt`, chỉ khác đích.
- **Mới hay bổ sung:** **Bổ sung** một nhánh "đích CNC": chọn ngân hàng trong `CNC_QUIZ_BANKS`,
  upsert theo `cnc_key`, bỏ bước nhãn YCCĐ (thay bằng năng lực/CLO từ Đ5 nếu muốn). Không cần skill
  soạn đề CNC riêng: dùng `de-vat-ly-thpt` là sai môn, nên nếu cần *soạn* câu CNC thì thêm
  `references/cnc.md` vào Đ3 sau.
- **Dữ liệu cần cung cấp:** 1–2 đề CNC mẫu (.docx) thầy đang dùng.

### Đ8. `mo-phong-bai-hoc` — nhúng mô phỏng vào bài học — ưu tiên **THẤP** (ROADMAP GĐ 3, Q1/2027)

- **Khâu lấp:** VL-2b mở rộng (mô phỏng tương tác) — §2.3 #4 [MỘT PHẦN rất nhỏ].
- **Nhận định:** đây là việc **dev LMS** hơn là skill giảng dạy; 6 mô hình trong `lib/Physics/*.ts`
  đã có sẵn nhưng là code chết. Khi tới GĐ 3, một skill "từ bài học → chọn mô hình → sinh component
  `next/dynamic` + `LazyErrorBoundary` + nhúng vào `body_html`" là hợp lý. Chưa nên làm bây giờ.
- **Dữ liệu cần cung cấp:** danh sách 5–10 mô phỏng ưu tiên theo bài (khi tới lúc).

### Không đề xuất (đã có, tránh trùng)
- Soạn đề TN 2025 / chuẩn hoá Azota / ngân hàng câu hỏi / MathType → đã có 4 skill (§2.1).
- Đăng bài học, đăng đề đơn lẻ, đăng hàng loạt → đã có 3 skill.
- Chấm tự động, thống kê lớp, mastery, phụ đạo, rank, phụ huynh → LMS đã có (§2.3 #1,2,3,12).
- Biên bản SHCN, điểm danh Zalo → đã có 2 skill.
- Tạo skill + eval → `skill-creator` đã có harness đầy đủ; chỉ thiếu rubric nội dung (Đ4).

### Tóm tắt ưu tiên

| # | Đề xuất | Loại | Khâu | Tần suất dùng |
|---|---|---|---|---|
| Đ1 | `khbd-5512` | mới | VL-2a, VL-2c, CNC-2 | hằng tuần |
| Đ2 | `phan-tich-ket-qua` | mới | VL-5/6, CNC-6 | sau mỗi bài KT |
| Đ3 | bổ sung `de-vat-ly-thpt` (đặc tả, rút ngân hàng, cổng verify) | bổ sung | VL-3b/3c, VL-1 | mỗi kỳ KT |
| Đ4 | rubric eval CSV cho 12 skill | bổ sung | xuyên suốt | một lần |
| Đ5 | `chuan-dau-ra-abet` | mới | CNC-1, CNC-7 | đợt curriculum |
| Đ6 | `phan-hoa-day-lai` (hoặc bước cuối Đ2) | mới/bổ sung | VL-7 | sau chữa bài |
| Đ7 | bổ sung `up-de-kiem-tra` đích CNC | bổ sung | CNC-3/4 | thỉnh thoảng |
| Đ8 | `mo-phong-bai-hoc` | mới, hoãn | VL-2b | Q1/2027 |

Dữ liệu cần thầy gửi trước khi duyệt làm Đ1–Đ3 (dùng chung): **PDF TT32/2018 môn Vật lí**, **1–2
KHBD mẫu tổ đã duyệt**, **1 file kết quả Azota xuất mẫu**, **mẫu bản đặc tả đang dùng**.

---

## 5. Phát hiện phụ trong lúc khảo sát (không phải đề xuất skill)

**Đã xử lý 29/09/2026:** đồng bộ 2 chiều `latex` (script OMML plugin → Codex, dòng lưu deliverable Codex → plugin) và `ngan-hang-cau-hoi` (`xuat_thachlab.py` bản mới Codex → plugin, `build_thachlab.py` plugin → Codex), hai thư mục giờ giống hệt; viết lại `docs/ANALYTICS-SETUP.md`; sửa dòng region `docs/STATE.md`; xoá `lib/Physics/*` (tsc sạch); ghi 8 đề xuất vào `docs/ROADMAP.md`. Các dòng dưới giữ làm log.

- **Bản Codex lạc hậu so với plugin:** `latex/scripts/docx_extract.py` plugin có thêm đọc OMML
  (`_omml_text`), Codex chưa có; `ngan-hang-cau-hoi` plugin có thêm `build_thachlab.py` và bước
  EMF/WMF→PNG trong `xuat_thachlab.py`. `azota`, `dang-bai-hoc-thachlab` giống hệt. Cần sync Codex ←
  plugin theo quy tắc memory `feedback_skill_two_copies`.
- **Docs cũ:** `docs/ANALYTICS-SETUP.md` còn mô tả nhập tay câu sai, trong khi `ExamRunner.tsx:226–229`
  đã tự ghi; `docs/STATE.md:7` ghi region Sydney trong khi đã chuyển Singapore 28/9;
  `docs/MANIFESTO.md`, `docs/PROJECT.md` rỗng.
- **Code chết:** `lib/Physics/{electricField,harmonicMotion,magneticField,pendulum,projectileMotion,waves}.ts`
  không được import ở đâu.
- **k12-teacher-skills** không có bộ prompt test hay harness, chỉ rubric CSV + system prompt
  LLM-as-judge; `k12-lesson-prep` chỉ 17 dòng (một đoạn văn hành vi hội thoại) — kiểu skill "đồng
  hành nội hoá bài trước khi dạy" này chưa có trong bộ của thầy nhưng tần suất dùng thấp nên không
  xếp vào đề xuất chính.
