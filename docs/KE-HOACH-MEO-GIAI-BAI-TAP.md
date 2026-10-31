# Kế hoạch "💡 Mẹo nhìn" — mô hình đời thường để giải nhanh một dạng bài (31/10/2026)

Nguồn: hai artifact thầy làm thử — **Đòn bẩy nhiệt** (thả lần lượt viên sắt 100 °C vào nước 20 °C) và
**Quỹ nhiệt** (bỏ N viên đá vào nước nóng, quỹ cạn dần → N_max = 39). Cả hai biến một phương trình
cân bằng nhiệt thành hình ảnh học sinh đã quen (bập bênh, ví tiền), dùng lại được ở mọi bài cùng dạng.

## 1. Khác gì với cái đã có

| Đã có | Là gì | Mẹo nhìn khác ở đâu |
|---|---|---|
| 🧠 `.tl-meo` (bài lý thuyết, `docs/BANG-MEO-TU-KHOA.md`) | vài chữ để **nhớ** khái niệm (Nhỏ – Loạn – Đập) | mẹo nhìn để **giải**: đổi phương trình thành một hình đời thường |
| `nhan_dang` của bài tập mẫu ("Thấy … → nghĩ tới …") | nhận ra dạng → công thức | mẹo nhìn trả lời "vì sao công thức đó đúng, và đoán nhanh kết quả" |
| Mô phỏng dưới đề | hiện tượng của **chính đề**, không lộ đáp số | mẹo nhìn chạy tới đáp số → chỉ được mở **sau** lời giải |

Dùng biểu tượng 💡 (không dùng 🧠 để khỏi lẫn với mẹo từ khoá).

## 2. Đặt ở đâu

**Chính: trong Bài tập mẫu, gắn vào đúng dạng** — khối gập "💡 Mẹo nhìn: <tên>" hiện **sau khi mở hết các bước
lời giải, ngay trước nút "Làm bài tương tự"**. Lý do:

- Mô phỏng mẹo chạy tới đáp số → đặt dưới đề là lộ đáp án (trái quy tắc mô phỏng dưới đề của skill `soan-bai-tap-mau`).
- Học sinh vừa giải bằng phương trình xong, thấy mẹo, rồi **dùng ngay ở 3 câu tương tự** — đúng thứ tự
  ví dụ mẫu → mô hình → tự làm (N6; chuyển giao bằng phép tương tự cần được dùng ngay mới bám, Gick & Holyoak).
- Không thêm tab/trang mới (N1, B7).

**Phụ: trong bài lý thuyết** chỉ khi mẹo giải thích **khái niệm** chứ không phải mẹo giải (ví dụ khúc xạ =
bánh xe đẩy chạy xiên từ đường nhựa vào cát) — khi đó là hộp ví dụ thường, tính vào hạn mức V11.

**Hai mẫu của thầy gắn vào:** HSG KHTN 9 CĐ12 Nhiệt (bài 153) dạng 1 "nhiệt lượng kế, thả vật nóng" ← Đòn bẩy nhiệt;
dạng 2 "thả nước đá vào nước" ← Quỹ nhiệt. Dùng lại y tên ở L12 bài 3 (Nội năng, dạng "hai vật trao đổi nhiệt")
và L12 bài 1 (Sự chuyển thể).

## 3. Quy tắc cho một mẹo nhìn (tư vấn theo nghiên cứu)

- **Một mẹo = một hình đời thường + ⚠ điều kiện áp dụng** (AI-TUTOR 9.1). Đòn bẩy nhiệt chỉ đúng khi
  không chuyển thể, bỏ qua hao phí → câu ⚠ nằm ngay dưới tên mẹo. Phép tương tự không có ranh giới là nguồn quan niệm sai.
- **Ít thứ trên màn** (G1): hai artifact hiện có 4 ô số đo + dải công thức + phụ đề + thanh tua — ở 375 px quá 4 khối.
  Bản đưa lên web giữ: hình + 1 dòng phụ đề đổi theo chặng (≤ 25 chữ) + 1 công thức chốt. Bỏ 4 ô số đo.
