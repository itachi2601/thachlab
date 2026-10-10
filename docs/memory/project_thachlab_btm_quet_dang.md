---
name: project_thachlab_btm_quet_dang
description: Bài tập mẫu — quét dạng → nháp → soạn lại → kiểm chéo → đăng; tiến độ tới 2026-10-10 (L12 24 bài + L11 20–44 + L10 49–57 & 58–66 đã ghi DB); việc treo: bài 38/43/45, L10 đợt B (68–79), bài 10 L12
metadata:
  node_type: memory
  type: project
  modified: 2026-10-10
---

**Mục tiêu:** bài tập mẫu có số dạng theo lý thuyết + ngân hàng câu hỏi cùng chủ đề (2–6 dạng, cấp 1–4 không giảm). Thứ tự: quét dạng → nháp (batch Opus) → builder Sonnet soạn lại (`scripts/data/bai-tap-mau/build-hinh-<id>.py` → `<id>.json`) → kiem-code tự giải độc lập → sửa → kiểm lại bài sửa nhiều → đặt `review.checked` → đăng (`dang-btm` qua `tao-muc-bai-tap-mau.mts --mau 224` + `publish-bai-tap-mau.mts --yes`, tab terminal Mac).

**Đã ghi DB tới 2026-10-10 (commit `9accb4478`, `f54afa7b9`, skill nhật ký `ddb2d46be`):**
- L12: bài 2,3,4,6,7,8 (đợt 1, `ce07b6902`, `scripts/dang-btm-l12-dot1.sh`+`dot1b.sh`); 9,11,13,14,15,16 (đợt 2, `32a3f6ec5`, `dang-btm-l12-dot2.sh`); 17,18,19,125,126,127 (đợt 3, `9e603f556`, `dang-btm-l12-dot3.sh`) — tất cả ghi 10/10, sao lưu `scripts/logs/bai-tap-mau-bai<id>-*.json`. Bài chưa có mục `bai_tap_mau` (6,7,8,9,15,16,17,18,19) phải `tao-muc-bai-tap-mau.mts --lesson <id> --mau 224` trước `publish` (script đăng đã gồm bước này).
- L11: 20–26, 27,28,30–33 (ghi 9/10, backup trong `scripts/logs`); 35,36,37,39,40,41,42,44 (ghi 10/10). 5–6 dạng/bài. Bài 40 là bản ghép (nền `40.json` của phiên kia + dạng 3 của builder; bản v2 ở `old/40.v2.json`).
- L10: 49,50,52–55,57 đã có; **58,60,62,63,66 (đợt A, commit `aca5b2add`) ĐÃ ĐĂNG 2026-10-10** bằng `scripts/dang-btm-l10-dotA.sh` (dạng cũ 20/13/?/8/15 đã sao lưu `scripts/logs/bai-tap-mau-bai<id>-*.json`, đã nằm trong `tu_luan` nên không dùng `--giu-cu`).
- Lý thuyết L11 bài 23,26,28,29,30,34: học sinh ảo → API sửa → kiểm chéo → đã đăng (10/10); dòng hang-doi đã `da-dang`.

**Còn chờ:**
- Bài 38, 43, 45 (L11): quét dạng báo "không có chủ đề nguồn" (0 câu ngân hàng) → thầy chọn: bổ sung ngân hàng hay gắn YCCĐ riêng. Dạng 1–2 bài 44, dạng 1 bài 35/42 đang gắn chủ đề cha.
- L10 còn chưa soạn BTM: **đợt B = 68–74, 76–79 (11 bài, có chủ đề ngân hàng, chạy tuần tự khi thầy bảo)**. Thầy chốt 2026-10-10: BỎ đợt E (59, 61, 64, 38, 46 — 0 chủ đề) và đợt F (thực hành/đặc biệt: 47, 48, 51, 56, 65, 67, 75, 29, 34, 45, 5, 12). Hỏi trước khi chạy: phiên "[96babb]" có đang đụng L10 không (đã xảy ra đụng L11: hai phiên cùng soạn 35–44, thầy bảo để phiên kia làm, phiên này dừng).
- Bài 10 (L12) vẫn bản 4 dạng cũ (soạn lại được, 1 bài); bài 5, 12 (thực hành L12) thầy chốt BỎ.
- Chưa xem lại bằng mắt vài hình sau lần sửa cuối: bài 44 dạng 3,5; 41 dạng 4,5; 42 dạng 3; 39 nhãn dạng 4.
- Chưa deploy lý thuyết (L10 25 bài + L11 6 bài ghi DB nhưng `public/data` sinh lúc build); BTM đọc DB lúc chạy nên không cần deploy. `docs/STATE.md` còn ghi L11 20–33 "chưa đăng" (sai) — cập nhật.
- Trợ giảng rà trên web (lý thuyết + BTM mới).
- HSG: migration `20261010200000` + `dang-hsg9-dot1.sh` chưa chạy (việc phiên khác).

**Quyết định đã chốt:**
- Chạy tuần tự từng đợt 5–6 bài (builder Sonnet song song + 1 kiem-code mỗi bài); builder đọc `brief` chung (hướng dẫn nhân ra + danh sách lỗi hay gặp) để tiết kiệm prompt; sửa theo kiểm chéo bằng SendMessage cho đúng builder cũ.
- Ô nhập đáp số luỹ thừa 10: `hoi` ghi "(nhập hệ số a của kết quả a·10ⁿ)", `don_vi` "×10ⁿ …" — UI chỉ chấm hệ số a (mất bẫy lệch bậc); chưa xác nhận giao diện hiển thị ổn trên web (bài 17, 127).
- Lỗi hay gặp ở 29/29 bài kiểm chéo: lộ đáp số/hướng giải ở loi_hay_gap, vi_sao (so sánh lớn/nhỏ, chiều), ô ⚠ + hàng bảng phân tích, nhan_dang, lựa chọn ĐÚNG của chon_buoc_ke chứa kết quả; `\t` trong chuỗi Python thường thành TAB (validate.mts không bắt); `\"` thừa trong raw string; lệch số hiển thị do làm tròn sớm; tu_luan cũ sai số/phụ thuộc hình thì BỎ.
- Còn lưu ý riêng (tự luận có ảnh Supabase chưa ai xem: bài 14, 58, 125, 127; mô phỏng D4 bài 66 vẫn cho thấy thanh nghiêng; bài 63 tu_luan chỉ còn 1 bài; bài 19 cả 6 dạng `form=ly_thuyet` vì ngân hàng thiếu bai_tap; bài 13 bỏ chủ đề thanh dẫn Blv — thầy quyết bổ sung lý thuyết hay không; bài 126/127 chưa có YCCĐ riêng).
- Model: quét = Sonnet 5.5 medium; nháp/viết = Opus 5.5 high (batch) hoặc builder Sonnet song song; kiểm chéo = kiem-code Sonnet; không dùng Haiku.
- Nguồn dạng: lý thuyết bài + `question_topics`/`question_bank`; dạng không có câu dùng `form=ly_thuyet`.
- Kiểm chéo xong MỚI đặt `review.checked`.
- `build-hinh` ghi `tu_luan` qua `re.sub` chỉ đổi `&gt;`; sau build luôn quét JSON `$…$` có `<`/`>`.

Liên quan: [[project_thachlab_cap_nhat_bai_theo_gemini]], [[project_thachlab_anthropic_credit]].
