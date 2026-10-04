# Hero — tab 4 "Hình chiếu": bóng quay đều đồng nhịp với con lắc lò xo

Ghi 2026-10-04.

## Mục tiêu
Mô hình thứ 4 của hero trang chủ (sau Ném xiên · Thả hàng · Giao thoa): cho học sinh thấy **cái gì quyết định
nhịp** của dao động điều hoà, bằng cách ghép hình chiếu của chuyển động tròn đều với một con lắc lò xo thật
trên cùng một trục. Nguồn: mục 5 "Liên hệ với chuyển động tròn đều" của Bài 1 Vật lí 11 (lesson 20), spec
`content/thi-nghiem/tn-l11-daodongdieuhoa-03.json` (thí nghiệm "bóng của van xe đạp").

## Đã xong (2026-10-04, trên `main`, chưa deploy)
- `lib/circularProjection.ts` — toán thuần: A₁ = 6 cm cố định, A₂ (chỗ thả) 2–10 cm, m 0,05–0,5 kg, k = 4 N/m,
  ω bánh xe 2–12 rad/s; `sameRhythm` (ngưỡng 0,5%), `alignedPhase` (ngưỡng 10°), `equalTimeDots`, 5 trạng thái
  câu nhận xét. Số liệu hình chiếu khớp đúng `so_lieu_mau` của spec.
- `hooks/useCircularProjection.ts` — θ và φ **tích luỹ** theo thời gian (θ += ω·dt), không tính lại θ = ω·t: nhờ
  vậy kéo thanh trượt ω giữa chừng thì bóng không nhảy vị trí, đúng như đĩa quay thật. Vòng lặp rAF chỉ chạy khi
  đã bấm Chạy VÀ canvas còn trong tầm mắt.
- `components/physics/ShadowSpringSimulation.tsx` — canvas 2 làn, `stageFor()` chia chiều cao theo nhu cầu thật
  rồi căn giữa (không hard-code px, chạy đúng ở 288×160 lẫn 611×340).
- `components/home/PhysicsSimulationHero.tsx` — tab 4 + nhãn 1 dòng ở 360px (`whitespace-nowrap`, 13px mobile).
- Kiểm: `npx tsx tmp/hero-review/hinhchieu-check.mts` (34 kiểm) · `tmp/hero-review/hinhchieu-verify.py` (ảnh
  360/375/1440 + đọc số đọc thật qua CDP). JS tải đầu trang chủ **216 KB gzip, không đổi**; chunk riêng 17 KB raw.

## Quyết định thiết kế (đọc code không tự suy ra)
- **"Đồng nhịp" ≠ "trùng vị trí".** Cùng chu kì mà khác pha là trạng thái thật và phải nói đúng: khớp ω chỉ làm
  hiệu pha **thôi tăng**, phần đã lệch thì giữ nguyên → có riêng trạng thái `samePeriod` và câu chữ buộc học sinh
  bấm "Đặt lại" để thả cùng lúc. Nếu gộp trạng thái này vào "đồng nhịp" là dạy sai.
- **Hai hệ phải nằm CÙNG một trục x.** Bóng chạy ngang mà con lắc treo thẳng đứng thì "đồng nhịp" chỉ còn là ẩn
  dụ, mất hình ảnh mạnh nhất (vòng tròn nét đứt trùm khít vật nặng). Vì vậy con lắc ở đây là con lắc lò xo
  **nằm ngang** (T = 2π√(m/k) đúng, không có g).
- **Thanh trượt A₂ bị khoá trong lúc chạy** (đổi biên độ giữa chừng làm vật nhảy vị trí), còn m và ω thì đổi
  được ngay — vì ω chính là động tác khoá nhịp, còn đổi m chỉ đổi ω_c chứ không nhảy vị trí.
- **Câu nhận xét chỉ nhận boolean `aligned`**, không nhận t sống: nó nằm trong `aria-live="polite"`, nếu đổi
  theo từng khung hình thì trình đọc màn hình đọc không dừng. Số đo tức thời để ở bảng số đọc riêng.
- **Không có đồ thị x–t** trong tab này: bằng chứng "cùng nhịp" là hiệu pha + số dao động + hình học cùng trục;
  thêm đồ thị nữa thì canvas 190px thành 4 lớp chồng (G1/N1). Hình x–t của riêng hình chiếu đã có ở hình tĩnh
  trong bài học.

## Còn chờ
- **Chưa deploy** (`bash scripts/deploy.sh`).
- **Chặng 2 — nhúng vào bài 1 lớp 11 (lesson 20)**: repo **chưa có cơ chế nào** để nhúng mô phỏng vào
  `theory.html` (mọi mô phỏng hiện chỉ được import ở hero). Phải thêm placeholder trong HTML bài + mount trong
  `components/exams/ContentHtml.tsx`, nhớ hai cạm bẫy: mount SAU khi KaTeX render xong (KaTeX thay cả node), và
  chỉ bài đó trả giá chunk. Kèm bộ câu hỏi gắn YCCĐ `daodong.hinh_chieu_tron_deu`.
- `HarmonicPanel`/`SpringSimulation` (con lắc lò xo treo thẳng đứng) vẫn **chưa được nhúng** — dùng cho phần
  chu kì con lắc lò xo, không liên quan tới tab này.
- Lưu ý khi build: `next build` (prebuild `build-content.mjs`) **tự sinh lại `content/thi-nghiem/index.json`**, nên
  file đó hay hiện là "modified" dù không ai sửa tay — đừng commit nó lẫn với việc của phiên khác.
