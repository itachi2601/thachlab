---
name: soan-bai-tap-tu-luan-hsg
description: Soạn BỘ BÀI TẬP TỰ LUẬN in giấy (PDF A4, không ghi DB) mức Vận dụng → Vận dụng cao cho lớp 9 chuyên / đội tuyển HSG KHTN 9 Vật lí (và lớp 10–12 ôn chuyên) — mỗi bài 3–4 ý khó dần, hình SVG trong script sinh, gợi ý 3 tầng theo phong cách thầy Thạch (kiến thức → điều kiện áp dụng → hướng tính), lời giải tập riêng (chữ trước số sau, Đáp số, Nhận dạng, Bẫy), số liệu tính bằng Python, kiểm chéo bắt buộc bằng agent kiem-code giải độc lập từ đề không đáp án, dàn trang bằng _tools/trang-mau-sach. Dùng khi thầy nói "soạn bài tập tự luận vận dụng cao cho lớp 9 chuyên", "ra bộ bài tập cơ học/điện/quang cho đội tuyển", "làm bài tập có gợi ý và đáp án kiểu pre-test", "soạn chuyên đề bài tập HSG có hình". KHÁC soan-bai-tap-mau (mục Bài tập mẫu trên web, có mô phỏng, ghi DB), de-vat-ly-thpt (đề thi trắc nghiệm Azota), up-de-kiem-tra (đăng đề lên web). Chạy trên Mac (cần Chrome + book/node_modules để dựng PDF).
---

# Soạn bộ bài tập tự luận VD–VDC cho lớp chuyên / HSG (thầy chốt 10/10/2026)

Sản phẩm: **một thư mục con riêng** trong kho nội dung HSG (`~/Documents/THPT/Lop09/00_Dung_chung/HSG_KHTN9_Vat_li/01_Chuyen_de/<Ten_bo>/`
hoặc nơi thầy chỉ), gồm `sinh-bai-tap.py` (nguồn duy nhất), 2 PDF (đề + gợi ý · lời giải), `de-chi-de.md`, `dap-an.json`, `README.md`.
Mẫu đầy đủ đã duyệt: `references/mau-sinh-bai-tap.py` (bộ Cơ học 12 bài, 10/10/2026) — **chép khung này, đừng viết lại từ đầu**.

## Nguyên tắc nội dung

1. **Phạm vi theo đề cương thi**, không theo SGK: lớp 9 chuyên được dùng mômen với thanh có khối lượng, hiệu suất máy cơ nối tiếp,
   bình thông nhau có pittông, động năng dòng chảy… nhưng **ghi nhãn "ngoài chuẩn KHTN 9"** trong README cho từng bài.
   Không dùng kiến thức lớp 10 (vectơ lực hợp thành, động lượng, gia tốc) trừ khi thầy bảo.
2. **Mỗi bài 3–4 ý, ý sau khó hơn ý trước** (a: áp dụng trực tiếp → b: thêm điều kiện/bẫy → c, d: kết hợp hoặc tình huống ngược).
   Mức ghi trên đề: *Vận dụng* (ý khó nhất là kết hợp 2 bước) · *Vận dụng cao* (phải nhận ra điều kiện ẩn, đi nhiều lượt, hệ nhiều vật).
   Trong một mảng, bài VD đi trước bài VDC (nền trước, kỹ năng sau — AI-TUTOR 9.2).
3. **Số liệu "đẹp" nhưng phải phân biệt được cách sai**: chọn số sao cho cách làm sai cho đáp số KHÁC đáp số đúng (vd. tốc độ trung bình:
   chọn v để trung bình cộng ≠ v_tb; bài gặp nhau: để lấy hiệu tốc độ ra số khác). Thử trước trong Python.
4. **Hình SVG cho mọi bài có bố trí không gian** (hệ ròng rọc, bình, máng, dốc, thanh). Bài thuần số (tốc độ trung bình) không cần hình.
   Dữ kiện ghi trên hình, đại lượng cần tìm ghi "?". Đầu mũi tên dùng marker `#ah` của `sach_mau` (bộ in giấy, không phải `svg_lib` của web).
