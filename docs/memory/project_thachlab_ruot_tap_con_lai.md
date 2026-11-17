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

**16/11/2026 (nhánh `claude/sach-in-web-dot-3-9872b7`, vào main):** (1) L12 Ch.4 bài 15–18 sang bố cục mới — tr.8–9 Bài tương tự giải vào vở (b15, b18: 6 dạng × 2; b16, b17: 5 × 2), sửa bài 10–11, làm lại + QR 12; quyển 60 tr. (2) HS ảo lượt 2 cho 5 quyển đợt 3 + L12 Ch.4: lỗi A chỉ còn 3 (L10 b16 tiêu đề đếm sai đặc điểm, L12 b15 thiếu N_A/MeV→J ×2), ~70 lỗi B — đã sửa hết bằng subagent trong phiên (không gửi về phiên bài), lỗi ghi ở `scripts/ruot-tap/out/loi-hs-ao-2/` (chỉ trên Mac). (3) L10 b18 tr.63, L11 b6 D1/D2 xong. 6 quyển dựng sạch, 0 tràn. **Còn:** thầy in thử; L12 b15–18 còn Helvetica (Hy Lạp/★/chỉ số trên trong SVG `hinh-ch4.mjs` + chú thích ảnh p–p, chung với bài 14); bài 14 Bài tương tự vẫn kiểu làm tại chỗ (chưa `vo`); L12 b15–18 tr.1–6 dư 20–46 mm (có từ trước); điểm chờ thầy: L11 b13 D4/D5 và L10 b5/b12 gộp nhiều ý một dòng để giữ trang, L10 b1 bảng ghi "TB" thay "Trung bình".

**17/11/2026 — bộ in thử đồng bộ:** dựng lại cả 15 quyển (L10 Ch.1–7, L11 Ch.1–4, L12 Ch.1–4) từ main trong ~3 phút, chép về MỘT chỗ cố định `/Users/MAC/Projects/thachlab/scripts/ruot-tap/out/ruot-tap-vl<lớp>-chuong<N>.pdf` (checkout chính, gitignore, 36 MB). Số trang: L10 36·108·120·60·36·24·24; L11 84·96·72·60; L12 48·48·96·60 = 972 tr. Sạch phông cả 15 quyển (L12 Ch.4 hết Helvetica 17/11 nhờ `ky-tu-in.mjs`); bài 14 tr.1 báo dư −1 mm (chữ không bị cắt). Dựng lại: chạy lần lượt `scripts/ruot-tap/dung-*.sh` rồi chép vào thư mục trên.

**17/11 — in THEO HỌC KÌ** (thầy yêu cầu): `bash scripts/ruot-tap/dung-hoc-ki.sh [vl12-hk1 …]` → 6 quyển `out/ruot-tap-vl<lớp>-hk<1|2>.pdf`, số trang liền cả quyển (BOOK_PAGE_START). Chia: VL10 HK1 Ch.1–3 (264 tr) · HK2 Ch.4–7 (144) · VL11 HK1 Ch.1–2 (180) · HK2 Ch.3–4 (132) · VL12 HK1 Ch.1–2 (96) · HK2 Ch.3–4 (156) — thầy chốt Ch.3 sang HK2. Mỗi quyển +2 trang đầu không số (muc-luc.mjs: mục lục + trang trống). Trường chia khác → sửa hàm `quyen`. Bản theo chương cũ cất ở `out/theo-chuong-cu/` (thư mục chung). ℰ → chữ E phông KaTeX_Caligraphic qua `ky-tu-in.mjs`.
**17/11 (chốt cuối)** — thầy chọn: VL10 in theo học kì (2 quyển 266·146 tr); VL11, VL12 MỖI CHƯƠNG MỘT QUYỂN (VL11 86·98·74·62, VL12 50·50·98·62 tr, đã gồm 2 trang mục lục). Cả 10 quyển: `bash scripts/ruot-tap/dung-hoc-ki.sh`. L12 Ch.4 in là bài 17–21 (file vẫn bai14–18.mjs). Thư mục chung `out/`: 10 quyển đang dùng + `vl12-bai14` lẻ; bản cũ ở `out/ban-cu/`. Chưa in thử giấy.
