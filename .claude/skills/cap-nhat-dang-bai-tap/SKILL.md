---
name: cap-nhat-dang-bai-tap
description: Nâng cấp dạng bài tập mẫu ĐÃ SOẠN thành "giải cùng hình": hình nét đơn giản dính nửa trên điện thoại, mọi bước tự trả lời ở nửa dưới, hình vẽ thêm theo bước đã xong. Gồm vẽ hình (cong_cu), xem thử 375px từng bước, học sinh ảo thử, đăng. Dùng khi thầy nói "cập nhật các dạng bài tập bài X", "làm hình tương tác cho dạng…", "/cap-nhat-dang-bai-tap". Soạn dạng mới thì dùng soan-bai-tap-mau.
---

# Cập nhật dạng bài tập → giải cùng hình (thầy chốt 2/11/2026)

Mẫu chuẩn là **bài 14 Sóng (lesson 33), Dạng 3: giao thoa hai nguồn**. Bản này đã qua 3 vòng góp ý của thầy và học sinh ảo (7/10 → sửa xong).
Code: `components/lessons/cong-cu/GiaiCungHinh.tsx` (khung) + `GiaoThoaHaiNguon.tsx` (hình). Dữ liệu: trường `cong_cu` của dạng trong `scripts/data/bai-tap-mau/<lesson_id>.json`.

**Học sinh thấy gì (375px):**
- Nửa trên là hình dính (khoảng 40% màn), thanh ◀ Bước i/n ▶ và một dòng nhắc. Nửa dưới là đúng MỘT bước đang làm.
- Mọi bước có câu hỏi đều phải tự trả lời: chọn bước kế, gõ đáp số. Khung ép `fading="giau_het"` nên không phải sửa JSON.
- Hình của bước i chỉ vẽ khi em đã làm xong bước i (không lộ đáp số). ▶ khoá kèm chữ nhắc cho tới khi em trả lời xong bước.
- Lời giải đầy đủ gập ở cuối. Khi em mở nó, hình thôi dính.

Quy tắc thiết kế (`docs/QUY-TAC-THIET-KE.md`): N1, N5, N6, N8 (split-attention), H3, H4, D2, D3, L1. Ghi các mã này vào commit.

## Không làm
- Không chạy sóng hay hoạt hình phức tạp. Thầy góp ý 2/11: "hình nhỏ, đơn giản hoá thành các đường".
- Không thêm chế độ "khám phá" với số liệu khác đề (bản v1 đã bỏ).
- Không làm cho mọi dạng: mỗi bài chỉ 1–2 dạng mà **hình thay đổi theo từng bước** thật sự giúp hiểu (giao thoa, sóng dừng, đồ thị x–t/v–t, vectơ lực, tia sáng, mạch điện). Dạng chỉ thế số vào công thức thì giữ giải từng bước thường.
- Chưa có dạng trong JSON thì soạn bằng `soan-bai-tap-mau` trước, rồi mới quay lại đây.

## Chọn model (thầy chốt 3/11/2026)
Kế hoạch đủ 492 dạng / 93 bài, bảng theo bài, theo chương và 9 đợt làm: [`KE-HOACH-MODEL.md`](KE-HOACH-MODEL.md) (chỉ mở phần chương đang làm).

| Việc | Model |
|---|---|
| Dạng đầu tiên của một **họ hình mới** (viết component SVG, vẽ lớp theo bước, chỉnh khối dính) — 15 dạng, 5 đợt Đ1–Đ5 | **Opus** |
| Dạng **dùng lại họ hình đã có** (khai `cong_cu` trong JSON, `tom_de`, soát `buoc[]`, checklist 375px) — 140 dạng, đợt Đ6–Đ9 | **Sonnet** |
| Dạng **chỉ tóm đề** (nhận biết, đổi đơn vị, thế một công thức) — 336 dạng | **Sonnet**, gộp nhiều bài một phiên |
| Soát lựa chọn từng bước (khác nghĩa, không lộ đáp án) khi thầy chưa duyệt | Opus (phiên chính) |
| Học sinh ảo thử (bước 6), `kiem-code` soát diff | Sonnet |
| Haiku | Không dùng |

- Mỗi bài tối đa **2 dạng** giải cùng hình; còn lại chỉ tóm đề.
- Đợt Sonnet chỉ chạy sau khi đợt Opus tạo họ hình nó cần đã vào main (ví dụ 7·D5 cần `cot_chat_long` của Đ4).
- Phiên Sonnet gặp dạng cần họ hình chưa có → dừng dạng đó, ghi vào bảng F của file kế hoạch, không tự viết component mới.

