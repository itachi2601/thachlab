// Dùng: node preview.mjs <theory.html> <thư-mục-ra>   (chạy từ gốc repo)
// Dựng trang rời với CSS thật (globals.css) + KaTeX, chụp 375px: từng figure.fig + cả bài,
// tự bấm mọi đáp án và in ra số phản hồi hiện đúng. Chromium: /opt/pw-browsers (không `playwright install`).
import fs from "node:fs";
import path from "node:path";
import { chromium } from "/opt/node22/lib/node_modules/playwright/index.mjs";
const [, , src, out = "preview-out"] = process.argv;
if (!src) { console.error("thiếu <theory.html>"); process.exit(1); }
fs.mkdirSync(out, { recursive: true });
const root = process.cwd();
const g = fs.readFileSync(path.join(root, "app/globals.css"), "utf8");
const css = g.slice(g.indexOf("/* Hình vẽ SVG nội tuyến"), g.indexOf("/* ---------- Nội dung bài viết blog")) + g.slice(g.indexOf("/* Bài lý thuyết tương tác"));
const katex = path.join(root, "node_modules/katex/dist");
const html = `<!doctype html><meta charset=utf8><meta name=viewport content="width=device-width"><link rel=stylesheet href="file://${katex}/katex.min.css"><style>body{background:#0f172a;color:#e2e8f0;font:16px/1.75 sans-serif;max-width:720px;margin:auto;padding:16px}${css}</style><span class="exam-content">${fs.readFileSync(src, "utf8")}</span><script src="file://${katex}/katex.min.js"></script><script src="file://${katex}/contrib/auto-render.min.js"></script><script>renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}]})</script>`;
const page_path = path.resolve(out, "page.html");
fs.writeFileSync(page_path, html);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }).catch(() => chromium.launch());
const p = await b.newPage({ viewport: { width: 375, height: 900 }, deviceScaleFactor: 2 });
await p.goto("file://" + page_path);
const figs = await p.$$("figure.fig");
for (let i = 0; i < figs.length; i++) await figs[i].screenshot({ path: path.join(out, `fig${i + 1}.png`) });
const quizzes = await p.$$(".tl-quiz");
for (let i = 0; i < quizzes.length; i++) {
  const labels = await quizzes[i].$$("label.tl-opt");
  const res = [];
  for (const l of labels) {
    await l.click();
    const shown = await quizzes[i].$$eval(".tl-fb", (e) => e.map((x) => getComputedStyle(x).display === "block"));
    const ok = await l.evaluate((x) => x.classList.contains("tl-ok"));
    res.push(ok ? (shown[0] && !shown[1] ? "✓" : "✗LỖI") : (!shown[0] && shown[1] ? "✓" : "✗LỖI"));
  }
  console.log(`quiz #${i + 1}: ${res.join(" ")}`);
}
for (const d of await p.$$("details > summary")) await d.click();
await p.screenshot({ path: path.join(out, "full.png"), fullPage: true });
await b.close();
console.log(`ảnh: ${figs.length} hình + full.png trong ${out}/ — XEM BẰNG MẮT`);
