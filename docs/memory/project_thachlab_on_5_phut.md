---
name: project_thachlab_on_5_phut
description: Ôn 5 phút (thẻ lật + lịch ôn giãn cách từng thẻ) + rút Bài toán mẫu trong lý thuyết — thử L11 bài 22–24, code+migration đã vào main/chạy 25/11/2026, CHƯA deploy, chưa triển khai các bài khác
metadata:
  type: project
---

**Mục tiêu (thầy 25/11/2026):** (1) mỗi bài có bản ôn thu gọn có tương tác để HS tự nhớ lại sau khi học, có lịch ôn lại đúng lúc sắp quên (học theo Duolingo); (2) xử lý mục "V. Bài toán mẫu" trong lý thuyết nay trùng Bài tập mẫu (100/120 bài có, ~15% số chữ).

**Đã xong (tất cả đã vào `main` 25/11, commit cuối `10ead635d`):**
- Rút thẻ: `scripts/on-tap/rut-the-on.py <slug>` đọc `content/lesson-samples/<slug>/theory.html` → `content/on-tap/<slug>.json`: thẻ lật từ ô Chốt mục 🎯 (`.tl-box.tl-keep.tl-chot`), thẻ chọn từ câu đầu hộp bẫy (`.tl-quiz`, bỏ dòng ⚠, đổi id `on-`), ≤2 thẻ "Nhìn hình" từ hình mục II; hình SVG ≤20 KB cùng tiểu mục gắn vào thẻ; đáp án tách `<ul>` (thầy chốt: ý khác nhau xuống dòng, không nối "·"). Mỗi thẻ `id` = sha1(neo)[:8] → sửa chữ câu hỏi = thẻ mới (mất lịch cũ của thẻ đó).
- Component `components/lessons/OnNamPhut.tsx` (+ `.module.css`): thẻ lật 3D; **trước khi lật phải gõ ≥2 ký tự chữ khoá hoặc bấm "Chưa nhớ ra" (= Quên)**, mặt sau hiện "Em ghi:" cạnh đáp án; tự chấm Nhớ rõ/Lơ mơ/Quên; thẻ Quên/Lơ mơ quay lại sau 3 thẻ, **chỉ 1 lần** (2 lần → lượt 7 thẻ dài 19, quá N5; giờ ≤14); kết quả + lịch tính theo lần GẶP ĐẦU. Đăng nhập → ghi `on_tap_ghi` lúc hết lượt, màn đầu hiện "Ôn N thẻ đến hạn"/"lần tới: dd/m"; khách → localStorage như cũ. Prop `tron` cho lượt trộn nhiều bài.
- DB: migration `20261125120000_on_tap_lich_on` **ĐÃ CHẠY 25/11 10:34** (thử trong giao dịch rollback trước; kiểm: RLS bật, 0 policy, chỉ authenticated execute). Bảng `on_tap_the` (user_id, slug, the_id, bac 1–5, han_on, lan_on, lan_quen), RPC `on_tap_ghi(p_slug, p_ket_qua jsonb)`, `on_tap_den_han(p_limit)`, `on_tap_trang_thai(p_slug)`. Bậc 1–5 = 1/3/7/21/60 ngày; Quên → bậc 1; **Nhớ rõ chỉ lên bậc khi đã tới hạn** (ôn lại nhiều lần trong ngày không leo bậc ảo); trần 5.000 thẻ/tài khoản.
- Trang `/lop-hoc/on-the` (`app/lop-hoc/on-the/page.tsx`): ≤8 thẻ đến hạn, trộn xen kẽ theo bài; loader `content/on-tap/index.ts` (slug → import, thêm tay từng dòng).
- Xem thử: `/dev/on-tap?bai=22|23|24` (đã thử 375px khi CHƯA đăng nhập).
- Bài toán mẫu: trùng dạng → giữ đề + bảng phân tích, thay lời giải bằng hộp "Tự giải trước, rồi so đáp số" + link `#muc=bai-tap-mau&dang=N`; không trùng dạng → chuyển thành dạng mới rồi mới rút; bài thực hành → bỏ. Đã sửa nguồn bài 22 (→ D5), 23 (→ D4, D5); bài 24 (lesson 43) thiếu dạng "I = E/(R+r), U, đoản mạch" → để nguyên. Code link dạng: `lesson-nav.ts`, `page.tsx` applyHash, `WorkedQuestionsGrid.tsx`.

