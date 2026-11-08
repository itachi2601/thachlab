# "Một dạng — một hình" cho Bài tập mẫu — quy trình áp cho mọi chương (thầy duyệt + đăng L12 Ch.3 ngày 5/11/2026)

Mẫu đã đăng: L12 Ch.3 Từ trường (bài 10, 11, 13, 14, 125, 126, 127) — xem `scripts/data/bai-tap-mau/<id>.json` các bài đó.
Lý do + cách đánh giá từng dạng (Có ích / Trang trí): `docs/RA-SOAT-HINH-BTM-TU-TRUONG.md`.
Họ hình có sẵn: `components/lessons/cong-cu/*.tsx` (đọc chú thích đầu file) + kiểu ở `features/lessons/types.ts`.
`cong_cu.de` và `cong_cu.dong` dùng được với MỌI họ (GiaiCungHinh/HinhDe/Dong.tsx không phụ thuộc họ).

## Cách làm một chương (phiên điều phối)
1. Với mỗi bài: lập bảng đánh giá từng dạng như mục 3 của `RA-SOAT-HINH-BTM-TU-TRUONG.md` (mô phỏng Có ích/Trang trí, bước dùng).
2. Giao agent con (general-purpose, 1–2 bài/agent, tối đa 2–3 agent cùng lúc) theo phần "Đích" dưới đây; brief của agent = file này + bảng đánh giá + cổng dev server.
3. Phiên điều phối kiểm bằng máy, KHÔNG tin báo cáo: mọi dạng `cong_cu.de == true`, `len(lop) == len(buoc)`, không còn `<figure` trong `problem_html`/`analysis_html`, `#kiem` = SACH; xem vài ảnh; 375px bằng `resize_window mobile` (Chrome headless 375 không ra layout điện thoại).
4. Commit từng bài theo đường dẫn (`git commit -- scripts/data/bai-tap-mau/<id>.json`), push.
5. KHÔNG sửa component dùng chung (`components/lessons/cong-cu/*`, `types.ts`, `globals.css`) — nhiều phiên chạy song song. Thiếu mục hình thì vẽ gần đúng bằng mục có sẵn và ghi "cần mục X" vào báo cáo cuối.
6. KHÔNG publish DB, KHÔNG deploy: báo thầy duyệt ở `/dev/btm/?f=btm-<id>` (sau `npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --xem-thu`). Thầy duyệt trong phiên thì mới publish `--giu-cu --yes` (bài có tự luận đã nằm trong dang_bai thì xem kĩ số dạng trước/sau) rồi `bash scripts/deploy.sh` từ checkout chính sau `git pull origin main`.
7. Không ghi vào nhật ký SKILL.md (nhiều nhánh cùng sửa cuối file sẽ kẹt gộp) — đưa bài học vào báo cáo cuối, phiên điều phối chung sẽ gộp.

## Vấn đề
Mỗi dạng đang có tới 3 hình khác nhau (mô phỏng SVG trong `problem_html`, hình dữ kiện trong `analysis_html`, hình
giải từng bước `cong_cu`), khác hướng nhìn/màu/nhãn; 23/35 dạng không có `cong_cu` nên giải từng bước không có hình.

## Đích (cho MỖI dạng của bài được giao)
1. **Một hình duy nhất = `cong_cu`, có `"de": true`.** UI mới (đã code xong) vẽ lớp 0 của `cong_cu` ngay dưới đề, rồi
   chính hình đó dính trên khi "Giải từng bước", thêm `lop[i]` sau khi em xong bước i+1.
   - Lớp 0 (`nen`, `hinh`, `duong`/`diem` gốc, `x_dich`…) = **bức hình của đề**: đủ mọi thứ đề mô tả hoặc nói "trên hình",
     có số liệu đề, ký hiệu khớp đề/lời giải. Nhìn lớp 0 phải hiểu tình huống mà không cần mô phỏng cũ.
   - Lớp 0 và các lớp chưa tới **không được lộ đáp án** của bước đang hỏi (chiều lực, chiều dòng, chiều đường sức khi đề
     hỏi chiều, số đáp số, góc cần tìm…). Đề hỏi chiều đường sức → vẽ đường sức KHÔNG mũi ở lớp 0, mũi thêm ở lớp sau.
     Không vẽ đúng tỉ lệ khi đo pixel ra đáp số.
   - `lop` có đúng `len(buoc)` phần tử (bước chỉ đọc có thể `[]`), thứ tự khớp `buoc[]`. Mỗi lớp vẽ đúng kết luận của bước
     đó; `ghi` ngắn (≤ ~45 ký tự, quá thì tự xuống 2 dòng — xem `chiaDong`). `het: k` để nhường chỗ.
   - Dạng đã có `cong_cu`: giữ phần lớp đang tốt, sửa lớp 0 cho đủ dữ kiện đề (vẽ cái đề có — vd. la bàn, dây, chiều I),
     sửa màu theo mục 3.
   - Dạng chưa có: viết mới bằng họ có sẵn (`tu_truong`, `do_thi`, `vong_tron`, `mach_dien`). Đọc chú thích đầu file
     component `components/lessons/cong-cu/<Ho>.tsx` và kiểu trong `features/lessons/types.ts` (tìm `TuTruongLop`,
     `DoThiLop`, `VongTronLop`, `MachDienLop`). Xem các dạng đã có `cong_cu` trong cùng file JSON làm mẫu.
   - Họ `vong_tron` chỉ là công cụ giải; nếu lớp 0 của nó trống thì không làm hình đề được → chọn họ thể hiện đúng đề
     (vd. đề cho đồ thị u(t) → `do_thi` có đường ngưỡng), hoặc bảo đảm lớp 0 có dữ kiện đề. Tự cân, ghi lý do vào báo cáo.
