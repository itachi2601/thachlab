// Báo cáo CHỈ ĐỌC: tìm tài khoản học sinh có vẻ đã bị bỏ (em không đăng nhập lại được nên thầy tạo tài khoản mới).
//   npx tsx scripts/bao-cao-tai-khoan-bo.mts
// Dấu hiệu "bị bỏ": cùng họ tên (bỏ dấu, không phân biệt hoa/thường) hoặc cùng student_code với một tài khoản MỚI HƠN,
// và tài khoản cũ không đăng nhập sau khi tài khoản mới được tạo. Ghi scripts/logs/tai-khoan-bo-<stamp>.json để duyệt.
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const env = (k: string) => fs.readFileSync(path.resolve(scriptDir, "..", ".env.local"), "utf8").split("\n").find((l) => l.startsWith(`${k}=`))?.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL")!, env("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });

const users: any[] = [];
for (let page = 1; ; page++) {
  const { data, error } = await sb.auth.admin.listUsers({ page, perPage: 1000 });
  if (error) throw error;
  users.push(...data.users);
  if (data.users.length < 1000) break;
}
const profs: any[] = [];
for (let from = 0; ; from += 1000) {
  const { data, error } = await sb.from("profiles").select("id,full_name,class_name,student_code,role").eq("role", "student").range(from, from + 999);
  if (error) throw error;
  profs.push(...(data ?? []));
  if (!data || data.length < 1000) break;
}
const uMap = new Map(users.map((u) => [u.id, u]));
const norm = (s: string | null) => (s ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/gi, "d").toLowerCase().replace(/\s+/g, " ").trim();

type Row = { id: string; name: string; code: string | null; class_name: string | null; email: string; created: string; last_sign_in: string | null; confirmed: boolean };
const rows: Row[] = profs.map((p) => {
  const u = uMap.get(p.id);
  return { id: p.id, name: p.full_name ?? "", code: p.student_code, class_name: p.class_name, email: u?.email ?? "", created: u?.created_at ?? "", last_sign_in: u?.last_sign_in_at ?? null, confirmed: !!u?.email_confirmed_at };
});

const groups = new Map<string, Row[]>();
for (const r of rows) {
  const keys = [norm(r.name) && "n:" + norm(r.name), r.code && "c:" + r.code].filter(Boolean) as string[];
  for (const k of keys) groups.set(k, [...(groups.get(k) ?? []), r]);
}
const abandoned = new Map<string, { old: Row; newer: Row; why: string }>();
for (const [k, g] of groups) {
  if (g.length < 2) continue;
  const sorted = [...g].sort((a, b) => a.created.localeCompare(b.created));
  const newest = sorted[sorted.length - 1];
  for (const o of sorted.slice(0, -1)) {
    if (o.id === newest.id) continue;
    const dead = !o.last_sign_in || o.last_sign_in < newest.created;
    if (dead) abandoned.set(o.id, { old: o, newer: newest, why: k.startsWith("c:") ? "trùng mã HS" : "trùng họ tên" });
  }
}

const out = [...abandoned.values()].map((x) => ({ id: x.old.id, name: x.old.name, class: x.old.class_name, email: x.old.email, created: x.old.created, last_sign_in: x.old.last_sign_in, why: x.why, newer_id: x.newer.id, newer_email: x.newer.email, newer_created: x.newer.created, newer_last_sign_in: x.newer.last_sign_in }));
const neverIn = rows.filter((r) => !r.last_sign_in && !abandoned.has(r.id) && !/^hs\.test/.test(r.email));
const stamp = new Date().toISOString().replace(/[:.]/g, "-");
const file = path.join(scriptDir, "logs", `tai-khoan-bo-${stamp}.json`);
fs.mkdirSync(path.dirname(file), { recursive: true });
fs.writeFileSync(file, JSON.stringify({ abandoned: out, neverSignedIn: neverIn }, null, 2));
console.log(`HS: ${rows.length} · nghi bị bỏ (có bản mới hơn): ${out.length} · chưa từng đăng nhập (không trùng): ${neverIn.length}`);
for (const o of out) console.log(`${o.name} | ${o.class ?? ""} | ${o.email} | tạo ${o.created.slice(0, 10)} | vào cuối ${o.last_sign_in?.slice(0, 10) ?? "chưa"} → mới: ${o.newer_email} (${o.newer_created.slice(0, 10)}, vào cuối ${o.newer_last_sign_in?.slice(0, 10) ?? "chưa"}) [${o.why}]`);
console.log(`Chi tiết: ${file}`);
