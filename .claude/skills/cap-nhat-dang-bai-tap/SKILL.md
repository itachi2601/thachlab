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
