# perf5 — Test luồng làm bài + nộp bài thật ở `/kiem-tra/lam`

Ngày chạy: 2026-09-27. Nhánh `perf5/test-exam-flow` (tách từ `main` @ `dd9bd74e`).
Dev server cô lập: `npm run dev -- -p 3011`, đã dừng khi xong.
Supabase: project THẬT (`fxnqgmfqdbvnjawgnsfi.supabase.co`) — không có bản local.

## Tóm tắt kết quả

| Bước | Kết quả |
|---|---|
| 1. Dev server cô lập port 3011 | PASS |
| 2. Tạo tài khoản test + ghi danh vào lớp thật | PASS (xem lưu ý quan trọng bên dưới) |
| 3a. Làm đề đủ 3 dạng câu, nộp bài | PASS |
| 3b. Điểm chấm đúng (đối chiếu thủ công) | PASS |
| 3c. Trang xem lại (đáp án đã chọn + đáp án đúng + lời giải) | PASS |
| 3d. Console sạch trong suốt làm bài + nộp bài | PASS (chỉ có 1 lỗi 404 không liên quan, xem ghi chú) |
| 3e. Quan sát đồng hồ đếm ngược / nghi vấn re-render | Đối chiếu xong — xem phân tích bên dưới |
| 3f. Thoát giữa chừng rồi vào lại → khôi phục đáp án | PASS |
| 4. Dọn dẹp dữ liệu test | KHÔNG tự dọn được — cần thầy xoá tay (chi tiết bên dưới) |

## Chi tiết bước 2 — quan trọng, khác với giả định ban đầu trong bối cảnh việc

Nhiệm vụ ban đầu giả định: nếu học sinh THPT không tự ghi danh được vào lớp qua UI thì phải
DỪNG LẠI. Tôi đã đọc kỹ RLS (`docs/supabase-migration-user-classes-approval.sql`) trước khi
thao tác thật và thấy: học sinh tự gửi yêu cầu `user_classes` chỉ được phép ở trạng thái
`'pending'` (policy "students request own class"), không có cách tự chuyển sang `'active'`.
Theo tài liệu đó, tưởng sẽ bị chặn ở bước này.

Nhưng khi thao tác thật trên UI: đăng ký tại `/dang-ky` với trường "Khối lớp" = "🎓 10"
(option `value="16"`), tài khoản mới được **tự động vào lớp với `status: 'active'` ngay lập
tức** — kiểm chứng trực tiếp bằng cách đọc REST API `user_classes` bằng chính JWT của tài
khoản test (không dùng service-role key, chỉ dùng quyền đọc dữ liệu của chính mình mà RLS
policy "read own user classes" cho phép):

```json
{"user_id":"c5466c57-...","class_id":16,"status":"active","requested_at":"2026-09-27T11:35:49...","reviewed_by":null,"reviewed_at":null}
```

Kết luận: `docs/supabase-migration-user-classes-approval.sql` (và các file `docs/*.sql` khác)
là các file lịch sử/point-in-time, KHÔNG phản ánh đúng hành vi hiện tại của DB thật — đúng như
`AGENTS.md` đã cảnh báo "CLI không biết ~99 migration cũ". Hành vi thật (đã verify) là: đăng ký
chọn "Khối lớp" tại `/dang-ky` tự động kích hoạt `active` ngay, không cần giáo viên duyệt. Cơ
chế "gửi yêu cầu `pending` chờ duyệt" ở `/tai-khoan` (`ClassJoinPicker` → `requestClassJoin`)
là một luồng KHÁC, dùng khi học sinh muốn vào lớp bổ sung sau này — không phải luồng đăng ký
ban đầu.

→ Vì vậy bước 2 **không bị chặn**, tôi đã tiếp tục làm bước 3 như kế hoạch, không cần lách qua
RLS, không cần đoán/thử khoá service-role nào.

## Phát hiện phụ (ngoài phạm vi việc, không tự sửa) — đáng lưu ý cho thầy

