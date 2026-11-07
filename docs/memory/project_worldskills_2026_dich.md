---
name: project_worldskills_2026_dich
description: "Bộ dịch song ngữ WorldSkills 2026 Skill 01 Industrial Mechanics: đã xong 3 bậc 1/11, học phần CTTC worldskills-im đã deploy 2/11 (16 bài, chỉ xem khi đăng nhập); chờ thầy xem thử + soát bậc 1"
metadata:
  node_type: memory
  type: project
  originSessionId: 8eecdbe4-83a3-45a6-b9f5-089fc5f8431a
  modified: 2026-11-02T01:30:00.000Z
---

Thầy được giao dịch bộ tài liệu WorldSkills Shanghai 2026, Skill 01 Industrial Mechanics, để huấn luyện SV Cao Thắng yếu cơ khí.
Thư mục: `/Users/MAC/Documents/CTTC/4 - Quản lý bộ môn/kỹ năng nghề quốc tế/2026/` (không phải git). Bản dịch ở `dich/` (README = mục lục + lộ trình 4 giai đoạn).

**Đã xong 1/11/2026** (3 phiên nhánh song song): bậc 1 đề thi + thang điểm CSV 277 dòng + 7 phiếu tự chấm A–G; bậc 2 TD mục 1, 2, 4, 5.3, 7, 9; bậc 3 tóm tắt máy phay, validation, danh mục 29 file. Thuật ngữ `00-dung-chung/thuat-ngu.md`, lỗi bản gốc #1–#19 `loi-ban-goc.md`.

**Chờ:** thầy soát bằng mắt bậc 1 (04-module-C, 06-ban-ve-chu-giai, phiếu C/D) rồi in cho SV. Chưa quyết: mượn/thuê bộ dụng cụ Module A (AT-400, WBT-400, OL2R… = 17.5 điểm) và bản quyền FluidSIM.

**Why:** trọng số điểm thật khác tỷ lệ thời gian; bản phân tích VN có sẵn (`Industrial_Mechanics_WorldSkills_2026.pdf`) lỗi thời vì dựa pre-release.
**How to apply:** mọi bản dịch/giáo án WS sau này dùng `thuat-ngu.md` và tra `loi-ban-goc.md` trước; không dùng PDF phân tích cũ làm nguồn. Liên quan: [[project_thachlab_avcn]].

**Sổ tay web 2/11/2026:** artifact https://claude.ai/artifact/MhNpd88AeV1A67tS3iesMz (riêng tư) dựng từ `dich/` bằng `dich/dung-so-tay.py` → `dich/so-tay-industrial-mechanics-2026.html` (8 tab, phiếu tự chấm lưu localStorage). Sửa md/csv xong chạy lại script rồi đăng lại cùng URL.

**Học phần trên thachlab 2/11/2026:** lớp/môn `worldskills-im` (vào tự do), 5 chương theo giai đoạn huấn luyện, 16 bài (lesson id 185–200), `published=true`. Mã: `services/classes.ts` (CTTC_CLASS_SLUGS), thẻ ở `/lop-hoc/cttc`. Nguồn trong repo `content/worldskills-im/dich/` (bản sao của Documents; sửa ở Documents thì `rsync` lại), dựng `node scripts/build-worldskills-im.mjs`, ghi DB `bash scripts/dang-worldskills-im.sh` (PATCH nếu đã có mục). Mỗi bài module = đề + phiếu tự chấm (checkbox không lưu) + thang điểm gập. Trang bài đòi đăng nhập (RLS) nên không xem được bằng khách.

**Trạng thái 2026-11-02 08h30:** code vào `main` (merge e9c5aece2, sau khi gộp tay xung đột `docs/STATE-archive.md` với phiên khác), `scripts/deploy.sh` đã push nhánh `deploy`. **Chờ:** (1) thầy đăng nhập mở `/lop-hoc/worldskills-im` xem thử, báo chỗ cần sửa; (2) muốn SV xem không cần tài khoản thì phải sửa RLS lesson_items (giống AVCN, chưa làm); (3) soát bậc 1 bằng mắt → sửa ở Documents → `rsync` sang `content/worldskills-im/dich/` → `node scripts/build-worldskills-im.mjs` → `bash scripts/dang-worldskills-im.sh` → deploy; (4) lặt vặt kiem-code để nguyên: tên file `.md` nội bộ còn hiện trong bài, tiêu đề EN dài. `supabase/.temp` trong worktree là symlink tạm, không commit.
