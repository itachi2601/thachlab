# ROADMAP ThachLab (cập nhật 28/09/2026 — bản đối chiếu mã nguồn + hệ động lực; kế hoạch lý thuyết tương tác bổ sung 4/10/2026)

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
- [x] **Trục "tiến bộ so với chính em"** (29/09 RP đã chạy; 30/09 thêm thành tích "Tiến Bộ Tuần" — file `…120000` chờ chạy; số liệu là tham chiếu, chỉnh sau mùa 1 qua `rank_seasons.config`): mỗi tuần tính tỉ lệ đúng theo YCCĐ so với 2 tuần trước;
      tăng → cộng RP + thành tích "Tiến bộ tuần"; mục "Tiến bộ nhất tuần" lên bảng vinh danh công
      khai cạnh top RP. (Dữ liệu: exam/practice_question_results đã có; thêm 1 RPC gộp, không thêm
      query rời ở trang chủ HS.)
- [x] **Mục tiêu tuần thích ứng** (29/09: xong và đã chạy; số liệu là tham chiếu, chỉnh qua cấu hình mùa): bỏ "3 bài ≥7,0" chung cho cả lớp; đặt từ dữ liệu 2 tuần gần
      nhất của chính em (số bài + ngưỡng điểm nhỉnh hơn trung bình của em), nhắm ~80–85% lượt thử
      thành công.
- [~] **Đổi khung kênh phụ đạo** (30/9: code + migration xong và đã chạy — nhãn HS/PH "đang mở khoá", chờ 24 giờ thay 3 lượt, gợi ý đoạn lý thuyết sau lượt trượt; thành tích "Phục hồi" = "Lật Kèo Ngoạn Mục" đã có sẵn; còn thiếu: tách lý thuyết theo đúng YCCĐ trượt): trên màn hình HS đổi "cần phụ đạo" → "đang mở khoá"; thành tích
      "Phục hồi" khi thoát; thay giới hạn 3 lượt tổng bằng thời gian chờ 1–2 ngày giữa các lượt +
      gợi ý đúng đoạn lý thuyết trước lượt sau. Nhãn phụ đạo chỉ GV/TA thấy.
- [x] **Luyện tập tăng dần độ khó** (30/9: xong, chỉ code phía client — mức lưu localStorage theo HS+mục luyện, không migration/round-trip mới; có nút "Luyện tự do"; `features/lessons/practice-ladder.ts`, `PracticeSession.tsx`): phiên luyện bắt đầu Dễ, đạt 80% mới lên TB rồi Khó (trùng 3
      mức danh hiệu, không thêm khái niệm mới).
- [x] **Bảng xếp hạng chia giải theo bậc** (30/9: code xong, migration `…110000` chờ chạy — `rank_class_board` so sánh chỉ trong cùng bậc, bỏ pos/total tuyệt đối; top 3 lớp giữ): chỉ so với em cùng bậc; bảng lớp giữ top 3, "vị trí
      của em" hiện 2 bạn ngay trên/dưới, không hiện số thứ tự tuyệt đối.
- [x] **Mục tiêu chung của lớp** (30/9: code + migration `…140000`, chờ chạy): "cả lớp đạt N huy hiệu tuần này" + phần thưởng chung (cấu trúc
      hợp tác, em giỏi có lý do giúp em yếu).
- [~] **Giãn cách trong điều kiện huy hiệu** (30/9: phần Huyền Thoại ≥ 2 tuần xong, migration `…120000` chờ chạy; **còn thiếu**: lịch "câu sai quay lại sau 2 ngày / 1 tuần / 1 tháng" — cần thiết kế màn ôn riêng, gộp với việc chống cày ở GĐ 1).
- [x] **Chuỗi ngày có đóng băng** (30/9: code + migration `…130000`, chờ chạy): 1 lần/tuần, tự động; ngày mới tính từ 3h sáng (nhiều em học 23h–1h).
- [x] **Danh sách thứ Hai cho thầy** (30/9: `MondayListPanel` ở tab Tổng quan lớp + migration `…150000`, chờ chạy): 5 em lên mức huy hiệu + 5 em tiến bộ nhất, để thầy nhắc tên
      trong lớp — ghi nhận qua thầy quan trọng hơn qua web với nhóm dưới.
