---
name: so-do-tu-duy-chuong
description: Làm SƠ ĐỒ TƯ DUY tổng hợp MỘT chương (1 tâm + 3–5 nhánh, hình khoá, công thức lõi, ô tự kiểm, nối mô phỏng sẵn có) theo mẫu L12 Chương 3, gắn vào cuối chương trên trang lớp. Dùng khi thầy nói "làm sơ đồ tư duy chương X", "sơ đồ tư duy cho lớp 11", "/so-do-tu-duy-chuong". Chỉ code + nội dung tĩnh, không ghi DB; chạy được trên cloud.
---

# Sơ đồ tư duy chương

Mẫu chuẩn (thầy duyệt 11/11/2026): Vật lí 12 · Chương 3 Từ trường. Mở mẫu trước khi làm chương mới:
`npm run dev` → `/lop-hoc/so-do/?chuong=4&lop=lop-12` (hoặc `/dev/so-do-tu-duy`).

| Việc | File |
|---|---|
| Dữ liệu mẫu (chép khung từ đây) | `features/lessons/so-do-tu-duy/l12-chuong-3.ts` |
| Kiểu dữ liệu + hạn mức | `features/lessons/so-do-tu-duy/types.ts` |
| Sổ đăng ký `chapters.id` → file dữ liệu | `features/lessons/so-do-tu-duy/index.ts` |
| Hình khoá của nhánh (SVG tự vẽ) | `components/lessons/so-do/HinhNhanh.tsx` |
| Component (KHÔNG sửa khi chỉ thêm chương) | `components/lessons/so-do/SoDoTuDuy.tsx` + `.module.css` |
| Trang HS + dòng cuối chương | `app/lop-hoc/so-do/page.tsx`, `renderChapterSection` trong `app/lop-hoc/page.tsx` |

Thêm một chương = 1 file dữ liệu mới + hình khoá mới + 1 dòng trong sổ đăng ký. Dòng "Sơ đồ tư duy chương" tự hiện
ở cuối chương (trước bài Kiểm tra chương) khi `chapters.id` có trong sổ đăng ký; không đụng trang lớp.

## Quy trình

1. **Lấy id thật, không đoán.** `chapters.id`, lesson id, tên bài: đọc `public/data/catalog.json`
   (worktree không có thì đọc `/Users/MAC/Projects/thachlab/public/data/catalog.json`; cloud không có file thì tải `https://thachlab.id.vn/data/catalog.json`, không được thì hỏi thầy).
   Không dò DB.
2. **Đọc nội dung chương từ bài đã soạn**: `content/lesson-samples/<lớp>-*/bundle.json` (mục lý thuyết) của từng bài trong chương.
   Chỉ rút từ khoá, công thức, bẫy, mô phỏng — grep `phet.colorado.edu`, `tl-sim`, `youtube` để biết bài nào có mô phỏng/clip.
   Công thức, kí hiệu, quy ước góc phải **y như bài đã đăng** (HS thấy hai cách viết là rối). Không chép nguyên văn SGK.
3. **Chia nhánh** (đây là phần quyết định chất lượng):
   - 3–5 nhánh, đánh số theo thứ tự học; gộp bài cùng một ý lớn vào một nhánh (mẫu: 8 bài → 5 nhánh). Không "mỗi bài một nhánh" (G1, N2).
   - `tam`: 1–3 chữ nói quan hệ lõi của chương (mẫu: "Điện ⇄ Từ"). `mach`: một câu ≤ 20 chữ tóm cả chương.
   - `noiTiep` từ nhánh 2 trở đi: vì sao nhánh này nối nhánh trước, viết thành một hành động/nguyên nhân (B8). Thiếu `noiTiep` thì sơ đồ chỉ là mục lục.
   - Mỗi nhánh: `chot` ≤ 12 chữ; `ct` MỘT công thức lõi (ngắn, hiển thị không xuống dòng ở nút 190px — công thức dài thì chọn dạng gọn, dạng đầy đủ để ở ý con);
     đúng ≤ 4 `yCon` (`tu` ≤ 4 chữ, `y` một dòng **không chứa công thức cần nhớ** để ô tự kiểm che được, `ct` tuỳ chọn);
     `bay` đúng MỘT dòng — bẫy hay sập nhất, lấy từ hộp Bẫy của bài; `bai[]` đủ mọi bài của nhánh.
