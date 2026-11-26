# Lộ trình học Vật lí kiểu Duolingo — bản thiết kế (26/11/2026, chờ thầy chốt)

Phạm vi: **lý thuyết + bài tập cơ bản** (Nhận biết/Thông hiểu, vận dụng 1 bước). Không thay trang bài
`/lop-hoc/bai` mà thêm **một con đường** đi xuyên qua nó, dành cho lúc HS tự học ở nhà trên điện thoại.

## 0. Tư vấn trước khi làm (theo nghiên cứu sẵn trong repo)

- **Hợp:** phiên ngắn có điểm kết (N5 segmenting, L2 goal-gradient), kiểm tra ngay sau học (L1 testing effect),
  ôn giãn cách (đã có `on_tap_the`), một nút "Học tiếp" duy nhất (L5 Zeigarnik), ví dụ mẫu mờ dần (N6).
- **Ngược — KHÔNG chép từ Duolingo:** *tim/mạng* (phạt sai → HS 14–18 né thử, mà sai rồi sửa mới là chỗ học);
  *chuỗi ngày* bắt buộc (G2: não vị thành niên nhạy thưởng, mất chuỗi = bỏ hẳn); *bảng xếp hạng tuần*
  (Hanus & Fox 2015, L3 — đã có rank RP, không thêm lớp thưởng mới trước khi đo mùa 1, xem
  `DE-XUAT-NGHIEN-CUU-HS-14-22` mục 4); *hoạt hình ăn mừng giữa bài* (L3, L6).
- **Điều chỉnh nhỏ:** chuỗi **tuần** (≥3 ngày/tuần, ngày nghỉ tự do), dùng lại RP thay vì thêm XP, câu sai quay
  lại cuối lượt 1 lần thay cho tim, không khoá cứng bài (lớp còn học theo lịch thầy) mà có "Kiểm tra vượt".
- **Đo:** thử 1 chương ở 2 lớp, so tỉ lệ đi hết chặng, % thẻ ôn đúng hạn sau 7 ngày, nhãn mastery YCCĐ trước/sau,
  với chương liền trước của cùng lớp (mục 7).

## 1. Ý tưởng chính: lắp ráp, không xây mới

Gần như mọi mảnh Duolingo đã có trong thachlab; thứ còn thiếu là **bản đồ + nhịp phiên 5–8 phút** nối chúng lại.

| Duolingo | Đã có ở thachlab | Còn thiếu |
|---|---|---|
| Bài học ngắn 10 câu | Hộp `.tl-quiz` sau từng mục, Kiểm tra nhanh 20 câu | Cắt lý thuyết thành phiên 5–8 phút có điểm kết |
| Ôn giãn cách, bài "nứt" | Ôn 5 phút `OnNamPhut` + `on_tap_den_han` (bậc 1/3/7/21/60 ngày) | Hiện "đến hạn" ngay trên bản đồ |
| Luyện vô hạn | `VariantPractice` (sinh câu đổi số), `SimilarBankPractice` (câu cùng dạng) | Lượt luyện cơ bản lọc câu **Dễ** |
| Vương miện/cấp độ | Mastery YCCĐ ✅🟡🔴 (`get_lesson_mastery`) | Gắn nhãn vào nút bài trên bản đồ |
| Gợi ý giảm dần | `StepwiseSolution` có `fading` | Mức fading theo lần thứ mấy HS làm |
| XP, giải đấu | Rank RP theo mùa, danh hiệu | **Không thêm** |
| Kiểm tra nhảy cóc | Kiểm tra nhanh 20 câu, ngưỡng % | Dùng nó làm "Kiểm tra vượt" |

## 2. Cấu trúc con đường

```
Lớp ─ Chương (= 1 "khu") ─ Bài (= 1 cụm nút) ─ 5 nút ─ mỗi nút = 1 phiên 5–8 phút
```

Mỗi **bài** có 5 nút, đi theo thứ tự (gợi ý, không khoá):

