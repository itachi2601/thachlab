---
name: ve-hinh-cau-hoi
description: Bổ sung hình minh hoạ (SVG tự vẽ) cho câu hỏi trong ngân hàng question_bank mà đề có mô tả tình huống/đồ thị/sơ đồ nhưng chưa có hình — quét theo chương, phân loại, vẽ bằng khuôn có tham số, thầy duyệt trên trang xem thử, ghi vào ngân hàng + các đề đang dùng, kiểm lại mỗi câu đúng 1 hình. Dùng khi thầy nói "vẽ hình cho câu hỏi chương X", "câu này mô tả mà thiếu hình", "mở rộng hình minh hoạ sang lớp 11/12", "/ve-hinh-cau-hoi". KHÁC anh-xau-ngan-hang (thay ảnh xấu) và soan-bai-ly-thuyet-tuong-tac (hình trong bài lý thuyết).
---

# Vẽ hình minh hoạ cho câu hỏi ngân hàng

Thí điểm L10 Động lực học (29/10/2026): 57 hình ghi xong. Mã nguồn mẫu: `scripts/data/hinh-cau-hoi/` (`ve-mau.py` khuôn mặt phẳng nghiêng/kéo xiên/vật treo, `ve-so-do.py` sơ đồ tay, `ve-do-thi.mts` đồ thị v–t, `dung-xem-thu.py` trang duyệt). Chương khác: copy thư mục, đổi tên theo `<lớp>-<chương>`.

## Nguyên tắc chọn câu và vẽ (M1, M3, M5)
- Chỉ vẽ khi hình **mang thông tin** đề cần (bố trí vật, góc, đồ thị). Không vẽ trang trí.
- **Không lộ đáp án**: không vẽ phản lực, thành phần lực, hợp lực khi đề hỏi các đại lượng đó; chỉ ghi nhãn cho số liệu đề đã cho (không tự thêm góc/độ dài mặc định).
- Nét `currentColor` (sáng/tối), mũi tên có marker riêng từng màu, nhãn không đè lên hình (nhãn chiều dài đặt trong tam giác).
- Câu mơ hồ (không dựng nổi bố trí chắc chắn) → **không vẽ**, liệt kê cho thầy. Câu ghi "như hình vẽ" mà thiếu hình → cần tìm đề gốc, không bịa.
- Nguồn ảnh thật (hiện tượng đời sống): chỉ giấy phép mở, ghi tác giả; không rõ giấy phép = không dùng (`/dieu-khoan`).

## Quy trình
1. **Quét (chỉ đọc)**: `npx tsx scripts/quet-cau-can-hinh-l10.mts` liệt kê chủ đề; thêm `--chu-de "<regex ASCII, dùng . thay chữ có dấu>"` để xuất JSON. (Terminal tool từ chối lệnh có ký tự không ASCII.) Lớp khác: `--lop 12 --ra hinh-cau-hoi-l12-c4/l12-hat-nhan.json` (đường dẫn tương đối `scripts/data/`). File xuất có thể vài MB → sau khi phân loại chỉ giữ các câu được chọn.
2. **Bộ dò "đã có hình"** — phải đủ 3 loại, thiếu là vẽ trùng (đã gặp 2 lần): `<img>` không `class="eq"` hoặc rộng ≥120px, **`<svg>` nội tuyến**, `<figure>`. Ảnh có alt "Hình…" vẫn là hình thật.
3. **Phân loại** (đặt `l10-…-phan-loai.json`): vẽ được bằng khuôn / cần sơ đồ tay / mơ hồ / thiếu hình gốc.
4. **Vẽ** vào `svg/<id>.svg`. Mỗi id ghi tham số riêng trong bảng của khuôn. Nhãn góc mặc định có thể bịa dữ liệu → đặt `lab=' '` khi đề không cho góc.
5. **Duyệt**: `python3 dung-xem-thu.py` → `xem-thu.html` (đề | hình, 375px hình trên đề). Thầy chọn → `quyet-dinh.json` (`{id: "dung"|"bo"}`). Xem cả sáng/tối.
6. **Ghi** (sau 22h hoặc khi thầy nói chạy ngay; DB chậm giờ học): trong **tab terminal**, từ **repo chính** `/Users/MAC/Projects/thachlab` (worktree chưa link Supabase CLI, `.env.local` chỉ ở repo chính):
   `npx tsx scripts/ghi-hinh-sau-duyet.mts --thu-muc hinh-cau-hoi`
   Script: sao lưu `scripts/logs/hinh-gemini-sao-luu-*.json`, bỏ qua câu đã có `<svg` (chạy lại không nhân đôi), gọi RPC `bank_set_question_figure_svc` (nối hình vào **cuối đề**, cập nhật bản sao trong `exams`). RPC quét mọi đề nên ~2 phút/câu: 57 câu ≈ 2 giờ, chạy nền và theo dõi bằng `read_terminal`.
7. **Kiểm**: `npx tsx scripts/kiem-hinh-da-ghi.mts hinh-cau-hoi` → mỗi id đúng 1 `<svg`, "sai số hình: 0". Mở thử 1–2 câu trên web (KaTeX + hình).
8. Hình ghi nhầm/nhân đôi: khôi phục từ file sao lưu bằng SQL giao dịch (tắt `trg_exams_sync_bank`, sửa `question_bank` + `content_hash`, hoàn `exams`, bật lại trigger, đếm dòng) — mẫu `scripts/logs/khoi-phuc-339825.sql`. Phải được thầy cho phép trước khi chạy.

## Việc chưa làm / giới hạn
- Hình đang nằm **dưới đề**, chưa "kế bên" như thầy muốn — cần đổi UI hiển thị câu hỏi (đọc `docs/QUY-TAC-THIET-KE.md`, chụp 375px).
- Chương L10 còn 109 câu hệ vật nối dây + 14 câu ròng rọc mơ hồ, 5 câu "như hình vẽ" thiếu hình.

## Nhật ký rút kinh nghiệm
- 2026-10-29 · Bộ dò hình ban đầu bỏ sót `<svg>` nội tuyến → vẽ trùng #339825 phải khôi phục → dò đủ img + svg + figure trước khi vẽ, ghi xong chạy `kiem-hinh-da-ghi.mts`.
- 2026-10-29 · Ảnh có alt "Hình…" bị loại nhầm khỏi "đã có hình" → 4 câu vẽ trùng; xoá và lọc lại.
- 2026-10-29 · Nhãn góc/độ dài mặc định của khuôn bịa số liệu đề không cho → `lab=' '`; nhãn L đè hình (#1538687) → đặt trong tam giác.
- 2026-10-29 · `supabase … --linked` báo "Cannot find project ref" trong worktree → chạy từ repo chính bằng đường dẫn tuyệt đối.
- 2026-10-29 · RPC ghi hình ~2 phút/câu giờ học → báo thầy trước, chọn chạy ngay hoặc chờ 22h.
- 2026-10-29 · L12 Ch.4 Hạt nhân: 1.994 câu, 197 đã có hình, chỉ 5 câu thật sự cần (đồ thị N–t, đường cong Wlk/A ×3, cảm biến khói); 14/19 khớp từ khoá là nhầm ("hình cầu", "hình thành") → lọc từ khoá xong phải đọc từng câu; câu "tia nào không lệch trong điện trường" không vẽ vì hình lộ đáp án.
