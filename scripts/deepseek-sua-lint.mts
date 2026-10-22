#!/usr/bin/env -S npx tsx
/**
 * DeepSeek sửa lỗi ESLint (nợ kỹ thuật React 19: set-state-in-effect, refs, purity…) — phần "code thường,
 * không đụng schema/RLS" mà AGENTS.md giao cho model ngoài. Claude (agent `kiem-code`) soát diff trước khi commit.
 *
 * Quy trình mỗi file:
 *   1. Lấy lỗi ESLint của file (eslint -f json).
 *   2. Gửi nguyên văn file + danh sách lỗi cho DeepSeek, yêu cầu sửa TỐI THIỂU, giữ hành vi, trả JSON {file, notes}.
 *   3. Ghi bản đề xuất + diff vào scripts/logs/deepseek-lint/<mốc>/ (luôn, kể cả --apply).
 *   4. --apply: ghi vào cây làm việc, chạy lại eslint cho file đó; còn lỗi → hoàn tác (git checkout) và ghi log.
 *      Cuối lượt chạy `tsc --noEmit` một lần; đỏ → hoàn tác MỌI file đã ghi trong lượt (đề xuất vẫn còn trong logs).
 *   5. Nhớ file đã thử (theo sha nội dung) trong scripts/logs/deepseek-lint/da-thu.json, lượt sau bỏ qua (--force để thử lại).
 *
 * Dùng:
 *   npx tsx scripts/deepseek-sua-lint.mts                      # dry-run 3 file, chỉ ghi đề xuất vào logs
 *   npx tsx scripts/deepseek-sua-lint.mts --limit 10 --apply   # ghi thật 10 file, có kiểm eslint + tsc
 *   npx tsx scripts/deepseek-sua-lint.mts --files components/admin/AdminSearch.tsx --apply
 *   npx tsx scripts/deepseek-sua-lint.mts --rule react-hooks/set-state-in-effect --max-lines 600
 *
 * Tuỳ chọn: --limit N (3) · --apply · --force · --files a,b · --rule <ruleId> · --max-lines N (900, file dài hơn bỏ qua —
 * model rẻ viết lại file lớn dễ hỏng, để Claude tách file trước) · --dirs "app components lib services features hooks"
 *
 * Env: DEEPSEEK_API_KEY (bắt buộc), DEEPSEEK_MODEL (mặc định "deepseek-flash" — tên model đổi theo thời gian, xem
 * api-docs.deepseek.com trước khi đổi; "deepseek-chat" đã khai tử 24/7/2026), DEEPSEEK_MAX_TOKENS (16000).
 * Chỉ gửi mã nguồn, không gửi .env hay dữ liệu học sinh.
 */
