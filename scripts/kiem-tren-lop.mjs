#!/usr/bin/env node
/**
 * Kiểm máy bản chiếu "trên lớp" (skill ban-chieu-tren-lop, bước 5) bằng Chrome headless (CDP, không cần Playwright).
 *
 *   python3 -m http.server 8765 -d public &      # phục vụ /fonts + /dev/tren-lop
 *   node scripts/kiem-tren-lop.mjs http://localhost:8765/dev/tren-lop/<slug>.html [--anh=/thu-muc/anh]
 *
 * Ở 1280×720 và 1920×1080: mở hết .an[hidden] (đáp án) và lần lượt từng .buoc (bước clip), rồi báo
 *  - màn .man tràn (scrollHeight > clientHeight + 1),
 *  - mỗi hình .fig: chiều cao (% màn) + cỡ chữ nhỏ nhất trong SVG (px thật trên màn, và tỉ lệ so với chữ thường),
 *  - số .katex-error.
 * Ở 375×812: tràn ngang (scrollWidth > clientWidth).
 * --anh: chụp từng màn ở 1280×720 (đáp án mở) vào thư mục đó, tên <id>.png.
 */
import { spawn } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";
import fs from "node:fs";
import path from "node:path";

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const url = process.argv[2];
if (!url) { console.error("thiếu url"); process.exit(2); }
const anh = process.argv.find((a) => a.startsWith("--anh="))?.slice(6) ?? "";
const PORT = 9400 + (process.pid % 400);
const chrome = spawn(CHROME, ["--headless=new", "--disable-gpu", "--hide-scrollbars", "--autoplay-policy=no-user-gesture-required",
  `--remote-debugging-port=${PORT}`, `--user-data-dir=/tmp/cdp-tl-${process.pid}`, "about:blank"], { stdio: "ignore" });

const DO = `(async () => {
  document.querySelectorAll(".an[hidden]").forEach((e) => e.hidden = false);
  document.querySelectorAll("details").forEach((e) => e.open = true);
  const base = parseFloat(getComputedStyle(document.body).fontSize);
  const vh = innerHeight, out = { base: Math.round(base * 10) / 10, tran: [], hinh: [], katexLoi: document.querySelectorAll(".katex-error").length,
    soMan: document.querySelectorAll(".man").length };
  const doMan = (m, nhan) => {
    if (m.scrollHeight > m.clientHeight + 1) out.tran.push(nhan + " +" + (m.scrollHeight - m.clientHeight) + "px");
  };
  for (const m of document.querySelectorAll(".man")) {
    const buoc = [...m.querySelectorAll(".buoc")];
    if (buoc.length) {
      for (const b of buoc) { buoc.forEach((x) => x.classList.toggle("hien", x === b)); doMan(m, m.id + "/buoc" + buoc.indexOf(b)); }
      buoc.forEach((x, i) => x.classList.toggle("hien", i === 0));
    } else doMan(m, m.id);
    for (const f of m.querySelectorAll(".fig svg")) {
      const r = f.getBoundingClientRect();
      if (!r.height) continue;
      const vb = f.viewBox?.baseVal, k = vb && vb.width ? r.width / vb.width : 1;
      let min = 1e9;
      for (const t of f.querySelectorAll("text")) { const fs = parseFloat(getComputedStyle(t).fontSize) * k; if (fs && fs < min) min = fs; }
      out.hinh.push({ man: m.id, caoPhanTramMan: Math.round(r.height / vh * 100), chuNhoNhatPx: min < 1e9 ? Math.round(min) : null,
        tiLe: min < 1e9 ? Math.round(min / base * 100) / 100 : null });
    }
  }
  return JSON.stringify(out);
})()`;
const NGANG = `JSON.stringify({ vw: document.documentElement.clientWidth, sw: document.documentElement.scrollWidth })`;

async function waitDev() {
  for (let i = 0; i < 80; i++) { try { if ((await fetch(`http://127.0.0.1:${PORT}/json/version`)).ok) return; } catch {} await sleep(250); }
  throw new Error("Chrome không mở cổng DevTools");
}
try {
  await waitDev();
  const tab = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: "PUT" })).json();
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.addEventListener("open", res); ws.addEventListener("error", rej); });
  let id = 0; const waiting = new Map(); let loadRes = null;
  ws.addEventListener("message", (e) => { const m = JSON.parse(e.data);
    if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); }
    if (m.method === "Page.loadEventFired" && loadRes) { loadRes(); loadRes = null; } });
  const send = (method, params = {}) => new Promise((r) => { waiting.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });
  const ev = async (expression) => (await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true })).result?.result?.value;
  await send("Page.enable"); await send("Runtime.enable");
  let loi = 0;
  for (const [w, h] of [[1280, 720], [1920, 1080], [375, 812]]) {
    await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 760 });
    const l = new Promise((r) => (loadRes = r)); await send("Page.navigate", { url }); await l;
    await sleep(2500); // KaTeX + font
    if (w < 760) {
      const r = JSON.parse(await ev(NGANG));
      console.log(`${w}×${h}: tràn ngang ${r.sw > r.vw ? "CÓ (" + r.sw + " > " + r.vw + ")" : "không"}`);
      if (r.sw > r.vw) loi++;
      continue;
    }
    const r = JSON.parse(await ev(DO));
    console.log(`${w}×${h}: ${r.soMan} màn · chữ thường ${r.base}px · katex-error ${r.katexLoi} · tràn ${r.tran.length ? r.tran.join(", ") : "0"}`);
    for (const f of r.hinh) console.log(`   hình ở ${f.man}: cao ${f.caoPhanTramMan}% màn · chữ hình nhỏ nhất ${f.chuNhoNhatPx}px (${f.tiLe}× chữ thường)${f.tiLe !== null && f.tiLe < 0.7 ? "  ← < 0,7" : ""}`);
    loi += r.tran.length + r.katexLoi;
    if (anh && w === 1280) {
      fs.mkdirSync(anh, { recursive: true });
      const ids = await ev(`JSON.stringify([...document.querySelectorAll(".man")].map((m) => m.id))`);
      for (const mid of JSON.parse(ids)) {
        await ev(`(() => { document.documentElement.style.scrollSnapType = "none"; document.documentElement.style.scrollBehavior = "auto"; document.getElementById(${JSON.stringify("")} + ${JSON.stringify(mid)}).scrollIntoView(); })()`);
        await sleep(150);
        const s = await send("Page.captureScreenshot", { format: "png" });
        fs.writeFileSync(path.join(anh, mid + ".png"), Buffer.from(s.result.data, "base64"));
      }
      console.log("   ảnh:", anh);
    }
  }
  console.log(loi ? `CÒN ${loi} LỖI` : "ĐẠT");
  process.exitCode = loi ? 1 : 0;
} finally { chrome.kill(); }
