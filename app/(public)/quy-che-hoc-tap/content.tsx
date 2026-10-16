import type { ReactNode } from "react";
import Link from "next/link";

// Nội dung quy chế — MỘT nguồn cho cả bản đọc (cuộn) lẫn bản chiếu lớp (?chieu=1). Sửa chữ ở đây, hai bản cùng đổi.
// Con số trùng với mã nguồn (services/tutoring.ts: WINDOW_QUIZ_*, EXIT_QUIZ_*, REGISTER_*, SLOT_MAX_CAPACITY, EXIT_COOLDOWN_HOURS). Đổi ở đó thì đổi cả ở đây.

// Ngày cập nhật: sửa nội dung thì sửa dòng này cùng lúc.
export const UPDATED = "16/10/2026";

export const PAGE_TITLE = "Quy chế học tập & cách dùng website";
export const PAGE_INTRO =
  "Trang này nói em cần làm gì để học tốt ở lớp thầy và dùng ThachLab thế nào cho đỡ mất công. Viết ngắn, đọc một lần là nhớ.";

const linkCls = "font-medium text-primary underline-offset-2 hover:underline";

export type Section = {
  id: string;
  title: string;
  lead?: string;
  /** Danh sách đánh số (chỉ mục 1) thay vì chấm tròn, và khung nổi bật. */
  ordered?: boolean;
  items: ReactNode[];
  note?: string;
};