4. **Mô phỏng** (`moPhong`, mỗi nhánh tối đa một): chỉ dùng thứ **đã có trên web** trong chính các bài của nhánh.
   - PhET đã nhúng ở bài → `kieu: "phet"`, chép đúng `src` trong bài (đã kiểm `?locale=vi`); cần sim mới thì theo skill `phet` trước.
   - Mô phỏng/clip nội bộ trong bài (`.tl-sim`, hoạt hình, video) → `kieu: "bai"`, `href` về bài đó.
   - `nhiemVu` luôn bắt đầu bằng "Đoán trước: …" rồi mới thao tác (một đại lượng đổi → một hệ quả). Nhánh không có gì thì bỏ `moPhong`, không bịa.
5. **Hình khoá**: mỗi nhánh một hình trong `HinhNhanh.tsx` (viewBox `0 0 96 64`), thêm tên vào union `hinh` ở `types.ts`, vào `HINH` và `MO_TA`.
   - Một hình gợi lại cả nhánh, ≤ 3 nhãn chữ, cỡ chữ ≥ 10.5 trong viewBox (ra ≥ 13px ở 112px rộng — H4).
   - Màu theo quy ước chương đang dùng trong bài (L12 Ch.3: B xanh `#2563eb`, I cam `#ea580c`, F đỏ `#dc2626`; nam châm N đỏ – S xanh);
     chương khác: lấy đúng quy ước màu trong `build_figs.py`/hình của bài. Nét phụ `currentColor`. Đường sức nét đứt, mũi chevron.
   - Toạ độ tính bằng sin/cos phải `.toFixed(2)` (lệch số lẻ giữa máy chủ và trình duyệt gây lỗi hydration). Dùng lại `Mui` cho mũi tên.
6. **File dữ liệu** `features/lessons/so-do-tu-duy/l<lớp>-chuong-<n>.ts` (export `L<LỚP>_CHUONG_<N>`), rồi thêm đúng một dòng vào `SO_DO` trong `index.ts`:
   `<chapters.id>: () => import("./l11-chuong-2").then((m) => m.L11_CHUONG_2), // Vật lí 11 · Chương 2. …`
7. **Kiểm** (`npm run dev`, không `next dev`; gặp lỗi "next/font/google queries have exactly one entry" thì xoá `.next/dev` rồi chạy lại):
   - `/lop-hoc/<slug lớp>/?chapter=<id>`: dòng "Sơ đồ tư duy chương" nằm sau bài cuối, trước Kiểm tra chương; bấm sang đúng trang.
   - 375px trước (D1): `document.documentElement.scrollWidth === 375` khi mở TỪNG nhánh; không chữ < 13px ngoài KaTeX/SVG; công thức không chạm viền, không tràn nút.
   - ≥ 1280px sáng + tối: nút không đè nhau, không tràn khung. Bố cục 3 và 4 nhánh (`VI_TRI_THEO_SO`) CHƯA được chụp kiểm lần nào — chương đầu tiên dùng 3/4 nhánh phải chụp và chỉnh toạ độ.
   - Bật "Tự kiểm: che công thức": mọi `ct` bị che, lật được từng ô. Bấm "▶ Thử mô phỏng": iframe chỉ nạp sau khi bấm. Bấm thử ít nhất một link bài.
   - `npx tsc --noEmit -p .` và `npx eslint <file đã đụng>` sạch; console không lỗi hydration.
   - Giao agent `kiem-code` soát độc lập nội dung file dữ liệu so với bài (công thức, đơn vị, bẫy) trước khi commit.
