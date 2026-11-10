// Tải nội dung WEB THẬT (DB, chỉ ĐỌC) của một cuốn sách về book/cache/<lesson_id>.json — nguồn duy nhất của pipeline book/.
//   npx tsx book/lay-noi-dung.mts <mã>                     mọi bài trong hồ sơ book/sach/<mã>.json (2 truy vấn cho cả cuốn)
//   npx tsx book/lay-noi-dung.mts --moi <mã> <lớp> <lesson_id>   tạo hồ sơ nháp từ CHƯƠNG chứa bài đó rồi tải luôn
// Cần mạng + .env.local (service role) → chạy trong tab terminal trên Mac; sandbox Bash chặn *.supabase.co.
// Thường không gọi trực tiếp: `cd book && python3 sach.py lech <mã>` gọi script này rồi so với sổ khoá.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const fail = (m: string): never => { console.error("✗ " + m); process.exit(1); };
const env = (k: string) =>
  process.env[k] ??
  (fs.existsSync(path.join(root, ".env.local"))
    ? fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").find((l) => l.startsWith(k + "="))?.slice(k.length + 1).trim()
    : undefined);

const argv = process.argv.slice(2);
const moi = argv[0] === "--moi";
const ma = moi ? argv[1] : argv[0];
if (!ma || (moi && argv.length < 4)) fail("cách dùng: npx tsx book/lay-noi-dung.mts <mã>  |  --moi <mã> <lớp> <lesson_id>");
const hoSoPath = path.join(here, "sach", `${ma}.json`);

const url = env("NEXT_PUBLIC_SUPABASE_URL"), key = env("SUPABASE_SERVICE_ROLE_KEY");
if (!url || !key) fail("thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local");
const sb = createClient(url!, key!, { auth: { persistSession: false, autoRefreshToken: false } });

if (moi) {
  if (fs.existsSync(hoSoPath)) fail(`đã có ${path.relative(root, hoSoPath)} — không ghi đè hồ sơ`);
  const lop = Number(argv[2]), lid = Number(argv[3]);
  const one = await sb.from("lessons").select("chapter_id").eq("id", lid).single();
  if (one.error) fail(one.error.message);
  const chapterId = (one.data as { chapter_id: number }).chapter_id;
  const [ch, ls] = await Promise.all([
    sb.from("chapters").select("title, sort_order").eq("id", chapterId).single(),
    sb.from("lessons").select("id, title, sort_order").eq("chapter_id", chapterId).eq("published", true).order("sort_order"),
  ]);
  if (ch.error || ls.error) fail((ch.error ?? ls.error)!.message);
  const title = (ch.data as { title: string }).title;
  const m = title.match(/^Chương\s+(\d+|[IVXLC]+)\s*[.:–-]?\s*(.*)$/i);
  const laMa = (s: string) => [...s.toUpperCase()].reduce((a, c, i, r) => { const v = { I: 1, V: 5, X: 10, L: 50, C: 100 }[c] ?? 0, n = { I: 1, V: 5, X: 10, L: 50, C: 100 }[r[i + 1]] ?? 0; return a + (v < n ? -v : v); }, 0);
  const so = m ? (/^\d+$/.test(m[1]) ? Number(m[1]) : laMa(m[1])) : (ch.data as { sort_order: number }).sort_order;
  const hoSo = {
    _ghi_chu: `Hồ sơ nháp sinh ${new Date().toISOString().slice(0, 10)} từ chương "${title}". Kiểm lại chuong/ten/lessons; các trường tuỳ chọn (bia, dang_chung, tiet, ban_do_chuong, tu_danh_gia) xem book/sach/l10-ch2-dong-hoc.json.`,
    lop, chuong: so, ten: m?.[2] || title, phu_de: "",
    tep: ma, lessons: (ls.data as { id: number }[]).map((l) => l.id),
  };
  fs.writeFileSync(hoSoPath, JSON.stringify(hoSo, null, 2) + "\n");
  console.log(`Đã tạo ${path.relative(root, hoSoPath)}: Chương ${so} · ${hoSo.ten} · ${hoSo.lessons.length} bài`);
  (ls.data as { id: number; title: string }[]).forEach((l) => console.log(`  ${l.id}  ${l.title}`));
}

if (!fs.existsSync(hoSoPath)) fail(`không có hồ sơ ${path.relative(root, hoSoPath)}`);
const ids: number[] = JSON.parse(fs.readFileSync(hoSoPath, "utf8")).lessons.map(Number);

const [les, items] = await Promise.all([
  sb.from("lessons").select("id, title, published").in("id", ids),
  sb.from("lesson_items").select("lesson_id, kind, body_html, questions").in("lesson_id", ids).in("kind", ["ly_thuyet", "bai_tap_mau"]),
]);
if (les.error || items.error) fail((les.error ?? items.error)!.message);

type Item = { lesson_id: number; kind: string; body_html: string | null; questions: Record<string, unknown>[] | null };
const FIELDS = ["label", "topic", "problem_html", "analysis_html", "solution_html"]; // khớp sach.BTM_FIELDS
const cacheDir = path.join(here, "cache");
fs.mkdirSync(cacheDir, { recursive: true });
let loi = 0;
for (const id of ids) {
  const l = (les.data as { id: number; title: string; published: boolean }[]).find((x) => x.id === id);
  const its = (items.data as Item[]).filter((x) => x.lesson_id === id);
  const lt = its.filter((x) => x.kind === "ly_thuyet"), btm = its.filter((x) => x.kind === "bai_tap_mau");
  if (!l || lt.length !== 1 || !lt[0].body_html) { console.error(`✗ bài ${id}: ${!l ? "không có trong DB" : `${lt.length} mục lý thuyết (cần đúng 1, có nội dung)`}`); loi++; continue; }
  if (btm.length > 1) { console.error(`✗ bài ${id}: ${btm.length} mục bài tập mẫu (cần ≤ 1)`); loi++; continue; }
  // chỉ Dạng có cấu trúc (problem_html) mới vào sách; mục tự luận / dạng cũ không có problem_html thì bỏ
  const dang = (btm[0]?.questions ?? []).filter((q) => q.problem_html).map((q) => Object.fromEntries(FIELDS.map((k) => [k, q[k] ?? ""])));
  fs.writeFileSync(path.join(cacheDir, `${id}.json`), JSON.stringify({ id, title: l.title, published: l.published, theory: lt[0].body_html, dang_bai: dang, tai_luc: new Date().toISOString() }));
  console.log(`  ${id}  ${l.title} · lý thuyết ${(lt[0].body_html.length / 1024).toFixed(0)} KB · ${dang.length} dạng${l.published ? "" : " · CHƯA công bố"}`);
}
if (loi) fail(`${loi} bài lỗi — chưa đủ nội dung để dựng sách`);
console.log(`✓ ${ids.length} bài → book/cache/`);