export const SECTIONS: Section[] = [
  {
    id: "bon-viec",
    title: "Bốn việc cần nhớ",
    ordered: true,
    items: [
      "Trước buổi: đọc lý thuyết bài sắp học, trả lời câu dự đoán.",
      "Trên lớp: mang bài tập về nhà để trợ giảng kiểm.",
      "Sau buổi: làm bài luyện tập của bài.",
      "Mỗi ngày: ôn các câu đã sai khi website báo đến hạn.",
    ],
    note: "Việc nào trong ngày, website đã gợi sẵn ở thẻ “Việc hôm nay” của trang chủ học sinh.",
  },
  {
    id: "tren-lop",
    title: "Trên lớp",
    items: [
      "Mỗi 20 em có một trợ giảng đi cùng thầy.",
      "10 phút đầu buổi, trợ giảng kiểm bài tập về nhà của cả lớp và ghi lỗi cụ thể lên bài của em.",
      "Em không làm bài hai buổi liên tiếp thì thầy sẽ hỏi riêng em.",
      "Khi cả lớp làm bài, trợ giảng đi từng bàn. Trợ giảng gợi ý để em tự làm, không đọc lời giải cho em chép. Em cứ hỏi, đừng ngại.",
      "Trợ giảng không bàn điểm số hay năng lực của một em trước các em khác.",
    ],
  },
  {
    id: "hoc-bai",
    title: "Học một bài trên website",
    lead: "Mỗi bài đi theo thứ tự này. Làm đủ thứ tự thì nhớ lâu hơn là đọc lại nhiều lần.",
    items: [
      <><b>Lý thuyết:</b> đọc từng mục, trả lời câu dự đoán trước khi xem đáp án, làm câu kiểm tra nhanh ngay sau mỗi mục. Trả lời sai sẽ có giải thích vì sao sai.</>,
      <><b>Bài tập mẫu:</b> làm theo từng bước, tự điền trước rồi mới xem gợi ý.</>,
      <><b>Luyện tập:</b> làm một mình. Làm lại được, nhưng RP của bài chỉ tính lần đầu.</>,
      <><b>Học dở thì quay lại đúng chỗ:</b> bấm “Tiếp tục học” ở trang chủ hoặc trang lớp.</>,
    ],
  },
  {
    id: "kiem-tra",
    title: "Làm bài kiểm tra",
    items: [
      "Bài kiểm tra mở lúc nào, thầy báo qua chuông thông báo. Quét mã QR trên bảng hoặc bấm link thì em vẫn phải đăng nhập, đăng nhập xong sẽ vào đúng bài.",
      "Câu hỏi có nhãn như đề thi thật: A. B. C. D.; ý a) b) c) d) chọn Đúng hoặc Sai; phần cuối ghi đáp số.",
      "Bài được lưu tiến độ tự động, mất mạng hay tắt trang thì mở lại làm tiếp.",
      "Website ghi nhận khi em rời khỏi màn hình bài thi hoặc thoát toàn màn hình. Bài không tự nộp, nhưng thầy và trợ giảng xem được. Rời nhiều lần thì thầy sẽ hỏi lại kiến thức của em.",
      "Làm bài một mình, bằng sức mình.",
    ],
  },
  {
    id: "cau-sai",
    title: "Ôn câu đã sai",
    items: [
      "Câu em làm sai được gom vào “Kho câu sai”. Website nhắc ôn theo lịch cách quãng: ôn đúng lúc sắp quên thì nhớ lâu hơn ôn dồn một lần.",
      "Mỗi lần ôn chỉ vài câu, vào phần Luyện tập để làm.",
      "Ôn đúng thì câu đó được gỡ khỏi kho. Đây là cách nhanh nhất để thôi mắc lại cùng một lỗi.",
    ],
  },
  {
    id: "phu-dao",
    title: "Phụ đạo",
    lead: "Phụ đạo là kèm nhóm nhỏ để lấp đúng chỗ em còn hổng, không phải phạt.",
    items: [
      <><b>Khi nào em được xếp:</b> trong 2 bài gần nhất, em sai từ một nửa số câu của một chủ đề (tối thiểu 3 câu). Chủ đề đó hiện ở trang chủ học sinh với trạng thái “Đang mở khoá”.</>,
      <><b>Đặt chỗ:</b> chọn 1 đến 3 chủ đề rồi đăng ký buổi. Đăng ký chốt trước giờ học 6 tiếng. Mỗi buổi tối đa 4 em. Buổi đầy thì vào hàng chờ, có bạn huỷ là được xếp vào.</>,
      <><b>Trong buổi:</b> trợ giảng dò bài cũ, mỗi em được hỏi ít nhất một lần.</>,
      <><b>Bài cuối buổi:</b> 10 câu, mở 20 phút, đạt từ 70%. Em tự đăng nhập tài khoản của mình để làm, không dùng tài khoản hay máy của bạn.</>,
      <><b>Tự kiểm tra ở nhà để mở khoá chủ đề:</b> 20 câu, đạt từ 80%. Chưa đạt thì chưa sao, ôn lại lý thuyết của đúng chủ đề đó, sau 24 giờ thử lượt mới.</>,
      <><b>Chủ đề tự mở khoá</b> khi bài sau em làm đúng từ 75% phần đó.</>,
      "Em vào trễ so với lớp thì làm bài kiểm tra đầu vào ngắn. Kết quả giúp trợ giảng bắt đầu đúng chỗ, không dạy lại phần em đã vững.",
    ],
  },
  {
    id: "xep-hang",
    title: "Điểm RP và xếp hạng",
    items: [
      "RP là điểm kinh nghiệm theo mùa. Em có RP khi làm bài lần đầu đạt điểm tối thiểu, giữ chuỗi mỗi ngày, đủ bài trong tuần và sửa lại chủ đề đã sai.",
      "Bảng xếp hạng chỉ để em thấy mình đã tiến được bao nhiêu. Em đi chậm hơn bạn cũng không sao, miễn tuần này hơn tuần trước.",
      "Con số cụ thể của mùa này xem ở mục “Cách tăng RP” trên thẻ “Việc hôm nay” và ở trang Xếp hạng.",
    ],
  },
  {
    id: "tai-khoan",
    title: "Tài khoản và dữ liệu của em",
    items: [
      "Mỗi em một tài khoản riêng. Không cho bạn mượn, không đăng nhập hộ bạn.",
      "Thầy và trợ giảng xem được kết quả học tập, bài đã làm và các chủ đề em còn hổng để kèm cho đúng.",
      <>Phụ huynh xem được kết quả của em ở <Link href="/phu-huynh" className={linkCls}>trang dành cho phụ huynh</Link>.</>,
      "Gặp lỗi hay câu hỏi sai, bấm nút báo lỗi trên website để thầy sửa.",
      <>Bài giảng và đề trên ThachLab thuộc bản quyền của thầy và các nguồn đã ghi, xem <Link href="/dieu-khoan" className={linkCls}>Điều khoản &amp; Bản quyền</Link>.</>,
    ],
  },
];
