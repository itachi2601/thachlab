import { CONTACT } from "@/lib/contact";

/**
 * Hỏi–đáp cho phụ huynh (P9/P14/P19): mỗi câu là một chỗ phụ huynh 45–60 tuổi hay hiểu sai hoặc
 * phải nhắn hỏi thầy — trả lời ngay trên trang để bớt một tin nhắn và để phụ huynh biết số liệu
 * này là số liệu gì (hiểu sai nguồn điểm là mất tin, không phải mất tính năng).
 *
 * Dùng <details> gốc của trình duyệt: bàn phím + trình đọc màn hình đã hỗ trợ sẵn, không JS,
 * không tự mở, không che nội dung (P13).
 */
const QA: { q: string; a: React.ReactNode }[] = [
  {
    q: "Điểm trên đây là điểm gì?",
    a: (
      <>
        Là điểm các bài con làm trên thachlab: bài tập thầy giao và bài kiểm tra định kỳ của lớp
        (giữa kỳ, cuối kỳ, kiểm tra chương) nếu lớp làm trên web. Điểm chính thức của nhà trường do
        nhà trường công bố — phụ huynh đối chiếu thêm sổ điểm của trường.
      </>
    ),
  },
  {
    q: "Bao lâu thì có điểm mới?",
    a: (
      <>
        Bài trắc nghiệm được chấm ngay khi con nộp. Bài có câu tự luận thì thầy chấm tay nên điểm có
        thể tới sau vài ngày.
      </>
    ),
  },
  {
    q: "Sao con tôi chưa có điểm nào?",
    a: (
      <>
        Con chưa làm bài nào trên web, hoặc tài khoản của con chưa được duyệt vào lớp. Phụ huynh nhắn
        Zalo cho thầy để thầy kiểm tra.
      </>
    ),
  },
  {
    q: "Một tài khoản xem được mấy con?",
    a: (
      <>
        Nhiều con. Khi nối từ hai con trở lên, đầu trang có ô <b>Chọn con</b> để đổi qua lại; số liệu
        bên dưới luôn là của con đang chọn.
      </>
    ),
  },
  {
    q: "Con có xem được trang này không?",
    a: (
      <>
        Con có trang riêng của mình với cùng số liệu. Trang này là bản dành cho phụ huynh và chỉ đọc —
        phụ huynh không sửa được gì, cũng không thấy điểm của các bạn khác.
      </>
    ),
  },
  {
    q: "Điểm thấp thì thầy xử lý thế nào?",
    a: (
      <>
        Thầy ghi nhận phần con sai và sắp buổi phụ đạo. Mục <b>Phần con đang được phụ đạo</b> cho biết
        đang ở bước nào (chờ sắp lịch · đã có người kèm · đã dạy lại · con đã làm đúng lại).
      </>
    ),
  },
  {
    q: "Muốn ngừng theo dõi thì làm sao?",
    a: <>Nhắn thầy để gỡ liên kết với con. Tài khoản của phụ huynh vẫn còn, chỉ là không xem được nữa.</>,
  },
];

export default function ParentFaq() {
  return (
    <section className="rounded-2xl border border-line bg-panel p-5 sm:p-6">
      <h2 className="font-display text-lg font-bold text-ink">Câu hỏi thường gặp</h2>
      <div className="mt-2 divide-y divide-line">
        {QA.map((item) => (
          <details key={item.q} className="group py-1">
            {/* grid 2 cột cố định (không dùng flex-1) để dấu ⌄ luôn nằm ở cột phải, không bị đẩy
                xuống dòng khi câu hỏi dài — 18px nên câu hỏi thường chiếm 2 dòng ở 375px. */}
            <summary className="grid cursor-pointer list-none grid-cols-[1fr_1.25rem] items-center gap-3 py-2 font-semibold text-ink marker:content-none">
              <span>{item.q}</span>
              <span aria-hidden className="text-center text-muted transition-transform group-open:rotate-180">
                ⌄
              </span>
            </summary>
            <p className="parent-copy pb-3 text-ink">{item.a}</p>
          </details>
        ))}
      </div>
      {CONTACT.zalo && (
        <p className="mt-3 text-muted">
          Chưa thấy câu trả lời?{" "}
          <a
            href={CONTACT.zalo}
            target="_blank"
            rel="noopener noreferrer"
            className="font-semibold text-primary underline-offset-2 hover:underline"
          >
            Nhắn Zalo cho thầy
          </a>
          .
        </p>
      )}
    </section>
  );
}
