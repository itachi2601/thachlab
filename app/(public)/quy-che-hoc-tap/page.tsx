import type { Metadata } from "next";
import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";

export const metadata: Metadata = {
  title: "Quy chế học tập & cách dùng website",
  description:
    "Học sinh học thế nào trên ThachLab: việc cần làm trước và sau buổi học, cách làm bài kiểm tra, ôn câu sai, phụ đạo, xếp hạng và những điều cần giữ.",
  alternates: { canonical: "/quy-che-hoc-tap" },
};

// Ngày cập nhật: sửa nội dung trang thì sửa dòng này cùng lúc.
const UPDATED = "16/10/2026";

// Con số trùng với mã nguồn (services/tutoring.ts: WINDOW_QUIZ_*, EXIT_QUIZ_*, REGISTER_*, SLOT_MAX_CAPACITY, EXIT_COOLDOWN_HOURS). Đổi ở đó thì đổi cả ở đây.
const h2 = "mt-10 font-display text-xl font-bold text-ink scroll-mt-28";
const p = "mt-3 text-base leading-relaxed text-ink";
const ul = "mt-3 list-disc space-y-2 pl-6 text-base leading-relaxed text-ink marker:text-muted";

const TOC: [string, string][] = [
  ["#bon-viec", "1. Bốn việc cần nhớ"],
  ["#tren-lop", "2. Trên lớp"],
  ["#hoc-bai", "3. Học một bài trên website"],
  ["#kiem-tra", "4. Làm bài kiểm tra"],
  ["#cau-sai", "5. Ôn câu đã sai"],
  ["#phu-dao", "6. Phụ đạo"],
  ["#xep-hang", "7. Điểm RP và xếp hạng"],
  ["#tai-khoan", "8. Tài khoản và dữ liệu của em"],
];