2. **Chuyển động (`dong`) chỉ cho dạng "Có ích"** trong bảng rà soát, và chỉ khi nó cho thấy điều một bước cần (quay khung
   tới góc α, dây quay đổi α, điểm chạy trên vòng tròn pha / đồ thị, dây đàn dao động, nam châm đi vào ống…). Không bịa
   chuyển động cho có. Dạng "Trang trí" / "Nửa vời": KHÔNG `dong`.
   Cú pháp (trong `cong_cu`):
   ```json
   "dong": [{"nut": "▶ Xem khung quay tới vị trí đề", "giay": 3,
             "doi": [{"p": "hinh.1.goc", "tu": 0, "den": 60}, {"p": "hinh.2.goc", "cac": [90, 120, 150]}]}]
   ```
   `buoc` (1-based) = nút hiện ở bước đó lúc giải; bỏ `buoc` = nút ở hình dưới đề. `p` = đường dẫn trong JSON của
   `cong_cu`; `cac` = các mốc cách đều (số thì nội suy, chữ/bool thì nhảy). Hết lượt, hình về đúng JSON gốc → **mốc cuối
   phải bằng giá trị gốc** (trạng thái đề) để không giật. Một lượt 2–4 giây; dao động thì cho 2–3 chu kì trong `cac`.
   Đổi được mọi số trong JSON (toạ độ `tu.1`, `diem.0.x`, `goc`, `dai`…), kể cả item nằm trong `lop.<i>.<j>` khi có `buoc`.
3. **Màu thống nhất cả chương** (họ `tu_truong`: `mau`): cảm ứng từ B = `"b"` (xanh), dòng điện I = mục `dong` (cam sẵn)
   hoặc `"i"`, lực từ F = `"luc"` (đỏ), pháp tuyến n và hình học = `"chu"` (đen). `vec` mặc định là cam → luôn ghi `mau`
   rõ. Nhãn chỉ số dưới viết `B_đ`, `B_{dây}`, `F_{AB}` (component tự hạ chỉ số); không viết "Bđ".
   Họ khác giữ màu của họ, chỉ cần đại lượng cùng tên cùng màu giữa các lớp.
4. **Gỡ hình cũ:** xoá nguyên khối `<figure …>…</figure>` (mỗi trường đúng 1 khối) khỏi `problem_html` và `analysis_html`.
   Sửa câu chữ còn nhắc tới mô phỏng/nút ("Bấm Chạy mô phỏng", "hình bên dưới", "trên hình mô phỏng"…) cho khớp hình mới;
   `analysis_html` chỉ còn bảng và chữ.
5. `tom_de`: giữ; sửa nếu ký hiệu đổi.

## Mục mới của `tu_truong` (đã có trong TuTruong.tsx, toạ độ 0..20 ngang × 0..11 dọc, y hướng lên, góc độ)
`diem {x,y,ten?,vi?}` · `vong {x,y,r,chieu?:"cung"|"nguoc",mau?,dut?}` (đường sức tròn quanh dây; bỏ `chieu` = không mũi)
· `la_ban {x,y,r,goc}` (kim, nửa N đỏ theo `goc`) · `thanh {x,y,goc,dai,mau?,dut?}` (đoạn qua tâm — khung nhìn dọc trục,
quay bằng `dong`) · `duong {diem:[[x,y]…],mau?,dut?,mui?,kin?,nhan?}` (đường cong gấp khúc — đường sức nam châm; `mui` =
số mũi theo chiều vẽ, 0 = không mũi) · `elip {x,y,rx,ry,goc?,mau?,dut?}` (vòng dây nhìn nghiêng) · `chu` nhận `mau`.
Thiếu thứ gì họ hình không vẽ được → vẽ gần đúng bằng `duong`/`chu`, ghi vào báo cáo "cần mục X"; KHÔNG sửa component.

