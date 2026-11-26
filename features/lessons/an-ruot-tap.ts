/**
 * Bài lý thuyết soạn cho lớp thầy dạy có RUỘT TẬP in sẵn: ô Chốt mục có dòng
 * `<summary>✍️ Tập ô 1·4 · đối chiếu 3 dòng</summary>` và hộp "Mang về" có câu "Ruột tập: điền đủ các ô …".
 * Học sinh không có Tập (tự học, lớp khác) không hiểu "Tập ô 1·4" → lúc render đổi nhãn thành
 * "✍️ Ghi vào vở · đối chiếu N dòng" và thay câu "Ruột tập: …" bằng câu chỉ việc ghi vở (hộp "Mang về"
 * thường chỉ có câu đó — bỏ hẳn thì còn hộp rỗng). KHÔNG sửa HTML lưu trong DB.
 * (docs/DE-XUAT-CAI-TIEN-LY-THUYET-2026-11-26.md P3; quy tắc N1 — bớt tải nhận thức thừa.)
 */

const CHOT_GHI_RE = /(<details\b[^>]*\btl-chot-ghi\b[^>]*>\s*<summary\b[^>]*>)([\s\S]*?)(<\/summary>)([\s\S]*?<\/details>)/g;
const TAP_O_RE = /✍️\s*Tập ô\s/;
const DOI_CHIEU_RE = /đối chiếu\s+(\d+)\s+dòng/;
/** "Ruột tập: điền đủ các ô …" tới hết đoạn `<p>` (câu đứng trước, nếu có, được giữ). */
const RUOT_TAP_RE = /Ruột tập:[\s\S]*?(?=<\/p>)/g;
/** Câu Trả bài nhắc "vào Tập ô 4·2", "(Tập ô 3·3)" → "vào vở", "(vở)". */
const TAP_O_TRONG_CAU_RE = /(<p>\s*)?Tập ô \d+·\d+(?:\s*[–-]\s*\d+(?:·\d+)?)?/g;
/** "(ô 2·3 Tập)", "điền ô 2·3 Tập trước", "Gấp Tập" (vài bài L11). */
const O_TAP_RE = /ô \d+·\d+ Tập(?![\p{L}])/gu;
const GAP_TAP_RE = /Gấp Tập(?![\p{L}])/gu;
const GHI_VO = "Ghi vào vở: chép các dòng ✍️ trong từng ô Chốt mục ở trên, gấp lại rồi tự đối chiếu.";

export function anRuotTap(html: string): string {
  if (!html.includes("Tập") && !html.includes("Ruột tập")) return html;
  const out = html.replace(CHOT_GHI_RE, (all, mo: string, nhan: string, dong: string, than: string) => {
    if (!TAP_O_RE.test(nhan)) return all;
    const n = DOI_CHIEU_RE.exec(nhan)?.[1] ?? String((than.match(/<li\b/g) ?? []).length);
    const moi = n !== "0" ? `✍️ Ghi vào vở · đối chiếu ${n} dòng` : "✍️ Ghi vào vở";
    return `${mo}${moi}${dong}${than}`;
  });
  return out
    .replace(RUOT_TAP_RE, GHI_VO)
    .replace(O_TAP_RE, "vào vở")
    .replace(GAP_TAP_RE, "Gấp vở")
    .replace(TAP_O_TRONG_CAU_RE, (_m, dauDoan?: string) => (dauDoan ? `${dauDoan}Vở` : "vở"));
}

/** Thầy chốt 26/11/2026: HS "có ruột Tập" = đã nhập từ danh sách lớp của thầy (có class_name hoặc student_code). */
export function hocSinhCoRuotTap(p: { class_name?: string | null; student_code?: string | null }): boolean {
  return Boolean(p.class_name?.trim() || p.student_code?.trim());
}
