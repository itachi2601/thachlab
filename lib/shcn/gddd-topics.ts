// Chủ đề GDĐĐ & PTNN dùng cho phần "Tự đọc thêm" của thẻ sinh hoạt tuần.
//
// Mỗi buổi SHCN chỉ dạy 1–2 trọng tâm của một chủ đề; phần còn lại của chủ đề để sinh viên tự
// đọc. Danh sách mục con vì vậy là dữ liệu tĩnh, không lưu lặp trong từng dòng
// homeroom_weekly_sessions.
//
// QUAN TRỌNG: chỉ điền vào đây những mục con đọc được từ tài liệu gốc. Chủ đề nào chưa có đủ
// danh sách thì để `complete: false` — giao diện sẽ không hiện dòng "Tự đọc thêm" thay vì bịa
// ra các mục sinh viên không hề có trong tài liệu. Khi bổ sung đủ mục con của một chủ đề, thêm
// vào `items` rồi đổi `complete: true`.
//
// Tên trọng tâm ghi trong biên bản tuần (ethics_taught) nên trùng tên mục con ở đây thì phần
// "Tự đọc thêm" mới trừ đúng; so khớp bỏ dấu và chấp nhận một bên chứa bên kia, nên
// "An toàn giao thông" hay "Chuyên đề an toàn giao thông" đều khớp.

export interface GdddTopic {
  /** Số chủ đề trong chương trình (1–12). */
  id: number;
  /** Tên hiển thị, khớp cách ghi trong biên bản: "Chủ đề 2: Kỹ năng sống". */
  title: string;
  /** Các mục con (trọng tâm) của chủ đề. */
  items: string[];
  /** true khi `items` đã đủ toàn bộ mục con của chủ đề — điều kiện để tính "phần còn lại". */
  complete: boolean;
}

/**
 * Link thư mục Drive chung cho toàn bộ 12 chủ đề. Đổi bằng NEXT_PUBLIC_GDDD_DOCS_URL trong
 * .env.local nếu thầy/cô chuyển thư mục. Khi nào mỗi chủ đề có link riêng thì chuyển sang bảng
 * map chu_de_id → url, chưa cần lúc này.
 */
export const GDDD_DOCS_URL =
  process.env.NEXT_PUBLIC_GDDD_DOCS_URL ??
  "https://drive.google.com/drive/u/2/folders/1Tkf3m_yF-ztZADp3T_wcthabV0oc-PaM";

/**
 * 12 chủ đề của môn (theo bảng "Các chủ đề Môn học Giáo dục đạo đức và Phát triển nghề nghiệp"),
 * mục con lấy từ đề mục cấp 1 của từng file PDF chủ đề trong thư mục tài liệu chung (GDDD_DOCS_URL).
 *
 * Lưu ý khi đối chiếu tài liệu: số "CHỦ ĐỀ" in trong ruột vài file PDF không khớp số thứ tự chủ đề
 * (vd file "3. 5S va tac phong cong nghiep.pdf" ghi "CHỦ ĐỀ 8") — đó là dấu vết của bản chương
 * trình cũ. Số dùng ở đây theo bảng 12 chủ đề hiện hành, cũng là số đầu tên file.
 *
 * Bốn chủ đề còn `complete: false`: "Sinh hoạt đầu khóa" và chủ đề 1 (thư mục chưa có tài liệu
 * riêng — file "1. Tai lieu long ghep Ky nang mem.pdf" là tài liệu tư vấn chung cho giáo viên),
 * chủ đề 4 (chưa có file), chủ đề 7 (bản PDF đọc được dừng giữa chừng, chưa chắc đã đủ mục).
 */