## Quy trình

### 1. Chọn dạng, tư vấn ngắn
- Đọc `scripts/data/bai-tap-mau/<id>.json`; chỉ đọc `dang_bai[i].buoc` của dạng định làm, không đọc cả file.
- Báo thầy 3–6 dòng: dạng nào, hình mỗi bước vẽ thêm gì, có dùng lại `loai` sẵn có không. Nếu là `loai` mới hoặc chương mới, chờ thầy gật rồi mới vẽ (AGENTS: tư vấn trước khi làm).

### 2. Soát `buoc[]` của dạng
- Mỗi bước có `hoi` với `dap_so` hoặc `lua_chon`; từ bước 2 có `chon_buoc_ke` (một đúng, hai sai, mỗi lựa chọn sai có `vi_sao`). Bước cuối "Kiểm tra" được phép chỉ đọc.
- Lựa chọn sai phải khác lựa chọn đúng ở **ý**, không chỉ ở một chữ (`<` với `≤`, "cùng pha" với "ngược pha"). Học sinh ảo chê kiểu khác một chữ là "phải đọc kỹ từng chữ".
- Lựa chọn đúng không được tự nói ra đáp án. Ví dụ "Cực tiểu (hiệu đường đi là số bán nguyên lần λ)" đã lộ đáp án.
- Thứ tự bước phải khớp thứ tự các lớp trong hình (mục 3).

### 3. Hình: dùng lại hoặc thêm `loai` mới
- **Dùng lại:** thêm vào dạng `"cong_cu": {"loai": "giao_thoa_2_nguon", "f": …, "v": …, "AB": …, "d1": …, "d2": …}`. Số liệu lấy theo đề, đơn vị Hz, cm/s, cm. Sửa JSON tối thiểu, giữ nguyên thụt lề cũ.
- **`loai` mới:**
  1. Tạo `components/lessons/cong-cu/<TenHinh>.tsx`, chép khung từ `GiaoThoaHaiNguon.tsx`: SVG thuần, props = số liệu đề + `layer`.
  2. Thêm kiểu vào union `WorkedTool` (`features/lessons/types.ts`) và một dòng vào `Hinh()` trong `GiaiCungHinh.tsx`.
- **Luật vẽ** (cả 3 đều đã gây lỗi thật):
  - `layer` = số bước đã xong. Lớp của bước i nằm trong `L >= i`; thứ chỉ cần tới bước k thì `L < k` để nhường chỗ.
  - Chiều cao viewBox **không đổi** giữa các bước: dải dưới luôn giữ chỗ, nếu không nút ◀ ▶ nhảy theo.
  - Nhãn dùng `Label` (có viền halo `--cc-halo`), cỡ ≥1,1 đơn vị khi hình rộng khoảng 20 đơn vị.
  - Hai nhãn không được nằm cùng một dòng nếu cộng chiều rộng vượt bề ngang hình: ước lượng mỗi ký tự ≈ 0,6 × cỡ chữ.
  - Nhãn dài thì cho xuống dòng riêng (như "11 cực đại · 12 cực tiểu" đặt dưới trục số).
  - Nét hai màu: `C_MAX #c2410c` cho cực đại, `C_MIN #0e7490` cho cực tiểu; đường loại thứ hai vẽ nét đứt (H4, không chỉ dựa vào màu).

### 3b. Tóm đề (`tom_de`, thử 3/11/2026 ở bài 33 Dạng 3)
- Thêm `"tom_de": {"cho": [...], "tim": [...]}` vào dạng. Mỗi phần tử là HTML ngắn, dùng được `$…$`, ký hiệu khớp lời giải.
- **Không đổi đơn vị sẵn**: ghi $v=0{,}50$ m/s như đề, vì đổi sang cm/s là việc của bước 1. "Tìm" đánh a) b) c) theo ý đề.
- Dưới 1280px là một dòng "Tìm: …" ở **ĐẦU khối dính, trên hình**; chạm vào thì Cho, Tìm và đề đầy đủ (đã bỏ hình) mở đè lên, trang không xô. Không đặt dòng này dưới nút ◀ ▶: lúc vừa mở bước 1 nó rơi đúng chỗ thanh điều hướng đáy điện thoại che.
- Từ 1280px là thẻ Cho/Tìm ở **lề phải, chỗ ghi chú lề** của bài lý thuyết (`--wide-bleed`), dính theo; dòng "Tìm" ẩn. Trang bài thật ở đúng 1280px lề chỉ ~140px nên dòng dài xuống 2–3 dòng — giữ mỗi phần tử ngắn.
- `/dev/btm` đã dựng khung rộng toàn màn như trang thật (3/11), nên thấy được thẻ lề ở cỡ 1280.
- Soát: chụp 375px **lúc vừa mở "Giải từng bước", chưa cuộn** (thấy dòng Tìm, không bị thanh đáy che) và chụp 1280px (thẻ lề hiện, `scrollWidth` = 1280).

