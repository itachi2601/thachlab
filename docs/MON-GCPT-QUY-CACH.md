# Môn "Các phương pháp gia công phi truyền thống" (mã `gcpt`) — quy cách soạn bài

Dựng 26/11/2026. Lớp CTTC (SV cao đẳng cơ khí), vào có duyệt. Khung code + migration `20261126140000_lop_gcpt_*` đã có;
12 bài, mỗi bài một chương, `published=false` tới khi thầy duyệt.

## Cách dạy–học–thi của môn (thầy chốt)
- SV **lập nhóm, thuyết trình từng bài**; thầy **tổng kết** sau mỗi bài. Nên bài trên web phục vụ hai việc: (a) nhóm chuẩn bị, (b) thầy chốt kiến thức cho cả lớp.
- **Thi tự luận, chủ yếu trả bài** (hiểu nguyên lý, nêu ưu nhược, giải thích). Trong đề có **1 câu chọn công nghệ gia công cho một chi tiết** (nêu công nghệ, lý do, thông số/điều kiện, vì sao không chọn phương án khác).
- Hệ quả: **không làm bộ 20 câu trắc nghiệm**. Mỗi bài chỉ ≤4 quiz tự kiểm; trọng tâm là câu tự luận mẫu có đáp án + thang điểm.

