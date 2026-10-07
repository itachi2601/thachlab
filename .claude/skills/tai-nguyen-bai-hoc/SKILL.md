---
name: tai-nguyen-bai-hoc
description: Lập kế hoạch tài nguyên trực quan (hình minh hoạ, hình vẽ kỹ thuật, mô phỏng PhET, video thí nghiệm) cho một bài lý thuyết/bài tập thachlab từ file .tex, đứng ở vị trí học sinh để chọn công cụ phù hợp cho từng chỗ khó hình dung; xuất sẵn prompt cho Gemini, chèn tài nguyên vào bài, rồi chuyển sang dang-bai-hoc-thachlab để đăng. Dùng khi người dùng nói "lập kế hoạch tài nguyên cho bài này", "bài này cần hình/mô phỏng/video gì", "tạo hình cho bài", "thêm mô phỏng PhET", "tìm video thí nghiệm cho bài", hoặc đưa file .tex bài giảng Vật lý/CNC và muốn bài sinh động hơn trước khi đăng.
---

# Tài nguyên trực quan cho bài học thachlab

Mục tiêu: học sinh hiểu bài nhanh hơn nhờ **tự tương tác** hoặc **tự quan sát**, không chỉ đọc chữ.
Người dùng không phải tự viết prompt. Quy trình là bán tự động: Claude lập kế hoạch và viết prompt,
người dùng dán vào Gemini (gói Pro, không dùng API) rồi tải ảnh về thư mục, Claude kiểm tra, chèn và đăng.

## Quy trình

1. **Đọc bài như một học sinh.** Đánh dấu mọi chỗ khó hình dung: khái niệm trừu tượng, hiện tượng
   động, thao tác thực hành, đại lượng thay đổi theo điều kiện, hình mà lời văn đang tả mà chưa có.
2. **Lập bảng kế hoạch** (xem mẫu bên dưới) và **dừng lại cho người dùng duyệt** trước khi làm tiếp.
   Mỗi dòng: vị trí trong bài, học sinh vướng gì, công cụ chọn, ai làm.
3. **Làm phần của Claude ngay:** hình kỹ thuật (TikZ/matplotlib/SVG), nhúng PhET, widget HTML, kiểm tra
   link video. Xuất file `prompts.md` cho phần ảnh Gemini.
4. **Người dùng dán prompt vào Gemini**, tải ảnh về đúng thư mục, đúng tên file đã ghi.
5. **Kiểm tra từng ảnh** (xem checklist), báo ảnh nào cần sinh lại kèm prompt đã sửa.
6. **Chèn tài nguyên vào bài** rồi chuyển sang skill `dang-bai-hoc-thachlab` để đăng.

## Bảng chọn công cụ (ưu tiên tương tác hơn quan sát)

| Học sinh cần | Công cụ | Ai làm |
|---|---|---|
| Tự đổi thông số xem kết quả (ném xiên, dao động, sóng, khí, mạch điện, quang hình, chuyển thể) | **Mô phỏng PhET nhúng bằng iframe** (ưu tiên số 1) | Claude |
| Dạng tương tác mà PhET không có | Widget HTML/JS thanh trượt tự viết | Claude |
| Hình cần đúng số liệu, nhãn, ký hiệu (sơ đồ lực, mạch, đồ thị, quang hình, bản vẽ kỹ thuật) | TikZ / matplotlib / SVG | Claude |
| Hình minh hoạ đời sống, không cần đúng số (người trượt băng, xe phanh, máy phay, dụng cụ) | **Ảnh Gemini** | Người dùng dán prompt |
| Thí nghiệm thật khó mô phỏng, thao tác thực hành | Video YouTube ngắn, nhúng kèm mốc thời gian cần xem | Gemini tìm link, Claude kiểm tra |
| Hiện tượng động nhẹ | Video ngắn Gemini (nếu còn hạn mức) | Người dùng dán prompt |

Quy tắc chọn: nếu PhET có mô phỏng khớp thì dùng PhET, đừng sinh ảnh. Ảnh AI chỉ dùng khi hình **không**
cần chính xác khoa học. Không dùng ảnh AI cho sơ đồ lực, mạch điện, đồ thị, hay bất cứ hình có chữ/ký hiệu.

## Mẫu bảng kế hoạch trả cho người dùng

| # | Vị trí trong bài | Học sinh vướng ở đâu | Công cụ | Tên file / nguồn | Ai làm |
|---|---|---|---|---|---|
| 1 | §I.2 Chuyển động ném xiên | Không hình dung quỹ đạo khi đổi góc | PhET Projectile Motion | nhúng iframe | Claude |
| 2 | §I.3 Lực ma sát khi phanh | Hình dung tình huống đời sống | Ảnh Gemini | `hinh-02-phanh-xe.png` | Người dùng |

Ngắn gọn, không giải thích dài. Cuối bảng hỏi một câu: "Duyệt hay sửa dòng nào?"

## Thư mục

Thư mục làm việc (trên máy người dùng, qua Claude desktop), đặt theo lớp/chương/bài:

```
thachlab-media/
  vl12/chuong-1/bai-2/
    kehoach.md        <- bảng kế hoạch đã duyệt
    prompts.md        <- prompt ảnh Gemini
    hinh-01-<mo-ta>.png   (đánh số theo thứ tự xuất hiện trong bài)
    hinh-02-<mo-ta>.png
    video-links.md
```

Khi đăng, ảnh được copy vào repo theo quy ước của skill `dang-bai-hoc-thachlab`:
`public/lessons/<slug>/media/` và tham chiếu `/lessons/<slug>/media/<ten>.png`. Giữ nguyên tên file để khỏi
phải sửa đường dẫn.

## File prompts.md

