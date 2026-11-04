// Cấu trúc học liệu: Chương → Bài học → Mục (6 loại, thứ tự cố định §1–§6)

export type LessonItemKind =
  | "ly_thuyet"
  | "video"
  | "bai_tap_mau"
  | "luyen_tap"
  | "bai_tap_ve_nha"
  | "kiem_tra";

export interface Chapter {
  id: number;
  title: string;
  sort_order: number;
  classIds: number[]; // rỗng = toàn trường
  subjectCode: string;
}

// Bài học thường, hoặc một bài chỉ có đề đặt cuối chương: kiểm tra chương,
// kiểm tra giữa học kì, kiểm tra cuối học kì.
export type LessonKind =
  | "bai_hoc"
  | "kiem_tra_chuong"
  | "kiem_tra_giua_ki"
  | "kiem_tra_cuoi_ki";

export interface Lesson {
  id: number;
  chapter_id: number;
  title: string;
  sort_order: number;
  published: boolean;
  lesson_kind: LessonKind;
  itemCount: number;
  description: string; // yêu cầu cần đạt, hiện ngắn gọn dưới tên bài
}

/** Bài chỉ gồm đề (kiểm tra chương / giữa kì / cuối kì) — không có các mục học liệu. */
export function isPeriodicExam(kind: LessonKind): boolean {
  return kind !== "bai_hoc";
}

/**
 * Kiểm tra giữa/cuối học kì: không thuộc nội dung chương nào, hiển thị thành
 * mục riêng xen giữa các chương (chương gắn nó chỉ quyết định vị trí đứng sau).
 */
export function isSemesterExam(kind: LessonKind): boolean {
  return kind === "kiem_tra_giua_ki" || kind === "kiem_tra_cuoi_ki";
}

/**
 * Tiêu đề chương trong CSDL thường đã có "Chương N: …". Bỏ tiền tố đó để nơi hiển thị tự ghép
 * "Chương N · Tên" (hoặc chỉ "Tên" khi số chương đã hiện riêng), tránh lặp "1  Chương 1: …".
 */
export function chapterDisplayTitle(title: string): string {
  return title.replace(/^chương\s*\d+\s*[:.\-–]?\s*/i, "").trim() || title;
}

/** "Chương N · Tên" — nhãn đầy đủ dùng cho breadcrumb, link quay lại, tiêu đề thẻ chương. */
export function chapterLabel(index: number, title: string): string {
  return `Chương ${index + 1} · ${chapterDisplayTitle(title)}`;
}

export interface LessonKindMeta {
  label: string; // nhãn đầy đủ, cũng là tên bài mặc định
  badge: string; // nhãn ngắn hiển thị dạng chip ("" = không hiện)
  icon: string;
  color: string;
}

export const LESSON_KIND_META: Record<LessonKind, LessonKindMeta> = {
  bai_hoc: { label: "Bài học", badge: "", icon: "📖", color: "#3B82F6" },
  kiem_tra_chuong: {
    label: "Kiểm tra chương",
    badge: "KIỂM TRA CHƯƠNG",
    icon: "📑",
    color: "#8B5CF6",
  },
  kiem_tra_giua_ki: {
    label: "Kiểm tra giữa học kì",
    badge: "GIỮA HỌC KÌ",
    icon: "📝",
    color: "#F59E0B",
  },
  kiem_tra_cuoi_ki: {
    label: "Kiểm tra cuối học kì",
    badge: "CUỐI HỌC KÌ",
    icon: "🏁",
    color: "#F43F5E",
  },
};

const LESSON_KINDS: LessonKind[] = [
  "bai_hoc",
  "kiem_tra_chuong",
  "kiem_tra_giua_ki",
  "kiem_tra_cuoi_ki",
];

export function normalizeLessonKind(kind: unknown): LessonKind {
  return LESSON_KINDS.includes(kind as LessonKind)
    ? (kind as LessonKind)
    : "bai_hoc";
}