## Cấu trúc mỗi bài (tab Học) — theo skill `soan-bai-ly-thuyet-tuong-tac`, mẫu cấu trúc thư mục: `content/lesson-samples/cnctm1-bai-7-mat-phang/`
1. **Tình huống mở bài** (một chi tiết/vật liệu mà phay, tiện, khoan không làm nổi) + 1 câu dự đoán.
2. **Phiếu nhóm thuyết trình** (hộp riêng, nhận ra ngay): 6–8 câu hỏi dẫn nhóm PHẢI trả lời; thời lượng 12' nói + 3' hỏi đáp; yêu cầu tối thiểu (1 sơ đồ nguyên lý tự vẽ/trích có nguồn, 1 clip ≤2' hoặc ảnh sản phẩm, 1 ví dụ chi tiết thật); rubric 4 tiêu chí (đúng nguyên lý 40%, ví dụ ứng dụng 25%, so sánh với phương pháp khác 20%, trình bày 15%).
3. **Bản tổng kết của thầy**: nguyên lý (1 hình SVG sơ đồ), cơ chế bóc vật liệu, thiết bị chính, thông số ảnh hưởng, **hộp số liệu điển hình** (khoảng, ghi "tham khảo"), ưu/nhược, ứng dụng, **bẫy hay nhầm**, mục **"Chọn / không chọn khi nào"** (3–5 dòng, nối sang Bài 11).
4. **2 câu tự luận mẫu** kiểu đề thi (1 câu giải thích nguyên lý/so sánh, 1 câu chọn phương pháp cho chi tiết cụ thể) + đáp án mẫu + thang điểm chia ý.
5. Trả bài (tự kiểm 3 dòng).
Tab Bài mẫu: đưa 2 câu tự luận ở mục 4 dưới dạng bài mẫu. Tab Luyện tập: ≤4 câu trắc nghiệm khái niệm nếu cần, không bắt buộc.

## Quy tắc nội dung
- Số liệu kỹ thuật (độ nhám Ra, độ chính xác, tốc độ bóc, áp suất, tần số…) **chỉ ghi dạng khoảng + "giá trị tham khảo"**, đối chiếu ≥2 nguồn; không chắc thì bỏ số, nói định tính. Không chép nguyên văn giáo trình/tài liệu (xem `/dieu-khoan`); hình tự vẽ SVG hoặc ảnh giấy phép mở có ghi tác giả.
- Giọng văn không dùng vai "thầy"; mỗi ý một dòng; công thức dùng KaTeX; thuật ngữ Việt (viết tắt Anh in kèm: EDM, WEDM, ECM, LBM, AWJ…).
- Luôn nhắc **vật liệu nào gia công được/không**, **lớp biến đổi nhiệt/ứng suất dư**, **an toàn** (laser, điện áp cao, chất ăn mòn, tia X của EBM).
- Giữ nhất quán thuật ngữ giữa các bài: "gia công phi truyền thống" = bóc vật liệu không chủ yếu bằng lực cắt của dụng cụ cứng hơn phôi.

## Danh sách 12 bài và ý chính
| Bài | Thư mục | Ý chính |
|---|---|---|
| 1 | `gcpt-bai-1-tong-quan` | Vì sao có phi truyền thống (vật liệu cứng, hình dạng phức tạp, chi tiết nhỏ); phân loại theo dạng năng lượng (cơ, điện–nhiệt, hoá–điện hoá); bảng so sánh sơ bộ; **cách học môn: lập nhóm, lịch thuyết trình, rubric, cách thi** |
| 2 | `gcpt-bai-2-edm` | EDM khuôn chìm: phóng điện, điện môi, điện cực (than chì/đồng), thông số xung (Ton, Toff, dòng), mòn điện cực, lớp tái đúc, ứng dụng khuôn |
| 3 | `gcpt-bai-3-wedm` | Cắt dây: dây, nước khử ion, cắt thô + cắt tinh (skim cut), côn, độ chính xác; so với EDM chìm; ứng dụng dưỡng, khuôn dập |
| 4 | `gcpt-bai-4-ecm` | Hoà tan anode, dung dịch điện phân, khe hở, định luật Faraday (tính tốc độ bóc), không mòn dụng cụ, không HAZ; mài điện hoá/ECDM nhắc ngắn |
| 5 | `gcpt-bai-5-laser` | Nguyên lý, laser CO2/fiber/Nd:YAG, cắt–khoan–hàn–khắc, vùng ảnh hưởng nhiệt, khí trợ, vật liệu phản xạ, an toàn |
| 6 | `gcpt-bai-6-tia-nuoc` | WJM thuần nước vs AWJ hạt mài, áp suất, đầu cắt, độ côn/độ nhám, cắt vật liệu composite/đá/kính, không nhiệt |
| 7 | `gcpt-bai-7-sieu-am` | USM: rung ~20 kHz, bùn hạt mài, vật liệu giòn (kính, gốm, silic), tỷ lệ tạo hình, RUM/hỗ trợ siêu âm nhắc ngắn |
| 8 | `gcpt-bai-8-ebm-plasma` | EBM (chân không, lỗ vi mô, hàn) và cắt plasma (tấm dày, kim loại dẫn điện, độ chính xác thấp), so với laser |
| 9 | `gcpt-bai-9-hoa-hoc` | CHM/PCM: mặt nạ, chất ăn mòn, ăn mòn ngang (undercut), tấm mỏng, mạch/lưới lọc |
| 10 | `gcpt-bai-10-boi-dap-lai` | In 3D kim loại (SLM/DED) khi nào hơn gia công cắt bớt; công nghệ lai (cắt gọt + bồi đắp, EDM + phay) |
| 11 | `gcpt-bai-11-chon-cong-nghe` | **Quy trình 5 bước chọn công nghệ** (vật liệu & dẫn điện → hình học → độ chính xác/Ra → số lượng/chi phí → ràng buộc nhiệt/an toàn); ma trận so sánh tất cả công nghệ; 4–5 chi tiết mẫu có lời giải đủ lý do chọn + lý do loại |
| 12 | `gcpt-bai-12-on-thi` | Cấu trúc đề tự luận, 3 đề mẫu (mỗi đề có 1 câu chọn công nghệ) + đáp án + thang điểm, lỗi SV hay mắc |

## Thao tác kỹ thuật
- Mỗi bài: thư mục `content/lesson-samples/<tên ở bảng>/` với `theory.src.html` (+ `build_figs.py` nếu có hình), `theory.html`, `bundle.json`; quy trình dựng/kiểm như skill `soan-bai-ly-thuyet-tuong-tac` (lint, `validate_bundle.mts`, xem thử 375px). Mẫu thực tế: `cnctm1-bai-*`.
- **Không ghi DB** (migration chờ chạy); chưa có id bài. Khi thầy chạy migration: `upload-lesson.mts … --lesson <id>`.
- Không sửa file chung (STATE.md, run-migrations.sh, services/classes.ts…). Commit theo đường dẫn thư mục bài của mình; push nhánh; báo lại bài nào xong/còn treo.
