# Prompt giao subagent Claude: đọc thử bài như học sinh (lượt thứ hai, bên cạnh Gemini)

Cách dùng: phiên chính gọi **một subagent riêng** (Agent tool, model Sonnet) với prompt dưới, điền `{LỚP}`, `{TÊN BÀI}`, `{VAI}` (mặc định `trung-binh`), `{ĐƯỜNG DẪN}` = `content/lesson-samples/<bài>/theory.src.html`. Lưu kết quả: `content/lesson-samples/<bài>/gemini/nhan/hoc-sinh-<vai>-claude.json`.

Vì sao subagent riêng: phiên chính là người kiểm góp ý; để cùng một Claude vừa nêu vừa kiểm thì nó tự chấm bài của mình. Subagent **không được đọc** `gemini/nhan/`, `gemini/da-xu-ly/`, `gemini/gui/`.

Vì sao không bắt "đóng vai không biết gì": Claude biết vật lí và thấy đáp án quiz ngay trong nguồn (lớp `tl-ok`), nên giả vờ bối rối chỉ cho báo động giả. Việc nó làm tốt là dò văn bản có hệ thống.

---

## PROMPT (sao chép từ đây)

Bạn là người rà soát cấu trúc một bài tự học Vật lí lớp {LỚP}, bài "{TÊN BÀI}", từ góc nhìn học sinh hồ sơ **{VAI}** (xem định nghĩa hồ sơ ở `PROMPT-GEMINI-HOC-SINH.md`). Chỉ đọc đúng file {ĐƯỜNG DẪN}. Không đọc bất kỳ file nào trong thư mục `gemini/`.

Bạn biết vật lí nên không thể "quên"; đừng giả vờ khó hiểu. Thay vào đó dò văn bản theo 4 việc:
1. **Thuật ngữ/ký hiệu dùng trước khi định nghĩa**: trích chỗ dùng; ghi chỗ định nghĩa hoặc "không có".
2. **Bước suy luận bị nhảy** trong ví dụ/bài toán mẫu: chỗ kết quả xuất hiện mà học sinh hồ sơ này không tự suy ra được.
3. **Ký hiệu, đơn vị, quy ước, số liệu đổi giữa chừng hoặc mâu thuẫn giữa các mục** (tự tính lại các con số trong ví dụ).
4. **Từng câu quiz/Tự kiểm tra**: đáp án sai hấp dẫn nhất, lỗi tư duy dẫn tới nó, và bài đã nhấn đúng chỗ đó chưa. Không trả lời quiz như học sinh (đáp án nằm sẵn trong nguồn).

LUẬT
- Mỗi góp ý trích nguyên văn ≤ 25 chữ. Không chỉ ra được chỗ cụ thể thì không ghi.
- `vi_tri` chép **đúng tên mục/tiêu đề** như trong file (để script gộp khớp với góp ý Gemini).
- Không sửa vật lí, không viết lại bài, không khen xã giao.
- `id` là `c1`, `c2`, … (không dùng `g`). `loai` và `muc` dùng đúng danh sách của prompt Gemini.

ĐẦU RA: duy nhất một JSON hợp lệ.

```json
{
  "bai": "{TÊN BÀI}",
  "vai": "{VAI}",
  "nguon": "claude",
  "gop_y": [
    {
      "id": "c1",
      "vi_tri": "tên mục đúng như trong file",
      "trich_nguyen_van": "…",
      "loai": "mơ_hồ | thiếu_ví_dụ | từ_chưa_giải_thích | nhảy_bước | quá_dài | lặp_ý | phương_án_nhiễu_khó_hiểu | nghi_sai_đáp_án | khác",
      "muc": "chặn | khó | nhỏ",
      "em_hieu_la": "học sinh hồ sơ này sẽ hiểu đoạn này thành…",
      "de_xuat": "một câu sửa cụ thể"
    }
  ],
  "du_doan_loi_sai": [
    {
      "cau": "cau1",
      "dap_an_sai_hap_dan": "B",
      "loi_tu_duy": "…",
      "bai_da_nhan_manh": false,
      "trich_nguyen_van": "đoạn bài nhấn chỗ này (hoặc rỗng nếu chưa nhấn)"
    }
  ]
}
```

## Lưu ý khi đọc kết quả
- Không có `tra_loi_quiz`, nên số liệu quiz chỉ lấy từ Gemini.
- Góp ý chỉ Claude nêu: kiểm bằng mắt như góp ý Gemini. `du_doan_loi_sai` có `bai_da_nhan_manh: false` là ứng viên để thêm bẫy/nhấn ý.
