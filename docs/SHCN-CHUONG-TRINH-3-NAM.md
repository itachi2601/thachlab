# Chương trình SHCN 3 năm — "Tự lập từng bước"

Lớp chủ nhiệm hệ cao đẳng (Cao Thắng, vd CĐ CK 26C) · 6 học kì · mỗi tuần 1 tiết SHCN 45'.
Soạn 8/11/2026, thay cho cách dạy 12 chủ đề GDĐĐ&PTNN theo thứ tự tài liệu. **Không bỏ chủ đề nào
của chương trình chính thức** — mọi mục con của 12 chủ đề (`lib/shcn/gddd-topics.ts`) đều có tuần dạy
(bảng đối chiếu ở mục 6); chỉ sắp lại thứ tự theo nhu cầu thật của sinh viên ở từng giai đoạn và
thêm các bài về tự chăm sóc bản thân, sức khoẻ, tiền, chỗ ở, thái độ làm việc.

Nội dung đầy đủ từng tiết (bản sinh viên + kịch bản giảng viên): `content/shcn-3-nam/` — xuất Word bằng
`python3 scripts/xuat-shcn-3-nam-docx.py <thư mục ra>`.

---

## 1. Ý tưởng xuyên suốt

Sinh viên năm 1 phần lớn 18 tuổi, lần đầu sống xa nhà. Thứ các em cần **trước** không phải "kỹ năng
phỏng vấn" mà là: ăn gì, ở với ai, tiêu tiền sao cho đủ tháng, ngủ đủ, không bị lừa, biết gọi ai khi
ốm. Kỹ năng làm việc nhóm, lập kế hoạch, giải quyết vấn đề cần khi bắt đầu làm đồ án (năm 2). Đạo đức
nghề, 5S, tìm việc cần sát lúc đi thực tập (năm 3). Vì vậy chương trình đi theo **3 chặng tự lập**:

| Năm | Chủ đề năm | HK lẻ | HK chẵn |
|---|---|---|---|
| 1 | **Tự lo cho mình** | HK1 · Đứng vững khi xa nhà | HK2 · Học có phương pháp, sống có nề nếp |
| 2 | **Làm việc cùng người khác** | HK3 · Giao tiếp và làm việc nhóm | HK4 · Tự quản trị: kế hoạch, vấn đề, tiền |
| 3 | **Bước vào nghề** | HK5 · Vào doanh nghiệp, tác phong và đạo đức nghề | HK6 · Tìm việc và sống tự lập hẳn |

Bốn **mạch** chạy suốt 6 học kì, mỗi mạch quay lại nhiều lần ở mức cao dần (học xoắn ốc):

| Mạch | Ký hiệu | Đi qua các HK |
|---|---|---|
| Tự chăm sóc & cuộc sống độc lập (ăn, ở, tiền, giấy tờ, an toàn) | **TL** | 1 → 2 → 4 → 6 |
| Sức khoẻ thể chất & tinh thần (ngủ, vận động, căng thẳng, chất gây nghiện) | **SK** | 1 → 2 → 3 → 4 → 5 → 6 |
| Kỹ năng mềm (học, giao tiếp, nhóm, kế hoạch, giải quyết vấn đề) | **KN** | 2 → 3 → 4 → 5 |
| Thái độ & tác phong làm việc (đúng giờ, trách nhiệm, trung thực, 5S, đạo đức nghề) | **TĐ** | 1 → 3 → 4 → 5 → 6 |

**Ai dẫn hoạt động** cũng chuyển dần, để chính tiết SHCN là chỗ tập tự chủ:
năm 1 GVCN dẫn · năm 2 mỗi tuần một nhóm 4–5 SV dẫn phần hoạt động 10' (GVCN dẫn phần cốt lõi) ·
năm 3 nhóm SV dẫn cả 20', GVCN chỉ chốt và bổ sung.

---

## 2. Khung một tiết 45'

Giữ đúng khung biên bản đang dùng (skill `bien-ban-shcn`), chỉ quy định rõ hơn bên trong 20':

| Phút | Phần | Ghi chú |
|---|---|---|
| 0–5 | Ổn định, điểm danh, **hỏi lại việc tuần trước** (1–2 SV tự nguyện kể, 1 phút) | Không gọi tên bắt kể; không chấm điểm cá nhân |
| 5–20 | Phổ biến lịch tuần, công việc của trường/khoa/lớp | Theo tài liệu CTCT tuần đó |
| 20–40 | **Sinh hoạt nội dung** (khung 2–5–10–3 bên dưới) | 1 tiết = 1 kỹ năng |
| 40–45 | Ý kiến lớp, kết luận, nhắc **việc tuần** | Ghi việc tuần vào nhóm Zalo/ThachLab |

Khung 20' sinh hoạt nội dung:

