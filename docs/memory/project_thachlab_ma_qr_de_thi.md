---
name: project_thachlab_ma_qr_de_thi
description: "Mã QR cho từng đề — thầy chiếu lên bảng, học sinh quét là vào đúng đề (/quet-ma + ExamQrPanel)"
metadata:
  node_type: memory
  type: project
---

# Mã QR cho từng đề (10/10/2026)

Thầy chốt: soạn đề xong muốn **mỗi đề có một mã QR chiếu lên bảng**, học sinh quét là vào đúng đề
trên thachlab (không phải gõ link). Chọn làm 2 bước, đã xong cả hai, **đã vào main** (commit
`a1a1b6e08` + `d58aeffa8`), chưa deploy, **chưa thử bằng điện thoại thật**.

## Bước 1 — phía thầy
- `components/admin/ExamQrPanel.tsx`: khối QR + link + **Sao chép link** + **Tải ảnh QR** (PNG) +
  nút **“Chiếu lên bảng”** (toàn màn hình, nền trắng, QR lớn, mã đề lớn, Esc để đóng).
- Gắn ở 2 chỗ: `/quan-tri/sua-de` (chọn đề nào là có QR; cảnh báo nếu đề đang là **bản nháp**) và
  `/quan-tri/dang-de` (hiện ngay sau khi bấm Đăng đề).
- QR sinh **tại máy** bằng `qrcode-generator` (cùng gói bản in sách dùng) trong `lib/qr.ts` — không
  gọi dịch vụ ngoài, không thêm request, chạy được với web xuất tĩnh.

## Bước 2 — phía học sinh
- Trang mới `/quet-ma` (`app/quet-ma/`): camera quét + **ô gõ số đề dự phòng**.
- Hai đường giải mã trong `components/scan/QrScannerCard.tsx`: `BarcodeDetector` nếu máy có
  (Chrome/Android), còn lại **tải chậm `jsqr`** — Safari/iOS **chưa bật** `BarcodeDetector` mặc
  định (MDN: Safari 17 để sau cờ, Firefox chưa có), nên thiếu `jsqr` là iPhone không quét được.
  `jsqr` nằm trong chunk async, không vào JS đầu trang.
- Vào từ menu **“Thêm”** ở thanh đáy (HS THPT) và nút **“Quét mã”** ở trang chủ HS
  (`components/dashboard/ThptStudentHome.tsx`).

## Quyết định kỹ thuật đáng nhớ
- **Một chỗ sinh link đề**: `lib/exam-link.ts` (`examTakePath`, `examQrUrl`, `examIdFromScan`) —
  để mã QR và mục quét không lệch nhau khi `/kiem-tra/lam` đổi cách nhận mã đề.
- `examIdFromScan` chỉ nhận `?id=` khi đích là `/kiem-tra/lam` (hoặc query trần `?id=770`). Cố ý
  **không** nhận `?id=` của trang khác: `/lop-hoc/bai/?id=9` là id **bài học**, nhận bừa sẽ mở nhầm
  thành đề số 9. Và **không bao giờ** điều hướng theo nội dung quét được — chỉ lấy số rồi tự dựng
  đường dẫn nội bộ, nên QR giả trỏ ra trang ngoài không dụ được học sinh đi đâu.
- **`RequireAuth` nay giữ `?next=`** (đường dẫn + query): trước đây quét QR lúc chưa đăng nhập thì
  bấm Đăng nhập xong bị thả về trang chủ và **mất luôn mã đề**. Đọc query bằng
  `useSyncExternalStore` (không dùng `useSearchParams`) để mọi trang có `RequireAuth` không phải
  bọc thêm `Suspense`.
- **QR phải nền trắng**: giao diện quản trị nền tối nên QR luôn bọc trong khung sáng có đệm (M5);
  màn chiếu dùng nền sáng chữ tối (M1). Vùng trắng quanh mã 4 ô (chuẩn QR) — ít hơn thì máy ảnh khó
  bắt góc.

## Kiểm chứng (bắt buộc, vì QR sai thì im lặng)
- `npx tsx scripts/kiem-qr.mts` — dựng ảnh bitmap từ **đúng** `lib/qr.ts` rồi **giải mã lại** bằng
  `jsqr`, đối chiếu chuỗi gốc (4/4 ca đúng). Mã QR sai không có lỗi build nào báo, chỉ tới lúc học
  sinh giơ máy mới biết.
- Parser mã đề: 15/15 ca (kể cả ca bẫy `?id=` của trang bài học).
- `tsc` + `eslint` sạch, `next build` ra 88→89 trang tĩnh.

## Còn treo
- Thử thật trên **iPhone + Android** với tài khoản học sinh (camera quét trong app là thứ duy nhất
  chưa kiểm bằng máy thật).
- QR cho đề **CNC** (`CncExamComposer`) và cho trang đăng bài học (`LessonImporter`) — chưa làm.
