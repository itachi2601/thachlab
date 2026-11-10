# Rà hình sách OpenStax *Physics* (bản THPT) cho 26 bài lớp 11 — 29/10/2026

Kết luận: **không chèn, không thay hình nào; 26 bài giữ nguyên.** Hai đợt trước (`hinh-openstax-l11-*.md`, `…-dot2.md`) đã lấy hết hình
cùng ý từ *College Physics 2e*, và *Physics* THPT là bản rút gọn của cùng nội dung: hình trùng ý thì đã có, hình còn lại là ảnh minh
hoạ ngành hoặc nằm ngoài mạch số liệu của bài. Chèn thêm hình tương đương chỉ làm tăng tải nhận thức (G1, Mayer: mạch lạc, không dư).

## Giấy phép (tra 29/10/2026)

- Trang chi tiết sách (API CMS `books.Book`, slug `physics`): **Creative Commons Attribution License 4.0 (CC BY 4.0)**. Chân trang
  site OpenStax ghi CC BY‑NC‑SA là của cả site, không phải của sách này. CC BY nới hơn *College Physics 2e* (CC BY‑NC‑SA): chỉ cần ghi nguồn.
- Hình nào có `(credit: …)` là ảnh bên thứ ba, phải giữ credit đó. Có credit trong các mục đã đọc: 3.10, 3.11, 5.41, 13.10, 14.6, 17.2, 18.13, 18.15, 18.29.
- Nếu sau này chèn: figcaption cuối ghi `Hình: OpenStax, Physics, Hình X.Y — CC BY 4.0 — openstax.org/books/physics`.

## Mục đã đọc (lấy chú thích bằng fetch + DOMParser, không chụp màn hình)

3.1, 3.2, 5.5, 13.1, 13.2, 13.3, 14.1, 14.4, 15.1, 17.1, 18.1–18.5, 19.1–19.4. (Chương 20 từ trường và 22 hạt nhân thuộc lớp 12.)
Hình đáng chú ý của sách: 5.39 (vật–lò xo), 5.40 (con lắc đơn), 13.3/13.4/13.5 (sóng ngang, sóng dọc trên lò xo), 13.7 (λ, A, T trên sóng nước),
13.11/13.12 (giao thoa cùng pha / ngược pha), 14.21–14.27 (cột khí cộng hưởng), 15.2/15.3 (sóng điện từ, phổ), 17.8–17.10 (khe Young),
18.17–18.19 (điện trường), 18.21/18.22 (tương tự trọng trường), 18.28/18.30 (tụ), 19.3–19.5 (dòng điện), 19.9 (tương tự nước), 19.20–19.22 (công suất).

## Bảng quyết định

Số từ lấy từ `lint_do_dai.py` (từ hiện ngay, 29/10). Trần 2440. "Đã có" = hình College Physics 2e đã chèn ở đợt 1–2.

