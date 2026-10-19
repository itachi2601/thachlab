// Gộp lịch tuần: thachlab (dạy vật lí) + TKB Cao Thắng (cache JSON) + lịch cố định + lịch công tác khoa/giao ban, rồi xếp trượt băng/gym vào chỗ trống.
// CHẠY TRÊN MAC (cần .env.local). Chỉ đọc DB.
//   npx tsx .claude/skills/lich-tuan/scripts/lich-tuan.mts [--tuan YYYY-MM-DD] [--tkb file.json] [--cong-tac file.txt] [--ghi email]
//   --ghi <email>  ghi tuần này vào staff_week_plans của tài khoản đó (hiện ở /tai-khoan); không có cờ = chỉ in ra
// TKB Cao Thắng: file JSON [{weekday,start,end,title,where}] (mặc định scripts/data/lich-tuan/tkb-caothang.json).
// Lịch công tác: mặc định tự tải từ caothang.edu.vn; --cong-tac nhận văn bản dán tay nếu tải lỗi.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const arg = (k: string) => (process.argv.includes(k) ? process.argv[process.argv.indexOf(k) + 1] : undefined);
const envLocal = (k: string) => fs.readFileSync(path.join(root, ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const rules = JSON.parse(fs.readFileSync(path.join(root, ".claude/skills/lich-tuan/references/lich-co-dinh.json"), "utf8"));

type Ev = { weekday: number; start: string; end: string; title: string; where?: string; src: string; note?: string; lesson?: string };
const iso = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
const vnNow = new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Ho_Chi_Minh" }));
const base = arg("--tuan") ? new Date(`${arg("--tuan")}T00:00:00`) : vnNow;
const mon = new Date(base); mon.setDate(mon.getDate() - ((mon.getDay() + 6) % 7)); mon.setHours(0, 0, 0, 0);
const dayOf = (w: number) => { const d = new Date(mon); d.setDate(d.getDate() + w - 1); return d; };
const fmt = (d: Date) => `${String(d.getDate()).padStart(2, "0")}/${String(d.getMonth() + 1).padStart(2, "0")}`;
const toMin = (t: string) => { const [h, m] = t.split(":").map(Number); return h * 60 + m; };
const hhmm = (n: number) => `${String(Math.floor(n / 60)).padStart(2, "0")}:${String(n % 60).padStart(2, "0")}`;
const warn: string[] = [];
const evs: Ev[] = [];

// 1. cố định (+ buổi HSG KHTN 9: mốc bài theo scripts/data/btvn-hsg9/tuan.json, cùng nguồn với lộ trình HS)
const hsgFile = path.join(root, "scripts/data/btvn-hsg9/tuan.json");
const hsgTuan: { buoi: number; ngay: string; chu_de: string; btvn: string }[] = fs.existsSync(hsgFile) ? JSON.parse(fs.readFileSync(hsgFile, "utf8")).tuan : [];
for (const e of rules.co_dinh) {
  const ev: Ev = { ...e, src: "cố định" };
  if (/HSG/i.test(e.title)) {
    const d = dayOf(e.weekday);
    const row = hsgTuan.find((t) => t.ngay === fmt(d));
    ev.lesson = row ? `Buổi ${row.buoi}: ${row.chu_de}` : "Không có buổi trong lộ trình tuần này (xem tuan.json)";
    if (row?.btvn) ev.note = `BTVN đã giao: ${row.btvn}`;
  }
  evs.push(ev);
}
// Chi tiết HSG KHTN 9 trong tuần: tự học của HS (T2–T6), thầy xem tiến độ, gửi bài tuần sau
{
  const sat = fmt(dayOf(6));
  const i = hsgTuan.findIndex((t: any) => t.ngay === sat);
  const row: any = i >= 0 ? hsgTuan[i] : null;
  const next: any = i >= 0 ? hsgTuan[i + 1] : null;
  const prev: any = i > 0 ? hsgTuan[i - 1] : null;
  if (row?.tu_hoc) {
    // tự học T2–T6 trước buổi này (gửi từ thứ Bảy trước)
    const names = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu"];
    row.tu_hoc.forEach((t: string[], k: number) => {
      const w = names.indexOf(t[0]) + 1;
      if (w) evs.push({ weekday: w, start: "21:45", end: "22:00", title: `HSG 9 tự học: ${t[1]}`, src: "HSG KHTN 9", note: "Việc em làm ở nhà; thầy chỉ theo dõi" });
    });
  }
  if (row) evs.push({ weekday: 4, start: "22:00", end: "22:20", title: "HSG 9: xem tiến độ tự học trên web", src: "HSG KHTN 9", note: `Chuẩn bị buổi ${row?.buoi ?? ""}` });
  if (next) evs.push({ weekday: 6, start: "11:00", end: "11:20", title: `HSG 9: giao BTVN & tự học tuần tới (buổi ${next.buoi}: ${next.chu_de})`, src: "HSG KHTN 9", note: next.btvn });
}

// 2. thachlab
const sb = createClient(envLocal("NEXT_PUBLIC_SUPABASE_URL")!, envLocal("SUPABASE_SERVICE_ROLE_KEY")!);
const today = iso(mon);
const { data: courses, error } = await sb.from("thpt_courses").select("id,name,status,starts_at,ends_at,current_topic_id,classes(name)").neq("status", "closed");
if (error) throw error;
const live = (courses ?? []).filter((c: any) => (!c.starts_at || c.starts_at <= iso(dayOf(7))) && (!c.ends_at || c.ends_at >= today));
const { data: sch } = await sb.from("thpt_course_schedules").select("course_id,weekday,start_time,end_time,location").in("course_id", live.map((c: any) => c.id));
// Mốc bài: chủ đề tầng bài (parent_id null) theo khối, sắp theo sort_order → "Đã tới … · Tiếp …"
const { data: topics } = await sb.from("question_topics").select("id,name,grade,sort_order").is("parent_id", null).order("sort_order");
const lessonOf = (c: any): string => {
  const over = rules.buoi_day?.ghi_chu_khoa?.[String(c.id)];
  if (over) return over;
  if (!c.current_topic_id) return "Chưa đặt mốc bài (dashboard giáo viên → tiến trình)";
  const cur = (topics ?? []).find((t: any) => t.id === c.current_topic_id);
  if (!cur) return "Chưa đặt mốc bài";
  const next = (topics ?? []).find((t: any) => t.grade === cur.grade && t.sort_order > cur.sort_order);
  return `Đã tới: ${cur.name} · Tiếp: ${next ? next.name : "hết chương trình"}`;
};
for (const s of sch ?? []) {
  const c: any = live.find((x: any) => x.id === s.course_id);
  evs.push({ weekday: s.weekday, start: s.start_time.slice(0, 5), end: s.end_time.slice(0, 5), title: `Dạy ${c.name}`, where: s.location ?? "", src: "thachlab", lesson: lessonOf(c), note: rules.buoi_day?.nhip });
}

// 3. TKB Cao Thắng (cache)
const tkbFile = arg("--tkb") ?? path.join(root, "scripts/data/lich-tuan/tkb-caothang.json");
if (fs.existsSync(tkbFile)) for (const e of JSON.parse(fs.readFileSync(tkbFile, "utf8"))) evs.push({ ...e, src: "TKB Cao Thắng" });
else warn.push(`Chưa có TKB Cao Thắng (${tkbFile}) — portal cần đăng nhập, xem SKILL.md bước 2. Lịch dưới đây CHƯA tính giờ dạy ở Cao Thắng.`);

// 4. lịch công tác
const COMB: Record<string, string> = { acute: "\u0301", grave: "\u0300", tilde: "\u0303", circ: "\u0302", uml: "\u0308", caron: "\u030C", ring: "\u030A" };
const decode = (h: string) =>
  h.replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n)).replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
    .replace(/&([a-z])(acute|grave|tilde|circ|uml|caron|ring);/gi, (_, c, a) => (c + COMB[a.toLowerCase()]).normalize("NFC"))
    .replace(/&dstrok;/g, "đ").replace(/&Dstrok;/g, "Đ")
    .replace(/&([a-z]+);/gi, (m, n) => ({ amp: "&", quot: '"', ldquo: "“", rdquo: "”", lsquo: "‘", rsquo: "’", nbsp: " ", ndash: "–", hellip: "…" } as any)[n.toLowerCase()] ?? m);