Mỗi ảnh một khối. Người dùng phải dán được **cả file một lượt**, nên mỗi khối tự đủ ý.

```
### hinh-02-phanh-xe.png  (16:9)
<mô tả cảnh bằng tiếng Anh, cụ thể: chủ thể, hành động, góc nhìn>
<KHỐI PHONG CÁCH CHUNG>
Lưu ý khi dùng: <ghi chú nếu có>
```

**Khối phong cách chung** (dán cuối mọi prompt để cả bộ ảnh đồng bộ):

> Clean flat educational illustration, simple vector-like line art with soft muted colors, plain white
> background, no text, no letters, no numbers, no labels, no watermark, no logo, uncluttered, centered
> composition.

Quy tắc viết prompt:
- Tiếng Anh, một cảnh một ý, không nhồi nhiều chủ thể.
- **Không bao giờ yêu cầu chữ, số, ký hiệu hay mũi tên có nhãn trong ảnh.** Nhãn thêm sau bằng LaTeX hoặc chú thích dưới ảnh.
- Nói rõ tỉ lệ khung hình (16:9 cho ngang, 1:1 cho vuông, 3:4 cho đứng).
- Thiết bị/dụng cụ phải mô tả đúng bản chất (ví dụ "CNC vertical milling machine, enclosed guard, tool in spindle") để tránh AI vẽ sai cấu tạo.
- Ảnh người trượt băng: nêu rõ giày trượt băng nghệ thuật hay tốc độ, tư thế, hướng chuyển động.

## Nhúng PhET

Dạng nhúng (dùng bản tiếng Việt khi có):

```html
<div class="my-4">
  <iframe src="https://phet.colorado.edu/sims/html/<ten-sim>/latest/<ten-sim>_all.html?locale=vi"
          width="100%" height="520" style="border:1px solid #ddd;border-radius:8px"
          allowfullscreen loading="lazy" title="Mô phỏng PhET: <tên>"></iframe>
  <p class="text-sm text-gray-600 mt-1">Mô phỏng: PhET Interactive Simulations, Đại học Colorado Boulder (CC BY 4.0).</p>
</div>
```

Một số tên mô phỏng thường dùng (**luôn kiểm tra URL còn sống bằng WebFetch trước khi dùng**, vì PhET
đổi tên/phiên bản, và bản dịch tiếng Việt không phải mô phỏng nào cũng có):
`projectile-motion`, `states-of-matter`, `gas-properties`, `pendulum-lab`, `masses-and-springs`,
`wave-on-a-string`, `forces-and-motion-basics`, `energy-skate-park-basics`, `collision-lab`,
`circuit-construction-kit-dc`, `faradays-law`, `geometric-optics`, `balancing-act`.

Luôn kèm **một câu hỏi dẫn dắt** ngay trên mô phỏng để học sinh thao tác có mục đích, ví dụ:
"Kéo góc ném từ 15° đến 75°. Góc nào cho tầm xa lớn nhất? Giải thích."

Trước khi đăng, kiểm tra trang hiển thị bài (`ContentHtml`) có giữ thẻ `<iframe>` không. Nếu bị lọc mất,
báo người dùng và đưa phương án thay: đặt nút liên kết mở mô phỏng ở tab mới.

## Video thí nghiệm

- Gemini tìm link, nhưng **không tin link chưa kiểm**. Claude mở/fetch từng link: video còn tồn tại, đúng
  nội dung, thời lượng hợp lý (ưu tiên dưới 5 phút), cho phép nhúng.
- Nhúng bằng iframe YouTube, ghi rõ **mốc thời gian cần xem** và câu hỏi quan sát:
  `https://www.youtube.com/embed/<id>?start=<giây>`
- Video đặt vào mục `video` của bài (một trong 6 mục cố định), không chèn lẫn vào lý thuyết trừ khi nó là
  một bước của lập luận.
- Ghi vào `video-links.md`: link, tên kênh, mốc thời gian, lý do chọn.

## Checklist kiểm tra ảnh Gemini (bước 5)

Mở từng ảnh, kiểm tra:
1. Đúng khoa học: hướng chuyển động/lực, cấu tạo dụng cụ, tư thế kỹ thuật, an toàn lao động (người trong ảnh CNC có kính bảo hộ, không đeo găng khi đứng gần trục quay).
2. Không có chữ/số/ký hiệu lạ hoặc watermark.
3. Phong cách khớp các ảnh khác trong bài.
4. Tỉ lệ, độ nét đủ hiển thị trên điện thoại.
5. Tên file đúng quy ước.

Ảnh lỗi: nói ngắn gọn lỗi gì, đưa **prompt đã sửa** để dán lại, không bắt người dùng tự nghĩ.

## Chèn vào bài

Chèn theo định dạng HTML của skill `dang-bai-hoc-thachlab`:

```html
<img class="figure" src="/lessons/<slug>/media/hinh-02-phanh-xe.png" alt="<mô tả ngắn nội dung hình>">
```

Alt không để trống. Sau khi chèn xong, bàn giao sang `dang-bai-hoc-thachlab` (các quy tắc an toàn của
skill đó vẫn áp dụng: không tự nhập mật khẩu, không tự deploy khi working tree có thay đổi không liên quan).

## Không làm

- Không tự gọi Gemini API hay tự động hoá giao diện gemini.google.com. Người dùng dán prompt thủ công.
- Không dùng ảnh AI cho hình có số liệu hoặc ký hiệu.
- Không bịa link video/mô phỏng. Chưa kiểm được thì ghi "chưa kiểm".
- Không bỏ qua bước duyệt kế hoạch.
- Không dùng ảnh, video có bản quyền không rõ; ưu tiên PhET (CC BY) và nguồn cho phép nhúng.