- **Không tự chạy, không lặp** (B4): bấm "▶ Chạy" một lần, dừng ở khung cuối, "↻ Chạy lại". Giảm chuyển động → hiện khung cuối.
- **Kĩ thuật**: SMIL như mô phỏng bài tập mẫu (`hinh.fig()` tự thêm nút `bt-run`), ≤ 15 KB, chữ SVG ≥ 13 px ở 360 px (H4),
  màu theo token nền sáng (`docs/MAU-NEN-SANG.md`). Phụ đề theo chặng làm bằng `<set>` trên các `<text>`.
  Không thêm JS mới vào trang HS; nếu sau này cần thanh tua thì làm **một** component dùng chung lazy + `LazyErrorBoundary`.
- **Tên mẹo 2–3 chữ, dùng y hệt ở mọi lớp** (như bảng mẹo từ khoá): Đòn bẩy nhiệt, Quỹ nhiệt, Thang cuốn…
- **Đo**: so tỉ lệ đúng lần đầu ở "Làm bài tương tự" giữa dạng có / chưa có mẹo cùng chương; mẹo nào không
  cải thiện sau 2–3 tuần thì gỡ, không nhân ra.

## 4. Kho mẹo đề xuất (ứng viên; ★ = đợt 1)

Tiêu chí chọn: (a) mẹo **rút ngắn lời giải hoặc cho đoán nhanh** (dùng được khi làm Phần III), không chỉ minh hoạ;
(b) dạng hay sai; (c) hình ảnh có thật trong đời học sinh 14–18 (đi học, ăn uống, xe, điện thoại, thể thao).

**Nhiệt** (HSG9 CĐ12/16, L12 Ch.1)
- ★ **Đòn bẩy nhiệt** — nhiệt dung = quả nặng, nhiệt độ cân bằng = điểm tựa; vật nặng kéo điểm tựa về phía mình. ⚠ không chuyển thể. → 153 d1, L12 b3, HSG rót qua lại (153 d5: mỗi lần rót là một lần cân đòn).
- ★ **Quỹ nhiệt** — nước nóng có "ví" Q₀ (mốc nước 0 °C), mỗi viên đá rút λm; ví cạn trước → còn đá, t = 0 °C. → 153 d2, L12 b1.
- **Phí cố định** — đun hai lần, hao phí không đổi = cước mở cửa taxi: trừ hai lần để khử. → 164 d2, 165 d3.
- **Bồn nước rò** — nhiệt độ ổn định khi nhiệt vào = nhiệt rò; rò nhanh khi chênh nhiệt lớn (như lỗ rò khi mực nước cao). → 164 d3.
- **Thang máy dừng tầng** — đoạn nằm ngang trên đồ thị t(τ): vẫn cấp năng lượng mà nhiệt độ đứng vì đang "trả" cho chuyển thể. → L12 b1 d3–4.

**Cơ học**
- ★ **Ngồi trên bè** — bè trôi/phao rơi: đổi sang hệ quy chiếu nước thì dòng chảy biến mất, thời gian đi = về. → 162 d4, 167.
- ★ **Con sâu qua cổng** — tàu qua cầu/hầm: tính từ đầu vào tới đuôi ra = cầu + tàu. → 162 d3, 167.
- **Điểm có hệ số** — tốc độ trung bình nửa quãng đường: thời gian là hệ số, không lấy trung bình cộng. → 162 d1, L10 b5.
- **Người giữ cửa** — ma sát nghỉ: đẩy bao nhiêu chống bấy nhiêu, quá ngưỡng thì trượt. → L10 b18 d1.
- **Bập bênh** — moment, đòn bẩy, thanh có bản lề. → L10 b21, 161 d2 (đã có chữ "bập bênh" trong bài: chỉ thêm hình chạy).
- **Giảm giá chồng** — hiệu suất nhiều khâu nhân nhau (giảm 20 % rồi 10 % ≠ 30 %). → L10 b27 d5, 163 d1.
- **Hai bạn patin đẩy nhau** — tách vật/súng giật: nhẹ thì lùi nhanh. → L10 b29 d5.
- **Ví cơ năng** — có ma sát: cơ năng là ví, ma sát rút phí (dùng lại khuôn Quỹ nhiệt). → L10 b26 d5, 166 d4/d7.
- **Chồng người** — áp suất đáy cột chất lỏng = sức nặng cột phía trên trên mỗi đơn vị diện tích; bình thông nhau = hai cột cân. → L10 b34, 154 d1–2.

