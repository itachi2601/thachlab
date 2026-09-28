# Đeo danh hiệu dưới tên + khung sưu tập huy hiệu — nghiên cứu thiết kế

Ngày 28/9/2026. Mockup trực quan: xem artifact "Huy Hiệu Sưu Tập ThachLab" (link trong hội thoại).

## 1. Hiện trạng (đã có gì, thiếu gì)

| Việc | Trạng thái | Ở đâu |
|---|---|---|
| Chọn 1 danh hiệu để "đeo" | **Đã có** | `profiles.display_title_code/level`, RPC `rank_set_display_title`, nút "Đeo danh hiệu" trong `TitleCollection.tsx` |
| Hiện danh hiệu đang đeo (dạng chữ) | Đã có | `RankCard`, `RankPage` (đầu trang), chip bạn cùng lớp `ClassRankGroups` |
| Hiện **dưới tên** ở khung chào trang HS | **Chưa** | `ThptStudentHome.tsx:298-306` chỉ có tên + "Lớp …" |
| Hiện ở bảng top tuần | Chưa | RPC `rank_class_board` không trả `title` |
| Logo riêng từng danh hiệu | **Chưa** | `TitleCollection` dùng icon chung Sparkles/Lock |
| Ảnh huy hiệu đã vẽ | **96 PNG đủ bộ** (32 chuyên môn × 3 mức, xong 28/9) + 7 PNG rank | `~/Downloads/thachlab-huy-hieu-96/` (gom từ design system Cowork), **chưa đưa vào repo** |
| 13 danh hiệu bộ sưu tập + thành tích | Chưa có cả spec ảnh | — |
| Cột icon trong `rank_titles` | Không có | ánh xạ code → file để ở client |

Kết luận: phần "đeo" chỉ cần **nối dây thêm 2 chỗ**; phần "khung sưu tập" là việc mới nhưng không cần migration ở giai đoạn 1.

## 2. Đề xuất A — danh hiệu đeo hiện dưới tên

Component chung `WornTitle` (icon 16–20px + tên + mức), thay cho 3 chỗ đang tự viết chữ + Sparkles.

- **Khung chào trang HS**: dòng 2 = danh hiệu đang đeo (màu theo mức), dòng 3 = "Lớp 12A1". Chưa đeo → giữ nguyên như hiện nay, không hiện chỗ trống.
- **Chip bạn cùng lớp** (`ClassRankGroups`): thay Sparkles bằng icon huy hiệu 14px thật.
- **Top tuần** (`ClassRankBoard`): thêm `title` vào RPC `rank_class_board` (giống `rank_class_groups` đã có) → hiện dưới tên.
- **Trang Kết quả / phụ huynh**: `RankCard` đã có, chỉ đổi sang `WornTitle`.

Màu theo mức (đã dùng trong bộ PNG): Thức Tỉnh = lam-cyan · Làm Chủ = bạc-xanh · Huyền Thoại = tím-vàng. Danh hiệu bộ sưu tập / thành tích (không có mức) = vàng.

## 3. Đề xuất B — khung sưu tập cạnh rank

**Vị trí**: (1) trang HS, ngay dưới `RankCard` (mobile) hoặc cạnh phải (desktop ≥ 640px); (2) đầu trang `/lop-hoc/xep-hang`, dưới thẻ bậc; (3) bấm vào tên bạn cùng lớp → popover xem khung của bạn.

**Nội dung**: chỉ danh hiệu **đã mở**, mỗi cái 1 ô 32px (mobile) / 40px (desktop), lấy đúng PNG của mức cao nhất đang có. Danh hiệu đang đeo có vành sáng. Ô "+N" khi quá 2 hàng trên mobile, bấm mở toàn bộ (= trang xếp hạng). Chưa mở danh hiệu nào → dòng "Chưa có huy hiệu — làm bài có gắn chủ đề để mở" (không hiện lưới ô khoá, tránh trống trải).

**Thứ tự trong khung**: đang đeo → Huyền Thoại → Làm Chủ → Thức Tỉnh → bộ sưu tập/thành tích; cùng mức thì mới nhận trước. Không cần HS sắp tay ở giai đoạn 1.