import { execFileSync, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { readEnvLocal, requireEnv } from "./lib/env.mts";

type LintMsg = { ruleId: string | null; severity: number; line: number; column: number; message: string };
type LintFile = { filePath: string; messages: LintMsg[] };
type Tried = Record<string, { sha: string; at: string; outcome: string; errorsBefore: number; errorsAfter?: number }>;

const ROOT = process.cwd();
const LOG_ROOT = join(ROOT, "scripts", "logs", "deepseek-lint");
const TRIED_PATH = join(LOG_ROOT, "da-thu.json");
const API_URL = "https://api.deepseek.com/chat/completions";

// ---------- tham số ----------
const argv = process.argv.slice(2);
const flag = (n: string) => argv.includes(`--${n}`);
const opt = (n: string, d: string) => {
  const i = argv.indexOf(`--${n}`);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : d;
};
const APPLY = flag("apply");
const FORCE = flag("force");
const LIMIT = Number(opt("limit", "3"));
const MAX_LINES = Number(opt("max-lines", "900"));
const ONLY_RULE = opt("rule", "");
const FILES = opt("files", "").split(",").map((s) => s.trim()).filter(Boolean);
const DIRS = opt("dirs", "app components lib services features hooks").split(/\s+/).filter(Boolean);

const MODEL = readEnvLocal("DEEPSEEK_MODEL") ?? "deepseek-flash";
const MAX_TOKENS = Number(readEnvLocal("DEEPSEEK_MAX_TOKENS") ?? "16000");

const stamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
const RUN_DIR = join(LOG_ROOT, stamp);
mkdirSync(RUN_DIR, { recursive: true });

const sha = (s: string) => createHash("sha256").update(s).digest("hex").slice(0, 16);
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

function loadTried(): Tried {
  if (!existsSync(TRIED_PATH)) return {};
  try {
    return JSON.parse(readFileSync(TRIED_PATH, "utf8")) as Tried;
  } catch {
    return {};
  }
}
function saveTried(t: Tried) {
  writeFileSync(TRIED_PATH, JSON.stringify(t, null, 2));
}

// ---------- eslint ----------
function runEslintJson(targets: string[]): LintFile[] {
  const r = spawnSync("npx", ["eslint", "-f", "json", ...targets], { cwd: ROOT, encoding: "utf8", maxBuffer: 64e6 });
  // eslint exit 1 khi có lỗi — vẫn có JSON ở stdout. exit 2 = lỗi cấu hình.
  if (r.status === 2 || !r.stdout.trim()) {
    console.error("ESLint lỗi cấu hình/không chạy được:\n" + (r.stderr || r.stdout).slice(0, 2000));
    process.exit(2);
  }
  const start = r.stdout.indexOf("[");
  return JSON.parse(r.stdout.slice(start)) as LintFile[];
}
function errorsOf(f: LintFile): LintMsg[] {
  return f.messages.filter((m) => m.severity === 2 && (!ONLY_RULE || m.ruleId === ONLY_RULE));
}

// ---------- git ----------
function gitClean(rel: string): boolean {
  const out = execFileSync("git", ["status", "--porcelain", "--", rel], { cwd: ROOT, encoding: "utf8" });
  return out.trim() === "";
}
function gitRestore(rel: string) {
  execFileSync("git", ["checkout", "--", rel], { cwd: ROOT });
}
function gitDiff(rel: string): string {
  return execFileSync("git", ["diff", "--", rel], { cwd: ROOT, encoding: "utf8", maxBuffer: 64e6 });
}

// ---------- DeepSeek ----------
const SYSTEM = `Bạn là kỹ sư React 19 / Next.js 16 / TypeScript strict, sửa nợ kỹ thuật cho một dự án giáo dục.
Nhiệm vụ: sửa ĐÚNG các lỗi ESLint được liệt kê trong MỘT file, với thay đổi tối thiểu. Quy tắc bắt buộc:
1. Giữ nguyên hành vi người dùng nhìn thấy, props, export, tên hàm công khai, chuỗi tiếng Việt, comment hiện có.
2. Không thêm dependency, không đổi import "@/..." sang đường dẫn khác, không sửa file khác, không viết lại toàn bộ component.
3. Không dùng eslint-disable, không đổi cấu hình lint, không ép kiểu "as any", không bỏ qua lỗi bằng cách xoá code.
4. Cách sửa chuẩn cho từng rule:
   - react-hooks/set-state-in-effect: (a) state suy ra từ props/state khác → tính trực tiếp lúc render hoặc useMemo, bỏ state;
     (b) reset state khi prop đổi → mẫu "lưu prop trước trong state và so sánh lúc render" hoặc đổi key ở cha (chỉ khi cha trong cùng file);
     (c) đồng bộ từ nguồn ngoài (localStorage, matchMedia, window) → useSyncExternalStore hoặc khởi tạo lazy trong useState(() => …);
     (d) gọi API/async trong effect rồi setState → giữ effect nhưng setState chỉ bên trong callback async/then (rule cho phép), kèm cờ cancelled;
     (e) thật sự cần chạy sau commit (đo DOM) → useLayoutEffect vẫn bị bắt; ưu tiên ref callback hoặc tính toán trong handler.
   - react-hooks/refs: không đọc/ghi ref.current trong lúc render; chuyển vào effect/handler hoặc dùng state.
   - react-hooks/purity: không gọi Date.now()/Math.random() lúc render; dùng useState(() => …) hoặc useMemo với nguồn ổn định.
   - react-hooks/preserve-manual-memoization: sửa mảng phụ thuộc useMemo/useCallback cho đủ và đúng, không xoá memo.
   - react-hooks/immutability: không mutate biến/props/state trong render; tạo bản sao.
   - react/no-unescaped-entities: thay ' " > } bằng &apos; &quot; &gt; &#125; hoặc đưa vào {"..."}.
5. KHÔNG bỏ nhánh reset (setX([]) / setX(null) khi khoá rỗng hoặc đổi): chuyển nó thành giá trị suy ra lúc render (state gắn khoá, so sánh khoá), đừng xoá.
6. Nếu một lỗi KHÔNG thể sửa an toàn mà không đổi hành vi, để nguyên dòng đó và ghi vào "notes" lý do, kèm số dòng.
Trả về DUY NHẤT một JSON hợp lệ dạng {"file": "<toàn bộ nội dung file sau khi sửa>", "notes": "<ngắn gọn, tiếng Việt, mỗi lỗi một dòng>"}.
Không bọc trong markdown, không giải thích ngoài JSON.`;

function buildUser(rel: string, src: string, errs: LintMsg[]): string {
  const list = errs.map((e) => `- dòng ${e.line}:${e.column} [${e.ruleId}] ${e.message}`).join("\n");
  return `File: ${rel}\n\nLỗi ESLint cần sửa (${errs.length}):\n${list}\n\n--- NỘI DUNG FILE (nguyên văn) ---\n${src}`;
}

async function callDeepSeek(apiKey: string, rel: string, src: string, errs: LintMsg[]) {
  let lastErr: unknown;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${apiKey}` },
        body: JSON.stringify({
          model: MODEL,
          temperature: 0,
          max_tokens: MAX_TOKENS,
          response_format: { type: "json_object" },
          messages: [
            { role: "system", content: SYSTEM },
            { role: "user", content: buildUser(rel, src, errs) },
          ],
        }),
      });
      if (res.status === 429 || res.status >= 500) throw new Error(`HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
      if (!res.ok) {
        // 400 Model Not Exist… — không thử lại, báo rõ.
        console.error(`DeepSeek ${res.status}: ${(await res.text()).slice(0, 500)}`);
        process.exit(1);
      }
      const data = (await res.json()) as {
        choices?: { finish_reason?: string; message?: { content?: string } }[];
        usage?: { prompt_tokens?: number; completion_tokens?: number };
      };
      const ch = data.choices?.[0];
      if (ch?.finish_reason === "length") throw Object.assign(new Error("Phản hồi bị cắt (finish_reason=length) — file quá dài hoặc tăng DEEPSEEK_MAX_TOKENS"), { fatal: true });
      const raw = ch?.message?.content ?? "";
      const s = raw.indexOf("{");
      const e = raw.lastIndexOf("}");
      if (s < 0 || e < 0) throw new Error("Không có JSON trong phản hồi");
      const parsed = JSON.parse(raw.slice(s, e + 1)) as { file?: unknown; notes?: unknown };
      if (typeof parsed.file !== "string" || parsed.file.trim().length < 20) throw new Error("JSON thiếu trường file");
      return { file: parsed.file, notes: typeof parsed.notes === "string" ? parsed.notes : "", usage: data.usage };
    } catch (err) {
      lastErr = err;
      if ((err as { fatal?: boolean }).fatal) break;
      console.warn(`  lần ${attempt} lỗi: ${(err as Error).message}`);
      await sleep(1500 * attempt);
    }
  }
  throw lastErr;
}

