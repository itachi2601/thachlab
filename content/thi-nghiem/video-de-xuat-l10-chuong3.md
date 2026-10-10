# Video đề xuất — Lớp 10 · Bài 13 "Tổng hợp và phân tích lực" (thầy chốt 7/10/2026)

Phạm vi đợt này: **chỉ** bài `l10-tong-hop-phan-tich-luc` (lesson 58, Chương 3 Động lực học).
Ba chỗ: 1 clip mở bài + 2 hộp thí nghiệm (`tn-l10-tonghopluc-01`, `tn-l10-tonghopluc-02`).
Ví dụ đèn treo hai dây (`tn-l10-tonghopluc-03`) là `vi_du`, không có hộp `.tl-box--exp`, nên không gắn clip.

Cách duyệt (thầy chốt 6/10/2026): agent tự chấm theo V1–V7 và ghi cột `Cờ`;
thầy soát mẫu + mọi dòng có cờ, điền `Duyệt?` = `x` cho dòng nhận, ghi `start–end` nếu muốn cắt khác.
Chưa điền thì không nhập. Nhập bằng `scripts/nhap-video-de-xuat.mts` — không chép tay id.

Đã kiểm oEmbed (link sống, nhúng được) ngày 7/10/2026 cho clip đề xuất. Mốc cắt ước từ storyboard
(11 tấm, mỗi tấm khoảng 17 giây trên clip dài 3:08), chưa nghe tiếng.

## Bảng

| # | Bài | Vị trí | Link | Kênh | Thời lượng | Nhãn | Nhìn vào | Cờ | Duyệt? | start–end |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | l10-tong-hop-phan-tich-luc | mo_bai | KHÔNG CÓ | — | — | — | — | Tình huống sân băng, hai dây kéo một xe là giả định. Không có clip quay đúng cảnh đó (xe đi chậm hơn khi hai dây mở rộng) mà không giải thích. Clip "Pulling a Car out of the Ditch" (6RuJ-SV1pEk, 21 s, Prof. Liepe) là hiện tượng khác: kéo ngang một dây gần thẳng thì lực căng rất lớn — gần ví dụ đèn treo, và tự nó đã lộ mẹo, nên không đặt trước câu dự đoán (V7) |  |  |
| 2 | l10-tong-hop-phan-tich-luc | tn-l10-tonghopluc-01 | https://www.youtube.com/watch?v=4duh8FCeRwM | Bảo Nguyên Huỳnh | 3:08 | hai lực kế, thước đo góc | Hai lực kế kéo lệch nhau. Dây treo quả nặng nằm về phía nào so với góc giữa hai lực kế? | Đúng thí nghiệm bài 13: lực kế 5 N, thước đo góc, dây đồng quy, có quả nặng treo làm lực thứ ba. **Không phải ba lực kế** như chữ trong bài (lực thứ ba là quả nặng). Chỉ một góc, không quay lúc đổi từ 0° đến 180°. **Từ khoảng 2:30 trở đi là hình vẽ hình bình hành (lộ quy tắc) rồi logo CapCut → phải cắt trước.** Mốc 0:50–2:15 ước từ storyboard, chưa nghe thuyết minh | x | 0:50–2:15 |
| 3 | l10-tong-hop-phan-tich-luc | tn-l10-tonghopluc-02 | KHÔNG CÓ | — | — | — | — | Không có clip lực kế giữ vật đứng yên trên ván nghiêng, số chỉ tăng theo góc. Clip gần nhất (Axv5m7E0hkc, Labkafe, 7:43) là con lăn + ròng rọc + quả cân, tiếng Anh, hình đã ghi sẵn F = mg sin θ, phần lớn là lắp dụng cụ và vẽ đồ thị — không dùng |  |  |

## Đã xem, không đưa vào bảng

| Clip | Vì sao bỏ |
|---|---|
| ZR3svziA6OU (Nguyen Thi Hong, 5:01) | Cùng kiểu thí nghiệm lực kế, nhưng chữ đỏ che gần hết hình |
| 5qqSS2ZWLEU (nhi tran, 3:12) | Mô phỏng có sẵn đáp án, không phải thí nghiệm thật |
| 2qrTP2-zDq8, 9w-ORd14Ucs | Bảng viết / thầy nói, không có lực kế trên mặt nghiêng |
| 8PuQPsWP_mw (30 s) | Lực kế đo ma sát trên mặt ngang, không phải thành phần trọng lực |
| zEkECy_lUw8 (48 s) | Hai em nói rồi kéo một tấm ván, không đọc lực kế theo góc |
| 6RuJ-SV1pEk (21 s) | Kéo xe khỏi rãnh: lực căng dây gần thẳng, không phải hai dây kéo một xe |

## Đã chốt (7/10/2026)

Dòng 2: thầy chốt, cắt 0:50–2:15. Dòng 1 và 3 không có clip, bỏ qua.

```
npx tsx scripts/nhap-video-de-xuat.mts content/thi-nghiem/video-de-xuat-l10-chuong3.md --ra /tmp/kho-thu
npx tsx scripts/chen-video-thi-nghiem.mts --kiem --kho /tmp/kho-thu
npx tsx scripts/nhap-video-de-xuat.mts content/thi-nghiem/video-de-xuat-l10-chuong3.md --apply
npx tsx scripts/chen-video-thi-nghiem.mts --kiem --apply
npx tsx scripts/chen-video-thi-nghiem.mts --bai l10-tong-hop-phan-tich-luc --apply
bash scripts/cap-nhat-ly-thuyet-hang-loat.sh l10-tong-hop-phan-tich-luc:58 --chi-video
```
