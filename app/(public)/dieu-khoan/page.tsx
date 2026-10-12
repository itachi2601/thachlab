import type { Metadata } from "next";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import { CONTACT } from "@/lib/contact";

export const metadata: Metadata = {
  title: "Điều khoản sử dụng & Bản quyền",
  description:
    "Quyền sở hữu nội dung ThachLab, quyền và giới hạn của người học, cách ghi nguồn đề bài và cách báo vi phạm bản quyền.",
  alternates: { canonical: "/dieu-khoan" },
};

// Ngày cập nhật: sửa nội dung trang thì sửa dòng này cùng lúc.
const UPDATED = "12/10/2026";

// Thời hạn xử lý khiếu nại — một chỗ duy nhất để đổi.
const TAKEDOWN_DAYS = 5;

const h2 = "mt-10 font-display text-xl font-bold text-ink scroll-mt-28";
const p = "mt-3 text-base leading-relaxed text-ink";
const ul = "mt-3 list-disc space-y-2 pl-6 text-base leading-relaxed text-ink marker:text-muted";

export default function DieuKhoanPage() {
  const mail = CONTACT.email;
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-2xl px-4 pt-28 pb-20">
        <h1 className="font-display text-3xl font-bold text-ink">Điều khoản sử dụng &amp; Bản quyền</h1>
        <p className="mt-2 text-sm text-muted">Cập nhật {UPDATED}</p>
        <p className={p}>
          Khi tạo tài khoản hoặc dùng ThachLab, bạn đồng ý với các điều dưới đây. Trang này viết ngắn để học sinh và
          phụ huynh đọc được hết.
        </p>

        <nav aria-label="Mục lục" className="mt-6 rounded-2xl border border-line bg-panel p-4">
          <ul className="space-y-1 text-base">
            {[
              ["#so-huu", "1. Quyền sở hữu của ThachLab"],
              ["#nguoi-hoc", "2. Quyền và giới hạn của người học"],
              ["#nguon", "3. Ghi nguồn đề bài"],
              ["#vi-pham", "4. Báo vi phạm bản quyền"],
            ].map(([href, label]) => (
              <li key={href}>
                <a href={href} className="inline-flex min-h-11 items-center text-primary underline-offset-2 hover:underline">
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <h2 id="so-huu" className={h2}>1. Quyền sở hữu của ThachLab</h2>
        <p className={p}>
          Thầy Ngô Diệu Thạch là tác giả và giữ bản quyền đối với toàn bộ nội dung do ThachLab tự soạn:
        </p>
        <ul className={ul}>
          <li>Bài giảng lý thuyết, bài tập mẫu, hướng dẫn từng bước và lời giải chi tiết.</li>
          <li>Hình vẽ, sơ đồ, clip, bài viết trên Blog và tin tức do ThachLab biên soạn.</li>
          <li>Mô phỏng, thí nghiệm tương tác và mã nguồn của website.</li>
          <li>Cách tổ chức đề, nhãn chủ đề – dạng bài và hệ thống xếp hạng, danh hiệu.</li>
        </ul>
        <p className={p}>
          Một số thành phần thuộc bên thứ ba (ví dụ mô phỏng PhET của Đại học Colorado Boulder, thư viện mã nguồn mở)
          giữ nguyên giấy phép và quyền tác giả của chủ sở hữu; ThachLab chỉ nhúng hoặc dẫn link tới các thành phần đó.
        </p>

        <h2 id="nguoi-hoc" className={h2}>2. Quyền và giới hạn của người học</h2>
        <p className={p}>Bạn được:</p>
        <ul className={ul}>
          <li>Học, làm bài, xem lời giải và theo dõi kết quả của mình trên ThachLab cho mục đích học tập cá nhân.</li>
          <li>Chụp hoặc ghi chú một phần nhỏ để ôn bài của chính mình.</li>
          <li>Cho phụ huynh xem kết quả của bạn qua tính năng dành cho phụ huynh.</li>
        </ul>
        <p className={p}>Bạn không được:</p>
        <ul className={ul}>
          <li>Chia sẻ tài khoản, mật khẩu hoặc mã lớp cho người khác dùng thay bạn.</li>
          <li>Sao chép, tải hàng loạt, chụp màn hình hàng loạt đề, câu hỏi hoặc lời giải để đăng lại, chia sẻ công khai hoặc bán lại.</li>
          <li>Dùng công cụ tự động (bot, scraper) để thu thập nội dung hoặc làm bài thay.</li>
          <li>Gian lận khi làm bài, can thiệp vào điểm số, xếp hạng hoặc hệ thống.</li>
          <li>Đăng nội dung của ThachLab lên nhóm học, nền tảng khác khi chưa được thầy đồng ý bằng văn bản.</li>
        </ul>
        <p className={p}>
          Vi phạm có thể dẫn tới khoá tài khoản. ThachLab đang trong giai đoạn thử nghiệm và có thể thay đổi, tạm
          ngừng hoặc gỡ một phần nội dung khi cần.
        </p>

        <h2 id="nguon" className={h2}>3. Ghi nguồn đề bài</h2>
        <p className={p}>
          Đề và câu hỏi trên ThachLab có hai loại. Phân biệt như sau:
        </p>
        <ul className={ul}>
          <li>
            <strong>Do thầy tự soạn hoặc biên soạn lại:</strong> thuộc bản quyền ThachLab theo mục 1.
          </li>
          <li>
            <strong>Trích hoặc phỏng theo đề của kỳ thi chính thức, đề của sở/trường, sách giáo khoa, sách tham khảo:</strong>{" "}
            quyền tác giả thuộc đơn vị ra đề hoặc nhà xuất bản. ThachLab chỉ dùng với mục đích giảng dạy, không thương mại,
            và ghi rõ nguồn (tên kỳ thi hoặc đơn vị ra đề, năm, mã đề nếu có) trong tên đề hoặc phần ghi chú của câu.
          </li>
        </ul>
        <p className={p}>
          Lời giải đi kèm là của ThachLab, kể cả khi đề gốc thuộc bên khác. Nếu bạn thấy một câu hỏi thiếu nguồn hoặc
          ghi sai nguồn, dùng nút <strong>Báo lỗi / Góp ý</strong> trên trang làm bài hoặc báo theo mục 4; thầy sẽ bổ sung
          hoặc gỡ câu đó.
        </p>

        <h2 id="vi-pham" className={h2}>4. Báo vi phạm bản quyền</h2>
        <p className={p}>
          Nếu bạn là tác giả, nhà xuất bản hoặc đại diện của chủ sở hữu và cho rằng nội dung trên ThachLab xâm phạm
          quyền của mình, vui lòng gửi thông báo tới{" "}
          {mail ? (
            <a href={`mailto:${mail}?subject=${encodeURIComponent("[ThachLab] Báo vi phạm bản quyền")}`} className="font-semibold text-primary underline underline-offset-2">
              {mail}
            </a>
          ) : (
            "email liên hệ của ThachLab"
          )}{" "}
          với tiêu đề <strong>[ThachLab] Báo vi phạm bản quyền</strong>, gồm:
        </p>
        <ul className={ul}>
          <li>Họ tên, đơn vị và cách liên lạc với bạn.</li>
          <li>Mô tả tác phẩm bạn sở hữu quyền (tên sách, kỳ thi, năm xuất bản…).</li>
          <li>Đường dẫn (URL) tới nội dung bị cho là vi phạm trên ThachLab.</li>
          <li>Tài liệu hoặc căn cứ cho thấy bạn là chủ sở hữu hoặc người được uỷ quyền.</li>
          <li>Cam kết rằng thông tin trong thông báo là chính xác.</li>
        </ul>
        <p className={p}>
          ThachLab sẽ phản hồi trong vòng {TAKEDOWN_DAYS} ngày làm việc. Nội dung có căn cứ sẽ được gỡ hoặc sửa (bổ
          sung ghi nguồn, thay bằng câu tự soạn) ngay khi xác minh xong. Thông báo cố ý sai sự thật có thể bị từ chối.
        </p>
        <p className={p}>
          Các quy định trên được hiểu theo pháp luật Việt Nam về sở hữu trí tuệ.
        </p>
      </main>
      <Footer />
    </>
  );
}
