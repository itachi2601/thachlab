/**
 * lib/abet.ts — phần tính toán thuần của module ABET (không gọi Supabase), dùng chung cho
 * trang nộp của giáo viên (app/abet/nop) và trang điều phối (app/quan-tri/(cttc)/abet).
 *
 * Quy ước lấy từ file Excel "ABET MET - Theo dõi đánh giá SO-PI" (tab Hướng dẫn, Tổng hợp):
 * - một sinh viên ĐẠT một PI khi điểm câu PI ≥ 60% điểm tối đa;
 * - PI/SO ĐẠT khi tỉ lệ sinh viên đạt ≥ 60%;
 * - % của PI và của SO là GỘP sinh viên (tổng số đạt / tổng số sinh viên của mọi dòng), như SUMIFS trong Excel.
 */

export const NGUONG_SINH_VIEN = 0.6;
export const MUC_TIEU_PI = 0.6;

export type DongDiem = { mssv: string; diem: number };
/** loi: dòng có MSSV nhưng điểm hỏng (chặn nộp); boQua: dòng không có MSSV (tiêu đề…, chỉ cảnh báo). */
export type KetQuaDan = { rows: DongDiem[]; loi: string[]; lap: string[]; boQua: string[] };

/** MSSV: 4–20 chữ/số, phải có ít nhất 4 chữ số (để không nhầm chữ "Họ tên" hay "STT"). */
function laMssv(s: string) {
  return /^[A-Za-z0-9]{4,20}$/.test(s) && (s.match(/\d/g)?.length ?? 0) >= 4;
}

/** "7,5" → 7.5; trả null nếu không phải số. */
export function docSo(s: string): number | null {
  const t = s.trim().replace(/\s/g, "").replace(",", ".");
  if (!/^\d+(\.\d+)?$/.test(t)) return null;
  return Number(t);
}

/**
 * Đọc bảng dán từ Excel/Word: mỗi dòng một sinh viên. Lấy ô đầu tiên giống MSSV và ô SỐ CUỐI CÙNG
 * khác MSSV làm điểm; họ tên và các cột khác bị bỏ qua (không gửi đi). Dòng tiêu đề, dòng trống tự bỏ.
 */
export function docBangDan(text: string, diemToiDa: number | null): KetQuaDan {
  const rows: DongDiem[] = [];
  const loi: string[] = [];
  const lap: string[] = [];
  const boQua: string[] = [];
  const daCo = new Set<string>();
  text.split(/\r?\n/).forEach((dong, i) => {
    if (!dong.trim()) return;
    // Tách theo mọi khoảng trắng/tab/;/| — họ tên vỡ thành nhiều từ cũng không sao vì không phải số.
    const o = dong
      .split(/[\s;|]+/)
      .map((x) => x.trim())
      .filter(Boolean);
    const mssv = o.find(laMssv);
    if (!mssv) {
      boQua.push(`Dòng ${i + 1}: ${dong.trim().slice(0, 40)}`);
      return;
    }
    const so = o
      .filter((x) => x !== mssv)
      .map(docSo)
      .filter((x): x is number => x !== null);
    const diem = so.length ? so[so.length - 1] : null;
    if (diem === null) {
      loi.push(`Dòng ${i + 1} (${mssv}): không thấy điểm`);
      return;
    }
    if (diemToiDa && diem > diemToiDa) {
      loi.push(`Dòng ${i + 1} (${mssv}): điểm ${diem} lớn hơn điểm tối đa ${diemToiDa}`);
      return;
    }
    if (daCo.has(mssv)) {
      lap.push(mssv);
      return;
    }
    daCo.add(mssv);
    rows.push({ mssv, diem });
  });
  return { rows, loi, lap, boQua };
}

export function demDat(diem: number[], diemToiDa: number | null) {
  if (!diemToiDa) return 0;
  return diem.filter((d) => d >= NGUONG_SINH_VIEN * diemToiDa - 1e-9).length;
}

export function phanTram(x: number | null | undefined) {
  return x === null || x === undefined ? "—" : `${Math.round(x * 100)}%`;
}