// Một "dạng bài" tự luận cũ của mục Bài tập mẫu: đề + lời giải soạn tự do (LaTeX/HTML).
// Nội dung mới của mục này là đề gắn qua exam_ids — em chọn đáp án rồi mới mở lời giải.
export interface LessonWorkedQuestion {
  label: string;
  /** Đề + lời giải đầy đủ gộp một khối — luôn có (bản cũ, trang tĩnh, importer chỉ đọc trường này). */
  body_html: string;
  /** Dạng bài tập mẫu có cấu trúc (skill soan-bai-tap-mau): đề + gợi ý từng bước + lời giải + nhãn tìm bài tương tự. */
  problem_html?: string;
  /** Phân tích đề (bảng Câu trong đề | Dữ liệu | Kiến thức liên quan, như bài toán mẫu trong lý thuyết) — mở bằng một nút, trước lời giải. */
  analysis_html?: string;
  /** Cách cũ: gợi ý theo tầng mở lần lượt. Dạng có `analysis_html` không dùng. */
  hints_html?: string[];
  solution_html?: string;
  /** Tên YCCĐ (khớp question_topics.name) và Dạng (question_bank.form) để tìm bài tương tự trong ngân hàng. */
  topic?: string;
  topic_id?: number;
  form?: string;
  /** Tự giải từng bước (skill soan-bai-tap-mau, thầy chốt 9/10/2026). Mỗi phần tử ứng với một `.bt-step` trong solution_html, cùng thứ tự. */
  buoc?: WorkedStep[];
  /** "Thấy … trong đề → nghĩ tới …" — hiện đầu dạng và cuối lời giải. */
  nhan_dang?: string;
  /** Cấp bắc cầu 1–4 (Áp dụng trực tiếp → Có điều kiện/bẫy → Kết hợp → Tình huống mới). */
  cap_do?: number;
  /** Ví dụ mờ dần: bước nào giấu để em tự làm. Thiếu = mo_het. */
  fading?: WorkedFading;
  /** Bài tương tự sai → hỏi "em tính đến bước nào", mặc định nhảy về bước này (chỉ số 0-based). */
  go_roi?: { buoc_hay_sai: number };
  /** 💡 Mẹo nhìn (1/11/2026): mô hình đời thường giải nhanh dạng này — chỉ hiện sau lời giải (hình chạy tới đáp số). */
  meo?: WorkedMeo;
  /** 🧪 Hình giải cùng bước (thử 2/11/2026, bài 14 Sóng dạng 3): hình dính nửa trên, bước làm nửa dưới, hình vẽ thêm theo bước đã xong. */
  cong_cu?: WorkedTool;
  /** 🧪 Tóm đề (thử 3/11/2026): Cho/Tìm ngắn — điện thoại là một dòng dính chạm mở, desktop ≥1280 là thẻ lề phải. Ký hiệu khớp lời giải; không đổi đơn vị sẵn (đó là việc của bước). */
  tom_de?: WorkedTomDe;
}

/** Hình giải cùng bước. Số liệu theo đề (đơn vị: Hz, cm/s, cm) — hình của bước chỉ vẽ khi em đã làm xong bước đó. */
/** Mỗi phần tử là HTML ngắn (được dùng $…$). */
export type WorkedTomDe = { cho: string[]; tim: string[] };

export type WorkedTool =
  | { loai: "giao_thoa_2_nguon"; f: number; v: number; AB: number; d1: number; d2: number; kieu?: "dem_day" }
  | { loai: "vong_tron"; A: number; don_vi?: string; x_dich?: number[]; lop?: VongTronLop[][] }
  | { loai: "song_day"; A: number; lam: number; x_max: number; diem?: { x: number; ten: string }[]; song?: { pha: number; dau?: number }; lop?: SongDayLop[][] }
  | { loai: "van_giao_thoa"; i: number; x_min: number; x_max: number; diem?: { x: number; ten: string }[]; nhom?: { n: number; L: number }; lop?: VanGiaoThoaLop[][] }
  | { loai: "do_thi"; x: DoThiTruc; y: DoThiTruc; duong?: DoThiDuong[]; diem?: DoThiDiem[]; lop?: DoThiLop[][] }
  | { loai: "tu_truong"; nen?: TuTruongNen; hinh?: TuTruongLop[]; lop?: TuTruongLop[][] }
  | { loai: "thanh_nang_luong"; canh: NangLuongCanh; cot: { ten: string; mau?: "max" | "min" | "chu" }[]; max: number; don_vi?: string; lop?: NangLuongLop[][] }
  | SoDoVectoTool
  | { loai: "dien_truong_deu"; L: number; d: number; duong: "tren" | "duoi"; v0?: string; an_hat?: boolean; hinh?: DienTruongLop[]; lop?: DienTruongLop[][] }
  | { loai: "mach_dien"; hinh?: MachDienLop[]; lop?: MachDienLop[][] }
  | { loai: "truc_chuyen_dong"; x_min: number; x_max: number; don_vi?: string; diem?: { x: number; ten: string }[]; hinh?: TrucChuyenDongLop[]; lop?: TrucChuyenDongLop[][] }
  | { loai: "quy_dao_nem"; v0: number; alpha: number; g?: number; h0?: number; x_max: number; y_max: number; hinh?: QuyDaoNemLop[]; lop?: QuyDaoNemLop[][] }
  | { loai: "cot_chat_long"; canh: CotChatLongCanh; hinh?: CotChatLongLop[]; lop?: CotChatLongLop[][] }
  | { loai: "tia_sang"; moi: TiaSangMoi[]; goc: number[]; x0?: number; chieu?: "xuong" | "len"; hinh?: TiaSangLop[]; lop?: TiaSangLop[][] }
  | { loai: "thau_kinh"; phan: ThauKinhPhan[]; lop?: ThauKinhLop[][] };

