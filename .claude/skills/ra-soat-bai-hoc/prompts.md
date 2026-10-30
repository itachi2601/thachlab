# Brief cho agent rà một bài (chép vào scratchpad, thay <REPO>, <CHƯƠNG>; cuối prompt thêm "Bài của bạn: …")

```
# Rà nội dung + vẽ lại hình SVG chưa đạt — một bài lý thuyết <CHƯƠNG>

Repo: <REPO> — chạy mọi lệnh từ đây.
Chỉ sửa file trong thư mục bài của bạn. Các agent khác làm các bài khác song song — KHÔNG đụng thư mục bài khác,
KHÔNG sửa svg_lib.py / _margin_fig.py / file dùng chung, KHÔNG git commit/stash/reset, KHÔNG ghi DB,
KHÔNG chạy cap-nhat-ly-thuyet.sh hay upload-lesson.mts. Mac không có lệnh `timeout`: đặt timeout bằng tham số Bash.

## Cấu trúc bài
- `theory.src.html` (mốc `<!--FIGn-->`) → `python3 build_figs.py` (chạy trong thư mục bài) sinh SVG, ghi `theory.html`.
- `python3 build_bundle.py` dựng `bundle.json` — chạy lại sau mỗi lần sửa.
- Thư viện: `.claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py` (defs, arrow, text, chevron, field_line, vec_luc…).
- Ảnh `<img>` (OpenStax/Commons) không vẽ lại, chỉ kiểm caption/nguồn khớp ảnh; bản xem thử không hiện ảnh /assets là bình thường.
- Chạy lại build_figs.py có thể làm MẤT `<sup class="tl-fn">` trong theory.html — so số lượng với `git show HEAD:<bài>/theory.html`, thiếu thì chèn lại y như cũ.

## Việc
1. Đọc `.claude/skills/soan-bai-ly-thuyet-tuong-tac/references/hinh-svg.md` và mục 20, 23, 27 trong
   `.claude/skills/soan-bai-ly-thuyet-tuong-tac/SKILL.md` (grep "^20\.\|^23\.\|^27\."); tiêu chí chấm ở mục 2 của
   `.claude/skills/ra-soat-bai-hoc/SKILL.md`. Đọc build_figs.py + theory.src.html của bài.
2. Rà nội dung: sai vật lí, số liệu/đơn vị, tính lại MỌI phép tính (bài toán mẫu, bảng số liệu, thử thách),
   quiz đúng một đáp án + phản hồi khớp phương án (kể cả phản hồi sai không được khen phương án sai),
   số hình đúng thứ tự xuất hiện, caption và câu nhắc hình khớp nội dung hình.
   Sửa tối thiểu lỗi CHẮC CHẮN (cả theory.src.html); chỗ nghi ngờ ghi vào báo cáo kèm số dòng. Không viết lại văn, không đổi cấu trúc.
3. Chụp: `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/build_preview.py <bài>/theory.html`
   rồi `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/chup_anh.py <bài>/xem-thu --chi-hinh`. Xem từng xem-thu/fig-*.webp.
4. Chấm từng hình đạt/chưa đạt (vật lí bằng toạ độ; chữ ≥ 14 trong viewBox ~440; không chồng/cắt; đầu V; mỗi ý một dòng; nhãn đúng loại đại lượng; thẩm mỹ).
5. Vẽ lại hình chưa đạt trong build_figs.py (giữ số hình, mốc FIG, ý của hình). Hình đạt để nguyên.
   build_figs → build_bundle → chụp lại → xem lại; tối đa 3 vòng mỗi hình.
6. Kiểm cuối: `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_theory.py <bài>/theory.html`;
   `git diff --stat -- <bài>` chỉ gồm file của bài; đếm tl-fn khớp HEAD.

## Báo cáo (≤ 40 dòng, không dán SVG)
- Bảng: hình · nội dung · đạt/chưa đạt · lỗi cụ thể (toạ độ nếu lỗi vật lí) · đã sửa gì.
- Lỗi nội dung đã sửa (dòng, trước → sau, lý do); chỗ nghi ngờ chưa sửa (dòng).
- Đường dẫn fig-*.webp sau sửa (ghi fig-n ứng với Hình mấy); file đã đổi.
```

# Tin nhắn cho agent bị treo

```
Bạn bị dừng giữa chừng (stall). Tiếp tục theo brief từ chỗ dở: kiểm git diff -- <bài> để biết đã sửa tới đâu,
làm nốt rồi gửi báo cáo theo mẫu. Đặt timeout cho lệnh chụp ảnh; sửa từng hình một.
```

# Brief kiem-code soát hình vẽ lại

```
Soát độc lập N hình SVG vừa vẽ lại (chỉ ĐỌC). Repo: <REPO>.
Ảnh 375px: <bài>/xem-thu/fig-k.webp (Hình m, nội dung …) — liệt kê từng hình.
Mã: build_figs.py của từng bài; tiêu chí: mục 2 của .claude/skills/ra-soat-bai-hoc/SKILL.md.
Trả bảng: bài · hình · ĐẠT / CHƯA ĐẠT · lỗi cụ thể kèm toạ độ/dòng build_figs.py. ≤ 25 dòng.
```
