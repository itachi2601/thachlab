// Sửa đề dẫn nhóm câu ("Sử dụng các thông tin sau cho câu X và câu Y: …") bị dính nhầm vào cuối
// ĐỀ hoặc LỜI GIẢI của câu đứng trước nhóm: cắt khỏi chỗ dính, chèn vào đầu đề của các câu trong nhóm.
//   npx tsx scripts/sua-de-dan-lac.mts                 dry-run (mặc định, CHỈ ĐỌC) → scripts/logs/sua-de-dan-lac-mau.md
//   npx tsx scripts/sua-de-dan-lac.mts --exam=131      chỉ một đề
//   npx tsx scripts/sua-de-dan-lac.mts --apply         ghi thật (sao lưu questions cũ ra scripts/logs/ trước) — chỉ ca "chắc"
// Ca "nghi" KHÔNG bao giờ tự sửa. Kết quả duyệt bằng mắt/agent (loại, giữ câu đầu, nghi) nằm ở
// scripts/logs/duyet-dan/ghi-de-duyet.json — khoá theo (đề, câu nguồn, trường).
import { createClient } from "@supabase/supabase-js";
import fs from "node:fs";
const envTxt = fs.readFileSync(".env.local", "utf8").split("\n");
const env = (k: string) => envTxt.find((l) => l.startsWith(`${k}=`))!.slice(k.length + 1).trim();
const sb = createClient(env("NEXT_PUBLIC_SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
const APPLY = process.argv.includes("--apply");
const ONLY = process.argv.find((a) => a.startsWith("--exam="))?.slice(7);

type Dec = { exam: number; from: number; field: string };
const duyet = JSON.parse(fs.readFileSync("scripts/logs/duyet-dan/ghi-de-duyet.json", "utf8")) as { loai: Dec[]; giuCauDau: Dec[]; nghi: Dec[] };
const inList = (l: Dec[], exam: number, from: number, field: string) => l.some((d) => d.exam === exam && d.from === from && d.field === field);

const STOP = new Set("được trong khi của các một những này đó thì là có không cho bao nhiêu biết giá trị khoảng bằng sau trước lúc tính tìm xác định lớn nhỏ hơn với theo như từ đến cũng nếu thể khối lượng độ hình bên dưới câu".split(" "));
const START = /(?:<br\s*\/?>\s*)*(?:Sử dụng|Dùng)\s+(?:các\s+)?(?:thông tin|dữ liệu|số liệu|kết quả)[^:<]{0,60}?câu\s*\d/gi;
const text = (s: string) => s.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").toLowerCase();
const words = (s: string) => new Set(text(s).match(/[\p{L}\d]{4,}/gu) ?? []);
const trimBr = (s: string) => s.replace(/^(?:<br\s*\/?>\s*)+/i, "").replace(/(?:<br\s*\/?>\s*)+$/i, "").trim();

type Q = Record<string, any>;
type Seg = { passage: string; nums: number[] };

/** Tách một trường thành phần gốc + các đoạn dẫn (mỗi đoạn bắt đầu ở một "Sử dụng thông tin … câu X"). */
function split(s: string): { rest: string; segs: Seg[] } | null {
  const ms = [...s.matchAll(START)];
  if (!ms.length) return null;
  const rest = trimBr(s.slice(0, ms[0].index).replace(/(<br\s*\/?>\s*)+$/i, ""));
  const segs: Seg[] = [];
  ms.forEach((m, k) => {
    const chunk = trimBr(s.slice(m.index, ms[k + 1]?.index ?? s.length));
    const head = /^[^:.]{0,90}[:.]/.exec(chunk);
    if (!head) return;
    let passage = chunk.slice(head[0].length).replace(/^(?:\s*<\/\w+>)+/i, "").trim();
    const nums = (head[0].match(/\d+/g) ?? []).map(Number);
    // đoạn dẫn tự lặp hai lần ngay trong nó → giữ một bản
    const key = text(passage).slice(0, 40);
    if (key.length >= 30) {
      const again = text(passage).indexOf(key, 20);
      if (again > 0) {
        // cắt theo vị trí tương ứng trong chuỗi gốc: tìm lần xuất hiện thứ hai của 40 ký tự đầu (dạng thô)
        const raw = passage.slice(0, 30);
        const at = passage.indexOf(raw, 20);
        if (at > 0) passage = passage.slice(0, at).trim();
      }
    }
    // bản lặp chính là header + chính đoạn → đã bị tách thành seg sau có passage trùng: bỏ ở khâu dedupe
    segs.push({ passage, nums });
  });
  // seg sau trùng seg trước (bản lặp) → bỏ
  const uniq: Seg[] = [];
  for (const sg of segs) if (sg.passage && !uniq.some((u) => text(u.passage).slice(0, 40) === text(sg.passage).slice(0, 40))) uniq.push(sg);
  return { rest, segs: uniq };
}

type Plan = { exam: number; title: string; published: boolean; from: number; field: "question" | "explanation"; targets: number[]; passage: string; sure: boolean; why: string; trimmed?: boolean };

const plans: Plan[] = [];
const examsQs = new Map<number, Q[]>();
let from = 0;
for (;;) {
  const { data, error } = ONLY
    ? await sb.from("exams").select("id,title,published,questions").eq("id", Number(ONLY))
    : await sb.from("exams").select("id,title,published,questions").order("id").range(from, from + 24);
  if (error) { console.error(error.message); process.exit(1); }
  if (!data?.length) break;
  for (const ex of data) {
    const qs = (ex.questions as Q[] | null) ?? [];
    examsQs.set(ex.id, qs);
    qs.forEach((k, i) => {
      for (const field of ["question", "explanation"] as const) {
        const sp = typeof k[field] === "string" ? split(k[field]) : null;
        if (!sp) continue;
        let offset = 0;
        for (const sg of sp.segs) {
          if (!sg.passage) continue;
          let count = sg.nums.length ? Math.min(Math.max(...sg.nums) - Math.min(...sg.nums) + 1, 6) : 1;
          let targets = Array.from({ length: count }, (_, j) => i + 1 + offset + j).filter((t) => t < qs.length);
          let sure = targets.length === count, why = sure ? "" : "không đủ câu đích phía sau";
          let trimmed = false;
          if (sure) {
            const pw = words(sg.passage);
            const share = (t: number) => [...words(qs[t].question || "")].filter((w) => pw.has(w) && !STOP.has(w)).length;
            // giữ tiền tố các câu đích còn chung từ khoá; dừng ở câu đầu tiên không chung
            const keep: number[] = [];
            for (const t of targets) { if (share(t) >= 2) keep.push(t); else break; }
            if (!keep.length) { sure = false; why = "câu đích không chung từ khoá với đề dẫn (nhóm có thể đã mất)"; }
            else if (keep.length < targets.length) { trimmed = true; targets = keep; }
            if (sure && targets.some((t) => text(qs[t].question || "").includes(text(sg.passage).slice(0, 30)))) { sure = false; why = "câu đích đã chứa đề dẫn"; }
          }
          // kết quả duyệt
          if (inList(duyet.loai, ex.id, i, field)) { sure = false; why = "đã duyệt: không phải đoạn dẫn nhóm / câu đích độc lập"; }
          else if (inList(duyet.nghi, ex.id, i, field) && sure) { sure = false; why = "đã duyệt: không chắc, cần đối chiếu đề gốc"; }
          else if (inList(duyet.giuCauDau, ex.id, i, field) && sure && targets.length > 1) { targets = [targets[0]]; trimmed = true; }
          plans.push({ exam: ex.id, title: ex.title, published: ex.published, from: i, field, targets, passage: sg.passage, sure, why, trimmed });
          offset += count;
        }
      }
    });
  }
  if (ONLY) break;
  from += 25;
}

const sure = plans.filter((p) => p.sure), doubt = plans.filter((p) => !p.sure);
const exams = (a: Plan[]) => new Set(a.map((p) => p.exam)).size;
console.log(`Tìm thấy ${plans.length} đoạn dẫn lạc / ${exams(plans)} đề`);
console.log(`  CHẮC: ${sure.length} đoạn / ${exams(sure)} đề (thu hẹp số câu đích: ${sure.filter((p) => p.trimmed).length})`);
console.log(`  NGHI (không tự sửa): ${doubt.length} / ${exams(doubt)} đề`);
const by: Record<string, number> = {};
doubt.forEach((p) => (by[p.why] = (by[p.why] || 0) + 1));
console.log("  lý do nghi:", by);

const md: string[] = ["# Dry-run sửa đề dẫn lạc (bản 2, sau duyệt)\n", `CHẮC ${sure.length}, NGHI ${doubt.length}\n`];
const pick = (a: Plan[], n: number) => a.filter((_, i) => i % Math.max(1, Math.floor(a.length / n)) === 0).slice(0, n);
for (const [name, list] of [["CHẮC (mẫu)", pick(sure, 6)], ["CHẮC nhưng đã thu hẹp (mẫu)", pick(sure.filter((p) => p.trimmed), 4)], ["NGHI (mẫu)", pick(doubt, 6)]] as const) {
  md.push(`\n## ${name}\n`);
  for (const p of list) {
    const qs = examsQs.get(p.exam)!;
    md.push(`- **đề ${p.exam}** (${p.published ? "HIỆN" : "ẩn"}) · gốc ở **${p.field}** câu ${p.from + 1} → chèn đầu đề câu ${p.targets.map((t) => t + 1).join(", ") || "—"}${p.why ? ` · ⚠ ${p.why}` : ""}\n  > ĐOẠN DẪN: ${p.passage.replace(/<img[^>]*>/g, "[ẢNH]").replace(/<[^>]+>/g, " ").slice(0, 160)}…\n` +
      p.targets.map((t) => `  > Câu ${t + 1} hiện: ${(qs[t].question || "").replace(/<[^>]+>/g, " ").slice(0, 100)}`).join("\n") + "\n");
  }
}
fs.writeFileSync("scripts/logs/sua-de-dan-lac-mau.md", md.join("\n"));
fs.writeFileSync("scripts/logs/sua-de-dan-lac-ke-hoach.json", JSON.stringify(plans, null, 1));
console.log("Mẫu: scripts/logs/sua-de-dan-lac-mau.md · kế hoạch: scripts/logs/sua-de-dan-lac-ke-hoach.json");
if (!APPLY) { console.log("DRY-RUN — chưa ghi gì."); process.exit(0); }

// ---- APPLY: chỉ ca CHẮC, sao lưu trước ----
// Cắt MỌI đoạn dẫn khỏi trường nguồn (kể cả ca nghi/loại: phần rác đó không thuộc trường này), chỉ chèn ca chắc.
const byExam = new Map<number, Plan[]>();
for (const p of plans) byExam.set(p.exam, [...(byExam.get(p.exam) ?? []), p]);
const backup: Record<number, Q[]> = {};
let written = 0;
for (const [id, ps] of byExam) {
  const sureHere = ps.filter((p) => p.sure);
  if (!sureHere.length) continue;
  const orig = examsQs.get(id)!;
  const qs: Q[] = structuredClone(orig);
  // chỉ cắt ở các trường mà mọi đoạn trong đó đều là ca chắc (không đụng trường có ca nghi/loại)
  const fields = new Set(ps.map((p) => `${p.from}|${p.field}`));
  for (const f of fields) {
    const [i, field] = f.split("|"); const group = ps.filter((p) => p.from === Number(i) && p.field === field);
    if (!group.every((p) => p.sure)) continue;
    qs[Number(i)][field] = split(orig[Number(i)][field])!.rest;
  }
  const done = new Set<string>();
  for (const p of sureHere) {
    if (!(fields.has(`${p.from}|${p.field}`) && ps.filter((x) => x.from === p.from && x.field === p.field).every((x) => x.sure))) continue;
    for (const t of p.targets) {
      const key = `${t}|${text(p.passage).slice(0, 40)}`;
      if (done.has(key)) continue; // cùng đoạn dẫn có bản ở đề và ở lời giải → chèn một lần
      done.add(key);
      qs[t].question = `${p.passage}<br>${qs[t].question}`;
    }
  }
  backup[id] = orig;
  const { error } = await sb.from("exams").update({ questions: qs }).eq("id", id);
  if (error) { console.error("LỖI đề", id, error.message); process.exit(1); }
  written++;
}
const bf = `scripts/logs/sua-de-dan-lac-sao-luu-${Date.now()}.json`;
fs.writeFileSync(bf, JSON.stringify(backup));
console.log(`ĐÃ GHI ${written} đề. Sao lưu: ${bf}`);
