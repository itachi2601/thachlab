# ROADMAP ThachLab (cập nhật 28/09/2026 — bản đối chiếu mã nguồn + hệ động lực)

Triết lý: **"Cho hết kiến thức. Bán sự đồng hành."**
Khác biệt: *Hệ thống biết học sinh đang yếu ở đâu và biết đưa học sinh đi đâu tiếp theo.*

Thay đổi lớn so với bản 23/09: **yêu cầu cần đạt (YCCĐ) không còn là nhãn khô để xem, mà là
đơn vị chơi.** Mỗi YCCĐ/chủ đề đã quy đổi thành một danh hiệu chuyên môn 3 mức; bộ huy hiệu của
mỗi lớp chính là bản đồ hành trình học tập; YCCĐ không đạt rơi xuống kênh phụ đạo và tự thoát
bằng bài kiểm tra. Learning Journey vì thế không còn là "trang mới cần làm" mà là **hoàn thiện
vòng lặp đã có**.

Quy ước mức độ câu hỏi: **Dễ / Trung bình / Khó** (đã có cột `difficulty`, backfill bằng AI).

---

## Vòng lặp cốt lõi (đã chạy thật từ 21/09/2026, mùa thử nghiệm tới 25/10)

```
Học bài → làm đề / luyện tập → chấm từng câu theo YCCĐ + mức độ
   ├─ đạt   → RP, bậc mùa, danh hiệu chuyên môn (Thức Tỉnh = đủ câu Dễ,
   │           Làm Chủ = đủ câu TB, Huyền Thoại = đủ câu Khó), huy hiệu đeo dưới tên,
   │           khung sưu tập, bảng tuần lớp, vinh danh công khai, chuỗi ngày
   └─ hụt   → tutoring_needs (sai ≥50% ở 2 bài gần nhất) → "Chủ đề cần phụ đạo"
               ├─ đăng ký buổi phụ đạo với trợ giảng (tính vào lương TA)
               └─ tự ôn rồi làm 20 câu đúng chủ đề, ≥80% thì tự thoát (tối đa 3 lượt)
```

Đã có (21–28/09): rank RP 7 bậc theo mùa; 32 danh hiệu chuyên môn × 3 mức (96 huy hiệu) + 13
bộ sưu tập/thành tích; Vô Song trên Chí Tôn; nhiệm vụ ngày + chuỗi ngày; bảng tuần của lớp;
vinh danh tuần trang chủ; danh hiệu đeo + khung sưu tập; lộ trình huy hiệu gợi ý theo lớp
10/11/12 (đang hoàn thiện ở phiên song song); nhãn Nắm vững / Cần luyện thêm / Chưa đạt theo
YCCĐ; thoát phụ đạo bằng tự kiểm tra; chấm BTVN.

**Chưa có: bằng chứng.** Toàn bộ hệ động lực chưa được test bằng tài khoản học sinh thật và
chưa đo được có làm các em học nhiều hơn không. Đây là việc số 1.

---

## Giai đoạn 0 — Nền dữ liệu ✅ (xong 25/09/2026)
Khung kỹ năng `question_topics` + YCCĐ con; câu hỏi gắn Chủ đề + Dạng + mức độ khi đăng đề;
dữ liệu làm bài từng câu; native quiz 3 dạng; retention gộp kết quả > 12 tháng.

## Giai đoạn 1 — Đo và chỉnh vòng lặp động lực (10/2026, hết mùa thử nghiệm 25/10)
Nguyên tắc: **không thêm lớp động lực mới** (danh hiệu, thành tích, bảng) cho tới khi có số
liệu mùa 1. Chỉ sửa cái đang có.
- [ ] Test toàn bộ luồng bằng 2–3 tài khoản HS thật (mobile 375px): nhận danh hiệu, đeo, khung
      sưu tập, bảng tuần, rơi vào phụ đạo, thoát phụ đạo.
- [ ] Đo mùa 1 (21/09–25/10) so với 4 tuần trước 21/09: số HS làm bài mỗi tuần, số bài/HS,
      % HS nhận ≥1 danh hiệu trong 2 tuần đầu, % HS còn làm bài ở tuần 4–5 (độ rơi), số HS
      trong "cần phụ đạo" và tỉ lệ thoát bằng tự kiểm tra vs bằng buổi học.
- [ ] Rà **độ phủ ngân hàng theo danh hiệu**: mỗi danh hiệu có đủ câu Dễ/TB/Khó để đạt được
      `min_de/min_tb/min_kho` không. Danh hiệu không thể đạt vì thiếu câu → tắt hoặc hạ ngưỡng,
      không để HS đuổi theo mục tiêu rỗng.
