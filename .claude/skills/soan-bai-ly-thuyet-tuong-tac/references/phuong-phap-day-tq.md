# Phong cách soạn bài chốt (rút từ bài Mô tả sóng, thầy duyệt 2/10/2026)

Đây là **checklist bắt buộc** cho mọi bài lý thuyết tương tác về sau. Tên tiếng Trung chỉ để nhớ nguồn gốc
phương pháp — **không** đưa chữ Hán vào bài cho học sinh đọc.

## Bảng 14 nét, và chỗ áp dụng trong bài

| Phương pháp | Việc phải làm trong bài | Nằm ở phần |
|---|---|---|
| **情境导入** — dẫn nhập bằng tình huống | Mở bằng một cảnh học sinh đã nhìn thấy (sân vận động, sân băng, bếp, xe đạp, xưởng CNC). Cấm mở bằng định nghĩa. Phải có một câu hỏi để nghĩ. | I. Mở bài |
| **目标导学** — mục tiêu trước khi học | Khung "🎯 Mục tiêu bài học hôm nay": 2–4 gạch đầu dòng + câu "cuối bài phải tự trả lời được N câu ở mục Trả bài". | Đầu bài, trước I. |
| **先猜后学** — đoán trước rồi mới học | Hộp dự đoán 3–4 phương án, phản hồi giải thích **vì sao**; chọn câu đoán đánh trúng hiểu lầm gốc của bài. | Ngay sau cảnh mở bài |
| **关键词记忆** — nhớ bằng từ khoá | Mỗi ý kiến thức một dòng **🔑 3–6 từ**; mẹo/口诀 riêng cho từng công thức khó nhớ. | II (mọi ý) |
| **实验探究 (做—看—得)** — thí nghiệm | Mỗi kiến thức chính có ví dụ hoặc thí nghiệm, viết 3 bước **Làm – Quan sát – Rút ra**, dụng cụ làm được ở lớp. Ghi vào `content/thi-nghiem/` + `data-exp`. | II (mỗi ý) |
| **数据分析** — xử lý số liệu thật | Ít nhất **một thí nghiệm đo** có bảng số liệu thật (3–5 lần đo) + câu hỏi "từ bảng này rút ra gì, sai số đến từ đâu". Học sinh ở nhà không làm lại thí nghiệm được, nên giá trị nằm ở việc **đọc bảng và nhận xét sai số** bằng giấy bút, không ở việc tự tay đo. Không chỉ thí nghiệm định tính. | II |
| **当堂检测 / 即时反馈** — kiểm tra ngay | 6–8 quiz rải khắp bài: sau dự đoán, sau mỗi khối kiến thức, sau mỗi cái bẫy, sau bài toán mẫu. | Rải cả bài |
| **错因分析** — phân tích nguyên nhân sai | Phản hồi sai phải **gọi tên lỗi** ("em nào ra 6,25 là đã chia nhầm") và chỉ cách nghĩ lại; không chỉ báo "sai". | Trong mọi `.tl-fb--no` |
| **易错点辨析** — bắt chỗ hay sai | 2–3 "cái bẫy" của riêng bài; mỗi bẫy có bảng đối chiếu hai khái niệm dễ lẫn + 1 quiz. | III. Cái bẫy |
| **对比表** — bảng đối chiếu | Cặp dễ lẫn nào cũng nên có bảng "cột này vs cột kia"; tối đa 3 cột ở 375px. | II, III |
| **审题训练** — luyện đọc đề | Bài toán mẫu: hộp **Đề bài** → bảng *Câu trong đề / Dữ liệu / Kiến thức liên quan* (mỗi cụm từ một hàng, kể cả dữ kiện ngầm) → lời giải từng bước → **bước kiểm tra kết quả**. | V |
| **变式训练** — luyện biến thể | Ngay sau bài toán mẫu: đổi số, **đổi chiều truyền**, đổi vị trí điểm trên dạng sóng/đồ thị. | V, sau lời giải |
| **分层练习** — bài tập phân tầng | Thử thách ⭐ (cơ bản) / ⭐⭐ (khá) / ⭐⭐⭐ (thách đấu, phải lập luận). | VI |
| **归纳小结 / 板书** — tổng kết có cấu trúc | Khung "✅ Mang về sau bài học": **chuỗi từ khoá**, mỗi dòng một ý, trong đó có một dòng về cách đọc đề. | Cuối bài |
| **拓展** — mở rộng cho học sinh khá | Công thức/hiện tượng mở rộng để trong `<details>`; **không** giấu kiến thức bắt buộc trong `<details>`. | II, III, VI |