/** Tia sáng qua các lớp môi trường (Đ5): đơn vị hình (ngang 20), môi trường theo thứ tự tia đi qua; mặt k nằm giữa môi trường k và k + 1. */
export type TiaSangMoi = { ten: string; cao: number; dam?: number; nhan_x?: number };
export type TiaSangHuong = "phap_vao" | "phap_ra" | "mat_trai" | "mat_phai" | "toi" | "phan_xa" | "khuc_xa" | number;
export type TiaSangLop =
  | LopGhi
  | { loai: "tia"; moi: number; nhan?: string; mau?: "max" | "min" | "chu"; dut?: boolean; het?: number }
  | { loai: "phan_xa"; mat: number; nhan?: string; mau?: "max" | "min" | "chu"; dut?: boolean; het?: number }
  | { loai: "phap_tuyen"; mat: number; dai?: number; het?: number }
  | { loai: "goc"; mat: number; tu: TiaSangHuong; den: TiaSangHuong; nhan: string; r?: number; r_nhan?: number; nhan_goc?: number; mau?: "max" | "min" | "chu"; het?: number }
  | { loai: "chu"; x: number; y: number; text: string; a?: "start" | "middle" | "end"; mau?: "max" | "min"; het?: number };
/** Thấu kính (Đ5): cm, y lên; mỗi `phan` là một khung (câu a/b/c), chọn theo chỉ số bước đang xem. */
export type ThauKinhPhan = { tu_buoc?: number; x_min: number; x_max: number; y_tren: number; y_duoi: number; o_ly?: number; phong_doc?: number; hinh?: ThauKinhLop[] };
export type ThauKinhLop =
  | LopGhi
  | { loai: "tk"; x: number; kieu: "hoi_tu" | "phan_ki"; ten?: string; ten_ben?: "trai" | "phai"; f?: number; tieu?: [string, string]; vi_tieu?: ["t" | "b" | "l" | "r", "t" | "b" | "l" | "r"]; het?: number }
  | { loai: "vat"; x: number; h: number; ten?: [string, string]; ten_b_ben?: "trai" | "phai"; ao?: boolean; mau?: "max" | "min"; het?: number }
  | { loai: "diem"; x: number; y?: number; ten: string; vi?: "t" | "b" | "l" | "r"; mau?: "max" | "min"; het?: number }
  | { loai: "tia"; qua: number[][]; keo?: number[][]; mau?: "max" | "min"; dut?: boolean; mep?: boolean; het?: number }
  | { loai: "thuoc"; tu: number; den: number; o: number; doc?: boolean; nhan: string; ben?: "tren" | "duoi" | "trai" | "phai"; het?: number }
  | { loai: "chu"; x: number; y: number; text: string; a?: "start" | "middle" | "end"; mau?: "max" | "min"; het?: number };

/** Trục chuyển động 1D (Đ4): x theo đơn vị đề; `hang` ≥ 1 trên trục, ≤ −1 dưới tên mốc, 0 = trên trục. */
export type TrucChuyenDongLop =
  | LopGhi
  | { loai: "doan"; tu: number; den: number; hang: number; nhan?: string; mau?: "max" | "min" | "muc"; dut?: boolean; het?: number }
  | { loai: "ngoac"; tu: number; den: number; hang: number; nhan: string; het?: number }
  | { loai: "cham"; x: number; hang?: number; ten?: string; het?: number }
  | { loai: "vat"; x: number; hang?: number; ten?: string; v?: number; nhan_v?: string; het?: number }
  | { loai: "chu"; x: number; hang: number; text: string; a?: "start" | "middle" | "end"; het?: number };