**Giai đoạn 2 (tuỳ chọn)**: cho HS **ghim tối đa 6** huy hiệu lên hàng đầu khung (kiểu showcase Steam / Genshin). Cần cột `profiles.pinned_titles jsonb` + RPC `rank_set_pinned_titles` + trả `pinned` trong `rank_status_of`/`rank_class_groups`. Chỉ làm khi HS thật sự có > 8 danh hiệu, hiện tại mùa thử nghiệm chưa cần.

## 4. Ảnh huy hiệu — cách đưa vào code

- **Đã có sẵn từ commit 39c71b76 (PR #15, 28/9/2026):** `public/images/rank/titles/cm-<slug>-<mức>.webp` 512px (96 file, 3,3 MB) + `features/rank/badge-assets.ts` (`SPECIALIST_SLUG` ánh xạ `rank_titles.code` → slug, `titleBadgeSrc`, `titleBadgeLockedSrc`). Đợt này bổ sung `SINGLE_SLUG` (13 danh hiệu bộ sưu tập/thành tích), `titleBadgeDisplaySrc` (mọi trạng thái), `levelTextColor`. Không tạo bộ ảnh thứ hai.
- Chưa có ảnh (13 danh hiệu bộ sưu tập/thành tích) → **fallback lục giác vàng có sao**, để khung không bị lỗ hổng.
- 7 PNG rank **không** thay `RankBadge.tsx` (huy chương SVG đã chốt) — chỉ dùng PNG cho danh hiệu.

## 5. Lộ trình

| Bước | Việc | Migration | Ước lượng |
|---|---|---|---|
| 1 | ~~Đưa PNG vào repo~~ (đã có ở PR #15) + `SINGLE_SLUG`/`titleBadgeDisplaySrc` + fallback | Không | xong 28/9 |
| 2 | `WornTitle` + gắn vào khung chào, chip lớp, RankCard, RankPage | Không | cùng phiên |
| 3 | `TitleShowcase` (khung sưu tập) ở trang HS + trang xếp hạng, dùng `rank_my_titles` sẵn có | Không | 1 phiên |
| 4 | `title` trong `rank_class_board` + popover xem khung của bạn (`rank_titles_of`, kiểm tra policy cho bạn cùng lớp) | Có (sửa RPC) | 1 phiên, thầy chạy migration |
| 5 | Ghim 6 huy hiệu | Có | chờ nhu cầu |
| 6 | Vẽ 13 PNG bộ sưu tập/thành tích (32 chuyên môn đã xong 28/9) | — | thầy làm trên Cowork |

Rủi ro cần thầy quyết:
- 13 danh hiệu bộ sưu tập/thành tích chưa có hướng vẽ nào — đề xuất cùng khung lục giác nhưng nền vàng (không phân mức), cần bổ sung spec vào design system trước khi vẽ.
- 4 danh hiệu chưa gắn chủ đề (Photon, Nguyên tử, Máy biến áp, Cân bằng nhiệt) sẽ không bao giờ xuất hiện trong khung của ai — nên gắn chủ đề hoặc ẩn hẳn.

## 6. Soát bộ 96 ảnh (28/9/2026)

- 96/96 file 1024×1024 RGBA, nền trong suốt; thân huy hiệu 814px (Thức Tỉnh/Làm Chủ) và 912px (Huyền Thoại, do tia/cánh tràn lề) — đúng spec.
- 26 danh hiệu mới khớp phong cách 6 cái cũ; biểu tượng đợt mới nét mảnh hơn một chút, không cần vẽ lại.
- Ở 40px và 32px vẫn nhận ra khung + màu; ở 20px chỉ còn màu. Nhiều danh hiệu trùng tông (6 vàng, 8 lam-ngọc, 3 bạc) → **luôn kèm tên khi chạm/hover**, chip 14–20px bắt buộc có chữ.
- Ba mức chỉ khác khung → cỡ nhỏ phải ghi mức bằng chữ hoặc màu chữ.
