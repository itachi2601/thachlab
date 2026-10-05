---
name: project_thachlab_l11_chuong4_ly_thuyet
description: Đợt 5/10/2026 soạn 5 bài lý thuyết tương tác Chương 4 Vật lí 11 (id 41–45) bằng agent song song — Fable soạn nội dung, Sonnet viết code SVG/bundle, Sonnet kiểm chéo; hết hạn mức giữa chừng, trạng thái từng bài + việc còn lại
metadata:
  type: project
---

## Phân công (thầy chốt 5/10/2026)
Fable = nội dung (theory.src.html, figs-spec.md, exam.json, tn-*.json, sửa theo kiểm chéo). Sonnet = code (build_figs.py, build_bundle.py, build_preview + chup_anh, sửa SVG) và kiểm chéo. Phiên chính chỉ điều phối + sửa số lẻ.

## Thư mục bài (commit 3fbfaa8d5 trên main local, CHƯA push; ĐÃ GHI DB + deploy 5/10/2026 — item 204/207/210/213/216; sao lưu scripts/logs/ly-thuyet-bai4N-backup-*.json)
| id | Bài | Thư mục | Trạng thái cuối (5/10) |
|---|---|---|---|
| 41 | Bài 22 Cường độ dòng điện | content/lesson-samples/l11-cuong-do-dong-dien | Nội dung + code + kiểm vòng 1 (1 chan) + đã sửa (2.283 từ) → kiểm vòng 2 OK (5/10), 2 góp ý nhỏ đã vá tay (hàng bảng đọc đề câu d; Trả bài 1 thêm 1 C = 1 A·s) → **XONG, chờ commit** |
| 42 | Bài 23 Điện trở. Định luật Ohm | content/lesson-samples/l11-dien-tro-dinh-luat-ohm | Kiểm vòng 2 OK (1 góp ý dấu chấm lẻ đã vá tay) → **XONG, chờ commit**; α đồng giữ 3,9·10⁻³ (thầy chưa chốt) |
| 43 | Bài 24 Nguồn điện | content/lesson-samples/l11-nguon-dien | Kiểm vòng 2 OK (thí nghiệm tụ+LED đã thay bằng siêu tụ 1 F + R 100 Ω; 3 góp ý nhỏ đã vá tay) → **XONG, chờ commit** |
| 44 | Bài 25 Năng lượng–công suất | content/lesson-samples/l11-nang-luong-cong-suat-dien | Kiểm vòng 2 OK (1 góp ý 'điểm phần trăm' đã vá tay 5/10) → **XONG, chờ commit** |
| 45 | Bài 26 Thực hành đo ℰ, r | content/lesson-samples/l11-thuc-hanh-do-sdd-pin | Kiểm vòng 2 OK (3 góp ý nhỏ đã vá tay: Trả bài 5, 9 %, dfrac) → **XONG, chờ commit** |

Thí nghiệm mới: tn-l11-cuong-do-dong-dien-01..03, tn-l11-dien-tro-ohm-01..03, tn-l11-nguon-dien-01..03, tn-l11-nang-luong-dien-01..03, tn-l11-do-sdd-pin-01..03 (content/thi-nghiem/).

## Còn chờ
1. ĐÃ đăng + deploy 5/10 (build out/data/lessons/41–45.json có tl-quiz; web thật đã kiểm OK 5/5 lúc 12:57 5/10). Commit main chưa push lên origin.
2. Thầy chốt α đồng (bài 23: 3,9 hay 4,3·10⁻³ K⁻¹ → ⭐⭐⭐ 71 hay 66,5 °C).
3. Rút kinh nghiệm đợt này đã ghi vào Nhật ký cuối SKILL.md (10 dòng 2026-10-05).
4. Trong `content/thi-nghiem/` còn nhiều `tn-l11-*dddh*`, `tn-l11-tatdan-*`, `tn-l12-*` của phiên khác chưa commit — không phải của đợt này, để nguyên.