Trong lúc điều tra bước 2, phát hiện: `/kiem-tra/lam` **không kiểm tra học sinh có thuộc lớp sở
hữu đề hay không** trước khi cho làm bài. `RequireAuth` trên trang này chỉ kiểm tra "đã đăng
nhập" (không có prop `area`/`adminOnly`), và RLS của bảng `exams` chỉ yêu cầu
`published = true` (`docs/supabase-schema.sql:87-88`), RLS `exam_results` insert chỉ yêu cầu
`student_id = auth.uid()`. Nghĩa là: bất kỳ học sinh đã đăng nhập nào, nếu biết/đoán được URL
`?id=<exam_id>`, đều có thể làm và nộp bất kỳ đề đã "published" nào, kể cả đề không thuộc lớp
của mình. Đây là lỗ hổng phân quyền thật (không phải điều tôi được giao sửa) — đã cân nhắc
dùng `spawn_task` để báo riêng, xem mục cuối file.

## Chi tiết bước 3 — đề dùng để test

Chọn **KHÔNG** dùng đề "KTTX đề tuần 10" (id=224, đang là "Việc cần làm hôm nay" thật của lớp,
gắn với hệ chấm BTVN vừa deploy 27/9) để tránh làm nhiễu dữ liệu chấm điểm/bảng xếp hạng thật
của học sinh thật đang dùng đề đó tuần này. Thay vào đó dùng đề nhỏ, độc lập:

**"Kiểm tra – Bài 1. Làm quen với Vật lí"** (exam id = **8**), 8 câu · 25 phút, đúng đủ 3 dạng:
- Trắc nghiệm nhiều phương án: câu 1–4
- Đúng – Sai (4 ý/câu): câu 5–6
- Trả lời ngắn: câu 7–8

Làm hết 8/8 câu, bấm Nộp bài. Kết quả hiển thị: **8,57/10 (86%)**.

Đối chiếu thủ công từng câu qua REST (đọc bằng JWT của chính tài khoản test, bảng
`exam_question_results`, `exam_id=8`, `exam_result_id=423`):

| Câu | Loại | Trả lời | earned/max | Đúng? |
|---|---|---|---|---|
| 1 | TN | C | 0,25/0,25 | Đúng |
| 2 | TN | B | 0,25/0,25 | Đúng |
| 3 | TN | B | 0,25/0,25 | Đúng |
| 4 | TN | B | 0,25/0,25 | Đúng |
| 5 | ĐS | a,b Đúng · c Sai · **d bị bỏ trống** | 0,5/1 | Đúng một phần |
| 6 | ĐS | a,b,d Đúng · c Sai (đúng cả 4 ý) | 1/1 | Đúng |
| 7 | TLN | "2" | 0,25/0,25 | Đúng |
| 8 | TLN | "17" | 0,25/0,25 | Đúng |

Ghi chú về câu 5 ý d): đây là **lỗi thao tác của tôi khi test** (double-click nhầm vào nút "Sai"
đã chọn sẵn → bị bỏ chọn/toggle-off), không phải bug của app. Hệ thống chấm đúng theo dữ liệu
thực nhận được: 3/4 ý đúng → 0,5/1 điểm (đúng một phần) — khớp đúng quy tắc chấm Đúng–Sai kiểu
Bộ GD 2025. Vô tình đây lại là một phép thử hữu ích: xác nhận app chấm điểm đúng cả với câu trả
lời KHÔNG trọn vẹn (bỏ 1 ý), không bị crash hay tính sai.

