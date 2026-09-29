import fs from "node:fs"; import path from "node:path"; import { execSync } from "node:child_process";
// Cách dùng: node perf/chunks-report.mjs <thư mục repo đã build> — liệt kê chunk JS lớn nhất và JS tải theo trang từ out/**/index.html
const root = process.argv[2] ?? ".";
const htmls = execSync(`find ${root}/out -name index.html -not -path "*/_next/*"`).toString().trim().split("\n");
const size = {}, gz = {}, pagesOf = {}, perPage = [];
for (const h of htmls) {
  const page = "/" + path.relative(path.join(root, "out"), path.dirname(h));
  const html = fs.readFileSync(h, "utf8");
  const srcs = [...html.matchAll(/<script[^>]+src="(\/_next\/static\/chunks\/[^"]+\.js)"/g)].map(m=>m[1]);
  const uniq = [...new Set(srcs)];
  let total = 0;
  for (const f of uniq) {
    if (!(f in size)) { const p = path.join(root, "out", f); size[f] = fs.statSync(p).size; gz[f] = execSync(`gzip -c "${p}" | wc -c`).toString().trim()*1; }
    total += size[f]; (pagesOf[f] ??= new Set()).add(page === "/." ? "/" : page);
  }
  perPage.push([page === "/." ? "/" : page, total, uniq.length]);
}
const nPages = htmls.length;
console.log(`Tổng số trang tĩnh: ${nPages}\n`);
console.log("### 10 chunk JS lớn nhất (được tải trực tiếp qua <script>)");
console.log("| Chunk | KB | KB gzip | Số trang dùng | Trang tiêu biểu |\n|---|---:|---:|---:|---|");
Object.entries(size).sort((a, b) => b[1] - a[1]).slice(0, 10).forEach(([f, s]) => {
  const p = [...pagesOf[f]]; console.log(`| ${f.replace("/_next/static/chunks/", "")} | ${(s/1024).toFixed(0)} | ${(gz[f]/1024).toFixed(0)} | ${p.length}/${nPages} | ${p.slice(0,3).join(", ")} |`);
});
console.log("\n### JS tải ban đầu mỗi trang (tổng các <script> chunk, KB chưa gzip) — 25 trang nặng nhất");
console.log("| Trang | KB | Số chunk |\n|---|---:|---:|");
perPage.sort((a,b)=>b[1]-a[1]).slice(0,25).forEach(([p,s,n])=>console.log(`| ${p} | ${(s/1024).toFixed(0)} | ${n} |`));
console.log("\n### Vài trang HS tiêu biểu");
for (const want of ["/", "/lop-hoc", "/kiem-tra", "/dashboard-thpt", "/dang-nhap"]) { const r = perPage.find(x=>x[0]===want); if (r) console.log(`- ${r[0]}: ${(r[1]/1024).toFixed(0)} KB (${r[2]} chunk)`); }