let ct = "";
try {
  if (arg("--cong-tac")) ct = fs.readFileSync(arg("--cong-tac")!, "utf8");
  else {
    const list = await (await fetch("https://caothang.edu.vn/m/bai_viet/Lich-Cong-Tac-Tuan-14")).text();
    const key = `den-ngay-${fmt(dayOf(7)).replace("/", "")}${dayOf(7).getFullYear()}`.toLowerCase();
    const m = [...list.matchAll(/href="([^"]*Lich-cong-tac[^"]*)"/gi)].map((x) => x[1]).find((h) => h.toLowerCase().includes(key));
    if (!m) warn.push("Chưa thấy trang lịch công tác của tuần này trên caothang.edu.vn (có thể chưa đăng).");
    else ct = decode((await (await fetch(new URL(m, "https://caothang.edu.vn/m/").href)).text()).replace(/<(br|\/p|\/tr|\/li|\/div)[^>]*>/gi, "\n").replace(/<[^>]+>/g, " ")).replace(/[ \t]+/g, " ");
  }
} catch (e) { warn.push(`Không tải được lịch công tác: ${e}`); }
const ctLines: { day: number; text: string }[] = [];
let cur = 0;
for (const raw of ct.split("\n").map((l) => l.trim()).filter(Boolean)) {
  const mm = raw.match(/^TH[ỨỪ]\s+(HAI|BA|TƯ|NĂM|SÁU|BẢY)|^CHỦ NHẬT/i);
  if (mm) { cur = ({ HAI: 1, BA: 2, TƯ: 3, NĂM: 4, SÁU: 5, BẢY: 6 } as any)[(mm[1] ?? "").toUpperCase()] ?? 7; continue; }
  if (cur) ctLines.push({ day: cur, text: raw });
}
// mỗi mục bắt đầu bằng giờ "09h00"; gộp các dòng tiếp theo cho tới giờ kế
const blocks: { day: number; text: string }[] = [];
for (const l of ctLines) {
  if (/^\d{1,2}h\d{0,2}\b/.test(l.text) || !blocks.length || blocks[blocks.length - 1].day !== l.day) blocks.push({ ...l });
  else blocks[blocks.length - 1].text += " | " + l.text;
}
const kw = (rules.loc_lich_cong_tac as string[]).map((s) => s.toLowerCase());
const myName = ((rules.ten_thay ?? []) as string[]).map((s) => s.toLowerCase()); // mục có đích danh thầy: luôn giữ
for (const b of blocks) {
  const low = b.text.toLowerCase();
  const byName = myName.find((k) => low.includes(k));
  const hit = byName ?? kw.find((k) => low.includes(k));
  if (!hit) continue;
  const t = b.text.match(/^(\d{1,2})h(\d{0,2})/);
  const r = b.text.match(/^(\d{1,2})h(\d{0,2})\s*[-–]\s*(\d{1,2})h(\d{0,2})/);
  const p2 = (h: string, m: string) => `${h.padStart(2, "0")}:${(m || "00").padStart(2, "0")}`;
  const start = t ? p2(t[1], t[2]) : "08:00";
  const end = r ? p2(r[3], r[4]) : hhmm(toMin(start) + 90);
  const parts = b.text.split(" | ");
  const where = parts[0].match(/tại\s+(.+)$/i)?.[1];
  const title = parts.length > 1 ? parts[1] : parts[0];
  const tp = parts.slice(2).join(" | ");
  evs.push({ weekday: b.day, start, end, title: title.slice(0, 200), where, src: "lịch công tác", note: [byName ? "CÓ TÊN THẦY" : "", tp.slice(0, 300), !t ? "KHÔNG rõ giờ — kiểm bản gốc" : r ? "" : "giờ kết thúc ước 90 phút"].filter(Boolean).join(" · ") });
  console.error(`  [lịch công tác] "${title.slice(0, 60)}" khớp "${hit}"`);
}
if (ct && !blocks.length) warn.push("Tải được trang công tác nhưng không tách được mục — dán nội dung vào file rồi dùng --cong-tac.");