/** Quỹ đạo ném (Đ4): mét, cùng tỉ lệ hai trục; `t` = phần thời gian bay (0..1). */
export type QuyDaoNemLop =
  | LopGhi
  | { loai: "quy_dao"; alpha?: number; tu?: number; den?: number; dut?: boolean; mau?: "max" | "min" | "muc"; nhan?: string; het?: number }
  | { loai: "van_toc"; t: number; alpha?: number; tach?: boolean; chi?: "x" | "y" | "ca"; nhan?: string; nhan_x?: string; nhan_y?: string; het?: number }
  | { loai: "diem"; t: number; alpha?: number; ten: string; vi?: "t" | "b" | "l" | "r"; het?: number }
  | { loai: "goc"; alpha?: number; nhan: string; het?: number }
  | { loai: "moc"; x: number; nhan: string; het?: number }
  | { loai: "thuoc_ngang"; tu: number; den: number; nhan: string; het?: number }
  | { loai: "thuoc_doc"; x: number; tu: number; den: number; nhan: string; ben?: "trai" | "phai"; het?: number };
/** Cột chất lỏng (Đ4): độ cao theo cm; ống U: y = 0 ở mặt phân cách; bể: y = 0 ở mặt nước. */
export type CotChatLongCanh = { kieu: "ong_u"; h_max: number } | { kieu: "be"; rong: number; cao: number; tren: number; sau: number };
export type CotChatLongLop =
  | LopGhi
  | { loai: "muc"; h1: number; h2: number; het?: number }
  | { loai: "diem"; ten: "A" | "B"; het?: number }
  | { loai: "ngang"; nhan?: string; het?: number }
  | { loai: "thuoc"; ong: "trai" | "phai" | "giua"; tu: number; den: number; nhan: string; het?: number }
  | { loai: "khoi"; chim: number; vat?: string; het?: number }
  | { loai: "luc"; ten: string; huong: "len" | "xuong"; do_lon: number; tu?: "khoi" | "vat"; lech?: number; het?: number }
  | { loai: "chu"; x: number; y: number; text: string; a?: "start" | "middle" | "end"; mau?: "max" | "min"; het?: number };

/** Điện trường đều (Đ3): x tính từ mép vào của bản (cùng đơn vị L), y tính từ đường giữa hai bản (cùng đơn vị d), lên là dương. */
export type DienTruongLop =
  | LopGhi
  | { loai: "duong_suc"; nhan?: string; het?: number }
  | { loai: "luc"; huong: "len" | "xuong"; nhan?: string; het?: number }
  | { loai: "quy_dao"; y_cuoi: number; cat?: boolean; dut?: boolean; mau?: "max" | "min"; het?: number }
  | { loai: "thuoc_ngang"; tu: number; den: number; nhan: string; vi: "tren" | "duoi"; het?: number }
  | { loai: "thuoc_doc"; x: number; tu: number; den: number; nhan: string; ben?: "trai" | "phai"; mau?: "max" | "min"; het?: number }
  | { loai: "chu"; x: number; y: number; text: string; a?: "start" | "middle" | "end"; het?: number };
/** Mạch điện (Đ3): toạ độ 0..20 ngang, 0..11 dọc, gốc dưới trái (y lên). Linh kiện đặt TÂM tại (x, y), che dây bên dưới bằng nền halo. */
export type MachDienHuong = "ngang" | "doc";
export type MachDienLop =
  | LopGhi
  | { loai: "day"; diem: [number, number][]; dut?: boolean; mau?: "max" | "min"; het?: number }
  | { loai: "nut"; x: number; y: number; het?: number }
  | { loai: "nguon"; x: number; y: number; huong?: MachDienHuong; duong?: "truoc" | "sau"; ten?: string; vi?: "t" | "b" | "l" | "r"; het?: number }
  | { loai: "dien_tro"; x: number; y: number; huong?: MachDienHuong; ten?: string; vi?: "t" | "b" | "l" | "r"; het?: number }
  | { loai: "den"; x: number; y: number; ten?: string; vi?: "t" | "b" | "l" | "r"; het?: number }
  | { loai: "dong_ho"; x: number; y: number; kieu: "V" | "A"; ten?: string; vi?: "t" | "b" | "l" | "r"; het?: number }
  | { loai: "khoa"; x: number; y: number; huong?: MachDienHuong; mo?: boolean; het?: number }
  | { loai: "dong"; tu: [number, number]; den: [number, number]; nhan?: string; vi?: "t" | "b" | "l" | "r"; het?: number }
  | { loai: "ngoac"; tu: [number, number]; den: [number, number]; nhan: string; vi?: "t" | "b"; mau?: "max" | "min"; het?: number }
  | { loai: "chu"; x: number; y: number; text: string; a?: "start" | "middle" | "end"; mau?: "max" | "min"; het?: number }
  | { loai: "bang"; x: number; y: number; hang: string[][]; het?: number };

