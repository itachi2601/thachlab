# Bản dịch bộ tài liệu WorldSkills 2026 — Skill 01 Industrial Mechanics

Mục đích: dùng để **huấn luyện** sinh viên dự thi, không phải bản dịch hành chính. Bố cục theo thứ tự sinh viên cần đọc.

## Cấu trúc

```
dich/
├── README.md                         ← file này: mục lục, cách dùng
├── 00-dung-chung/
│   ├── thuat-ngu.md                  ← bảng thuật ngữ Anh–Việt + quy ước dịch (đọc trước)
│   ├── loi-ban-goc.md                ← lỗi trong bản gốc, cách chú thích
│   └── nguon-text/                   ← text trích từ PDF/xlsx (pdftotext), để dịch, không phát cho SV
├── 01-bac1-de-thi-va-thang-diem/     ← SV cầm hàng ngày (song ngữ)
│   ├── 00-tong-quan-de-thi.md        ← 4 module, 20 giờ, trọng số điểm, luật trừ điểm, điểm ký xác nhận
│   ├── 01-module-A1-bao-tri-du-doan.md
│   ├── 02-module-A2-sua-loi-fluidsim.md
│   ├── 03-module-B-han-va-lay-dau.md
│   ├── 04-module-C-tien-phay.md
│   ├── 05-module-D-lap-rap-van-hanh.md
│   ├── 06-ban-ve-chu-giai.md         ← chú giải ghi chú bản vẽ, BOM, mã vít, vật liệu (không vẽ lại)
│   ├── 07-so-do-khi-nen.md           ← chuỗi hoạt động, mã tham chiếu, danh sách linh kiện, danh sách ống
│   ├── 08-thang-diem-song-ngu.csv    ← toàn bộ Aspect, 2 cột EN/VI, nhập lại xlsx được
│   ├── kiem-tra-csv.py               ← python3 kiem-tra-csv.py <tsv nguồn> <csv>: đối chiếu điểm/số đo với xlsx gốc
│   └── phieu-tu-cham/                ← mỗi tiêu chí A..G một phiếu checklist in A4 cho SV tự chấm
├── 02-bac2-technical-description/    ← cho giáo viên huấn luyện
│   ├── 01-muc-1-2-mo-ta-nghe-va-WSOS.md
│   ├── 02-muc-4-cach-cham-va-tru-diem.md
│   ├── 03-muc-5.3-yeu-cau-thiet-ke-de.md
│   ├── 04-muc-7-PPE.md
│   └── 05-muc-9-luat-rieng-nghe.md
└── 03-bac3-tom-tat/                  ← tóm tắt 1 trang, không dịch nguyên văn
    ├── may-phay-M5-thong-so.md
    ├── statement-of-validation.md
    └── danh-muc-file-goc.md          ← file nào trùng, file nào bỏ qua, vì sao
```

## Quy ước (bắt buộc với mọi file)

1. Song ngữ: tiếng Việt kèm thuật ngữ Anh trong ngoặc lần đầu; bảng hai cột EN | VI. Dùng đúng `00-dung-chung/thuat-ngu.md`.
2. Giữ nguyên số liệu, dấu chấm thập phân, mã chi tiết, mã linh kiện, mã tham chiếu, tên tiêu chuẩn.
3. Lỗi bản gốc: dịch nguyên + `[Ghi chú dịch: …]`, liệt kê cuối file trong mục "Ghi chú bản gốc". Không sửa im lặng.
4. Mỗi file bậc 1 mở đầu bằng khối "Dùng để huấn luyện": điểm tối đa của phần này, điểm dễ lấy, bẫy mất điểm (sign-off, nộp đúng giờ, an toàn).
5. Thuật ngữ mới chưa có trong bảng: thêm vào cuối `thuat-ngu.md` (chỉ thêm dòng, không sắp xếp lại).

## Trạng thái

Hoàn thành 1/11/2026 (bậc 1, 2, 3). Thang điểm CSV đã đối chiếu 198/198 mục, tổng 100.0. Lỗi bản gốc đã ghi #1–#19 trong `00-dung-chung/loi-ban-goc.md`. Chưa có ai soát lại bằng mắt — việc tiếp theo là kỹ sư cơ khí đọc bậc 1 (ưu tiên 04-module-C, 06-ban-ve-chu-giai, phiếu C/D) trước khi in cho sinh viên.

## Dùng cho đào tạo

| Giai đoạn | Đọc gì |
|---|---|
| 0. Nền tảng (2–3 tuần) | 01/00-tong-quan, 01/06-ban-ve-chu-giai, 02/04-PPE, 02/05-luat-rieng-nghe |
| 1. Kỹ năng đơn lẻ (6–8 tuần) | 01/03, 01/04, 01/07 + phiếu tự chấm B, C, E |
| 2. Tích hợp (4 tuần) | 01/05, 01/01, 01/02 + phiếu D, F, G, A |
| 3. Thi thử 20 giờ | 08-thang-diem-song-ngu.csv để người đóng vai Expert chấm |

## Sổ tay web (artifact tra cứu)

`so-tay-industrial-mechanics-2026.html` — một file, mở bằng trình duyệt (cần mạng để tải font và thư viện marked): 8 tab Tổng quan · Module đề thi · Thang điểm (tìm kiếm, lọc theo tiêu chí, bật/tắt tiếng Anh) · Phiếu tự chấm (tick ô, chọn mức 0–3, tự cộng điểm, lưu trong trình duyệt) · Thuật ngữ · Bản vẽ & khí nén · Giáo viên (TD) · Ghi chú bản gốc. Bản đăng: https://claude.ai/artifact/MhNpd88AeV1A67tS3iesMz (riêng tư, cần Share mới mở được).
Sửa file .md/.csv xong thì dựng lại: `python3 dung-so-tay.py . so-tay-industrial-mechanics-2026.html`.
