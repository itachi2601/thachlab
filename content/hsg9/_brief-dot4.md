# Brief chung đợt 4 khoá HSG Vật lí 9 (CĐ06, 07, 14, 17, 08, 09) — mọi agent đọc file này trước

Quy trình gốc: `.claude/skills/soan-bai-hsg9/SKILL.md`. Mẫu đã chạy tốt, BẮT CHƯỚC cấu trúc file: CĐ12 bài 153
(`content/hsg9/cd12-nhiet-hoc/{nguon.md,theory.src.html,build_figs.py,luyen-tap/sinh.py}`,
`scripts/data/bai-tap-mau/{btm153_d123.py,btm153_d456.py,btm153_tl.py,build-hinh-153.py,153.json}`).

| CĐ | lesson_id | Thư mục | Nguồn |
|---|---|---|---|
| 14 Gương phẳng, bóng tối và nửa tối | 158 | `content/hsg9/cd14-guong-phang-bong-toi/` | `nguon.txt` (docx 14, CHỈ phần gương phẳng + bóng; phần Trái Đất–bầu trời thuộc CĐ17) |
| 06 Khúc xạ, phản xạ toàn phần, lăng kính, tán sắc | 151 | `content/hsg9/cd06-khuc-xa-phan-xa-toan-phan/` | `nguon.txt` (docx 06) |
| 17 Thiên văn: Mặt Trăng, Hệ Mặt Trời, Ngân Hà | 178 | `content/hsg9/cd17-thien-van/` | không docx; dùng phần Trái Đất–bầu trời của `../cd14-guong-phang-bong-toi/nguon.txt` + tự viết theo đề cương THI HSG 9 KHTN 26-27 |
| 07 Thấu kính mỏng, kính lúp | 156 | `content/hsg9/cd07-thau-kinh-kinh-lup/` | `nguon.txt` (docx 07) |
| 08 Cảm ứng điện từ, dòng xoay chiều | 152 | `content/hsg9/cd08-cam-ung-dien-tu/` | `nguon.txt` (docx 08) |
| 09 Năng lượng với cuộc sống | 163 | `content/hsg9/cd09-nang-luong-cuoc-song/` | `nguon.txt` (docx 09) |

Tuần dùng bài (`scripts/data/btvn-hsg9/tuan.json`): buổi 13 (gửi 26/12) CĐ14, CĐ06, CĐ17 phần nhật/nguyệt thực + pha Mặt Trăng;
buổi 14–15 CĐ07 (dựng ảnh trên giấy ô ly; công thức thấu kính + quy ước dấu; dịch chuyển vật/ảnh; hệ hai thấu kính; đo tiêu cự);
buổi 16 CĐ08 (máy biến áp, hao phí truyền tải), CĐ09 (quiz), CĐ17 phần còn lại. Nội dung phải khớp các việc đó.

## Quy ước (giữ thống nhất lý thuyết ↔ bài tập mẫu ↔ luyện tập)
- g = 10 m/s² nếu cần, ghi ở mục tiêu; kết quả làm tròn hợp lý; sai số 1 chữ số có nghĩa.
- Chỉ Vật lí (không soạn Hoá–Sinh của phần chung). KHTN 9 CT 2018 + mở rộng HSG/chuyên (Lê Hồng Phong, Trần Đại Nghĩa).
- Quang: góc tới/khúc xạ đo so với PHÁP TUYẾN; thấu kính dùng công thức $\frac1f=\frac1d+\frac1{d'}$ với quy ước dấu ghi rõ ở lý thuyết
  (ảnh ảo $d'<0$, TK phân kì $f<0$) — cách chứng minh bằng tam giác đồng dạng là trọng tâm (HSG 9 yêu cầu).
- Bản quyền: KHÔNG chép nguyên văn docx/SGK; viết lại bằng lời mình; ví dụ D/E/G của docx KHÔNG chép — số liệu tự đặt mới.
  Sửa sai sót của docx nếu phát hiện (ghi chú lại trong nguon.md mục "Sai sót docx").
- Mọi số liệu tính bằng Python (đưa đoạn tính vào nguon.md hoặc `tinh.py` cạnh nó), không tính nhẩm.
- Ký hiệu dùng chung ghi sẵn trong nguon.md (agent lý thuyết và bài tập mẫu dùng y như vậy).

## Kỹ thuật (bài học đợt trước)
- Chữ trong SVG ≥ 14 đơn vị (chỉ số dưới 12). Đường sức từ nét đứt, đầu mũi tên chevron 30° (helper ở
  `.claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py`). Tia sáng: nét liền có mũi tên giữa tia; đường kéo dài (ảnh ảo) nét đứt.
- Trong $…$: số thập phân viết `a{,}b`; chữ có dấu bọc `\text{}`; `<`/`>` viết `\lt`/`\gt`. Quét JSON không có ký tự điều khiển `\t`.
- Hình/mô phỏng không lộ đáp số (figcaption, khung cuối mô phỏng, hình vẽ sẵn kết quả).
- Nhãn câu hỏi như đề thật: Phần I A. B. C. D.; Phần II a) b) c) d) Đúng/Sai; Phần III đáp số.
- Chú thích/đáp án nhiều ý: mỗi ý một dòng. Bài lý thuyết không dùng vai "thầy". Mobile 375px.
- Mỗi agent dùng thư mục scratch RIÊNG `/private/tmp/claude-501/-Users-MAC-Projects-thachlab/920a2363-b671-4361-a3d6-4e0892d724cc/scratchpad/<id>-<module>/`.
- Chỉ ghi file được giao. KHÔNG ghi DB, KHÔNG commit, KHÔNG deploy.
