// Chuẩn hoá tên đề thi — dùng chung cho trang /de-thi (tên hiển thị) và script đổi tên gốc trong CSDL.
// Tên chuẩn trong CSDL giữ tiền tố loại đề + năm vì ExamShelf / build-content phân kệ theo chữ trong tên:
//   Thi thử TN 2026 – Sở GD&ĐT Sơn La – Lần 2
//   Giữa HK1 2024–2025 – 11 – THPT Lê Duẩn (đã lược 2 câu)

// Tên đề trong CSDL do nhiều nguồn dán vào nên lộn xộn: không dấu, gạch dưới, lẫn năm và "Lần". Chuẩn hiển thị:
//   "<Nơi ra đề> · Lần N"  (năm và lớp đã có ở dòng dưới thẻ). Chỉ đổi cách HIỂN THỊ, không đổi tên gốc.
const hasDiacritics = (t: string) => /[\u0300-\u036f]/.test(t.normalize("NFD")) || /[đĐ]/.test(t);
const fold = (t: string) => t.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/gi, "d").toLowerCase();

const PROVINCES = [
  "An Giang","Bà Rịa Vũng Tàu","Bắc Giang","Bắc Kạn","Bạc Liêu","Bắc Ninh","Bến Tre","Bình Định","Bình Dương","Bình Phước","Bình Thuận","Cà Mau","Cần Thơ","Cao Bằng","Đà Nẵng","Đắk Lắk","Đắk Nông","Điện Biên","Đồng Nai","Đồng Tháp","Gia Lai","Hà Giang","Hà Nam","Hà Nội","Hà Tĩnh","Hải Dương","Hải Phòng","Hậu Giang","Hòa Bình","Hưng Yên","Khánh Hòa","Kiên Giang","Kon Tum","Lai Châu","Lâm Đồng","Lạng Sơn","Lào Cai","Long An","Nam Định","Nghệ An","Ninh Bình","Ninh Thuận","Phú Thọ","Phú Yên","Quảng Bình","Quảng Nam","Quảng Ngãi","Quảng Ninh","Quảng Trị","Sóc Trăng","Sơn La","Tây Ninh","Thái Bình","Thái Nguyên","Thanh Hóa","Thừa Thiên Huế","Tiền Giang","Trà Vinh","Tuyên Quang","Vĩnh Long","Vĩnh Phúc","Yên Bái",
].map((name) => ({ name, key: fold(name) }));

// Cụm hay gặp (so khớp trên bản không dấu, thay bằng bản chuẩn). Cụm dài đặt trước.
const PHRASES: [RegExp, string][] = [
  [/\bso (?:giao duc va dao tao|gd ?(?:&|va)? ?dt)\b/g, "Sở GD&ĐT"],
  [/\btrung tam luyen thi dai hoc su pham\b/g, "Trung tâm luyện thi ĐH Sư phạm"],
  [/\bde phat trien de minh (?:hoa|hoạ)\b/g, "Đề phát triển đề minh hoạ"],
  [/\bcua bo giao duc va dao tao\b/g, "(Bộ GD&ĐT)"],
  [/\bde (?=\d)/g, "Đề "],
  [/\bkontum\b/g, "Kon Tum"],
  [/\bsp (?:tap )?huan\b/g, "SP tập huấn"],
  [/\blien truong\b/g, "Liên trường"],
  [/\bchuyen\b/g, "Chuyên"],
  [/\btruong thpt\b/g, "THPT"],
  [/\bttgdtx\b/g, "TTGDTX"],
  [/\btp\.? ?(?:ho chi minh|hcm)\b|\bho chi minh\b/g, "TP.HCM"],
  [/\bnguyen khuyen\b|\bnguyenkhuyen\b/g, "Nguyễn Khuyến"],
  [/\ble thanh tong\b/g, "Lê Thánh Tông"],
  [/\bve dich\b/g, "Về đích"],
  [/\bthpt\b/g, "THPT"],
  [/\bhcm\b/g, "TP.HCM"],
];

function capitalizeWords(t: string) {
  return t.replace(/\S+/g, (w) => (/^[A-ZĐ0-9&.+()]+$/.test(w) ? w : w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()));
}

function accentize(text: string): string {
  // Chỉ sửa đoạn chưa có dấu; tên đã gõ có dấu thì giữ nguyên.
  if (hasDiacritics(text)) return text;
  let out = fold(text);
  const marks: string[] = [];
  const stash = (v: string) => `\u0001${marks.push(v) - 1}\u0002`;
  for (const [re, to] of PHRASES) out = out.replace(re, () => stash(to));
  for (const p of [...PROVINCES].sort((x, y) => y.key.length - x.key.length)) {
    out = out.replace(new RegExp(`\\b${p.key}\\b`, "g"), () => stash(p.name));
  }
  out = capitalizeWords(out);
  return out.replace(/\u0001(\d+)\u0002/g, (_, i) => marks[Number(i)]);
}


