// Chạy HS ảo tự động cả bài (đi kèm hs-ao-driver.js). Chép cả hai vào public/xem-thu/, ghi mỗi bài một file
// public/xem-thu/btm-<id>.json (cp btm.json sau --xem-thu), mở /dev/btm?f=btm-<id>, nạp 2 script rồi:
//   await ALL([dạng có cong_cu], tổng số dạng)  → chỉ in bước lỗi: sw≠375, OUT (chữ ra ngoài viewBox), HIT (chữ đè), px<10, KHOÁ.
// >45 s thì ALL(...).then(x=>window.OUT=x) rồi đọc window.OUT ở lệnh sau.
window.RUN = async (ds) => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const fm = location.search.match(/f=([\w-]+)/); const data = await (await fetch('/xem-thu/' + (fm ? fm[1] : 'btm') + '.json?' + Date.now())).json();
  const out = [];
  for (const n of ds) {
    const r = { n, steps: [], err: null };
    try {
      document.querySelectorAll('[data-hsao]').forEach((x) => delete x.dataset.hsao);
      if (!(await HSAO.mo(n))) { r.err = 'no .cc-split'; out.push(r); continue; }
      const buoc = data.questions[n - 1].buoc || [];
      for (let i = 1; i <= buoc.length; i++) {
        const root = document.querySelector('.cc-split');
        await HSAO.traLoi(buoc[i - 1]);
        await sleep(300);
        const s = { i, sw: document.documentElement.scrollWidth };
        const svg = root.querySelector('.cc-sticky svg');
        if (svg) {
          const vb = svg.viewBox.baseVal; const ts = [...svg.querySelectorAll('text')].filter((t) => t.getBBox().width > 0 && getComputedStyle(t).opacity !== '0' && getComputedStyle(t).visibility !== 'hidden');
          const bb = ts.map((t) => { const b = t.getBBox(); return { b, t: t.textContent.slice(0, 14) }; });
          s.out = bb.filter(({ b }) => vb.width && (b.x < vb.x - 1 || b.y < vb.y - 1 || b.x + b.width > vb.x + vb.width + 1 || b.y + b.height > vb.y + vb.height + 1)).map((x) => x.t);
          s.hit = [];
          for (let a = 0; a < bb.length; a++) for (let c = a + 1; c < bb.length; c++) { const A = bb[a].b, C = bb[c].b; const ox = Math.min(A.x + A.width, C.x + C.width) - Math.max(A.x, C.x), oy = Math.min(A.y + A.height, C.y + C.height) - Math.max(A.y, C.y); if (ox > 2 && oy > 2) s.hit.push(bb[a].t + '|' + bb[c].t); }
          const fs = ts.map((t) => parseFloat(getComputedStyle(t).fontSize) * (svg.getBoundingClientRect().width / (vb.width || 1)));
          s.minPx = fs.length ? Math.round(Math.min(...fs) * 10) / 10 : null;
        }
        const next = root.querySelector('[aria-label="Bước sau"]');
        s.lock = next ? next.disabled : null;
        if (!s.out?.length) delete s.out; if (!s.hit?.length) delete s.hit;
        r.steps.push(s);
        if (i < buoc.length && next && !next.disabled) { next.click(); await sleep(700); } else if (i < buoc.length) { r.err = 'KHOÁ bước ' + i; break; }
      }
    } catch (e) { r.err = String(e).slice(0, 120); }
    out.push(r);
  }
  window.RES = out; return 'done';
};
window.TOMDE = async (ds) => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const out = [];
  for (const n of ds) {
    const r = { n };
    try {
      await HSAO.mo(n); await sleep(400);
      const root = document.querySelector('.cc-split');
      r.sw0 = document.documentElement.scrollWidth;
      // tự bấm hết các lựa chọn (thử từng nút tới khi bước mở)
      const x = [...root.querySelectorAll('button')].find((b) => /Xem cả lời giải/.test(b.innerText)); if (x) { x.click(); await sleep(600); }
      r.sw1 = document.documentElement.scrollWidth;
      const W = root.getBoundingClientRect().width;
      r.wide = [...root.querySelectorAll('.katex-display, .katex, table, svg')].filter((e) => { const p = e.closest('.katex-display') || e; return e.scrollWidth > (p.parentElement?.clientWidth || W) + 2; }).map((e) => (e.querySelector('annotation')?.textContent || e.tagName).slice(0, 40)).slice(0, 6);
      r.steps = root.querySelectorAll('.bt-step').length;
    } catch (e) { r.err = String(e).slice(0, 120); }
    out.push(r);
  }
  window.RES2 = out; return out;
};
window.ALL = async (hinh, ntot) => {
  await new Promise((r) => setTimeout(r, 1500));
  await RUN(hinh);
  const tom = []; for (let n = 1; n <= ntot; n++) if (!hinh.includes(n)) tom.push(n);
  const t = tom.length ? await TOMDE(tom) : [];
  const bad = [];
  for (const r of RES) {
    if (r.err) bad.push(`D${r.n} ERR ${r.err}`);
    for (const s of r.steps) {
      const p = [];
      if (s.sw !== 375) p.push('sw' + s.sw);
      if (s.out) p.push('OUT[' + s.out.join(',') + ']');
      if (s.hit) p.push('HIT[' + s.hit.join(';') + ']');
      if (s.minPx != null && s.minPx < 10) p.push('px' + s.minPx);
      if (p.length) bad.push(`D${r.n}.b${s.i} ${p.join(' ')}`);
    }
    bad.push(`D${r.n} ok ${r.steps.length}b`);
  }
  for (const r of t) { if (r.err || r.sw0 !== 375 || r.sw1 !== 375 || r.wide?.length) bad.push(`T${r.n} ${r.err || ''} sw${r.sw0}/${r.sw1} wide[${(r.wide || []).join(';')}]`); }
  bad.push('tomde ' + t.map((r) => r.n).join(','));
  return bad.join('\n');
};