- [ ] Chống cày: điều kiện danh hiệu đếm **câu khác nhau** giải đúng, không đếm lượt làm lại
      cùng câu; RP mỗi bài chỉ tính lượt đầu hoặc lượt tốt nhất.
- [ ] Trang Luyện tập lọc theo lớp / chương / bài / YCCĐ / mức độ — đây là đường để HS chủ động
      "săn" danh hiệu còn thiếu, hiện chưa có.
- [ ] Mở "3 kỹ năng yếu nhất" cho HS (dữ liệu đã có ở tab Phụ đạo GV).
- [ ] Đăng nốt ~300 đề thi thử theo quy tắc script-trước-agent-sau (skill `dang-de-hang-loat`).

## Giai đoạn 1b — Để TẤT CẢ cùng tiến bộ (thầy chốt 28/09/2026, làm ngay khi có hạn mức — dự kiến từ 02/10)
Căn cứ: thuyết tự quyết (Deci & Ryan), mục tiêu gần (Bandura & Schunk), mastery learning (Bloom),
giãn cách + ôn truy hồi (Cepeda, Roediger), tư duy phát triển (Dweck), nhạy cảm địa vị tuổi vị thành
niên (Steinberg, Blakemore). Nhắm vào **nhóm 25% thấp nhất** — nhóm trên tiến bộ với mọi hệ thống.
Thứ tự = thứ tự làm. Ba việc đầu là tối thiểu cho mùa 2.
- [ ] **Trục "tiến bộ so với chính em"**: mỗi tuần tính tỉ lệ đúng theo YCCĐ so với 2 tuần trước;
      tăng → cộng RP + thành tích "Tiến bộ tuần"; mục "Tiến bộ nhất tuần" lên bảng vinh danh công
      khai cạnh top RP. (Dữ liệu: exam/practice_question_results đã có; thêm 1 RPC gộp, không thêm
      query rời ở trang chủ HS.)
- [ ] **Mục tiêu tuần thích ứng**: bỏ "3 bài ≥7,0" chung cho cả lớp; đặt từ dữ liệu 2 tuần gần
      nhất của chính em (số bài + ngưỡng điểm nhỉnh hơn trung bình của em), nhắm ~80–85% lượt thử
      thành công.
- [ ] **Đổi khung kênh phụ đạo**: trên màn hình HS đổi "cần phụ đạo" → "đang mở khoá"; thành tích
      "Phục hồi" khi thoát; thay giới hạn 3 lượt tổng bằng thời gian chờ 1–2 ngày giữa các lượt +
      gợi ý đúng đoạn lý thuyết trước lượt sau. Nhãn phụ đạo chỉ GV/TA thấy.
- [ ] **Luyện tập tăng dần độ khó**: phiên luyện bắt đầu Dễ, đạt 80% mới lên TB rồi Khó (trùng 3
      mức danh hiệu, không thêm khái niệm mới).
- [ ] **Bảng xếp hạng chia giải theo bậc**: chỉ so với em cùng bậc; bảng lớp giữ top 3, "vị trí
      của em" hiện 2 bạn ngay trên/dưới, không hiện số thứ tự tuyệt đối.
- [ ] **Mục tiêu chung của lớp**: "cả lớp đạt N huy hiệu tuần này" + phần thưởng chung (cấu trúc
      hợp tác, em giỏi có lý do giúp em yếu).
- [ ] **Giãn cách trong điều kiện huy hiệu**: Huyền Thoại chỉ tính câu Khó đúng ở ≥2 tuần khác
      nhau; câu sai quay lại sau 2 ngày / 1 tuần / 1 tháng (gộp với việc chống cày ở GĐ 1).
- [ ] **Chuỗi ngày có đóng băng**: 1 lần/tuần; mốc reset không phải 0h (nhiều em học 23h–1h).
- [ ] **Danh sách thứ Hai cho thầy**: 5 em lên mức huy hiệu + 5 em tiến bộ nhất, để thầy nhắc tên
      trong lớp — ghi nhận qua thầy quan trọng hơn qua web với nhóm dưới.
- [ ] **Đo đúng chỗ**: theo dõi nhóm 25% thấp nhất từ đầu mùa — % còn làm bài tuần 4–5, % nhận ≥1
      huy hiệu, % thoát ≥1 chủ đề. Ba số này không nhúc nhích = hệ đang nới khoảng cách.