// ---------- kiểm tra an toàn trước khi nhận bản sửa ----------
function sanityCheck(before: string, after: string): string | null {
  const lb = before.split("\n").length;
  const la = after.split("\n").length;
  if (la < lb * 0.7) return `file ngắn đi quá nhiều (${lb} → ${la} dòng) — nghi xoá code`;
  if (la > lb * 1.6) return `file dài lên quá nhiều (${lb} → ${la} dòng)`;
  if (/eslint-disable/.test(after) && !/eslint-disable/.test(before)) return "thêm eslint-disable";
  if ((after.match(/\bas any\b/g)?.length ?? 0) > (before.match(/\bas any\b/g)?.length ?? 0)) return "thêm `as any`";
  const exp = (s: string) => (s.match(/^export\s+(?:default\s+)?(?:async\s+)?(?:function|const|class|type|interface)\s+(\w+)/gm) ?? []).sort().join("|");
  if (exp(before) !== exp(after)) return "danh sách export thay đổi";
  const imp = (s: string) => new Set((s.match(/from\s+["']([^"']+)["']/g) ?? []).map((m) => m.replace(/from\s+["']|["']/g, "")));
  for (const m of imp(after)) if (!imp(before).has(m) && !m.startsWith("react")) return `import module mới: ${m}`;
  return null;
}

// ---------- main ----------
async function main() {
  const apiKey = requireEnv("DEEPSEEK_API_KEY");
  const tried = loadTried();

  console.log(`Model ${MODEL} · ${APPLY ? "GHI THẬT (--apply)" : "dry-run (chỉ ghi đề xuất vào logs)"} · limit ${LIMIT} · max-lines ${MAX_LINES}`);
  console.log("Quét ESLint…");
  const report = runEslintJson(FILES.length ? FILES : DIRS);

  const candidates = report
    .map((f) => ({ rel: relative(ROOT, f.filePath), errs: errorsOf(f) }))
    .filter((f) => f.errs.length > 0)
    .sort((a, b) => a.errs.length - b.errs.length); // file ít lỗi trước: rẻ, dễ kiểm

  const totalErrs = candidates.reduce((s, c) => s + c.errs.length, 0);
  console.log(`${candidates.length} file có lỗi (${totalErrs} lỗi)${ONLY_RULE ? ` · rule ${ONLY_RULE}` : ""}.`);

  const summary: string[] = [];
  const applied: string[] = [];
  let done = 0;
  let promptTok = 0;
  let outTok = 0;

  for (const c of candidates) {
    if (done >= LIMIT) break;
    const abs = resolve(ROOT, c.rel);
    const src = readFileSync(abs, "utf8");
    const lines = src.split("\n").length;
    const key = c.rel;
    const h = sha(src);

    if (lines > MAX_LINES) {
      summary.push(`BỎ QUA ${c.rel}: ${lines} dòng > ${MAX_LINES} (Claude tách file trước)`);
      continue;
    }
    if (!FORCE && tried[key]?.sha === h) {
      summary.push(`BỎ QUA ${c.rel}: đã thử (${tried[key].outcome}, ${tried[key].at})`);
      continue;
    }
    if (APPLY && !gitClean(c.rel)) {
      summary.push(`BỎ QUA ${c.rel}: có thay đổi chưa commit, không ghi đè`);
      continue;
    }

    done++;
    console.log(`\n[${done}/${LIMIT}] ${c.rel} — ${c.errs.length} lỗi, ${lines} dòng`);
    let out: Awaited<ReturnType<typeof callDeepSeek>>;
    try {
      out = await callDeepSeek(apiKey, c.rel, src, c.errs);
    } catch (err) {
      const msg = (err as Error).message;
      summary.push(`LỖI API ${c.rel}: ${msg}`);
      tried[key] = { sha: h, at: stamp, outcome: `api: ${msg.slice(0, 80)}`, errorsBefore: c.errs.length };
      saveTried(tried);
      continue;
    }
    promptTok += out.usage?.prompt_tokens ?? 0;
    outTok += out.usage?.completion_tokens ?? 0;

    const proposed = out.file.endsWith("\n") ? out.file : out.file + "\n";
    const propPath = join(RUN_DIR, c.rel);
    mkdirSync(dirname(propPath), { recursive: true });
    writeFileSync(propPath, proposed);
    writeFileSync(propPath + ".notes.md", `# ${c.rel}\n\nLỗi gửi đi:\n${c.errs.map((e) => `- ${e.line}:${e.column} ${e.ruleId}`).join("\n")}\n\nGhi chú của model:\n${out.notes || "(không)"}\n`);

    const bad = sanityCheck(src, proposed);
    if (bad) {
      console.log(`  TỪ CHỐI: ${bad}`);
      summary.push(`TỪ CHỐI ${c.rel}: ${bad} (đề xuất ở logs)`);
      tried[key] = { sha: h, at: stamp, outcome: `từ chối: ${bad}`, errorsBefore: c.errs.length };
      saveTried(tried);
      continue;
    }
    if (proposed === src) {
      summary.push(`KHÔNG ĐỔI ${c.rel}: model trả nguyên file. Ghi chú: ${out.notes.slice(0, 120)}`);
      tried[key] = { sha: h, at: stamp, outcome: "không đổi", errorsBefore: c.errs.length };
      saveTried(tried);
      continue;
    }

    // Ghi tạm để eslint kiểm (cả dry-run cũng kiểm rồi hoàn tác — biết được chất lượng mà không tốn gì thêm).
    writeFileSync(abs, proposed);
    const after = runEslintJson([c.rel]);
    const errsAfter = after.flatMap((f) => f.messages.filter((m) => m.severity === 2));
    const diff = gitDiff(c.rel);
    writeFileSync(propPath + ".diff", diff);

    if (errsAfter.length > 0) {
      gitRestore(c.rel);
      const list = errsAfter.map((e) => `${e.line} ${e.ruleId}`).join("; ");
      console.log(`  CÒN ${errsAfter.length} lỗi sau sửa → hoàn tác. ${list}`);
      summary.push(`CÒN LỖI ${c.rel}: ${c.errs.length} → ${errsAfter.length} (${list.slice(0, 150)})`);
      tried[key] = { sha: h, at: stamp, outcome: "còn lỗi", errorsBefore: c.errs.length, errorsAfter: errsAfter.length };
      saveTried(tried);
      continue;
    }

    if (!APPLY) {
      gitRestore(c.rel);
      console.log(`  OK (eslint sạch) — dry-run, đã hoàn tác; đề xuất + diff ở ${relative(ROOT, propPath)}`);
      summary.push(`SẠCH (dry-run) ${c.rel}: ${c.errs.length} → 0, diff ${diff.split("\n").length} dòng`);
      tried[key] = { sha: h, at: stamp, outcome: "sạch (dry-run)", errorsBefore: c.errs.length, errorsAfter: 0 };
    } else {
      applied.push(c.rel);
      console.log(`  OK (eslint sạch) — đã ghi vào cây làm việc`);
      summary.push(`ĐÃ GHI ${c.rel}: ${c.errs.length} → 0, diff ${diff.split("\n").length} dòng. ${out.notes ? "Ghi chú: " + out.notes.slice(0, 120) : ""}`);
      tried[key] = { sha: sha(proposed), at: stamp, outcome: "đã ghi", errorsBefore: c.errs.length, errorsAfter: 0 };
    }
    saveTried(tried);
  }

  // tsc một lần cho cả lượt (chậm ~1 phút, không chạy từng file)
  if (applied.length) {
    console.log(`\nChạy tsc --noEmit cho ${applied.length} file đã ghi…`);
    const r = spawnSync("npx", ["tsc", "--noEmit"], { cwd: ROOT, encoding: "utf8", maxBuffer: 64e6 });
    if (r.status !== 0) {
      writeFileSync(join(RUN_DIR, "tsc.txt"), r.stdout + r.stderr);
      const touched = applied.filter((f) => (r.stdout + r.stderr).includes(f));
      const toRevert = touched.length ? touched : applied;
      for (const f of toRevert) {
        gitRestore(f);
        tried[f] = { ...tried[f], outcome: "tsc đỏ → hoàn tác" };
      }
      saveTried(tried);
      summary.push(`TSC ĐỎ → hoàn tác ${toRevert.join(", ")} (log ${relative(ROOT, join(RUN_DIR, "tsc.txt"))})`);
      for (const f of toRevert) applied.splice(applied.indexOf(f), 1);
      console.log(`  tsc đỏ → đã hoàn tác ${toRevert.length} file. Xem ${relative(ROOT, join(RUN_DIR, "tsc.txt"))}`);
    } else {
      console.log("  tsc sạch.");
    }
  }

  const head = [
    `# DeepSeek sửa lint — ${stamp}`,
    `Model ${MODEL} · ${APPLY ? "apply" : "dry-run"} · token vào ${promptTok} / ra ${outTok}`,
    "",
    ...summary.map((s) => `- ${s}`),
    "",
    applied.length ? `File còn trong cây làm việc: ${applied.length}. Bước tiếp: agent kiem-code soát \`git diff\`, rồi commit theo đường dẫn.` : "",
  ].join("\n");
  writeFileSync(join(RUN_DIR, "TONG-KET.md"), head);
  console.log("\n" + head);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
