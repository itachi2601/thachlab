---
name: project-thachlab-tai-nguyen-bai-hoc-skill
description: Tài nguyên trực quan cho bài học: skill tai-nguyen-bai-hoc (trong repo từ 2026-10-07) và đợt nhúng PhET hàng loạt 6 đợt đã đăng 2026-10-18 (49 bài, 55 khối); việc còn chờ thầy
metadata:
  type: project
---

## Skill
`tai-nguyen-bai-hoc` (`.claude/skills/tai-nguyen-bai-hoc/SKILL.md`) lập kế hoạch hình/PhET/video cho bài; `phet` (`.claude/skills/phet/SKILL.md`) lo riêng PhET. Chép từ Library plugin ngày 2026-10-07; sửa skill thì sửa bản trong repo rồi `scripts/cai-skill.sh` ([[feedback_skill_two_copies]]). Đăng bài theo [[project_thachlab_dang_bai_hoc_skill]]; bài lý thuyết tương tác theo [[project_thachlab_bai_ly_thuyet_tuong_tac]].

## Đợt nhúng PhET hàng loạt (2026-10-18, thầy duyệt từng bảng kế hoạch)
Mỗi khối là `<details class="tl-details">` đóng mặc định, 3 bước Thử có câu dự đoán, nhúng trước một `<h3>` chọn theo bài. Ghi DB bằng `scripts/cap-nhat-ly-thuyet.sh --yes` (chỉ mục lý thuyết, đã đối chiếu trước/sau), deploy 6 lần, kiểm live 375px (iframe 311px, không tràn). Tài liệu từng đợt nằm ở `content/tai-nguyen/<thư mục>/` (`kehoach.md`, `TIEN-DO.md`, `prompts-video.md`).

| Đợt | Phạm vi | Bài (id) | Khối | Thư mục |
|---|---|---|---|---|
| 1 | L12 ch1–2 | 2, 4, 6×2, 7, 8, 9 | 7 | `vl12-ch1-2` |
| 2 | L12 ch3–4 | 10, 13, 14, 15×2, 18 | 6 | `vl12-ch3-4` |
| 3 | L11 ch1,3,4 | 20,21,24,25,35,36,39,40,41,42,43,45 | 12 | `vl12-125-127-vl11-ch134` |
| 4 | L10 | 48,57,64,67,70,71,73,74,78,79×2 | 11 | `vl10-id46-79` |
| 5 | KHTN 9 Ánh sáng | 83–88 | 6 | `khtn9-id83-88` |
| 6 | HSG KHTN 9 | 150,151×2,152,153,154×2,155×2,156,158,163,166 | 13 | `hsg9-id150-166` |

Tổng 49 bài, 55 khối. Commit cuối mỗi đợt nằm trong `git log --grep="PhET"`.

## Còn chờ (thầy làm)
1. Bấm thử mọi mục CHƯA thử ở 6 file `TIEN-DO.md` (nặng nhất: máy phát điện id 14 vòi nước không vận hành được bằng chuột giả lập; màn chưa mở: pendulum-lab Năng lượng/Ma sát, collision-lab Phần giới thiệu, energy-forms Hệ thống, projectile-motion Lực cản, chọn gương phẳng ở geometric-optics). Sửa bước Thử nào sai thì sửa `theory.src.html` + `theory.html` rồi `cap-nhat-ly-thuyet.sh`.
2. Dán 6 file `prompts-video.md` vào Gemini, gửi kết quả; Claude kiểm link rồi ghi `video` vào `content/thi-nghiem/` và chạy `scripts/chen-video-thi-nghiem.mts` (quy ước ở `content/thi-nghiem/README.md`). WebSearch không lập chỉ mục YouTube nên Claude không tự tìm được.
3. Chưa làm: AVCN (id 168–177), bài không có sim HTML5 khớp (kinematics: `moving-man` 404; chuyển động tròn: `ladybug` 404; phân hạch/`radioactive-dating-game` chỉ Java).
4. Ngoài phạm vi: id 129–131 (KHTN 9 cơ học) có bản nháp PhET trong `content/lesson-samples`, DB vẫn bản cũ chờ thầy duyệt ([[project_thachlab_l9_co_hoc_129_131]]); id 157/159/165 HSG và 58–60, 63, 66 (L10), 89–91 (KHTN 9), L11 ch2 đã có PhET từ trước.

## Quyết định và bẫy
- Chỉ viết bước Thử cho màn/nút đã nhìn thấy; chưa thấy thì ghi CHƯA thử ([[feedback_content_images_eyeball]] cùng tinh thần). `gas-properties` giữ ~300 K khi nén tường nên đừng viết "nén thì nóng"; sim "Mật độ" = khối lượng riêng (đã giải thích ở id 79).
- Chèn thẳng vào cả `theory.src.html` và `theory.html` (chỉ thêm dòng); KHÔNG chạy lại `build_figs.py` vì SVG sinh lại khác bản trong DB.
- Deploy: lỗi font "exactly one entry" = cache `.next` hỏng → `rm -rf .next`; `scripts/` đã loại khỏi typecheck (`tsconfig.json` exclude, commit 12bc84943) vì `.mts` của phiên khác làm build lỗi; sau deploy học sinh cũ còn thấy bản cũ tới khi service worker (`thachlab-runtime-v4`) làm mới (tải lại lần 2).
- Ghi DB 10–12 bài mất 12–25 phút; gặp `TypeError: fetch failed` thì vòng lặp dừng ở bài lỗi, chạy lại các bài còn lại (an toàn vì script tự đối chiếu). Sim lần đầu mở trong pane có thể treo ở logo: tải lại.

## Bổ sung 25/10/2026: L12 chương 4
Thêm `build-an-atom` (id 15, bài 14) và `beta-decay` (id 18, bài 17), đã mở thật, đã ghi DB (backup `scripts/logs/ly-thuyet-bai15-*`, `bai18-*`), chưa deploy. Video mở bài id 16, 17 (V7, V8) chờ thầy dán Gemini (`content/tai-nguyen/vl12-ch3-4/prompts-video.md`). Chưa thử: kéo electron, ô Điện tích/Số khối ở build-an-atom; nút Chậm ở beta-decay.
