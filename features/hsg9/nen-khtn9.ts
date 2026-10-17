// Bài KHTN 9 (phần Vật lí) làm nền cho từng chuyên đề HSG. Nguồn: bảng ánh xạ trong docs/HSG9-KHUNG.md.
// Chuyên đề chưa có bài KHTN 9 tương ứng (Lực, Chất lưu, Nhiệt, Âm, Gương phẳng, Thiên văn…) thì không có mục ở đây.
export interface NenKhtn9Lesson {
  id: number;
  title: string;
}

const L: Record<number, string> = {
  83: "Khúc xạ ánh sáng",
  84: "Phản xạ toàn phần",
  85: "Lăng kính",
  86: "Thấu kính",
  87: "Thực hành đo tiêu cự",
  88: "Kính lúp. Bài tập thấu kính",
  89: "Điện trở. Định luật Ohm",
  90: "Đoạn mạch nối tiếp, song song",
  91: "Năng lượng của dòng điện và công suất điện",
  92: "Cảm ứng điện từ, dòng xoay chiều",
  93: "Tác dụng của dòng điện xoay chiều",
  94: "Vòng năng lượng trên Trái Đất",
  95: "Năng lượng tái tạo",
  129: "Động năng. Thế năng",
  130: "Cơ năng",
  131: "Công và công suất",
};

/** id bài HSG → id các bài KHTN 9 nền */
const NEN: Record<number, number[]> = {
  161: [131],
  166: [129, 130],
  159: [89],
  157: [90],
  165: [91],
  151: [83, 84, 85],
  156: [86, 87, 88],
  152: [92, 93],
  163: [94, 95],
};

export function nenKhtn9Of(hsgLessonId: number): NenKhtn9Lesson[] {
  return (NEN[hsgLessonId] ?? []).map((id) => ({ id, title: L[id] }));
}

export function nenKhtn9Href(id: number) {
  return `/lop-hoc/bai?${new URLSearchParams({ id: String(id), subject: "vat-ly", class: "khtn-9" }).toString()}`;
}

// Bài lớp 10 học tiếp sau chuyên đề HSG (cột "Bài lớp 10–12 trùng chủ đề" của docs/HSG9-KHUNG.md).
// Chỉ nối Cơ học lớp 10; Điện lớp 11 và Nhiệt lớp 12 xa trình độ lớp 9 nên không nối.
const L10: Record<number, string> = {
  50: "Bài 5. Tốc độ và vận tốc",
  52: "Bài 7. Đồ thị độ dịch chuyển – thời gian",
  58: "Bài 13. Tổng hợp và phân tích lực. Cân bằng lực",
  62: "Bài 17. Trọng lực và lực căng",
  63: "Bài 18. Lực ma sát",
  66: "Bài 21. Moment lực. Cân bằng của vật rắn",
  68: "Bài 23. Năng lượng. Công cơ học",
  69: "Bài 24. Công suất",
  70: "Bài 25. Động năng, thế năng",
  71: "Bài 26. Cơ năng và định luật bảo toàn cơ năng",
  72: "Bài 27. Hiệu suất",
  79: "Bài 34. Khối lượng riêng. Áp suất chất lỏng",
};

/** id bài HSG → id các bài lớp 10 học tiếp */
const TIEP_L10: Record<number, number[]> = {
  161: [68, 69, 72],
  166: [70, 71],
  155: [58, 62, 63, 66],
  154: [79],
  162: [50, 52],
};

export function tiepLop10Of(hsgLessonId: number): NenKhtn9Lesson[] {
  return (TIEP_L10[hsgLessonId] ?? []).map((id) => ({ id, title: L10[id] }));
}

export function tiepLop10Href(id: number) {
  return `/lop-hoc/bai?${new URLSearchParams({ id: String(id), subject: "vat-ly", class: "lop-10" }).toString()}`;
}