| # | Nút | Nội dung | Nguồn | Xong khi |
|---|---|---|---|---|
| 1 | 📖 **Hiểu** (1–3 phiên) | Một mốc lý thuyết I/II/III: tình huống/dự đoán → đoạn ngắn + hình → 2–3 câu `.tl-quiz` | `theory.html` cắt theo `wrapTheorySections` | trả lời hết câu kiểm tra của mốc |
| 2 | 🧠 **Nhớ** | Lượt đầu thẻ lật của bài (gõ chữ khoá trước khi lật) | `content/on-tap/<slug>.json` | hết lượt, lịch ôn bắt đầu |
| 3 | 🧮 **Xem mẫu** | 1 dạng bài tập mẫu cơ bản, tự giải từng bước, fading mức 1 | Bài tập mẫu + `StepwiseSolution` | tới Đáp số |
| 4 | ✏️ **Luyện** | 8 câu cơ bản: câu Dễ theo YCCĐ của bài + câu đổi số của dạng vừa xem | `question_bank` (difficulty=Dễ), `bien_the` | ≥6/8 đúng (sai thì câu quay lại 1 lần) |
| 5 | 🏁 **Chốt bài** | Kiểm tra nhanh của bài | đề Kiểm tra nhanh sẵn có | ≥ `quiz_min_correct` |

Cuối mỗi **chương** thêm 1 nút 🏆 **Ôn chương** (trộn thẻ + câu Dễ/TB các bài, cùng đề Kiểm tra nhanh mà Ôn tập theo
chặng đang dùng) và, nếu có, nút sơ đồ tư duy chương.

**Nút ôn đến hạn:** bài đã chốt mà có thẻ `han_on ≤ hôm nay` → nút bài mờ đi + nhãn "Ôn 3 phút". Chạm = lượt
`OnNamPhut` chỉ các thẻ đến hạn. Đây là phần "Duolingo" giá trị nhất (Ebbinghaus/Cepeda 2006) và đã có sẵn DB.

**Kiểm tra vượt:** ở đầu mỗi bài chưa học, nút phụ "Đã biết bài này?" → làm Kiểm tra nhanh; đạt ngưỡng thì 5 nút
tự xong, thẻ ôn vào bậc 2. Giữ HS khá không phải đi chậm (Kalyuga 2003, expertise reversal).

## 3. Một phiên (5–8 phút) trông thế nào

Màn hình ở 375px, mỗi bước một màn (N1), nút chính ở đáy (D3):

1. Thanh tiến độ phiên (bước 3/10), nút ✕ ở góc trên trái — không đồng hồ.
2. Màn nội dung **hoặc** màn câu hỏi, không trộn hai thứ trên một màn.
3. Câu hỏi giữ nhãn đề thật (E1–E3): A. B. C. D. · a) b) c) d) Đúng/Sai · ô đáp số `inputmode="decimal"`.
4. Bấm "Kiểm tra" → phản hồi ngay ở dải đáy: đúng = 1 dòng vì sao; sai = vì sao sai + "Xem lại đoạn này"
   (dùng neo `theory-sec-*` sẵn có) (L1, L4). Câu sai quay lại cuối phiên **1 lần** (như `OnNamPhut`).
5. Màn kết: số câu đúng, RP nhận (nếu bài tính RP), lịch ôn kế tiếp, nút **"Học tiếp"** trỏ nút kế. Phần thưởng
   chỉ ở đây (L3).

**Dạng câu cho bài tập cơ bản** (chỉ dạng đề thi có hoặc tập kỹ năng nền):
chọn A–D · Đúng/Sai · điền đáp số · **ghép đại lượng ↔ đơn vị ↔ kí hiệu** · **chọn công thức đúng để tính X** ·
**đổi đơn vị** · **đọc đồ thị/hình** (chạm vào điểm) · **sắp thứ tự bước giải** (từ `buoc[]` bài tập mẫu).
Ba dạng in đậm là mới, sinh tự động được từ dữ liệu sẵn (bảng công thức bài, `bien_the`, `buoc[]`) — không cần soạn tay.

## 4. Bản đồ (`/lop-hoc/lo-trinh?chuong=<id>`)

- Một cột nút zigzag dọc, mỗi bài một cụm 5 nút nhỏ + tên bài; chương là tiêu đề dính đầu.
- Trạng thái nút: chưa học (viền) · đang tới (đặc, màu nhấn duy nhất — Von Restorff, N7) · xong (✓) · đến hạn ôn (mờ +
  "Ôn 3 phút"). Không nhấp nháy/nảy (G2); chỉ một nút nổi.
- Nhãn mastery YCCĐ ✅🟡🔴 đặt cạnh tên bài, không trên từng nút (N4).
- Đáy cố định: **"Học tiếp: <tên nút>"** (L5). Trang chủ HS và `ContinueLearningCard` trỏ về đây.
- Chuỗi tuần: một dòng nhỏ ở đầu "Tuần này: 2/3 ngày" — không ngọn lửa, không cảnh báo mất chuỗi.
- Bản đồ đi theo **chương thầy đang dạy** (lịch dạy đã có trong `/lich-tuan`), mặc định mở đúng chương đó.