/** Mục vẽ thêm của từng bước (lop[i] hiện khi em đã xong bước i + 1; `het: k` ẩn từ khi xong bước k). Góc theo đơn vị π. */
type LopGhi = { loai: "ghi"; text: string; het?: number };
export type VongTronLop =
  | LopGhi
  | { loai: "diem"; goc: number; ten?: string; chieu?: boolean; het?: number }
  | { loai: "cung"; tu: number; den: number; het?: number }
  | { loai: "giao"; x: number; so?: string[]; het?: number };
export type SongDayLop =
  | LopGhi
  | { loai: "song"; pha: number; dau?: number; het?: number }
  | { loai: "thuoc"; tu: number; den: number; nhan: string; hang?: number; het?: number }
  | { loai: "mui"; x: number; huong: "len" | "xuong"; het?: number }
  | { loai: "dau_song"; x: number; het?: number };
/** Đồ thị (Đ2): trục có `vach` (số ghi trên trục, khai đúng số đề cho để không lộ đáp số) và `luoi` (bước lưới mờ). */
export type DoThiTruc = { min: number; max: number; ten: string; vach?: number[]; luoi?: number };
/** Hàm lấy mẫu (không chạy chuỗi công thức): cos y = c + a·cos(wπx + phiπ) · mu y = c + a·2^(−x/T) · nghich y = a/x · da_thuc Σ he[i]·xⁱ. */
export type DoThiHam =
  | { kieu: "cos"; a: number; w: number; phi?: number; c?: number }
  | { kieu: "mu"; a: number; T: number; c?: number }
  | { kieu: "nghich"; a: number }
  | { kieu: "da_thuc"; he: number[] };
export type DoThiDuong = {
  diem?: [number, number][];
  ham?: DoThiHam;
  tu?: number;
  den?: number;
  /** max = cam liền, min = xanh nét đứt (H4), chu = màu chữ (mặc định). */
  mau?: "max" | "min" | "chu";
  ten?: string;
  /** chỗ đặt tên đường, toạ độ số liệu */
  ten_xy?: [number, number];
};
/** Vị trí nhãn so với điểm: t trên, b dưới, l trái, r phải, tl/tr/bl/br chéo. */
export type DoThiVi = "t" | "b" | "l" | "r" | "tl" | "tr" | "bl" | "br";
export type DoThiDiem = { x: number; y: number; ten?: string; vi?: DoThiVi };
export type DoThiLop =
  | LopGhi
  | ({ loai: "diem" } & DoThiDiem & { het?: number })
  | { loai: "duong"; duong: DoThiDuong; het?: number }
  | { loai: "chieu"; x: number; y: number; nhan_x?: string; nhan_y?: string; het?: number }
  | { loai: "ngang"; y: number; nhan?: string; tu?: number; den?: number; het?: number }
  | { loai: "dung"; x: number; nhan?: string; het?: number }
  | { loai: "doan"; tu: number; den: number; duong?: number; nhan?: string; vi?: "t" | "b"; nhan_xy?: [number, number]; het?: number }
  | { loai: "thuoc"; tu: number; den: number; y: number; nhan: string; het?: number }
  | { loai: "doc"; tu: [number, number]; den: [number, number]; nhan_x?: string; nhan_y?: string; het?: number }
  | { loai: "dien_tich"; tu: number; den: number; duong?: number; nhan?: string; het?: number };
/** Từ trường (Đ2): toạ độ hình 0..20 ngang, 0..11 dọc, gốc dưới trái (y hướng lên). Góc theo độ, 0° = sang phải. */
/** `hang`: toạ độ dọc các đường sức (kiểu duong_suc), chừa chỗ dây/khung. */
export type TuTruongNen = { kieu: "ra" | "vao" | "duong_suc"; goc?: number; nhan?: string; hang?: number[] };
export type TuTruongLop =
  | LopGhi
  | { loai: "day"; tu: [number, number]; den: [number, number]; nhan?: string; mau?: "max" | "min" | "chu"; dut?: boolean; het?: number }
  | { loai: "dong"; tu: [number, number]; den: [number, number]; nhan?: string; het?: number }
  | { loai: "tiet_dien"; x: number; y: number; chieu: "ra" | "vao"; ten?: string; het?: number }
  | { loai: "vec"; x: number; y: number; goc: number; dai: number; nhan?: string; mau?: "max" | "min" | "chu"; dut?: boolean; trai?: boolean; het?: number }
  | { loai: "goc"; x: number; y: number; tu: number; den: number; nhan?: string; het?: number }
  | { loai: "chu"; x: number; y: number; text: string; a?: "start" | "middle" | "end"; het?: number }
  | { loai: "nam_cham"; x: number; y: number; dai: number; cao: number; n_trai?: boolean; het?: number }
  | { loai: "tran"; x1: number; x2: number; y: number; het?: number }
  | { loai: "khung"; x: number; y: number; rong: number; sau: [number, number]; ten?: [string, string, string, string]; B?: boolean; nhan?: string; het?: number };