**Điện**
- ★ **Cổng soát vé** — nối tiếp: một hàng qua nhiều cổng (cùng I, U chia); song song: nhiều làn (cùng U, I chia). → L9 b12, 157 d1.
- **Ống hút trà sữa** — R = ρl/S: ống dài khó hút, ống to dễ hút; kéo dãn (thể tích không đổi) dài gấp n thì mảnh đi n → R gấp n². → 159 d1–3, L9 b11.
- **Ống đầy bi** — tốc độ trôi rất chậm mà đèn sáng ngay. → L11 b22 d4.
- **Xe tải lớn ít chuyến** — truyền tải: tăng U để giảm I, hao phí ∝ I². → L12 b14 d4, 152 d4.
- **Bể chứa** — tụ điện: U = mực nước, C = diện tích đáy, Q = lượng nước. → L11 b21.

**Dao động – sóng – hạt nhân – quang**
- ★ **Bóng đu quay** — dao động điều hoà là bóng của điểm chạy tròn: đếm "lần thứ n", quãng đường bằng góc quét. → L11 b4 d4–5, b1 d5 (bài đã có chữ "hình chiếu": thêm hình chạy + đếm vòng).
- ★ **Chia đôi chiếc bánh** — chu kì bán rã: đếm số lần chia đôi, không trừ đều. → L12 b17 d2.
- **Đèn pin lan ra** — liều/cường độ ∝ 1/r²: lùi gấp đôi, vệt sáng rộng gấp 4. → L12 b18 d3.
- ★ **Xe đẩy vào cát** — khúc xạ: bánh chạm cát trước chậm lại, xe bẻ hướng về pháp tuyến. → L9 b5, 151 d1 (khái niệm → để trong lý thuyết).
- **Bóng dưới đèn đường** — đồng dạng cho bóng người đi dưới đèn. → 158 d2.

Bỏ ra khỏi kho: chỗ đã có mẹo từ khoá đủ dùng (ném ngang "Ngang Đều – Dọc Rơi", sóng dừng "Cố Định / Tự Do").

## 5. Các chặng

| Chặng | Việc | Ra gì | Ai/đâu |
|---|---|---|---|
| 0 | Thầy chốt: tên "💡 Mẹo nhìn", vị trí sau lời giải, danh sách ★ đợt 1 | dòng chốt trong file này | thầy |
| 1 | UI: trường tuỳ chọn `meo` mỗi dạng (`ten`, `dieu_kien`, `html`) trong `WorkedQuestionsGrid.tsx`, khối gập sau bước cuối; validator `scripts/lib.ts` (có ⚠, ≤ 15 KB, không `<script>`); `publish-bai-tap-mau.mts` chuyển trường; xem ở `/dev/btm` | 1 commit, chụp 375 px | phiên Mac |
| 2 | Chuyển 2 artifact sang SMIL theo mục 3, gắn 153 d1–d2; tính lại số (30 °C → C_nước = 7C; 39 viên, dư 9 000 J); `kiem-code` soát vật lí + lộ đáp số | 2 khối mẹo, chụp sáng/tối 375/1280 | phiên Mac |
| 3 | `docs/BANG-MEO-GIAI.md` (tên mẹo · dạng gắn · ⚠ · chỗ mẹo sai) + mục "Mẹo nhìn" trong skill `soan-bai-tap-mau` | bảng tra trước khi đặt mẹo mới | phiên Mac |
| 4 | Đợt 1: 6 mẹo ★ còn lại (bè, con sâu, cổng soát vé, bóng đu quay, chia đôi bánh, xe đẩy vào cát) — mỗi mẹo một agent `ve-hinh-dong`, phiên chính soát; dùng lại tên ở mọi lớp có dạng đó | ~8 dạng có mẹo, đăng ngoài giờ HS | Mac, ≥ 22h |
| 5 | Đo 2–3 tuần (mục 3) rồi mới mở đợt 2 | ghi số liệu vào file này | thầy + phiên sau |

Hạn mức: mỗi dạng ≤ 1 mẹo, mỗi bài ≤ 2 dạng có mẹo (G1, V11 tinh thần).
