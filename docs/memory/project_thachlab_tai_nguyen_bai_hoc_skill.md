---
name: project-thachlab-tai-nguyen-bai-hoc-skill
description: Skill tai-nguyen-bai-hoc (kế hoạch hình/PhET/video cho bài học) đã chép vào repo 7/10/2026; bản gốc ở Library plugin
metadata:
  type: project
---

Skill `tai-nguyen-bai-hoc` lập kế hoạch tài nguyên trực quan cho bài từ file .tex: bảng chọn công cụ (PhET iframe ưu tiên, widget HTML, TikZ/SVG cho hình có số liệu, ảnh Gemini chỉ cho hình đời sống, video YouTube kèm mốc thời gian), xuất `prompts.md` cho Gemini, kiểm ảnh, chèn rồi chuyển sang `dang-bai-hoc-thachlab`.

Nguồn gốc: Library plugin (`~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/.../skills/tai-nguyen-bai-hoc/`), chỉ có `SKILL.md`. Ghi nhận 7/10/2026: chép nguyên bản vào `.claude/skills/tai-nguyen-bai-hoc/` (repo là nguồn chính).

**Why:** trước đó skill chỉ nằm ngoài repo, phiên cloud và Codex không thấy.
**How to apply:** sửa skill thì sửa bản trong repo rồi chạy `scripts/cai-skill.sh`; bản Library có thể lệch, diff trước ([[feedback_skill_two_copies]]). Đăng bài theo [[project_thachlab_dang_bai_hoc_skill]]. Với bài lý thuyết tương tác thì dùng [[project_thachlab_bai_ly_thuyet_tuong_tac]] (hình SVG tự vẽ), skill này chủ yếu cho bài .tex kiểu cũ.

**18/10/2026 · Đợt 1 L12 ch1–2 (id 2–9):** 8 sim PhET nhúng vào 6 bài (2, 4, 6×2, 7, 8, 9) đã ghi DB + deploy; kế hoạch `content/tai-nguyen/vl12-ch1-2/kehoach.md`. Bài 3 và 5 bỏ PhET (sim không minh hoạ được). Video: `prompts-video.md` chờ thầy dán Gemini (WebSearch không có YouTube). Bẫy deploy: lỗi font "exactly one entry" = cache `.next` hỏng → `rm -rf .next`; typecheck `scripts/*.mts` đã loại khỏi tsconfig; sau deploy HS cũ vẫn thấy bài cũ vì service worker cache (`thachlab-runtime-v4`) tới khi tải lại lần 2. Đợt sau: L12 ch3–4 (id 10–19) rồi L11/L10 theo `docs/memory` + kehoach.

**18/10/2026 · Đợt 2 L12 ch3–4 (id 10–19):** 6 sim PhET nhúng vào 5 bài (10, 13, 14, 15×2, 18), đã ghi DB + deploy; kế hoạch + TIEN-DO ở `content/tai-nguyen/vl12-ch3-4/` (generator chưa vận hành được vòi nước, thầy bấm thử). Video: `prompts-video.md` chờ Gemini. Đợt sau: L12 còn id 125–127; rồi L11 (id 20–45, một phần đã có PhET ch2), L10 (46–79), KHTN 9 (83–91, 129–131), HSG.

**18/10/2026 · Đợt 3 (L11 ch1,3,4, 12 bài id 20,21,24,25,35,36,39,40,41,42,43,45):** 12 khối PhET (8 sim) đã ghi DB + deploy + kiểm live; kế hoạch/TIEN-DO/prompts-video ở `content/tai-nguyen/vl12-125-127-vl11-ch134/`. Không PhET: L12 id 125–127, L11 id 22, 23, 26, 37, 38, 44. Đợt sau còn: L10 (id 46–79), KHTN 9 (83–91, 129–131), HSG; video cả 3 đợt chờ thầy dán Gemini. Mẹo: ghi 12 bài bằng `cap-nhat-ly-thuyet.sh` mất ~25 phút (mỗi bài ~2 phút do dry-run + ghi); đợt sau gộp một script dry-run rồi apply như `scratchpad/dry3.sh`, và gộp deploy một lần cuối.

**18/10/2026 · Đợt 4 (L10, 10 bài id 48,57,64,67,70,71,73,74,78,79×2):** 11 khối PhET (8 sim) đã ghi DB + deploy + kiểm live; `content/tai-nguyen/vl10-id46-79/`. L10 không PhET: id 46, 47, 49–56, 61, 62, 65, 68, 69, 72, 75–77 (không sim HTML5: moving-man, ladybug 404). Còn lại: KHTN 9 (83–91, 129–131), HSG (153–166). Video 4 đợt chờ thầy dán Gemini: `content/tai-nguyen/*/prompts-video.md`. Ghi DB chỉ cần `cap-nhat-ly-thuyet.sh --yes` (đã tự dry-run + đối chiếu), khỏi chạy dry-run riêng: 10 bài ~12 phút.

**18/10/2026 · Đợt 5 (KHTN 9 Ánh sáng, 6 bài id 83–88):** 6 khối PhET (bending-light ×3, geometric-optics ×3) đã ghi DB + deploy + kiểm live; `content/tai-nguyen/khtn9-id83-88/`. Id 89–91 đã có PhET, 129–131 là bản nháp có PhET trong `content/lesson-samples` nhưng DB vẫn bản ngắn (chờ thầy duyệt đăng). Gặp `TypeError: fetch failed` giữa vòng ghi (bài 86) → vòng lặp dừng ở bài lỗi, chạy lại đúng các bài còn lại (script tự đối chiếu nên chạy lại an toàn). Còn chưa làm: HSG (id 153–166), AVCN. Video 5 đợt chờ thầy dán Gemini (`content/tai-nguyen/*/prompts-video.md`); các mục CHƯA thử ở `TIEN-DO.md` từng thư mục.

**18/10/2026 · Đợt 6 (HSG KHTN 9, 10 chuyên đề id 150,151,152,153,154,155,156,158,163,166, 13 khối PhET):** đã ghi DB + deploy + kiểm live; `content/tai-nguyen/hsg9-id150-166/`. Bản nguồn `content/hsg9/` giống DB 10/10. Không PhET: id 160–162, 164; CĐ17 chưa đăng; id 157/159/165 đã có sẵn. **Tổng 6 đợt:** 59 bài, 62 khối PhET; còn lại chưa làm: AVCN, tin/blog. Việc thầy còn: bấm thử mọi mục CHƯA thử trong 6 `TIEN-DO.md`, dán 6 file `prompts-video.md` vào Gemini rồi gửi kết quả (Claude kiểm link + chèn bằng `chen-video-thi-nghiem.mts`).