### 4. Xem thử (Mac)
```bash
npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --xem-thu
```
- Lệnh này ghi `public/xem-thu/btm.json` (gitignore). Chạy dev bằng `preview_start {name:"thachlab-dev"}` rồi mở `http://localhost:3000/dev/btm`.
- **CSS mới không ăn** (Turbopack giữ CSS cũ, gặp 2 lần ngày 2/11): dừng server, `rm -rf .next/cache .next/dev` trong worktree, chạy lại. Kiểm bằng `document.styleSheets` xem đã có luật mới chưa.

### 5. Kiểm 375px — qua ĐỦ mọi bước, không chỉ bước đầu
Đặt `resize_window mobile`, mở dạng, bấm "Giải từng bước", rồi lái bằng `javascript_tool`:
```js
const W=ms=>new Promise(r=>setTimeout(r,ms)), steps=document.querySelector('.cc-steps');
const pick=async f=>{[...steps.querySelectorAll('button')].find(b=>f(b.textContent)).click(); await W(500)};
const ans=async v=>{const i=steps.querySelector('input'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(i,v);
  i.dispatchEvent(new Event('input',{bubbles:true})); await W(80); [...steps.querySelectorAll('button')].find(b=>/Kiểm tra/.test(b.textContent)).click(); await W(700)};
const next=async()=>{document.querySelector('.cc-stepper button:last-child').click(); await W(400)};
const sw=()=>document.documentElement.scrollWidth; // mỗi bước phải = 375
```
- Chữ KaTeX trong nút bị tách ký tự, nên `pick` lọc bằng `startsWith`/`includes` từ ngắn ("cùng pha", "−"), không khớp nguyên câu.
- Đáp án đúng xem trong `buoc[]`.

Kiểm từng mục:
- [ ] `sw() === 375` ở **mọi** bước. Lỗi 2/11: dòng nhắc cuối dài làm cột lưới phình tới 457px; đã sửa bằng `minmax(0,1fr)`.
- [ ] Chụp bước cuối (đủ mọi lớp): nhãn không chạm nhau, không chạm A/B, không chạm mép.
- [ ] Trước khi trả lời, hình không lộ đáp số của bước đang hỏi.
- [ ] ▶ khoá kèm chữ nhắc; trả lời xong thì ▶ đổi màu.
- [ ] Cuộn để ô nhập nằm sát đầu màn rồi trả lời: sau 0,7 giây, `.cc-steps` top ≥ `.cc-sticky` bottom (lời giải bước không bị hình che).
- [ ] Bấm chuột thật vào ô nhập (`computer left_click`, không `focus()` bằng JS vì khung chạy ngầm thì `:focus` không khớp): `.cc-sticky` phải `position: static`.
- [ ] Mở "Lời giải đầy đủ": hình thôi dính.
- [ ] Nền tối: đặt `resize_window colorScheme: dark` rồi chụp một lần.

### 6. Học sinh ảo thử (thầy yêu cầu từ 2/11)
- Dùng `start_session` (initiation "user_asked" nếu thầy đã bảo thử; `model: "sonnet"`, `use_worktree: false`, chỉ đọc, giữ dev server chạy).
- Brief: "Đóng vai học sinh lớp N dùng điện thoại. Mở `http://localhost:3000/dev/btm` ở 375×812, Dạng X → Giải từng bước. Làm hết các bước, cố tình sai 1–2 lần. Báo lại: chỗ rối/khó bấm/khó đọc, hình có giúp từng bước không, chấm 1–10. Đo `document.documentElement.scrollWidth` ở mỗi bước. Không sửa code."
- Lần sau dùng `SendMessage` tới đúng phiên đó (nó đã có ngữ cảnh), không mở phiên mới.
- Sửa lỗi chắc chắn ngay. Góp ý về nội dung (lựa chọn, câu chữ) thì đưa thầy quyết.