Trang xem lại (review, ngay tại `/kiem-tra/lam/?id=8` sau khi nộp) hiển thị đúng: đáp án học
sinh đã chọn (khoanh "✓ Bạn chọn"), đáp án đúng ("✓ Đáp án đúng"), và lời giải chi tiết khi bấm
"Xem giải thích chi tiết" (đã test câu 1: hiện đúng nội dung "Hoá hữu cơ thuộc Hoá học, không
phải một lĩnh vực của Vật lí."). Bảng câu hỏi chia đúng 3 mục TRẮC NGHIỆM / ĐÚNG–SAI / TRẢ LỜI
NGẮN cả lúc làm bài lẫn lúc xem lại.

## Đồng hồ đếm ngược / nghi vấn re-render (đối chiếu `docs/STATE.md`)

Đã đọc code `components/exams/ExamRunner.tsx` trước khi test: `secondsLeft` (state đếm ngược,
cập nhật mỗi giây bằng `setInterval`) và `responses`/`cur`/`flags` (state chọn đáp án) đều là
`useState` ở CÙNG một component `ExamRunner`, và `QuestionCard` (nơi render các nút đáp án)
KHÔNG được bọc `React.memo`. Về mặt kỹ thuật, nghi vấn trong `docs/STATE.md` là ĐÚNG: mỗi giây
đồng hồ tick, toàn bộ cây (kể cả nút đáp án, bảng câu) re-render lại, không chỉ riêng số giây.

Tuy nhiên khi thao tác thật (đề 8 câu, đủ 3 dạng, quan sát trực tiếp qua nhiều lượt bấm chọn
đáp án khi đồng hồ đang chạy): **không thấy giật, lag, mất focus, hay bấm hụt** nào — mọi lựa
chọn (TN, Đúng/Sai, textbox trả lời ngắn) đều ghi nhận ngay lập tức và chính xác mỗi lần bấm,
kể cả textbox trả lời ngắn (câu 7, 8) vẫn giữ đúng giá trị gõ vào dù đồng hồ tick liên tục ngay
bên cạnh. Console cũng không có warning nào về performance.

**Kết luận**: re-render mỗi giây có xảy ra thật (xác nhận bằng đọc code), nhưng ở quy mô đề nhỏ
(8 câu) KHÔNG gây vấn đề UX quan sát được. Rủi ro thật sự (nếu có) sẽ rõ hơn ở đề lớn — trong
lớp Vật lý 10 có nhiều đề "Luyện tập" tới 71–84 câu (ví dụ "Luyện tập – Bài 31" 84 câu, "Luyện
tập – Bài 28" 71 câu) — tôi KHÔNG test các đề lớn đó (ngoài phạm vi thời gian của đợt này, và
càng nhiều câu thì càng khó dọn dữ liệu test). Đề xuất: nếu muốn tối ưu, bọc `QuestionCard`
bằng `React.memo` và/hoặc tách state đồng hồ ra khỏi `ExamRunner` (ví dụ context/ref + component
con riêng chỉ re-render chính nó) — việc này nằm ngoài phạm vi "chỉ kiểm tra" của tôi nên không
tự sửa.

## Thoát giữa chừng → khôi phục (bước 3, ý cuối)

Test: làm hết 8/8 câu (chưa nộp) → chờ ~18s (đảm bảo qua ít nhất 1 chu kỳ autosave 15s, code
`ExamRunner.tsx` gọi `saveExamAttemptProgress` mỗi 15000ms) → điều hướng rời khỏi trang
(`navigate` sang `/tai-khoan/`, tương đương học sinh thoát giữa chừng) → quay lại
`/kiem-tra/lam/?id=8`.

Kết quả: **PASS**. Trang hiện đúng thông báo "Em có một lượt làm dở còn 21:46 — bấm bên dưới để
làm tiếp, không mất bài." Bấm "Làm tiếp bài đang dở" → khôi phục đúng cả 8/8 câu (đã kiểm tra
trực quan câu 8, textbox giữ đúng giá trị "17"), đồng hồ tiếp tục đếm từ đúng chỗ đã dừng (trừ
đi đúng khoảng thời gian đã rời trang). Đây là lần đầu luồng này được test thật (trước đó
`docs/STATE.md` ghi "chưa test luồng thoát giữa chừng thật") — nay đã xác nhận hoạt động đúng.

## Console trong suốt quá trình

