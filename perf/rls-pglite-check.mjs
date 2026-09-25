// Kiểm tra cú pháp migration RLS + RPC trên pglite (Postgres trong WASM, không đụng DB thật).
//   node perf/rls-pglite-check.mjs
// Thứ tự: stub schema (bảng rỗng đúng cột, hàm stub, auth.uid()) → migration RLS →
// rollback RLS → migration RLS lần 2 (idempotent) → migration RPC → rollback RPC (khối
// comment cuối file, bỏ dấu "-- ").
import { PGlite } from "@electric-sql/pglite";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => fs.readFileSync(path.join(root, p), "utf8");

const steps = [
  ["stub schema", read("perf/pglite-stub-schema.sql")],
  ["migration RLS", read("supabase/migrations/20260925140000_perf_rls.sql")],
  ["rollback RLS", read("perf/rollback/20260925140000_perf_rls.down.sql")],
  ["migration RLS (lần 2, idempotent)", read("supabase/migrations/20260925140000_perf_rls.sql")],
  ["migration RPC", read("supabase/migrations/20260925130000_perf_rpc_gv.sql")],
  ["rollback RPC", read("supabase/migrations/20260925130000_perf_rpc_gv.sql").split("-- ROLLBACK")[1].split("\n").map((l) => l.replace(/^-- ?/, "")).filter((l) => /^(begin;|drop function|commit;)/.test(l)).join("\n")],
  ["migration RPC (lần 2)", read("supabase/migrations/20260925130000_perf_rpc_gv.sql")],
];

const db = new PGlite();
let failed = false;
for (const [label, sql] of steps) {
  const t0 = Date.now();
  try {
    await db.exec(sql);
    console.log(`✓ ${label} (${Date.now() - t0} ms)`);
  } catch (error) {
    failed = true;
    console.log(`✗ ${label}: ${error.message}`);
    break;
  }
}
if (!failed) {
  const { rows } = await db.query(
    "select count(*)::int as n, count(*) filter (where qual ~ 'auth\\.uid\\(\\)' and qual !~ '\\( ?SELECT auth\\.uid\\(\\)')::int as bare from pg_policies where schemaname = 'public'",
  );
  console.log(`policy trong pglite: ${rows[0].n}, còn auth.uid() trần trong qual: ${rows[0].bare}`);
  const fns = await db.query(
    "select count(*)::int as n from pg_proc p join pg_namespace n on n.oid = p.pronamespace where n.nspname = 'public' and p.prokind = 'f' and p.provolatile = 's' and prosecdef and pg_get_functiondef(p.oid) ~ '[^t] auth\\.uid\\(\\)'",
  );
  console.log(`hàm helper stable còn auth.uid() trần (không đứng sau select): ${fns.rows[0].n}`);
}
await db.close();
process.exit(failed ? 1 : 0);
