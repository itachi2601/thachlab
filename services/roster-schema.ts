// Định nghĩa chung các cột điểm cho 2 mẫu file phòng đào tạo cấp — dùng cả khi đọc (parse),
// hiển thị bảng điểm và khi xuất lại file (export) để 3 nơi không lệch key nhau.

export interface GradeColumn {
  key: string;
  label: string;
}

/** Môn lý thuyết (LT) — vd "Tiếng Anh chuyên ngành". Mọi cột đều nhập tay, kể cả 2 cột tổng hợp. */
export const LT_GRADE_COLUMNS: GradeColumn[] = [
  { key: "chuyen_can", label: "Chuyên Cần" },
  { key: "kt_hs1_1", label: "KT HS1" },
  { key: "kt_hs1_2", label: "KT HS1" },
  { key: "kt_hs1_3", label: "KT HS1" },
  { key: "kt_hs2_1", label: "KT HS2" },
  { key: "kt_hs2_2", label: "KT HS2" },
  { key: "kt_hs2_3", label: "KT HS2" },
  { key: "tb_kiem_tra", label: "TB Kiểm Tra" },
  { key: "thi_lan_1", label: "Thi Lần 1" },
  { key: "tong_ket", label: "Tổng Kết 1" },
];

/** Môn thực hành (TH, CNC/Tiện-Phay) — Tổng Kết đã có công thức chính thức trong
 * TeacherFinalGradebook, không nhập tay lại ở đây. */
export const TH_GRADE_COLUMNS: GradeColumn[] = [{ key: "tong_ket", label: "Tổng Kết" }];

function normalize(text: string) {
  return text.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
}

/** Nhận diện tên cột điểm trong file Excel (không phân biệt dấu/hoa-thường) → grade_key.
 * Trả về null nếu không nhận diện được (vd cột "Ghi Chú" hoặc cột lạ). */
export function classifyGradeHeader(headerText: string, counters: Record<string, number>): string | null {
  const text = normalize(headerText);
  if (!text) return null;
  if (text.includes("chuyen can")) return "chuyen_can";
  if (text.includes("kt hs1")) { counters.hs1 = (counters.hs1 ?? 0) + 1; return `kt_hs1_${counters.hs1}`; }
  if (text.includes("kt hs2")) { counters.hs2 = (counters.hs2 ?? 0) + 1; return `kt_hs2_${counters.hs2}`; }
  if (text.includes("tb kiem tra")) return "tb_kiem_tra";
  if (text.includes("thi lan")) { counters.thi = (counters.thi ?? 0) + 1; return counters.thi === 1 ? "thi_lan_1" : `thi_lan_${counters.thi}`; }
  if (text.includes("tong ket")) return "tong_ket";
  return null;
}
