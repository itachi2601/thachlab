---
name: vat-ly-quanh-ta
description: Soạn bài đọc "Vật lý quanh ta" cho blog thachlab (content/blog/*.md, category "Vật lý quanh ta") — giải thích một hiện tượng đời sống, hoặc một tin tức/nghiên cứu mới có ứng dụng gần gũi, bằng đúng kiến thức Vật lí THCS (KHTN 6–9) và THPT (10–12), để học sinh đọc cho tò mò, thích môn Vật lí. Mỗi bài mở bằng câu hỏi "Vì sao…?", cho em đoán trước, giải thích từng tầng, có ít nhất 2 hình minh hoạ (cảnh đời sống + sơ đồ vật lí), một phép ước lượng bằng số, một thí nghiệm an toàn tự làm ở nhà, chỉ ra bài học trên thachlab liên quan và có nguồn kiểm chứng. Dùng khi thầy nói "viết bài vật lý quanh ta", "giải thích hiện tượng X cho học sinh", "vì sao … (hiện tượng đời thường)", "tìm nghiên cứu vật lý gần gũi đời sống", "làm bài đọc thêm kích thích tò mò", "lên lịch bài vật lý quanh ta hằng tuần". KHÁC dang-tin-tuc-vat-ly (tin ngắn 80–200 chữ lên /tin-tuc, bảng posts) và soan-bai-ly-thuyet-tuong-tac (bài học chính khoá). Tìm + soạn + kiểm chạy được trên cloud; deploy phải chạy trên Mac.
---

# Vật lý quanh ta — bài đọc kích thích tò mò

**Đầu ra:** `content/blog/<slug>.md` (+ hình trong `public/images/blog/`). Trang `/blog/<slug>` là trang **tĩnh**
(`lib/blog.ts`, `marked` GFM) → bài chỉ lên web sau **commit + `bash scripts/deploy.sh`**.

**Mục đích không phải dạy đủ kiến thức mà là gây tò mò** (lý thuyết "khoảng trống thông tin" — Loewenstein 1994:
tò mò sinh ra khi người đọc thấy mình *gần* biết mà chưa biết). Vì vậy bài luôn: đặt câu hỏi trước, cho đoán,
trả lời từng tầng, và để lại một câu hỏi mở ở cuối.

Mẫu bài cũ để tham khảo giọng: `content/blog/vi-sao-co-bap-co-lai-khi-nang-ta.md` (thiếu mục Nguồn, Tự thử, liên kết bài
học — bài mới phải có đủ).

## Quy trình

1. **Chốt đề tài.** Thầy đưa hiện tượng → dùng luôn. Thầy chỉ nói "viết bài" → chọn 3 ứng viên, ưu tiên:
   (a) học sinh **đã tự gặp** (bếp, điện thoại, xe máy, mưa, thể thao, mạng xã hội);
   (b) giải thích được bằng kiến thức trong chương trình — tra `references/kho-chu-de.md`;
   (c) chương đang dạy (xem `docs/STATE.md` / hỏi 1 câu nếu không rõ);
   (d) chưa viết — `python3 .claude/skills/vat-ly-quanh-ta/scripts/kiem-bai.py --da-viet`.
   Hai nguồn đề tài: **Hiện tượng** ("Vì sao nồi áp suất nấu nhanh?") hoặc **Tin/nghiên cứu mới** có ứng dụng gần gũi
   (pin, vật liệu, y học, giao thông, thời tiết, vũ trụ nhìn thấy được). Đưa 3 ứng viên dạng 1 dòng/đề tài, thầy chọn — hoặc tự
   chọn ứng viên đầu nếu thầy đã bảo "tự chọn".
2. **Tìm & kiểm chứng.** `WebSearch`/`WebFetch` (nạp qua ToolSearch). Nguồn gốc ưu tiên: bài báo/thông cáo của ĐH–viện
   (Nature, Science, APS Physics, phys.org đối chiếu bài gốc, NASA, ESA, CERN), sách giáo khoa, trang cơ quan chính thức
   (NCHMF cho thời tiết, Bộ Y tế cho y học). Mỗi số liệu: ≥ 2 nguồn hoặc 1 nguồn gốc. Preprint / "phá vỡ định luật" /
   "năng lượng miễn phí" → bỏ hoặc nói rõ là kết quả sơ bộ. Ghi lại link cụ thể + ngày.
3. **Rút ra chuỗi vật lí** trước khi viết (chỉ để mình dùng): hiện tượng → đại lượng nào thay đổi → định luật/công thức nào
   → bài nào trên thachlab (`kiem-bai.py --tim <từ khoá>` trả id bài + link). Nếu giải thích đúng cần kiến thức ngoài chương
   trình, nói gọn đúng mức ("ở đại học em sẽ học…"), **không đơn giản hoá đến mức sai** (vd không nói "nước nóng nhẹ hơn nên
   nổi lên" khi đúng là "khối lượng riêng nhỏ hơn").
4. **Viết** theo khung `references/khung-bai.md` (tiêu đề "Vì sao…?" → tình huống → Đoán thử → giải thích từng tầng →
   Ước lượng bằng số → Tự thử ở nhà → Hiểu lầm hay gặp → Em đã học ở đâu → Nghĩ tiếp → Nguồn). Quy tắc cứng:
   - 700–1200 chữ (đọc 4–6 phút). Đoạn ≤ 4 câu, câu ngắn, thuật ngữ mới giải nghĩa ngay lần đầu (`docs/QUY-TAC-THIET-KE.md`).
   - Gọi người đọc là "em"/"chúng ta"; **không tự xưng "thầy"** trong thân bài (frontmatter `author: "Thầy Thạch"` vẫn giữ).
   - **Blog không có KaTeX**: không dùng `$…$`. Công thức viết chữ + Unicode: `p = F / S`, `v²`, `½·m·v²`, `Δt`, `≈`, `×10³`.
     Mỗi đại lượng kèm đơn vị; số thập phân dùng dấu phẩy kiểu Việt (2,5 m/s).
   - Viết **bằng lời mình**; tối đa một trích dẫn < 15 chữ, có ngoặc kép + nguồn. Không chép hình của nguồn.
   - Thí nghiệm ở nhà: chỉ đồ an toàn (nước, chai nhựa, bóng bay, đồng xu, đèn pin, điện thoại). **Cấm**: lửa trần, điện lưới,
     hoá chất, độ cao, laser chiếu mắt, lò vi sóng chạy rỗng/có kim loại. Có rủi ro nhỏ → ghi "nhờ người lớn".
   - Không lời khuyên y tế/đầu tư; chủ đề sức khoẻ chỉ giải thích cơ chế, kết bằng "hỏi bác sĩ" nếu cần.
5. **Hình — bắt buộc ≥ 2 hình minh hoạ trong thân bài (tối đa 4; thầy chốt 10/10/2026).** Gợi ý phân vai:
   hình 1 ngay sau đoạn mở = **cảnh đời sống** (cái em thấy); hình 2 trong mục giải thích = **sơ đồ vật lí** (lực, tia sáng,
   đường sức, dòng điện, phân tử… có nhãn đại lượng). Thêm hình 3 cho thí nghiệm "Tự thử ở nhà" nếu các bước khó hình dung.
   - Sơ đồ: SVG tự vẽ bằng `svg_lib.py` của skill `soan-bai-ly-thuyet-tuong-tac` (đường sức nét đứt, mũi tên V 30°,
     vectơ lực dài tỉ lệ độ lớn — quy tắc AGENTS.md). Cảnh đời sống: SVG tự vẽ, hoặc ảnh tự tạo (prompt Gemini do thầy chạy).
     Không lấy ảnh/hình của nguồn tin (bản quyền).
   - File: `public/images/blog/<slug>-<ten>.{svg,webp}`, `.webp` ≤ 150 KB, rộng ≤ 1200 px; alt mô tả đúng nội dung hình.
   - Chú thích in nghiêng ngay dưới hình, mỗi ý một dòng. Chữ trong hình đọc được ở 375 px (cỡ ≥ 14 px khi hiển thị).
   - Xem hình đã render (Chrome headless hoặc giao subagent đọc ảnh) trước khi báo xong — sai nhãn/chiều mũi tên là lỗi vật lí.
   - Ảnh `cover` (chia sẻ mạng xã hội) là `.png`/`.jpg` ≤ 150 KB, có thể dùng lại hình 1; không có thì bỏ trường `cover`.
6. **Kiểm máy:** `python3 .claude/skills/vat-ly-quanh-ta/scripts/kiem-bai.py content/blog/<slug>.md` — frontmatter, độ dài,
   không `$`, không tự xưng "thầy", đủ mục bắt buộc, link bài thachlab trỏ đúng id có thật, đủ ≥ 2 hình, hình tồn tại + đúng dung lượng,
   có ≥ 1 link nguồn https. Sửa tới khi hết ✗.
7. **Kiểm người:** giao agent `kiem-code` soát vật lí độc lập (prompt: "đọc <file>, liệt kê mọi phát biểu sai/khó hiểu với HS
   14–18 tuổi, kiểm lại phép ước lượng và đơn vị, thí nghiệm có an toàn không"). Sửa theo góp ý đúng.
8. **Đưa thầy duyệt**: đường dẫn file + tiêu đề + 2 dòng tóm tắt + nguồn đã dùng. **Duyệt là đăng** (không PR, không hỏi thêm).
9. **Đăng (Mac):** `git add content/blog/<slug>.md public/images/blog/<slug>-*` → `git commit -- <các path đó>` → deploy theo
   skill `xong-viec` (working tree có WIP phiên khác thì deploy từ worktree sạch). Phiên cloud: push nhánh `claude/*`
   (workflow tự gộp vào main), rồi in cho thầy:
   ```bash
   cd /Users/MAC/Projects/thachlab && git pull origin main && bash scripts/deploy.sh
   ```
10. **Tin dẫn (tuỳ chọn):** muốn học sinh thấy bài ở `/tin-tuc` → dùng skill `dang-tin-tuc-vat-ly` đăng 1 tin ngắn
    (câu hỏi "Vì sao…?" + 2 câu gợi tò mò + link `https://thachlab.id.vn/blog/<slug>` làm `source_url`).

## Đặt lịch định kỳ
Thầy muốn mỗi tuần một bài: dùng skill `schedule`, tác vụ chạy bước 1–7 rồi **dừng ở bước 8 chờ duyệt** — không tự deploy.

## Nhật ký rút kinh nghiệm
- 2026-10-10 · Tạo skill. Blog render bằng `marked` không có KaTeX → cấm `$…$`, viết công thức Unicode; đã có sẵn category
  "Vật lý quanh ta" (bài cơ bắp – nâng tạ) nên dùng lại đúng chuỗi đó để trang blog gom nhóm. Chưa chạy vòng thật nào:
  lần đầu xem `/blog/<slug>` ở 375 px sau deploy để kiểm hình + chú thích.
- 2026-10-10 · Thầy chốt: mỗi bài ≥ 2 hình minh hoạ (cảnh đời sống + sơ đồ vật lí) → bước 5 bắt buộc, `kiem-bai.py` báo ✗ nếu < 2.