| Bài | Hình hiện có | Hình *Physics* đề xuất | Quyết định | Lý do |
|---|---|---|---|---|
| l11-mo-ta-dao-dong | 4 SVG (hook con lắc đồng hồ, vòng tròn pha, lệch pha, 5 chấm x = 5cos) | 5.39 (vật–lò xo), 5.40 (con lắc đơn) | **Giữ** | 5.39 thiếu mốc pha và số liệu của bài; con lắc đơn chưa dạy ở đây |
| l11-dao-dong-dieu-hoa | 1 SVG + 2 ảnh College (đồ thị li độ trên giấy, hình chiếu chuyển động tròn) | 5.39 | **Giữ** | SVG đã gắn nhãn O, ±A theo bài; 5.39 chỉ lặp ý |
| l11-van-toc-gia-toc | 2 SVG + 1 ảnh College (đồ thị x–v–a) | 3.6, 3.7 (độ dốc là vận tốc/gia tốc, chuyển động thẳng) | **Giữ** | Hình sách nói về chuyển động thẳng đều/biến đổi đều, không phải dao động; đồ thị x–v–a đã có |
| l11-co-nang-dao-dong | 3 SVG + ảnh College 16.14 (đổi thế năng ↔ động năng) | 5.39 | **Giữ** | Đã có ảnh cùng ý, 5.39 không có năng lượng |
| l11-tat-dan-cuong-buc | 3 SVG + ảnh College (đường cong cộng hưởng) | 14.18 (quả bóng gắn dây cao su, ngón tay đưa theo tần số riêng) | **Giữ** | Cộng hưởng đã có đường cong và hook xích đu; 14.18 chỉ trùng ý, thêm một hình |
| l11-bai-tap-dao-dong, l11-bai-tap-nang-luong-dao-dong, l11-bai-tap-song | SVG theo số liệu đề | — | **Giữ** | Hình bài tập nằm trong mạch số liệu của đề |
| l11-mo-ta-song | 3 SVG + ảnh College (hai âu nhấp nhô) | 13.7 (λ, A, T trên sóng nước, có chim biển) | **Giữ** | Ảnh College đã diễn đạt λ trên sóng; 13.7 là ảnh minh hoạ thêm; bài 2457 từ, sát trần |
| l11-song-ngang-song-doc | 2 SVG + 2 ảnh College (sóng ngang trên dây, sóng dọc trên lò xo) | 13.3, 13.4, 13.5 (dây đàn ngang, loa làm tờ giấy rung dọc) | **Giữ** | 13.3/13.4 trùng ảnh đã có; 13.5 là ý "âm là sóng dọc" bài đã nói bằng chữ; bài 2686 từ, vượt trần nên chỉ được thay, không có hình để thay |
| l11-giao-thoa-song | 2 SVG + 3 ảnh College (hai loa cực đại, cùng pha/ngược pha, khe Young cường độ) | 13.11, 13.12 (giao thoa cùng pha/ngược pha), 17.8–17.10 (khe Young) | **Giữ** | Cả hai cặp trùng ý với ảnh đã có; đang 5 hình, thêm nữa là chồng thêm (Mayer) |
| l11-song-dung | 2 SVG + ảnh College (hai sóng ngược chiều) | 14.26/14.27 (cột khí một đầu kín, hai đầu hở) | **Giữ** | Cột khí vẽ độ dời không khí, không có trường hợp dây hai đầu cố định 3 bó trong lời giải; bài 2780 từ |
| l11-bai-tap-song | SVG số liệu | — | **Giữ** | như trên |
| l11-song-dien-tu | 2 SVG + ảnh College (E–B) | 15.2 (E, B cùng pha), 15.3 (phổ điện từ nhãn Anh) | **Giữ** | 15.2 trùng ảnh đã có; phổ cần nhãn tiếng Việt và vùng số liệu của bài nên giữ SVG |
| l11-thuc-hanh-do-tan-so-am | SVG dụng cụ, dao động kí, đồ thị | — | **Giữ** | Sách không có dao động kí hay ukulele |
| l11-thuc-hanh-do-toc-do-am | 4 SVG (chai nước, hai ống cộng hưởng, bộ dụng cụ, đồ thị độ to) | 14.21–14.25 (âm thoa + ống kín một đầu) | **Giữ** | Không có hiệu chỉnh đầu ống e mà phương pháp đo dựa vào; số liệu bài riêng |
| l11-luc-coulomb | 3 SVG + ảnh College (lực hai điện tích) | 18.16 (định luật Coulomb, định luật 3), 18.15 (cân xoắn, credit) | **Giữ** | 18.16 trùng ảnh đã có; 18.15 là ảnh lịch sử có credit, không giải thích ý nào |
| l11-khai-niem-dien-truong | 1 SVG + 3 ảnh College (vectơ E, đường sức, chồng chất) | 18.17–18.19 | **Giữ** | Đã thay bằng College 18.19/18.20/18.21 ở đợt 2; sách THPT chỉ có bản đơn giản hơn. Bài 2785 từ, vượt trần |
| l11-dien-truong-deu | 3 SVG + ảnh College (hai bản song song) | 18.27/18.28 | **Giữ** | Đã có ảnh cùng ý; hook không để lộ đáp án |
| l11-dien-the | 3 SVG + ảnh College (hai bản đẳng thế) | 18.21, 18.22 (tương tự trọng trường: quả bóng càng cao thế năng càng lớn) | **Giữ** | Bài đã dùng chính phép so sánh "độ cao bậc cầu thang" bằng chữ; thêm ảnh là dư (Mayer: dư thừa) |
| l11-the-nang-dien | 4 SVG | 18.22, 18.23 (thế năng theo dấu điện tích) | **Giữ** | Bài 2775 từ, vượt trần, SVG nằm trong mạch số liệu (M→N, 3 cm, 2 cm) |
| l11-tu-dien | 2 SVG + 2 ảnh College (ghép nối tiếp / song song) | 18.28 (hai bản + pin), 18.30/18.31 (điện môi), 18.29 (ảnh tụ, credit) | **Giữ** | 18.28/18.30 cao 775–1003 px, chữ nhỏ ở 375 px; không có ghép tụ trong sách THPT; 18.29 là ảnh minh hoạ có credit |
| l11-cuong-do-dong-dien | 3 SVG + ảnh College (hạt tải trong dây) | 19.3, 19.4 (chiều quy ước, electron), 19.5 (va chạm) | **Giữ** | H1 đã có mũi tên chiều dòng điện; 19.4 dư; bài 2484 từ, sát trần |
| l11-dien-tro-dinh-luat-ohm | 4 SVG | 19.9 (mạch điện ↔ mạch nước), 19.10 (điện trở vòng màu) | **Giữ** | Bài 2466 từ (trên trần), không thêm; đồ thị 10 Ω và đèn sợi đốt là số đo riêng; vòng màu ngoài chương trình |
| l11-nguon-dien, l11-thuc-hanh-do-sdd-pin | 4 SVG mỗi bài | 19.2 (pin nối dây) | **Giữ** | Sách không có ε, r; số liệu 9,0 V, 1,0 Ω, 1,50 V riêng |
| l11-nang-luong-cong-suat-dien | 4 SVG | 19.20 (bóng 25 W, 60 W), 19.21, 19.22 (bánh xe công thức) | **Giữ** | 19.20 là ảnh minh hoạ ngành (chi tiết hấp dẫn), 19.22 nặng chữ; bài 2842 từ, vượt trần |

## Việc không làm và vì sao

- Không tải ảnh, không đọc ảnh bằng subagent: không hình nào qua được bước chọn theo mô tả và chú thích (cùng ý đã có, ngoài mạch số liệu, hoặc ảnh minh hoạ).
- Không đổi hình College Physics sang hình tương đương của *Physics*: không cải thiện khả năng tiếp thu, chỉ tăng việc phải đăng lại và rủi ro trộn giấy phép (CC BY‑NC‑SA ↔ CC BY).
- Số từ và hình của 26 bài không đổi; không cần build, không đụng `content/thi-nghiem/`.
