---
name: phet
description: Chọn, kiểm và nhúng mô phỏng PhET (iframe) vào bài lý thuyết/bài tập mẫu thachlab — tìm sim khớp bài, kiểm URL sống + có tiếng Việt, mở thật để xác nhận màn hình/điều khiển trước khi viết bước "Thử", viết 2–3 nhiệm vụ có câu dự đoán, nhúng trong <details> không tràn 375px, ghi nguồn CC BY 4.0. Dùng khi thầy nói "thêm PhET cho bài X", "bài này có sim nào", "kiểm lại các PhET đã nhúng", "/phet", hoặc khi chặng 2 của bai-hoc-tron-goi cần mô phỏng. KHÁC tai-nguyen-bai-hoc (kế hoạch hình/video tổng thể) — skill này chỉ lo PhET.
---

# PhET cho bài học thachlab

Quy tắc chọn công cụ nằm ở `tai-nguyen-bai-hoc` (PhET khớp thì dùng PhET, đừng sinh ảnh). Skill này là quy trình đầy đủ cho riêng PhET. Bản quyền: PhET CC BY 4.0, nhúng iframe + ghi nguồn, không tải về đăng lại.

## Quy trình
1. **Chọn sim theo chỗ khó hình dung**, không theo chủ đề chung chung. Mỗi bài 1–2 sim; sim chỉ đáng nhúng khi học sinh đổi được một đại lượng và thấy hệ quả ngay. Bảng gợi ý bên dưới.
2. **Kiểm URL** (Bash, không cần trình duyệt): `curl -s -o /dev/null -w '%{http_code}' 'https://phet.colorado.edu/sims/html/<sim>/latest/<sim>_all.html?locale=vi'` phải 200. Không chắc có tiếng Việt thì thử `?locale=vi` rồi mở xem; thiếu thì dùng bản gốc và ghi trong bước Thử tên nút tiếng Anh.
3. **Mở thật sim** bằng browser pane (`preview_start` với `url`) và ghi lại: có mấy màn (tab), tên màn, điều khiển nào có (thanh đổi khối lượng? bật ma sát? biểu đồ cột?). **Chỉ viết bước "Thử" dựa trên điều đã thấy**; đừng giả định màn/nút. Đợt 12/10/2026 ba agent viết bước Thử theo trí nhớ và phải để thầy bấm thử — đó là việc skill này loại bỏ. Không mở được thì ghi rõ "CHƯA thử" trong `TIEN-DO.md`.
4. **Viết nhiệm vụ** (2–3 bước, mỗi bước một thao tác + một quan sát), mở đầu bằng **câu dự đoán** ("Theo em… sẽ thế nào?") trước khi bấm — QUY-TAC-THIET-KE (tải nhận thức, học chủ động). Một câu hỏi chốt ở cuối: "Rút ra điều gì?". Không gợi sẵn đáp án ngay trên sim.
5. **Nhúng** đúng khuôn dưới đây. Vị trí: sau đoạn kiến thức liên quan, TRONG `<details>` (đóng mặc định) để không làm bài dài/nặng; không đặt trên đầu bài.
6. **Kiểm 375px**: iframe không tràn ngang (`max-width:100%`, `box-sizing:border-box`); chụp trang xem thử.
7. **Ghi `TIEN-DO.md`**: sim nào, đã mở thử hay chưa, màn/nút đã xác nhận. Chưa thử thì để thầy biết.

## Khuôn nhúng
```html
<details class="tl-details">
<summary>🧪 Thử với mô phỏng: <tên ngắn></summary>
<iframe src="https://phet.colorado.edu/sims/html/<sim>/latest/<sim>_all.html?locale=vi" width="100%" height="520" style="border:1px solid #ddd;border-radius:8px;box-sizing:border-box;max-width:100%;display:block" allowfullscreen loading="lazy" title="Mô phỏng PhET: <tên>"></iframe>
<p><strong>Thử:</strong></p>
<ol>
<li>…</li>
</ol>
<p><small>Mô phỏng: PhET Interactive Simulations, Đại học Colorado Boulder (CC BY 4.0).</small></p>
</details>
```
Mỗi bước một `<li>`. Nhãn a) b) c) cho câu hỏi thi thì dùng `<p>a) …</p>`, không dùng `<ol type="a">` (hiện "a.").