// 5. xếp thể thao vào chỗ trống
const PAD = 45; // đệm di chuyển/thay đồ trước-sau buổi tập
const busy = (w: number, a: number, b: number) => evs.some((e) => e.weekday === w && toMin(e.start) < b + PAD && toMin(e.end) > a - PAD);
const slots = (spec: any, kind: string, n: number, avoidDays: number[]) => {
  const placed: number[] = [];
  const order = [2, 4, 6, 3, 5, 7, 1].filter((d) => !avoidDays.includes(d)); // tránh T2 (họp) và T7 (dạy HSG) nếu được
  for (const d of order) {
    if (placed.length >= n) break;
    if (placed.some((p) => Math.abs(p - d) === 1) && kind === "Tập gym") continue; // gym cách ngày
    for (const g of spec.gio_uu_tien as string[]) {
      const [a, b] = g.split("-").map(toMin);
      const dur = spec.thoi_luong_phut;
      if (!busy(d, a, a + dur)) { evs.push({ weekday: d, start: hhmm(a), end: hhmm(a + dur), title: kind, src: "xếp tự động" }); placed.push(d); break; }
    }
  }
  if (placed.length < spec.min_buoi) warn.push(`${kind}: chỉ xếp được ${placed.length}/${spec.min_buoi} buổi tối thiểu — tuần quá kín.`);
  return placed;
};
const sk = slots(rules.the_thao.truot_bang, "Trượt băng", rules.the_thao.truot_bang.min_buoi, [1]);
slots(rules.the_thao.gym, "Tập gym", rules.the_thao.gym.min_buoi, []); // gym được cùng ngày với trượt băng (gym trước, trượt sau)

