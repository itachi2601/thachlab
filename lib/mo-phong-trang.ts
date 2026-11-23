/**
 * Danh sách mô phỏng tự dựng có trang riêng /mo-phong/<slug>.
 * Nguồn duy nhất: scripts/gen-thu-vien-mo-phong.mts đọc file này sinh thẻ cho /mo-phong,
 * `app/(public)/mo-phong/[slug]/page.tsx` sinh trang, `components/mo-phong/MoPhongTheoSlug.tsx` nạp component.
 * Thêm dụng cụ đo của Gói A (thuoc-kep, panme, dong-ho-da-nang, dong-ho-hien-so): thêm 1 dòng ở đây
 * + 1 dòng trong MoPhongTheoSlug.tsx, rồi chạy `npx tsx scripts/gen-thu-vien-mo-phong.mts`.
 */
export type ChuDeKey = "co" | "nhiet" | "dien" | "song" | "hatnhan" | "do";

export interface MoPhongTrang {
  slug: string;
  ten: string;
  lop: 9 | 10 | 11 | 12;
  chu_de: ChuDeKey;
  /** Dòng "Nhìn vào:" trên thẻ (V2). */
  nhin_vao: string;
  /** Mô tả ngắn cho trang + meta. */
  mo_ta: string;
  /** Một nhiệm vụ đo/quan sát cụ thể thay vì "nghịch tự do". */
  nhiem_vu: string;
  /** Bài học chứa mô phỏng này (để dẫn học tiếp). */
  lesson_id?: number;
  /** Mô phỏng khoá tới khi học sinh chọn đáp án dự đoán (PredictGate). */
  khoa_doan?: boolean;
  /** Trang tĩnh viết tay riêng (không đi qua [slug]). */
  rieng?: boolean;
}

