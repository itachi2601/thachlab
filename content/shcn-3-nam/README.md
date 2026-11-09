# Bài SHCN 3 năm — bản sinh viên & kịch bản giảng viên

Nội dung đầy đủ cho chương trình ở `docs/SHCN-CHUONG-TRINH-3-NAM.md` (6 HK × 16 tiết có nội dung:
K = khởi động, 1–14 = bài, T = tổng kết; 2 tuần đệm không có bài).

## Cấu trúc thư mục

```
content/shcn-3-nam/
  hk1/ b00.sv.md b00.gv.md  b01.sv.md b01.gv.md … b14.* b15.*   (b00 = K, b15 = T)
  hk2/ … hk6/
```

Mỗi bài có **2 file**: `.sv.md` (sinh viên tự đọc) và `.gv.md` (kịch bản giảng viên dạy). Bài mẫu
chuẩn: `hk1/b03.sv.md`, `hk1/b03.gv.md` — đọc trước khi soạn bài khác.

## Front matter (giống nhau ở cả hai file)

```yaml
---
hk: 1
bai: 3            # 0 = khởi động, 15 = tổng kết
ten: "Tiền tháng đầu"
mach: [TL]        # TL, SK, KN, TĐ
chu_de: "Chủ đề 2: Kỹ năng sống"
trong_tam: "Quản lý thời gian và tiền bạc"   # ghi biên bản, trùng tên mục con trong lib/shcn/gddd-topics.ts
ban: sv           # sv | gv
---
```

## Bản sinh viên (`.sv.md`) — 450–700 chữ, đọc trong ≤5 phút trên điện thoại

Xưng "bạn". Câu ngắn, mỗi đoạn ≤4 dòng, không lý thuyết dài. Thứ tự cố định:

1. `# Tên bài` + một dòng in nghiêng: *Sau bài này bạn sẽ…* (1 câu, động từ làm được).
2. `## Chuyện của Minh` (hoặc nhân vật khác) — tình huống 3–5 câu, giống đời thật SV cao đẳng ở TP.HCM.
3. `## 3 điều cần nhớ` — đúng 3 mục đánh số, mỗi mục: một câu in đậm dễ nhớ + 1–3 câu giải thích/ví dụ.
4. `## Làm ngay` — một công cụ dùng được: bảng, checklist, mẫu câu, phiếu tự điền.
5. `## Việc tuần này` — 1 việc ≤15 phút/ngày + câu mẫu "Nếu … thì tôi sẽ …".
6. `## Tự kiểm tra` — 3 câu hỏi ngắn (tình huống, chọn/giải thích), đáp án gọn trong
   `<details><summary>Đáp án</summary>…</details>`.
7. `## Cần giúp?` (chỉ khi bài có liên quan: tiền, sức khoẻ, an toàn, tâm lý, pháp lý) — ai/nơi nào để hỏi.
8. `## Đọc thêm` (tuỳ chọn) — các mục con còn lại của chủ đề chính thức, hoặc 1–2 nguồn uy tín (tên tổ chức, không bịa link).

## Bản giảng viên (`.gv.md`) — 700–1.200 chữ, dạy được ngay không cần soạn thêm

Xưng hô trong lời thoại: GV gọi "các em". Thứ tự cố định:

1. `# Tên bài — kịch bản giảng viên`
2. `## Thông tin nhanh` — bảng: Mục tiêu (1–2 câu đo được) · Ghi biên bản (chủ đề · trọng tâm) ·
   Chuẩn bị (in phiếu bao nhiêu bản, chiếu gì, đồ dùng) · Ai dẫn (năm 1: GV; năm 2: GV + nhóm SV dẫn
   phần Làm; năm 3: nhóm SV dẫn, GV chốt).
3. `## Đầu tiết (trong 5' ổn định)` — câu hỏi lại việc tuần trước (cụ thể theo bài trước).
4. `## Kịch bản 20'` — 4 phần có mốc phút: **Mở (2')** · **Cốt lõi (5')** · **Làm (10')** · **Chốt + việc tuần (3')**.
   Mỗi phần: việc GV làm + **lời thoại gợi ý** (dạng `> "…"`) + câu trả lời SV hay gặp và cách GV đáp.
5. `## Phiếu hoạt động` — nội dung ĐẦY ĐỦ để in/chiếu: tình huống, số liệu, tin nhắn mẫu, bảng trống.
   Không ghi "GV tự chuẩn bị 8 tin nhắn" — phải viết sẵn đủ 8 tin.
6. `## Đáp án / gợi ý chốt` cho phiếu.
7. `## Lưu ý` — nhạy cảm, SV khó khăn, lớp đông (80+ SV: chia nhóm theo dãy bàn), phương án khi thiếu thời gian (bỏ gì trước).
8. `## Nếu còn thời gian / mở rộng` (tuỳ chọn, 1–3 dòng).

## Quy tắc nội dung (bắt buộc)

- **Không bịa số liệu pháp lý/hành chính có thể sai**: mức lương tối thiểu vùng, mức giảm trừ thuế
  TNCN, tỉ lệ đóng BHXH, mức phí BHYT SV, điều khoản quy chế đào tạo của trường, số đường dây nóng
  ngoài 113/114/115. Viết dạng hướng dẫn tra cứu ("tra mức hiện hành trên trang Bộ LĐ-TB-XH / hỏi phòng
  Đào tạo") và với bản GV đánh dấu `**[GV kiểm tra trước khi dạy: …]**`.
- Giá cả sinh hoạt (tiền trọ, bữa ăn, xăng) được dùng làm số ví dụ, ghi "khoảng", mức TP.HCM 2026.
- Căn cứ nghiên cứu chỉ nêu khi chắc chắn (tác giả, năm), không trích nguyên văn, không bịa.
- Tình huống dùng **nhân vật giả định** (Minh, Lan, Tuấn, Vy, Khoa… SV cao đẳng kỹ thuật Cao Thắng,
  ngành cơ khí/điện/ô tô); không yêu cầu SV kể chuyện riêng về tiền, gia đình, tình cảm, sức khoẻ.
- Chủ đề nhạy cảm (tâm lý, sức khoẻ sinh sản, chất gây nghiện, quấy rối): bản GV có mục Lưu ý ghi rõ
  khi nào chuyển cho y tế/ tư vấn trường, không hỏi riêng trước lớp.
- Không chép nguyên văn tài liệu GDĐĐ&PTNN hay sách; viết bằng lời mình.
- Markdown thuần (tiêu đề, danh sách, bảng, `<details>`); không HTML khác, không ảnh.