## Nhịp 6 phần (mỗi phần một `<h3>`)

```
🎯 Mục tiêu bài học hôm nay        (hộp tl-box, không phải <h3>)
I.   Mở bài: <cảnh thật> + hộp dự đoán + hình 1
II.  Kiến thức: mỗi ý = 🔑 + bullet + ví dụ/thí nghiệm + quiz; có hình minh hoạ
III. Ba cái bẫy sập nhiều nhất     (bảng đối chiếu + quiz mỗi bẫy)
IV.  Trả bài: 5–6 câu nhớ lại, mỗi câu một <details>
V.   Bài toán mẫu: Đề bài → bảng dữ liệu → lời giải → Thử sức (biến thể)
VI.  Đời sống + Thử thách phân tầng ⭐ + "✅ Mang về sau bài học"
```

## Giọng văn — 5 điều nhớ kỹ

1. **Không có vai "thầy" trong bài.** Không "thầy cho cả lớp…", "Thầy hỏi: …", "thầy tự hỏi: …".
2. Người học là "em"; câu ngắn; vào thẳng ý.
3. Được trích lời học sinh ("Thầy ơi, em…") — đó là thoại của học sinh, không phải người dẫn chuyện.
4. Đoạn văn xuôi tối đa 2–3 câu; dài hơn thì tách từ khoá + bullet hoặc đẩy vào `<details>`.
5. Ví dụ ưu tiên ba mảng của thầy: vật lí THPT, CNC/chế tạo máy, trượt băng.

## Ba nét bổ sung từ nghiên cứu tự học (thêm 2/10/2026, bắt buộc như 14 nét trên)

| Nét | Việc phải làm | Vì sao (nghiên cứu) | Nằm ở phần |
|---|---|---|---|
| **Tự giải thích trước khi xem** | Ở mục Trả bài, mỗi `<summary>` kết bằng dòng nhỏ "Nói bằng lời của em vì sao, rồi mới bấm xem." Trong `.tl-fb--ok` của quiz khó: thêm một câu "Em giải thích được cho bạn ngồi cạnh chưa?" | Self-explanation (Chi): học sinh tự nói lý do nhớ lâu và chuyển giao tốt hơn chỉ đọc đáp án. | IV, quiz khó |
| **Rút dần giàn giáo** | Giữa bài toán mẫu giải trọn và biến thể, có **một bài giải để trống 1–2 bước** (bước dễ nhầm nhất) cho học sinh điền, đáp án bước trống trong `<details>`. Thứ tự: giải trọn → điền bước trống → tự giải biến thể. | Worked example → completion problem → independent (Sweller, Renkl); đọc mãi lời giải đầy đủ làm học sinh khá bị "đảo ngược chuyên môn". | V |
| **Hiệu chuẩn tự tin** | Với 2–3 quiz quan trọng (bẫy, bài toán mẫu): trước phương án A–D có dòng radio "Em chắc bao nhiêu? ○ Chắc ○ Không chắc". Phản hồi sai nhắc: "Nếu em đã chọn *Chắc* mà sai, đây là chỗ cần xem lại nhất." | Siêu nhận thức: học sinh THPT thường tự tin quá mức ở đúng chỗ hiểu sai; tự chấm độ chắc giúp biết mình chưa biết gì (Dunlosky, Bjork). Chỉ cần radio, không JS. | III, V |

Hai thứ **không** thêm: quá 8 quiz một bài (quá tải, bài đã ~50 KB) và chữ Hán/tên phương pháp trong bài cho học sinh đọc.

## Tỉ lệ vàng đã kiểm chứng (bài Mô tả sóng)

- ~51 KB HTML trong đó ~25 KB là SVG; 4 hình SVG; 7 quiz; 13 `<details>`; 6 phần.
- 2 thí nghiệm có số liệu; 1 bài toán mẫu 4 câu; 2 biến thể; 3 mức thử thách.
- Thời gian soạn trọn gói (soạn + hình + thí nghiệm + xem thử) trong một lượt là hợp lý; đừng phình thêm phần chữ.