export const MO_PHONG_TRANG: MoPhongTrang[] = [
  {
    slug: "giao-thoa-am",
    rieng: true,
    ten: "Giao thoa sóng âm bằng hai loa của máy",
    lop: 11,
    chu_de: "song",
    nhin_vao: "Chỗ nào to, chỗ nào nhỏ khi dịch đầu sang ngang?",
    mo_ta: "Phát âm đơn sắc ra hai loa trái/phải của máy, xem bản đồ vân giao thoa và tự nghe chỗ to chỗ nhỏ.",
    nhiem_vu: "",
  },
  {
    slug: "khi-ly-tuong",
    khoa_doan: true,
    ten: "Khí lí tưởng: p, V, T cùng lúc",
    lop: 12,
    chu_de: "nhiet",
    nhin_vao: "Giữ T cố định, nén thể tích thì áp suất đổi ra sao?",
    mo_ta: "Chọn quá trình đẳng nhiệt, đẳng tích hoặc đẳng áp rồi kéo điểm trạng thái; ba đồ thị p–V, p–T, V–T cập nhật cùng lúc.",
    nhiem_vu: "Đoán trước rồi kéo điểm: đường nào trên đồ thị V–T là quá trình đẳng áp?",
  },
  {
    slug: "hat-trong-tu-truong",
    khoa_doan: true,
    ten: "Hạt mang điện trong từ trường đều",
    lop: 12,
    chu_de: "dien",
    nhin_vao: "Đổi dấu điện tích thì hạt vòng về phía nào, bán kính đổi ra sao?",
    mo_ta: "Đổi vận tốc, cảm ứng từ, điện tích và khối lượng để thấy quỹ đạo tròn, bán kính và chu kì thay đổi thế nào.",
    nhiem_vu: "Tăng gấp đôi vận tốc: bán kính đổi bao nhiêu lần, chu kì đổi bao nhiêu lần?",
  },
  {
    slug: "can-dong-dien",
    khoa_doan: true,
    ten: "Cân dòng điện đo cảm ứng từ",
    lop: 12,
    chu_de: "dien",
    nhin_vao: "Tăng dòng điện thì số chỉ của cân đổi thế nào?",
    mo_ta: "Nam châm chữ U đặt trên cân, đoạn dây có dòng điện nằm trong khe. Chọn cường độ và chiều dòng, đọc số cân rồi suy ra B.",
    nhiem_vu: "Đọc số cân ở ba giá trị I khác nhau, tự tính B = F/(I·l) rồi so ba kết quả.",
    lesson_id: 12,
  },
  {
    slug: "nem-xien",
    ten: "Ném xiên: kéo và thả",
    lop: 10,
    chu_de: "co",
    nhin_vao: "Góc nào cho tầm xa lớn nhất?",
    mo_ta: "Kéo bệ phóng như kéo ná cao su rồi thả tay; chấm trên quỹ đạo cách nhau đúng 0,1 s.",
    nhiem_vu: "Tìm góc cho tầm xa lớn nhất khi giữ nguyên lực kéo, rồi đối chiếu với 45°.",
  },
  {
    slug: "giao-thoa-song",
    ten: "Giao thoa hai nguồn sóng nước",
    lop: 11,
    chu_de: "song",
    nhin_vao: "Các vân cực đại nằm ở những chỗ nào so với hai nguồn?",
    mo_ta: "Khay sóng hai mũi nhọn: chạm và kéo điểm M, đọc d₂ − d₁ để biết M ở vân cực đại hay cực tiểu.",
    nhiem_vu: "Đặt M ở một vân sáng, đọc d₂ − d₁ rồi tắt nguồn B để thấy vân biến mất.",
  },
  {
    slug: "thuoc-kep",
    ten: "Thước kẹp du xích: đọc đến 0,02 mm",
    lop: 10,
    chu_de: "do",
    nhin_vao: "Vạch nào của du xích trùng với một vạch của thước chính?",
    mo_ta: "Kéo hàm thước kẹp quanh vật, kính lúp phóng to chỗ đọc; xem ba bước đọc rồi luyện với số ngẫu nhiên, chấm ngay.",
    nhiem_vu: "Luyện đọc đúng 5 lần liên tiếp, có cả ca vạch 0 của du xích trùng vạch thước chính.",
    lesson_id: 48,
  },
  {
    slug: "panme",
    ten: "Panme: đọc đến 0,01 mm",
    lop: 10,
    chu_de: "do",
    nhin_vao: "Đã lộ vạch nửa milimét dưới đường ngang chưa?",
    mo_ta: "Xoay thước tròn 50 vạch, mỗi vạch 0,01 mm; bốn bước đọc tô đúng phần đang đọc, rồi luyện với số ngẫu nhiên.",
    nhiem_vu: "Luyện đọc đúng 5 lần liên tiếp, chú ý ca thước tròn gần vạch 0.",
    lesson_id: 48,
  },
  {
    slug: "dong-ho-da-nang",
    ten: "Đồng hồ đo điện đa năng",
    lop: 10,
    chu_de: "do",
    nhin_vao: "Núm, thang và lỗ cắm que đỏ đã khớp với đại lượng cần đo chưa?",
    mo_ta: "Vặn núm, chọn thang, cắm que đỏ, chọn mắc song song hay nối tiếp rồi chạm que; đặt sai thì máy phản ứng như máy thật.",
    nhiem_vu: "Đặt máy đúng ngay lần chạm que đầu tiên cho 5 tình huống liên tiếp.",
    lesson_id: 47,
  },
  {
    slug: "dong-ho-hien-so",
    ten: "Đồng hồ đo thời gian hiện số + cổng quang",
    lop: 10,
    chu_de: "do",
    nhin_vao: "MODE đang đếm khoảng thời gian nào giữa hai cổng?",
    mo_ta: "Bi lăn trên máng nghiêng qua hai cổng quang E, F; chọn MODE, bấm Thả rồi đọc số chỉ 0,001 s.",
    nhiem_vu: "Với cùng một lần thả, đọc thời gian ở từng MODE và nói mỗi số đo khoảng nào.",
    lesson_id: 51,
  },
];