## Cách sửa JSON
File `scripts/data/bai-tap-mau/<id>.json` là nguồn duy nhất. Sửa bằng script Python tại chỗ:
`json.load` → sửa → `json.dump(J, f, ensure_ascii=False, indent=1)` + xuống dòng cuối. **Không chạy `build-hinh-<id>.py`**
(ghi lại từ đầu, mất `cong_cu`/`tom_de`). Sau mỗi lần sửa, `git diff --stat` chỉ được đụng file bài của mình.

## Kiểm (bắt buộc, lặp tới sạch)
Dev server: mỗi phiên một cổng riêng (ghi trong brief phiên), chạy `npm run dev -- -p <cổng>` trong tab terminal (KHÔNG `next dev` trực tiếp — `predev` nối `.env.local`). Thay `3000` bên dưới bằng cổng đó.
```bash
npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --xem-thu      # ghi public/xem-thu/btm-<id>.json (không ghi DB)
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; S=<thư mục scratchpad của em>
"$C" --headless=new --disable-gpu --virtual-time-budget=20000 --window-size=1200,1400 --user-data-dir=$S/chr-<id> \
  --dump-dom "http://localhost:3000/dev/btm-hinh/?f=btm-<id>" | python3 -c "import sys,re;print(re.search(r'<pre id=\"kiem\"[^>]*>(.*?)</pre>',sys.stdin.read(),re.S).group(1))"
"$C" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=20000 --window-size=1150,1500 --user-data-dir=$S/chr-<id> \
  --screenshot=$S/<id>-d<k>.png "http://localhost:3000/dev/btm-hinh/?f=btm-<id>&d=<k>"
```
- `#kiem` phải là `SACH` (TRAN = chữ ra ngoài hình, DE = hai chữ đè nhau). Dấu `/` cuối `btm-hinh/` bắt buộc (308).
- Mở ảnh từng dạng (Read) và tự soát: lớp 0 khớp đề, không lộ đáp án; mỗi lớp khớp kết luận bước; mũi tên/nhãn không
  chạm nhau, không chạm mép; khung `dong` (t=0 / 0,5 / 0,97) đúng ý và mốc cuối trùng hình gốc; màu đúng quy ước.
  Ô hình trong bảng soát ≈ 360px — gần cỡ điện thoại 375px; chữ < ~10px là quá nhỏ.
- `npx tsc --noEmit -p .` không cần (không sửa code), nhưng JSON phải hợp lệ.

## Không được làm
(Dành cho agent con.) Không sửa code/CSS/component, không sửa file bài khác, không commit, không publish DB, không deploy,
không ghi vào SKILL.md/STATE.md/memory. Không đổi đề, số liệu, đáp án, `buoc[].hoi/lua_chon` (chỉ sửa câu nhắc tới hình cũ).

## Báo cáo (≤ 40 dòng)
Mỗi dạng một dòng: có/không `dong` (vì sao), họ hình, đã sửa gì ở lớp 0/lớp bước/màu, chỗ còn băn khoăn (nội dung cần thầy
quyết), "cần mục X" nếu có. Cuối cùng: `#kiem` của từng bài = SACH?, đường dẫn ảnh đã soát.

## Trạng thái 6/11/2026 (7 phiên nhánh dừng giữa chừng vì hết hạn mức tuần)
- **Xong trên main (55 bài):** 2 3 4 6 7 8 · 20–25 26 27 · 35 36 37 38 39 40 41 42 · 46–50 52–55 57 58 60 · 68 69 70 72 73 74 · 83 84 89 90 91 129 130 131 · 150 153 157 159 160 162 164.
  Trong đó 23 bài (commit 6426c6cf5) được cứu từ worktree phiên nhánh. 6/11 23:45 thầy duyệt ảnh 30 bài (23 bài này + 10 11 13 14 125 126 127) → ĐÃ ĐĂNG DB + deploy. 25 bài còn lại trong 55 chưa rõ đã đăng chưa — kiểm DB trước khi publish.