**Đặt ở đâu — THẦY ĐÃ CHỐT 2026-11-25 (như đề xuất, làm theo đúng 1–3 dưới đây):**
1. **Trong trang bài — một thẻ thu gọn ngay cuối mục Lý thuyết, trước Bài tập mẫu** ("Ôn 5 phút · 7 thẻ · Bắt đầu"). Lý do: truy xuất ngay sau khi đọc (L1), đúng mạch học; KHÔNG làm tab riêng (thêm một chỗ điều hướng, HS 14–18 ít bấm sang — N2). Mở thẻ mới nạp JSON (`next/dynamic` + chunk riêng, không đụng tải ban đầu của `/lop-hoc/bai`).
2. **Trang lớp `/lop-hoc` — MỘT dòng ngay dưới "Học tiếp", cùng chỗ `<ReviewBanner compact />`** (`app/lop-hoc/page.tsx` ~dòng 887): "🔁 N thẻ đến hạn ôn → /lop-hoc/on-the", chỉ hiện khi N>0. Số N phải gộp vào RPC dữ liệu trang lớp (không thêm round-trip); không banner, không huy hiệu (B2, L3, G2).
3. Không đặt ở trang chủ `/` công khai, không thông báo đẩy. Sau này cân nhắc: gợi ý "Ôn thẻ bài này" trước khi vào đề kiểm tra của bài.

**Triển khai cho mọi bài (kế hoạch, chưa làm):**
- Điều kiện: bài có ô Chốt mục. Hiện 81/122 bài: L10 34/34, L11 26/26, L12 21/23; 41 bài còn lại (HSG9, KHTN, AVCN, CNC…) chưa có → bỏ qua hoặc làm Chốt mục trước.
- Chặng A — rút hàng loạt: chạy script cho 81 slug; đổi `content/on-tap/index.ts` thành file SINH TỰ ĐỘNG (script quét thư mục), và ghi thêm `lesson_id` vào JSON (bundle.json chỉ có class_name + lesson_title → tra `lessons` qua REST) để trang bài tìm bộ thẻ theo lesson_id. JSON hiện ~20 KB/bài (phần lớn là SVG) — chấp nhận được vì nạp lười.
- Chặng B — soát: agent `kiem-code` đọc từng JSON (≤8 thẻ, bỏ thẻ trùng ý, thẻ "Nhìn hình" phải có đáp án rõ, KaTeX render được); lô nghi ngờ đưa thầy duyệt kèm link `/dev/on-tap?bai=…` (mở rộng trang dev đọc từ index).
- Chặng C — gắn vào trang bài (vị trí 1) + dòng ở `/lop-hoc` (vị trí 2, cần sửa RPC trang lớp = migration mới).
- Chặng D — deploy, rồi thử bằng tài khoản HS thật: làm lượt ôn → kiểm `on_tap_the` có dòng, hôm sau `/lop-hoc/on-the` có thẻ đến hạn.
- Thứ tự với bài toán mẫu: deploy code TRƯỚC rồi mới `cap-nhat-ly-thuyet.sh` bài 22, 23 (sau 22h). Rút bài toán mẫu cho các bài khác là việc riêng, làm theo 3 loại ở trên.

**Còn treo:** CHƯA deploy; chưa thử khi đăng nhập; nền tối chưa kiểm; thầy chưa duyệt giao diện thẻ lật (vị trí đặt đã chốt 25/11); chưa cập nhật lý thuyết bài 22, 23 lên DB.
**Cách đo (đề xuất):** tỉ lệ Nhớ rõ ở lần ôn ngày 7 (thẻ có gõ chữ khoá trước vs không), tỉ lệ HS quay lại lượt ôn sau 1 ngày — đọc từ `on_tap_the` (`lan_on`, `lan_quen`, `bac`).