- [x] **Đo đúng chỗ** (30/9: tab "Đo nhóm thấp" ở `/quan-tri/xep-hang` + migration `…150000`, chờ chạy): theo dõi nhóm 25% thấp nhất từ đầu mùa — % còn làm bài tuần 4–5, % nhận ≥1
      huy hiệu, % thoát ≥1 chủ đề. Ba số này không nhúc nhích = hệ đang nới khoảng cách.

## Giai đoạn 2 — Learning Journey = bộ huy hiệu của lớp (Q4/2026 → 01/2027, mốc ThachLab 2.0)
Thay vì dựng trang lộ trình riêng theo chương, **bộ huy hiệu theo lớp là trang lộ trình**:
- [ ] Mỗi huy hiệu trong bộ của lớp hiện trạng thái ✅ đạt / 🟡 đang tới / 🔴 đang cần phụ đạo /
      ⚪ chưa học, lấy từ mastery + tutoring_needs (không thêm RPC rời, mở rộng RPC rank có sẵn).
- [x] "Bước tiếp theo" (bản rút gọn, 5/10/2026): thẻ ở trang chủ HS gợi ý tối đa 3 việc theo thứ tự — mở khoá
      MỘT chủ đề đang phụ đạo → làm lại đề điểm thấp (<6,5) → học bài kế (luôn giữ chỗ để có việc dễ thắng).
      Rule-based, chỉ dùng dữ liệu trang chủ đã tải (không RPC/migration mới): `features/learning/next-steps.ts`,
      `components/learning/NextStepsCard.tsx`, test `npm run test:next-steps`.
- [ ] "Bước tiếp theo" bản đầy đủ: chọn 1 huy hiệu gần đạt nhất + 10 câu luyện đúng YCCĐ đó — làm sau, khi RPC rank
      trả được tiến độ huy hiệu; lúc đó chỉ thêm dòng "làm xong sẽ gần huy hiệu X", không đổi thứ tự ưu tiên.
- [ ] Thành tích "Phục hồi" cho HS thoát phụ đạo — kênh hụt cũng phải có lối ra tích cực.
- [ ] Chương mẫu **Vật lý 10 – Động học**: đủ ảnh lý thuyết + ≥30 câu/bài có mức độ, đo trên
      lớp offline 1 tháng. Đây là lớp 10, bộ huy hiệu lớp 10 phải đạt được trọn vẹn bằng chương này.
- [ ] Ra mắt công khai ThachLab 2.0 với chương Động học 10 hoàn chỉnh + số liệu mùa 1–2.

## Giai đoạn 2.6 — Mobile PWA (đề xuất 5/10/2026, đã đối chiếu code; chờ thầy duyệt trước khi làm)
Không làm app native: biến site `output: "export"` thành PWA cài được (Android + iOS 16.4+), không phá mốc
"mobile app chỉ khi ≥500 HS/tuần" ở GĐ 6. **Chỉ dựng vỏ + lối vào + nhắc**, không viết lại luyện tập.
Chi tiết, ràng buộc và thứ tự: `docs/BAN-GIAO-MOBILE-PWA-2026-10-05.md`.
- [ ] **M1 Vỏ PWA**: `app/manifest.ts` (static export dùng được), icon 192/512/maskable + apple-touch-icon (`.webp`/PNG
      sinh từ logo), `public/sw.js` viết tay (precache shell, KHÔNG cache `/data/*.json` kiểu cache-first vì
      `services/static-content.ts` đã tự đối chiếu Supabase), đăng ký SW ở client, `theme_color` lấy từ
      `--color-bg`. Banner "Thêm vào màn hình chính" 1 lần, sau khi HS xong bài luyện đầu tiên.
- [ ] **M2 Luyện nhanh 10 câu**: nút ở thẻ `WeakestSkillsCard` (đã gọi `get_my_weakest_topics`) mở thẳng
      `TopicPracticeModal` với chủ đề yếu nhất, 10 câu, chế độ "Từng câu" có sẵn. KHÔNG thêm RPC/bảng/URL mới.
- [ ] **M3 Offline**: cache phần đã mở + hàng đợi `savePracticeSession` khi mất mạng (localStorage/IndexedDB), gửi lại
      khi có mạng. Làm sau M2; giữ kết quả LẦN ĐẦU từng câu như hiện nay.
- [ ] **M4 Nhắc 1 lần/ngày**: Web Push (VAPID) qua Edge Function mới + bảng đăng ký (migration, chạy theo
      quy trình `run-migrations.sh`); nội dung lấy từ chủ đề yếu nhất; HS tự chọn giờ. Streak đóng băng **đã có**
      (migration 20260930130000) — chỉ hiển thị, không làm lại.