/** Năng lượng (Đ2): cảnh bên trái + cột cùng thang `max` bên phải. */
export type NangLuongCanh =
  | { kieu: "lo_xo_ngang"; A: number; don_vi?: string; x?: number }
  | { kieu: "con_lac_don"; goc0: number; goc?: number }
  | { kieu: "doc"; h: number; don_vi?: string; vi?: number }
  | { kieu: "hop_he"; ten?: string };
export type NangLuongLop =
  | LopGhi
  | { loai: "cot"; ten: string; gia_tri: number; nhan?: string; het?: number }
  | { loai: "vat"; x?: number; goc?: number; vi?: number; bong?: boolean; het?: number }
  | { loai: "v"; nhan: string; chieu?: 1 | -1; het?: number }
  | { loai: "mui"; vao: boolean; nhan: string; hang?: number; het?: number };
export type VanGiaoThoaLop =
  | LopGhi
  | { loai: "dem" | "thuoc_i" | "van"; het?: number }
  | { loai: "thuoc"; tu: number; den: number; nhan: string; het?: number };

/** Điểm đặt: tên điểm của cảnh ("vat", "vat_day", "chan", "dinh", "O", tên đầu dây, "m1", "m2", "A", "B") hoặc toạ độ [x, y] (y lên). */
export type VecPoint = string | [number, number];
/** Hướng: độ (0 = sang phải, 90 = lên) hoặc "phai" | "trai" | "len" | "xuong" | "doc_xuong" | "doc_len" | "phap_tuyen" | "vao_doc" | "day:<tên đầu dây>". */
export type VecDir = number | string;
type Mau = "muc" | "cam" | "lam" | "tim";

/** 🧪 Họ `so_do_vecto` (3/11/2026): cảnh vẽ bằng code + vectơ khai ở đây; `buoc` = hiện khi đã xong bước đó (0 = có từ đầu), `den` = ẩn từ bước đó. */
export type SoDoVectoTool = {
  /** "thanh_moment" dùng chung component, cảnh `nen.kieu: "thanh"` (thanh ngang, x thật tính từ đầu trái). */
  loai: "so_do_vecto" | "thanh_moment";
  nen:
    | { kieu: "mat_ngang"; vat?: string; vat_x?: number }
    | { kieu: "mat_nghieng"; alpha: number; vat?: string; vat_t?: number; dai?: string }
    | { kieu: "nut"; ten_nut?: string; ten_nut_lech?: [number, number]; day: { goc: number; dai: number; neo: "tuong" | "tran" | "cot" | "vat" | "khong"; ten?: string; vat?: string }[] }
    | { kieu: "rong_roc"; vat1?: string; vat2?: string; lech?: number }
    | { kieu: "ban_rong_roc"; vat1?: string; vat2?: string }
    | { kieu: "khong" }
    | {
        /** Đ4: hai bờ sông (bờ dưới y = 0, bờ trên y = rong), `chay` = nhãn mũi tên dòng nước; `duong` nét đứt nối hai điểm. */
        kieu: "song";
        rong: number;
        chay?: string;
        diem: { ten: string; x: number; bo: "tren" | "duoi"; buoc?: number; lech?: number }[];
        duong?: { tu: string; toi: string; buoc?: number; den?: number }[];
      }
    | {
        kieu: "thanh";
        dai: number;
        diem: { ten: string; x: number; buoc?: number; nhan?: "tren" | "duoi" | "trai" | "phai"; nhan_lech?: [number, number] }[];
        /** Giá đỡ nhọn dưới thanh hoặc bản lề (vòng tròn); `buoc` = hiện khi xong bước đó (vd vị trí O là đáp số). */
        do?: { kieu: "gia_do" | "ban_le"; x: number; buoc?: number };
        khoi?: { x: number; text?: string }[];
        /** Dây từ điểm `tu` (tên điểm, x thật) theo hướng `goc` tới tường trái (nếu `tuong`). Hướng "day:<tu>". */
        day?: { tu: string; x: number; goc: number; ten_neo?: string };
        tuong?: boolean;
      };
  /** kieu: "luc" (mặc định, nét liền) · "thanh_phan" (nét đứt) · "dong_hoc" (a, v: màu lam, tỉ lệ riêng). `so` = độ lớn hiện ở bảng số từ bước `so_buoc` (mặc định = `buoc`). */
  vec: { ten: string; goc: VecDir; do_lon: number; tu?: VecPoint; lech?: [number, number]; buoc?: number; den?: number; kieu?: "luc" | "thanh_phan" | "dong_hoc"; mau?: Mau; so?: string; so_buoc?: number; nhan_lech?: [number, number] }[];
  /** Nét chấm từ ngọn vectơ `vec` tới ngọn các thành phần (hình bình hành / hình chữ nhật phân tích). */
  hbh?: { vec: string; thanh: string[]; buoc?: number; den?: number }[];
  truc?: { tai?: VecPoint; goc: number; dai?: number; ten?: [string, string]; buoc?: number; den?: number };
  goc?: { tai?: VecPoint; tu: VecDir; den: VecDir; r?: number; text?: string; mau?: Mau; buoc?: number; an?: number }[];
  /** Dòng thêm ở bảng số (vd "θ = 9,46°"). */
  bang?: { text: string; mau?: Mau; buoc?: number; den?: number }[];
  /** Mặc định "phai" (nới khung sang phải); mặt nghiêng mặc định "trong" (góc trên phải, khoảng trống trên chân dốc). */
  bang_vi_tri?: "trai" | "phai" | "trong" | "tren";
  /** Độ dài (đơn vị hình) của vectơ lớn nhất mỗi nhóm; mặc định 5. */
  ti_le?: number;
  /** Ngoặc đo ngang dưới hình (vd AB = 1,0 m); `an` = ẩn từ bước đó. */
  kich_thuoc?: { a: VecPoint; b: VecPoint; text?: string; buoc?: number; an?: number }[];
  /** Cánh tay đòn của lực `luc` đối với trục qua điểm `truc`: lực đứng → ngoặc đo; lực xiên → đoạn vuông góc + dấu góc vuông. */
  tay_don?: { truc: VecPoint; luc: string; text?: string; buoc?: number; an?: number }[];
};

