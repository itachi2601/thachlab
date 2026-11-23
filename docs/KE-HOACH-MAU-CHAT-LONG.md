# Màu chất lỏng trong hình — quy ước và kế hoạch triển khai (23/11/2026)

Thầy chốt 23/11/2026: chất lỏng vẽ **trong suốt, phủ màu đỏ hoặc xanh**, không tô xám/đen đặc.
Lý do: mảng đặc che mất điểm A/B, thước, nét ống nằm trong chất lỏng; trên nền chiếu tối thành mảng đen
(mẫu trình chiếu ống thuỷ ngân trước đây tô `var(--hg)` không có giá trị → đen đặc).

## 1. Quy ước

| Chất lỏng | Màu | Mã |
|---|---|---|
| Thuỷ ngân; chất lỏng **nặng hơn** khi có hai chất (đáy ống chữ U) | đỏ trong | `#dc2626`, độ phủ 0,22 |
| Nước, dầu, rượu; chất lỏng **nhẹ hơn**; bể/chậu nước; nước trong ống cộng hưởng | xanh trong | `#2563eb`, độ phủ 0,22 |

- Mặt thoáng / mặt phân cách: nét liền cùng màu, đậm (độ phủ 1) — nhìn ra mức chất lỏng (M3, M4).
- Chỉ một chất lỏng là nước → xanh. Chỉ một chất lỏng là thuỷ ngân → đỏ.
- Hai chất lỏng → nặng đỏ, nhẹ xanh, luôn kèm **chữ tên chất** trên hình (M4: không chỉ dựa vào màu).
- Khí giữ như cũ (lam rất nhạt / màu trạng thái ①②); vật rắn (khối gỗ, khối sắt) giữ màu vật, không dùng đỏ/xanh chất lỏng.
- Nguồn duy nhất trong code: `LONG_DO`, `LONG_XANH`, `LONG_OP` ở `components/lessons/cong-cu/chung.tsx`.
- Sách in đen–trắng (`book/`): **không áp** đỏ/xanh — giữ xám nhạt 15–20 % + nét mặt thoáng đậm.

## 2. Đã làm (23/11/2026, có hiệu lực mọi bài sau khi deploy — không cần đăng lại DB)

Các hình "giải cùng hình" vẽ bằng code từ JSON `cong_cu`:

| Họ hình | Chỗ đổi | Dạng dùng (quét `scripts/data/bai-tap-mau/`) |
|---|---|---|
| `cot_chat_long` · ống U | đáy đỏ, cột nhẹ xanh, mặt thoáng cùng màu | bài 7, 79, 154, 167 (10 dạng, cả cảnh `be`/`ong_kin`) |
| `cot_chat_long` · bể | nước xanh 0,22 (trước 0,14 lam) | như trên |
| `cot_chat_long` · ống kín | cột Hg đỏ trong (trước xám 0,34) | như trên |
| ống cộng hưởng (`song_day` cảnh ống) | nước xanh | bài 34 |
| `tia_sang` · môi trường có tên nước/dầu/rượu… | xanh trong, kể cả lớp đầu | 17 dạng: bài 2, 3, 83, 84, 150, 151, 167 |
| Mẫu trình chiếu ống thuỷ ngân (`/dev/btm-trinh-chieu`) | Hg đỏ trong + mặt thoáng | — |

Đã chụp kiểm `/dev/btm-trinh-chieu` (sáng + tối), `/dev/btm-hinh?f=btm-154`, `?f=btm-34`.

## 3. Còn lại — theo chặng

**Chặng 1 — chốt quy ước vào skill (1 phiên, không đụng DB)**
- Thêm 1 dòng quy ước + trỏ về file này vào: `soan-bai-ly-thuyet-tuong-tac`, `soan-bai-tap-mau`,
  `cap-nhat-dang-bai-tap`, `ra-soat-bai-hoc` (mục chấm hình: "chất lỏng đặc/xám = chưa đạt"), `ve-hinh-cau-hoi`;
  agent `ve-hinh-dong`. Sau khi vào main in lệnh `cai-skill.sh` cho thầy.
