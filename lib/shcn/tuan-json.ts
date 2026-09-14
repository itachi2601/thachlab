// Đọc file tuan-XX.json (dữ liệu đang dùng để sinh biên bản .docx nộp portal) thành dữ liệu
// của một dòng homeroom_weekly_sessions.
//
// Tên field trong các file tuần không thống nhất tuyệt đối (đã qua vài đợt chỉnh), nên mỗi
// trường chấp nhận vài cách viết. scripts/import-shcn-tuan.mjs giữ một bản sao của bảng alias
// này (script chạy bằng Node thuần, không qua bundler TypeScript) — sửa ở đây thì sửa cả bên đó.

export interface ParsedTuan {
  lopId: string;
  weekNo: number;
  metOn: string | null;
  announcements: { tieu_de: string; ghi_chu?: string }[];
  ethicsTopic: string;
  ethicsTaught: string[];
  headcount: number | null;
  presentCount: number | null;
}

type Json = Record<string, unknown>;

function pick(source: Json, keys: string[]): unknown {
  for (const key of keys) if (source[key] !== undefined && source[key] !== null && source[key] !== "") return source[key];
  return undefined;
}

function toInt(value: unknown): number | null {
  const number = Number(value);
  return Number.isFinite(number) ? Math.trunc(number) : null;
}

function toDate(value: unknown): string | null {
  if (typeof value !== "string" || !value.trim()) return null;
  const iso = value.trim().match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (iso) return `${iso[1]}-${iso[2]}-${iso[3]}`;
  // Dạng dd/mm/yyyy vẫn gặp trong vài file tuần cũ.
  const vn = value.trim().match(/^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$/);
  if (vn) return `${vn[3]}-${vn[2].padStart(2, "0")}-${vn[1].padStart(2, "0")}`;
  return null;
}

function toStringList(value: unknown): string[] {
  if (Array.isArray(value)) return value.map((item) => (typeof item === "string" ? item : String((item as Json)?.tieu_de ?? ""))).map((item) => item.trim()).filter(Boolean);
  if (typeof value === "string") return value.split(/[;\n]/).map((item) => item.trim()).filter(Boolean);
  return [];
}

function toAnnouncements(value: unknown): { tieu_de: string; ghi_chu?: string }[] {
  if (!Array.isArray(value)) return [];
  return value
    .map((item) => {
      if (typeof item === "string") return { tieu_de: item.trim() };
      const row = item as Json;
      const title = String(pick(row, ["tieu_de", "tieu_de_ngan", "noi_dung", "ten", "title"]) ?? "").trim();
      const note = String(pick(row, ["ghi_chu", "chi_tiet", "note"]) ?? "").trim();
      return note ? { tieu_de: title, ghi_chu: note } : { tieu_de: title };
    })
    .filter((item) => item.tieu_de)
    .slice(0, 5);
}

/** Ném lỗi khi thiếu số tuần — các trường còn lại thiếu thì để trống, GVCN bổ sung trên web. */
export function parseTuanJson(raw: unknown): ParsedTuan {
  if (!raw || typeof raw !== "object") throw new Error("File JSON không đúng định dạng.");
  const source = raw as Json;
  const weekNo = toInt(pick(source, ["tuan_so", "tuan", "week", "so_tuan"]));
  if (!weekNo) throw new Error("Không đọc được số tuần (tuan_so).");
  return {
    lopId: String(pick(source, ["lop_id", "lop", "ma_lop", "class_label"]) ?? "").trim(),
    weekNo,
    metOn: toDate(pick(source, ["ngay_sinh_hoat", "ngay", "ngay_shcn", "date"])),
    announcements: toAnnouncements(pick(source, ["noi_dung_pho_bien", "noi_dung", "pho_bien", "muc"])),
    ethicsTopic: String(pick(source, ["gdnn_chu_de", "chu_de", "gddd_chu_de"]) ?? "").trim(),
    ethicsTaught: toStringList(pick(source, ["gdnn_da_day", "da_day", "gddd_da_day", "trong_tam"])),
    headcount: toInt(pick(source, ["si_so", "siso", "tong_so"])),
    presentCount: toInt(pick(source, ["co_mat", "comat", "hien_dien"])),
  };
}
