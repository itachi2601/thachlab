# Ảnh thẻ "Vật lý quanh ta" — khung, nguyên tắc bản quyền, brief cho Gemini

Thẻ ở trang chủ (`PhysicsPostRibbon`) và `/blog` (`PhysicsCuriosityCard`) có khung ảnh 16:9. **Chưa có ảnh thì hiện khung giữ chỗ**
(dấu "?"), có ảnh nhưng thiếu ghi công thì **vẫn không hiện** (`lib/blog.ts` → `resolvePhoto`). Quy tắc bản quyền gốc: `AGENTS.md` mục "Bản quyền" + `/dieu-khoan`.

## 1. Ảnh nào được dùng
- **Giấy phép cho phép**: `CC0`, `Public Domain`, `CC BY 2.0–4.0`, `CC BY-SA 2.0–4.0`. Không NC, không ND, không "all rights reserved", không "dùng cho mục đích giáo dục" (không phải giấy phép mở).
- **Nguồn đã duyệt** (script kiểm theo host): Wikimedia Commons (`commons.wikimedia.org`, `upload.wikimedia.org`), PhET (`phet.colorado.edu`), Openverse, Flickr (chỉ ảnh có giấy phép CC ở trên).
- Không rõ giấy phép = **không dùng**. Đừng tin chữ "free" ở trang trung gian: mở trang gốc, đọc ô "Licensing" của chính file đó.
- **Không** dùng ảnh AI sinh làm "ảnh thật" cho hiện tượng (dễ sai vật lí, đã từng có đề mất hình). Ảnh tự chụp của thầy luôn dùng được (`CC0`, tác giả "Ngô Diệu Thạch").
- **Tránh mặt người nhận ra được** (quyền hình ảnh). Cần người thì chọn ảnh chụp xa, lưng, hoặc hình bóng.
- Ảnh có logo/nhãn hiệu rõ (xe, hãng) hoặc công trình có hạn chế chụp: ghi trong `note`, Claude/thầy duyệt trước khi dùng.

## 2. Ảnh phải làm gì (H1: mỗi hình trả lời một câu hỏi)
Ảnh là cái "móc" 3 giây đầu, nên phải **cho thấy chính hiện tượng trong câu hỏi** (con chim trên dây, nồi đang xì hơi…), không phải ảnh minh hoạ chung chung. Sơ đồ/đồ thị đã có trong bài, **không** dùng làm ảnh thẻ.
Ảnh sáng, chủ thể to ở giữa (thẻ bị cắt `object-cover`; chữ nhãn trên thẻ đè góc trên-trái nên **chừa góc trên-trái ít chi tiết**). Tránh ảnh nền trắng tinh (M5), tránh ảnh có chữ lớn trong ảnh.

## 3. Quy cách file
- Lưu ở `public/images/blog/<slug>-the.webp`, **16:9, rộng 1200px (tối thiểu 800), ≤150 KB**, `.webp`.
- Chuyển bằng sharp, ví dụ: `npx sharp -i goc.jpg -o public/images/blog/<slug>-the.webp resize 1200 675 --fit cover -f webp -q 78` (hạ `-q` nếu >150 KB).
- Giữ ảnh gốc ngoài repo (thư mục tải của thầy), repo chỉ giữ bản webp.

## 4. Khai báo trong front-matter của bài (`content/blog/<slug>.md`)
```yaml
photo: "/images/blog/<slug>-the.webp"
photoAlt: "Mô tả cái ảnh thể hiện, ≥15 ký tự (ví dụ: Hàng chim sẻ đậu trên dây điện cao thế)"
photoCredit:
  author: "Tên tác giả đúng như trang gốc"
  license: "CC BY-SA 4.0"          # đúng một trong danh sách mục 1
  licenseUrl: "https://creativecommons.org/licenses/by-sa/4.0/"
  sourceUrl: "https://commons.wikimedia.org/wiki/File:...."   # trang của CHÍNH file ảnh
```
Thẻ tự in dòng "Ảnh: tác giả · giấy phép" dưới khung ảnh, có link về nguồn.

## 5. Kiểm trước khi coi là xong
```
npx tsx scripts/kiem-anh-vat-ly-quanh-ta.mts
```
Báo LỖI (exit 1) nếu: file không có / không webp / >150 KB / >1200px / không 16:9 / thiếu alt / thiếu tác giả / giấy phép ngoài danh sách / nguồn ngoài host đã duyệt. Thiếu ảnh chỉ là cảnh báo. Sau đó xem thẻ ở 375px (trang chủ + `/blog`).

