// Nạp nội dung sinh hoạt tuần từ các file tuan-XX.json (dữ liệu đang dùng để sinh biên bản
// .docx nộp portal) vào bảng homeroom_weekly_sessions.
//
// App export tĩnh, không có API route dùng service role key ở production — script này CHỈ chạy
// cục bộ trên máy thầy/cô, SAU KHI đã chạy docs/supabase-migration-shcn.sql:
//
//   SUPABASE_SERVICE_ROLE_KEY=xxx NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co \
//     node scripts/import-shcn-tuan.mjs --lop CD-CK-26C ~/Documents/CTTC/.../ND-SHCN/tuan-*.json
//
// Chọn lớp bằng --lop <class_label hoặc tên khóa> (khớp không phân biệt hoa thường, cũng nhận
// lop_id ghi trong chính file JSON) hoặc --course-id <id> nếu biết sẵn id khóa.
// Thêm --dry-run để chỉ xem sẽ ghi gì mà không ghi thật.
//
// Lấy SUPABASE_SERVICE_ROLE_KEY ở Supabase Dashboard → Settings → API → service_role
// (secret, KHÔNG commit, KHÔNG đưa vào .env.local dùng chung với NEXT_PUBLIC_*, KHÔNG dán vào chat).
//
// Chạy lại an toàn nhiều lần: upsert theo (course_id, week_no).

import fs from "node:fs";
import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  console.error("Thiếu NEXT_PUBLIC_SUPABASE_URL hoặc SUPABASE_SERVICE_ROLE_KEY trong biến môi trường.");
  process.exit(1);
}

const argv = process.argv.slice(2);
const flag = (name) => {
  const index = argv.indexOf(name);
  return index >= 0 ? argv[index + 1] : undefined;
};
const dryRun = argv.includes("--dry-run");
const lopArg = flag("--lop");
const courseIdArg = flag("--course-id");
const files = argv.filter((item, index) => item.endsWith(".json") && argv[index - 1] !== "--lop" && argv[index - 1] !== "--course-id");

if (!files.length) {
  console.error("Chưa chỉ định file JSON nào. Ví dụ: node scripts/import-shcn-tuan.mjs --lop CD-CK-26C ND-SHCN/tuan-*.json");
  process.exit(1);
}

// ---------- Đọc JSON (giữ đồng bộ với lib/shcn/tuan-json.ts) ----------
const pick = (source, keys) => {
  for (const key of keys) if (source[key] !== undefined && source[key] !== null && source[key] !== "") return source[key];
  return undefined;
};
const toInt = (value) => (Number.isFinite(Number(value)) ? Math.trunc(Number(value)) : null);
const toDate = (value) => {
  if (typeof value !== "string" || !value.trim()) return null;
  const iso = value.trim().match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (iso) return `${iso[1]}-${iso[2]}-${iso[3]}`;
  const vn = value.trim().match(/^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$/);
  return vn ? `${vn[3]}-${vn[2].padStart(2, "0")}-${vn[1].padStart(2, "0")}` : null;
};
const toStringList = (value) => {
  if (Array.isArray(value)) return value.map((item) => (typeof item === "string" ? item : String(item?.tieu_de ?? ""))).map((item) => item.trim()).filter(Boolean);
  if (typeof value === "string") return value.split(/[;\n]/).map((item) => item.trim()).filter(Boolean);
  return [];
};
const toAnnouncements = (value) => {
  if (!Array.isArray(value)) return [];
  return value
    .map((item) => {
      if (typeof item === "string") return { tieu_de: item.trim() };
      const title = String(pick(item, ["tieu_de", "tieu_de_ngan", "noi_dung", "ten", "title"]) ?? "").trim();
      const note = String(pick(item, ["ghi_chu", "chi_tiet", "note"]) ?? "").trim();
      return note ? { tieu_de: title, ghi_chu: note } : { tieu_de: title };
    })
    .filter((item) => item.tieu_de)
    .slice(0, 5);
};

function parseTuan(raw) {
  const weekNo = toInt(pick(raw, ["tuan_so", "tuan", "week", "so_tuan"]));
  if (!weekNo) throw new Error("không đọc được số tuần (tuan_so)");
  return {
    lopId: String(pick(raw, ["lop_id", "lop", "ma_lop", "class_label"]) ?? "").trim(),
    week_no: weekNo,
    met_on: toDate(pick(raw, ["ngay_sinh_hoat", "ngay", "ngay_shcn", "date"])),
    announcements: toAnnouncements(pick(raw, ["noi_dung_pho_bien", "noi_dung", "pho_bien", "muc"])),
    ethics_topic: String(pick(raw, ["gdnn_chu_de", "chu_de", "gddd_chu_de"]) ?? "").trim(),
    ethics_taught: toStringList(pick(raw, ["gdnn_da_day", "da_day", "gddd_da_day", "trong_tam"])),
    headcount: toInt(pick(raw, ["si_so", "siso", "tong_so"])),
    present_count: toInt(pick(raw, ["co_mat", "comat", "hien_dien"])),
  };
}

// ---------- Tìm khóa (lớp chủ nhiệm) ----------
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

async function resolveCourseId(label) {
  if (courseIdArg) return Number(courseIdArg);
  const key = String(label ?? "").trim().toLowerCase();
  if (!key) throw new Error("chưa có --lop và file JSON cũng không ghi lop_id");
  const { data, error } = await supabase
    .from("course_offerings")
    .select("id, name, class_label, school_year, subjects!inner(code)")
    .eq("subjects.code", "gddd-ptnn");
  if (error) throw error;
  const matches = (data ?? []).filter(
    (row) => row.class_label?.toLowerCase() === key || row.name?.toLowerCase() === key,
  );
  if (!matches.length) {
    const available = (data ?? []).map((row) => `${row.class_label || row.name} (id ${row.id})`).join(", ") || "chưa có lớp chủ nhiệm nào";
    throw new Error(`không tìm thấy lớp "${label}". Các lớp hiện có: ${available}`);
  }
  if (matches.length > 1) {
    throw new Error(`có ${matches.length} lớp trùng tên "${label}" — chỉ định --course-id (${matches.map((row) => row.id).join(", ")})`);
  }
  return matches[0].id;
}

let failed = 0;
for (const file of files) {
  try {
    const parsed = parseTuan(JSON.parse(fs.readFileSync(file, "utf8")));
    const courseId = await resolveCourseId(lopArg ?? parsed.lopId);
    const row = {
      course_id: courseId,
      week_no: parsed.week_no,
      met_on: parsed.met_on,
      announcements: parsed.announcements,
      ethics_topic: parsed.ethics_topic,
      ethics_taught: parsed.ethics_taught,
      headcount: parsed.headcount,
      present_count: parsed.present_count,
      updated_at: new Date().toISOString(),
    };
    if (dryRun) {
      console.log(`[thử] ${file} → khóa ${courseId}, tuần ${row.week_no}, ${row.announcements.length} mục, "${row.ethics_topic}"`);
      continue;
    }
    const { error } = await supabase.from("homeroom_weekly_sessions").upsert(row, { onConflict: "course_id,week_no" });
    if (error) throw error;
    console.log(`Đã nạp tuần ${row.week_no} (khóa ${courseId}) từ ${file}`);
  } catch (cause) {
    failed += 1;
    console.error(`Lỗi ở ${file}: ${cause instanceof Error ? cause.message : cause}`);
  }
}

process.exit(failed ? 1 : 0);