- Đo: % HS cài PWA, phiên/tuần/HS, độ dài phiên, quay lại ngày 7. Đợt 2 (sau ra mắt): chụp ảnh bài → AI Tutor (GĐ 4),
  thẻ chia sẻ lên hạng, tin tuần cho phụ huynh, mô phỏng cảm biến nghiêng, QR điểm danh lớp Cao Thắng.

## Giai đoạn 3 — Khám phá / Mô phỏng (song song từ Q1/2027, 1–2 mô phỏng/tháng)
Đã có: con lắc lò xo SVG (`SpringSimulation`) làm hero trang chủ.
- 5/10/2026: con lắc lò xo **rời hero** (thay bằng tab "Thả hàng" — máy bay cứu hộ thả gói, ném ngang, Bài 12
  Vật lí 10). `HarmonicPanel` + `SpringSimulation` giữ nguyên code, chờ nhúng vào bài Dao động ở đây.
- 4/10/2026: hero có **tab 4 "Hình chiếu"** — bóng của M quay đều và con lắc lò xo nằm ngang trên CÙNG một trục x
  (`components/physics/ShadowSpringSimulation.tsx`, `hooks/useCircularProjection.ts`, `lib/circularProjection.ts`),
  nguồn là spec `content/thi-nghiem/tn-l11-daodongdieuhoa-03.json` của Bài 1 Vật lí 11. Việc còn lại của Giai
  đoạn 3: nhúng bản tương tác vào chính bài 1 (lesson 20) + gắn bộ câu hỏi YCCĐ `daodong.hinh_chieu_tron_deu` —
  cần thêm cơ chế mount mô phỏng trong `components/exams/ContentHtml.tsx` (chi tiết ở `docs/STATE.md`).
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

## Skill Claude cần xây (công cụ của thầy, không phải tính năng web) — đề xuất 29/09/2026, chờ duyệt
Bản đồ quy trình + bằng chứng khâu trống + dữ liệu cần cung cấp: `docs/DE-XUAT-SKILL-2026-09-29.md`.
Thứ tự = tần suất dùng. Chưa tạo skill nào khi thầy chưa duyệt.
- [ ] **Đ1 `khbd-5512`** (mới): kế hoạch bài dạy CV 5512, 4 hoạt động, bám YCCĐ TT32; tái dùng
      `lesson_items` + đề đã đăng; 2 reference Vật lí THPT / CNC cao đẳng. Cần: PDF TT32 môn Vật lí,
      1–2 KHBD mẫu tổ đã duyệt, mẫu giáo án LT/TH/tích hợp Cao Thắng.
- [ ] **Đ2 `phan-tich-ket-qua`** (mới): đọc RPC phân tích ThachLab hoặc file kết quả Azota → báo cáo
      Word/Excel sau kiểm tra + nhận xét HS. Cần: 1 file Azota xuất mẫu, mẫu báo cáo tổ.
- [ ] **Đ3 bổ sung `de-vat-ly-thpt`**: bản đặc tả, rút đề từ `question_bank` theo ma trận YCCĐ ×
      Dễ–TB–Khó (chồng với mục GĐ 5 "Tạo đề theo ma trận" — làm ở skill trước, web sau), cổng kiểm
      định sau khi ghi file. Cần: mẫu bản đặc tả, chốt ánh xạ NB/TH/VD ↔ Dễ/TB/Khó.
- [ ] **Đ4 rubric eval CSV** cho 12 skill nghiệp vụ (bucket P/R/O/M, cột Conditional/Source theo
      k12-teacher-skills), chạy bằng harness `skill-creator` sẵn có. Cần: 3–5 file thật/skill.
- [ ] **Đ5 `chuan-dau-ra-abet`** (mới): ma trận CLO ↔ PLO ↔ ETAC outcomes, performance indicators,
      đề cương học phần CNC. Cần: bộ tiêu chí ETAC đang áp dụng, PLO CĐ CNCTM, đề cương hiện có.
- [ ] **Đ6 `phan-hoa-day-lai`** (bước cuối Đ2 hoặc skill riêng): gói 3 mức + kế hoạch tiết chữa bài.
- [ ] **Đ7 bổ sung `up-de-kiem-tra`** nhánh đích CNC (`cnc_key`, `/quan-tri/cnc-dang-de`).
- [ ] **Đ8 `mo-phong-bai-hoc`**: hoãn tới GĐ 3 (Q1/2027); `lib/Physics/*` đã xoá 29/09 vì là code
      chết — khi làm thì viết lại theo mô hình cần, lấy lại từ git nếu cần tham khảo.