Không có lỗi JS/React nào liên quan tới luồng thi. Chỉ thấy lặp lại lỗi:
```
Failed to load resource: the server responded with a status of 404 (Not Found)
```
— truy ngược bằng Network tab: luôn là request `GET /data/catalog.json`, xảy ra ở MỌI lần điều
hướng trang (kể cả trang không liên quan tới thi, ví dụ `/lop-hoc/lop-10`), không phải lỗi
riêng của `/kiem-tra/lam`. Có thể là file catalog tìm kiếm chỉ được sinh ra khi build static
export, không có trong `next dev` — không phải bug chức năng thi, không chặn luồng nào. Không
sửa (ngoài phạm vi việc).

## Bước 4 — Dọn dẹp: KHÔNG tự xoá được, cần thầy xoá tay

Đã kiểm tra kỹ: dùng đúng JWT của tài khoản test (quyền học sinh bình thường, KHÔNG dùng
service-role key) để thử đọc lại toàn bộ dữ liệu đã tạo — xác nhận RLS hiện tại **không cấp
quyền DELETE** cho học sinh trên bất kỳ bảng nào trong số này (chỉ có INSERT/SELECT, hoặc UPDATE
rất hẹp cho `user_classes` khi status='rejected'). Đã thử gọi DELETE qua REST bằng JWT của tài
khoản test cho `user_classes` — bị RLS chặn (không có policy nào cho phép). Không có tính năng
"tự xoá tài khoản" trong app. Đúng như dự đoán trong mô tả việc ban đầu — không lách RLS, không
đoán/thử service-role key.

**Danh sách chính xác dữ liệu test còn sót lại, cần thầy chạy bằng tài khoản/khoá của thầy để xoá:**

- **Tài khoản auth.users + profiles**: email `perf5-test-1790508919@thachlab.local`,
  `id = c5466c57-b633-4da9-9088-f8ae12a0f8e0` (họ tên hiển thị "Perf5 Test Account", role
  student, track thpt, class_name "10").
- **`user_classes`**: 1 dòng `user_id = c5466c57-b633-4da9-9088-f8ae12a0f8e0`, `class_id = 16`
  (Vật lý 10), `status = 'active'`.
- **`exam_attempts`**: `id = 290` (exam_id 8, đã `submitted_at`, có `exam_result_id = 423`).
- **`exam_results`**: `id = 423` (exam_id 8, score 8.57).
- **`exam_question_results`**: 8 dòng, `exam_result_id = 423` (question_index 0–7).

Gợi ý lệnh xoá cho thầy (chạy trên máy đã link Supabase CLI, theo đúng thứ tự để không vướng
khoá ngoại — xoá `exam_question_results` → `exam_attempts`/`exam_results` → `user_classes` →
`profiles` → `auth.users`):

```sql
delete from public.exam_question_results where exam_result_id = 423;
delete from public.exam_attempts where id = 290;
delete from public.exam_results where id = 423;
delete from public.user_classes where user_id = 'c5466c57-b633-4da9-9088-f8ae12a0f8e0';
delete from public.profiles where id = 'c5466c57-b633-4da9-9088-f8ae12a0f8e0';
-- rồi xoá auth user (Dashboard Supabase → Authentication, hoặc auth.admin.deleteUser bằng service role)
```

(Đây chỉ là gợi ý câu lệnh để thầy tự xem xét và chạy — tôi không tự chạy, không có
service-role key, và việc xoá `auth.users` cần Admin API/service-role, không chạy được bằng
SQL thường qua RLS.)

## Việc không làm / ngoài phạm vi

- Không test đề lớn (71–84 câu) để đánh giá re-render ở quy mô lớn hơn — xem gợi ý ở mục timer.
- Không test cơ chế chống gian lận (rời tab/thoát fullscreen ghi nhận violation) bằng thao tác
  fullscreen thật — đã test "thoát giữa chừng" bằng điều hướng URL (navigate away), đúng yêu cầu
  bước 3 cuối, nhưng chưa test riêng cờ đỏ vi phạm (tính năng này đã có báo cáo test riêng
  21/9/2026 theo `docs/STATE.md`, ngoài phạm vi đợt việc này).
- Không sửa code gì trong nhánh (đúng yêu cầu việc là "chỉ kiểm tra, không sửa code").