export type TrangThai = "chua_gui" | "da_gui" | "da_nop" | "da_duyet" | "khong_thu_duoc";
export const NHAN_TRANG_THAI: Record<TrangThai, string> = {
  chua_gui: "Chưa gửi",
  da_gui: "Đã gửi link",
  da_nop: "Đã nộp",
  da_duyet: "Đã duyệt",
  khong_thu_duoc: "Không thu được",
};

export type LoaiTep = "de_dap_an" | "bai_mau_cao" | "bai_mau_tb" | "bai_mau_thap" | "khac";
export const NHAN_LOAI_TEP: Record<LoaiTep, string> = {
  de_dap_an: "Đề + đáp án",
  bai_mau_cao: "Bài mẫu điểm cao",
  bai_mau_tb: "Bài mẫu điểm trung bình",
  bai_mau_thap: "Bài mẫu điểm thấp",
  khac: "Tệp khác",
};

/** Năm đánh giá trước của cùng SO (chu kì 2 năm: SO1/2/4 năm lẻ-chẵn xen SO3/5). */
export function namSoSanh(namHoc: string) {
  const [a] = namHoc.split("-").map(Number);
  return `${a - 2}-${a - 1}`;
}

export type DongTongHop = {
  nam_hoc: string;
  ma: string; // PI1.1 hoặc SO1
  so_sv: number;
  so_dat: number;
  ti_le: number | null;
  nam_truoc: string;
  ti_le_truoc: number | null;
};

export function ketLuan(tiLe: number | null) {
  if (tiLe === null) return "Chưa có dữ liệu";
  return tiLe >= MUC_TIEU_PI - 1e-9 ? "Đạt" : "Chưa đạt";
}

/** Câu dùng cho báo cáo SO — giống cột "Câu cho báo cáo" của Excel. */
export function cauBaoCao(d: DongTongHop) {
  if (d.ti_le === null) return "";
  const truoc = d.ti_le_truoc === null ? "." : `; năm ${d.nam_truoc}: ${phanTram(d.ti_le_truoc)}.`;
  return `${d.ma}: ${phanTram(d.ti_le)} sinh viên đạt (${d.so_dat}/${d.so_sv}), mục tiêu ${phanTram(MUC_TIEU_PI)}, ${ketLuan(d.ti_le).toLowerCase()}${truoc}`;
}

/** Tin nhắn Zalo gửi chủ PI, kèm link nộp. */
export function tinNhan(s: {
  chu_pi: string | null;
  nam_hoc: string;
  so: string;
  pi: string;
  hoc_phan: string;
  khoa: string | null;
  hoc_ky: string | null;
  noi_dung: string | null;
  han_nop: string | null;
  link: string;
}) {
  const han = s.han_nop ? new Date(`${s.han_nop}T00:00:00`).toLocaleDateString("vi-VN") : "sớm nhất có thể";
  return [
    `Chào ${s.chu_pi ? s.chu_pi : "thầy/cô"},`,
    ``,
    `Khoa đang tổng hợp ABET năm học ${s.nam_hoc} (${s.so}). Học phần ${s.hoc_phan}${s.khoa ? `, lớp ${s.khoa}` : ""}${s.hoc_ky ? ` (${s.hoc_ky})` : ""} là nguồn dữ liệu cho ${s.pi}: ${s.noi_dung ?? ""}.`,
    ``,
    `Nhờ thầy/cô mở link dưới đây (không cần đăng nhập), làm 3 việc:`,
    `1. Ghi điểm tối đa của câu/phần đó.`,
    `2. Dán bảng MSSV + điểm câu đó (chép thẳng từ Excel, có cột họ tên cũng được, trang chỉ lấy MSSV và điểm).`,
    `3. Chụp đề + đáp án và 3 bài mẫu (một bài cao, một trung bình, một thấp).`,
    ``,
    s.link,
    ``,
    `Hạn: ${han}. Nếu không còn bài thi hay điểm từng câu, thầy/cô bấm nút "Không còn dữ liệu" trong link là được.`,
    ``,
    `Em cảm ơn thầy/cô.`,
  ].join("\n");
}