- **Dở, còn lỗi chữ đè/tràn (10 bài)** — bản dở nằm ở worktree phiên nhánh, chưa commit: 9 15 16 17 (`.claude/worktrees/xenodochial-antonelli-2bf293`), 28 31 (`vigilant-maxwell-0d1cf4`), 43 44 (`vibrant-hypatia-aa60fe`), 161 178 (`ecstatic-wilson-bdc8a9`). Chép file sang rồi chỉ dời nhãn tới `#kiem` SACH.
- **Chưa làm (25 bài):** 18 19 · 30 32 33 34 · 45 · 62 63 66 · 71 76 77 78 79 · 151 152 154 155 156 158 · 163 165 166 167.
- Họ `so_do_vecto` không có `lop` (mỗi `vec` mang `buoc` riêng) — đừng báo lỗi "lop ≠ buoc" cho họ này. Bài 46–48 có dạng cố ý không có hình.

## Trạng thái 8/11/2026 — L12 + L11 (27 bài)
- ĐÃ ĐĂNG DB (`--giu-cu --yes`, DB `cong_cu.de` = repo, không còn `<figure`) + deploy 8/11: L12 `3 4 6 7 8 9 15 16 17 19`, L11 `20 21 22 24 25 28 30 31 32 33 34 35 36 39 40 43 44`. Thầy duyệt ảnh sau soát Sonnet (sửa nhãn ở 3 6 15 16 17 19 25 28 30 31 32 33 35 36 39 40 43 44). Kiểm live 375px (8/11, tài khoản thầy): bài 43 (hình dưới đề + Giải từng bước dính hình trên, bước 1/4) và bài 33 (6 dạng + 1 mục thêm, không tràn ngang) đạt.
- Còn lệch nhỏ, cần sửa COMPONENT (không sửa được bằng JSON): 33 D3 (`giao_thoa_2_nguon`: thiếu AB, nhãn d₁/d₂/M bị hypebol cắt) · 39 D4 (`DienTruongDeu` thiếu mục `doan` vẽ tam giác MNP; nhãn MP vắt qua mép bản) · 39 D5 (nhãn cm bị đường sức cắt) · 4 (`thanh_nang_luong` nhãn mũi tên chạm khung vật) · 44 D3 (nhãn A, I sát dây) · 28 D4 (tiêu đề `$A^2$` nghi chưa render) · 20 D5 (lớp 0 không vẽ M ở đỉnh, cố ý tránh lộ pha).

## Cách làm tiết kiệm token (rút từ đợt 5–6/11)
- Phiên MỚI (không resume phiên cũ — context cũ 150k+ bị gửi lại mỗi lượt). Tối đa 2 phiên cùng lúc.
- Phiên điều phối KHÔNG đọc ảnh; chỉ kiểm máy (script trạng thái + `#kiem`). Agent con tự soát ảnh, mỗi bài ≤ 1 ảnh/dạng.
- Sửa nhãn đè/tràn = việc cơ học → Sonnet. Soạn hình mới (cần giải lại vật lí, chống lộ đáp án) → Opus, 2–3 bài/agent, 2 agent cùng lúc.
- Commit ngay sau mỗi bài sạch (đừng dồn), để hết hạn mức giữa chừng không mất việc.

## Cập nhật 8/11/2026 — L10 + KHTN 9: 19 bài đã lên DB (thầy duyệt 8/11)
- **Đã đăng DB (`--giu-cu --yes`, sao lưu `scripts/logs/bai-tap-mau-bai<id>-*.json`):** L10 45 46 47 48 49 50 52 53 62 63 66 71 72 73 76 77 78 79; KHTN 9 156. Đối chiếu DB↔repo: số dạng và số `cong_cu.de` khớp, không còn `<figure` trong `problem_html`/`analysis_html` (`scripts/logs/kiem-db-19-btm.mts`).
- Ngoài phạm vi gỡ: 52 (`solution_html`), 71 (`tu_luan.body_html`), 156 (`solution_html` + `tu_luan`) còn `<figure`.
- **Còn treo (cần thầy quyết / sửa component):** 156-d1 lớp 0 thiếu hình b (cần mục "hiện 2 khung ở lớp 0"); 156-d7 nhãn B₂′; 62/63 họ `so_do_vecto` chữ ~8px, vector gạch nhãn "m" (sửa ở component); 72 nhãn vá bằng ký tự rộng 0/khoảng trắng em (nên sửa lề chữ trong `ThanhNangLuong.tsx`); 71-d5 đổi sang họ `tu_truong` nên mất cột năng lượng; 79-d2 nhãn "8000 Pa" còn vắt thành bể (đã sửa thành "p_M = 8000 Pa" ngoài bể).
- Bài học: ảnh headless ~31 KB là trang chưa render → chụp lại với `--virtual-time-budget=40000`; agent dời nhãn có thể tạo đè mới → luôn chạy lại `#kiem`.