8. **Giao thầy duyệt**: gửi ảnh 375px + 1280px (SendUserFile) kèm link `/lop-hoc/so-do/?chuong=<id>&lop=<slug>`; nêu chỗ chia nhánh còn phân vân.
   Commit theo đường dẫn (`git commit -- <path>`), ghi mã quy tắc trong mô tả commit. Deploy là việc riêng, sau khi thầy duyệt.

## Quy tắc thiết kế đã chốt (`docs/QUY-TAC-THIET-KE.md`) — không đổi khi thêm chương

- G1/N2: 1 tâm + ≤ 5 nhánh, ≤ 4 ý con. N5: mỗi lúc mở một nhánh. H1/H3/N8: hình khoá + câu chốt + công thức lõi đi cùng nhau.
- B8: nhánh đánh số + câu nối tiếp. L1: ô tự kiểm che công thức, nhớ lại rồi mới lật. V5/B4: PhET chỉ nạp khi bấm, không gì tự chạy.
- D1/D2/C1: điện thoại là thân cây dọc; ≥ 1024px mới toả tròn + bảng chi tiết dính bên phải.
- **Cố ý vượt M3**: mỗi nhánh một màu (`.c1`–`.c5`) làm mã ghi nhớ; màu chỉ ở nét nhánh + số thứ tự, nhánh vẫn phân biệt bằng số và hình (M4). Không thêm màu thứ 6.
- Giọng văn: câu ngắn, không xưng "thầy", không dấu gạch dài; nhãn tiếng Việt có dấu.

## Không làm

- Không sửa `SoDoTuDuy.tsx` để "vừa" một chương (đổi nội dung cho vừa khung; cần đổi khung thì hỏi thầy vì ảnh hưởng mọi chương).
- Không thêm round-trip Supabase, không thêm bảng: sơ đồ là nội dung tĩnh trong bundle, nạp động theo chương.
- Không tự nhúng mô phỏng mới vào sơ đồ; không đưa nội dung ngoài chương trình hoặc chưa có trong bài đã đăng.
- Không làm nhiều chương trong một phiên nếu context > 150k: mỗi chương một commit, giao tiếp chương sau cho phiên mới.

## Thứ tự chương đề xuất

Lớp 12: Ch.1 Vật lí nhiệt → Ch.2 Khí lí tưởng → Ch.4 Vật lí hạt nhân (Ch.3 đã xong). Sau đó lớp 11, lớp 10 theo chương đang dạy
(xem lịch ở `/lich-tuan`). Chương nào bài lý thuyết còn "chờ duyệt/chưa đăng" (xem `docs/memory/MEMORY.md`) thì làm sau.

## Nhật ký rút kinh nghiệm

- 2026-11-11 · Id bài lấy từ ghi chú cũ, suýt gắn link chưa kiểm → luôn đối chiếu `catalog.json` (bước 1) trước khi viết `bai[]`.
- 2026-11-11 · Công thức lõi nhánh 1 và 4 quá dài, tràn nút 190px ở màn rộng → `ct` chọn dạng gọn nhất, kiểm ở 1280px trước khi viết ý con.
- 2026-11-11 · Phân số/dấu |…| của KaTeX chạm viền dưới hộp → đã có `.ct { padding-bottom }`; công thức cao bất thường (phân số lồng) thì chụp kiểm riêng.
- 2026-11-11 · L10 Ch.3: `tam` "Lực → Chuyển động" (158px) tràn nút trung tâm elip ở 1280px → `tam` ≤ ~10 ký tự (đo `span.text-xl` trong `.tam` ≤ 120px) trước khi chụp.
- 2026-11-11 · Script kiểm 375px bấm mọi `button[aria-expanded]` dính cả nút menu đầu trang, mở menu che trang → lọc trong `main`.