---

## Việc bắt đầu ngay
Hạn mức tuần Claude reset **12:00 trưa Thứ Năm 02/10/2026** (giờ VN). Tới lúc đó chỉ làm việc rẻ.
- **28/09 → 02/10 (rẻ, không code)**: chốt số liệu nền (4 tuần trước 21/09); rà độ phủ ngân hàng theo
  danh hiệu bằng 1 câu SQL đọc; thầy tự test luồng động lực bằng tài khoản HS thật trên mobile.
- **Từ 02/10**: 3 việc đầu của GĐ 1b (tiến bộ so với chính em, mục tiêu tuần thích ứng, đổi khung
  phụ đạo) — mỗi việc 1 phiên riêng, xong commit + deploy rồi mới sang việc sau.
- **Song song, rẻ**: đăng ~300 đề thi thử theo quy tắc mới trong `dang-de-hang-loat`.
- Không thêm lớp động lực mới nào khác cho tới hết mùa 1 (25/10).

## Lý thuyết tương tác — việc tiếp (chốt 4/10/2026)

Bài đọc có tương tác (mục tiêu, dự đoán, từ khoá, thí nghiệm, bẫy, trả bài, bài toán mẫu) theo skill `soan-bai-ly-thuyet-tuong-tac`. Không tính 17 mục Kiểm tra.

**Đã lên web 4/10/2026 — Vật lí 12 gần đủ.** 19/20 bài dạy đã có lý thuyết tương tác. Ba bài có từ trước (Bài 1, Bài 12, Bài 13). Mười sáu bài ghi cơ sở dữ liệu trong ngày và lên web cùng bản deploy này: Bài 2–10, Bài 14–16 (từ trường), Bài 14–18 (hạt nhân). Kèm Bài 14 lớp 11 (Bài tập về sóng, id 33) vì đã ghi cùng đợt. **Còn trống ở lớp 12:** Bài 11 Thực hành đo độ lớn cảm ứng từ (id 12) — chưa có mục lý thuyết.

Cách làm mỗi đợt: 4 bài một lượt, soạn song song, kiểm chéo trước khi ghi, chỉ ghi mục Lý thuyết, rồi deploy.

- [ ] **Đợt 1 — Lớp 11, chương Dao động** (đang dạy đầu năm). Soạn 4 bài kiến thức còn lý thuyết cũ: Bài 2 Mô tả dao động điều hoà (id 21), Bài 3 Vận tốc và gia tốc (id 22), Bài 5 Động năng và thế năng (id 24), Bài 6 Tắt dần, cưỡng bức, cộng hưởng (id 25). Xong bốn bài đó mới tới hai tiết bài tập đang trống: Bài 4 (id 23), Bài 7 (id 26).
- [ ] **Đợt 2 — Lớp 10, chương Động học.** Soạn Bài 4, 5, 7, 8, 9, 10 (id 49, 50, 52, 53, 54, 55). Bài 12 Chuyển động ném đã có. Bài 6 và Bài 11 (thực hành, đang trống) để sau các bài kiến thức.
- [ ] **Đợt 3 — Lớp 11, nốt Sóng rồi sang Điện.** Sóng: Bài 9, Bài 11, Bài 15 và Bài 10 thực hành (id 28, 30, 34, 29). Bài 8, 12, 13 đã có; Bài 14 vừa lên web. Tiếp điện trường Bài 16–21 (id 35–40), rồi dòng điện Bài 22–26 (id 41–45).
- [ ] **Đợt 4 — Lớp 10, phần còn lại.** Mở đầu Bài 1–3 (id 46–48). Động lực học trừ Bài 13 và Bài 16 đã có (id 59, 60, 62–67; Bài 20 và Bài 22 đang trống). Sau đó năng lượng Bài 23–27, động lượng Bài 28–30, chuyển động tròn Bài 31–32, biến dạng và áp suất Bài 33–34.
- [ ] **Đợt 5 — KHTN 9.** 17 bài, chưa bài nào tương tác. Đã có lý thuyết cũ: Bài 2–6. Đang trống: Bài 1 và Bài 7–17. Làm khi 10–12 đã phủ chương đang dạy.
- [ ] **Lớp 12, một bài còn lại:** Bài 11 Thực hành đo cảm ứng từ (id 12).
