---
name: project_thachlab_cap_nhat_bai_theo_gemini
description: "Quy trình cập nhật bài học bằng Gemini (học sinh ảo + nháp bài tập mẫu) — skill cap-nhat-bai-hoc-theo-gemini; vòng thật đầu Bài 9 L12 ngày 2026-10-08; việc treo (duyệt lý thuyết, dán lại tin nhắn 3, gói sửa nhỏ chờ thầy)"
metadata:
  node_type: memory
  type: project
  originSessionId: 93631dbb-5985-466a-824c-20fa557b1fe8
  modified: 2026-10-08T03:58:38.049Z
---

**Mục tiêu:** thầy dán tay vào gemini.google.com (không API) để Gemini (1) đóng vai học sinh đọc bài lý thuyết, (2) nháp 4 dạng bài tập mẫu; Claude kiểm, sửa tối thiểu, đăng. Skill duy nhất ở repo `.claude/skills/cap-nhat-bai-hoc-theo-gemini/` (không chép lên tài khoản claude.ai — thầy hỏi 2026-10-08 vì không thấy trong Settings; đó là skill cấp dự án, đúng thiết kế). Điều phối: `content/gemini/hang-doi.md`; mỗi bài có `content/lesson-samples/<bài>/gemini/{gui,nhan,da-xu-ly}/`.

**Đã xong tới 2026-10-08** (commit `33811cf79`, `87bc826c5`, `bb1d3e7a1`, đều trên `origin/main`):
- `scripts/gemini-phan-hoi.mts --xuat` cần `--lesson-id`: nhúng danh mục YCCĐ vào tin nhắn 3, chỉ xuất tin nhắn 3 cho vai trung-binh, tự sinh `nhan/dap-an-that.json` từ lớp `tl-ok`.
- `kiem-ban-nhap-gemini.py`: 0/4 YCCĐ khớp = lỗi (lạc phạm vi). `gop-phan-hoi.py`: chịu fence json, tách nguồn `vai@claude`, cảnh báo quiz sai không có góp ý.
- Bước 1b "lượt Claude" (subagent Sonnet dò cấu trúc theo `references/PROMPT-CLAUDE-HOC-SINH.md`), do phiên khác thêm, tôi commit.
- **Bài 9 L12 Khái niệm từ trường (lesson_id 10):** 3 góp ý Gemini đã sửa trong `theory.src.html`, build lại `theory.html` + `bundle.json`, chụp 375px sạch. Nháp bài tập mẫu vòng 1 LOẠI (4 dạng đều góc từ khuynh), giữ ở `da-xu-ly/bai-tap-mau.loai-vong1.json`. Lượt Claude trả 17 góp ý: 9 đáng nhận, 5 từ chối, 2 hỏi thầy — toàn bộ phán quyết trong `da-xu-ly/so-quyet-dinh.json`.

**Còn chờ (thầy quyết, 2026-10-08):**
1. Duyệt lý thuyết Bài 9 → đăng bằng `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l12-khai-niem-tu-truong/theory.html 10` (chạy tab terminal, rồi deploy).
2. Gói sửa nhỏ đề xuất ở `so-quyet-dinh.json` (`quiz_sai_khong_gop_y`, `luot_claude_vong1.moi_dang_nhan`): 2 dòng nhấn cho câu 1/câu 6, B₃→B₁ trong bảng phân tích, gộp "từ trường đều" lặp ở mục 3, câu quy trình cộng theo trục; câu c bài toán mẫu trùng 53° với câu a — đổi số hay giữ. Bài đang 2499/2500 từ, sửa thì phải cắt đoạn sai số bù.
3. Thầy dán lại `gemini/gui/trung-binh-3-bai-tap-mau.txt` (đã có danh mục YCCĐ) vào cuộc chat Gemini cũ → lưu `nhan/bai-tap-mau.json` → kiểm máy → viết lại theo `soan-bai-tap-mau`.
4. 7 bài còn lại trong `hang-doi.md` (Bài 10–16 L12) đang `da-gui`, chưa có file `nhan/`. Khi xuất lại phải thêm `--lesson-id`.

**Quyết định đã chốt, đọc code không suy ra:**
- Tỉ lệ quiz của Gemini KHÔNG là tiêu chí dừng (nó giỏi hơn HS thật); câu nó sai = bẫy cần nhấn. Dừng khi hết `chặn`, tóm tắt khớp mục tiêu, lí do chọn không viện kiến thức ngoài bài.
- Chấp nhận góp ý ≠ chấp nhận câu chữ Gemini đề xuất (g2 bài 9: "chỉ đúng riêng thí nghiệm" sai vật lí; 1/d³ là quy luật nam châm ở xa).
- Giới hạn còn lại: `gop-phan-hoi.py` gộp theo chuỗi `vi_tri`+`loai` nên Gemini và Claude cùng chỗ vẫn báo 0 trùng → nên gộp theo trích dẫn tìm trong `theory.src.html`. Gemini mù hình (SVG bị thay bằng placeholder) → cân nhắc gửi kèm `xem-thu/fig-*.webp`.
- Vòng 2 trở đi chỉ vai trung-binh, chỉ gửi mục đã sửa (giảm công dán của thầy).

Liên quan: [[project_thachlab_bai_ly_thuyet_tuong_tac]], [[project_thachlab_cap_nhat_ly_thuyet]], [[feedback_skill_two_copies]].

**Cập nhật 8/10/2026 (chiều) — thầy chốt bỏ Gemini, Claude tự chốt và đăng, trợ giảng rà sau:**
- Bài 10 (L12 Bài 9): lý thuyết đã ĐĂNG (26 góp ý Opus+Sonnet, 2.487 từ, câu c bài toán mẫu đổi thành 30 µT → 42 µT/45°, Câu 2 đổi phương án A); bài tập mẫu 4 dạng đã ĐĂNG (publish-bai-tap-mau, sao lưu scripts/logs/bai-tap-mau-bai10-*.json). Chờ trợ giảng rà trên web.
- Batch đang chạy cho L12: rà lý thuyết 20 bài (msgbatch_01PW6g79SnwaejgoRgix7EHq), nháp BTM 18 bài (msgbatch_01Mt2jX1SPqWh8Rf8nETtHEz). Nhận bằng `--nhan <id> --cho`.
- Chế độ mới `--che-do sua-ly-thuyet`: API trả cả theory.src.html đã sửa + sổ quyết định; `--nhan` tự sao lưu, ghi nguồn, build_figs/build_bundle, lint, cập nhật so-quyet-dinh.json + hang-doi.md; ≈ $0.32/bài (31k vào). Đã thử --du-toan bài 10, CHƯA chạy thật — bước tiếp: khi 20 bài có nhan/hoc-sinh-trung-binh-claude.json → `--che-do sua-ly-thuyet --gui --lop 12` → nhận → đăng từng bài `da-sua` bằng cap-nhat-ly-thuyet.sh --yes.
- Chưa làm: chế độ `viet-bai-tap-mau` (API viết lại nháp đủ phong cách + hình SVG + request kiểm chéo riêng), đầu ra scripts/data/bai-tap-mau/<id>.json; hình mô phỏng vẫn cần Claude Code xem/sửa.
