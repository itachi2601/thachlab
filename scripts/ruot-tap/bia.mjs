// Trang BÌA cho quyển ruột tập theo học kì (27/11/2026). Khổ 165×240 như ruột, in màu hoặc đen trắng đều đọc được.
//   node scripts/ruot-tap/bia.mjs vl11-hk2            → scripts/ruot-tap/out/bia-vl11-hk2.pdf (+ .html để xem)
// Bìa in riêng (giấy dày), KHÔNG ghép vào dung-hoc-ki.sh. Thêm quyển: thêm mục vào QUYEN (tên phần, bài, hình).
// Hình điện trường: đường sức lưỡng cực +q/−q tính số (Euler), mũi tên chevron 30° (AGENTS.md: quy tắc hình).
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { fonts } from './khung.mjs';
import { chuanHoa } from './ky-tu-in.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const BOOK = [resolve(HERE, '../../book/'), '/Users/MAC/Projects/thachlab/book'].find((d) => existsSync(d + '/node_modules')) + '/';
const puppeteer = createRequire(BOOK + 'package.json')('puppeteer-core');

// ---------- hình ----------
const chevron = (x, y, ang, s = 2.6, mau = 'currentColor') => {   // mũi tên chevron 30° tại (x,y), hướng ang (rad)
  const a1 = ang + Math.PI - Math.PI / 6, a2 = ang + Math.PI + Math.PI / 6;
  return `<path d="M${(x + s * Math.cos(a1)).toFixed(2)} ${(y + s * Math.sin(a1)).toFixed(2)}L${x.toFixed(2)} ${y.toFixed(2)}L${(x + s * Math.cos(a2)).toFixed(2)} ${(y + s * Math.sin(a2)).toFixed(2)}" fill="none" stroke="${mau}" stroke-width=".7" stroke-linecap="round" stroke-linejoin="round"/>`;
};

function hinhDienTruong() {
  const W = 120, H = 62, P = [38, 31], N = [82, 31], R0 = 4.2;
  const E = (x, y) => {
    let ex = 0, ey = 0;
    for (const [[cx, cy], q] of [[P, 1], [N, -1]]) {
      const dx = x - cx, dy = y - cy, r3 = Math.pow(dx * dx + dy * dy, 1.5);
      ex += (q * dx) / r3; ey += (q * dy) / r3;
    }
    return [ex, ey];
  };
  let out = '';
  const nLine = 14;
  for (let k = 0; k < nLine; k++) {
    const a = (2 * Math.PI * (k + 0.5)) / nLine;
    let x = P[0] + R0 * Math.cos(a), y = P[1] + R0 * Math.sin(a);
    const pts = [[x, y]];
    for (let i = 0; i < 2000; i++) {
      const [ex, ey] = E(x, y), m = Math.hypot(ex, ey);
      x += (0.35 * ex) / m; y += (0.35 * ey) / m;
      pts.push([x, y]);
      if (Math.hypot(x - N[0], y - N[1]) < R0 || x < -5 || x > W + 5 || y < -5 || y > H + 5) break;
    }
    out += `<path d="M${pts.map(([u, v]) => `${u.toFixed(2)} ${v.toFixed(2)}`).join('L')}" fill="none" stroke="currentColor" stroke-width=".55"/>`;
    // mũi tên ở giữa phần đường nằm trong khung
    const trong = pts.filter(([u, v]) => u > 2 && u < W - 2 && v > 2 && v < H - 2);
    const j = Math.floor(trong.length / 2);
    if (trong.length > 6) {
      const [u0, v0] = trong[j - 1], [u1, v1] = trong[j + 1];
      out += chevron(trong[j][0], trong[j][1], Math.atan2(v1 - v0, u1 - u0));
    }
  }
  const dt = (c, mau, dau) => `<circle cx="${c[0]}" cy="${c[1]}" r="${R0}" fill="${mau}" stroke="#fff" stroke-width=".6"/>`
    + `<path d="M${c[0] - 2.2} ${c[1]}h4.4${dau ? `M${c[0]} ${c[1] - 2.2}v4.4` : ''}" stroke="#fff" stroke-width=".9" stroke-linecap="round"/>`;
  return `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" style="color:#c63b2f">${out}${dt(P, '#c63b2f', true)}${dt(N, '#1d3a78', false)}</svg>`;
}

