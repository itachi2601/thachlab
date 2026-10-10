#!/usr/bin/env node
/**
 * Chụp + đo bố cục một trang thật bằng Chrome DevTools Protocol (không cần Playwright).
 *
 *   node tmp/do-bo-cuc.mjs <url> [--rong=375] [--cao=812] [--theme=light|dark] [--anh=/tmp/x.png] [--toan-trang]
 *
 * Vì sao không dùng `chrome --screenshot --window-size=375,812`: cửa sổ 375 đó KHÔNG phải viewport
 * 375 — Chrome headless vẫn đặt layout viewport ~500px rồi cắt ảnh còn 375, nên ảnh trông như
 * "nội dung bị cắt ở mép phải" trong khi trang không hề tràn. Ở đây đặt thẳng
 * Emulation.setDeviceMetricsOverride nên đo và chụp đúng bề rộng yêu cầu (D1 của QUY-TAC-THIET-KE).
 *
 * In ra: viewport, scrollWidth (tràn ngang thật), và các phần tử có mép phải vượt viewport.
 */
import { spawn } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";
import fs from "node:fs";

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const arg = (name, fallback) => process.argv.find((a) => a.startsWith(`--${name}=`))?.split("=")[1] ?? fallback;
const has = (name) => process.argv.includes(`--${name}`);

const url = process.argv[2] ?? "http://localhost:3001/";
const width = Number(arg("rong", 375));
const height = Number(arg("cao", 812));
const theme = arg("theme", "");
const shotPath = arg("anh", "");
const fullPage = has("toan-trang");
const PORT = 9400 + (process.pid % 400);

const chrome = spawn(
  CHROME,
  ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${PORT}`,
   `--user-data-dir=/tmp/cdp-prof-${process.pid}`, "about:blank"],
  { stdio: "ignore" },
);

async function waitForDevtools() {
  for (let i = 0; i < 80; i++) {
    try {
      if ((await fetch(`http://127.0.0.1:${PORT}/json/version`)).ok) return;
    } catch {}
    await sleep(250);
  }
  throw new Error("Chrome không mở cổng DevTools");
}

const EXPR = `(() => {
  const vw = document.documentElement.clientWidth;
  const over = [];
  for (const el of document.querySelectorAll("body *")) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.right > vw + 1) {
      const cs = getComputedStyle(el);
      let clipped = false;
      for (let p = el.parentElement; p; p = p.parentElement) {
        const pc = getComputedStyle(p);
        if (pc.overflowX !== "visible" || pc.overflowY !== "visible") { clipped = true; break; }
      }
      over.push({ tag: el.tagName.toLowerCase(), cls: (el.className || "").toString().slice(0, 80),
        right: Math.round(r.right), width: Math.round(r.width), minW: cs.minWidth, ws: cs.whiteSpace,
        biCat: clipped, txt: (el.textContent || "").trim().slice(0, 32) });
    }
  }
  return JSON.stringify({
    vw, scrollWidth: document.documentElement.scrollWidth, bodyScrollWidth: document.body.scrollWidth,
    tranThatSu: over.filter((o) => !o.biCat).slice(0, 12),
    soTranBiCat: over.filter((o) => o.biCat).length,
    soTranThatSu: over.filter((o) => !o.biCat).length,
  }, null, 1);
})()`;

try {
  await waitForDevtools();
  const tab = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: "PUT" })).json();
  const ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.addEventListener("open", res); ws.addEventListener("error", rej); });

  let id = 0;
  const waiting = new Map();
  let loadResolve = null;
  ws.addEventListener("message", (e) => {
    const m = JSON.parse(e.data);
    if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); }
    if (m.method === "Page.loadEventFired" && loadResolve) { loadResolve(); loadResolve = null; }
  });
  const send = (method, params = {}) => new Promise((resolve) => { waiting.set(++id, resolve); ws.send(JSON.stringify({ id, method, params })); });
  const nextLoad = () => new Promise((resolve) => { loadResolve = resolve; });

  await send("Page.enable");
  await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: true });

  if (theme) {
    // Đặt theme trước khi vào trang: cùng origin nên localStorage dùng được ngay.
    await send("Page.navigate", { url });
    await nextLoad();
    await send("Runtime.evaluate", { expression: `localStorage.setItem("thachlab-theme", ${JSON.stringify(theme)})` });
  }
  const loaded = nextLoad();
  await send("Page.navigate", { url });
  await loaded;
  await send("Runtime.evaluate", { expression: `document.documentElement.dataset.theme = ${JSON.stringify(theme || "")} || document.documentElement.dataset.theme` }).catch(() => {});
  await sleep(3000); // chờ JS muộn (mô phỏng canvas, biểu đồ, ảnh)

  const r = await send("Runtime.evaluate", { expression: EXPR, returnByValue: true });
  console.log(`${url} · ${width}×${height}${theme ? " · theme=" + theme : ""}`);
  console.log(r.result?.result?.value ?? JSON.stringify(r));

  if (shotPath) {
    const shot = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: fullPage });
    fs.writeFileSync(shotPath, Buffer.from(shot.result.data, "base64"));
    console.log("ảnh:", shotPath);
  }
} finally {
  chrome.kill();
}
