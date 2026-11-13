---
name: project_thachlab_ruot_tap_con_lai
description: Kế hoạch ruột tập (sách in theo bài) cho mọi chương còn lại L10/L11/L12 — 65 bài, 3 đợt phiên song song, phân model
metadata:
  type: project
---

Lập 12/11/2026 (nhánh `claude/sach-in-tu-web-chuong-3-5ffba2`). Quy trình: skill `sach-in-tu-web` mục "Ruột tập cả chương bằng phiên song song".
Đã xong trước đó: L12 Ch.4 (bài 14–18), L10 Ch.4 (23–27), L11 Ch.3 (16–21). Sách A4 cả chương (book/make.py) có L10 Ch.2, Ch.3 — khác ruột tập.

**Đã chuẩn bị (vào main 12/11):** hồ sơ `book/sach/<mã>.json` cho mọi chương (bỏ bài Kiểm tra; `l11-ch2-song` thêm lesson 34) +
script dựng quyển `scripts/ruot-tap/dung-l<lớp>-chuong<N>.sh` cho 12 chương.

| Đợt | Chương (mã hồ sơ) | Bài · lesson_id | baiDau |
|---|---|---|---|
| 1 | L10 Ch.5 `l10-ch5-dong-luong` | 28·73, 29·74, 30·75 (TH) | 28 |
| 1 | L10 Ch.6 `l10-ch6-chuyen-dong-tron` | 31·76, 32·77 | 31 |
| 1 | L10 Ch.7 `l10-ch7-bien-dang-ap-suat` | 33·78, 34·79 | 33 |
| 1 | L11 Ch.4 `l11-ch4-dong-dien` | 22·41, 23·42, 24·43, 25·44, 26·45 (TH) | 22 |
| 2 | L12 Ch.1 `l12-ch1-vat-li-nhiet` | 1·2, 2·3, 3·4, 4·5 (TH) | 1 |
| 2 | L12 Ch.2 `l12-ch2-khi-li-tuong` | 5·6, 6·7, 7·8, 8·9 | 5 |
| 2 | L12 Ch.3 `l12-ch3-tu-truong` | 9·10, 10·11, 11·12 (TH), 12·13, 13·14, 14·125, 15·126, 16·127 — file `l12-c3-bai<N>.mjs`, `out` `ruot-tap-vl12-c3-bai<N>.pdf` (14–16 trùng số Ch.4) | 9 |
| 3 | L10 Ch.1 `l10-ch1-mo-dau` | 1·46, 2·47, 3·48 (TH) | 1 |
| 3 | L10 Ch.2 `l10-ch2-dong-hoc` | 4·49 … 12·57 (6·51, 11·56 TH) | 4 |
| 3 | L10 Ch.3 `l10-ch3-dong-luc-hoc` | 13·58 … 22·67 (20·65 bài giải mẫu, 22·67 TH; không BTM) | 13 |
| 3 | L11 Ch.1 `l11-ch1-dao-dong` | 1·20 … 7·26 | 1 |
| 3 | L11 Ch.2 `l11-ch2-song` | 8·27 … 15·34 (10·29 TH không BTM, 15·34 TH) | 8 |

**Phân model:** bài lý thuyết có bài tập mẫu → Opus (soạn nội dung HS, hình SVG, đáp số). Bài thực hành (TH) và L10 bài 1–2
(làm quen, an toàn) → Sonnet. HS ảo cả quyển sau mỗi chương → một phiên Sonnet đọc các `.pdf.html` (text), giao lỗi về phiên bài bằng `SendMessage`.
**Vì sao chia đợt:** đợt 1 = nội dung dạy HK2 sắp tới; lỗi lặp HS ảo bắt ở đợt trước đưa vào brief đợt sau (L11 Ch.3: 4 lỗi lặp).

**Trạng thái (12/11/2026 tối):** đợt 1 (12 bài) xong + HS ảo 4 quyển (0 lỗi A trừ 1 ở bài 26, ~45 lỗi B) → các phiên bài đã sửa, vào main. Đợt 2 (16 bài L12) xong, vào main, CHƯA qua HS ảo; bài 10 (lesson 11) có 3 chỗ cắt bớt chờ thầy quyết. 7 quyển dựng sạch: L10 Ch.5 36 tr, Ch.6 24, Ch.7 24, L11 Ch.4 60, L12 Ch.1 48, Ch.2 48, Ch.3 96 (`scripts/ruot-tap/out/ruot-tap-vl<lớp>-chuong<N>.pdf`, chỉ trên Mac). Còn: HS ảo đợt 2 (3 quyển, gửi lỗi về phiên `rt-l12-b<N>`/`rt-l12-c3-b<N>` qua list_sessions linked), sửa `khung.mjs` trang QR tràn 1 mm (rồi dựng lại mọi bài), đợt 3 (37 bài). Liên quan: [[project_thachlab_ruot_tap_bai14]], [[project_thachlab_sach_in_chuong2]].

**Đợt 3 (13/11/2026, phiên điều phối nhánh `claude/sach-in-web-dot-3-9872b7`):** khung sửa bộ đo trang 12 (−1 mm là báo giả do ô QR tuyệt đối; thực dư 22 mm, `c57259a59` vào main). Mở 37 phiên `rt-l10-b1…b22`, `rt-l11-b1…b15` (Sonnet: L10 b1–3, b6, b11, b22, L11 b10, b15; còn lại Opus). Còn: chờ các phiên vào main → dựng 5 quyển (`dung-l10-chuong1/2/3.sh`, `dung-l11-chuong1/2.sh`) → HS ảo mỗi quyển → gửi lỗi về phiên bài qua `SendMessage`. **13/11 tối:** 37/37 bài vào main, HS ảo xong 5 quyển (lỗi A: L10 b2,4,5,6,9,15,22, L11 b1 — đã sửa), mọi phiên đã sửa lỗi HS ảo. 5 quyển dựng sạch (0 tràn, pdffonts sạch), đã gửi thầy: L10 Ch.1 36 tr, Ch.2 108, Ch.3 120, L11 Ch.1 84, Ch.2 96. Còn: chờ thầy xem/in thử; chưa có lượt HS ảo thứ hai; điểm treo nhỏ: L10 b18 2 điểm tr.63, L11 b6 D1/D2 thiếu 1 dòng giải.

**13/11 khuya — đối chiếu:** 65/65 bài đã soạn (L10 b1–34, L11 b1–26, L12 b1–16 + Ch.4 b14–18 cũ) — không còn bài nào phải soạn. Mọi lỗi HS ảo đợt 1–3 đã có commit sửa trên main (L12 Ch.3 b12 không có lỗi A/B nên không cần). Từ nay HS ảo ghi lỗi từng bài ra `scripts/ruot-tap/out/loi-hs-ao/` (skill `sach-in-tu-web` bước 5). Còn: thầy in thử; lượt HS ảo thứ hai chưa chạy; L12 Ch.4 (b14–18) bố cục cũ chưa có Bài tương tự (trừ b14).