## 5. Dữ liệu

Phần lớn trạng thái suy ra được từ bảng có sẵn: thẻ ôn (`on_tap_the`), lượt luyện (`practice_question_results`),
kiểm tra (`exam_results`), mastery. Chỉ cần thêm:

- Bảng `lo_trinh_buoc` (user_id, lesson_id, nut smallint 1–5, phien smallint, xong_luc, dung smallint, tong smallint),
  khoá (user_id, lesson_id, nut, phien); RLS bật, revoke anon/authenticated, chỉ đi qua RPC.
- RPC gộp `lo_trinh_chuong(p_chapter)` → trạng thái mọi nút + số thẻ đến hạn + mastery + chuỗi tuần trong **một**
  lượt gọi (quy tắc không thêm round-trip). RPC `lo_trinh_ghi(p_lesson, p_nut, p_phien, p_dung, p_tong)`.
- Nội dung phiên dựng **tĩnh lúc build** từ `theory.html`/`bundle.json`/`on-tap/*.json` (không thêm truy vấn); chỉ nút
  Luyện bốc câu Dễ từ `question_bank` qua 1 RPC.
- Khách chưa đăng nhập: tiến độ lưu localStorage như `OnNamPhut`.

## 6. Điều kiện nội dung (đo trước khi code)

- Mỗi bài cần **≥15 câu Dễ** gắn YCCĐ trong `question_bank` để nút Luyện không lặp câu. Chạy 1 SQL đếm theo bài
  (chỉ đọc) trước; bài thiếu thì bù bằng câu đổi số `bien_the` hoặc gắn mức độ còn thiếu bằng
  `backfill-question-bank-difficulty.mts`.
- Mốc lý thuyết phải ≤ ~600 chữ để vừa phiên 5–8 phút (hạn mức ở `PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`); mốc dài
  hơn thì nút Hiểu tách 2 phiên tại `<h4>`, không sửa bài.
- Đếm bài đã có thẻ ôn (81 bài có `content/on-tap/*.json`) và bài tập mẫu có `bien_the`.

## 7. Thử và đo

- **Chương thử:** một chương đang dạy, đủ 3 điều kiện mục 6 — đề xuất **L10 Ch.2 Động học** hoặc chương L11 đang dạy.
- **Đo (2 lớp, 3 tuần):** % HS mở bản đồ ≥1 lần/tuần · % nút hoàn thành, nút nào HS bỏ giữa chừng (phễu) · % thẻ ôn
  được ôn trong 2 ngày sau hạn · nhãn mastery YCCĐ của chương thử so với chương trước · điểm Kiểm tra nhanh lần đầu.
- **Ngưỡng giữ:** ≥40% HS dùng đều 3 tuần và mastery không thấp hơn chương trước → mở cho mọi chương.

## 8. Các bước làm (sau khi thầy chốt)

| GĐ | Việc | Công | Migration |
|---|---|---|---|
| 0 | SQL đếm câu Dễ/bài, thẻ ôn, `bien_the` cho chương thử | 0,5 ngày | không |
| 1 | Bản đồ chỉ đọc từ dữ liệu sẵn có (thẻ đến hạn, mastery, kiểm tra) + nút Học tiếp | 1 ngày | không |
| 2 | Trình chạy phiên 10 bước: nút Hiểu (cắt mốc), Nhớ, Xem mẫu, Chốt bài — tái dùng component sẵn | 2 ngày | không |
| 3 | Nút Luyện (câu Dễ + đổi số) + 3 dạng câu mới + bảng `lo_trinh_buoc` + RPC gộp | 2 ngày | có |
| 4 | Kiểm tra vượt, chuỗi tuần, Ôn chương | 1 ngày | không |
| 5 | Thử 3 tuần, đo, quyết mở rộng | — | — |

## 9. Thầy cần chốt

1. Đồng ý **không** có tim / chuỗi ngày / bảng xếp hạng tuần, dùng lại RP?
2. Khoá mềm (gợi ý thứ tự + Kiểm tra vượt) hay khoá cứng bài sau đến khi chốt bài trước?
3. Chương thử nào, lớp nào?
4. Nút Luyện chỉ câu Dễ, hay Dễ + một ít Trung bình ở cuối lượt?