export default function QuyCheHocTapPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto min-h-screen w-full max-w-2xl px-4 pb-20 pt-28">
        <h1 className="font-display text-3xl font-bold text-ink">Quy chế học tập &amp; cách dùng website</h1>
        <p className="mt-2 text-sm text-muted">Cập nhật {UPDATED}</p>
        <p className={p}>
          Trang này nói em cần làm gì để học tốt ở lớp thầy và dùng ThachLab thế nào cho đỡ mất công. Viết ngắn, đọc một lần là nhớ.
        </p>

        <section id="bon-viec" className="mt-10 scroll-mt-28 rounded-2xl border border-primary/30 bg-primary-soft p-5">
          <h2 className="font-display text-xl font-bold text-ink">1. Bốn việc cần nhớ</h2>
          <ol className="mt-3 list-decimal space-y-2 pl-6 text-base leading-relaxed text-ink marker:font-semibold">
            <li>Trước buổi: đọc lý thuyết bài sắp học, trả lời câu dự đoán.</li>
            <li>Trên lớp: mang bài tập về nhà để trợ giảng kiểm.</li>
            <li>Sau buổi: làm bài luyện tập của bài.</li>
            <li>Mỗi ngày: ôn các câu đã sai khi website báo đến hạn.</li>
          </ol>
          <p className="mt-3 text-sm text-muted">Việc nào trong ngày, website đã gợi sẵn ở thẻ “Việc hôm nay” của trang chủ học sinh.</p>
        </section>

        <nav aria-label="Mục lục" className="mt-8 rounded-2xl border border-line bg-panel p-4">
          <ul className="space-y-1 text-base">
            {TOC.map(([href, label]) => (
              <li key={href}>
                <a href={href} className="inline-flex min-h-11 items-center text-primary underline-offset-2 hover:underline">
                  {label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <h2 id="tren-lop" className={h2}>2. Trên lớp</h2>
        <ul className={ul}>
          <li>Mỗi 20 em có một trợ giảng đi cùng thầy.</li>
          <li>10 phút đầu buổi, trợ giảng kiểm bài tập về nhà của cả lớp và ghi lỗi cụ thể lên bài của em.</li>
          <li>Em không làm bài hai buổi liên tiếp thì thầy sẽ hỏi riêng em.</li>
          <li>Khi cả lớp làm bài, trợ giảng đi từng bàn. Trợ giảng gợi ý để em tự làm, không đọc lời giải cho em chép. Em cứ hỏi, đừng ngại.</li>
          <li>Trợ giảng không bàn điểm số hay năng lực của một em trước các em khác.</li>
        </ul>

        <h2 id="hoc-bai" className={h2}>3. Học một bài trên website</h2>
        <p className={p}>Mỗi bài đi theo thứ tự này. Làm đủ thứ tự thì nhớ lâu hơn là đọc lại nhiều lần.</p>
        <ul className={ul}>
          <li><b>Lý thuyết:</b> đọc từng mục, trả lời câu dự đoán trước khi xem đáp án, làm câu kiểm tra nhanh ngay sau mỗi mục. Trả lời sai sẽ có giải thích vì sao sai.</li>
          <li><b>Bài tập mẫu:</b> làm theo từng bước, tự điền trước rồi mới xem gợi ý.</li>
          <li><b>Luyện tập:</b> làm một mình. Làm lại được, nhưng RP của bài chỉ tính lần đầu.</li>
          <li><b>Học dở thì quay lại đúng chỗ:</b> bấm “Tiếp tục học” ở trang chủ hoặc trang lớp.</li>
        </ul>

        <h2 id="kiem-tra" className={h2}>4. Làm bài kiểm tra</h2>
        <ul className={ul}>
          <li>Bài kiểm tra mở lúc nào, thầy báo qua chuông thông báo. Quét mã QR trên bảng hoặc bấm link thì em vẫn phải đăng nhập, đăng nhập xong sẽ vào đúng bài.</li>
          <li>Câu hỏi có nhãn như đề thi thật: A. B. C. D.; ý a) b) c) d) chọn Đúng hoặc Sai; phần cuối ghi đáp số.</li>
          <li>Bài được lưu tiến độ tự động, mất mạng hay tắt trang thì mở lại làm tiếp.</li>
          <li>Website ghi nhận khi em rời khỏi màn hình bài thi hoặc thoát toàn màn hình. Bài không tự nộp, nhưng thầy và trợ giảng xem được. Rời nhiều lần thì thầy sẽ hỏi lại kiến thức của em.</li>
          <li>Làm bài một mình, bằng sức mình.</li>
        </ul>

        <h2 id="cau-sai" className={h2}>5. Ôn câu đã sai</h2>
        <ul className={ul}>
          <li>Câu em làm sai được gom vào “Kho câu sai”. Website nhắc ôn theo lịch cách quãng: ôn đúng lúc sắp quên thì nhớ lâu hơn ôn dồn một lần.</li>
          <li>Mỗi lần ôn chỉ vài câu, vào phần Luyện tập để làm.</li>
          <li>Ôn đúng thì câu đó được gỡ khỏi kho. Đây là cách nhanh nhất để thôi mắc lại cùng một lỗi.</li>
        </ul>

        <h2 id="phu-dao" className={h2}>6. Phụ đạo</h2>
        <p className={p}>Phụ đạo là kèm nhóm nhỏ để lấp đúng chỗ em còn hổng, không phải phạt.</p>
        <ul className={ul}>
          <li><b>Khi nào em được xếp:</b> trong 2 bài gần nhất, em sai từ một nửa số câu của một chủ đề (tối thiểu 3 câu). Chủ đề đó hiện ở trang chủ học sinh với trạng thái “Đang mở khoá”.</li>
          <li><b>Đặt chỗ:</b> chọn 1 đến 3 chủ đề rồi đăng ký buổi. Đăng ký chốt trước giờ học 6 tiếng. Mỗi buổi tối đa 4 em. Buổi đầy thì vào hàng chờ, có bạn huỷ là được xếp vào.</li>
          <li><b>Trong buổi:</b> trợ giảng dò bài cũ, mỗi em được hỏi ít nhất một lần.</li>
          <li><b>Bài cuối buổi:</b> 10 câu, mở 20 phút, đạt từ 70%. Em tự đăng nhập tài khoản của mình để làm, không dùng tài khoản hay máy của bạn.</li>
          <li><b>Tự kiểm tra ở nhà để mở khoá chủ đề:</b> 20 câu, đạt từ 80%. Chưa đạt thì chưa sao, ôn lại lý thuyết của đúng chủ đề đó, sau 24 giờ thử lượt mới.</li>
          <li><b>Chủ đề tự mở khoá</b> khi bài sau em làm đúng từ 75% phần đó.</li>
          <li>Em vào trễ so với lớp thì làm bài kiểm tra đầu vào ngắn. Kết quả giúp trợ giảng bắt đầu đúng chỗ, không dạy lại phần em đã vững.</li>
        </ul>

        <h2 id="xep-hang" className={h2}>7. Điểm RP và xếp hạng</h2>
        <ul className={ul}>
          <li>RP là điểm kinh nghiệm theo mùa. Em có RP khi làm bài lần đầu đạt điểm tối thiểu, giữ chuỗi mỗi ngày, đủ bài trong tuần và sửa lại chủ đề đã sai.</li>
          <li>Bảng xếp hạng chỉ để em thấy mình đã tiến được bao nhiêu. Em đi chậm hơn bạn cũng không sao, miễn tuần này hơn tuần trước.</li>
          <li>Con số cụ thể của mùa này xem ở mục “Cách tăng RP” trên thẻ “Việc hôm nay” và ở trang Xếp hạng.</li>
        </ul>

        <h2 id="tai-khoan" className={h2}>8. Tài khoản và dữ liệu của em</h2>
        <ul className={ul}>
          <li>Mỗi em một tài khoản riêng. Không cho bạn mượn, không đăng nhập hộ bạn.</li>
          <li>Thầy và trợ giảng xem được kết quả học tập, bài đã làm và các chủ đề em còn hổng để kèm cho đúng.</li>
          <li>Phụ huynh xem được kết quả của em ở <Link href="/phu-huynh" className="font-medium text-primary underline-offset-2 hover:underline">trang dành cho phụ huynh</Link>.</li>
          <li>Gặp lỗi hay câu hỏi sai, bấm nút báo lỗi trên website để thầy sửa.</li>
          <li>Bài giảng và đề trên ThachLab thuộc bản quyền của thầy và các nguồn đã ghi, xem <Link href="/dieu-khoan" className="font-medium text-primary underline-offset-2 hover:underline">Điều khoản &amp; Bản quyền</Link>.</li>
        </ul>

        <div className="mt-10 flex flex-wrap gap-3">
          <Link href="/lop-hoc" className="inline-flex min-h-11 items-center rounded-xl bg-primary px-5 py-3 font-semibold text-white hover:bg-primary-dark">
            Vào lớp học
          </Link>
          <Link href="/tai-khoan" className="inline-flex min-h-11 items-center rounded-xl border border-line px-5 py-3 font-semibold text-ink hover:border-line-strong">
            Trang chủ học sinh
          </Link>
        </div>
      </main>
      <Footer />
    </>
  );
}