function hinhMachDien() {
  // mạch nối tiếp: nguồn (ℰ, r) — khoá K — ampe kế — điện trở R — biến trở; dòng I chạy cùng chiều kim đồng hồ ở mạch ngoài
  const s = 'stroke="currentColor" stroke-width=".7" fill="none" stroke-linecap="round"';
  const L = 14, R = 106, T = 12, B = 52;
  let o = '';
  // dây: trên (nguồn ở giữa cạnh trên), phải, dưới, trái
  o += `<path d="M${L} ${T}H52M60 ${T}H${R}V24M${R} 40V${B}H78M64 ${B}H48M34 ${B}H${L}V${T}" ${s}/>`;
  // nguồn: vạch dài (+) bên trái, vạch ngắn (−) bên phải
  o += `<path d="M52 ${T - 6}v12" ${s} stroke-width="1"/><path d="M60 ${T - 3.2}v6.4" ${s} stroke-width="2"/>`;
  o += `<text x="56" y="${T - 8}" class="nh" text-anchor="middle">ℰ, r</text><text x="49" y="${T - 1.5}" class="nh s" text-anchor="end">+</text><text x="63" y="${T - 1.5}" class="nh s">−</text>`;
  // điện trở R (cạnh phải, đứng)
  o += `<rect x="${R - 3.2}" y="24" width="6.4" height="16" ${s} fill="#fff"/><text x="${R + 6}" y="34" class="nh">R</text>`;
  // ampe kế (cạnh dưới)
  o += `<circle cx="71" cy="${B}" r="7" ${s} fill="#fff"/><text x="71" y="${B + 2.4}" class="nh" text-anchor="middle" style="font-size:6.4px;font-weight:700">A</text>`;
  // khoá K (cạnh dưới, mở nghiêng)
  o += `<circle cx="34" cy="${B}" r="1" fill="currentColor"/><circle cx="48" cy="${B}" r="1" fill="currentColor"/><path d="M34 ${B}L46.5 ${B - 5.5}" ${s}/><text x="41" y="${B + 7.5}" class="nh" text-anchor="middle">K</text>`;
  // chiều dòng điện I (mạch ngoài, từ cực +): trên-trái → xuống cạnh trái → cạnh dưới sang phải → lên cạnh phải → về cực −
  o += chevron(L, 32, Math.PI / 2, 3, '#c63b2f') + `<text x="${L - 4}" y="34" class="nh i" text-anchor="end">I</text>`;
  o += chevron(88, B, 0, 3, '#c63b2f');
  o += chevron(R, 46, -Math.PI / 2, 3, '#c63b2f');
  return `<svg viewBox="0 0 120 62" xmlns="http://www.w3.org/2000/svg" style="color:#1c2540">${o}</svg>`;
}

// ---------- dữ liệu quyển ----------
const QUYEN = {
  'vl11-hk2': {
    lop: 11, hk: 'II',
    phan: [
      { so: 1, ten: 'ĐIỆN TRƯỜNG', ch: 'Chương III', mau: '#c63b2f', hinh: hinhDienTruong,
        bai: [[16, 'Lực tương tác giữa hai điện tích'], [17, 'Khái niệm điện trường'], [18, 'Điện trường đều'],
          [19, 'Thế năng điện'], [20, 'Điện thế'], [21, 'Tụ điện']] },
      { so: 2, ten: 'MẠCH ĐIỆN MỘT CHIỀU', ch: 'Chương IV · Dòng điện. Mạch điện', mau: '#1d3a78', hinh: hinhMachDien,
        bai: [[22, 'Cường độ dòng điện'], [23, 'Điện trở. Định luật Ohm'], [24, 'Nguồn điện'],
          [25, 'Năng lượng điện. Công suất điện'], [26, 'Thực hành: Đo suất điện động và điện trở trong của pin']] },
    ],
  },
};

const ma = process.argv[2] || 'vl11-hk2';
const Q = QUYEN[ma];
if (!Q) throw new Error(`không có quyển ${ma} (có: ${Object.keys(QUYEN).join(', ')})`);
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

const the = Q.phan.map((p) => `<div class="phan" style="--m:${p.mau}">
  <div class="ph-h"><span class="ph-so">PHẦN ${p.so}</span><span class="ph-ch">${esc(p.ch)}</span></div>
  <div class="ph-b"><div class="ph-t">${esc(p.ten)}</div>
    <ol>${p.bai.map(([n, t]) => `<li><em>Bài ${n}</em>${esc(t)}</li>`).join('')}</ol></div>
  <div class="ph-art">${p.hinh()}</div>
</div>`).join('');