export interface ParsedExamTitle {
  /** Nơi ra đề, đã chuẩn hoá (không năm, không lần, không mã đề). */
  name: string;
  lan: string;
  maDe: string;
  /** "HK1" / "HK2" hoặc "". */
  term: string;
  /** Năm hoặc năm học như tên gốc ghi ("2025", "2024–2025") hoặc "". */
  yearToken: string;
  /** "(đã lược N câu)" nếu có. */
  trimmed: string;
}

export function parseExamTitle(rawTitle: string): ParsedExamTitle {
  const title = rawTitle.normalize("NFC");
  const trimmed = title.match(/\(đã lược[^)]*\)\s*$/i)?.[0].trim() ?? "";
  const term = title.match(/\bHK([12])\b/i)?.[0].toUpperCase() ?? "";
  const yearMatch = title.match(/20\d{2}(?:\s*[-–—]\s*20\d{2})?/);
  const yearToken = yearMatch ? yearMatch[0].replace(/\s*[-–—]\s*/, "–") : "";
  let t = title
    .replace(/\s*\(đã lược[^)]*\)\s*$/i, "")
    .replace(/^(?:thi thử tn|giữa hk\d|cuối hk\d)(?:\s*\d{4}(?:\s*[–—-]\s*\d{4})?)?\s*[–—-]\s*(?:(?:10|11|12)\s*[–—-]\s*)?/i, "")
    .replace(/^lop\d+_thithutn_/i, "")
    .replace(/_/g, " ");
  // Lần: "Lan 18", "Lần 3", "L05" → "Lần N"; mã đề tách riêng.
  let lan = "";
  t = t.replace(/\b(?:l[aầ]n|l)\s*0*(\d{1,3})\b/gi, (_m, n: string) => {
    lan = lan || `Lần ${Number(n)}`;
    return " ";
  });
  const maDeRe = /\bm[aã](?:\s*(?:đề|đe|de))?\s*0*(\d{1,4})\b/i;
  const maDe = t.match(maDeRe)?.[1]?.padStart(3, "0") ?? "";
  t = t.replace(new RegExp(maDeRe.source, "gi"), " ").replace(/\(\s*\)/g, " ").replace(/\bn[aăằ]m\s*h[oọ]c\b/gi, " ");
  t = t.replace(/(?<!\b(?:quang|ha|viet)\s)\b(?:nam\s+)?(?:năm\s+)?20\d{2}\s*(?:[-–—/]\s*20\d{2})?\b/gi, " ").replace(/\bthang\s*\d{1,2}\b/gi, " ");
  t = t.replace(/\.\d{2}\.\d{2}$/, "").replace(/\s[–—-]\s*(?=\()/g, " ").replace(/\s*[–—-]\s*$/g, "").replace(/\s{2,}/g, " ").trim();
  t = t.replace(/(?:\s[–—-]\s+)(?=[–—-]\s)/g, " ").replace(/\s{2,}/g, " ");
  t = accentize(t).replace(/\s[–—-]\s*(?=\()/g, " ").replace(/\s{2,}/g, " ").trim();
  // Tên nhập hỏng hoa/thường ("SảN PhẩM NhóM") → viết lại Title Case.
  if (/\p{Ll}\p{Lu}/u.test(t)) t = capitalizeWords(t);
  return { name: t || title, lan, maDe, term, yearToken, trimmed };
}

/** Tên hiển thị trên thẻ: "<Nơi> · Lần N · Mã đề X". */
export function displayExamName(title: string): string {
  const p = parseExamTitle(title);
  return [p.name, p.lan, p.maDe ? `Mã đề ${p.maDe}` : ""].filter(Boolean).join(" · ");
}

export type ExamTitleShelf = "giua-ki" | "cuoi-ki" | "thi-thu";

/**
 * Tên gốc chuẩn lưu trong CSDL: "<Loại>[ HKn] [năm] – [lớp – ]<Nơi>[ – Lần N][ – Mã đề X][ (đã lược…)]".
 * Chỉ dùng cho đề có tên "máy sinh"; đề thầy tự đặt giữ nguyên.
 */
export function standardExamTitle(title: string, shelf: ExamTitleShelf, grade: string): string {
  const p = parseExamTitle(title);
  const year = shelf === "thi-thu" ? p.yearToken.split("–").pop() ?? "" : p.yearToken;
  const head =
    shelf === "thi-thu"
      ? ["Thi thử TN", year].filter(Boolean).join(" ")
      : [shelf === "giua-ki" ? "Giữa" : "Cuối", p.term, year].filter(Boolean).join(" ");
  const tail = [p.name, p.lan, p.maDe ? `Mã đề ${p.maDe}` : ""].filter(Boolean).join(" – ");
  const middle = shelf === "thi-thu" ? "" : `${grade} – `;
  return `${head} – ${middle}${tail}${p.trimmed ? ` ${p.trimmed}` : ""}`
    .replace(/(?:\s[–—-]){2,}\s/g, " – ")
    .replace(/\s{2,}/g, " ");
}

/** Tên "máy sinh" cần chuẩn hoá (khác tên thầy tự đặt như "Kiểm tra giữa học kì 1 lần 1"). */
export function isMachineExamTitle(title: string): boolean {
  return /^(?:thi thử tn|giữa hk\d|cuối hk\d|lop\d+_thithutn_|đề phát triển đề minh)/i.test(title);
}