5. **Gợi ý 3 tầng, in ở cuối đề** (học sinh che lại): tầng 1 nêu tên kiến thức; tầng 2 là **câu hỏi về điều kiện áp dụng** ("đoạn nào có lực
   không bảo toàn?", "lực dọc mặt nghiêng là lực nào trong hệ?"); tầng 3 mới chạm công thức/hướng tính. Không giải hộ ở gợi ý (AI-TUTOR 9.1, 9.5).
6. **Lời giải tập riêng**, mỗi ý: công thức chữ → thế số → kết quả đậm; mỗi bước một dòng; có dòng "Kiểm:" khi thế ngược được.
   Sau các ý: ô **Đáp số** (mỗi ý một dòng) → **Nhận dạng** ("Thấy **…** → nghĩ tới **…**", ≤ 25 chữ, từ khoá in đậm là chữ gặp trong đề)
   → **Bẫy thường gặp** (2–3 dòng, mỗi dòng một lỗi + vì sao sai). Giọng trung tính, câu ngắn, không "thầy/con", không khen.
7. Đầu đề có khung "Quy ước và cách làm": g, D nước; **3 dòng viết trước khi giải** (kiến thức – điều kiện – công thức); trình bày; cách dùng gợi ý;
   đối chiếu lời giải xong thì gấp lại giải lại (retrieval, AI-TUTOR 9.3).

## Quy trình (một bộ 10–12 bài ≈ 1 phiên)

1. Đọc nhanh (grep/đoạn, không đọc cả file): `docs/memory/project_thachlab_khoa_hsg9_vat_ly.md`, README của kho HSG, README của pre-test
   cùng mảng (phong cách, quy ước g, D), `docs/AI-TUTOR.md` mục 9 (chỉ 9.1/9.3/9.5). Không mở docx chuyên đề trừ khi cần đối chiếu một bài.
2. **Lên khung trước khi viết**: bảng Mảng → bài → mức → ý a/b/c/d → số liệu dự kiến. Tính thử mọi đáp số trong Python ngay lúc này
   (mục `N1..N12` trong script) — sửa số rẻ hơn sửa văn.
3. Viết `sinh-bai-tap.py` theo mẫu: `bai(n, muc, lvl, ten, fig, de[], goi_y[3], giai[(tiêu đề ý, [dòng…])], dap[], nhan_dang, bay[])`.
   Mọi số trong `giai` lấy từ `N*` qua `f()` (dấu phẩy thập phân), không gõ tay. `dung(..., school=False)` trừ khi thầy yêu cầu tên trường.
4. Chạy script → 2 PDF + `de-chi-de.md` (đề thuần chữ, mô tả hình bằng lời) + `dap-an.json`.
5. **Hai subagent song song** (phiên chính không đọc ảnh):
   - `kiem-code` (Sonnet): đọc **chỉ** `de-chi-de.md`, giải độc lập bằng python3, trả bảng đáp số + danh sách vấn đề (mâu thuẫn đề, cách hiểu
     khác, ngoài chương trình, mức độ). Prompt mẫu: `references/prompt-kiem-cheo.md`.
   - `general-purpose`: `pdftoppm -r 70 -png` hai PDF vào `.xem-thu/`, xem từng trang: nhãn cắt mép, nhãn đè, hình không khớp đề, ký tự lạ, trang trắng.
6. Đối chiếu `dap-an.json` với bảng của agent → lệch thì tự giải lại bằng tay thứ ba rồi sửa **số liệu hoặc đề**, chạy lại, kiểm lại bài đó.
   Góp ý "đề nhiều cách hiểu" → sửa câu chữ đề ngay (thêm "dây song song mặt nghiêng", "miệng cốc hướng lên"…).
7. Viết `README.md` (file nào là gì, mảng → bài, mức, bài ngoài chuẩn, cách kiểm), xoá `.xem-thu/`. Báo thầy ngắn: bảng bài–mức–đáp số,
   việc chưa làm, rút kinh nghiệm. Số hoá lên thachlab chỉ khi thầy bảo (theo `docs/DANG-DE-TU-WORD.md`).

## Lỗi hay gặp khi dựng (đã gặp 10/10/2026)
- `fig()` đánh số hình theo thứ tự gọi: dựng đề xong mới reset `FIGN` nếu lời giải cũng chèn hình.
- Ký tự toán Unicode (𝒫, ½, ·, ⇒, ₁) hiện tốt với font Be Vietnam Pro + Times; tránh LaTeX vì trang mẫu không có KaTeX.
- `pdftoppm` có sẵn trên Mac (`/opt/homebrew/bin`); `fitz` cũng có. Không dùng `sips` (chỉ trang 1).
- Hình ròng rọc trên mặt nghiêng: vẽ bằng toạ độ dọc/ngang mặt nghiêng (`on(s, off)`), đừng vẽ tay từng điểm.

## Nhật ký rút kinh nghiệm
- 2026-10-10 · Bộ Cơ học 12 bài đầu tiên: `kiem-code` khớp 12/12 đáp số nhưng chỉ ra 9 chỗ đề **thiếu điều kiện phụ** (lực cản "không đổi" mâu thuẫn với câu xuống dốc; bình có thể tràn; cốc có ngập; công suất tiêu thụ hay có ích; dây không giãn; dầu không tan) → khi viết đề, rà checklist điều kiện phụ: *bình đủ cao · bỏ qua thể tích dây/thành · dây không giãn · vật ngập hoàn toàn · công suất nào · lực cản áp cho đoạn nào*. Đáp số đúng không có nghĩa đề đã kín.
- 2026-10-10 · Hình ròng rọc trên mặt nghiêng vẽ sai lần đầu vì **dấu của pháp tuyến** (`off` đi vào trong nêm) → luôn định nghĩa `on(s, off)` với `n = (uy, −ux)` và kiểm bằng cách in toạ độ 2–3 điểm trước khi render. Agent xem ảnh nhỏ báo "dây không song song" nhưng toạ độ cho thấy song song → **kiểm toạ độ trước khi tin agent xem ảnh**, đỡ một lần vẽ lại.
- 2026-10-10 · Soát hình lần 2 chỉ cần 3–4 hình → render riêng từng SVG bằng Chrome headless (`--screenshot --window-size=340,210`) rồi xem ở phiên chính (≈ 300 token/ảnh), rẻ hơn 100 k token của một agent soát cả 18 trang. Agent soát cả trang chỉ dùng một lần đầu.
- 2026-10-10 · Thay chuỗi trong script bằng danh sách `(cũ, mới)` + `assert count==1`: một mục "không đổi gì" làm assert fail và **không ghi file** mà lệnh dựng sau vẫn chạy → nhìn kỹ "edited N" trước khi dựng lại.
- 2026-10-10 · Token: đọc cả `sinh-pretest` (28 KB) để lấy phong cách là thừa — chỉ cần 60 dòng helper + 2 câu mẫu; lần sau `sed -n` đúng đoạn.