export interface WorkedMeo {
  /** Tên 2–3 chữ, dùng y hệt ở mọi lớp (docs/KE-HOACH-MEO-GIAI-BAI-TAP.md). */
  ten: string;
  /** ⚠ Khi nào mẹo đúng — không có ranh giới thì phép so sánh thành quan niệm sai (AI-TUTOR 9.1). */
  dieu_kien: string;
  /** Hình SMIL bấm mới chạy + 1–2 câu nối mẹo với đề của dạng. */
  html: string;
}

export type WorkedFading = "mo_het" | "giau_buoc_cuoi" | "giau_tu_buoc_2" | "giau_het";

export interface WorkedChoice {
  text: string;
  dung?: boolean;
  /** Vì sao lựa chọn này sai (bắt buộc với lựa chọn sai). */
  vi_sao?: string;
}

export interface WorkedStep {
  tieu_de: string;
  /** Câu hỏi của bước. Không có → bước phụ (kiểm tra…), tự mở ngay sau bước trước. */
  hoi?: string;
  /** Đáp số bằng số + sai số tuyệt đối chấp nhận. */
  dap_so?: number;
  don_vi?: string;
  sai_so?: number;
  /** Câu định tính: chọn 1 trong nhiều, thay cho dap_so. */
  lua_chon?: WorkedChoice[];
  /** Lỗi hay gặp ở bước này — hiện khi em trả lời sai. */
  loi_hay_gap?: string;
  /** "Bước tiếp theo là gì?" — 3 lựa chọn (1 đúng, 2 là cách làm sai hay chọn). Chỉ ở bước ≥ 2. */
  chon_buoc_ke?: WorkedChoice[];
}

export interface LessonItem {
  id: number;
  lesson_id: number;
  kind: LessonItemKind;
  title: string;
  subtitle: string;
  body_html: string; // chỉ dùng cho ly_thuyet
  summary_html: string; // ly_thuyet: "Tóm tắt ý chính cần thuộc" — rỗng = chưa có, ẩn khối này
  video_url: string;
  pdf_url: string;
  questions: LessonWorkedQuestion[]; // bai_tap_mau: các dạng bài tự luận cũ
  exam_ids: number[]; // bai_tap_mau / luyen_tap / bai_tap_ve_nha / kiem_tra
  due_at: string | null; // bai_tap_ve_nha: hạn nộp (null = không đặt hạn)
  sort_order: number;
  required: boolean; // có tính vào tiến độ bắt buộc không (mặc định true)
  quiz_min_correct: number | null; // ly_thuyet có quiz: số câu đúng tối thiểu để đạt
  practice_pass_score: number | null; // luyen_tap: điểm đạt thang 10 (áp cho phiên cao nhất)
  published_at: string | null; // null = chưa đăng, học sinh chưa thấy mục này
  draft_payload: LessonItemDraftPayload | null; // bản nháp đang sửa dở, chưa ghi đè bản đã đăng
  draft_saved_at: string | null;
  /** Chỉ có khi mục đến từ file tĩnh /data/lessons/<id>.json: số dạng bài tập mẫu trên DB
   *  (file tĩnh không chứa lời giải, `questions` rỗng cho tới khi đối chiếu Supabase xong). */
  questions_count?: number;
}