## Gợi ý sim (kiểm lại URL mỗi lần)
| Chỗ khó hình dung | Sim |
|---|---|
| Động năng, thế năng, cơ năng, ma sát → nhiệt | `energy-skate-park-basics` |
| Con lắc, chuyển hoá năng lượng | `pendulum-lab` |
| Công, lực, gia tốc, ma sát trượt | `forces-and-motion-basics` |
| Ném xiên | `projectile-motion` |
| Mạch điện, Ohm, nối tiếp/song song | `circuit-construction-kit-dc` |
| Lực – đòn bẩy | `balancing-act` |
| Lò xo | `masses-and-springs` |
| Sóng | `wave-on-a-string` |
| Khí, chuyển thể | `gas-properties`, `states-of-matter` |
| Va chạm | `collision-lab` |
| Quang hình | `geometric-optics` |
| Cảm ứng điện từ | `faradays-law` |

## Không làm
- Không viết bước Thử cho màn/nút chưa nhìn thấy; không nhúng sim chưa kiểm HTTP 200.
- Không nhúng quá 2 sim/bài; không để sim thay phần giải thích (sim chỉ để khám phá).
- Không dùng sim làm đáp án cho câu kiểm tra.
- Trang hiển thị bài (`ContentHtml`) có thể lọc `<iframe>`: sau khi đăng, mở bài thật; nếu mất, đổi sang nút liên kết mở tab mới và báo thầy.

## Nhật ký rút kinh nghiệm
Dạng: `- YYYY-MM-DD · <sự cố> → <quy tắc>`.
- 2026-10-12 · Tạo skill sau đợt L9 cơ học (bài 129–131): 3 agent soạn bước "Thử" cho PhET theo trí nhớ, cả 3 báo "cần thầy bấm thử" → bắt buộc mở sim thật (bước 3) và ghi đã thử/chưa thử vào TIEN-DO.
- 2026-10-18 · Đợt L12 ch1–2: `build_figs.py` sinh lại SVG khác bản trong DB nên build lại `theory.html` sẽ lẫn thay đổi hình → chèn khối PhET thẳng vào cả `theory.src.html` lẫn `theory.html` (chỉ thêm dòng), diff chỉ được là `+`. Sim `gas-properties` giữ ~300 K khi nén tường nên KHÔNG viết "nén thì nóng"; thanh Nóng–Mát nhích ~1 K mỗi lần kéo, không dùng để minh hoạ tiến sát 0 K. WebSearch không lập chỉ mục YouTube → video chuyển sang `prompts-video.md` ngay, đừng tốn lượt tìm.
- 2026-10-18 · Làm hàng loạt 49 bài, 55 khối (6 đợt) → quy trình chạy tốt: (1) lập bảng một file `content/tai-nguyen/<đợt>/kehoach.md`, dừng cho duyệt; (2) mở thật mỗi sim, ghi cột "Đã thử/CHƯA thử"; (3) so `theory.html` với DB trước (giống hệt mới chèn); (4) chèn thẳng vào `theory.src.html` và `theory.html` (diff chỉ `+`), lint; (5) `cap-nhat-ly-thuyet.sh --yes` cả lô trong terminal (đã tự dry-run + đối chiếu); (6) deploy một lần; (7) kiểm live bằng `fetch('/data/lessons/<id>.json')` rồi đo iframe ở 375px (xoá service worker + cache trước khi tải lại). Sim mở lần đầu trong pane có thể treo ở logo: tải lại trang là hết. Tab terminal có thể đóng giữa chừng: mở tab mới.