### 7. Commit, đăng
- Commit theo đường dẫn (code + JSON), ghi mã quy tắc vào commit.
- Code (khung hoặc `loai` mới) phải **deploy trước** rồi mới đăng JSON. Web chưa có khung thì bỏ qua `cong_cu` (vẫn giải từng bước thường); có khung mà thiếu `loai` thì `Hinh()` trả `null` → khung hình trống.
- Đăng sau khi thầy duyệt:
```bash
npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --dry-run
```
```bash
npx tsx scripts/publish-bai-tap-mau.mts --lesson <id> --giu-cu
```
  Chạy trong tab terminal; xem mục **Đăng (Mac)** của `soan-bai-tap-mau`. Ảnh hưởng một dòng `lesson_items` nên chạy giờ nào cũng được.

## Bẫy kỹ thuật đã gặp (đừng gỡ lại)
- Tổ tiên có `overflow: hidden` làm `position: sticky` mất tác dụng → `.lesson-worked-row:has(.cc-split) { overflow: clip }`.
- `window.scrollTo({behavior:"smooth"})` không chạy khi khung trình duyệt ở chế độ nền → dùng `"instant"`.
- Khi đang gõ, bàn phím điện thoại chiếm nửa dưới, hình dính chiếm nửa trên → khi ô nhập đang focus thì hình thôi dính. Trả lời đúng thì `blur` rồi kéo khung về chỗ cũ (`GiaiCungHinh`: effect theo `opened`).
- `StepwiseSolution` có thêm `only` (chỉ vẽ một bước), `onProgress` (số bước đã mở liên tiếp) và `fading` (ghi đè). Đổi API này thì kiểm lại cả `WorkedQuestionsGrid`.