- `tia_sang` còn chỗ chưa theo quy ước: **ô vùng** (`vung`, vd hộp "rượu" bài 83 dạng 1) tô theo `mau` của JSON.
  Cách sửa: thêm nhận tên chất lỏng như phần môi trường, hoặc sửa JSON `mau` các dạng đó rồi đăng lại mục bài tập mẫu.
- `cot_chat_long` cảnh `be` đang vẽ **lớp dầu** bằng "khối" màu hổ phách (bài 154 dạng 1): thêm mục `lop_long`
  (chất lỏng nhiều lớp) để dầu xanh nhạt / nước xanh đậm hơn, có tên trên hình.

**Chặng 2 — hình bài lý thuyết (SVG dựng sẵn bằng `build_figs.py`, cần đăng lại DB)**

Quét 23/11: 24/116 bài có `build_figs.py` nhắc tới chất lỏng; 6 file khai hằng màu riêng (`WATER`, `OIL`) với 5 sắc khác nhau:
`l10-khoi-luong-rieng-ap-suat`, `l11-thuc-hanh-do-toc-do-am`, `l9-khuc-xa-anh-sang`, `l9-phan-xa-toan-phan`,
`hsg9/cd06-khuc-xa-phan-xa-toan-phan`, `hsg9/cd11-co-hoc-chat-luu`. 18 bài còn lại tô trực tiếp trong hàm vẽ — rà bằng mắt.

Mỗi bài, làm theo lịch dạy (chương sắp dạy trước), mỗi đợt ≤ 6 bài như `ra-soat-bai-hoc`:
1. Thêm `LIQ_RED = "rgba(220,38,38,.22)"`, `LIQ_BLUE = "rgba(37,99,235,.22)"` vào `svg_lib.py` của bài (thư viện đang chép
   theo từng bài) → thay hằng/inline; mặt thoáng nét đậm cùng màu.
2. `python3 build_figs.py` → chụp từng hình 375 px sáng + tối; nhãn/điểm trong chất lỏng đọc được.
3. Commit từng bài; đăng bằng `bash scripts/cap-nhat-ly-thuyet.sh <file> <lesson_id>` **sau 22h**.

Thứ tự gợi ý: L10 Khối lượng riêng–Áp suất chất lỏng → HSG9 CĐ11 Cơ học chất lưu → L12 Ch.1–2 (thuỷ ngân, chuyển thể,
khí) → L9/HSG9 khúc xạ (nước) → L11 thực hành tốc độ âm → còn lại.

**Chặng 3 — ngân hàng câu hỏi (`question_bank`)**
- Ảnh đề scan/PNG: **không đổi** (là đề thật, giữ nguyên).
- Hình SVG Claude vẽ qua `ve-hinh-cau-hoi`/`anh-xau-ngan-hang`: hình mới theo quy ước ngay; hình cũ chỉ sửa khi rà
  chương đó (sửa cả `question_bank` lẫn `exams.questions`, theo mục "Sửa hàng loạt câu" trong AGENTS.md, sau 22h).

**Chặng 4 — clip/SVG chuyển động, bản chiếu trên lớp (`tren-lop.html`)**
- Theo quy ước khi làm mới; bản cũ sửa khi bài đó được rà.

## 4. Cách kiểm
- Sau mỗi đợt: `grep` hằng `WATER|OIL|HG` trong `build_figs.py` đã chuyển sang `LIQ_*`.
- Chụp 375 px sáng + tối: chữ/điểm nằm trong chất lỏng còn đọc được; hai chất lỏng phân biệt được khi in xám
  (nhờ chữ tên chất + nét mặt phân cách).
- Thầy chiếu thử một bài thật (ống chữ U bài 154) trên tivi lớp: màu đỏ/xanh 0,22 có đủ rõ không — chưa rõ thì nâng
  `LONG_OP` (một chỗ, mọi hình đổi theo).
