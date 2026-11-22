# Triển khai bản chiếu trên lớp cho mọi bài — 4 phiên song song (20/11/2026)

Mở trong app desktop: phiên mới, **model Opus 5.5** (thiết kế màn chiếu + soạn câu hỏi là việc phiên chính; lớp ảo tự dùng subagent Sonnet),
**worktree cắt từ nhánh `claude/tren-lop-l11-dien-the-96ea37`** (skill + bài mẫu chưa vào main). Dán nguyên một khối dưới đây cho mỗi phiên.

| Phiên | Phạm vi | Số bài |
|---|---|---|
| tren-lop-l10a | `scripts/ruot-tap/l10-bai1.mjs` … `l10-bai17.mjs` | 17 |
| tren-lop-l10b | `l10-bai18.mjs` … `l10-bai34.mjs` | 17 |
| tren-lop-l11 | `l11-bai1.mjs` … `l11-bai26.mjs`, trừ bài 20 (đã xong, là mẫu) | 25 |
| tren-lop-l12 | `l12-bai1.mjs` … `l12-bai8.mjs` + `bai14.mjs` … `bai18.mjs` (tên cũ, đều là L12) | 13 |

## Khối giao việc (thay `<PHẠM VI>`)

```
Dựng "đường trên lớp" cho các bài có ruột tập <PHẠM VI>, theo đúng skill .claude/skills/ban-chieu-tren-lop/SKILL.md
(đọc trước, đủ 8 bước, kể cả lớp ảo và bước 8 lên web). Mẫu chuẩn: content/lesson-samples/l11-dien-the/.
- Mỗi bài: tìm thư mục content/lesson-samples/<slug>/ khớp bài (đầu file .mjs ghi lesson id và nguồn); chưa có theory.html → bỏ qua, ghi treo.
- Làm tuần tự, commit riêng từng bài theo đường dẫn ngay khi xong; context > 150k thì /compact giữa hai bài.
  Lớp ảo dùng subagent Sonnet như skill nói; phiên chính chỉ nhắn "lượt N".
- Không đăng DB, không deploy, không push, không sửa đề kiểm tra, không sửa theory/bundle; ruột tập sửa được nhưng PDF giữ số trang.
- Truy vấn DB (tìm đề Kiểm tra lý thuyết) chạy trong tab terminal (sandbox chặn supabase).
- Bài học mới → thêm dòng vào "Nhật ký rút kinh nghiệm" cuối SKILL.md.
Xong: một bảng, mỗi bài một dòng theo mẫu "Báo cáo mỗi bài" của skill, kèm nhánh và việc treo.
```

Thứ tự nên làm trong mỗi phiên: bài sắp dạy trước (theo lịch tuần), rồi theo số bài.
