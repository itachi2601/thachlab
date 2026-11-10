# Prompt điều phối + prompt agent — cập nhật thí nghiệm 20 bài L12

Chép nguyên khối, thay chỗ `<…>`. Chạy trên Mac (cần `.env.local` để đăng). Mỗi lô 2–3 bài cùng chương.

## Phân vai (theo AGENTS.md "Phân công mô hình")

| Việc | Agent | Lý do |
|---|---|---|
| Điều phối lô, gộp, đăng DB, ghi sổ | **phiên chính** (Opus) | cần `.env.local`, terminal, quyết định cắt chữ |
| Soạn lại hộp thí nghiệm + JSON + build + lint cho MỘT bài | `general-purpose` (mặc định Opus; không hạ xuống Sonnet vì phải tính số liệu và viết cơ chế vật lí) | mỗi agent một thư mục bài, chạy song song không đụng nhau |
| Kiểm chéo ảnh 375px + tự giải quiz + tính lại bảng | `kiem-code` (Sonnet) | rẻ, chỉ đọc; ảnh không vào phiên chính |
| Sửa theo phản hồi kiểm | gửi `SendMessage` cho **chính agent soạn** bài đó (giữ ngữ cảnh), không mở agent mới | |

Không dùng `chep-de`, `nhap-du-lieu-hoc-sinh`, Cursor/Gemini cho việc này (nội dung lý thuyết, không có dữ liệu học sinh).

## Lô đề xuất

| Lô | Bài (id) | Ghi chú chung của lô |
|---|---|---|
| 1 | Thực hành nhiệt (5), Nội năng (4) | ký hiệu chung `Q = UIt = Pτ`, `c`, `λ`; đề 2025 II.1 + 2026 II.4; bài 5 phải THÊM thí nghiệm phễu nước đá + dây điện trở hai giai đoạn |
| 2 | Thực hành cảm ứng từ (12), Lực từ (11) | cân dòng điện, hướng B từ N sang S, bàn tay trái, `F = BIL sinα`; đề 2025 II.2 + 2026 II.1 |
| 3 | Phóng xạ (18), An toàn phóng xạ (19) | phông nền, √N, bảng theo thời gian; **bài 18 sửa bảng chưa trừ phông** |
| 4 | Sự chuyển thể (2), Thang nhiệt độ (3) | **bài 2 sửa bảng đun đá** cho khớp một công suất; cả hai lộ kết quả T2 |
| 5 | Boyle–Charles (7), PT trạng thái (8), Áp suất–động năng (9) | tích/tỉ số không đổi (T8), ký hiệu `p, V, T` chung |
| 6 | Cảm ứng điện từ (13), Khái niệm từ trường (10), Ứng dụng cảm ứng (126) | Faraday, Oersted, Foucault; bài 13 cân nhắc thêm thanh trượt trên ray `e = Blv` (đề 2026 III) |
| 7 | Động học phân tử (6), Năng lượng liên kết (16), Phân hạch (17) | bài 6 hết quỹ chữ; bài 17 chỉ đổi nhãn + vá T7 |
| 8 (vá nhẹ) | Dòng xoay chiều (14), Máy phát–biến áp (125), Điện từ trường (127) | chỉ T5, T6, T7, T9; không dựng lại hộp |

---

## A. Prompt cho PHIÊN CHÍNH (điều phối một lô)

```
/cap-nhat-thi-nghiem-l12 Lô <N>: bài <slug1> (id <id1>) và <slug2> (id <id2>).

Đọc docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md mục 2–3 và .claude/skills/cap-nhat-thi-nghiem-l12/SKILL.md (bảng mục 1 có cột
"Rà 25/10" ghi lỗi từng bài). Bài mẫu: content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/theory.src.html mục I, II.3.

Làm theo thứ tự, không hỏi từng bước:
1. Chạy lint_do_dai.py cho từng bài, ghi số từ hiện ngay làm mốc.
2. Mở MỖI bài một agent general-purpose chạy song song với prompt B (điền slug, id, dòng "Rà 25/10" của bài, ký hiệu chung
   của lô). Hai agent không chung thư mục; file dùng chung (index.json, SKILL.md, docs) agent KHÔNG được sửa.
3. Agent soạn xong → mở kiem-code với prompt C cho từng bài. Lỗi "chặn" → SendMessage cho chính agent soạn sửa, kiểm lại.
4. Chạy lại thi_nghiem.py một lần ở phiên chính để sinh index.json; lint_do_dai 0 lỗi cứng; check_quizzes OK.
5. Đưa tôi ảnh xem thử (sec-0 + ảnh mục có hộp 6 ô) rồi ĐĂNG từng bài:
   cd /Users/MAC/Projects/thachlab && bash scripts/cap-nhat-ly-thuyet.sh <đường dẫn tuyệt đối theory.html> <id> --yes
   trong tab terminal; đọc dòng "đã đối chiếu trước/sau".
6. Ghi sổ: ✓ + ngày vào bảng SKILL.md, bảng mục 4 docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md, STATE.md; nhật ký rút kinh nghiệm
   cuối SKILL.md. Commit theo đường dẫn (không commit xem-thu/), push.
Báo một lần cuối: mỗi bài đổi gì, số từ trước/sau, file sao lưu, bài học.
```