export const GDDD_TOPICS: GdddTopic[] = [
  { id: 0, title: "Sinh hoạt đầu khóa", items: [], complete: false },
  { id: 1, title: "Chủ đề 1: Giới thiệu", items: [], complete: false },
  {
    id: 2,
    title: "Chủ đề 2: Kỹ năng sống",
    items: [
      "An toàn giao thông",
      "Sinh hoạt tập thể",
      "Quản lý thời gian và tiền bạc",
      "Biết yêu thương",
      "Facebook và các mạng xã hội",
      "Thoát hiểm trong đám cháy",
      "Những điều cần cảnh giác",
      "Các số điện thoại liên lạc cần thiết",
    ],
    complete: true,
  },
  {
    id: 3,
    title: "Chủ đề 3: 5S và tác phong công nghiệp",
    items: ["5S", "Tác phong công nghiệp"],
    complete: true,
  },
  { id: 4, title: "Chủ đề 4: Điều kiện học tiếp và tốt nghiệp", items: [], complete: false },
  {
    id: 5,
    title: "Chủ đề 5: Học tập hiệu quả",
    items: [
      "Khái niệm về học tập",
      "Sự khác biệt giữa học tập ở Cao Thắng và bậc THPT",
      "Các phương pháp học tập hiệu quả",
      "Chuẩn bị tốt cho các kỳ thi",
      "Các phần mềm hỗ trợ học tập",
    ],
    complete: true,
  },
  {
    id: 6,
    title: "Chủ đề 6: Kỹ năng làm việc nhóm",
    items: [
      "Sự cần thiết của kỹ năng làm việc nhóm",
      "Các giai đoạn phát triển của nhóm",
      "Phương pháp đánh giá hoạt động của nhóm",
      "Thực hành làm việc nhóm",
      "Các kỹ năng chung trong tổ chức nhóm",
    ],
    complete: true,
  },
  {
    id: 7,
    title: "Chủ đề 7: Kỹ năng lập kế hoạch",
    items: [
      "Vai trò của kỹ năng lập kế hoạch trong học tập và công việc",
      "Phương pháp xác định nội dung công việc",
    ],
    complete: false,
  },
  {
    id: 8,
    title: "Chủ đề 8: Kỹ năng giải quyết vấn đề",
    items: [
      "Giải quyết vấn đề và nhiệm vụ của người kỹ sư thực hành",
      "Các bước cơ bản để giải quyết vấn đề",
      "Các công cụ và phương pháp giải quyết vấn đề",
    ],
    complete: true,
  },
  {
    id: 9,
    title: "Chủ đề 9: Đạo đức nghề nghiệp",
    items: [
      "Đạo đức và pháp luật",
      "Các chuẩn mực đạo đức nghề nghiệp",
      "Các chuẩn mực đạo đức nghề nghiệp cơ bản của kỹ sư thực hành",
    ],
    complete: true,
  },
  {
    id: 10,
    title: "Chủ đề 10: Trường học và doanh nghiệp",
    items: ["Trường học và doanh nghiệp khác nhau như thế nào", "Thích nghi với môi trường doanh nghiệp"],
    complete: true,
  },
  {
    id: 11,
    title: "Chủ đề 11: Giao tiếp trong kỹ thuật",
    items: [
      "Tầm quan trọng trong giao tiếp kỹ thuật",
      "Viết trong kỹ thuật",
      "Giao tiếp bằng lời nói (thuyết trình)",
      "Giao tiếp bằng biểu đồ, bảng biểu",
      "Làm sao để đạt hiệu quả cao trong giao tiếp",
    ],
    complete: true,
  },
  {
    id: 12,
    title: "Chủ đề 12: Kỹ năng tìm việc làm và ứng tuyển",
    items: ["Tìm việc làm", "Ứng tuyển", "Phỏng vấn ứng tuyển", "Thực hành tìm việc và phỏng vấn ứng tuyển"],
    complete: true,
  },
];

/** Bỏ dấu + hạ chữ thường để so khớp tên trọng tâm không phụ thuộc cách gõ. */
function normalize(value: string) {
  return value.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/\s+/g, " ").trim();
}

/** Bỏ phần "Chủ đề N:" để so tên thuần, vì biên bản có lúc chỉ ghi tên chủ đề. */
function bareTitle(value: string) {
  return normalize(value.replace(/^\s*ch[uủ]\s*đ[eề]\s*\d{1,2}\s*[:.\-–]?\s*/i, ""));
}

/** Tìm chủ đề theo nhãn tự do ghi trong biên bản, vd "Chủ đề 2: Kỹ năng sống" → chủ đề id 2. */
export function findGdddTopic(label: string): GdddTopic | null {
  if (!label.trim()) return null;
  const number = Number(label.match(/ch[uủ]\s*đ[eề]\s*(\d{1,2})/i)?.[1] ?? label.match(/^\s*(\d{1,2})\b/)?.[1]);
  if (Number.isFinite(number)) {
    const byNumber = GDDD_TOPICS.find((topic) => topic.id === number);
    if (byNumber) return byNumber;
  }
  const key = bareTitle(label);
  return GDDD_TOPICS.find((topic) => bareTitle(topic.title) === key) ?? null;
}

/**
 * Các mục con của chủ đề chưa dạy trong buổi này — phần "Tự đọc thêm".
 * Rỗng khi chưa biết đủ mục con của chủ đề (tránh gợi ý thiếu/sai cho sinh viên).
 */
export function selfStudyItems(topicLabel: string, taught: string[]): string[] {
  const topic = findGdddTopic(topicLabel);
  if (!topic || !topic.complete) return [];
  const done = taught.map(normalize).filter(Boolean);
  // Biên bản hay ghi gộp ("An toàn giao thông và cảnh giác") hoặc ghi tắt, nên so khớp theo kiểu
  // một bên chứa bên kia thay vì bằng tuyệt đối.
  return topic.items.filter((item) => {
    const key = normalize(item);
    return !done.some((entry) => entry.includes(key) || key.includes(entry));
  });
}