const html = `<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>${fonts}
@page{size:165mm 240mm;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:BV,sans-serif;color:#1c2540;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;width:165mm;height:240mm;overflow:hidden;background:#fff}
.top{background:#1d3a78;color:#fff;padding:12mm 12mm 8mm 16mm;position:relative}
.nhan{display:flex;justify-content:space-between;font-weight:700;font-size:3mm;letter-spacing:.6mm;border-bottom:.3mm solid rgba(255,255,255,.55);padding-bottom:2.2mm}
.mon{margin:6mm 0 0;font-weight:700;font-size:15mm;line-height:.95;letter-spacing:-.2mm}
.mon b{color:#ffcf5a}
.hk{margin-top:2.5mm;font-size:6mm;font-weight:700;letter-spacing:.9mm}
.sub{margin-top:2.5mm;font-size:3.5mm;opacity:.9}
.body{padding:9mm 12mm 0 16mm;display:flex;flex-direction:column;gap:8mm}
.phan{border:.35mm solid var(--m);border-radius:2.5mm;overflow:hidden;display:grid;grid-template-columns:1fr 60mm;grid-template-rows:auto 1fr}
.ph-h{grid-column:1/3;background:var(--m);color:#fff;display:flex;justify-content:space-between;align-items:baseline;padding:1.6mm 4mm}
.ph-so{font-weight:700;font-size:3.6mm;letter-spacing:.6mm}.ph-ch{font-size:3.1mm}
.ph-b{padding:3mm 2mm 3mm 4mm}
.ph-t{font-weight:700;font-size:6.6mm;line-height:1.05;color:var(--m);margin-bottom:2.5mm}
ol{list-style:none;margin:0;padding:0;font-size:3.45mm;line-height:1.5}li{display:flex}
li em{font-style:normal;font-weight:700;color:var(--m);flex:none;width:12.5mm}
.ph-art{padding:2mm 3mm 2mm 0;display:flex;align-items:center}
.ph-art svg{width:57mm;height:auto;display:block}
svg .nh{font:italic 6px BV,sans-serif;fill:#1c2540}svg .nh.s{font-style:normal;font-size:5.5px}svg .nh.i{fill:#c63b2f;font-weight:700}
.foot{position:absolute;left:16mm;right:12mm;bottom:11mm}
.ten{display:grid;grid-template-columns:1fr 34mm;gap:5mm;font-size:3.5mm;margin-bottom:6mm}
.ten div{display:flex;align-items:baseline;gap:2mm;white-space:nowrap}.ten i{flex:1;border-bottom:.3mm dotted #5f6a88}
.brand{display:flex;justify-content:space-between;align-items:baseline;border-top:.5mm solid #1d3a78;padding-top:2.2mm;font-size:3mm;color:#5f6a88}
.brand b{color:#1d3a78;font-size:3.8mm;letter-spacing:.5mm}
.gay{position:absolute;left:0;top:0;bottom:0;width:5mm;background:#1d3a78}
</style></head><body>
<section class="page"><div class="gay"></div>
  <div class="top">
    <div class="nhan"><span>RUỘT TẬP</span><span>HỌC · LUYỆN · SỬA BÀI</span></div>
    <h1 class="mon">VẬT LÍ <b>${Q.lop}</b></h1>
    <div class="hk">HỌC KÌ ${Q.hk}</div>
    <div class="sub">Điện trường và mạch điện một chiều · Bài ${Q.phan[0].bai[0][0]}–${Q.phan.at(-1).bai.at(-1)[0]}</div>
  </div>
  <div class="body">${the}</div>
  <div class="foot">
    <div class="ten"><div>Họ và tên:<i></i></div><div>Lớp:<i></i></div></div>
    <div class="brand"><b>THẠCH LAB</b><span>thachlab.id.vn</span></div>
  </div>
</section></body></html>`;

const OUT = resolve(HERE, 'out'); mkdirSync(OUT, { recursive: true });
const out = `${OUT}/bia-${ma}.pdf`;
writeFileSync(out + '.html', html);
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true, args: ['--no-sandbox', '--allow-file-access-from-files'] });
const p = await b.newPage();
await p.goto(pathToFileURL(out + '.html').href, { waitUntil: 'networkidle0' });
await p.evaluate(chuanHoa);
await p.evaluate('document.fonts.ready');
const du = await p.evaluate(() => Math.round((document.querySelector('.foot').getBoundingClientRect().top - document.querySelector('.body').getBoundingClientRect().bottom) / 3.7795));
await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
await b.close();
console.log(`  bìa ${ma}: ${out} · khoảng trống giữa thẻ và chân ${du} mm${du < 3 ? ' ! CHẬT/TRÀN' : ''}`);