## B. Prompt cho agent `general-purpose` (soạn MỘT bài)

```
Thư mục làm việc: /Users/MAC/Projects/thachlab (hoặc worktree hiện tại). Chỉ sửa trong thư mục
content/lesson-samples/<slug>/ và các file content/thi-nghiem/tn-l12-<tiền tố>-NN.json của bài này. KHÔNG sửa
index.json, SKILL.md, docs/, AGENTS.md, file của bài khác.

Việc: viết lại PHẦN THÍ NGHIỆM của bài <tên bài> (id <id>) theo docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md (đọc mục 2 T1–T12
và mục 3 checklist trước). Bài mẫu đã đạt: content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/theory.src.html
(mục I: hộp Dự đoán không lộ kết quả; mục II.3: hộp 6 ô + bảng trong details + quiz "phát biểu nào sai") và
content/thi-nghiem/tn-l12-hatnhan-03.json (trường gia_thuyet / du_doan_neu_dung / khong_chung_minh).

Kết quả rà 25/10 của bài này (sửa đúng các điểm này, không mở rộng):
<dán dòng "Rà 25/10" của bài từ bảng SKILL.md>

Ký hiệu + số liệu dùng chung trong lô (để hai bài không lệch nhau): <ví dụ: Q = UIt = Pτ; c nước 4 180 J/(kg·K);
λ nước đá 3,34·10⁵ J/kg; g = 9,8 m/s²>

Đề thi liên quan (lấy đúng từ ngữ của đề, T10): <dán 4 ý a)–d) câu đề TN THPT tương ứng, hoặc ghi "không có">

Ràng buộc cứng:
- Thí nghiệm kinh điển → hộp 6 ô đúng thứ tự: Giả thuyết cần kiểm / Dự đoán nếu đúng / Dụng cụ và cách đo (details
  trong li nếu dài; có dòng "Coi rằng… / Bỏ qua…" in đậm chữ đầu) / Quan sát (chỉ điều thấy, không "vì/nên/chứng tỏ")
  / Rút ra / Chưa nói được gì. Thí nghiệm minh hoạ nhỏ giữ 3 ô.
- Kết quả không xuất hiện trước hộp Dự đoán; câu dự đoán hỏi HIỆN TƯỢNG. Sửa mở bài nếu đang lộ.
- Thí nghiệm đo: sai số có CHIỀU (lớn hơn/nhỏ hơn giá trị thật) + ít nhất một cách giảm; bảng số liệu có câu "em tự
  tính ô cuối" và ghi nguồn (minh hoạ hay đo thật). Số liệu phải khớp mô hình: TÍNH LẠI BẰNG SCRIPT, ghi công thức
  dùng; không ước lượng bằng mắt. Nếu bảng cũ sai (ghi trong dòng Rà), sửa số và sửa luôn so_lieu_mau trong JSON.
- Quiz ngay sau hộp: "phát biểu nào sai?" 4 phương án A–D = hiện tượng / kết luận / cơ chế / giới hạn, đúng 1 ô
  tl-ok; feedback nhắc đúng tên phương án; thêm dòng "⚠ Khung: hiện tượng – kết luận – cơ chế – giới hạn."
  KHÔNG thay đổi số quiz của bài (sửa quiz có sẵn, không thêm/bớt) để dòng "N câu tự kiểm tra" và tập in không lệch.
- Không đụng Bẫy, Trả bài, Bài toán mẫu, Mang về, thuộc tính data-tap, số mục <h3>/<h4>. Không dùng vai "thầy".
- Hạn mức: tổng từ hiện ngay ≤ 2 500, mục con ≤ 480, đoạn liền ≤ 300 (lint_do_dai.py). Khung 6 ô thêm 120–180 từ,
  nên cắt theo thứ tự: Dụng cụ + Làm vào details → bảng vào details → thí nghiệm mô hình/analog vào details (giữ
  data-exp) → bỏ gạch đầu dòng trùng ý với hộp → rút ngắn phương án quiz. Không cắt Bẫy/Trả bài. Vẫn vượt → dừng,
  báo lại số từ, không tự tách mục.
- JSON: thí nghiệm lịch sử → file mới loai "vi_du" đủ trường bắt buộc (xem content/thi-nghiem/README.md) + 3 trường
  mới; thí nghiệm đo có sẵn → thêm 3 trường + sai_so_thuong_gap có chiều; so_lieu_mau khớp bảng trong bài.
- PhET có mô hình đối chứng → bước Thử chạy mô hình sai trước.

Cách làm: sửa theory.src.html bằng script Python có assert chuỗi cũ (lưu script ở thư mục scratchpad, không commit),
rồi trong thư mục bài chạy python3 build_figs.py && python3 build_bundle.py. Kiểm bằng
python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/{lint_theory,lint_do_dai,check_quizzes,thi_nghiem}.py
<dir>/theory.html (bỏ qua lỗi video-theo-bai.json của bài cd*), rồi build_preview.py <dir>/theory.html <dir>/xem-thu
và chup_anh.py <dir>/xem-thu. Không commit, không ghi DB.

Báo về (≤ 25 dòng): số từ hiện ngay trước/sau; hộp nào thành 6 ô; mở bài sửa gì; quiz nào đổi; file JSON đã
thêm/sửa; kết quả 4 lint; tên ảnh xem thử của mục có hộp; điều chưa làm được và vì sao.
```

