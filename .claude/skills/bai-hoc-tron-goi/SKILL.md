---
name: bai-hoc-tron-goi
description: Điều phối làm MỘT bài học thachlab từ đầu đến cuối (lý thuyết tương tác → tài nguyên hình/PhET/video → bài tập mẫu → rà và cập nhật → đăng) hoặc chỉ các chặng cần thiết của bài đã đăng. Skill mỏng, chỉ chọn chặng và trỏ tới skill chuyên trách; mỗi chặng chỉ đọc phần của mình. Dùng khi thầy nói "làm trọn bài X", "làm bài mới đủ lý thuyết + bài tập mẫu", "nâng cấp bài X", "bài này còn thiếu gì", "/bai-hoc-tron-goi". Việc lẻ một chặng (sửa một chữ, chỉ soạn quiz) thì gọi thẳng skill chặng đó, không qua đây.
---

# Điều phối bài học trọn gói (thầy chốt 11/10/2026)

**Skill này không chứa quy trình.** Quy trình nằm ở bốn skill chuyên trách; ở đây chỉ có: hỏi bối cảnh → chọn chặng → đọc ĐÚNG phần của chặng → ghi nhận bàn giao giữa chặng.
**Quy tắc nạp (tiết kiệm token): không đọc SKILL.md của chặng chưa tới lượt.** `soan-bai-ly-thuyet-tuong-tac` ~85 KB, `soan-bai-tap-mau` ~43 KB — mở bằng `grep -n '^## '` rồi đọc đoạn cần, không đọc cả file trừ khi lần đầu soạn bài mới.

## Bước 0 — Hỏi bối cảnh (một lần, ngắn)
1. Bài nào (Lớp → Chương → Bài, `public/data/catalog.json`); **mới hay đã đăng?** Đã đăng → đọc `lesson_items` hiện có và `content/lesson-samples/<bài>/` trước; xem còn thiếu mục nào (lý thuyết / bài tập mẫu / video / mô phỏng).
2. Chặng nào cần (mặc định theo bảng dưới). Bài đã đăng: chỉ làm chặng thiếu, đừng soạn lại cả bài.
3. Nơi chạy: soạn + kiểm làm được ở cloud; **ĐĂNG DB và deploy chỉ trên Mac** (Supabase bị chặn ở cloud).

## Các chặng

| # | Chặng | Làm gì | Đọc phần nào |
|---|---|---|---|
| 1 | Soạn lý thuyết | `theory.html`, hình SVG, `content/thi-nghiem/*.json`, `bundle.json` | `soan-bai-ly-thuyet-tuong-tac`: mục **Quy trình** (bước 1–6) + **Dàn ý** + **Giọng văn**; lần đầu thì đọc thêm **Bài học rút ra** |
| 2 | Tài nguyên | Hình AI (prompt Gemini), PhET, clip YouTube | Video mở bài / hộp thí nghiệm: **bước 4c** của skill chặng 1. Hình AI/PhET: `tai-nguyen-bai-hoc` mục **Bảng chọn công cụ**, **Nhúng PhET**, **Checklist kiểm ảnh**, **Không làm** |
| 3 | Bài tập mẫu | Quét số dạng → nháp → `buoc[]` + mô phỏng + phân tích đề → kiểm chéo | `soan-bai-tap-mau`: **Bước 0 — quét dạng** + **Quy trình — ĐƯỜNG CHÍNH** + **Dạng file**; mục "5 quy tắc mới" và "Mô phỏng dưới đề" khi viết |
| 4 | Rà + cập nhật | Học sinh ảo → góp ý → Claude tự chốt, sửa tối thiểu → build | `cap-nhat-bai-hoc-theo-gemini`: **Đường chính** (bước 1–5) + **Ranh giới**. Bài MỚI soạn xong chặng 1 thì bỏ qua chặng này |
| 5 | Đăng (Mac) | Lý thuyết rồi bài tập mẫu rồi deploy | Lệnh ở bước 7 của skill chặng 1 và mục **Đăng (Mac)** của `soan-bai-tap-mau` |

Thứ tự chuẩn bài mới: 1 → 2 → 3 → (kiểm) → 5. Bài cũ nâng cấp: 4 → rồi quay lại 1/2/3 đúng chỗ góp ý chỉ ra → 5.

## Quy tắc chung (một chỗ, các chặng không lặp lại)
- Giọng văn: không dùng vai "thầy"; ít chữ, từ khoá 3–6 chữ; chú thích nhiều ý thì **mỗi ý một dòng**; đường sức nét đứt, đầu mũi tên hai vạch chéo 30°.
- Nhãn câu hỏi như đề thật: A. B. C. D. / a) b) c) d) / ô đáp số (QUY-TAC-THIET-KE E1–E3); hộp "Đề bài" dùng font đề thi (E4).
- Hạn mức độ dài/nhịp: `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md` (`lint_do_dai.py`). Xem ảnh 375px bằng mắt trước khi báo xong.
- Công thức có `<`/`>` trong `$…$` viết `\lt`/`\gt`.
- Ranh giới ghi DB: đăng lý thuyết chỉ ghi mục `ly_thuyet` (`cap-nhat-ly-thuyet.sh`); bài tập mẫu qua `publish-bai-tap-mau.mts --giu-cu`. Không dùng `upload-lesson.mts` cho việc này.
- Nhiều bài một đợt: mỗi bài một subagent, prompt tự đủ (đường dẫn, chặng cần làm, lệnh build/lint), báo cáo ≤ 25 dòng. Chọn model theo mục "Chọn mô hình" của skill chặng 1.
- Không đốt credit API: làm trực tiếp trong phiên; Batch chỉ khi thầy bảo ("chạy batch").

## Bàn giao giữa chặng
Cuối mỗi chặng ghi 1–3 dòng vào `content/lesson-samples/<bài>/TIEN-DO.md` (chặng nào xong, file nào, việc treo). Chặng sau đọc file này thay vì dò lại. Cuối cùng báo thầy một lần: bài gì, chặng nào xong, lệnh Mac cần chạy.

## Điểm dừng cho thầy duyệt (nghiên cứu: CLT/Mayer — tránh dồn quá nhiều vào một lượt xem)
Bài mới: dừng xin xem sau chặng 1 (ảnh xem thử) rồi mới làm 2–3. Bài cũ nâng cấp theo đường chính của chặng 4 thì tự chốt như skill đó quy định, không dừng.

## Nhật ký rút kinh nghiệm (bắt buộc cập nhật cuối MỖI phiên dùng skill này — xem `AGENTS.md`)
Dạng: `- YYYY-MM-DD · <sự cố/phát hiện> → <quy tắc>`. Bài học riêng của một chặng ghi vào nhật ký của skill chặng đó; ở đây chỉ ghi chuyện về **phối hợp giữa các chặng**.
- 2026-10-11 · tạo skill điều phối; chưa chạy thật → phiên đầu tiên dùng phải ghi lại chặng nào bị đọc thừa hoặc thiếu chỉ dẫn.