/** Các trường nội dung soạn trong ItemForm — lưu tạm vào lesson_items.draft_payload khi "Lưu nháp". */
export interface LessonItemDraftPayload {
  kind: LessonItemKind;
  title: string;
  subtitle: string;
  body_html: string;
  video_url: string;
  pdf_url: string;
  questions: LessonWorkedQuestion[];
  exam_ids: number[];
  due_at: string | null;
}

/** Mục học sinh xem được: đã đăng chính thức ít nhất 1 lần (published_at khác null). */
export function isItemLive(item: LessonItem): boolean {
  return item.published_at !== null;
}

/** Mục gắn đề trắc nghiệm (dùng ExamPicker khi soạn). */
export const EXAM_KINDS: LessonItemKind[] = [
  "bai_tap_mau",
  "luyen_tap",
  "bai_tap_ve_nha",
  "kiem_tra",
];

export function isExamKind(kind: LessonItemKind): boolean {
  return EXAM_KINDS.includes(kind);
}

/** Mục làm bài trọn đề, chấm điểm và vào bảng điểm. */
export function isGradedKind(kind: LessonItemKind): boolean {
  return kind === "bai_tap_ve_nha" || kind === "kiem_tra";
}

export const SECTION_ORDER: LessonItemKind[] = [
  "ly_thuyet",
  "video",
  "bai_tap_mau",
  "luyen_tap",
  "bai_tap_ve_nha",
  "kiem_tra",
];

export interface SectionMeta {
  label: string;
  icon: string;
  color: string; // màu chủ đạo của mục (tiêu đề, icon)
  action: string; // nhãn nút hành động
}

export const SECTION_META: Record<LessonItemKind, SectionMeta> = {
  ly_thuyet: { label: "Lý thuyết trọng tâm", icon: "📖", color: "#3B82F6", action: "Xem" },
  video: { label: "Video bài giảng", icon: "🎬", color: "#38BDF8", action: "Xem video" },
  bai_tap_mau: { label: "Bài tập mẫu", icon: "✏️", color: "#8B5CF6", action: "Làm bài" },
  luyen_tap: { label: "Luyện tập", icon: "📚", color: "#F59E0B", action: "Luyện ngay" },
  bai_tap_ve_nha: { label: "Bài tập về nhà", icon: "🏠", color: "#10B981", action: "Làm bài" },
  kiem_tra: { label: "Kiểm tra", icon: "📝", color: "#F43F5E", action: "Làm bài" },
};

/** Chuẩn hóa dữ liệu của cấu trúc 6 mục cũ trong lúc migration DB chưa được chạy. */
export function normalizeLessonItemKind(kind: unknown): LessonItemKind {
  if (kind === "luyen_tap_sach" || kind === "luyen_tap_de") return "luyen_tap";
  return SECTION_ORDER.includes(kind as LessonItemKind)
    ? (kind as LessonItemKind)
    : "ly_thuyet";
}

// Nhãn viết tắt số câu theo dạng: 12 TN · 2 ĐS · 4 TLN
export const TYPE_SHORT: Record<string, string> = {
  multiple_choice: "TN",
  true_false: "ĐS",
  short_answer: "TLN",
};

export type TypeCounts = Partial<Record<string, number>>;

export function formatTypeCounts(counts: TypeCounts | null | undefined): string {
  if (!counts) return "";
  return Object.entries(TYPE_SHORT)
    .filter(([type]) => (counts[type] ?? 0) > 0)
    .map(([type, short]) => `${counts[type]} ${short}`)
    .join(" · ");
}

/** Đổi link YouTube bất kỳ (watch/youtu.be/shorts) thành id video. */
export function youTubeId(url: string): string | null {
  const m = url.match(
    /(?:youtube\.com\/(?:watch\?v=|shorts\/|embed\/)|youtu\.be\/)([\w-]{11})/,
  );
  return m ? m[1] : null;
}

export function youTubeEmbed(url: string): string | null {
  const id = youTubeId(url);
  return id ? `https://www.youtube.com/embed/${id}` : null;
}

export function youTubeThumb(url: string): string | null {
  const id = youTubeId(url);
  return id ? `https://i.ytimg.com/vi/${id}/hqdefault.jpg` : null;
}