## C. Prompt cho agent `kiem-code` (kiểm MỘT bài sau khi agent soạn báo xong)

```
Thư mục: /Users/MAC/Projects/thachlab (hoặc worktree). Chỉ đọc, không sửa.
Soát bài <tên> (id <id>) vừa sửa phần thí nghiệm theo docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md (mục 2–3).

1. Ảnh 375px: content/lesson-samples/<slug>/xem-thu/sec-0.webp và <ảnh mục có hộp 6 ô>. Báo chữ chạm mép, bảng tràn,
   details trong li lệch, nhãn SVG chồng, dấu câu rơi đầu dòng sau công thức. Mở details không chụp được thì nói rõ.
2. Nội dung content/lesson-samples/<slug>/theory.src.html — chỉ mục I, hộp .tl-box--exp và quiz ngay sau, bước Thử PhET:
   - Chạy checklist mục 3: hộp kinh điển đủ 6 ô? kết quả có lộ trước Dự đoán? ô Quan sát có "vì/nên/chứng tỏ"?
     có dòng Coi rằng/Bỏ qua và Chưa nói được gì? sai số có chiều + cách giảm? bảng có câu kiểm + nguồn?
   - Tự tính lại MỌI số trong bảng và trong lời giải thích sai số từ công thức mô hình (viết phép tính ra).
   - Tự giải từng quiz từ đề: đúng 1 tl-ok, nhiễu không vô tình đúng, feedback không gọi phương án không tồn tại.
   - Đối chiếu so_lieu_mau trong content/thi-nghiem/tn-l12-<tiền tố>-*.json với bảng trong bài; 3 trường
     gia_thuyet / du_doan_neu_dung / khong_chung_minh có chưa.
   - grep "thầy" phải = 0; lint_do_dai.py 0 lỗi cứng.
Trả về: danh sách lỗi theo mức (chặn / nên sửa / nhỏ), mỗi lỗi một dòng kèm chuỗi cần tìm trong file; không có thì ghi "sạch".
```

## D. Lệnh đăng (phiên chính, Mac, sau khi kiểm sạch và thầy xem ảnh)

```bash
cd /Users/MAC/Projects/thachlab && bash scripts/cap-nhat-ly-thuyet.sh /Users/MAC/Projects/thachlab/content/lesson-samples/<slug>/theory.html <id> --yes
```

Đọc dòng `✓ Đã ghi body_html … đã đối chiếu trước/sau: N mục khác của bài không đổi`; ghi tên file sao lưu vào báo cáo.
Làm trong worktree thì thay đường dẫn `theory.html` bằng đường dẫn tuyệt đối trong worktree (script vẫn chạy từ checkout chính).
