# Ô 📌 Chốt mục trỏ ruột tập (thầy chốt 25/11/2026, bài mẫu: Boyle–Charles L12, lesson 7)

Mẫu chuẩn: `content/lesson-samples/l12-boyle-charles/theory.src.html` (commit `839d1fac5` + `f25d7c224`).
Trang học đã tự chia mỗi `<h3>` thành từng bước "Tiếp" theo `<h4>`/`.tl-trap` (`splitTheorySteps`) — không phải sửa code.

## Ô Chốt mục — đặt cuối MỖI mục kiến thức (trước `<h4>` / `<h3>` kế tiếp)
```html
<div class="tl-box tl-keep tl-chot"><p class="tl-label">Chốt mục</p>
<p class="tl-chot-h">🎯 Cần nắm</p>
<details class="tl-details tl-more"><summary>Câu hỏi nhớ lại (có dấu ?)</summary><p>Đáp ngắn.</p></details>
<details class="tl-details tl-more tl-chot-ghi"><summary>✍️ Tập ô 2·2 · đối chiếu 2 dòng</summary><ul><li>…</li></ul></details>
</div>
```
- 🎯: MỘT câu nhớ lại. **Lấy câu Trả bài có sẵn** của bài đúng mục đó chuyển lên (N4 — không thêm câu mới làm phình bài); mục Trả bài cuối bài chỉ giữ câu còn lại, đánh số lại.
- ✍️: 2–3 dòng ý cốt lõi, **trỏ ô ruột tập** đang chứa đúng các ý đó (đọc `scripts/ruot-tap/<file bài>.mjs`: `h3(k, 'tên', 'trang·ô')`). Không có ô Tập nào chứa ý đó → giữ `✍️ Ghi vở · N dòng` và ghi vào báo cáo.
- Mục "Mang về" cuối bài: thay danh sách bằng một dòng "Ruột tập: điền đủ các ô …. Ô nào còn trống, mở dòng ✍️ trong ô Chốt mục tương ứng ở trên."
- Bài 1–2 mục kiến thức: 2–3 ô là đủ; bài thực hành: một ô cuối phần Kết quả/Rút ra (nếu Tập có ô tương ứng).

## Nhãn `data-tap` (trình chiếu hiện "Tập: trang · ô")
Gắn trên `<h3>` và `<h4>` mục: `data-tap="trang.ô"` hoặc `"trang.ô-ô"` — trang 1–5 tính trong bài (không phải số trang quyển). Lấy đúng từ đối số thứ ba của `h3(...)` trong file ruột tập.

## Kiểm trước khi commit
1. `python3 build_figs.py && python3 build_bundle.py` trong thư mục bài (bài không có `build_figs.py` thì theo README/skill của thư mục).
2. `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py <thư mục>/theory.html` — 0 lỗi cứng; tổng từ hiện ngay không tăng quá ~2% so với trước.
3. Ruột tập: so từng ô ✍️ với nội dung ô Tập (cùng ý, cùng ký hiệu, cùng số liệu). Web lệch Tập về số liệu → không tự sửa, ghi báo cáo.
4. Commit theo đường dẫn từng thư mục bài. KHÔNG đăng DB (thầy duyệt rồi mới chạy `cap-nhat-ly-thuyet.sh`).