## Nhật ký rút kinh nghiệm (bắt buộc cập nhật cuối MỖI phiên dùng skill này — xem `AGENTS.md`)
- 2026-11-02 · v1 dùng canvas sóng chạy cộng chế độ khám phá; thầy chê xa hình, rối → v2: SVG nét, hình dính nửa trên, mỗi lần một bước. Học sinh ảo: "chỉ 1 bước tương tác" → v3: `giau_het`, hình theo bước đã xong.
- 2026-11-02 · Học sinh ảo bắt 2 lỗi mà ảnh chụp bước 2 bỏ sót: tràn ngang ở bước cuối, lời giải bị hình che sau khi gõ → luôn chạy đủ checklist mục 5 qua MỌI bước trước khi báo xong.
- 2026-11-03 · Tóm đề: chỉ đo phần tử tồn tại + không tràn, không chụp lúc vừa mở → dòng "Tìm" bị thanh điều hướng đáy che, thầy không thấy; trang xem thử cắt mất lề phải nên thầy cũng không thấy thẻ desktop → dòng Tìm lên đầu khối dính; trang xem thử phải dựng khung giống trang thật; luôn chụp màn ở trạng thái học sinh thấy đầu tiên.
- 2026-11-03 · Đ1 (3 họ mới): nhãn số trục vòng tròn bị cung xoắn đè, nhãn "truyền" đè nhãn M ở đỉnh sóng, chữ dải dưới tràn khỏi viewBox (giao thoa đếm dãy) — chỉ thấy khi chụp bước CUỐI → đặt nhãn cố định phía trong/ngoài vùng vẽ thêm, giữ chỗ dải dưới đủ số dòng của bước dài nhất. Ảnh chụp ngay sau bấm có thể bắt giữa hiệu ứng `cc-in` (nhạt/mất nét) → chờ ~1,5 s rồi chụp, nghi thì đo `getAttribute('d')` thay vì sửa code.
- 2026-11-03 · Đ2 (do_thi, tu_truong, thanh_nang_luong): chồng nhãn chỉ lộ ở bước sau (Δt đè "nóng chảy", số vạch trục sát nhãn chiếu, nhãn −2/O/2 chen nhau) → dùng `het: k` ẩn mục đã xong việc, component tự ẩn số vạch gần nhãn mới; ghi dài tự thu cỡ chữ. Ô `ghi` phải khớp đúng gợi ý của bước (26·D5 viết v=ωA trong khi lựa chọn đúng là √(2W/m)) → đọc `lua_chon` đúng của bước trước khi viết `ghi`. `Txt` chỉ hạ một ký tự sau `_` → chỉ số nhiều chữ viết `_{max}`.
- 2026-11-03 · Khung xem thử ở pane nền không chạy hết `cc-in` (ảnh nhạt) → chèn `.cc-in{animation:none!important}` trước khi chụp. Bước trắc nghiệm đứng trước ô nhập: kịch bản lái phải bấm lựa chọn rồi mới gõ số. Dạng chỉ `tom_de` chưa có UI hiện (tóm đề nằm trong `GiaiCungHinh`) — soát ở `/dev/btm` sẽ không thấy gì; xem mục F kế hoạch.
- 2026-11-03 · L10 Ch.3 (họ `so_do_vecto` + `thanh_moment`, một component `SoDoVecto.tsx`): khai vectơ bằng dữ liệu (`goc` chữ "doc_len", "day:B"…, `buoc`/`den`) dùng lại được cho 8 dạng mà không sửa engine; chỗ hỏng lặp lại toàn ở **bố cục**: bảng số đẩy hình nhỏ (mặt dốc thoải, mặt ngang dẹt), nhãn tay đòn bị cắt, nhãn đè nét → thêm `bang_vi_tri: "tren"` cho hình dẹt, bảng né nhãn điểm, khung tính cả nhãn neo start/end; chỉ để ở bảng số đại lượng TÍNH RA (dữ kiện đã có ở tóm đề), mỗi hình ≤4–5 dòng.
- 2026-11-03 · Tên vectơ phải khớp lời giải (F_ms/F_mst, N_y, d_T, a'): đọc `solution_html` trước khi đặt tên; vectơ là đáp án của bước (hướng N_y, chiều a) chỉ hiện SAU bước đó (`buoc` = số bước), bảng số có `so_buoc` riêng.
- 2026-11-03 · Dạng chỉ tóm đề: `tom_de` chỉ hiện trong `GiaiCungHinh` (cần `cong_cu`) — 18 dạng ghi dữ liệu nhưng UI chưa hiện → trước khi giao đợt "chỉ tóm đề" phải cho `StepwiseSolution` hiện `tom_de`, nếu không là làm dữ liệu chết. Soát bằng xem thử thật, không chỉ JSON hợp lệ.
- 2026-11-03 · Đã vá: dạng không có `cong_cu` bọc `StepwiseSolution` trong `TomDeKhung` (`components/lessons/TomDe.tsx`, dùng chung với `GiaiCungHinh`) — dòng "Tìm" dính đầu phần lời giải, chạm mở Cho/Tìm + đề; ≥1280 thẻ ở lề (`.bt-tomde-khung`). Đợt "chỉ tóm đề" giờ có UI.
- 2026-11-03 · Tốn vô ích: driver chọn phương án theo tiền tố chữ bị lệch khi phương án mở đầu bằng công thức KaTeX (chọn nhầm 3 lần) → so theo đoạn chữ thường dài nhất ngoài `$…$`; ảnh chụp ngay sau bước dính hiệu ứng mờ `.cc-in` → tắt `animation` bằng JS trước khi chụp, khỏi chụp hai lần.
- 2026-11-03 · Sửa theo HS ảo Đ2: khung dây nhìn dọc cạnh chỉ là một đoạn thẳng → HS không thấy ABCD; thêm mục `khung` (hình nhỏ ABCD nhìn nghiêng, ghi cạnh đi vào hình) và mục `hinh` cũng nhận `het` để bước "khung quay" thay hẳn khung cũ (lực F đi theo khung, có vectơ B qua tâm để cung góc nằm giữa n′ và B). Nhãn vectơ đứng dài đặt cạnh thân ngay sau mũi (khỏi đụng trần/sợi chỉ); nhãn đường sức trên cùng sát mép thì xuống dưới đường (viewBox cắt chữ). Đồ thị: ghi dài tách 2 dòng thay vì thu chữ (≥10px ở 375), tên trục ngang xuống dưới trục khi không đụng số vạch. Màu/nét đường trong hình bước phải khớp hình đề (`problem_html`) — soát cả hai khi dạng có đồ thị.
- 2026-11-03 · Tốn vô ích: khung xem thử 375×812 bị thu nhỏ vào pane 800×600 nên `zoom` ra ảnh mờ → đặt cỡ cao vừa pane (375×590) khi soát chữ nhỏ; driver lưu vào `sessionStorage` rồi `eval` sau mỗi lần nạp lại thay vì dán lại; so phương án bằng chữ đã thay KaTeX bằng `annotation` (tiền tố chữ trùng nhau ở "cách $T/2$ / $T/4$" làm chọn nhầm).
- 2026-11-03 · Đăng: `publish-bai-tap-mau.mts` không `--yes` thì treo ở y/N (bị `tail` giấu) → vòng lặp luôn `--yes` sau dry-run; JSON có `tu_luan` thì thêm mục cuối "Bài tập tự luận" (sao lưu ghi "5 dạng cũ" là bình thường). Phiên con báo hở/việc sửa → kiểm `list_sessions` trước khi tự làm (2 lần làm trùng 3/11).
- 2026-11-03 · Đ3: soát chồng/tràn nhãn bằng mắt ở 375px bỏ sót (hình nhỏ) → driver đo `getBBox` mọi `text` qua từng bước (ra ngoài viewBox, giao nhau) rồi mới chụp; phóng hình bằng svg `position:fixed` 780px để nhìn. `chiaDong` đếm cả ký hiệu `_{max}` nên tách dòng thừa → đã sửa bỏ markup khi đo. Nhãn ngoặc trên cùng bị viewBox cắt → chừa lề trên trong viewBox thay vì dời cả mạch. Hàm vẽ mục trong component: dùng hàm `veMuc()` chứ không khai component con trong render (remount mỗi lần, mất hiệu ứng `.cc-in`).
- 2026-11-03 · HS ảo Đ3: (1) dòng ghi bị ngắt giữa biểu thức ("36,4 : ⏎ 0,010", "1,2 ⏎ A") vì `chiaDong` chỉ ưu tiên "⇒" → nay cắt ở ⇒ / sau ";,:" / " · ", tránh sau số và sát phép toán, rồi mới trước "="; soát mọi dòng ghi các bài bằng script gọi `chiaDong` (không cần trình duyệt). (2) Chi tiết của bước trước còn sót sang bước sau (khung 6,48 mm, dây nối tắt, đường U_max không chú giải) → mục chỉ phục vụ một bước phải có `het`. (3) Nhãn ngoặc dài hơn ngoặc thì đè vạch đầu → nhãn ngắn, chi tiết để ở ghi. Driver tự giải: đọc `/xem-thu/btm.json`, chọn `dung`, nhập `dap_so` — khỏi nhớ đáp án.
- 2026-11-03 · HS ảo bài 60 D2: bước không hỏi (Hướng, Kiểm tra) mở sẵn nên `opened` nhảy quá `step + 1` → lời giải bước hỏi cuối bị hình dính che (đã vá điều kiện căn khung). Bước "Hướng của …" mà đề hỏi đúng cái đó thì phải có câu hỏi (`lua_chon`), đừng để HS chỉ bấm ▶ đọc.
- 2026-11-03 · Đ4 (50, 57, 79): driver lấy `.cc-steps` đầu trang nên chọn đáp án của dạng khác → mọi selector lấy phần tử CUỐI (dạng vừa mở). Nhãn chữ có chỉ số dưới vượt khung ~0,3 đơn vị → viewBox chừa H+3,7. Vectơ quy tắc tam giác chung ngọn → nhãn đè nhau, cần `nhan_lech` riêng; quỹ đạo ném vẽ cùng tỉ lệ hai trục mới đúng góc; thước trong ống chữ U hẹp → nhãn ngắn (h₁, Δh), số để ở ghi; hai lực cùng phương (P, P') phải `lech` khác nhau kẻo trùng nét.
- 2026-11-03 · HS ảo Đ4: chỉnh tay JSON (nhan_lech, het) rồi chạy lại script sinh dữ liệu ở scratchpad → ghi đè mất chỉnh, commit bản lỗi, HS ảo thử đúng bản lỗi → sau lần sinh đầu, JSON là nguồn duy nhất, mọi chỉnh sửa bằng python sửa tại chỗ; trước commit `git diff` tìm lại dấu hiệu của lần chỉnh. Đề thiếu g mà đáp số dùng g = 10 → HS nhập 9,8 bị chấm sai, gợi ý lệch → ghi g vào đề + câu hỏi bước. Công thức `$$…$$` dài ~30 ký tự hiện ở 375px phải cuộn ngang (HS tưởng bị cắt) → tách đôi tại dấu "=" giữa. Bước 1 hình trống → vẽ sẵn cái đã biết (v₀, góc "α = ?").
- 2026-11-04 · Nội dung theo HS ảo Đ4: `loi_hay_gap` hiện cho MỌI đáp số sai → viết theo dạng "Ra X là …; ra Y là …" cho 2–3 đáp số sai hay gặp, không chỉ một lỗi. Lựa chọn đúng dài nhất (9/18 bước) → HS đoán được: cho ba lựa chọn cùng dạng (cùng là công thức trần, hoặc cùng đuôi ", rồi …"), soát bằng script đếm độ dài trước khi xem thử. Chữ hình đề 12–13 trên viewBox 420 chỉ còn ~9px ở 375 → dùng ≥15 (≈11px), đo `getBBox` chữ tràn/đè sau khi tăng. `\text{gỗ}` trong KaTeX lệch dấu → viết chữ Việt ngoài công thức.
- 2026-11-04 · Đ5 (83, 156): bài nhiều câu a/b/c cần khung hình khác nhau → `thau_kinh` chọn khung theo BƯỚC đang làm (`phan[].tu_buoc`), không theo `layer` (bước chỉ đọc làm layer vượt lên, hiện nhầm khung). Ghi chứa phép nhân " · " bị `chiaDong` cắt giữa biểu thức → trong ghi viết `30·20` liền, " · " chỉ để nối hai mệnh đề. Driver bấm tiêu đề dạng ngay sau tải trang hay hụt → mở tiêu đề riêng, chờ 1,5 s rồi `run(n,true)`; ảnh chụp sau `gal()` có lúc là ảnh cũ → xoá `#gal`, gọi lại rồi chụp. Khung 375×590 chỉ còn hình cao 150px → nhãn chỉ số dưới đầu mũi tên ảnh chạm dải ghi; nới `y_duoi` chứ không thu chữ.
- 2026-11-04 · HS ảo Đ5: chọn đúng rồi chạm nhầm lựa chọn khác → bước mở lại, mất ô nhập → `StepwiseSolution` khoá lựa chọn sau khi đã đúng. Hình bước trước lộ đáp án bước sau (ảnh cuối vẽ xong khi bước sau hỏi chiều ảnh) → mục trả lời câu nào để vào `lop` của chính bước đó. Đề hỏi ý định tính (chiều ảnh, dụng cụ tương đương) thì phải có bước hỏi, không chỉ ghi trong dải ghi. Gợi ý: mỗi đáp số sai hay gặp tự tính lại cho khớp (Ra 12 là…, ra −60 là…), đừng viết theo trí nhớ.

- 2026-11-04 · Đ8 (L10, 15 bài, chỉ sửa JSON, không đụng component): (1) Nhãn vectơ/`mui` dài (`W_đ = …`, "10 kJ = …") tràn viewBox, bảng ≥3 dòng dài đè nhãn nền cảnh (`dai`, α) → bảng `bang_vi_tri` "phai"/"tren", mỗi dòng có `den` để chỉ ≤2–3 dòng cùng lúc, bỏ `dai`; nhãn ngắn, số liệu dài để ở `ghi`. (2) `so` trong `vec` tự thành dòng bảng KHÔNG có `den` → dồn cả bước cũ lên hình: số đặt trong `bang` có `buoc`/`den`, không dùng `so`. (3) Chỉ số dưới nhiều chữ cần ngoặc (`W_{tA}`, `F_{đh}`, `A_{AB}`), tóm đề dùng `W_{\text{đ}}` (`W_đ` hiện sai). (4) Rơi tự do dùng `do_thi` v–t chứ không `quy_dao_nem`; hình phẳng thì `bang` "tren"; trục `truc_chuyen_dong` nhãn sát mép bị cắt → nới x_min/x_max, đối tượng chỉ phục vụ một bước thì `het`. (5) `vong_tron` chiếu lên trục x nên dùng cho chuyển động tròn chỉ để thấy vòng + chiều + cung quét; điểm đặt ở goc 0 đè chữ trục "x" → đặt goc 0,3; mỗi ghi ≤~28 ký tự, tách hai dòng `ghi` thay vì một dòng dài (cờ OUT của `run()` với chỉ số dưới là báo sai, nhìn ảnh để chốt). (6) Việc rẻ: dump đề + bước bằng script rồi viết JSON bằng python `patch` theo lô cả bài, xem thử từng bước một lần/dạng; đừng chụp mọi bước.