## 6. Brief cho từng bài (Gemini tìm ảnh)
| Bài (slug) | Ảnh cần thấy | Từ khoá gợi ý (Commons) |
|---|---|---|
| `vi-sao-chim-dau-day-dien-khong-bi-giat` | Chim đậu trên dây điện (cao thế hoặc dây trần), thấy rõ chim + dây | birds on power line, bird on high voltage wire |
| `vi-sao-co-bap-co-lai-khi-nang-ta` | Cánh tay đang cuốn tạ (biceps curl), nên cắt/chụp sao cho không lộ mặt | dumbbell curl, biceps curl arm |
| `vi-sao-noi-ap-suat-nau-chin-nhanh` | Nồi áp suất đang xì hơi hoặc van áp suất | pressure cooker steam, pressure cooker valve |
| `vi-sao-phai-that-day-an-toan` | Dây an toàn đang cài/khoá, hoặc ảnh thử va chạm với hình nộm | seat belt buckle, crash test dummy |
| `vi-sao-phanh-tai-sinh-giup-xe-dien-sac-lai-pin` | Xe điện đang sạc hoặc bảng đồng hồ có biểu tượng thu hồi năng lượng | electric car charging, regenerative braking dashboard |
| `vi-sao-taipei-101-treo-mot-con-lac-khong-lo` | Quả cầu giảm chấn bên trong Taipei 101 (ưu tiên) hoặc toà nhà | Taipei 101 tuned mass damper |
| `vi-sao-tim-duoc-tam-dong-dat-chi-bang-ba-tram-do` | Địa chấn kế / bản ghi sóng địa chấn (seismogram) thật | seismograph, seismogram record |
| `vi-sao-van-dong-vien-xoay-nhanh-hon-khi-thu-tay` | Vận động viên trượt băng nghệ thuật đang xoay, tay thu sát người (chụp xa/mờ mặt) | figure skater spin, camel/upright spin |

## 7. Đầu ra Gemini trả về (để Claude nạp)
Mỗi bài một mục, JSON, **không bịa**: trường nào không chắc thì để `null` và ghi lý do vào `note`.
```json
{ "slug": "...", "fileUrl": "link trang file trên Commons", "downloadUrl": "link tải trực tiếp",
  "author": "...", "license": "CC BY-SA 4.0", "licenseUrl": "...", "altVi": "...", "note": "..." }
```
Gemini chỉ **tìm và khai báo**. Claude đối chiếu từng link với trang gốc (giấy phép, tác giả có khớp không) trước khi nạp; ảnh nào lệch thì loại.

## 8. Mã quy tắc
H1 (ảnh trả lời một câu hỏi), M5 (nền trắng), M4/E1 (đúng/sai kèm chữ, nhãn A. B. C.), D2 (nút ≥44px), B4 (không chuyển động), N1 (một câu đố/thẻ, không điểm, không xếp hạng), G2 (không màu bão hoà kéo chú ý).

## 9. Vòng 1 (14/10/2026): 7/8 ảnh đã nạp, còn `van-dong-vien-xoay-nhanh-hon-khi-thu-tay`
Đã đối chiếu từng ảnh bằng API Commons (tác giả + giấy phép khớp 8/8; 3 link `downloadUrl` của Gemini sai mã băm nên Claude lấy link từ API). Dữ liệu gốc Gemini: `scripts/data/anh-vat-ly-quanh-ta/ket-qua.json`.
Ảnh trượt băng `John_Hamer.JPG` bị loại: 368×640px (quá nhỏ), có logo nhà tài trợ, nhận ra mặt một VĐV cụ thể. Các ảnh thi trượt băng Lillehammer/Youth Olympics cũng loại: tư thế dang tay (ngược với bài, bài nói về **thu tay**) và nhiều VĐV là trẻ vị thành niên.
**Yêu cầu vòng 2 cho Gemini** (một ảnh duy nhất): người xoay tròn với tay **thu sát người** (spin đứng của trượt băng, hoặc pirouette múa ba lê, hoặc ghế xoay), rộng ≥1600px, CC0/CC BY/CC BY-SA, không logo tài trợ, chụp xa hoặc không rõ mặt, người lớn. Nếu không có ảnh đạt thì để trống, khung "?" vẫn dùng được.
Ghi chú các ảnh đã nạp: ảnh chim là dây rào kim loại (không phải dây điện cao thế), ảnh xe là xe đang sạc (không thấy phanh tái sinh) — alt đã mô tả đúng cái thấy trong ảnh.

## 10. Bài vận động viên xoay: dùng video của thầy (14/10/2026)
Thay ảnh Gemini bằng video thầy tự quay ở sân băng (file gốc từ điện thoại, 576×1024, cắt từ giây 1,4). Thẻ dùng một khung hình tĩnh (`-the.webp`, tay dang ra), trong bài là clip bấm để phát (`public/videos/blog/<slug>.mp4`, `preload="none"` + poster, V5/V7) kèm dòng "Nhìn vào". Ghi công: Ngô Diệu Thạch, CC BY 4.0 (đề xuất của Claude, thầy đổi được); `sourceUrl` trỏ về chính bài (đã thêm `thachlab.id.vn` vào danh sách nguồn của script kiểm). Video của chính chủ: không cần đối chiếu giấy phép.