## Giai đoạn 2 — Learning Journey = bộ huy hiệu của lớp (Q4/2026 → 01/2027, mốc ThachLab 2.0)
Thay vì dựng trang lộ trình riêng theo chương, **bộ huy hiệu theo lớp là trang lộ trình**:
- [ ] Mỗi huy hiệu trong bộ của lớp hiện trạng thái ✅ đạt / 🟡 đang tới / 🔴 đang cần phụ đạo /
      ⚪ chưa học, lấy từ mastery + tutoring_needs (không thêm RPC rời, mở rộng RPC rank có sẵn).
- [ ] "Bước tiếp theo": chọn 1 huy hiệu gần đạt nhất + 10 câu luyện đúng YCCĐ đó, đặt ngay
      trên trang chủ HS (rule-based, dùng `tutoring_needs` + tiến độ danh hiệu).
- [ ] Thành tích "Phục hồi" cho HS thoát phụ đạo — kênh hụt cũng phải có lối ra tích cực.
- [ ] Chương mẫu **Vật lý 10 – Động học**: đủ ảnh lý thuyết + ≥30 câu/bài có mức độ, đo trên
      lớp offline 1 tháng. Đây là lớp 10, bộ huy hiệu lớp 10 phải đạt được trọn vẹn bằng chương này.
- [ ] Ra mắt công khai ThachLab 2.0 với chương Động học 10 hoàn chỉnh + số liệu mùa 1–2.

## Giai đoạn 3 — Khám phá / Mô phỏng (song song từ Q1/2027, 1–2 mô phỏng/tháng)
Đã có: con lắc lò xo SVG (`SpringSimulation`) làm hero trang chủ.
- [ ] Nhúng vào bài Dao động kèm bộ câu hỏi gắn YCCĐ (mô phỏng cũng góp câu cho danh hiệu).
- [ ] Đồ thị x–t, v–t → rơi tự do, ném ngang → sóng → nhiệt → điện.
- Không làm mô phỏng nào không gắn với một bài học + một bộ câu hỏi.

## Giai đoạn 4 — AI Tutor Socratic (Q2–Q3/2027)
- [ ] MVP trên Claude API: hỏi gợi mở, chia nhỏ bài; chỉ đưa đáp án sau ≥2 gợi ý hoặc "Em bó tay".
- [ ] AI đọc `exam_question_results` + `tutoring_needs` + tiến độ danh hiệu để gợi đúng chỗ yếu;
      ưu tiên chạy trong kênh phụ đạo (nơi HS đang kẹt) trước khi mở đại trà.
- [ ] Giới hạn lượt/ngày cho tài khoản miễn phí → tính năng trả phí đầu tiên.

## Giai đoạn 5 — Teacher Studio (~75%, chỉ hoàn thiện)
Đã có thêm từ 23/09: `/quan-tri/xep-hang`, sửa đề, ngân hàng câu hỏi + chống mất hình, quy chế
trợ giảng gắn phụ đạo, vinh danh. **Dừng ở đây** — không thêm mảng quản lý mới tới 2.0.
- [ ] Tạo đề theo ma trận (YCCĐ × Dễ–TB–Khó) từ ngân hàng — giờ đã đủ dữ liệu, làm khi cần
      đề cho chương Động học.
- [ ] Xuất Word/PDF trong web.

## Giai đoạn 6 — Premium & mở rộng (2028)
Gói trả phí = AI Tutor không giới hạn + lớp online có GV theo dõi + luyện đề chuyên sâu. Kiến
thức nền và hệ danh hiệu giữ miễn phí (danh hiệu là bằng chứng học, không bán). Lớp 9 mở khi
10–12 ổn. Mobile app chỉ khi web đạt ≥500 HS hoạt động hàng tuần.

## Ngoài roadmap Vật lý (giữ, không mở rộng)
CNC/CTTC, SHCN, trợ giảng: chỉ sửa lỗi.

---

## Việc bắt đầu ngay
Hạn mức tuần Claude reset **12:00 trưa Thứ Năm 02/10/2026** (giờ VN). Tới lúc đó chỉ làm việc rẻ.
- **28/09 → 02/10 (rẻ, không code)**: chốt số liệu nền (4 tuần trước 21/09); rà độ phủ ngân hàng theo
  danh hiệu bằng 1 câu SQL đọc; thầy tự test luồng động lực bằng tài khoản HS thật trên mobile.
- **Từ 02/10**: 3 việc đầu của GĐ 1b (tiến bộ so với chính em, mục tiêu tuần thích ứng, đổi khung
  phụ đạo) — mỗi việc 1 phiên riêng, xong commit + deploy rồi mới sang việc sau.
- **Song song, rẻ**: đăng ~300 đề thi thử theo quy tắc mới trong `dang-de-hang-loat`.
- Không thêm lớp động lực mới nào khác cho tới hết mùa 1 (25/10).
