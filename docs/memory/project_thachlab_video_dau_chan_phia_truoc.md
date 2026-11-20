---
name: project_thachlab_video_dau_chan_phia_truoc
description: Clip nền sân khấu "Dấu chân phía trước" (120 năm CĐ Kỹ thuật Cao Thắng) — bản 4 xong 2026-11-04, chờ thầy duyệt
metadata:
  type: project
---

**Mục tiêu:** clip nền chiếu sau tiết mục hát "Dấu chân phía trước" (Phạm Minh Tuấn), 20 người. Nội dung: hành trình ra đi tìm đường cứu nước, lồng cảnh trường Cơ khí Á Châu, nay là CĐ Kỹ thuật Cao Thắng. Dịp kỷ niệm 120 năm thành lập trường (1906–2026). Clip chỉ dùng nội bộ.

**Nơi lưu (KHÔNG có trong git):**
- Thư mục: `/Users/MAC/Projects/thachlab/.claude/worktrees/video-montage-dau-chan-bef97e/video-dau-chan/`, nặng 1,1 GB, bị loại khỏi git bằng `.git/info/exclude`.
- Dọn worktree là mất hết, nên phải chép thư mục ra ngoài trước khi dọn.
- `nguon/`: 4 video YouTube gốc:
  - `100YSLR08J4`: VTV9
  - `D-HAd5uAr2A`: VTV1
  - `IjryYnuWsZo`: THVL
  - `i7QY8Kmeg2E`: karaoke, vừa là nguồn nhạc vừa là nguồn dải lời
- `xem/kk/*.json`: danh sách đoạn cắt cảnh chính xác.
- `xem/kk/cham_*.jsonl`: điểm chấm từng đoạn, kèm lý do loại.
- Script:
  - `build.py`: dựng clip từ `plan.json`.
  - `kichban3.py`: kịch bản hiện hành, sinh ra `plan.json`.
- Thành phẩm:
  - `Dau-chan-phia-truoc_nen_1080p.mp4`: 341,5 s, 296 MB.
  - `xem-thu-dien-thoai.mp4`: 28 MB, đã gửi thầy.

**Cách dựng lại:** `python3 kichban3.py Dau-chan-phia-truoc_nen_1080p.mp4`, rồi `rm -rf seg`, rồi `/usr/bin/python3 build.py plan.json .`. Chạy trong tab terminal, mất khoảng 10 phút.
- Phải dùng `/usr/bin/python3` vì Pillow nằm ở đó.
- ffmpeg Homebrew không có drawtext, nên mọi chữ đều là ảnh PNG vẽ bằng PIL.

**Quyết định đã chốt (thầy sửa ngày 2026-11-04):**
- Cảnh quay luôn chạy đúng tốc độ thật. Thầy chê cảnh "tua nhanh" ở 0:14.
  - Ảnh tĩnh dùng `freeze`: giữ một khung, đẩy máy chậm.
  - Bỏ các đoạn có chuyển cảnh bên trong: C165, C27 lấy cả đoạn, C08.
- Không cắt khung để bỏ logo VTV/THVL, vì clip chỉ dùng nội bộ.
- Chữ dẫn đặt ở góc trên trái: dòng mốc vàng, tiêu đề trắng, dòng phụ nghiêng.
- Ba Đình ghi "khai sinh nước Việt Nam Dân chủ Cộng hòa", không ghi "Việt Nam mới".
- Lời bài hát: Claude không chép hay gõ lời vì lời có bản quyền.
  - Thay vào đó cắt dải lời của chính video karaoke (`crop 1280:220:0:460`), đặt ô nhỏ ở góc dưới phải.
  - Thời gian karaoke = thời gian clip + 14 s, nên dải lời tự khớp với nhạc.
- Khung kết bắt đầu từ giây nhạc 340,5 (sau câu hát cuối) và giữ 15 s.
  - Nội dung: "CHÀO MỪNG KỶ NIỆM 120 NĂM NGÀY THÀNH LẬP TRƯỜNG CAO ĐẲNG KỸ THUẬT CAO THẮNG 1906 – 2026".
  - Nền là dãy nhà cổ làm mờ.
  - Trong 15 s này nhạc tắt dần, sau đó còn khoảng 12 s im để cả đội xếp 2 hàng chào.
- Tượng ở A39/B43 đã kiểm: Nhà Rồng (có rồng trên mái) và tượng Nguyễn Tất Thành thanh niên, không phải tượng Tôn Đức Thắng.

**Còn chờ:**
- Thầy xem bản 4 và góp ý.
- Câu "Năm 1911 Nguyễn Tất Thành theo học tại trường" lấy theo phóng sự VTV, chưa đối chiếu nguồn sử khác.
- Nếu thầy cần link chia sẻ thì tải lên Drive (hỏi thầy trước).
- Đội hình 20 người, 9 thế, đã trả lời trong chat, không lưu thành file.