1. **Mở (2')** — một tình huống thật, ngắn (tin nhắn lừa đảo, hoá đơn tiền điện, ảnh tủ lạnh trống…)
   và một câu hỏi để cả lớp đoán/chọn trước khi nghe.
2. **Cốt lõi (5')** — tối đa **3 ý**, mỗi ý một câu dễ nhớ. Không đọc slide dài.
3. **Làm (10')** — cặp/nhóm 4 người xử lý tình huống, điền phiếu, đóng vai, tính toán. Đây là phần
   chính; tình huống dùng **nhân vật giả định** ("bạn Minh, năm nhất, ở trọ Thủ Đức…"), không bắt SV
   kể chuyện riêng về tiền, gia đình, tình cảm, sức khoẻ.
4. **Chốt + việc tuần (3')** — mỗi SV tự viết một câu "**Nếu** [lúc/tình huống] **thì** tôi sẽ [việc
   nhỏ]". Việc tuần làm được trong ≤15 phút/ngày.

Tuần không có nội dung (thi, lễ, hoạt động trường): 5' + phổ biến 35' + 5', ghi biên bản
`coGDDD: false` như cũ.

### Vì sao thiết kế như vậy (căn cứ ngắn)

- **Một tiết một kỹ năng, ≤3 ý** — trí nhớ làm việc chỉ giữ được vài khối thông tin cùng lúc (lý
  thuyết tải nhận thức, Sweller); 20' nhồi cả chủ đề thì về nhà không còn gì.
- **Việc tuần dạng "nếu–thì"** — cam kết hành động cụ thể theo tình huống làm tăng rõ khả năng thực
  hiện so với chỉ đặt mục tiêu (implementation intentions, Gollwitzer & Sheeran 2006). Thói quen mới
  cần trung bình khoảng 2 tháng lặp lại mới thành tự động (Lally và cs. 2010) → việc tuần nhỏ, lặp,
  quay lại ở học kì sau.
- **Hỏi lại việc tuần đầu tiết** — nhớ lại có chủ đích giúp nhớ lâu hơn đọc lại (testing effect,
  Roediger & Karpicke 2006), đồng thời cho SV thấy việc tuần là thật chứ không phải hình thức.
- **Giao dần quyền dẫn cho SV** — tự chủ, năng lực, gắn kết là ba nhu cầu nền của động lực bền (thuyết
  tự quyết, Deci & Ryan); tuổi 18–25 là giai đoạn "trưởng thành mới nổi" — muốn tự quyết nhưng chưa có
  kỹ năng (Arnett 2000), nên đưa quyền theo từng bậc chứ không thả ngay.
- **Nhân vật giả định, không ép tự kể** — tuổi này rất nhạy với đánh giá của bạn bè; buộc kể chuyện tiền
  bạc/gia đình trước lớp làm các em im lặng hoặc bịa, và có thể làm tổn thương em đang khó khăn.
- **Đặt bài theo thời điểm cần** — tháng đầu năm 1 là lúc SV dễ bị lừa, hụt tiền và nhớ nhà nhất; giai
  đoạn chuyển tiếp năm nhất quyết định phần lớn việc bỏ học (Tinto). Dạy "cảnh giác lừa đảo" ở năm 2 là muộn.

---

## 3. Bảng bài theo học kì

Mỗi HK tính **18 tuần SHCN**: 1 tuần khởi động + 14 bài + 2 tuần đệm (thi/lễ — xếp vào đúng tuần lịch
trường) + 1 tuần tổng kết. Số tuần dưới đây là thứ tự bài, không phải số tuần lịch trường.

Cột **Ghi biên bản** là tên chủ đề + trọng tâm ghi vào `tuan-XX.json`, viết **trùng tên mục con trong
`gddd-topics.ts`** để phần "Tự đọc thêm" trên ThachLab trừ đúng. Bài không có mục con chính thức tương
ứng ghi vào chủ đề gần nhất (thường là Chủ đề 2: Kỹ năng sống) với tên bài làm trọng tâm.

### HK1 — Đứng vững khi xa nhà (năm 1)

Mục tiêu học kì: cuối HK1 mỗi SV tự lo được ăn – ở – tiền – đi lại – an toàn – khi ốm trong một tháng mà
không phải gọi về nhà xin "cứu".

| # | Bài | Mạch | Hoạt động 10' | Việc tuần | Ghi biên bản |
|---|---|---|---|---|---|
| K | Khởi động: làm quen lớp, nội quy, bầu ban cán sự, giới thiệu chương trình 3 năm và **Hộ chiếu tự lập** | TĐ | Trò "tìm người": tìm bạn cùng quê, cùng trọ, cùng sở thích | Lưu số GVCN, lớp trưởng, nhóm lớp | Sinh hoạt đầu khóa · Chủ đề 1: Giới thiệu |
| 1 | Cao Thắng khác THPT thế nào — từ "được nhắc" sang "tự chịu trách nhiệm" | TĐ | So sánh 2 cột THPT/CĐ trên 6 việc (điểm danh, bài tập, thi lại, học phí…) | Tìm và chụp vị trí 3 nơi: phòng Đào tạo, phòng CTCT, phòng Y tế | Chủ đề 5 · Sự khác biệt giữa học tập ở Cao Thắng và bậc THPT |
| 2 | Quy chế đào tạo: tín chỉ, điều kiện thi, cảnh báo học vụ, điều kiện tốt nghiệp | TĐ | 5 tình huống "bạn Minh vắng 4 buổi, có được thi không?" — tra quy chế trả lời | Tự đăng nhập portal, xem lịch học và điểm danh của mình | Chủ đề 4: Điều kiện học tiếp và tốt nghiệp |
| 3 | Tiền tháng đầu: lập ngân sách, chia tiền cố định/ăn/đi lại/dự phòng | TL | Phiếu ngân sách cho "Minh" có 4 triệu/tháng; nhóm cân đối để không âm | Ghi mọi khoản chi 7 ngày (app hoặc sổ) | Chủ đề 2 · Quản lý thời gian và tiền bạc |
| 4 | Cảnh giác tháng đầu: việc nhẹ lương cao, đa cấp, app vay, giả công an/nhà trường gọi điện, "khoá học" lừa | TL | Phân loại 8 tin nhắn/quảng cáo thật: lừa hay thật, dấu hiệu nào | Kể cho 1 người thân 1 kiểu lừa vừa học | Chủ đề 2 · Những điều cần cảnh giác |
| 5 | Ở trọ/KTX: hợp đồng thuê, tiền cọc, điện nước, sống chung với bạn cùng phòng | TL | Nhóm soạn "thoả thuận phòng" 5 điều (giờ giấc, vệ sinh, khách, tiền chung, tiếng ồn) | Thống nhất thoả thuận với bạn cùng phòng (hoặc tự đặt nếu ở một mình) | Chủ đề 2 · Sinh hoạt tập thể |
| 6 | Ăn đủ chất với 50.000đ/ngày: đĩa ăn cân bằng, đi chợ, 3 món dễ nấu, an toàn thực phẩm | TL·SK | Nhóm lên thực đơn 3 ngày cho "Minh" trong ngân sách, chỉ ra chỗ thiếu rau/đạm | Tự nấu ít nhất 2 bữa | Chủ đề 2 · Ăn uống tự lập |
| 7 | An toàn giao thông khi tự đi lại: tuyến đường đi học, xe máy, mũ, rượu bia, mưa ngập | TL | Vẽ tuyến nhà trọ → trường, đánh dấu 3 điểm nguy hiểm và cách tránh | Kiểm tra phanh, đèn, mũ bảo hiểm của mình | Chủ đề 2 · An toàn giao thông |
| 8 | Thoát hiểm khi cháy nhà trọ và các số điện thoại cần thiết (113, 114, 115, y tế trường, GVCN) | TL | Xem ảnh một dãy trọ thật: chỉ lối thoát, chỗ nguy hiểm (ổ cắm, xe sạc điện) | Vẽ sơ đồ lối thoát nơi ở; lưu các số khẩn cấp vào danh bạ | Chủ đề 2 · Thoát hiểm trong đám cháy · Các số điện thoại liên lạc cần thiết |
| 9 | Ngủ và nhịp ngày: người trẻ cần 7–9 giờ; điện thoại trước giờ ngủ; ngủ bù không bù được | SK | Mỗi người vẽ "đồng hồ 24h" hôm qua, cặp đôi tìm 1 chỗ cắt bớt để ngủ thêm | Nhật ký giờ ngủ 7 ngày | Chủ đề 2 · Giấc ngủ và nhịp sinh hoạt |
| 10 | Nhớ nhà và cô đơn: bình thường hoá cảm giác, giữ liên lạc với gia đình, tìm chỗ thuộc về ở trường | SK | Đọc thư giả định của "Minh" tuần thứ 6; nhóm viết 3 lời khuyên thiết thực | Gọi về nhà, hỏi bố mẹ một điều chưa từng hỏi | Chủ đề 2 · Biết yêu thương |
| 11 | Tuần 168 giờ: lịch học, làm thêm, việc nhà, ngủ, giải trí — lập lịch tuần | KN | Điền lịch tuần mẫu, đếm giờ "biến mất" | Theo lịch tuần tự lập trong 5 ngày, đánh dấu ngày làm được | Chủ đề 2 · Quản lý thời gian và tiền bạc |
| 12 | Điện thoại và mạng xã hội: thời gian màn hình, dấu chân số, bình luận, chia sẻ ảnh người khác | SK·TĐ | Xem 4 bài đăng/bình luận: cái nào sau 3 năm nhà tuyển dụng thấy sẽ hại mình | Xem thống kê screen time, đặt 1 giới hạn | Chủ đề 2 · Facebook và các mạng xã hội |
| 13 | Khi bị ốm: tủ thuốc cơ bản, BHYT sinh viên, khi nào phải đi khám, không tự uống kháng sinh | TL·SK | 4 tình huống (sốt 2 ngày, đau bụng dữ dội, trầy xước, cảm): tự xử hay đi khám | Kiểm tra thẻ BHYT, lưu địa chỉ cơ sở khám gần nhà trọ | Chủ đề 2 · Tự chăm sóc khi ốm |
| 14 | Chuẩn bị thi học kì đầu: lịch ôn ngược từ ngày thi, quy chế thi, hậu quả gian lận | KN·TĐ | Lập lịch ôn 14 ngày cho 4 môn mẫu | Dán lịch ôn của mình ở chỗ học | Chủ đề 5 · Chuẩn bị tốt cho các kỳ thi |
| T | Tổng kết HK1: tự chấm Hộ chiếu tự lập, 1 điều đã làm được, 1 điều HK2 muốn sửa | — | Cặp đôi phỏng vấn nhau 3 câu | — | Chủ đề 2 · Tổng kết học kì |

### HK2 — Học có phương pháp, sống có nề nếp (năm 1)

Mục tiêu: SV biết học sao cho nhớ lâu, giữ được 1–2 thói quen tốt (ngủ, vận động, dọn dẹp) và biết tự
nhận ra khi mình đang quá tải.

| # | Bài | Mạch | Hoạt động 10' | Việc tuần | Ghi biên bản |
|---|---|---|---|---|---|
| K | Khởi động: nhìn lại điểm HK1, đặt **một** mục tiêu HK2 cụ thể, đo được | KN | Viết lại mục tiêu mơ hồ ("học tốt hơn") thành mục tiêu cụ thể | Chia mục tiêu thành việc từng tuần | Chủ đề 5 · Khái niệm về học tập |
| 1 | Não nhớ thế nào: vì sao đọc lại nhiều lần vẫn quên | KN | Thử nhanh: nhóm A đọc lại, nhóm B tự kiểm tra — so kết quả | Sau mỗi buổi học, tự viết ra 3 ý không nhìn vở | Chủ đề 5 · Khái niệm về học tập |
| 2 | Phương pháp học hiệu quả: tự kiểm tra, học giãn cách, làm bài xen kẽ | KN | Lập lịch giãn cách cho 1 môn chuyên ngành | Làm 2 phiên tự kiểm tra trong tuần | Chủ đề 5 · Các phương pháp học tập hiệu quả |
| 3 | Nghe giảng và ghi chép (Cornell), dám hỏi giảng viên | KN | Ghi chép 1 đoạn video kỹ thuật 3' theo mẫu Cornell | Hỏi giảng viên ít nhất 1 câu (trên lớp hoặc tin nhắn) | Chủ đề 5 · Các phương pháp học tập hiệu quả |
| 4 | Phần mềm hỗ trợ học: lịch, thẻ nhớ (Anki), Drive, dùng AI đúng cách — và liêm chính khi dùng AI | KN·TĐ | Phân biệt 5 cách dùng AI: cách nào là học, cách nào là chép | Cài/ dùng 1 công cụ cho 1 môn | Chủ đề 5 · Các phần mềm hỗ trợ học tập |
| 5 | Trì hoãn: vì sao mình trì hoãn, quy tắc 2 phút, chia việc nhỏ | KN | Mỗi nhóm "mổ" một việc bị trì hoãn thành bước đầu tiên ≤5' | Mỗi ngày làm bước đầu tiên của 1 việc đang hoãn | Chủ đề 2 · Quản lý thời gian và tiền bạc |
| 6 | Xây một thói quen nhỏ trong 6 tuần (gắn vào việc có sẵn, ghi dấu mỗi ngày) | SK·KN | Chọn thói quen, viết câu "nếu–thì", tìm bạn cùng theo dõi | Đánh dấu thói quen mỗi ngày (theo dõi đến hết HK) | Chủ đề 2 · Xây dựng thói quen |
| 7 | Vận động: tối thiểu 150 phút/tuần; tập trong phòng trọ không cần dụng cụ; ngồi lâu khi học | SK | Cả lớp tập thử bài 7 phút; nhóm xếp lịch 3 buổi/tuần | Vận động 3 buổi, mỗi buổi ≥20' | Chủ đề 2 · Vận động và sức khoẻ |
| 8 | Dọn dẹp chỗ ở, giặt giũ, rác — 5S áp dụng cho góc học tập và phòng trọ | TL·TĐ | Xem ảnh 2 góc học tập, áp 5S: sàng lọc, sắp xếp, sạch sẽ | Chụp góc học tập trước/sau khi 5S (tuỳ chọn chia sẻ) | Chủ đề 3 · 5S |
| 9 | Căng thẳng và tâm trạng: nhận biết dấu hiệu, thở hộp, nói ra với ai, khi nào cần chuyên gia | SK | Thực hành thở 4-4-4-4 hai phút; nhóm lập "danh sách người có thể gọi" cho "Minh" | Viết danh sách 3 người/nơi mình có thể tìm khi khó khăn (giữ riêng) | Chủ đề 2 · Sức khoẻ tinh thần |
| 10 | Rượu bia, thuốc lá điện tử, chất kích thích, cờ bạc online | SK | Đóng vai từ chối lời mời ở tiệc sinh nhật — 3 cách nói "không" mà không mất bạn | Ghi 1 câu từ chối của riêng mình | Chủ đề 2 · Những điều cần cảnh giác |
| 11 | Biết yêu thương: tình bạn, tình yêu, tôn trọng sự đồng thuận, chia tay văn minh | SK·TĐ | 4 tình huống nhắn tin: tôn trọng hay kiểm soát? | Làm 1 việc tử tế cho một người bạn | Chủ đề 2 · Biết yêu thương |
| 12 | Sức khoẻ sinh sản và quan hệ an toàn (mời y tế trường/ cán bộ đoàn cùng dạy) | SK | Hộp câu hỏi ẩn danh, trả lời chung | — | Chủ đề 2 · Sức khoẻ sinh sản |
| 13 | Đi làm thêm: chọn việc không hỏng học, hợp đồng, tiền lương, bị quỵt lương thì làm gì | TL·TĐ | So sánh 3 tin tuyển làm thêm: chỗ nào đáng ngờ, giờ làm có hợp lịch học không | Tính số giờ làm thêm tối đa không ảnh hưởng lịch học | Chủ đề 2 · Quản lý thời gian và tiền bạc |
| 14 | Ôn thi và liêm chính thi cử; giữ sức trong mùa thi (ngủ, ăn) | KN·TĐ | Lập lịch ôn + lịch ngủ mùa thi | Theo lịch ôn | Chủ đề 5 · Chuẩn bị tốt cho các kỳ thi |
| T | Tổng kết năm 1: chấm Hộ chiếu tự lập năm 1, viết **thư gửi chính mình năm 2** (GVCN giữ, trả đầu HK3) | — | Viết thư | — | Chủ đề 2 · Tổng kết năm học |

### HK3 — Giao tiếp và làm việc nhóm (năm 2)

Mục tiêu: SV làm được một dự án nhóm nhỏ có phân việc, biên bản, góp ý và trình bày; giao tiếp lịch sự
với giảng viên và người ngoài trường. **Dự án nhóm phục vụ lớp** chạy từ bài 4 đến bài 14 (vd làm
video hướng dẫn tân sinh viên, dọn khu xưởng, quyên góp, sổ tay ở trọ cho khoá dưới).

| # | Bài | Mạch | Hoạt động 10' | Việc tuần | Ghi biên bản |
|---|---|---|---|---|---|
| K | Khởi động: trả thư năm 1, đọc lại; năm 2 khác gì; vai trò "đàn anh/chị" với khoá dưới | TĐ | Cặp đôi: điều thư năm ngoái đúng/sai | — | Chủ đề 6 · Sự cần thiết của kỹ năng làm việc nhóm |
| 1 | Vì sao cần làm việc nhóm — người kỹ thuật không làm một mình | KN | Trò chơi xây tháp giấy 5' rồi rút kinh nghiệm | Ghi 1 việc trong tuần mà một mình không làm được | Chủ đề 6 · Sự cần thiết của kỹ năng làm việc nhóm |
| 2 | Các giai đoạn phát triển của nhóm (hình thành → xung đột → ổn định → hiệu quả) | KN | Nhận diện giai đoạn qua 4 đoạn hội thoại nhóm đồ án | Nhận ra nhóm đồ án của mình đang ở giai đoạn nào | Chủ đề 6 · Các giai đoạn phát triển của nhóm |
| 3 | Tầm quan trọng của giao tiếp kỹ thuật; lắng nghe chủ động | KN | Trò "truyền bản vẽ bằng lời": 1 người mô tả, 1 người vẽ — đo sai lệch | Trong 1 cuộc nói chuyện, nhắc lại ý người kia trước khi trả lời | Chủ đề 11 · Tầm quan trọng trong giao tiếp kỹ thuật |
| 4 | Các kỹ năng chung trong tổ chức nhóm: vai trò, phân việc, hạn chót, biên bản họp | KN | Lập nhóm dự án lớp, phân vai, viết biên bản buổi họp đầu | Họp nhóm lần 1 (≤20'), có biên bản | Chủ đề 6 · Các kỹ năng chung trong tổ chức nhóm |
| 5 | Viết tin nhắn và email chuẩn mực cho giảng viên, nhà trường, doanh nghiệp | KN·TĐ | Sửa 3 tin nhắn "thầy ơi cho em hỏi…" thành chuẩn | Gửi 1 email đúng chuẩn (xin tài liệu, hỏi lịch) | Chủ đề 11 · Viết trong kỹ thuật |
| 6 | Nói "không", nói điều khó, quyết đoán mà không gây hấn | KN | Đóng vai 3 tình huống (bạn nhờ làm hộ bài, mượn tiền, rủ bỏ học) | Dùng 1 lần câu "tôi" thay cho câu "bạn" | Chủ đề 11 · Làm sao để đạt hiệu quả cao trong giao tiếp |
| 7 | Xung đột trong nhóm và trong phòng trọ: tách vấn đề khỏi con người | KN | Nhóm giải 1 xung đột giả định theo 4 bước | — (dự án nhóm tiếp tục) | Chủ đề 6 · Thực hành làm việc nhóm |
| 8 | Góp ý và nhận góp ý không làm tổn thương | KN·TĐ | Góp ý mẫu "điều tốt – điều nên sửa – gợi ý cụ thể" cho 1 sản phẩm | Góp ý cho 1 thành viên nhóm theo mẫu | Chủ đề 6 · Phương pháp đánh giá hoạt động của nhóm |
| 9 | Sức khoẻ tinh thần năm 2: kiệt sức, so sánh trên mạng xã hội, khi bạn mình không ổn | SK | Nhận diện 5 dấu hiệu bạn đang gặp khó; tập câu mở lời và chỉ đường hỗ trợ | Hỏi thăm 1 người bạn lâu không gặp | Chủ đề 2 · Sức khoẻ tinh thần |
| 10 | Nấu cho cả tuần, đọc nhãn dinh dưỡng, cân nặng không phải nỗi ám ảnh | TL·SK | Đọc 4 nhãn (mì gói, sữa, nước tăng lực, bánh): so đường, muối | Chuẩn bị đồ ăn sẵn cho 3 ngày | Chủ đề 2 · Ăn uống tự lập |
| 11 | Giao tiếp bằng biểu đồ, bảng biểu: trình bày số liệu kỹ thuật cho dễ hiểu | KN | Biến một bảng số liệu đo thành biểu đồ đúng loại | Đưa 1 biểu đồ vào sản phẩm dự án | Chủ đề 11 · Giao tiếp bằng biểu đồ, bảng biểu |
| 12 | Thuyết trình 3 phút: mở – 3 ý – kết; đứng, nhìn, nói | KN | 2 SV xung phong thuyết trình nháp, lớp góp ý theo mẫu | Tập trước gương/ quay video 1 lần | Chủ đề 11 · Giao tiếp bằng lời nói (thuyết trình) |
| 13 | Các nhóm báo cáo dự án lớp (3' mỗi nhóm) | KN·TĐ | Báo cáo + lớp chấm theo tiêu chí công khai | — | Chủ đề 6 · Thực hành làm việc nhóm |
| 14 | Đánh giá nhóm và tự đánh giá; ôn thi | KN | Phiếu đánh giá đóng góp từng thành viên (ẩn danh với lớp, GVCN xem) | Lịch ôn thi | Chủ đề 6 · Phương pháp đánh giá hoạt động của nhóm |
| T | Tổng kết HK3: Hộ chiếu tự lập | — | — | — | Chủ đề 6 · Tổng kết học kì |

### HK4 — Tự quản trị: kế hoạch, vấn đề, tiền (năm 2)

Mục tiêu: SV tự lập được kế hoạch đến lúc tốt nghiệp, giải quyết vấn đề có phương pháp, quản lý tiền
có tiết kiệm và tránh được nợ xấu, có thái độ an toàn ở xưởng.

| # | Bài | Mạch | Hoạt động 10' | Việc tuần | Ghi biên bản |
|---|---|---|---|---|---|
| K | Khởi động: năm 2 còn nửa — mình đang ở đâu so với mục tiêu tốt nghiệp | KN | Đếm tín chỉ còn thiếu, môn nợ (nếu có) | Xem bảng điểm toàn khoá trên portal | Chủ đề 4: Điều kiện học tiếp và tốt nghiệp |
| 1 | Vai trò của lập kế hoạch trong học tập và công việc | KN | So sánh 2 nhóm đồ án: có/không kế hoạch — hậu quả | Viết kế hoạch 1 tuần có ưu tiên | Chủ đề 7 · Vai trò của kỹ năng lập kế hoạch trong học tập và công việc |
| 2 | Xác định nội dung công việc: chia một việc lớn thành việc nhỏ có hạn chót | KN | Chia "làm đồ án môn học" thành cây việc | Áp dụng cho 1 bài lớn đang làm | Chủ đề 7 · Phương pháp xác định nội dung công việc |
| 3 | Ưu tiên: gấp/quan trọng, mỗi ngày 1 việc lớn – 3 việc vừa | KN | Xếp 12 việc của "Minh" vào ma trận 4 ô | Mỗi tối chọn 1 việc lớn cho ngày mai | Chủ đề 7 · Vai trò của kỹ năng lập kế hoạch trong học tập và công việc |
| 4 | Kế hoạch đến tốt nghiệp: chứng chỉ ngoại ngữ, tin học, tay nghề, liên thông | KN·TĐ | Lập đường thời gian 3 HK còn lại | Hỏi phòng Đào tạo/ khoa 1 điều kiện mình chưa rõ | Chủ đề 4: Điều kiện học tiếp và tốt nghiệp |
| 5 | Giải quyết vấn đề và nhiệm vụ của người kỹ sư thực hành | KN | Kể 1 lỗi kỹ thuật thường gặp ở xưởng: ai phát hiện, ai sửa | Ghi 1 vấn đề nhỏ đang gặp | Chủ đề 8 · Giải quyết vấn đề và nhiệm vụ của người kỹ sư thực hành |
| 6 | Các bước cơ bản: xác định đúng vấn đề, tìm nguyên nhân gốc (5 lần "Vì sao") | KN | Hỏi 5 lần "vì sao" cho "chi tiết tiện bị sai kích thước" | Áp 5 Why cho vấn đề đã ghi | Chủ đề 8 · Các bước cơ bản để giải quyết vấn đề |
| 7 | Công cụ và phương pháp: biểu đồ xương cá, động não, PDCA | KN | Nhóm vẽ xương cá cho "hay đi học muộn" | Thử 1 giải pháp, ghi kết quả | Chủ đề 8 · Các công cụ và phương pháp giải quyết vấn đề |
| 8 | Ra quyết định tiền lớn: mua xe, điện thoại trả góp, đóng học thêm — tính tổng chi phí thật | TL·KN | Tính lãi thật của gói trả góp 0% có phí; so mua ngay/để dành | Liệt kê 1 thứ định mua, tính tổng chi phí | Chủ đề 2 · Quản lý thời gian và tiền bạc |
| 9 | Nợ và tín dụng: thẻ tín dụng, mua trước trả sau, app vay, nợ xấu ảnh hưởng thế nào | TL | Đọc hợp đồng vay mẫu, tìm phí ẩn | Kiểm tra mình có khoản trả góp/ nợ nào không | Chủ đề 2 · Những điều cần cảnh giác |
| 10 | Tiết kiệm và quỹ khẩn cấp; bảo mật tài khoản ngân hàng, OTP, mật khẩu | TL | Lập kế hoạch để dành 1 tháng chi tiêu trong 12 tháng | Bật xác thực 2 lớp cho tài khoản quan trọng | Chủ đề 2 · Quản lý thời gian và tiền bạc |
| 11 | Thái độ an toàn ở xưởng: vì sao "làm tắt" gây tai nạn, bảo hộ lao động, báo cáo sự cố | TĐ·SK | Phân tích 1 vụ tai nạn xưởng (tin thật): sai ở thái độ nào | Kiểm tra đồ bảo hộ cá nhân đủ chưa | Chủ đề 3 · Tác phong công nghiệp |
| 12 | Sức khoẻ nghề nghiệp: tư thế, mắt khi vẽ CAD, tai ở xưởng, lưng khi bê vác | SK | Chỉnh tư thế ngồi máy tính theo checklist | Nghỉ mắt 20-20-20 khi học máy tính | Chủ đề 3 · Tác phong công nghiệp |
| 13 | Đứng dậy sau thất bại: trượt môn, bị mắng, đồ án hỏng — nhìn lỗi như thông tin | SK·TĐ | Viết lại 3 câu tự trách thành câu "chưa… nên tôi sẽ…" | Ghi 1 lỗi tuần này và điều học được | Chủ đề 2 · Sức khoẻ tinh thần |
| 14 | Ôn thi; tổng kết dự án tự quản trị | KN | Lịch ôn | Theo lịch ôn | Chủ đề 5 · Chuẩn bị tốt cho các kỳ thi |
| T | Tổng kết năm 2: Hộ chiếu tự lập năm 2, thư gửi chính mình năm 3 | — | — | — | Chủ đề 7 · Tổng kết năm học |

### HK5 — Vào doanh nghiệp: tác phong và đạo đức nghề (năm 3)

Mục tiêu: SV sẵn sàng đi thực tập — biết mình được làm gì, có quyền gì, phải cư xử thế nào; có tác
phong đúng giờ, báo cáo, 5S. **Từ HK5 nhóm SV dẫn cả 20'.**

| # | Bài | Mạch | Hoạt động 10' | Việc tuần | Ghi biên bản |
|---|---|---|---|---|---|
| K | Khởi động: trả thư năm 2; kế hoạch thực tập; phân nhóm dẫn tiết | TĐ | Nhóm bốc thăm bài sẽ dẫn | — | Chủ đề 10 · Trường học và doanh nghiệp khác nhau như thế nào |
| 1 | Trường học và doanh nghiệp khác nhau như thế nào | TĐ | So sánh 1 ngày SV và 1 ngày công nhân kỹ thuật (mời cựu SV kể nếu được) | Hỏi 1 người đang đi làm về ngày làm việc của họ | Chủ đề 10 · Trường học và doanh nghiệp khác nhau như thế nào |
| 2 | Thích nghi với môi trường doanh nghiệp: tuần đầu đi làm, người hướng dẫn, văn hoá công ty | TĐ | Đóng vai ngày đầu: chào hỏi, nhận việc, hỏi lại khi chưa rõ | Viết 5 câu hỏi cần hỏi ngày đầu thực tập | Chủ đề 10 · Thích nghi với môi trường doanh nghiệp |
| 3 | 5S ở nhà máy: sàng lọc, sắp xếp, sạch sẽ, săn sóc, sẵn sàng | TĐ | Xem ảnh xưởng trước/sau 5S, chỉ ra từng S | Áp 5S cho tủ đồ/ góc làm việc ở xưởng trường | Chủ đề 3 · 5S |
| 4 | Tác phong công nghiệp: đúng giờ, báo cáo khi trễ, giữ cam kết, trang phục | TĐ | 5 tình huống "trễ 10 phút" — báo thế nào, lúc nào | Đến mọi buổi học đúng giờ cả tuần | Chủ đề 3 · Tác phong công nghiệp |
| 5 | Đạo đức và pháp luật: điều không phạm luật nhưng vẫn sai | TĐ | Xếp 6 hành vi vào ô "hợp pháp/ đạo đức" | — | Chủ đề 9 · Đạo đức và pháp luật |
| 6 | Các chuẩn mực đạo đức nghề nghiệp | TĐ | Tranh luận 2 phe một tình huống khó (sếp bảo bỏ qua lỗi nhỏ) | — | Chủ đề 9 · Các chuẩn mực đạo đức nghề nghiệp |
| 7 | Chuẩn mực của kỹ sư thực hành: trung thực số liệu đo, bảo mật bản vẽ, nhận lỗi | TĐ | Tình huống: đo sai, hàng đã giao — làm gì | Ghi 1 lần mình đã nhận lỗi/ chưa dám nhận | Chủ đề 9 · Các chuẩn mực đạo đức nghề nghiệp cơ bản của kỹ sư thực hành |
| 8 | Quyền của người lao động: hợp đồng, thử việc, lương, bảo hiểm xã hội, giờ làm thêm | TL·TĐ | Đọc 1 hợp đồng lao động mẫu, đánh dấu 5 điều phải có | Tra mức lương tối thiểu vùng nơi định làm | Chủ đề 10 · Thích nghi với môi trường doanh nghiệp |
| 9 | Nhận việc và báo cáo với cấp trên: hỏi lại cho rõ, báo tiến độ, báo sớm khi có trục trặc | KN·TĐ | Đóng vai giao việc mơ hồ → SV hỏi lại cho rõ | Báo tiến độ 1 việc nhóm mà không ai nhắc | Chủ đề 11 · Làm sao để đạt hiệu quả cao trong giao tiếp |
| 10 | Viết nhật ký và báo cáo thực tập | KN | Viết 1 trang nhật ký mẫu từ 1 buổi thực hành xưởng | Viết nhật ký 3 buổi thực hành | Chủ đề 11 · Viết trong kỹ thuật |
| 11 | Chuẩn bị đi thực tập: hồ sơ, tìm trọ gần khu công nghiệp, đi lại, ngân sách mới | TL | Lập ngân sách tháng thực tập (xa trường, có thể có phụ cấp) | Hoàn thành hồ sơ thực tập | Chủ đề 10 · Thích nghi với môi trường doanh nghiệp |
| 12 | Làm ca: ngủ khi làm ca đêm, ăn uống theo ca, an toàn khi về khuya | SK | Lập lịch ngủ – ăn cho 1 tuần làm ca 2 | — | Chủ đề 2 · Giấc ngủ và nhịp sinh hoạt |
| 13 | Quấy rối, bắt nạt, ép làm việc nguy hiểm ở nơi làm việc: nhận biết, ghi lại, báo ai | SK·TĐ | 4 tình huống: chuyện bình thường hay cần báo? Báo cho ai? | Lưu số GVCN/ khoa phụ trách thực tập | Chủ đề 9 · Các chuẩn mực đạo đức nghề nghiệp |
| 14 | Ôn thi | KN | — | — | Chủ đề 5 · Chuẩn bị tốt cho các kỳ thi |
| T | Tổng kết HK5: Hộ chiếu tự lập | — | — | — | Chủ đề 10 · Tổng kết học kì |

### HK6 — Tìm việc và sống tự lập hẳn (năm 3)

HK6 thường trùng thực tập tốt nghiệp — SHCN có thể thưa hơn hoặc trực tuyến. Bài 1–7 ưu tiên dạy
trước khi đi thực tập; bài 8–13 có thể dạy dồn hoặc giao tự đọc trên ThachLab rồi trao đổi ở buổi gặp.

| # | Bài | Mạch | Hoạt động 10' | Việc tuần | Ghi biên bản |
|---|---|---|---|---|---|
| K | Khởi động: nghề mình muốn làm trong 2 năm đầu, mức lương thực tế | TĐ | Tra 5 tin tuyển dụng đúng ngành, ghi yêu cầu chung | — | Chủ đề 12 · Tìm việc làm |
| 1 | Tìm việc làm: kênh tìm việc (khoa, cựu SV, trang tuyển dụng, hội chợ việc làm), tin tuyển dụng lừa đảo | TĐ·TL | Phân biệt 6 tin tuyển dụng: thật/ đáng ngờ | Lưu 3 tin tuyển dụng phù hợp | Chủ đề 12 · Tìm việc làm |
| 2 | Ứng tuyển: CV 1 trang, thư ứng tuyển, ảnh và email nghiêm túc | KN | Sửa 1 CV mẫu kém | Viết bản nháp CV | Chủ đề 12 · Ứng tuyển |
| 3 | Hồ sơ năng lực: ảnh sản phẩm, bản vẽ, đồ án, chứng chỉ — sắp thành 1 file | KN | Chọn 3 sản phẩm tốt nhất của mình và viết 2 dòng mô tả | Tạo thư mục hồ sơ năng lực | Chủ đề 12 · Ứng tuyển |
| 4 | Phỏng vấn ứng tuyển: câu hỏi hay gặp, kể chuyện theo Tình huống – Việc – Hành động – Kết quả | KN | Cặp đôi tập trả lời 3 câu hỏi phổ biến | Viết sẵn 2 câu chuyện của mình | Chủ đề 12 · Phỏng vấn ứng tuyển |
| 5 | Thực hành phỏng vấn thử (mời cựu SV/ doanh nghiệp nếu được) | KN·TĐ | 3 cặp phỏng vấn trước lớp, lớp góp ý | Quay video tự phỏng vấn 1 lần | Chủ đề 12 · Thực hành tìm việc và phỏng vấn ứng tuyển |
| 6 | Đọc kỹ thư mời nhận việc và hợp đồng; hỏi về lương, ca, bảo hiểm một cách lịch sự | TL·KN | Đóng vai trao đổi lương | — | Chủ đề 12 · Thực hành tìm việc và phỏng vấn ứng tuyển |
| 7 | Tháng lương đầu tiên: lương gộp/ thực nhận, BHXH, thuế TNCN, để dành, gửi về nhà | TL | Tính lương thực nhận từ 1 phiếu lương mẫu, lập ngân sách | Lập ngân sách tháng đầu đi làm | Chủ đề 2 · Quản lý thời gian và tiền bạc |
| 8 | Học tiếp sau tốt nghiệp: liên thông đại học, chứng chỉ nghề, học ngắn hạn | KN | Tra 1 lộ trình liên thông/ chứng chỉ phù hợp | — | Chủ đề 4: Điều kiện học tiếp và tốt nghiệp |
| 9 | Sống tự lập lâu dài: thuê nhà dài hạn, đăng ký cư trú, giấy tờ cá nhân cần giữ | TL | Danh sách giấy tờ cần có và nơi cất | Chụp lưu bản sao giấy tờ quan trọng ở chỗ an toàn | Chủ đề 2 · Sống tự lập |
| 10 | Sức khoẻ dài hạn: khám định kỳ, bảo hiểm, vận động khi đi làm 8 tiếng | SK | Lập "lịch sức khoẻ" một năm | — | Chủ đề 2 · Vận động và sức khoẻ |
| 11 | Gia đình khi mình đã trưởng thành: đỡ đần bố mẹ, nói chuyện về tiền, giữ ranh giới | SK | Viết 1 tin nhắn cảm ơn gia đình (không bắt đọc) | Gửi tin nhắn đó | Chủ đề 2 · Biết yêu thương |
| 12 | Giữ quan hệ nghề nghiệp: đồng nghiệp, thầy cô, cựu SV; nghỉ việc đúng cách | KN·TĐ | Viết email cảm ơn người hướng dẫn thực tập | — | Chủ đề 11 · Làm sao để đạt hiệu quả cao trong giao tiếp |
| 13 | Nhìn lại 3 năm: chấm Hộ chiếu tự lập toàn khoá, viết thư cho tân sinh viên khoá sau | — | Viết thư (GVCN dùng cho tiết khởi động của khoá sau) | — | Chủ đề 12 · Tổng kết khoá học |
| T | Chia tay lớp | — | — | — | Chủ đề 12 · Tổng kết khoá học |

---

## 4. Hộ chiếu tự lập (SV tự chấm cuối mỗi HK)

Một trang SV giữ (giấy hoặc ThachLab), tự đánh dấu **chưa / đang tập / làm được**. Không xếp hạng,
không công khai — chỉ để mỗi em thấy mình đi được bao xa. Cuối năm GVCN chỉ xem tỉ lệ cả lớp để biết
mạch nào cần dạy lại.

| Năm 1 — Tự lo cho mình | Năm 2 — Làm việc cùng người khác | Năm 3 — Bước vào nghề |
|---|---|---|
| Tự lập và giữ ngân sách tháng không bị âm | Họp nhóm có biên bản, phân việc rõ | Có CV và hồ sơ năng lực |
| Nấu được ít nhất 3 món đủ chất | Viết email chuẩn cho giảng viên/ doanh nghiệp | Trả lời được 5 câu phỏng vấn phổ biến |
| Nhận ra 5 kiểu lừa đảo phổ biến | Góp ý và nhận góp ý không cãi nhau | Đọc được hợp đồng lao động, phiếu lương |
| Biết lối thoát hiểm nơi ở, lưu số khẩn cấp | Thuyết trình 3 phút | Đúng giờ và báo trước khi trễ — thành thói quen |
| Ngủ đủ 7 giờ ít nhất 5 đêm/tuần | Lập kế hoạch đến tốt nghiệp | Áp 5S được ở chỗ làm |
| Vận động 150 phút/tuần | Dùng 5 Why/ xương cá cho 1 vấn đề thật | Biết báo cáo khi bị ép làm sai/ không an toàn |
| Có danh sách người để tìm khi khó khăn | Có quỹ khẩn cấp đang tích luỹ | Lập được ngân sách tháng lương đầu |
| Biết tra quy chế, điểm, lịch trên portal | Không có khoản nợ trả góp ngoài khả năng | Giữ đủ bản sao giấy tờ quan trọng |
| Giữ 1 thói quen tốt ≥6 tuần | Đeo bảo hộ đầy đủ ở xưởng mà không cần nhắc | Có kế hoạch học tiếp 2 năm sau tốt nghiệp |

---

## 5. Hai bài soạn mẫu đầy đủ

### Mẫu 1 — HK1 bài 3: "Tiền tháng đầu" (20')

**Mở (2')** — Chiếu tin nhắn giả định: *"Mẹ ơi, mới 18 mà con hết tiền rồi…"*. Hỏi cả lớp giơ tay:
tiền thường hết vì (a) ăn uống, (b) mua sắm online, (c) tiền trọ/ điện nước, (d) không biết đi đâu mất.

**Cốt lõi (5')** — 3 ý:
1. Trả trước những khoản **bắt buộc** (trọ, điện nước, đi lại, học phí) ngay ngày nhận tiền.
2. Chia phần còn lại thành **tiền ăn theo tuần** — hết tuần nào biết tuần đó, không "vay" của tuần sau.
3. Giữ một khoản **dự phòng** (ốm, hỏng xe) và không đụng tới khi không có sự cố.

**Làm (10')** — Phiếu nhóm 4 người: "Minh nhận 4.000.000đ/tháng. Trọ 1.300.000đ (chia đôi), điện nước
~200.000đ, xăng 300.000đ, điện thoại 100.000đ." Nhóm điền: tiền ăn/tuần bao nhiêu, dự phòng bao nhiêu,
còn lại bao nhiêu cho mua sắm – giải trí. Hai nhóm trình bày 1 phút; GVCN chỉ ra chỗ hay quên (sinh
nhật bạn, mua đồ thực hành, phí in ấn).

**Chốt + việc tuần (3')** — Mỗi SV viết: "Nếu tôi chuẩn bị trả tiền cho thứ gì, thì tôi ghi ngay
vào sổ/app." Việc tuần: ghi mọi khoản chi 7 ngày. Đầu tiết sau: 1–2 bạn tự nguyện nói **đã bất ngờ
vì khoản nào** (không nói số tiền).

### Mẫu 2 — HK2 bài 9: "Căng thẳng và tâm trạng" (20')

**Lưu ý trước khi dạy:** hỏi phòng CTCT/ Y tế trường xem trường có cán bộ tư vấn tâm lý, giờ làm việc,
cách đặt lịch, và đường dây hỗ trợ tâm lý đang được trường khuyến nghị — ghi đúng thông tin đó lên
bảng. Không tự đưa số điện thoại chưa kiểm tra.

**Mở (2')** — Hỏi: "Tuần trước thi giữa kì, ai ngủ dưới 6 tiếng ít nhất 1 đêm?" (giơ tay, không bắt
giải thích). Nói rõ: căng thẳng là phản ứng bình thường, không phải yếu đuối.

**Cốt lõi (5')**
1. **Dấu hiệu sớm**: khó ngủ, ăn thất thường, cáu gắt, né bạn bè, không tập trung được.
2. **Hạ nhịp ngay**: thở hộp 4 giây hít – 4 giữ – 4 thở ra – 4 giữ, 2 phút; đi bộ 10 phút; nói ra
   với một người.
3. **Khi nào cần người giúp**: kéo dài trên 2 tuần, ảnh hưởng học tập/ ăn ngủ rõ, hoặc có ý nghĩ làm
   hại bản thân → báo ngay GVCN/ cán bộ tư vấn/ người thân; trường hợp khẩn cấp gọi **115**.

**Làm (10')** — Cả lớp thở hộp 2 phút cùng GVCN. Sau đó nhóm đọc tình huống "Minh tuần 10: bỏ 3 buổi,
không trả lời tin nhắn nhóm" và lập danh sách: 3 dấu hiệu, 1 câu mở lời với Minh, 2 nơi có thể đưa
Minh tới.

**Chốt + việc tuần (3')** — Mỗi SV tự viết (giữ riêng, không nộp): 3 người/ nơi mình tìm tới khi khó
khăn. Câu "nếu–thì": "Nếu tôi mất ngủ 2 đêm liền, thì tôi sẽ…".

**Sau tiết**: GVCN để ý SV có biểu hiện bất thường trong buổi; nhắn riêng, không hỏi trước lớp.

---

## 6. Đối chiếu 12 chủ đề chính thức → bài dạy

Mọi mục con trong `lib/shcn/gddd-topics.ts` đều có ít nhất một tuần.

| Chủ đề | Mục con | Dạy ở |
|---|---|---|
| 0 · Sinh hoạt đầu khóa | — | HK1·K |
| 1 · Giới thiệu | — | HK1·K |
| 2 · Kỹ năng sống | An toàn giao thông | HK1·7 |
| | Sinh hoạt tập thể | HK1·5 |
| | Quản lý thời gian và tiền bạc | HK1·3, HK1·11, HK2·5, HK2·13, HK4·8, HK4·10, HK6·7 |
| | Biết yêu thương | HK1·10, HK2·11, HK6·11 |
| | Facebook và các mạng xã hội | HK1·12 |
| | Thoát hiểm trong đám cháy | HK1·8 |
| | Những điều cần cảnh giác | HK1·4, HK2·10, HK4·9 |
| | Các số điện thoại liên lạc cần thiết | HK1·8 |
| 3 · 5S và tác phong công nghiệp | 5S | HK2·8, HK5·3 |
| | Tác phong công nghiệp | HK4·11, HK4·12, HK5·4 |
| 4 · Điều kiện học tiếp và tốt nghiệp | (chưa có mục con) | HK1·2, HK4·K, HK4·4, HK6·8 |
| 5 · Học tập hiệu quả | Khái niệm về học tập | HK2·K, HK2·1 |
| | Sự khác biệt giữa học tập ở Cao Thắng và bậc THPT | HK1·1 |
| | Các phương pháp học tập hiệu quả | HK2·2, HK2·3 |
| | Chuẩn bị tốt cho các kỳ thi | HK1·14, HK2·14, HK4·14, HK5·14 |
| | Các phần mềm hỗ trợ học tập | HK2·4 |
| 6 · Kỹ năng làm việc nhóm | Sự cần thiết của kỹ năng làm việc nhóm | HK3·K, HK3·1 |
| | Các giai đoạn phát triển của nhóm | HK3·2 |
| | Phương pháp đánh giá hoạt động của nhóm | HK3·8, HK3·14 |
| | Thực hành làm việc nhóm | HK3·7, HK3·13 |
| | Các kỹ năng chung trong tổ chức nhóm | HK3·4 |
| 7 · Kỹ năng lập kế hoạch | Vai trò của kỹ năng lập kế hoạch… | HK4·1, HK4·3 |
| | Phương pháp xác định nội dung công việc | HK4·2 |
| 8 · Kỹ năng giải quyết vấn đề | Giải quyết vấn đề và nhiệm vụ của người kỹ sư thực hành | HK4·5 |
| | Các bước cơ bản để giải quyết vấn đề | HK4·6 |
| | Các công cụ và phương pháp giải quyết vấn đề | HK4·7 |
| 9 · Đạo đức nghề nghiệp | Đạo đức và pháp luật | HK5·5 |
| | Các chuẩn mực đạo đức nghề nghiệp | HK5·6, HK5·13 |
| | Các chuẩn mực… cơ bản của kỹ sư thực hành | HK5·7 |
| 10 · Trường học và doanh nghiệp | Trường học và doanh nghiệp khác nhau như thế nào | HK5·K, HK5·1 |
| | Thích nghi với môi trường doanh nghiệp | HK5·2, HK5·8, HK5·11 |
| 11 · Giao tiếp trong kỹ thuật | Tầm quan trọng trong giao tiếp kỹ thuật | HK3·3 |
| | Viết trong kỹ thuật | HK3·5, HK5·10 |
| | Giao tiếp bằng lời nói (thuyết trình) | HK3·12 |
| | Giao tiếp bằng biểu đồ, bảng biểu | HK3·11 |
| | Làm sao để đạt hiệu quả cao trong giao tiếp | HK3·6, HK5·9, HK6·12 |
| 12 · Kỹ năng tìm việc làm và ứng tuyển | Tìm việc làm | HK6·K, HK6·1 |
| | Ứng tuyển | HK6·2, HK6·3 |
| | Phỏng vấn ứng tuyển | HK6·4 |
| | Thực hành tìm việc và phỏng vấn ứng tuyển | HK6·5, HK6·6 |

Bài **thêm mới** (ngoài mục con chính thức, ghi dưới Chủ đề 2): Ăn uống tự lập (HK1·6, HK3·10), Giấc
ngủ và nhịp sinh hoạt (HK1·9, HK5·12), Tự chăm sóc khi ốm (HK1·13), Xây dựng thói quen (HK2·6), Vận
động và sức khoẻ (HK2·7, HK6·10), Sức khoẻ tinh thần (HK2·9, HK3·9, HK4·13), Sức khoẻ sinh sản (HK2·12),
Sống tự lập (HK6·9). Nếu muốn ThachLab hiện "Tự đọc thêm" cho các bài này, thêm chúng vào `items` của
chủ đề 2 trong `gddd-topics.ts` (lúc đó cần có tài liệu đọc thêm tương ứng).

---

## 7. Lưu ý triển khai

- **Lớp đang học năm 1 (CĐ CK 26C, NH 2026–2027)**: HK1 đã qua khoảng 10 tuần. Các bài HK1 chưa dạy
  ưu tiên theo thứ tự: 4 (cảnh giác) → 3 (tiền) → 13 (khi ốm) → 9 (ngủ) → 14 (thi); bài nào lớp đã học
  theo chủ đề 2 thì bỏ qua, phần còn thiếu dồn sang đầu HK2.
- **Tuần đệm** đặt đúng tuần thi/ lễ/ hoạt động lớn của trường; không dồn hai bài vào một tiết.
- **Chủ đề nhạy cảm** (tiền gia đình, tâm lý, tình cảm, sức khoẻ sinh sản): luôn dùng nhân vật giả
  định; việc tuần dạng "giữ riêng"; phối hợp y tế/ CTCT/ Đoàn khi cần người có chuyên môn.
- **Đo hiệu quả, không chấm điểm**: cuối mỗi HK xem (1) tỉ lệ SV tự đánh dấu "làm được" trong Hộ chiếu,
  (2) số SV nhắc lại được việc tuần đầu tiết, (3) điểm danh/ cảnh báo vắng trên ThachLab trước và sau
  các bài về ngủ, thói quen, thời gian. Mạch nào thấp thì đưa bài nhắc lại vào HK sau.
- **Nhóm SV dẫn tiết (năm 2–3)**: GVCN duyệt nội dung trước 1 tuần; nhóm dẫn dùng đúng khung 2–5–10–3.