// 5b. thời gian phát triển thachlab: sau khi xếp thể thao, lấy khoảng trống dài nhất mỗi ngày (>= tối thiểu), tối đa `toi_da_phut`
{
  const pt = rules.phat_trien_thachlab ?? { min_buoi: 4, toi_thieu_phut: 120, toi_da_phut: 180, tu: "08:00", den: "21:30", dem: 15 };
  const cand: { w: number; a: number; b: number }[] = [];
  for (let w = 1; w <= 7; w++) {
    const ev = evs.filter((e) => e.weekday === w).map((e) => [toMin(e.start), toMin(e.end)]).sort((x, y) => x[0] - y[0]);
    let cur = toMin(pt.tu), best: [number, number] | null = null;
    for (const [a, b] of [...ev, [toMin(pt.den), toMin(pt.den)]]) {
      const gs = cur + (cur === toMin(pt.tu) ? 0 : pt.dem), ge = Math.min(a, toMin(pt.den)) - pt.dem;
      if (ge - gs >= pt.toi_thieu_phut && (!best || ge - gs > best[1] - best[0])) best = [gs, ge];
      cur = Math.max(cur, b);
    }
    if (best) cand.push({ w, a: best[0], b: Math.min(best[1], best[0] + pt.toi_da_phut) });
  }
  cand.sort((x, y) => y.b - y.a - (x.b - x.a));
  for (const c of cand.slice(0, pt.min_buoi)) evs.push({ weekday: c.w, start: hhmm(c.a), end: hhmm(c.b), title: "Phát triển thachlab", src: "xếp tự động" });
  if (cand.length < pt.min_buoi) warn.push(`Phát triển thachlab: chỉ có ${cand.length}/${pt.min_buoi} khoảng trống đủ ${pt.toi_thieu_phut} phút.`);
}

// 6. xuất
const NAME = ["", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"];
let out = `# Lịch tuần ${fmt(mon)}–${fmt(dayOf(7))}/${mon.getFullYear()}\n\n`;
for (let w = 1; w <= 7; w++) {
  out += `## ${NAME[w]} ${fmt(dayOf(w))}\n`;
  const day = evs.filter((e) => e.weekday === w).sort((a, b) => a.start.localeCompare(b.start));
  if (!day.length) out += "- (trống)\n";
  for (const e of day) {
    const clash = day.filter((o) => o !== e && toMin(o.start) < toMin(e.end) && toMin(o.end) > toMin(e.start));
    out += `- ${e.start}–${e.end} · ${e.title}${e.where ? ` (${e.where})` : ""} _[${e.src}]_${e.lesson ? ` — ${e.lesson}` : ""}${e.note && e.src !== "thachlab" && !e.lesson ? ` — ${e.note}` : ""}${clash.length ? " ⚠ TRÙNG GIỜ với " + clash.map((c) => c.title.slice(0, 30)).join("; ") : ""}\n`;
  }
  out += "\n";
}
if (warn.length) out += `## Cần chú ý\n${warn.map((w) => `- ${w}`).join("\n")}\n`;
if (arg("--ghi")) {
  const email = arg("--ghi")!.toLowerCase();
  let uid: string | undefined;
  for (let page = 1; page <= 10 && !uid; page++) {
    const { data, error: ue } = await sb.auth.admin.listUsers({ page, perPage: 200 });
    if (ue) throw ue;
    uid = (data.users as { id: string; email?: string }[]).find((u) => u.email?.toLowerCase() === email)?.id;
    if (data.users.length < 200) break;
  }
  if (!uid) throw new Error(`Không tìm thấy tài khoản ${email}`);
  const events = evs.map((e) => ({ ...e, clash: evs.some((o) => o !== e && o.weekday === e.weekday && toMin(o.start) < toMin(e.end) && toMin(o.end) > toMin(e.start)) }));
  const { error: we } = await sb.from("staff_week_plans").upsert({ user_id: uid, week_start: iso(mon), events, warnings: warn, updated_at: new Date().toISOString() });
  if (we) throw we;
  console.log(`Đã ghi ${events.length} mục vào staff_week_plans (${email}, tuần ${iso(mon)}).`);
}
const file = path.join(root, `scripts/data/lich-tuan/${iso(mon)}.md`);
fs.writeFileSync(file, out);
console.log(out + `\n→ ${file}`);
