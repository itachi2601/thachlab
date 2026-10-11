// Đọc public/data/exam-index.json (sinh bởi scripts/build-content.mjs) lúc render trang /de-thi.
// Chỉ metadata — không câu hỏi/đáp án. Không gọi Supabase.
import { readFileSync } from "node:fs";
import { join } from "node:path";

export type ExamShelf = "giua-ki" | "cuoi-ki" | "thi-thu";

export interface ExamIndexItem {
  id: number;
  /** Tên đã bỏ tiền tố loại đề và hậu tố "(đã lược…)". */
  name: string;
  shelf: ExamShelf;
  grade: string;
  year: string;
  /** "HK1" / "HK2" khi tên đề có ghi, ngược lại rỗng. */
  term: string;
  questionCount: number;
  durationMinutes: number;
}

interface RawExam {
  id: number;
  title: string;
  shelf: string;
  grade: string;
  year: string;
  questionCount: number;
  durationMinutes: number;
}

const SHELVES = new Set<string>(["giua-ki", "cuoi-ki", "thi-thu"]);

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

function cleanName(title: string): string {
  let t = title
    .replace(/\s*\(đã lược[^)]*\)\s*$/i, "")
    .replace(/^(?:thi thử tn|giữa hk\d|cuối hk\d)(?:\s*\d{4}(?:\s*[–—-]\s*\d{4})?)?\s*[–—-]\s*(?:(?:10|11|12)\s*[–—-]\s*)?/i, "")
    .replace(/^lop\d+_thithutn_/i, "")
    .replace(/_/g, " ");
  // Lần: "Lan 18", "Lần 3", "L05" (đứng riêng, sau tên) → "Lần N"; mã đề giữ lại.
  let lan = "";
  t = t.replace(/\b(?:l[aầ]n|l)\s*0*(\d{1,3})\b/gi, (_m, n: string) => {
    lan = lan || `Lần ${Number(n)}`;
    return " ";
  });
  const maDe = t.match(/\bm[aã]\s*đ?d?e?\s*(?:de\s*)?(\d{2,4})\b/i);
  t = t.replace(/\bm[aã] đ?d?e\s*\d{2,4}\b/gi, " ");
  // Năm / năm học và chữ "Nam" đứng trước năm: đã hiện ở dòng dưới thẻ.
  t = t.replace(/\b(?:nam\s+)?(?:năm\s+)?20\d{2}\s*(?:[-–—/]\s*20\d{2})?\b/gi, " ").replace(/\bthang\s*\d{1,2}\b/gi, " ");
  t = t.replace(/\.\d{2}\.\d{2}$/, "").replace(/\s[–—-]\s*(?=\()/g, " ").replace(/\s*[–—-]\s*$/g, "").replace(/\s{2,}/g, " ").trim();
  t = accentize(t).replace(/\s[–—-]\s*(?=\()/g, " ").replace(/\s{2,}/g, " ").trim();
  const parts = [t || title, lan, maDe ? `Mã đề ${maDe[1]}` : ""].filter(Boolean);
  return parts.join(" · ");
}

export function readExamIndex(): ExamIndexItem[] {
  try {
    const raw = readFileSync(join(process.cwd(), "public", "data", "exam-index.json"), "utf8");
    const parsed = JSON.parse(raw) as { exams?: RawExam[] };
    if (!Array.isArray(parsed.exams)) return [];
    return parsed.exams
      .filter((e) => e && typeof e.id === "number" && SHELVES.has(e.shelf) && !/^luyện tập/i.test(e.title))
      .map((e) => ({
        id: e.id,
        name: cleanName(e.title) || e.title,
        shelf: e.shelf as ExamShelf,
        grade: e.grade,
        year: e.year,
        term: e.title.match(/\bHK([12])\b/i)?.[0].toUpperCase() ?? "",
        questionCount: e.questionCount,
        durationMinutes: e.durationMinutes,
      }));
  } catch {
    return [];
  }
}
